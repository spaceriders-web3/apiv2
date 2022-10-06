from dataclasses import dataclass

from .Common import (
    BuildableItemBaseType,
    BuildableItemLevelInfo,
    BuildableItemRequirement,
)
from .GameData import GameData
from .InstallationData import InstallationData as ID


@dataclass
class ResearchData(GameData):
    """
    Data class representing in game items
    """

    TYPE = "research"

    ASTEROID_PRECISION = "asteroidPrecision"
    TERRAFORMING = "terraforming"
    LASER_RESEARCH = "laserResearch"

    TYPES = [ASTEROID_PRECISION, TERRAFORMING, LASER_RESEARCH]

    __ITEMS = {
        ASTEROID_PRECISION: BuildableItemBaseType(
            "Asteroid Precision",
            ASTEROID_PRECISION,
            TYPE,
            None,
            "For every upgrade increase chance by 1% of hitting an asteroid",
            {
                0: BuildableItemLevelInfo(),
                1: BuildableItemLevelInfo(
                    1,    100,    550,    250,    0,      0,    0,  1200,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 1)], 0,
                ),
                2: BuildableItemLevelInfo(
                    2,    200,    650,    350,    0,      0,    0,  1400,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 2)], 0,
                ),
                3: BuildableItemLevelInfo(
                    3,    300,    750,    450,    0,      0,    0,  1600,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 3)], 0,
                ),
                4: BuildableItemLevelInfo(
                    4,    400,    850,    550,    0,      0,    0,  1800,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 4)], 0,
                ),
                5: BuildableItemLevelInfo(
                    5,    500,    950,    650,    0,      0,    0,  2000,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 5)], 0,
                ),
                6: BuildableItemLevelInfo(
                    6,    600,    1050,   750,    0,      0,    0,  2200,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 6)], 0,
                ),
                7: BuildableItemLevelInfo(
                    7,    700,    1150,   850,    0,      0,    0,  2400,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 7)], 0,
                ),
                8: BuildableItemLevelInfo(
                    8,    800,    1250,   950,    0,      0,    0,  2600,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 8)], 0,
                ),
                9: BuildableItemLevelInfo(
                    9,    900,    1350,   1050,   0,      0,    0,  2800,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 9)], 0,
                ),
                10: BuildableItemLevelInfo(
                    10,   1000,   1450,   1150,   0,      0,    0,  3000,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 10)], 0,
                ),
            },
        ),
        TERRAFORMING: BuildableItemBaseType(
            "Terraforming",
            TERRAFORMING,
            TYPE,
            None,
            "For Every upgrade get 1 additional slot on your planet.",
            {
                0: BuildableItemLevelInfo(),
                1: BuildableItemLevelInfo(
                    1,    500,     500,      500,    0,      0,    0,  2000,   0,      0,  20,     [
                        BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 2)], 0,
                ),
                2: BuildableItemLevelInfo(
                    2,    1000,    800,      600,    0,      0,    0,  3000,   0,      0,  30,     [
                        BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 4)], 0,
                ),
                3: BuildableItemLevelInfo(
                    3,    2000,    1100,      700,    0,      0,    0,  4000,   0,      0,  40,     [
                        BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 6)], 0,
                ),
                4: BuildableItemLevelInfo(
                    4,    3000,    1400,      800,    0,      0,    0,  5000,   0,      0,  50,     [
                        BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 8)], 0,
                ),
                5: BuildableItemLevelInfo(
                    5,    4000,    1700,      900,    0,      0,    0,  6000,   0,      0,  60,     [
                        BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 10)], 0,
                ),
            },
        ),
        LASER_RESEARCH: BuildableItemBaseType(
            "Laser Research",
            LASER_RESEARCH,
            TYPE,
            None,
            "Research in how to implement/improve laser technology in using laser for military approach.",
            {
                0: BuildableItemLevelInfo(),
                1: BuildableItemLevelInfo(
                    1,    100,    350,    550,    0,      0,    0,  1200,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 1)], 0,
                ),
                2: BuildableItemLevelInfo(
                    2,    200,    450,    650,    0,      0,    0,  1400,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 2)], 0,
                ),
                3: BuildableItemLevelInfo(
                    3,    300,    550,    750,    0,      0,    0,  1600,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 3)], 0,
                ),
                4: BuildableItemLevelInfo(
                    4,    400,    650,    850,    0,      0,    0,  1800,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 4)], 0,
                ),
                5: BuildableItemLevelInfo(
                    5,    500,    750,    950,    0,      0,    0,  2000,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 5)], 0,
                ),
                6: BuildableItemLevelInfo(
                    6,    600,    850,   1050,    0,      0,    0,  2200,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 6)], 0,
                ),
                7: BuildableItemLevelInfo(
                    7,    700,    950,   1150,    0,      0,    0,  2400,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 7)], 0,
                ),
                8: BuildableItemLevelInfo(
                    8,    800,    1050,   1250,    0,      0,    0,  2600,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 8)], 0,
                ),
                9: BuildableItemLevelInfo(
                    9,    900,    1150,   1350,   0,      0,    0,  2800,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 9)], 0,
                ),
                10: BuildableItemLevelInfo(
                    10,   1000,   1250,   1450,   0,      0,    0,  3000,   0,      0,  10,
                    [BuildableItemRequirement(ID.TYPE, ID.INVESTIGATION_LABORATORY, 10)], 0,
                ),
            },
        ),
    }

    @staticmethod
    def valid_type(label: str) -> bool:
        return label in ResearchData.TYPES

    @staticmethod
    def get_type() -> str:
        return ResearchData.TYPE

    @staticmethod
    def get_item(key: str) -> BuildableItemBaseType:
        if key not in ResearchData.TYPES:
            raise ValueError(
                f"{key} not in {ResearchData.TYPES} for {ResearchData.TYPE}"
            )

        return ResearchData.__ITEMS[key]
