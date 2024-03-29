import json
from pathlib import Path

from decouple import config
import emcache

from adapters.http import HttpResponsePort
from adapters.shared.beani_repository_adapter import (
    BeaniCurrencyMarketOrderRepositoryAdapter,
    BeaniCurrencyMarketTradeRepositoryAdapter,
    BeaniPlanetRepositoryAdapter,
    BeaniUserRepositoryAdapter,
    BKMDepositRepositoryAdapter,
    EmailRepositoryAdapter,
    EnergyDepositRepositoryAdapter, BeaniVoucherRepositoryAdapter,
)
from adapters.shared.cache_adapter import MemCacheCacheServiceAdapter
from adapters.shared.evm_adapter import EvmChainServiceAdapter, TokenPriceAdapter
from adapters.shared.logging_adapter import LoggingAdapter, get_logger
from adapters.shared.medium_parser import MediumContentParser
from controllers.http import HttpController
from core.account import Account
from core.authenticate import Authenticate
from core.buildable_items import BuildableItems
from core.currency_market import CurrencyMarket
from core.favourite_planet import FavouritePlanet
from core.fetch_chain_data import FetchChainData
from core.get_planets import GetPlanets
from core.leaderboard import LeaderBoard
from core.medium_scraper import MediumScraper
from core.mint_planet import MintPlanet
from core.nft_metadata import NftData
from core.planet_bkm import PlanetBKM
from core.planet_email import PlanetEmail
from core.planet_energy import PlanetEnergy
from core.experience_points import ExperiencePoints
from core.planet_resources import PlanetResources
from core.planet_staking import Staking
from core.redeem_voucher import RedeemVoucher
from core.shared.ports import (
    CacheServicePort,
    ChainServicePort,
    EmailRepositoryPort,
    PlanetRepositoryPort,
    TokenPricePort,
    UserRepositoryPort,
)

http_response_port = HttpResponsePort()
logging_adapter = LoggingAdapter(get_logger("http_app"))


async def cache_dependency():
    client = await emcache.create_client(
        node_addresses=[
            emcache.MemcachedHostAddress(
                config("CACHE_HOST"), int(config("CACHE_PORT"))
            )
        ]
    )

    return MemCacheCacheServiceAdapter(client)


async def contract_dependency(cache: CacheServicePort, rpc_urls: str):
    root = Path(__file__).parent.parent.parent
    env = config("ENV")

    path = str(root) + f"/static/contract_addresses/contracts.{env}.json"
    with open(path) as f:
        contract_addresses = json.loads(f.read())
        spaceriders_token_address: str = contract_addresses[
            ChainServicePort.SPACERIDERS_TOKEN_CONTRACT
        ]
        spaceriders_game_address: str = contract_addresses[
            ChainServicePort.SPACERIDERS_GAME_CONTRACT
        ]
        spaceriders_nft_address: str = contract_addresses[
            ChainServicePort.SPACERIDERS_NFT_CONTRACT
        ]
        spaceriders_ticket_nft_address: str = contract_addresses[
            ChainServicePort.SPACERIDERS_TICKET_NFT_CONTRACT
        ]
        router_address: str = contract_addresses[ChainServicePort.ROUTER_CONTRACT]
        busd_address: str = contract_addresses[ChainServicePort.BUSD_CONTRACT]
        pair_address: str = contract_addresses[ChainServicePort.PAIR_CONTRACT]

    abi_base_path = str(root) + "/static/abi"

    with open(f"{abi_base_path}/Spaceriders.json") as f:
        spaceriders_token_abi = json.loads(f.read())

    with open(f"{abi_base_path}/SpaceRidersGame.json") as f:
        spaceriders_game_abi = json.loads(f.read())

    with open(f"{abi_base_path}/SpaceRiderNFT.json") as f:
        spaceriders_nft_abi = json.loads(f.read())

    with open(f"{abi_base_path}/TicketNft.json") as f:
        spaceriders_ticket_nft_abi = json.loads(f.read())

    with open(f"{abi_base_path}/PancakeRouter.json") as f:
        router_abi = json.loads(f.read())

    return EvmChainServiceAdapter(
        cache,
        rpc_urls,
        config("PRIVATE_KEY"),
        spaceriders_token_address,
        spaceriders_game_address,
        spaceriders_nft_address,
        spaceriders_ticket_nft_address,
        router_address,
        busd_address,
        pair_address,
        spaceriders_token_abi,
        spaceriders_game_abi,
        spaceriders_nft_abi,
        spaceriders_ticket_nft_abi,
        router_abi,
    )


async def token_price_dependency(cache: CacheServicePort, contract: ChainServicePort):
    return TokenPriceAdapter(cache, contract)


# Use cases


async def authenticate_use_case(
    user_repo: UserRepositoryPort, chain_service_adapter: ChainServicePort, planet_repo: PlanetRepositoryPort, planet_email: PlanetEmail
):
    return Authenticate(
        config("SECRET_KEY"),
        config("ENV"),
        user_repo,
        chain_service_adapter,
        planet_repo,
        planet_email,
        http_response_port,
    )


async def buy_planet_use_case(
    token_price: TokenPricePort,
    contract: ChainServicePort,
    planet_repository: PlanetRepositoryPort,
):
    return MintPlanet(
        token_price,
        contract,
        config("API_ENDPOINT"),
        config("PLANET_IMAGES_BUCKET_PATH"),
        planet_repository,
        http_response_port,
    )


async def fetch_chain_data_use_case(
    token_price: TokenPricePort, contract: ChainServicePort
):
    return FetchChainData(
        token_price,
        contract,
        config("CHAIN_ID"),
        config("CHAIN_NAME"),
        http_response_port,
    )


async def get_planets_use_case(planet_repository: PlanetRepositoryPort):
    return GetPlanets(
        planet_repository, config("PLANET_IMAGES_BUCKET_PATH"), http_response_port
    )


async def get_buildable_items_use_case(
    planet_repository: PlanetRepositoryPort, lvl_up_use_case: ExperiencePoints
):
    return BuildableItems(planet_repository, lvl_up_use_case, http_response_port)


async def get_planet_resources_use_case(planet_repository: PlanetRepositoryPort):
    return PlanetResources(planet_repository, http_response_port)


async def get_planet_energy_use_case(
    token_price_adapter: TokenPricePort,
    energy_repository: EnergyDepositRepositoryAdapter,
    planet_repository: PlanetRepositoryPort,
    logging_adapter: LoggingAdapter,
    contract: ChainServicePort,
):
    return PlanetEnergy(
        token_price_adapter,
        energy_repository,
        planet_repository,
        logging_adapter,
        contract,
        http_response_port,
    )


async def get_planet_bkm_use_case(
    bkm_repository: BKMDepositRepositoryAdapter,
    planet_repository: PlanetRepositoryPort,
    logging_adapter: LoggingAdapter,
    contract: ChainServicePort,
):
    return PlanetBKM(
        bkm_repository, planet_repository, logging_adapter, contract, http_response_port
    )


async def nft_data_use_case(
    api_endpoint: str,
    planet_images_base_url: str,
    testnet_ticket_images_base_url: str,
    planet_repository_port: PlanetRepositoryPort,
    contract_testnet: ChainServicePort,
):
    return NftData(
        api_endpoint,
        planet_images_base_url,
        testnet_ticket_images_base_url,
        planet_repository_port,
        contract_testnet,
        http_response_port,
    )


async def get_email_use_case(
    planet_repository_port: PlanetRepositoryPort,
    email_repository_port: EmailRepositoryPort,
):
    return PlanetEmail(
        planet_repository_port, email_repository_port, http_response_port
    )


async def get_staking_use_case(
    planet_repository_port: PlanetRepositoryPort,
    token_price: TokenPricePort,
    chain_service_adapter: ChainServicePort,
):
    return Staking(
        planet_repository_port, token_price, chain_service_adapter, http_response_port
    )


async def get_planet_level_use_case(
    planet_repository_port: PlanetRepositoryPort,
    user_repository_port: UserRepositoryPort,
    email_use_case: PlanetEmail,
    chain_service_adapter: ChainServicePort,
):
    return ExperiencePoints(
        planet_repository_port,
        user_repository_port,
        email_use_case,
        chain_service_adapter,
        http_response_port,
    )


async def get_favourite_planet_use_case(
    planet_repository_port: PlanetRepositoryPort,
):
    return FavouritePlanet(
        planet_repository_port,
        http_response_port,
    )


async def get_account_use_case(
    user_repository_port: UserRepositoryPort,
):
    return Account(
        user_repository_port,
        http_response_port,
    )


async def get_leaderboard_use_case(
    planet_repository_port: PlanetRepositoryPort,
    user_repository_port: UserRepositoryPort
):
    return LeaderBoard(
        planet_repository_port,
        user_repository_port,
        config("PLANET_IMAGES_BUCKET_PATH"),
        http_response_port,
    )

async def get_redeem_voucher_use_case(
    planet_repository_port: PlanetRepositoryPort,
    redeem_voucher_port: BeaniVoucherRepositoryAdapter
):
    return RedeemVoucher(redeem_voucher_port, planet_repository_port, http_response_port)
# Controllers


async def get_middleware():
    cache = await cache_dependency()
    contract_service = await contract_dependency(cache, config("RPCS_URL"))
    planet_repository = BeaniPlanetRepositoryAdapter()
    email_repository = EmailRepositoryAdapter()
    user_repository = BeaniUserRepositoryAdapter()

    token_price = await token_price_dependency(cache, contract_service)
    email_use_case = await get_email_use_case(planet_repository, email_repository)

    lvl_up_use_case = await get_planet_level_use_case(
        planet_repository, user_repository, email_use_case, contract_service
    )

    items_use_case = await get_buildable_items_use_case(
        planet_repository, lvl_up_use_case
    )
    planet_resources = await get_planet_resources_use_case(planet_repository)
    planet_staking = await get_staking_use_case(
        planet_repository, token_price, contract_service
    )

    return items_use_case, planet_resources, planet_staking


async def http_controller():
    user_repository = BeaniUserRepositoryAdapter()
    planet_repository = BeaniPlanetRepositoryAdapter()
    energy_repository = EnergyDepositRepositoryAdapter()
    bkm_repository = BKMDepositRepositoryAdapter()
    email_repository = EmailRepositoryAdapter()
    currency_market_order_repository = BeaniCurrencyMarketOrderRepositoryAdapter()
    currency_market_trade_repository = BeaniCurrencyMarketTradeRepositoryAdapter()
    redeem_voucher_repository = BeaniVoucherRepositoryAdapter()

    cache = await cache_dependency()
    contract_service = await contract_dependency(cache, config("RPCS_URL"))
    contract_mainnet_service = await contract_dependency(
        cache, config("RPCS_URL_MAINNET")
    )

    token_price = await token_price_dependency(cache, contract_service)

    email_use_case = await get_email_use_case(planet_repository, email_repository)
    planet_level_use_case = await get_planet_level_use_case(planet_repository, user_repository, email_use_case, contract_service)

    auth_contract_service = contract_service
    if config("ENV") == "testnet":
        auth_contract_service = contract_mainnet_service

    a = await authenticate_use_case(user_repository, auth_contract_service, planet_repository, email_use_case)
    b = await buy_planet_use_case(token_price, contract_service, planet_repository)
    c = await fetch_chain_data_use_case(token_price, contract_service)
    d = await get_planets_use_case(planet_repository)
    e = await get_buildable_items_use_case(planet_repository, planet_level_use_case)
    f = await get_planet_energy_use_case(
        token_price,
        energy_repository,
        planet_repository,
        logging_adapter,
        contract_service,
    )

    nft_contract_service = contract_service
    if config("ENV") == "testnet":
        nft_contract_service = contract_mainnet_service

    g = await nft_data_use_case(
        config("API_ENDPOINT"),
        config("PLANET_IMAGES_BUCKET_PATH"),
        config("TESTNET_TICKET_IMAGES_BUCKET_PATH"),
        planet_repository,
        nft_contract_service,
    )

    j = await get_staking_use_case(planet_repository, token_price, contract_service)

    trading_use_case = CurrencyMarket(
        planet_repository,
        currency_market_order_repository,
        currency_market_trade_repository,
        http_response_port,
    )

    planet_bkm_use_case = await get_planet_bkm_use_case(
        bkm_repository, planet_repository, logging_adapter, contract_service
    )

    medium_scrapper_use_case = MediumScraper(
        config("MEDIUM_ACCOUNT"), MediumContentParser()
    )

    favourite_planet_use_case = await get_favourite_planet_use_case(planet_repository)

    account_use_case = await get_account_use_case(user_repository)

    leaderboard_user_case = await get_leaderboard_use_case(planet_repository, user_repository)

    redeem_voucher_use_case = await get_redeem_voucher_use_case(planet_repository, redeem_voucher_repository)
    return HttpController(
        a,
        b,
        c,
        d,
        e,
        f,
        g,
        email_use_case,
        j,
        trading_use_case,
        planet_bkm_use_case,
        medium_scrapper_use_case,
        favourite_planet_use_case,
        account_use_case,
        leaderboard_user_case,
        redeem_voucher_use_case
    )
