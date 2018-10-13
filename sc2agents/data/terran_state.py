"""A random agent for starcraft."""
from pysc2.lib import actions, units

FUNCTIONS = actions.FUNCTIONS

SCOUT_GROUP = 1
CCS_GROUP = 6


class TerranState:

    def __init__(self, minimap_size):
        self.already_recruit = {
            units.Terran.SCV: 12
        }
        self.already_built = {
            units.Terran.CommandCenter: 1
        }

        self.current_loc = None
        self.current_main_cc_loc = None

        self.recruit_order_pos = 0
        self.build_order_pos = 0

        self.minimap_size = minimap_size

        self.currently_building = None
        self.army_selected = False

        self.current_scout_target = None
        self.current_scout_list = None

    def centered_at_cc(self):
        return self.current_loc == self.current_main_cc_loc

    def add_building(self, building, count=1):
        self.already_built[building] = self.already_built.get(building, 0) + count

    def add_unit(self, unit, count=1):
        self.already_recruit[unit] = self.already_recruit.get(unit, 0) + count
