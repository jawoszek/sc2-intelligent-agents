"""A random agent for starcraft."""
from pysc2.lib.point import Point
from sc2agents.data.building_state import BuildingState
from sc2agents.data.build_order import BuildOrder


# TODO proper logging
class Parameters:

    def __init__(self, build_order: BuildOrder, screen_size, minimap_size):
        self.build_order = build_order
        self.screen_size = screen_size
        self.minimap_size = minimap_size

    def build_order_reached(self, food_used, state: BuildingState):
        return self.build_order.build_order_reached(food_used, state)

    def build_order_building(self, state: BuildingState, index=None):
        return self.build_order.build_order_building(state, index)

    def recruit_order_finished(self, state: BuildingState):
        return self.build_order.recruit_order_finished(state)

    def recruit_order_next(self, state: BuildingState):
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
