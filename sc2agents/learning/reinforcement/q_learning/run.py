from absl import app, flags

from sc2agents.learning.reinforcement.q_learning.table import Table
from sc2agents.learning.reinforcement.q_learning.terran.build_order import BuildOrder

from sc2agents.data.build_order_providers import random_build_order
from sc2agents.entrypoint import run_game, setup_flags, setup_model_flags
from sc2agents.learning.deep.keras.models import NAME_TO_MODEL
from sc2agents.learning.deep.keras.network import build_order_prediction, train
from sc2agents.learning.deep.keras.parsers import balance_data, \
    read_data_file, write_build_result
from sc2agents.race import Race
from sc2agents.terran_agent import TerranAgent

import pandas as pd
import os.path
import numpy as np
from sc2agents.learning.reinforcement.q_learning.table import Table


from pysc2.lib import units


def read_pickle(name, actions):
    if os.path.isfile(name):
        return pd.read_pickle(name, compression='gzip')
    return pd.DataFrame(columns=actions, dtype=np.float64)


def run(output_file_path):
    build_pickle = 'buildpickle'
    recruit_pickle = 'recruitpickle'
    actions_b = [None, units.Terran.SupplyDepot, units.Terran.Barracks]
    actions_r = [units.Terran.Marine, None, units.Terran.SCV]
    b_q_table = read_pickle(build_pickle + '.gz', actions_b)
    r_q_table = read_pickle(recruit_pickle + '.gz', actions_r)
    b_table = Table(actions_b, b_q_table)
    r_table = Table(actions_r, r_q_table)

    build = BuildOrder(b_table, r_table)
    agent = TerranAgent(build)
    try:
        result = run_game(agent)
        b_table.learn(build.previous_state, build.next_building, 0, 'terminal')
        r_table.learn(build.previous_recruit_state, build.next_recruit, 0, 'terminal')
        with open(output_file_path, 'a') as file:
            file.write("{0},{1}\n".format(result, build.marines))
    except ValueError:
        print('Unavailable action')  # TODO remove after pysc2 release
    except EnvironmentError:
        print('Some error')
    b_table.q_table.to_pickle(build_pickle + '.gz', compression='gzip')
    r_table.q_table.to_pickle(recruit_pickle + '.gz', compression='gzip')


def main(_):
    for _ in range(0, flags.FLAGS.gamescount):
        run(flags.FLAGS.outfile)


if __name__ == "__main__":
    setup_flags(('outfile',))
    app.run(main)
