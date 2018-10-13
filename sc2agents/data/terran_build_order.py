
"""A random agent for starcraft."""

from pysc2.lib import actions, units
from sc2agents.data.terran_state import TerranState

FUNCTIONS = actions.FUNCTIONS

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


def recruit_order_pos_to_str(recruit_order):
    return map(lambda unit: str(unit.value), recruit_order)


class TerranBuildOrder:

    def __init__(self, recruit_order=None, build_order=None):
        if recruit_order is None:
            self.recruit_order = RECRUIT_ORDER_DEFAULT
        else:
            self.recruit_order = recruit_order

        if build_order is None:
            self.build_order = BUILD_ORDER_DEFAULT
        else:
            self.build_order = build_order

    def build_order_reached(self, obs, state: TerranState):
        return state.build_order_pos < len(self.build_order) \
               and \
               obs.observation.player.food_used >= self.build_order[state.build_order_pos][0]

    def build_order_building(self, state: TerranState, index=None):
        if index is None:
            index = state.build_order_pos

        return self.build_order[index][1] if index < len(self.build_order) else None

    def recruit_order_finished(self, state: TerranState):
        return state.recruit_order_pos >= len(self.recruit_order)

    def recruit_order_next(self, state: TerranState):
        return self.recruit_order[state.recruit_order_pos]

    def storage_format(self):
        build_order_part = self.build_order_storage_format()
        recruit_order_part = self.recruit_order_storage_format()
        return "{0},{1}".format(build_order_part, recruit_order_part)

    def build_order_storage_format(self):
        build_order_listed = [
            "({0},{1})".format(pop, building)
            for pop, building in self.build_order
        ]
        return "[{0}]".format(','.join(build_order_listed))

    def recruit_order_storage_format(self):
        recruit_order_listed = ','.join(recruit_order_pos_to_str(self.recruit_order))
        return '[{0}]'.format(recruit_order_listed)
