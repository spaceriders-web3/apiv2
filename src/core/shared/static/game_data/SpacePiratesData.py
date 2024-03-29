from dataclasses import dataclass
import random


@dataclass
class SpacePiratesData:
    """
    Data class representing in game items
    """

    LEVELS = ["2-9"]

    SPACE_PIRATES = {
        "2-9": {
            # Amount of spacepirates
            "amount": (2, 3),
            "amount_steal_per_surviving_pirate": (50, 100),
            # Expressed in meters
            "distance": (3500, 8000),
            # Expressed in meters/s
            "speed": (400, 1000),
            "health_per_space_ship": (30, 80),
        }
    }

    @staticmethod
    def get_space_pirate_data_level(planet_level):
        for level in SpacePiratesData.LEVELS:
            lvl_info = level.split("-")
            if int(lvl_info[0]) <= planet_level <= int(lvl_info[1]):
                space_pirate_lvl_info = SpacePiratesData.SPACE_PIRATES[level]

                amount = random.randint(
                    space_pirate_lvl_info["amount"][0],
                    space_pirate_lvl_info["amount"][1],
                )
                distance = random.randint(
                    space_pirate_lvl_info["distance"][0],
                    space_pirate_lvl_info["distance"][1],
                )
                speed = random.randint(
                    space_pirate_lvl_info["speed"][0], space_pirate_lvl_info["speed"][1]
                )

                health = random.randint(
                    space_pirate_lvl_info["health_per_space_ship"][0],
                    space_pirate_lvl_info["health_per_space_ship"][1],
                )

                steal_per_space_ship = random.randint(
                    space_pirate_lvl_info["amount_steal_per_surviving_pirate"][0],
                    space_pirate_lvl_info["amount_steal_per_surviving_pirate"][1],
                )

                return amount, distance, speed, health, steal_per_space_ship

        raise ValueError(f"No space pirate info for level {planet_level}")
