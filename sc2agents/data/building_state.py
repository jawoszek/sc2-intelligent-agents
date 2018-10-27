"""A random agent for starcraft."""
from pysc2.lib import units


class BuildingState:

    def __init__(self, initial_recruited, initial_built):
        self.already_recruit = initial_recruited
        self.already_built = initial_built

        self.recruit_order_pos = 0
        self.build_order_pos = 0

        self.currently_building = None

    def add_building(self, building, count=1):
        new_value = self.already_built.get(building, 0) + count
        self.already_built[building] = new_value

    def add_unit(self, unit, count=1):
        new_value = self.already_recruit.get(unit, 0) + count
        self.already_recruit[unit] = new_value

    def already_recruited_army_units(self):
        return [
            count for unit, count
            in self.already_recruit.items()
            if unit is not units.Terran.SCV
        ]
