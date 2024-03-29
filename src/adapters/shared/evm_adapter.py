import concurrent.futures
from dataclasses import dataclass
import hashlib
import time

from eth_account.messages import encode_defunct
from web3 import Web3

from core.shared.ports import (
    CacheServicePort,
    ChainServicePort,
    SignedMessageDict,
    TokenPricePort,
)


@dataclass
class EvmChainServiceAdapter(ChainServicePort):
    cache: CacheServicePort
    rpc_urls: str
    private_key: str

    spaceriders_token_address: str
    spaceriders_game_address: str
    spaceriders_nft_address: str
    spaceriders_ticket_nft_address: str
    router_address: str
    busd_address: str
    pair_address: str

    spaceriders_token_abi: str
    spaceriders_game_abi: str
    spaceriders_nft_abi: str
    spaceriders_ticket_nft_abi: str
    router_abi: str

    async def to_wei(self, amount: float) -> int:
        return Web3.toWei(amount, "ether")

    async def get_contract_address(self, contract_name: str) -> str:
        if contract_name == ChainServicePort.SPACERIDERS_TOKEN_CONTRACT:
            return self.spaceriders_token_address

        if contract_name == ChainServicePort.SPACERIDERS_GAME_CONTRACT:
            return self.spaceriders_game_address

        if contract_name == ChainServicePort.SPACERIDERS_NFT_CONTRACT:
            return self.spaceriders_nft_address

        if contract_name == ChainServicePort.SPACERIDERS_TICKET_NFT_CONTRACT:
            return self.spaceriders_ticket_nft_address

        if contract_name == ChainServicePort.ROUTER_CONTRACT:
            return self.router_address

        if contract_name == ChainServicePort.BUSD_CONTRACT:
            return self.busd_address

        if contract_name == ChainServicePort.PAIR_CONTRACT:
            return self.pair_address

    async def get_rpc_url(self):
        faster_rpc = await self.cache.get(CacheServicePort.FASTEST_RPC)

        if not faster_rpc:
            faster_rpc = self.rpc_urls.split(",")[0]

        return faster_rpc

    def __contract_call(self, url, contract_address, abi_file, func_name, args):
        contract_instance = Web3(Web3.HTTPProvider(url)).eth.contract(
            address=contract_address, abi=abi_file
        )
        contract = contract_instance.functions

        start = time.time()
        error = False
        re = False
        try:
            if func_name not in ["address"]:
                func = getattr(contract, func_name)(*args)
                re = func.call()
            else:
                re = getattr(contract, "address")
        except Exception as e:
            error = True

        end = time.time()

        return {"start": start, "end": end, "rpc": url, "error": error, "re": re}

    async def __contract_multi_rpc_call(
        self, contract_address, abi_file, func_name, args
    ):
        key_str = f"{contract_address}{func_name}{''.join(map(str, args))}"
        key = hashlib.md5(key_str.encode("utf-8")).hexdigest()

        multi_call_result = await self.cache.get(key)

        if multi_call_result is None:
            rpc_urls = self.rpc_urls.split(",")
            with concurrent.futures.ThreadPoolExecutor(5) as executor:
                results = []
                for url in rpc_urls:
                    results.append(
                        executor.submit(
                            self.__contract_call,
                            url,
                            contract_address,
                            abi_file,
                            func_name,
                            args,
                        )
                    )

                done, not_done = concurrent.futures.wait(
                    results, return_when=concurrent.futures.FIRST_COMPLETED
                )
                multi_call_result = (done.pop()).result()

                while multi_call_result["error"] and len(not_done) > 0:
                    done, not_done = concurrent.futures.wait(
                        not_done, return_when=concurrent.futures.FIRST_COMPLETED
                    )
                    multi_call_result = (done.pop()).result()

                await self.cache.set(key, multi_call_result, 120)

            if not await self.cache.get(CacheServicePort.FASTEST_RPC):
                await self.cache.set(
                    CacheServicePort.FASTEST_RPC, multi_call_result["rpc"], 60
                )

        return multi_call_result["re"]

    def __to_32byte_hex(self, val):
        return Web3.toHex(Web3.toBytes(val).rjust(32, b"\0"))

    async def sign_message(self, types: list, values: list) -> SignedMessageDict:
        rpc_url = self.rpc_urls.split(",")[0]
        w3 = Web3(Web3.HTTPProvider(rpc_url))

        h = encode_defunct(Web3.solidityKeccak(types, values))

        sm = w3.eth.account.sign_message(h, private_key=self.private_key)
        return {
            "v": sm.v,
            "r": self.__to_32byte_hex(sm.r),
            "s": self.__to_32byte_hex(sm.s),
        }

    async def spaceriders_token_call(self, func_name, *args):
        return await self.__contract_multi_rpc_call(
            self.spaceriders_token_address, self.spaceriders_token_abi, func_name, args
        )

    async def router_call(self, func_name, *args):
        return await self.__contract_multi_rpc_call(
            self.router_address, self.router_abi, func_name, args
        )

    async def spaceriders_nft_call(self, func_name, *args):
        return await self.__contract_multi_rpc_call(
            self.spaceriders_nft_address, self.spaceriders_nft_abi, func_name, args
        )

    async def spaceriders_game_call(self, func_name, *args):
        return await self.__contract_multi_rpc_call(
            self.spaceriders_game_address, self.spaceriders_game_abi, func_name, args
        )

    async def spaceriders_ticket_nft_call(self, func_name, *args):
        return await self.__contract_multi_rpc_call(
            self.spaceriders_ticket_nft_address,
            self.spaceriders_ticket_nft_abi,
            func_name,
            args,
        )


@dataclass
class TokenPriceAdapter(TokenPricePort):
    cache: CacheServicePort
    contract_service: ChainServicePort

    async def fetch_token_price_usd(self) -> float:
        re = await self.cache.get("TOKEN_PRICE")
        if re is not None:
            return re

        spaceriders_address = await self.contract_service.get_contract_address(
            ChainServicePort.SPACERIDERS_TOKEN_CONTRACT
        )
        busd_address = await self.contract_service.get_contract_address(
            ChainServicePort.BUSD_CONTRACT
        )

        path = [spaceriders_address, busd_address]

        price = await self.contract_service.router_call("getAmountsOut", 10**18, path)
        price = price[1]

        try:
            price /= 10**18
        except:
            price = -1

        await self.cache.set("TOKEN_PRICE", price, 60)
        return price
