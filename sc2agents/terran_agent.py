"""A terran agent."""
from absl import app
from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features

from sc2agents.race import Race
import sc2agents.data.terran as terran
from sc2agents.data.build_order import BuildOrder
from sc2agents.data.build_order_providers import default_build_order
from sc2agents.data.building_state import BuildingState
from sc2agents.data.control_state import ControlState
from sc2agents.data.map_state import MapState
from sc2agents.data.observations import Observations
from sc2agents.data.parameters import Parameters
from sc2agents.data.player_state import PlayerState
from sc2agents.stages.stage_provider import StageProvider

FUNCTIONS = actions.FUNCTIONS

MINIMAP_SIZE = 64
SCREEN_SIZE = 84
STEP_MUL = 16
DIFFICULTY = sc2_env.Difficulty.easy


class TerranAgent(base_agent.BaseAgent):
    """A Terran Agent."""

    def __init__(self,
                 build_order: BuildOrder = default_build_order(Race.TERRAN)):
        super().__init__()
        self.state = PlayerState(
            BuildingState(
                terran.constants.INITIAL_UNITS,
                terran.constants.INITIAL_BUILDINGS
            ),
            ControlState(),
            MapState(MINIMAP_SIZE)
        )
        self.parameters = Parameters(
            build_order,
            screen_size=SCREEN_SIZE,
            minimap_size=MINIMAP_SIZE
        )
        self.stage_provider = StageProvider()
        self.stage = self.stage_provider.provide_next_stage(None)(
            self.parameters, self.state)

    def step(self, obs):
        super(TerranAgent, self).step(obs)
        observations = Observations(obs)

        if self.stage.has_next_action():
            return self.stage.next_action()

        if self.stage.ended():
            next_stage = self.stage_provider.provide_next_stage(self.stage)(
                self.parameters, self.state)

            if next_stage is None:
                message = 'Stage {0} is not known to provider'.format(
                    type(self.stage))
                raise NotImplementedError(message)

            self.stage = next_stage
            self.stage.prepare(observations)
        else:
            self.stage.process(observations)

        if self.stage.has_next_action():
            return self.stage.next_action()

        return FUNCTIONS.no_op()


def main(_):
    try:
        while True:
            with sc2_env.SC2Env(
                    map_name="AcidPlant",
                    players=[sc2_env.Agent(sc2_env.Race.terran),
                             sc2_env.Bot(sc2_env.Race.zerg,
                                         DIFFICULTY)],
                    agent_interface_format=features.AgentInterfaceFormat(
                        feature_dimensions=features.Dimensions(
                            screen=SCREEN_SIZE, minimap=MINIMAP_SIZE),
                        use_feature_units=True),
                    step_mul=STEP_MUL,
                    game_steps_per_episode=0,
                    visualize=False) as env:
                # TODO ignore not available action after new pysc2 release

                agent = TerranAgent()
                agent.setup(env.observation_spec(), env.action_spec())

                timesteps = env.reset()
                agent.reset()

                while True:
                    step_actions = [agent.step(timesteps[0])]
                    if timesteps[0].last():
                        print('Finished {0}'.format(timesteps[0].reward))
                        # TODO proper place for result resources
                        with open("results_scripted.txt", "a") as file:
                            file.write(
                                '{0}\n'.format(str(timesteps[0].reward)))
                        break
                    timesteps = env.step(step_actions)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    app.run(main)
