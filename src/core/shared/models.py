from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, root_validator

from core.shared.service.tier_benefit import tier_benefit_buildable_items
from core.shared.static.game_data.Common import (
    BuildableItemBaseType,
    BuildableItemLevelInfo,
)
from core.shared.static.game_data.DefenseData import DefenseData as DD
from core.shared.static.game_data.InstallationData import InstallationData as ID
from core.shared.static.game_data.PlanetLevelData import PlanetLevelData
from core.shared.static.game_data.ResearchData import ResearchData as RE
from core.shared.static.game_data.ResourceData import ResourceData
from core.shared.static.game_data.ResourceData import ResourceData as RD
from core.shared.static.game_data.StakingData import StakingData as SD


class AppBaseException(Exception):
    msg: str
    code = 400


class ShadyActivityException(AppBaseException):
    msg = "This looks suspicious to me, what are you trying boi?"


class UserNotFoundException(AppBaseException):
    msg = "Provided user was not found"
    code = 401


class PlanetNameMissingException(AppBaseException):
    msg = "Please choose a name for your planet"


class PlanetIdAlreadyExistsException(AppBaseException):
    msg = "Provided planet id already exists"


class NotMyPlanetException(AppBaseException):
    msg = "This planet belongs to other user..."


class NoPlanetFoundException(AppBaseException):
    msg = "No planet with this id found..."
    code = 404


class QueueIsFullException(AppBaseException):
    msg = "Can't upgrade/repair, queue is full..."


class User(BaseModel):
    id: str = None
    wallet: str = None
    username: str = ""
    planets: list["Planet"] = []
    level: int = None
    experience: int = None
    last_login: int = None

    daily_login_next_reward_timer: int = None
    daily_login_streak: int = None

    def exists(self):
        return self.id is not None


class PlanetTier(BaseModel):
    tier_code: str = SD.TIER_0
    tier_name: str = SD.TIER_NAMES[SD.TIER_0]
    token_amount: float = 0
    time_release: float | None = None
    staked: bool = False


class BuildableItemState(Enum):
    BUILDING = "BUILDING"
    REPAIRING = "REPAIRING"
    FINISHED = "FINISHED"


class BuildableItem(BaseModel):
    label: str
    type: str
    current_level: int = 0
    building: bool = False
    finish: float = None

    repairing: bool = False
    health: int = -1

    quantity: int = -1
    quantity_building: int = -1
    state: BuildableItemState = BuildableItemState.FINISHED


class Resources(BaseModel):
    metal: float = None
    crystal: float = None
    petrol: float = None
    energy: float = None
    bkm: float = None

    metal_last_updated: float = None
    crystal_last_updated: float = None
    petrol_last_updated: float = None

    energy_usage: float = 0


class Reserves(BaseModel):
    # Total resources reserve left
    total_metal: float = 0
    total_crystal: float = 0
    total_petrol: float = 0


class EnergyDeposit(BaseModel):
    created_time: float = None
    energy_amount: float = None
    planet_id: str


class BKMTransaction(BaseModel):
    request_id: str
    created_time: float = None
    token_amount: float = None
    planet_id: str
    was_recovered = False
    type: str


class Email(BaseModel):
    id: str = None
    title: str = None
    sub_title: str = None
    template: str = None
    body: str = None
    sender: str = None
    read: bool = False
    planet: str = None
    topic: str = None


class BuildingQueueItem(BaseModel):
    label: str
    type: str
    action: BuildableItemState
    next_level: Optional[int]
    quantity: Optional[int]
    time_to_finish: float | int  # in seconds
    start_at: float | int  # timestamp


class BuildingQueue(BaseModel):
    items: list[BuildingQueueItem] = []
    reduced_time: bool = False  # has paid to reduce time?


class Planet(BaseModel):
    id: str = None
    request_id: str = None
    created_at: float = None
    name: str = None
    rarity: str = None
    image: str = None  # image num
    type: str = None  # planet type
    image_url: str = None  # image without bg
    image_url_bg: str = None  # image with bg
    level: int = None
    experience: int = None
    experience_needed: int = None
    diameter: int = None
    slots: int = None  # = Diameter/1000
    slots_used: int = None
    min_temperature: int = None
    max_temperature: int = None

    is_favourite: bool = None

    reserves: Reserves = None

    galaxy: int = None
    solar_system: int = None
    position: int = None
    user: str = None

    claimable: int = None  # timestamp
    claimed: bool = None

    tier: PlanetTier = None
    resources: Resources = Resources()

    price_paid: int = None

    resources_level: list[BuildableItem] = []
    installation_level: list[BuildableItem] = []
    research_level: list[BuildableItem] = []
    defense_items: list[BuildableItem] = []

    building_queue: BuildingQueue = None

    energy_deposits: list[EnergyDeposit] = []
    bkm_deposits: list[BKMTransaction] = []
    emails: list[Email] = []

    def set_image_url(self, url: str):
        self.image_url = f"{url}/{self.type}-{self.rarity}-{self.image}.webp"
        self.image_url_bg = f"{url}/{self.type}-{self.rarity}-{self.image}-bg.webp"

    # @TODO: Pydantic bug dont serialize properties, using root_validator is a workaround
    # @SEE: https://github.com/samuelcolvin/pydantic/pull/2625
    @root_validator
    def compute_energy_usage(cls, values):
        mines: list[BuildableItem] = values["resources_level"]
        energy_usage = 0
        mine: BuildableItem

        for mine in mines:
            mine_info: BuildableItemBaseType = RD.get_item(mine.label)

            if mine_info.category is not RD.MINE_CATEGORY:
                continue

            current_level = mine.current_level
            if current_level == 0:
                continue

            level_info = mine_info.get_level_info(current_level)
            health_percentage = mine.health / level_info.health
            energy_usage += level_info.energy_usage
            if health_percentage < 1:
                energy_health_factor = health_percentage * 1.5
                if energy_health_factor > 1:
                    energy_health_factor = 1

                energy_usage *= energy_health_factor

        values["resources"].energy_usage = energy_usage

        try:
            values["experience_needed"] = PlanetLevelData.get_level_experience(values["level"]+1)
        except:
            pass

        return values

    def get_planet_resource_data(self):
        re = {}
        resources_level = self.resources_level

        resource_level: BuildableItem
        for resource_level in resources_level:
            label = resource_level.label
            upgrading = resource_level.building
            repairing = resource_level.repairing
            current_level = resource_level.current_level

            current_level_info: BuildableItemLevelInfo = ResourceData.get_item(
                label
            ).get_level_info(current_level)

            tmp = {"building": upgrading, "repairing": repairing}

            if upgrading or repairing:
                tmp["finish"] = resource_level.finish

            tmp["level"] = current_level
            tmp["type"] = RD.TYPE

            resources_data: BuildableItemBaseType = RD.get_item(label)
            tmp["name"] = resources_data.name
            tmp["label"] = resources_data.label
            tmp["description"] = resources_data.description
            tmp["health"] = resource_level.health
            tmp["upgrades"] = {}

            if resources_data.category == RD.MINE_CATEGORY:
                tmp["production"] = current_level_info.production

            if resources_data.category == RD.WAREHOUSE_CATEGORY:
                tmp["capacity"] = current_level_info.capacity

            for upgrade in resources_data.builds:
                upgrade_data: BuildableItemLevelInfo = resources_data.builds[upgrade]
                # upgrade_data = resources_data.builds[upgrade]
                tmp["upgrades"][upgrade_data.level] = tier_benefit_buildable_items(
                    self.tier.tier_code, upgrade_data
                )

            re[label] = tmp

        return re

    def get_planet_research_data(self):
        re = {}

        research_levels = self.research_level
        research_level: BuildableItem
        for research_level in research_levels:
            label = research_level.label
            upgrading = research_level.building
            current_level = research_level.current_level

            research_data: BuildableItemBaseType = RE.get_item(label)

            tmp = {"building": upgrading}

            if upgrading:
                tmp["finish"] = research_level.finish

            tmp["level"] = current_level
            tmp["type"] = RE.TYPE
            tmp["name"] = research_data.name
            tmp["label"] = research_data.label
            tmp["description"] = research_data.description

            tmp["upgrades"] = {}
            for upgrade in research_data.builds:
                upgrade_data: BuildableItemLevelInfo = research_data.builds[upgrade]
                tmp["upgrades"][upgrade_data.level] = tier_benefit_buildable_items(
                    self.tier.tier_code, upgrade_data
                )

            re[label] = tmp

        return re

    def get_planet_installation_data(self):
        re = {}
        installations_level = self.installation_level

        installation_level: BuildableItem
        for installation_level in installations_level:
            label = installation_level.label
            upgrading = installation_level.building
            current_level = installation_level.current_level

            installation_data: BuildableItemBaseType = ID.get_item(label)

            tmp = {"building": upgrading}

            if upgrading:
                tmp["finish"] = installation_level.finish

            tmp["level"] = current_level
            tmp["type"] = ID.TYPE
            tmp["name"] = installation_data.name
            tmp["label"] = installation_data.label
            tmp["description"] = installation_data.description

            tmp["upgrades"] = {}
            for upgrade in installation_data.builds:
                upgrade_data: BuildableItemLevelInfo = installation_data.builds[upgrade]
                tmp["upgrades"][upgrade_data.level] = tier_benefit_buildable_items(
                    self.tier.tier_code, upgrade_data
                )

            re[label] = tmp

        return re

    def get_planet_defense_data(self):
        re = {}

        defense_items: list[BuildableItem] = self.defense_items
        defense_item: BuildableItem
        for defense_item in defense_items:
            label = defense_item.label
            defense_data: BuildableItemBaseType = DD.get_item(label)

            tmp = {}
            tmp["type"] = DD.TYPE
            tmp["name"] = defense_data.name
            tmp["label"] = label
            tmp["description"] = defense_data.description
            tmp["available"] = defense_item.quantity
            tmp["data"] = tier_benefit_buildable_items(
                self.tier.tier_code, defense_data.get_level_info()
            )

            tmp["building"] = False
            tmp["finish"] = False

            if defense_item.building:
                tmp["building"] = defense_item.building
                tmp["quantity_building"] = defense_item.quantity_building
                tmp["finish"] = defense_item.finish

            re[label] = tmp

        return re

    def get_emails(self):
        re = []
        for email in self.emails:
            re.append(
                {
                    "id": email.id,
                    "sender": email.sender,
                    "title": email.title,
                    "subTitle": email.sub_title,
                    "template": email.template,
                    "body": email.body,
                    "read": email.read,
                    "topic": email.topic,
                }
            )
        return re


class PlanetResponse(BaseModel):
    id: str
    created_at: float = None
    name: str = None
    rarity: str = None
    image: str = None
    type: str = None
    image_url: str = None
    image_url_bg: str = None
    level: int = None
    experience: int = None
    experience_needed: int = None
    diameter: int = None
    slots: int = None
    slots_used: int = None
    min_temperature: int = None
    max_temperature: int = None

    is_favourite: bool = False

    reserves: Reserves = None

    galaxy: int = None
    solar_system: int = None
    position: int = None
    user: str = None

    claimable: int = None  # timestamp
    claimed: bool = None

    tier: PlanetTier = None
    resources: Resources = None

    price_paid: int = None

    resources_level: list[BuildableItem] = []
    installation_level: list[BuildableItem] = []
    research_level: list[BuildableItem] = []
    defense_items: list[BuildableItem] = []

    building_queue: BuildingQueue = None
    energy_deposits: list[EnergyDeposit] = []
    emails: list[Email] = []

    @staticmethod
    def from_planet(p: Planet) -> "PlanetResponse":
        re = PlanetResponse(id=str(p.id))
        re.created_at = p.created_at
        re.name = p.name
        re.rarity = p.rarity
        re.image = p.image
        re.image_url = p.image_url
        re.image_url_bg = p.image_url_bg
        re.level = p.level
        re.experience = p.experience
        re.diameter = p.diameter
        re.slots = p.slots
        re.slots_used = p.slots_used
        re.min_temperature = p.min_temperature
        re.max_temperature = p.max_temperature
        re.reserves = p.reserves
        re.galaxy = p.galaxy
        re.solar_system = p.solar_system
        re.position = p.position
        re.user = p.user
        re.claimable = p.claimable
        re.claimed = p.claimed
        re.tier = p.tier
        re.resources = p.resources
        re.price_paid = p.price_paid
        re.resources_level = p.resources_level
        re.installation_level = p.installation_level
        re.research_level = p.research_level
        re.defense_items = p.defense_items
        re.energy_deposits = p.energy_deposits
        re.emails = p.emails
        re.building_queue = p.building_queue
        re.is_favourite = p.is_favourite
        re.experience_needed = p.experience_needed
        re.type = p.type
        return re


# Open/Partially Filled/ Completed Orders
class CurrencyMarketOrder(BaseModel):
    order_type: str  # buy, sell
    user_id: str
    planet_id: str
    created_time: float
    updated_time: float
    market_code: str  # Metal/Petrol - Metal/Spr ...
    price: float
    amount: float
    amount_filled: float
    state: str  # not_filled, partially_filled, fully_filled
    # only make visible new balance for user if state completed
    # balance should be withdrawn/deposited right after placing an order

    def to_be_filled(self):
        return self.amount - self.amount_filled

    def update_state(self):
        to_be_filled = self.to_be_filled()

        if to_be_filled <= 0:
            self.state = "fully_filled"
        elif to_be_filled >= 0:
            self.state = "partially_filled"


# Completed Trade
class CurrencyMarketTrade(BaseModel):
    market_code: str  # Metal/Petrol - Metal/Spr ...
    price: float
    amount: float
    created_time: datetime = None


class MetadataResponse(BaseModel):
    response_type: str
    data: Any


class OpenOrdersGroupedByPrice(BaseModel):
    order_type: str
    grouped_price: float
    sum_amount: float
    sum_amount_filled: float
    sum_to_be_filled: float
    total_price: float


class PriceCandleDataGroupedByTimeInterval(BaseModel):
    id: dict = Field(None, alias="_id")
    open: float = None
    close: float = None
    high: float = None
    low: float = None


class Volume24Info(BaseModel):
    max_24: float = None
    min_24: float = None
    pair1_volume: float = None
    pair2_volume: float = None


class Voucher(BaseModel):
    voucher_id: str
    amount_metal: float = 0
    amount_crystal: float = 0
    amount_petrol: float = 0
    amount_energy: float = 0
    redeemed: bool
