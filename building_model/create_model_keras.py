import keras
import tensorflow as tf


def make_new_model():
    model = tf.keras.models.Sequential()
    model.add(keras.layers.Dense(168, input_dim=42, activation='relu'))
    model.add(keras.layers.Dense(42, activation='relu'))
    model.add(keras.layers.Dense(42, activation='relu'))
    model.add(keras.layers.Dense(42, activation='relu'))
    model.add(keras.layers.Dense(42, activation='relu'))
    model.add(keras.layers.Dense(42, activation='relu'))
    model.add(keras.layers.Dense(42, activation='relu'))
    model.add(keras.layers.Dense(42, activation='relu'))
    model.add(keras.layers.Dense(42, activation='relu'))
    model.add(keras.layers.Dense(42, activation='relu'))
    model.add(keras.layers.Dense(42, activation='relu'))
    model.add(keras.layers.Dense(42, activation='relu'))
    model.add(keras.layers.Dense(42, activation='relu'))
    model.add(keras.layers.Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.save("evaluation")

# tensorboard
