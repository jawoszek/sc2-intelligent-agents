"""A random agent for starcraft."""
from pysc2.lib import units
from sc2agents.data.build_order import BuildOrder
from sc2agents.data.build_order_providers import randomized_build_order, \
    randomized_recruit_order

RECRUIT_ORDER_DEFAULT = [
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.SCV,
    units.Terran.Marine,
    units.Terran.SCV,
    units.Terran.Marine,
    units.Terran.SCV,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine,
    units.Terran.Marine
]

BUILD_ORDER_DEFAULT = [
    (12, units.Terran.SupplyDepot),
    (14, units.Terran.Barracks),
    (16, units.Terran.SupplyDepot),
    (17, units.Terran.Refinery),
    (18, units.Terran.Barracks),
    (19, units.Terran.SupplyDepot),
    (22, units.Terran.Barracks),
    (23, units.Terran.Refinery),
    (24, units.Terran.SupplyDepot),
    (28, units.Terran.Barracks),
    (34, units.Terran.SupplyDepot),
    (40, units.Terran.SupplyDepot),
    (48, units.Terran.SupplyDepot),
    (56, units.Terran.SupplyDepot),
    (64, units.Terran.SupplyDepot)
]

UNITS_TO_CHOOSE = [
    units.Terran.SCV,
    units.Terran.Marine
]

BUILDINGS_TO_CHOOSE = [
    units.Terran.SupplyDepot,
    units.Terran.Barracks,
    units.Terran.Refinery
]


def default_build_order() -> BuildOrder:
    return BuildOrder(
        RECRUIT_ORDER_DEFAULT,
        BUILD_ORDER_DEFAULT
    )


def random_build_order(recruit_length, build_length) -> BuildOrder:
    return BuildOrder(
        randomized_recruit_order(recruit_length, UNITS_TO_CHOOSE),
        randomized_build_order(build_length, BUILDINGS_TO_CHOOSE)
    )
