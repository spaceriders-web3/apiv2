import math
import random

from core.shared.models import BuildableItem, Planet, Reserves
from core.shared.ports import PlanetRepositoryPort
from core.shared.static.game_data.Common import (
    BuildableItemBaseType,
    BuildableItemLevelInfo, CommonKeys as CK,
)
from core.shared.static.game_data.DefenseData import DefenseData
from core.shared.static.game_data.InstallationData import InstallationData
from core.shared.static.game_data.PlanetData import PlanetData
from core.shared.static.game_data.ResearchData import ResearchData
from core.shared.static.game_data.ResourceData import ResourceData


async def get_new_planet(
    user: str,
    name: str,
    planet_repository_port: PlanetRepositoryPort,
    price_paid: int,
    planet_images_bucket_path: str,
    claimed: bool,
    claimable: int = None,
) -> Planet:
    galaxy, solar_system, position = await get_new_random_planet_planet_position(
        planet_repository_port
    )

    resource_levels, installation_level, research_level, defense_items = create_planet_levels()

    (
        initial_reserve,
        image,
        rarity,
        diameter,
        slots,
        metal_mine_amount,
        crystal_mine_amount,
        petrol_mine_amount,
        min_temperature,
        max_temperature,
        planet_type,
    ) = get_planet_data()

    planet = Planet(
        user=user,
        price_paid=price_paid,
        name=name,
        rarity=rarity,
        resources_level=resource_levels,
        installation_level=installation_level,
        research_level=research_level,
        defense_items=defense_items,
        type=planet_type
    )

    planet.reserves = Reserves()
    planet.position = position
    planet.solar_system = solar_system
    planet.galaxy = galaxy
    planet.resources.metal = initial_reserve["metal"]
    planet.resources.petrol = initial_reserve["petrol"]
    planet.resources.crystal = initial_reserve["crystal"]
    planet.resources.energy = initial_reserve["energy"]
    planet.resources.bkm = 0
    planet.image = image
    planet.set_image_url(planet_images_bucket_path)
    planet.diameter = diameter
    planet.slots = slots
    planet.slots_used = 0
    planet.min_temperature = min_temperature
    planet.max_temperature = max_temperature

    planet.reserves.total_metal = metal_mine_amount
    planet.reserves.total_crystal = crystal_mine_amount
    planet.reserves.total_petrol = petrol_mine_amount

    planet.claimed = claimed
    planet.claimable = claimable

    return planet


async def get_new_random_planet_planet_position(
    planet_repository_port: PlanetRepositoryPort,
) -> tuple[int, int, int]:
    galaxy = 0
    solar_system = 0
    free_planet_positions = []

    while True:

        planets_range_occupied = (
            await planet_repository_port.occupied_positions_by_range(
                galaxy, solar_system, solar_system + 7
            )
        )

        # [from solar system, to solar system at >= aprox. 80%  capacity]
        if len(planets_range_occupied) >= 70:
            solar_system += 7
            if solar_system + 7 >= 100:
                solar_system = 0
                galaxy += 1
            continue

        for y in range(solar_system, solar_system + 7):
            for x in range(1, 13):
                pos = f"{galaxy}:{y}:{x}"
                if pos not in planets_range_occupied:
                    free_planet_positions.append(pos)

        break

    random.shuffle(free_planet_positions)
    planet_pos = random.randrange(len(free_planet_positions))

    galaxy, solar_system, position = map(
        int, free_planet_positions[planet_pos].split(":")
    )
    return galaxy, solar_system, position


def get_planet_data():
    rarity = random.choices(
        PlanetData.RARITIES, weights=PlanetData.RARITY_WEIGHTS, k=1
    )[0]

    planet_type = random.choices(
        PlanetData.PlANET_TYPES, weights=PlanetData.PLANET_TYPE_WEIGHTS, k=1
    )[0]

    planet_image = random.randrange(1, PlanetData.PLANET_IMAGES_AMOUNT_PER_TYPE_RARITY+1)
    planet_level_data = PlanetData.DATA[rarity][planet_type]

    diameter_range = planet_level_data[CK.DIAMETER][CK.RANGE]
    diameter = random.randint(diameter_range[0], diameter_range[1])
    slots = math.floor(diameter / 1000)

    metal_reserve_range = planet_level_data[CK.RESERVES][CK.METAL]
    crystal_reserve_range = planet_level_data[CK.RESERVES][CK.CRYSTAL]
    petrol_reserve_range = planet_level_data[CK.RESERVES][CK.PETROL]

    metal_mine_amount = random.randint(metal_reserve_range[0], metal_reserve_range[1])
    crystal_mine_amount = random.randint(crystal_reserve_range[0], crystal_reserve_range[1])
    petrol_mine_amount = random.randint(petrol_reserve_range[0], petrol_reserve_range[1])

    # @TODO: calculate based on distance to sun
    min_temperature = random.randint(-60, 0)
    max_temperature = random.randint(1, 150)

    return (
        planet_level_data[CK.INITIAL_RESERVE],
        planet_image,
        rarity,
        diameter,
        slots,
        metal_mine_amount,
        crystal_mine_amount,
        petrol_mine_amount,
        min_temperature,
        max_temperature,
        planet_type,
    )


def create_planet_levels() -> tuple:
    resource_levels = []
    installation_level = []
    research_level = []
    defense_items = []

    for resource_data in ResourceData.TYPES:
        item: BuildableItemBaseType = ResourceData.get_item(resource_data)
        level_info: BuildableItemLevelInfo = item.get_level_info()

        rl = BuildableItem(
            label=item.label,
            type=ResourceData.TYPE,
            current_level=0,
            health=level_info.health,
        )
        resource_levels.append(rl)

    for installation_type in InstallationData.TYPES:
        item: BuildableItemBaseType = InstallationData.get_item(installation_type)
        il = BuildableItem(
            label=item.label, type=InstallationData.TYPE, current_level=0
        )
        installation_level.append(il)

    for research_type in ResearchData.TYPES:
        item: BuildableItemBaseType = ResearchData.get_item(research_type)
        rl = BuildableItem(label=item.label, type=ResearchData.TYPE, current_level=0)
        research_level.append(rl)

    for defense_item in DefenseData.TYPES:
        di = BuildableItem(label=defense_item, type=DefenseData.TYPE, quantity=0)
        defense_items.append(di)

    return resource_levels, installation_level, research_level, defense_items
