# -*- coding: utf-8 -*-
"""
Define the architecture of deep neural networks.

Created on Wed Jul 27 22:30:20 2022
@author: Yuxiao Yi
"""

import torch
from torch import Tensor, nn
import torch.nn.functional as F
import math

##custom activation functions
class SReLU(nn.Module):

    def __init__(self):
        super(SReLU, self).__init__()

    def forward(self, x):
        y = torch.pow(F.relu(x), 2)-3*torch.pow(F.relu(x-1), 2) + \
            3*torch.pow(F.relu(x-2), 2)-torch.pow(F.relu(x-3), 2)
        return y


class Sin(nn.Module):

    def __init__(self):
        super(Sin, self).__init__()

    def forward(self, x):
        return torch.sin(x)


class CustomGELU(nn.Module):

    def __init__(self):
        super(CustomGELU, self).__init__()
        self.torch_PI = 3.1415926536  #used for custom gelu

    def forward(self, x):
        return 0.5 * x * (1 + torch.tanh(
            math.sqrt(2 / self.torch_PI) * (x + 0.044715 * torch.pow(x, 3))))


##neural network architecture
class FeedForwardNet(nn.Module):

    def __init__(self, args, Actfuns):
        super(FeedForwardNet, self).__init__()
        neurons = args.layers
        self.depth = len(neurons) - 1
        self.actfun = Actfuns[args.actfun]
        self.layers = []
        for i in range(self.depth - 1):
            self.layers.append(nn.Linear(neurons[i], neurons[i + 1]))
            self.layers.append(self.actfun)
        self.layers.append(nn.Linear(neurons[-2], neurons[-1]))  # last layer
        # self.layers.append(nn.Sigmoid())
        self.fc = nn.Sequential(*self.layers)

    def forward(self, x):
        x = self.fc(x)
        return x


class ResNet(nn.Module):

    def __init__(self, args, Actfuns):
        super(ResNet, self).__init__()
        neurons = args.layers
        self.depth = len(neurons) - 1
        self.actfun = Actfuns[args.actfun]
        self.layers = []
        for i in range(self.depth - 1):
            self.layers.append(nn.Linear(neurons[i], neurons[i + 1]))
            self.layers.append(self.actfun)
        self.layers.append(nn.Linear(neurons[-2], neurons[-1]))
        # self.layers.append(nn.Sigmoid())
        self.fc = nn.Sequential(*self.layers)

    def forward(self, x):
        dx = self.fc(x)
        return x + dx


#Xu. et al propose Multi-scale DNN :https://arxiv.org/abs/2007.11207
#custom activation function SReLU(), see page 6
class MultiscaleLinear(nn.Linear):

    def __init__(self,
                 in_features: int,
                 out_features: int,
                 scale: list,
                 bias: bool = True) -> None:
        super().__init__(in_features, out_features, bias=bias)
        # self.scaleMatrix = torch.eye(self.out_features, self.out_features)
        length = len(scale)
        diagElement = torch.ones(self.out_features)
        unitEach = int(np.floor(self.out_features / length))
        for i in range(length - 1):
            diagElement[i * unitEach:(i + 1) * unitEach] = scale[i]
        diagElement[(length - 1) * unitEach:] = scale[-1]

        self.scaleMatrix = torch.diag_embed(diagElement)
        self.register_buffer('buffer', self.scaleMatrix)
        # logging.info(self.scaleMatrix)

    def forward(self, input: Tensor) -> Tensor:
        weight = torch.mm(self.buffer, self.weight)
        return F.linear(input, weight, self.bias)


class MultiscaleNet(nn.Module):

    def __init__(self, args, Actfuns):
        super(MultiscaleNet, self).__init__()
        neurons = args.layers
        self.depth = len(neurons) - 1
        self.actfun = Actfuns[args.actfun]
        self.layers = []

        mscaleLayer = MultiscaleLinear(neurons[0], neurons[1], args.scale)
        self.layers.append(mscaleLayer)
        self.layers.append(SReLU())

        for i in range(1, self.depth - 1):
            self.layers.append(nn.Linear(neurons[i], neurons[i + 1]))
            self.layers.append(self.actfun)

        self.layers.append(nn.Linear(neurons[-2], neurons[-1]))  # 最后一层
        # self.layers.append(nn.Sigmoid())
        self.fc = nn.Sequential(*self.layers)  # * is useful

    def forward(self, x):
        x = self.fc(x)
        return x