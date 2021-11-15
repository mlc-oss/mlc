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


class TimeSeriesModel(nn.Module):

    def __init__(self, input_shape, output_shape):
        super(TimeSeriesModel, self).__init__()
        self.rnn = nn.LSTM(input_size=input_shape, hidden_size=output_shape, batch_first=True)

    def forward(self, x):
        x = torch.from_numpy(x).float()
        return self.rnn(x)


if __name__ == "__main__":
    input_shape = 4
    output_shape = 8

    model = FullyConnectedModel(input_shape=input_shape, output_shape=output_shape)
    inputs = np.random.uniform(-1.0, 1.0, (1, input_shape))
    output = model(inputs)
    print(f'FullyConnectedModel: {inputs.shape} -> {output.shape}')

    model = TimeSeriesModel(input_shape=input_shape, output_shape=output_shape)
    inputs = np.random.uniform(-1.0, 1.0, (1, 1, input_shape))
    output, hidden = model(inputs)
    print(f'TimeSeriesModel: {inputs.shape} -> {output.shape} ({hidden[0].shape}, {hidden[1].shape}')
