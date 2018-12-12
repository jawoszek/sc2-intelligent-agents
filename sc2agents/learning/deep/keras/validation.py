from random import shuffle

from keras.utils import to_categorical
from numpy import array


def is_class_hit(result, real_result):
    resulting_class = 1 if result[1] > result[0] else 0
    return resulting_class == real_result


def results_to_classes(results, output_t):
    return [
        (is_class_hit(results[i], output_t[i][0]),
         output_t[i][0], results[i])
        for i in range(0, len(results))
    ]


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
        x_train = array(train_input)
        y_train = to_categorical(array(train_output).T[0])
        model.fit(x_train, y_train, epochs=epochs, batch_size=256)
        x_test = array(test_input)
        results = model.predict(x_test, batch_size=256)
        results_single = results_to_classes(results, test_output)
        results_all.append(results_single)
    results_sum = sum([
        len([c for c in classes if c[0]]) / len(classes) * 100
        for classes in results_all
    ])
    return results_sum / k


def validate(model, data, epochs):
    input_data, output_data = data
    x_train = array(input_data)
    y_train = to_categorical(array(output_data).T[0])
    model.fit(x_train, y_train, epochs=epochs, batch_size=256)
    results = model.predict(x_train, batch_size=256)
    classes = results_to_classes(results, output_data)
    percent = len([c for c in classes if c[0]]) / len(classes) * 100
    return percent
