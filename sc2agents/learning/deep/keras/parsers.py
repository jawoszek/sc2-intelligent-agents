from ast import literal_eval
from random import shuffle

BUILD_NODES = 20
RECRUIT_NODES = 100
MIN_POP = 10
MAX_POP = 100

UNITS_TO_VALUE = {
    45: 0,
    48: 1
}

BUILDING_TO_VALUE = {
    19: 0,
    20: 0.5,
    21: 1
}

VALUE_TO_BUILDING = {v: k for k, v in BUILDING_TO_VALUE.items()}


def normalize_row(row):
    output_norm = []
    for i in range(0, BUILD_NODES):
        pop = row[i * 2]
        building = row[i * 2 + 1]
        output_norm.append((pop - MIN_POP) / (MAX_POP - MIN_POP))
        output_norm.append(BUILDING_TO_VALUE[building])
    for i in range(BUILD_NODES * 2, BUILD_NODES * 2 + RECRUIT_NODES):
        unit = row[i]
        output_norm.append(UNITS_TO_VALUE[unit])
    return output_norm


def normalize_output_row(row):
    return [1 if i == 1 else 0 for i in row]


def read_data_file(path):
    inputs_read = []
    outputs_read = []
    with open(path, 'r') as file:
        for line in file.readlines():
            whole_line = "({})".format(line)
            whole_object = literal_eval(whole_line)
            whole_record = []
            for pop, building in whole_object[0]:
                whole_record.append(pop)
                whole_record.append(building)
            for unit in whole_object[1]:
                whole_record.append(unit)
            inputs_read.append(whole_record)
            outputs_read.append([whole_object[2]])

    inputs_read = list(
        map(lambda row: normalize_row(row),
            inputs_read))
    outputs_read = list(map(normalize_output_row, outputs_read))
    return inputs_read, outputs_read


def read_input_from_text(text):
    inputs_read = []
    for line in text.split('\n'):
        whole_line = "({})".format(line)
        whole_object = literal_eval(whole_line)
        whole_record = []
        for pop, building in whole_object[0]:
            whole_record.append(pop)
            whole_record.append(building)
        for unit in whole_object[1]:
            whole_record.append(unit)
        inputs_read.append(whole_record)

    inputs_read = list(
        map(lambda row: normalize_row(row),
            inputs_read))
    return inputs_read


def balance_data(input_data, output_data):
    indexes = shuffle(list(range(0, len(output_data))))

    def find_indexes(result):
        return [index for index in indexes if output_data[index][0] == result]

    def with_indexes(indexes_to_take, input_list):
        return [input_list[index] for index in indexes_to_take]
    count_won = len([1 for result in output_data if result[0] == 1])
    count_lost = len(output_data) - count_won
    count = min(count_won, count_lost)
    indexes_won = find_indexes(1)[:count]
    indexes_lost = find_indexes(-1)[:count]
    chosen_indexes = shuffle(indexes_won + indexes_lost)
    chosen_inputs = with_indexes(chosen_indexes, input_data)
    chosen_outputs = with_indexes(chosen_indexes, output_data)
    return chosen_inputs, chosen_outputs


def write_build_result(build, result, file_path):
    with open(file_path, 'a') as file:
        file.write("{0},{1}\n".format(build.storage_format(), result))
