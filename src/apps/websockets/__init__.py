import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# Info, seems like this need to be at the top, also some have src before and others not (maybe due to relationship?)
from adapters.shared.beanie_models_adapter import UserDocument, EnergyDepositDocument, PlanetDocument, EmailDocument, \
    LevelUpRewardClaimsDocument, ResourceExchangeDocument, TokenConversionsDocument, CurrencyMarketOrderDocument, \
    CurrencyMarketTradeDocument

from decouple import config
from beanie import init_beanie
import motor.motor_asyncio
import src.apps.websockets.dependencies as dependencies

app = FastAPI()


@app.on_event("startup")
async def app_init():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        host=config('DB_URL'),
    )

    db = client[config('DB_NAME')]
    await init_beanie(database=db,
                      document_models=[UserDocument,
                                       TokenConversionsDocument,
                                       ResourceExchangeDocument,
                                       EnergyDepositDocument,
                                       PlanetDocument,
                                       EmailDocument,
                                       LevelUpRewardClaimsDocument,
                                       CurrencyMarketOrderDocument,
                                       CurrencyMarketTradeDocument]
    )

    ws_entry_point = await dependencies.ws_entry_point()
    app.add_api_websocket_route(path="/ws", endpoint=ws_entry_point)

if __name__ == "__main__":
    uvicorn.run("__main__:app", port=8011, host='0.0.0.0', reload=True, workers=1, debug=True)