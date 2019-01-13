from keras.utils import to_categorical
from numpy import array

import sc2agents.learning.deep.keras.parsers as parsers


def train(model, input_data, output_data, epochs):
    x_train = array(input_data)
    y_train = to_categorical(array(output_data).T[0], num_classes=2)
    model.fit(x_train, y_train, epochs=epochs, batch_size=256)


def predict(model, input_data, hit_condition):
    results = model.predict(array(input_data), batch_size=256)
    return [
        hit_condition(results, index)
        for index in range(0, len(results))
    ]


def build_order_prediction(model, build_order, confidence=0.9):
    data = parsers.read_input_from_text(build_order.storage_format())

    def confidence_check(results, index):
        return results[index][1] > confidence \
               and results[index][0] < 1 - confidence

    return predict(model, data, confidence_check)[0]
