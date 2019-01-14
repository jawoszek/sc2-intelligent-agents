from pathlib import Path

from absl import flags
from pysc2.env import sc2_env
from pysc2.lib import features

import sc2agents.learning.deep.keras.models as keras_models

DEFAULT_MINIMAP_SIZE = 64
DEFAULT_SCREEN_SIZE = 84
DEFAULT_STEP_MUL = 32
DEFAULT_DIFFICULTY = sc2_env.Difficulty.very_easy

DEFAULT_GAME_SPECIFICATION = {
    'map_name': "Eastwatch",
    'players': [
        sc2_env.Agent(sc2_env.Race.terran),
        sc2_env.Bot(
            sc2_env.Race.zerg,
            DEFAULT_DIFFICULTY
        )
    ],
    'agent_interface_format': features.AgentInterfaceFormat(
        feature_dimensions=features.Dimensions(
            screen=DEFAULT_SCREEN_SIZE,
            minimap=DEFAULT_MINIMAP_SIZE
        ),
        use_feature_units=True),
    'step_mul': DEFAULT_STEP_MUL,
    'game_steps_per_episode': 0,
    'visualize': False
    # 'ensure_available_actions': False #TODO enable after pysc2 release
}


def run_game(agent, game_specification=None):
    if game_specification is None:
        game_specification = DEFAULT_GAME_SPECIFICATION
    with sc2_env.SC2Env(**game_specification) as env:
        agent.setup(env.observation_spec(), env.action_spec())
        time_steps = env.reset()
        agent.reset()
        while True:
            step_actions = [agent.step(time_steps[0])]
            if time_steps[0].last():
                return time_steps[0].reward
            time_steps = env.step(step_actions)


def setup_model_flags(required=False):
    flags.DEFINE_enum('model', None, keras_models.NAME_TO_MODEL.keys(),
                      'Name of the model to use.')
    flags.DEFINE_integer('epochs', 100, 'Epochs count.')
    if required:
        flags.mark_flag_as_required('model')


def setup_flags(required_flags=()):
    flags.DEFINE_bool('cross', False, 'Enables cross-validation.')
    flags.DEFINE_bool('balanced', False, 'Set to learn on balanced data.')
    flags.DEFINE_string('outfile', None, 'Path to output file.')
    flags.DEFINE_string('datafile', None, 'Path to file with data.')
    flags.DEFINE_integer('gamescount', 1, 'Number of games to play.')

    def file_exists_if_arg_given(path):
        return path is None or Path(path).is_file()

    flags.register_validator(
        'datafile',
        file_exists_if_arg_given,
        message='Datafile must exists.'
    )

    for required_flag in required_flags:
        flags.mark_flag_as_required(required_flag)
