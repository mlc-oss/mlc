import torch
import torch.nn as nn
import numpy as np


class FullyConnectedModel(nn.Module):

    def __init__(self, input_shape, output_shape):
        super(FullyConnectedModel, self).__init__()
        self.linear = nn.Linear(input_shape, output_shape)

    def forward(self, x):
        x = torch.from_numpy(x).float()
        return self.linear(x)


if __name__ == "__main__":
    input_shape = 4
    output_shape = 8
    model = FullyConnectedModel(input_shape=input_shape, output_shape=output_shape)
    inputs = np.random.uniform(-1.0, 1.0, (1, input_shape))
    output = model(inputs)
    print(f'{inputs.shape} -> {output.shape}')
