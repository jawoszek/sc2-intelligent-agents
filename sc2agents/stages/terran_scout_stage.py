"""A random agent for starcraft."""
from pysc2.lib import actions, units
from sc2agents.data.control_state import SCOUT_GROUP
from sc2agents.data.player_state import PlayerState
from sc2agents.data.parameters import Parameters
from sc2agents.stages.stage import Stage

FUNCTIONS = actions.FUNCTIONS


class TerranScoutStage(Stage):

    def __init__(self,
                 parameters: Parameters,
                 player_state: PlayerState):

        super().__init__(1, parameters, player_state)
        self.scout_selected = False

    def process(self, obs):
        super(TerranScoutStage, self).process(obs)
        map_state = self.player_state.map_state
        control_state = self.player_state.control_state
        enemies_location_minimap = self.positions_of_enemy_on_minimap()

        if not enemies_location_minimap:
            if self.obs.obs.control_groups[SCOUT_GROUP][1] < 1:
                if not map_state.centered_at_base():
                    self.move_screen_to_cc()
                    return
                if not self.obs.unit_type_selected(units.Terran.SCV, 1):
                    self.select_units(units.Terran.SCV, 1)
                    return

                self.queue.append(
                    FUNCTIONS.select_control_group('set', SCOUT_GROUP))
                return

            self.queue.append(
                FUNCTIONS.select_control_group('recall', SCOUT_GROUP))
            if not self.obs.unit_type_selected(units.Terran.SCV, 1):
                self.queue.append(
                    FUNCTIONS.select_control_group('recall', SCOUT_GROUP))
                return

            if not self.scout_selected:
                self.scout_selected = True
                return

            if control_state.current_scout_target is None:

                if not control_state.current_scout_list:
                    control_state.current_scout_list = self.sorted_expansions()

                target = control_state.current_scout_list.pop()
                control_state.current_scout_target = target
                self.queue.append(FUNCTIONS.Move_minimap('now', target))
                self.remaining_executions -= 1
                return

            scout_y, scout_x = self.obs.obs.feature_minimap.selected.nonzero()
            scout_location = self.parameters.minimap_point(scout_x[0],
                                                           scout_y[0])

            if scout_location.dist(control_state.current_scout_target) < 2:
                control_state.current_scout_list = \
                    self.filter_close_expansions(scout_location)
                if not control_state.current_scout_list:
                    control_state.current_scout_target = None
                    self.remaining_executions -= 1
                    return
                self.sort_scout_targets_by_distance(scout_location)
                target = control_state.current_scout_list.pop(0)
                control_state.current_scout_target = target
                self.queue.append(FUNCTIONS.Move_minimap('now', target))

            self.remaining_executions -= 1
            return

        if self.obs.obs.control_groups[SCOUT_GROUP][1] < 1:
            control_state.current_scout_target = None
            control_state.current_scout_list = None

        self.remaining_executions -= 1
        return

    def sort_scout_targets_by_distance(self, scout_location):
        self.player_state.control_state.current_scout_list.sort(
            key=lambda loc: loc.dist(scout_location))

    def filter_close_expansions(self, scout_location, distance=2):
        return [
            location for location
            in self.player_state.control_state.current_scout_list
            if location.dist(scout_location) > distance
        ]
