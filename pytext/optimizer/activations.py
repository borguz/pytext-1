#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import math

import torch
import torch.nn as nn
from pytext.config.module_config import Activation


class GeLU(nn.Module):
    """
    Implements Gaussian Error Linear Units (GELUs). Note: x * x * x is used
    instead of torch.pow(x, 3) due to issues with ONNX compatibility:
    https://github.com/pytorch/pytorch/issues/18475

    Reference:
    Gaussian Error Linear Units (GELUs). Dan Hendrycks, Kevin Gimpel.
    Technical Report, 2017. https://arxiv.org/pdf/1606.08415.pdf
    """

    def forward(self, x):
        return (
            0.5
            * x
            * (1 + torch.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * (x * x * x))))
        )


def get_activation(name):
    if name == Activation.RELU:
        return nn.ReLU()
    elif name == Activation.LEAKYRELU:
        return nn.LeakyReLU()
    elif name == Activation.TANH:
        return torch.tanh
    elif name == Activation.GELU:
        return GeLU()
    elif name == Activation.GLU:
        return nn.GLU(dim=1)
    else:
        raise RuntimeError(f"{name} is not supported")
