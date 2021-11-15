import os
import sys
import random
import unittest

import numpy as np
import torch

from mlc.models import tensorflow_impl, pytorch_impl


class InterOpsTestCase(unittest.TestCase):

    def setUp(self):
        self.seed = 42

    def test_fully_connected_compatability(self):
        input_size = 4
        output_size = 8
        inputs = np.random.uniform(-1.0, 1.0, (1, input_size))

        tf_model = tensorflow_impl.FullyConnectedModel(input_size, output_size)
        torch_model = pytorch_impl.FullyConnectedModel(input_size, output_size)

        tf_output = tf_model(inputs).numpy()
        _ = torch_model(inputs)

        w, b = tf_model.get_weights()
        for m in tuple(torch_model.modules())[1:]:
            m.weight.data = torch.from_numpy(np.transpose(w))
            m.bias.data = torch.from_numpy(b)

        torch_output = torch_model(inputs).detach().numpy()

        self.assertTrue(np.allclose(tf_output, torch_output, rtol=1e-5, atol=1e-6))

    def test_lstm_compatibility(self):
        input_size = 4
        output_size = 8
        inputs = np.random.uniform(-1.0, 1.0, (1, 1, input_size))

        tf_model = tensorflow_impl.TimeSeriesModel(input_size, output_size)
        torch_model = pytorch_impl.TimeSeriesModel(input_size, output_size)

        tf_output = tf_model(inputs).numpy()
        _ = torch_model(inputs)

        w_ih, w_hh, b = tf_model.get_weights() # [(4, 32), (8, 32), (32,)]
        for m in tuple(torch_model.modules())[1:]:
            for name, param in m.named_parameters():
                if 'weight_ih' in name:
                    param.data = torch.from_numpy(np.transpose(w_ih))
                elif 'weight_hh' in name:
                    param.data = torch.from_numpy(np.transpose(w_hh))
                elif 'bias' in name:
                    param.data = torch.from_numpy(b)

        torch_output, _ = torch_model(inputs)
        torch_output = torch_output.detach().numpy()

        self.assertTrue(np.allclose(tf_output, torch_output, rtol=1e-5, atol=1e-6))


if __name__ == "__main__":
    unittest.main()
