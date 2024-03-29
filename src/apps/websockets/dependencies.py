import datetime
from dataclasses import dataclass
import json

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from starlette.websockets import WebSocketState

from adapters.shared.beani_repository_adapter import (
    BeaniCurrencyMarketOrderRepositoryAdapter,
    BeaniCurrencyMarketTradeRepositoryAdapter,
    BeaniPlanetRepositoryAdapter,
)
from controllers.websockets import WebsocketController
from core.currency_market import CurrencyMarket, TradeRequest
from core.shared.models import AppBaseException, MetadataResponse
from core.shared.ports import ResponsePort


class WebsocketConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message):
        for connection in self.active_connections:
            if connection.client_state == WebSocketState.CONNECTED:
                await connection.send_text(message)

    async def broadcast_except(self, message, websocket: WebSocket):
        for connection in self.active_connections:
            if connection == websocket:
                continue

            if connection.client_state == WebSocketState.CONNECTED:
                await connection.send_text(message)

    async def broadcast_from_list_except(self, message, websockets: list[WebSocket], websocket: WebSocket):
        print("broadcast_from_list_except 0")
        for connection in websockets:
            print("broadcast_from_list_except 1")
            if connection == websocket:
                print("broadcast_from_list_except if")
                continue

            if connection.client_state == WebSocketState.CONNECTED:
                print("broadcast_from_list_except if2")
                await connection.send_text(message)
                print("broadcast_from_list_except if3")



websocket_manager = WebsocketConnectionManager()


@dataclass
class WebsocketResponsePort(ResponsePort):
    async def publish_response(self, response: BaseModel):
        return response


response_port = WebsocketResponsePort()


@dataclass
class WebsocketEntryPoint:
    websocket_manager: WebsocketConnectionManager
    websocket_controller: WebsocketController
    chat_messages: dict[str, list[dict[str, str]]]
    websocket_frequency: dict

    # chat = {
    #     "1.1": [
    #         {"sender": "wallet1", "message": "hello"}
    #     ]
    # }

    async def __call__(self, websocket: WebSocket):
        await self.websocket_manager.connect(websocket)

        # output port sends to user only, not to all
        # here we receive response, and use "broadcast_except" to send all except to this websocket
        try:
            while True:
                data = await websocket.receive_json()
                use_case = data["use_case"]

                if use_case == "ping":
                    await self.websocket_manager.send_personal_message(
                        '{"response_type": "ping", "data": "pong"}', websocket
                    )

                elif use_case == "subscribe_frequency":
                    frequency = data["data"]["frequency"]
                    if frequency not in self.websocket_frequency:
                        self.websocket_frequency[frequency] = []
                    self.websocket_frequency[frequency].append(websocket)

                elif use_case == "emit_frequency":
                    timestamp = datetime.datetime.timestamp(datetime.datetime.now())
                    frequency = data["data"]["frequency"]
                    message = data["data"]["message"]
                    sender = data["data"]["sender"]
                    sender_alias = data["data"]["sender_alias"]

                    if frequency not in self.websocket_frequency:
                        self.websocket_frequency[frequency] = [websocket]

                    if websocket not in self.websocket_frequency[frequency]:
                        self.websocket_frequency[frequency].append(websocket)

                    if frequency not in self.chat_messages:
                        self.chat_messages[frequency] = []

                    msg = {
                        "sender": sender,
                        "sender_alias": sender_alias,
                        "message": message,
                        "frequency": frequency,
                        "timestamp": timestamp
                    }

                    self.chat_messages[frequency].append(msg)
                    await self.websocket_manager.broadcast_from_list_except(json.dumps(msg), self.websocket_frequency[frequency], websocket)

                elif use_case == "receive_full_chat":
                    frequency = data["data"]["frequency"]
                    msgs = {
                        "response_type": "receive_full_chat",
                        "data": []
                    }

                    if frequency in self.chat_messages:
                        msgs["data"] = self.chat_messages[frequency]

                    if frequency not in self.websocket_frequency:
                        self.websocket_frequency[frequency] = [websocket]

                    if websocket not in self.websocket_frequency[frequency]:
                        self.websocket_frequency[frequency].append(websocket)

                    await self.websocket_manager.send_personal_message(json.dumps(msgs), websocket)

                elif use_case == "trade":
                    trade_re = await self.trade(data)
                    fetch_data_ob = (
                        await self.websocket_controller.trade_fetch_order_book_data(
                            data["data"]["market_code"]
                        )
                    )

                    re1 = MetadataResponse(response_type="trade", data=trade_re)
                    re2 = MetadataResponse(
                        response_type="trade_fetch_order_book_data", data=fetch_data_ob
                    )

                    await self.websocket_manager.broadcast(re1.json())
                    await self.websocket_manager.broadcast(re2.json())

                elif use_case == "trade_fetch_order_book_data":
                    fetch_data_ob = (
                        await self.websocket_controller.trade_fetch_order_book_data(
                            data["data"]["market_code"]
                        )
                    )
                    re = MetadataResponse(
                        response_type="trade_fetch_order_book_data", data=fetch_data_ob
                    )
                    await self.websocket_manager.send_personal_message(
                        re.json(), websocket
                    )

                elif use_case == "trade_fetch_current_candle":
                    fetch_data_cc = (
                        await self.websocket_controller.trade_fetch_current_candle(
                            data["data"]["market_code"],
                            data["data"]["candle_time_frame"],
                        )
                    )
                    re3 = MetadataResponse(
                        response_type="trade_fetch_current_candle", data=fetch_data_cc
                    )
                    await self.websocket_manager.send_personal_message(
                        re3.json(), websocket
                    )

                elif use_case == "trade_fetch_historical_data":
                    fetch_data_re = (
                        await self.websocket_controller.trade_fetch_historical_data(
                            data["data"]["market_code"],
                            data["data"]["candle_time_frame"],
                        )
                    )
                    re = MetadataResponse(
                        response_type="trade_fetch_historical_data", data=fetch_data_re
                    )
                    await self.websocket_manager.send_personal_message(
                        re.json(), websocket
                    )
                # else:
                #     # request not found
                #     await self.websocket_manager.send_personal_message('{}', websocket)

        except AppBaseException as ex:
            re = MetadataResponse(response_type="error", data=ex.msg)
            await self.websocket_manager.send_personal_message(re.json(), websocket)

        except WebSocketDisconnect:
            self.websocket_manager.disconnect(websocket)

    async def trade(self, data: dict):
        req: TradeRequest = TradeRequest(
            trade_type=data["data"]["trade_type"],
            user_id=data["data"]["user_id"],
            planet_id=data["data"]["planet_id"],
            order_type=data["data"]["order_type"],
            pair1=data["data"]["pair1"],
            pair2=data["data"]["pair2"],
            price_unit=data["data"]["price"],
            amount=data["data"]["amount"],
            total=data["data"]["total"],
        )

        return await self.websocket_controller.trade(req)


planet_repository = BeaniPlanetRepositoryAdapter()
currency_market_order_repository = BeaniCurrencyMarketOrderRepositoryAdapter()
currency_market_trade_repository = BeaniCurrencyMarketTradeRepositoryAdapter()


async def ws_controller():
    trading_use_case = CurrencyMarket(
        planet_repository,
        currency_market_order_repository,
        currency_market_trade_repository,
        response_port,
    )

    return WebsocketController(trading_use_case)


async def ws_entry_point():
    ws_controller_dependency = await ws_controller()
    return WebsocketEntryPoint(websocket_manager, ws_controller_dependency, {}, {})
