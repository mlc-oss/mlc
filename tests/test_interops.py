import os
import sys
import random
import unittest

import numpy as np
import tensorflow as tf
import torch

from mlc.models.tensorflow_impl import FullyConnectedModel as TFModel
from mlc.models.pytorch_impl import FullyConnectedModel as TorchModel


class InterOpsTestCase(unittest.TestCase):

    def setUp(self):
        self.seed = 42

    def test_listener_compatability(self):
        input_size = 4
        output_size = 8
        inputs = np.random.uniform(-1.0, 1.0, (1, input_size))

        tf_model = TFModel(input_size, output_size)
        torch_model = TorchModel(input_size, output_size)

        tf_output = tf_model(inputs).numpy()
        _ = torch_model(inputs)

        w, b = tf_model.get_weights()
        for m in tuple(torch_model.modules())[1:]:
            m.weight.data = torch.from_numpy(np.transpose(w))
            m.bias.data = torch.from_numpy(b)

        torch_output = torch_model(inputs).detach().numpy()

        print('tf_output:', tf_output.shape)
        print('torch_output:', torch_output.shape)

        self.assertTrue(np.allclose(tf_output, torch_output, rtol=1e-5, atol=1e-6))


if __name__ == "__main__":
    unittest.main()
