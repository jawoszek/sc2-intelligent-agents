"""A random agent for starcraft."""
import random
from pysc2.lib import actions, units
from sc2agents.data.control_state import MAIN_GROUP
from sc2agents.data.player_state import PlayerState
from sc2agents.data.parameters import Parameters
from sc2agents.stages.stage import Stage

FUNCTIONS = actions.FUNCTIONS


class TerranRefreshStateStage(Stage):

    def __init__(self,
                 parameters: Parameters,
                 player_state: PlayerState):

        super().__init__(1, parameters, player_state)

    def process(self, obs):
        super(TerranRefreshStateStage, self).process(obs)
        if self.obs.timestep.first():
            ccs = self.obs.units_on_screen(units.Terran.CommandCenter)

            if not ccs:
                raise EnvironmentError

            cc = random.choice(ccs)
            point = self.parameters.screen_point(cc.x, cc.y)
            self.queue.append(FUNCTIONS.select_point('select_all_type', point))
            return

        if self.obs.unit_type_selected(units.Terran.CommandCenter):
            self.queue.append(
                FUNCTIONS.select_control_group('set', MAIN_GROUP))
            ccs_y, ccs_x = self.obs.obs.feature_minimap.selected.nonzero()
            point = self.parameters.screen_point(ccs_x[0], ccs_y[0])
            self.player_state.map_state.current_loc = point
            self.player_state.map_state.current_main_base_loc = point
            self.remaining_executions -= 1
            return

        raise NotImplementedError('Mid-game refresh state not implemented yet')
