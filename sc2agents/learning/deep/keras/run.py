from absl import app, flags

from sc2agents.entrypoint import run_game
from sc2agents.entrypoint import setup_flags, setup_model_flags
from sc2agents.learning.deep.keras.models import NAME_TO_MODEL
from sc2agents.learning.deep.keras.network import build_order_prediction, train
from sc2agents.learning.deep.keras.parsers import read_data_file

from sc2agents.data.build_order_providers import random_build_order
from sc2agents.race import Race
from sc2agents.terran_agent import TerranAgent
from sc2agents.learning.deep.keras.parsers import write_build_result, balance_data


def prepare_network():
    input_data, output_data = read_data_file(flags.FLAGS.datafile)
    if flags.FLAGS.balanced:
        input_data, output_data = balance_data(input_data, output_data)
    epochs = flags.FLAGS.epochs
    model = NAME_TO_MODEL[flags.FLAGS.model]
    train(model, input_data, output_data, epochs)
    return model


def model_validation():
    model = prepare_network()

    def validate(build):
        return build_order_prediction(model, build)
    return validate


def run(validation, output_file_path):
    while True:
        build = random_build_order(Race.TERRAN)
        if validation(build):
            break
    agent = TerranAgent(build)
    result = run_game(agent)
    write_build_result(build, result, output_file_path)


def main(_):
    def always(_):
        return True
    validation = model_validation() if flags.FLAGS.datafile else always
    for _ in range(0, flags.FLAGS.gamescount):
        run(validation, flags.FLAGS.outfile)


if __name__ == "__main__":
    setup_flags(('outfile',))
    app.run(main)
