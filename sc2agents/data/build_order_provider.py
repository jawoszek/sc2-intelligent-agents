"""A random agent for starcraft."""
from random import randint, sample
from operator import itemgetter
from pysc2.lib import units
from sc2agents.data.terran_build_order import TerranBuildOrder

DEFAULT_BUILD_LENGTH = 20
DEFAULT_RECRUIT_LENGTH = 100

UNITS_TO_CHOOSE = [units.Terran.SCV, units.Terran.Marine]
BUILDINGS_TO_CHOOSE = [units.Terran.SupplyDepot, units.Terran.Barracks, units.Terran.Refinery]


def randomized_recruit_order(length):
    return sample(UNITS_TO_CHOOSE, length)


def randomized_build_order(length):
    building_types = sample(BUILDINGS_TO_CHOOSE, length)
    return [(randint(10, length-10), building) for building in building_types]


class BuildOrderProvider:

    def provide(self) -> TerranBuildOrder:
        raise NotImplementedError('Cannot call methods of abstract class')


class RandomBuildOrderProvider(BuildOrderProvider):  # pylint: disable=too-few-public-methods

    def __init__(self, recruit_length=DEFAULT_RECRUIT_LENGTH, build_length=DEFAULT_BUILD_LENGTH):
        super().__init__()
        self.recruit_length = recruit_length
        self.build_length = build_length

    def provide(self) -> TerranBuildOrder:
        recruit_order = randomized_recruit_order(self.recruit_length)
        build_order = randomized_build_order(self.build_length)
        build_order.sort(key=itemgetter(0))
        return TerranBuildOrder(recruit_order, build_order)
