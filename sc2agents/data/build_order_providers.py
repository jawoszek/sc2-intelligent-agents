"""A random agent for starcraft."""
from operator import itemgetter
from random import choices, randint

from sc2agents.data.build_order import BuildOrder
from sc2agents.race import Race

DEFAULT_BUILD_LENGTH = 20
DEFAULT_RECRUIT_LENGTH = 100


def default_build_order(race: Race) -> BuildOrder:
    return BuildOrder(
        race.constants().RECRUIT_ORDER_DEFAULT,
        race.constants().BUILD_ORDER_DEFAULT
    )


def random_build_order(race: Race,
                       recruit_length=DEFAULT_RECRUIT_LENGTH,
                       build_length=DEFAULT_BUILD_LENGTH) -> BuildOrder:
    return BuildOrder(
        randomized_recruit_order(recruit_length,
                                 race.constants().UNITS_TO_CHOOSE),
        randomized_build_order(build_length, recruit_length,
                               race.constants().BUILDINGS_TO_CHOOSE)
    )


def randomized_recruit_order(length, units_to_choose):
    return choices(units_to_choose, k=length)


def randomized_build_order(length, recruit_length, buildings_to_choose):
    building_types = choices(buildings_to_choose, k=length)
    order = [(randint(10, recruit_length - 10), building) for building in
             building_types]
    return sorted(order, key=itemgetter(0))
