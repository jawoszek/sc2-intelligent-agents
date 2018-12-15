"""A random agent for starcraft."""
from operator import itemgetter
from random import randint, sample

from sc2agents.data.build_order import BuildOrder
from sc2agents.race import Race

DEFAULT_BUILD_LENGTH = 20
DEFAULT_RECRUIT_LENGTH = 100


def default_build_order(race) -> BuildOrder:
    return BuildOrder(
        race.constants.RECRUIT_ORDER_DEFAULT,
        race.constants.BUILD_ORDER_DEFAULT
    )


def random_build_order(race: Race,
                       recruit_length=DEFAULT_RECRUIT_LENGTH,
                       build_length=DEFAULT_BUILD_LENGTH) -> BuildOrder:
    return BuildOrder(
        randomized_recruit_order(recruit_length,
                                 race.constants.UNITS_TO_CHOOSE),
        randomized_build_order(build_length,
                               race.constants.BUILDINGS_TO_CHOOSE)
    )


def randomized_recruit_order(length, units_to_choose):
    return sample(units_to_choose, length)


def randomized_build_order(length, buildings_to_choose):
    building_types = sample(buildings_to_choose, length)
    order = [(randint(10, length - 10), building) for building in
             building_types]
    return sorted(order, key=itemgetter(0))
