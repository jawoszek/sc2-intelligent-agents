"""A random agent for starcraft."""
from random import randint, sample
from operator import itemgetter
from sc2agents.race import Race

DEFAULT_BUILD_LENGTH = 20
DEFAULT_RECRUIT_LENGTH = 100


def random_build_order(race: Race,
                       recruit_length=DEFAULT_RECRUIT_LENGTH,
                       build_length=DEFAULT_BUILD_LENGTH):
    race.build_order_provider().random_build_order(recruit_length,
                                                   build_length)


def randomized_recruit_order(length, units_to_choose):
    return sample(units_to_choose, length)


def randomized_build_order(length, buildings_to_choose):
    building_types = sample(buildings_to_choose, length)
    order = [(randint(10, length-10), building) for building in building_types]
    return sorted(order, key=itemgetter(0))
