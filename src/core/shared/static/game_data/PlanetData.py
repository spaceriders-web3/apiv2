from dataclasses import dataclass

from .Common import CommonKeys as CK


@dataclass
class PlanetData:
    BUY_PLANET_COST_USD = 15

    POISON = "poison"
    WATER = "water"
    FIRE = "fire"
    GAS = "gas"
    SAND = "sand"

    PlANET_TYPES = [POISON, GAS, WATER, SAND, FIRE]
    PLANET_TYPE_WEIGHTS = (44, 30, 17, 7, 2)
    PLANET_TYPE_IMAGE_MAPPING = {
        POISON: 1,
        WATER: 2,
        FIRE: 3,
        GAS: 4,
        SAND: 5,
    }

    UNCOMMON = "uncommon"
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

    RARITIES = [COMMON, UNCOMMON, RARE, EPIC, LEGENDARY]
    RARITY_WEIGHTS = (56, 30, 10, 3, 1)

    DATA = {
        COMMON: {                                                                                                                                   
            POISON: {
                CK.DIAMETER: {
                    CK.RANGE: (180000, 200000),
                },
                CK.RESERVES: {
                    CK.METAL: (9000000, 11000000),
                    CK.CRYSTAL: (2571429, 3142857),
                    CK.PETROL: (159011, 194346),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 875,
                    CK.PETROL: 177,
                    CK.CRYSTAL: 429,
                    CK.ENERGY: 500,
                },
            },

            WATER: {
                CK.DIAMETER: {
                    CK.RANGE: (180000, 200000),
                },
                CK.RESERVES: {
                    CK.METAL: (4500000, 5500000),
                    CK.CRYSTAL: (5142857, 6285714),
                    CK.PETROL: (159011, 194346),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 750,
                    CK.PETROL: 177,
                    CK.CRYSTAL: 500,
                    CK.ENERGY: 500,
                },
            },

            FIRE: {
                CK.DIAMETER: {
                    CK.RANGE: (180000, 200000),
                },
                CK.RESERVES: {
                    CK.METAL: (4500000, 5500000),
                    CK.CRYSTAL: (257143, 314286),
                    CK.PETROL: (3180212, 3886926),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 750,
                    CK.PETROL: 309,
                    CK.CRYSTAL: 286,
                    CK.ENERGY: 500,
                },
            },

            GAS: {
                CK.DIAMETER: {
                    CK.RANGE: (180000, 200000),
                },
                CK.RESERVES: {
                    CK.METAL: (9000000, 11000000),
                    CK.CRYSTAL: (257143, 314286),
                    CK.PETROL: (1590106, 1943463),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 875,
                    CK.PETROL: 265,
                    CK.CRYSTAL: 286,
                    CK.ENERGY: 500,
                },
            },

            SAND: {
                CK.DIAMETER: {
                    CK.RANGE: (180000, 200000),
                },
                CK.RESERVES: {
                    CK.METAL: (450000, 550000),
                    CK.CRYSTAL: (5142857, 6285714),
                    CK.PETROL: (1590106, 1943463),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 500,
                    CK.PETROL: 265,
                    CK.CRYSTAL: 500,
                    CK.ENERGY: 500,
                },
            },
        },
        UNCOMMON: {
            POISON: {
                CK.DIAMETER: {
                    CK.RANGE: (200000, 230000),
                },
                CK.RESERVES: {
                    CK.METAL: (9450000, 11550000),
                    CK.CRYSTAL: (2700000, 3300000),
                    CK.PETROL: (166961, 204064),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 919,
                    CK.PETROL: 186,
                    CK.CRYSTAL: 450,
                    CK.ENERGY: 750,
                },
            },
            WATER: {
                CK.DIAMETER: {
                    CK.RANGE: (200000, 230000),
                },
                CK.RESERVES: {
                    CK.METAL: (4725000, 5775000),
                    CK.CRYSTAL: (5400000, 6600000),
                    CK.PETROL: (166961, 204064),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 788,
                    CK.PETROL: 186,
                    CK.CRYSTAL: 525,
                    CK.ENERGY: 750,
                },
            },
            FIRE: {
                CK.DIAMETER: {
                    CK.RANGE: (200000, 230000),
                },
                CK.RESERVES: {
                    CK.METAL: (4725000, 5775000),
                    CK.CRYSTAL: (270000, 330000),
                    CK.PETROL: (3339223, 4081272),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 788,
                    CK.PETROL: 325,
                    CK.CRYSTAL: 300,
                    CK.ENERGY: 750,
                },
            },
            GAS: {
                CK.DIAMETER: {
                    CK.RANGE: (200000, 230000),
                },
                CK.RESERVES: {
                    CK.METAL: (9450000, 11550000),
                    CK.CRYSTAL: (270000, 330000),
                    CK.PETROL: (1669611, 2040636),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 919,
                    CK.PETROL: 278,
                    CK.CRYSTAL: 300,
                    CK.ENERGY: 750,
                },
            },
            SAND: {
                CK.DIAMETER: {
                    CK.RANGE: (200000, 230000),
                },
                CK.RESERVES: {
                    CK.METAL: (472500, 577500),
                    CK.CRYSTAL: (5400000, 6600000),
                    CK.PETROL: (1669611, 2040636),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 525,
                    CK.PETROL: 278,
                    CK.CRYSTAL: 525,
                    CK.ENERGY: 750,
                },
            },

        },
        RARE: {
            POISON: {
                CK.DIAMETER: {
                    CK.RANGE: (230000, 260000),
                },
                CK.RESERVES: {
                    CK.METAL: (10350000, 12650000),
                    CK.CRYSTAL: (2957143, 3614286),
                    CK.PETROL: (182862, 223498),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 1006,
                    CK.PETROL: 203,
                    CK.CRYSTAL: 493,
                    CK.ENERGY: 1000,
                },
            },
            WATER: {
                CK.DIAMETER: {
                    CK.RANGE: (230000, 260000),
                },
                CK.RESERVES: {
                    CK.METAL: (5175000, 6325000),
                    CK.CRYSTAL: (5914286, 7228571),
                    CK.PETROL: (182862, 223498),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 863,
                    CK.PETROL: 203,
                    CK.CRYSTAL: 575,
                    CK.ENERGY: 1000,
                },
            },
            FIRE: {
                CK.DIAMETER: {
                    CK.RANGE: (230000, 260000),
                },
                CK.RESERVES: {
                    CK.METAL: (5175000, 6325000),
                    CK.CRYSTAL: (295714, 361429),
                    CK.PETROL: (3657244, 4469965),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 863,
                    CK.PETROL: 356,
                    CK.CRYSTAL: 329,
                    CK.ENERGY: 1000,
                },
            },
            GAS: {
                CK.DIAMETER: {
                    CK.RANGE: (230000, 260000),
                },
                CK.RESERVES: {
                    CK.METAL: (10350000, 12650000),
                    CK.CRYSTAL: (295714, 361429),
                    CK.PETROL: (1828622, 2234982),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 1006,
                    CK.PETROL: 305,
                    CK.CRYSTAL: 329,
                    CK.ENERGY: 1000,
                },
            },
            SAND: {
                CK.DIAMETER: {
                    CK.RANGE: (230000, 260000),
                },
                CK.RESERVES: {
                    CK.METAL: (517500, 632500),
                    CK.CRYSTAL: (5914286, 7228571),
                    CK.PETROL: (1828622, 2234982),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 575,
                    CK.PETROL: 305,
                    CK.CRYSTAL: 575,
                    CK.ENERGY: 1000,
                },
            },


        },
        EPIC: {
            POISON: {
                CK.DIAMETER: {
                    CK.RANGE: (260000, 300000),
                },
                CK.RESERVES: {
                    CK.METAL: (11700000, 14300000),
                    CK.CRYSTAL: (3342857, 4085714),
                    CK.PETROL: (206714, 252650),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 1138,
                    CK.PETROL: 230,
                    CK.CRYSTAL: 557,
                    CK.ENERGY: 1250,
                },
            },
            WATER: {
                CK.DIAMETER: {
                    CK.RANGE: (260000, 300000),
                },
                CK.RESERVES: {
                    CK.METAL: (5850000, 7150000),
                    CK.CRYSTAL: (6685714, 8171429),
                    CK.PETROL: (206714, 252650),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 975,
                    CK.PETROL: 230,
                    CK.CRYSTAL: 650,
                    CK.ENERGY: 1250,
                },
            },
            FIRE: {
                CK.DIAMETER: {
                    CK.RANGE: (260000, 300000),
                },
                CK.RESERVES: {
                    CK.METAL: (5850000, 7150000),
                    CK.CRYSTAL: (334286, 408571),
                    CK.PETROL: (4134276, 5053004),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 975,
                    CK.PETROL: 402,
                    CK.CRYSTAL: 371,
                    CK.ENERGY: 1250,
                },
            },
            GAS: {
                CK.DIAMETER: {
                    CK.RANGE: (260000, 300000),
                },
                CK.RESERVES: {
                    CK.METAL: (11700000, 14300000),
                    CK.CRYSTAL: (334286, 408571),
                    CK.PETROL: (2067138, 2526502),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 1138,
                    CK.PETROL: 345,
                    CK.CRYSTAL: 371,
                    CK.ENERGY: 1250,
                },
            },
            SAND: {
                CK.DIAMETER: {
                    CK.RANGE: (260000, 300000),
                },
                CK.RESERVES: {
                    CK.METAL: (585000, 715000),
                    CK.CRYSTAL: (6685714, 8171429),
                    CK.PETROL: (2067138, 2526502),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 650,
                    CK.PETROL: 345,
                    CK.CRYSTAL: 650,
                    CK.ENERGY: 1250,
                },
            },
        },
        LEGENDARY: {
            POISON: {
                CK.DIAMETER: {
                    CK.RANGE: (300000, 330000),
                },
                CK.RESERVES: {
                    CK.METAL: (13500000, 16500000),
                    CK.CRYSTAL: (3857143, 4714286),
                    CK.PETROL: (238516, 291519),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 1313,
                    CK.PETROL: 265,
                    CK.CRYSTAL: 643,
                    CK.ENERGY: 1500,
                },
            },
            WATER: {
                CK.DIAMETER: {
                    CK.RANGE: (300000, 330000),
                },
                CK.RESERVES: {
                    CK.METAL: (6750000, 8250000),
                    CK.CRYSTAL: (7714286, 9428571),
                    CK.PETROL: (238516, 291519),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 1125,
                    CK.PETROL: 265,
                    CK.CRYSTAL: 750,
                    CK.ENERGY: 1500,
                },
            },
            FIRE: {
                CK.DIAMETER: {
                    CK.RANGE: (300000, 330000),
                },
                CK.RESERVES: {
                    CK.METAL: (6750000, 8250000),
                    CK.CRYSTAL: (385714, 471429),
                    CK.PETROL: (4770318, 5830389),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 1125,
                    CK.PETROL: 464,
                    CK.CRYSTAL: 429,
                    CK.ENERGY: 1500,
                },
            },
            GAS: {
                CK.DIAMETER: {
                    CK.RANGE: (300000, 330000),
                },
                CK.RESERVES: {
                    CK.METAL: (13500000, 16500000),
                    CK.CRYSTAL: (385714, 471429),
                    CK.PETROL: (2385159, 2915194),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 1313,
                    CK.PETROL: 398,
                    CK.CRYSTAL: 429,
                    CK.ENERGY: 1500,
                },
            },
            SAND: {
                CK.DIAMETER: {
                    CK.RANGE: (300000, 330000),
                },
                CK.RESERVES: {
                    CK.METAL: (675000, 825000),
                    CK.CRYSTAL: (7714286, 9428571),
                    CK.PETROL: (2385159, 2915194),
                },
                CK.INITIAL_RESERVE: {
                    CK.METAL: 750,
                    CK.PETROL: 398,
                    CK.CRYSTAL: 750,
                    CK.ENERGY: 1500,
                },
            },
        }
    }
