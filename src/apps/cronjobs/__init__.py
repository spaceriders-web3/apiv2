# https://schedule.readthedocs.io/en/stable/parallel-execution.html
# stuff like cronjobs like planet imports, building queues etc t oremove some burden from api
from beanie import init_beanie
from decouple import config
import motor.motor_asyncio
import asyncio
import aioschedule as schedule
import apps.cronjobs.dependencies as dependencies
from adapters.shared.beani_repository_adapter import UserDocument, PlanetDocument, EnergyDepositDocument
from adapters.shared.beanie_models_adapter import EmailDocument, LevelUpRewardClaimsDocument, ResourceExchangeDocument, \
    TokenConversionsDocument
from controllers.cronjobs import CronjobController
from core.planet_energy import PlanetEnergyRecoverEnergyDepositsRequest
from core.shared.models import Planet
import apps.cronjobs.settings as settings


async def asteroid(controller: CronjobController):
    all_claimed: list[Planet] = await dependencies.planet_repository.all_claimed_planets()
    for planet in all_claimed:
        await controller.asteroid_pve(str(planet.id))


async def smart_contract_recover_by_user_cronjob(controller: CronjobController):
    all_users = await dependencies.user_repository.all()
    for user in all_users:
        await controller.recover_planets(user.wallet)


async def smart_contract_recover_by_planet_cronjob(controller: CronjobController):
    all_claimed: list[Planet] = await dependencies.planet_repository.all_claimed_planets()
    for planet in all_claimed:
        request = PlanetEnergyRecoverEnergyDepositsRequest(planet_id=str(planet.id))
        await controller.recover_deposits(request)
        await controller.recover_staking(str(planet.id))
        await controller.recover_level_up(str(planet.id))


# @TODO: add emails when something got imported
async def main():
    await dependencies.logging_adapter.info("App started")
    client = motor.motor_asyncio.AsyncIOMotorClient(config("DB_URL"), )
    db = client[config('DB_NAME')]

    await init_beanie(database=db, document_models=[UserDocument, TokenConversionsDocument, ResourceExchangeDocument, EnergyDepositDocument,
                       PlanetDocument, EmailDocument, LevelUpRewardClaimsDocument])

    controller = await dependencies.cronjob_controller()

    # If this is not here in main function it won't work (also below model initialization)
    schedule.every(30).seconds.do(smart_contract_recover_by_planet_cronjob, controller)
    schedule.every(30).seconds.do(smart_contract_recover_by_user_cronjob, controller)
    schedule.every(6).hours.do(controller.generate_new_resource_price)
    schedule.every(12).hours.do(asteroid, controller)

    print("Starting cronjobs")
    while True:
        await schedule.run_pending()
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())

