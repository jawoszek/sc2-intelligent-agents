from random import shuffle

from absl import app, flags

from sc2agents.entrypoint import setup_flags, setup_model_flags
from sc2agents.learning.deep.keras.models import NAME_TO_MODEL
from sc2agents.learning.deep.keras.network import predict, train
from sc2agents.learning.deep.keras.parsers import read_data_file


def is_class_hit(result, real_result):
    resulting_class = 1 if result[1] > result[0] else 0
    return resulting_class == real_result


def results_parsing(output_t):
    def compare_results(results, i):
        return (
            is_class_hit(results[i], output_t[i][0]),
            output_t[i][0],
            results[i]
        )

    return compare_results


def all_with_indexes_in(source, target_range):
    return [
        source[index]
        for index in range(0, len(source))
        if index in target_range
    ]


def all_with_indexes_not_in(source, target_range):
    return [
        source[index]
        for index in range(0, len(source))
        if index not in target_range
    ]


def cross_validate(model, data, epochs, k=5):
    input_data, output_data = data
    indexes = list(range(0, len(input_data)))
    shuffle(indexes)
    segment_length = int(len(input_data) / k)
    results_all = []
    for i in range(0, k):
        test_range = range(i * segment_length, (i + 1) * segment_length)
        indexes_l = all_with_indexes_not_in(indexes, test_range)
        indexes_t = all_with_indexes_in(indexes, test_range)
        train_input = all_with_indexes_in(input_data, indexes_l)
        train_output = all_with_indexes_in(output_data, indexes_l)
        test_input = all_with_indexes_in(input_data, indexes_t)
        test_output = all_with_indexes_in(output_data, indexes_t)
        train(model, train_input, train_output, epochs)
        results_single = predict(model, test_input,
                                 results_parsing(test_output))
        results_all.append(results_single)
    results_sum = sum([
        len([c for c in classes if c[0]]) / len(classes) * 100
        for classes in results_all
    ])
    return results_sum / k


def validate(model, data, epochs):
    input_data, output_data = data
    train(model, input_data, output_data, epochs)
    classes = predict(model, input_data, results_parsing(output_data))
    percent = len([c for c in classes if c[0]]) / len(classes) * 100
    return percent


def main(_):
    data = read_data_file(flags.FLAGS.datafile)
    model = NAME_TO_MODEL[flags.FLAGS.model]()
    epochs = flags.FLAGS.epochs
    args = (model, data, epochs)
    result = cross_validate(*args) if flags.FLAGS.cross else validate(*args)
    print(result)


if __name__ == "__main__":
    setup_flags(('datafile',))
    setup_model_flags(True)
    app.run(main)
