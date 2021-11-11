import tensorflow as tf
import numpy as np


class FullyConnectedModel(tf.keras.Model):

    def __init__(self, input_shape, output_shape):
        super(FullyConnectedModel, self).__init__()
        self.dense = tf.keras.layers.Dense(output_shape)

    def call(self, x):
        return self.dense(x)


if __name__ == "__main__":
    input_shape = 4
    output_shape = 8
    model = FullyConnectedModel(input_shape=input_shape, output_shape=output_shape)
    inputs = np.random.uniform(-1.0, 1.0, (1, input_shape))
    inputs = tf.convert_to_tensor(inputs)
    output = model(inputs)
    print(f'{inputs.shape} -> {output.shape}')
