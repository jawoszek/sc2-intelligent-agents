"""A random agent for starcraft."""

from pysc2.lib import actions
from pysc2.lib.point import Point
from sc2agents.data.terran_state import TerranState
from sc2agents.data.terran_build_order import TerranBuildOrder

FUNCTIONS = actions.FUNCTIONS


# TODO proper logging
class TerranParameters:

    def __init__(self, build_order: TerranBuildOrder, screen_size, minimap_size):
        self.build_order = build_order
        self.screen_size = screen_size
        self.minimap_size = minimap_size

    def build_order_reached(self, obs, state: TerranState):
        return self.build_order.build_order_reached(obs, state)

    def build_order_building(self, state: TerranState, index=None):
        return self.build_order.build_order_building(state, index)

    def recruit_order_finished(self, state: TerranState):
        return self.build_order.recruit_order_finished(state)

    def recruit_order_next(self, state: TerranState):
        return self.build_order.recruit_order_next(state)

    def screen_point(self, x, y):
        if x < 0:
            print("Screen x coord with wrong value - {0}".format(x))
            x = 0
        if x >= self.screen_size:
            print("Screen x coord with wrong value - {0}".format(x))
            x = self.screen_size - 1
        if y < 0:
            print("Screen y coord with wrong value - {0}".format(y))
            y = 0
        if y >= self.screen_size:
            print("Screen y coord with wrong value - {0}".format(y))
            y = self.screen_size - 1
        return Point(x, y)

    def minimap_point(self, x, y):
        if x < 0:
            print("Minimap x coord with wrong value - {0}".format(x))
            x = 0
        if x >= self.minimap_size:
            print("Minimap x coord with wrong value - {0}".format(x))
            x = self.minimap_size - 1
        if y < 0:
            print("Minimap y coord with wrong value - {0}".format(y))
            y = 0
        if y >= self.minimap_size:
            print("Minimap y coord with wrong value - {0}".format(y))
            y = self.minimap_size - 1
        return Point(x, y)
