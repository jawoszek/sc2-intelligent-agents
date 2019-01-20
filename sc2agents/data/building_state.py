"""A random agent for starcraft."""
from copy import deepcopy

from pysc2.lib import units


def merge_count(data, key, count):
    new_value = data.get(key, 0) + count
    data[key] = new_value


class BuildingState:

    def __init__(self, initial_recruited, initial_built):
        self.already_recruit = deepcopy(initial_recruited)
        self.already_built = deepcopy(initial_built)

        self.recruit_order_pos = 0
        self.build_order_pos = 0

        self.currently_building = None

    def add_building(self, building, count=1):
        merge_count(self.already_built, building, count)

    def add_unit(self, unit, count=1):
        merge_count(self.already_recruit, unit, count)

    def already_recruited_army_units(self):
        return sum([
            count for unit, count
            in self.already_recruit.items()
            if unit is not units.Terran.SCV
        ])
