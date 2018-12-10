from keras import Model, Sequential
from keras.layers import Dense, Dropout, Input, concatenate


def simple_dense_model():
    model = Sequential()
    model.add(Dense(units=64, activation='relu', input_dim=140))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(units=2, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='sgd',
                  metrics=['accuracy'])
    return model


def simple_sparse_model():
    buildings_1_input = Input(shape=(10,), dtype='float32',
                              name='buildings_1')
    buildings_2_input = Input(shape=(10,), dtype='float32',
                              name='buildings_2')
    buildings_3_input = Input(shape=(10,), dtype='float32',
                              name='buildings_3')
    buildings_4_input = Input(shape=(10,), dtype='float32',
                              name='buildings_4')
    units_input = Input(shape=(100,), dtype='float32', name='units')
    inputs = [buildings_1_input, buildings_2_input, buildings_3_input,
              buildings_4_input, units_input]
    b_1_l = Dense(18, activation='relu')(buildings_1_input)
    b_2_l = Dropout(0.5)(Dense(18, activation='relu')(buildings_2_input))
    b_3_l = Dropout(0.5)(Dense(18, activation='relu')(buildings_3_input))
    b_4_l = Dropout(0.5)(Dense(18, activation='relu')(buildings_4_input))
    u_l = Dropout(0.5)(Dense(32, activation='relu')(units_input))
    merged = concatenate([b_1_l, b_2_l, b_3_l, b_4_l, u_l])
    main_l = Dense(64, activation='relu')(merged)
    main_output = Dense(2, activation='softmax', name='main_output')(main_l)
    model = Model(inputs=inputs, outputs=[main_output])
    model.compile(loss='categorical_crossentropy',
                  optimizer='sgd',
                  metrics=['accuracy'])
    return model
