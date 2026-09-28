"""Serializable CNN–BiLSTM–attention models."""

import keras
from keras import layers, ops


@keras.saving.register_keras_serializable(package="PPG")
class TemporalAttention(layers.Layer):
    def build(self, shape):
        self.w = self.add_weight(
            name="attention_weight", shape=(shape[-1], 1), initializer="random_normal"
        )
        self.b = self.add_weight(
            name="attention_bias", shape=(shape[1], 1), initializer="zeros"
        )
        super().build(shape)

    def call(self, inputs):
        weights = ops.softmax(ops.tanh(ops.matmul(inputs, self.w) + self.b), axis=1)
        return ops.sum(inputs * weights, axis=1)


def build(kind, shape, pretrained=False):
    inputs = keras.Input(shape=shape)
    if kind == "waveform":
        x = layers.Conv1D(16, 3, padding="same")(inputs)
        x = layers.ReLU()(layers.BatchNormalization()(x))
        x = layers.MaxPooling1D(2, strides=4, padding="same")(x)
    else:
        x = layers.Conv2D(16, 3, padding="same")(inputs)
        x = layers.ReLU()(layers.BatchNormalization()(x))
        x = layers.MaxPooling2D(2, strides=4, padding="same")(x)
        x = layers.Permute((2, 1, 3))(x)  # Time is the recurrent sequence axis.
        x = layers.Reshape((int(x.shape[1]), int(x.shape[2]) * int(x.shape[3])))(x)
    x = layers.Bidirectional(layers.LSTM(64, return_sequences=True))(x)
    x = TemporalAttention()(layers.Dropout(0.2)(x))
    model = keras.Model(inputs, layers.Dense(1)(x))
    model.compile(optimizer=keras.optimizers.Adam(0.001), loss="mse")
    return model
