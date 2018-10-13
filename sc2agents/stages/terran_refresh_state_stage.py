"""A random agent for starcraft."""
import random
from pysc2.lib import actions, units
from sc2agents.stages.stage import Stage
from sc2agents.data.terran_state import TerranState, CCS_GROUP
from sc2agents.data.terran_parameters import TerranParameters

FUNCTIONS = actions.FUNCTIONS


class TerranRefreshStateStage(Stage):

    def __init__(self, state: TerranState, parameters: TerranParameters, stage_provider):
        super().__init__(1, state, parameters, stage_provider)

    def process(self, obs):
        if obs.first():
            ccs = self.units_on_screen(obs, units.Terran.CommandCenter)

            if not ccs:
                raise EnvironmentError

            cc = random.choice(ccs)
            point = self.parameters.screen_point(cc.x, cc.y)
            self.queue.append(FUNCTIONS.select_point('select_all_type', point))
            return

        if self.unit_type_selected(obs, units.Terran.CommandCenter):
            self.queue.append(FUNCTIONS.select_control_group('set', CCS_GROUP))
            ccs_y, ccs_x = obs.observation.feature_minimap.selected.nonzero()
            point = self.parameters.screen_point(ccs_x[0], ccs_y[0])
            self.state.current_loc = point
            self.state.current_main_cc_loc = point
            self.remaining_actions -= 1
            return

        raise NotImplementedError('Mid-game refresh state not implemented yet')
