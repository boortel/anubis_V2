#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 18:40:39 2020

@author: kratochvila
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

from base.base_net import BaseNet


class LOTUS_2conv(BaseNet):

    def __init__(self, width, height, rep_dim = 128):
        super().__init__()

        self.rep_dim = rep_dim
        self.width = width
        self.height = height
        self.pool = nn.MaxPool2d(2, 2)

        self.conv1 = nn.Conv2d(3, 32, 5, bias=False, padding=2)
        self.bn2d1 = nn.BatchNorm2d(32, eps=1e-04, affine=False)
        self.conv2 = nn.Conv2d(32, 64, 5, bias=False, padding=2)
        self.bn2d2 = nn.BatchNorm2d(64, eps=1e-04, affine=False)
        self.fc1 = nn.Linear(64 * int(self.width/4) * int(self.height/4), self.rep_dim, bias=False) # 20 * 15

    def forward(self, x):
        x = self.conv1(x)
        x = self.pool(F.leaky_relu(self.bn2d1(x)))
        x = self.conv2(x)
        x = self.pool(F.leaky_relu(self.bn2d2(x)))
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        return x


class LOTUS_Autoencoder_2conv(BaseNet):

    def __init__(self, width, height, rep_dim = 128):
        super().__init__()

        self.rep_dim = rep_dim
        self.width = width
        self.height = height
        self.pool = nn.MaxPool2d(2, 2)

        # Encoder (must match the Deep SVDD network above)
        self.conv1 = nn.Conv2d(3, 32, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.conv1.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d1 = nn.BatchNorm2d(32, eps=1e-04, affine=False)
        self.conv2 = nn.Conv2d(32, 64, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.conv2.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d2 = nn.BatchNorm2d(64, eps=1e-04, affine=False)
        self.fc1 = nn.Linear(64 * int(self.width/4) * int(self.height/4), self.rep_dim, bias=False)
        self.bn1d = nn.BatchNorm1d(self.rep_dim, eps=1e-04, affine=False)

        # Decoder
        self.deconv1 = nn.ConvTranspose2d(int(self.rep_dim / (self.width/4 * self.height/4)), 64, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.deconv1.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d3 = nn.BatchNorm2d(64, eps=1e-04, affine=False)
        self.deconv2 = nn.ConvTranspose2d(64, 32, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.deconv2.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d4 = nn.BatchNorm2d(32, eps=1e-04, affine=False)
        self.deconv3 = nn.ConvTranspose2d(32, 3, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.deconv3.weight, gain=nn.init.calculate_gain('leaky_relu'))

    def forward(self, x):
        x = self.conv1(x)
        x = self.pool(F.leaky_relu(self.bn2d1(x)))
        x = self.conv2(x)
        x = self.pool(F.leaky_relu(self.bn2d2(x)))
        x = x.view(x.size(0), -1)
        x = self.bn1d(self.fc1(x))
        x = x.view(x.size(0), int(self.rep_dim / (self.width/4 * self.height/4)), int(self.width/4), int(self.height/4))
        x = F.leaky_relu(x)
        x = self.deconv1(x)
        x = F.interpolate(F.leaky_relu(self.bn2d3(x)), scale_factor=2)
        x = self.deconv2(x)
        x = F.interpolate(F.leaky_relu(self.bn2d4(x)), scale_factor=2)
        x = self.deconv3(x)
        x = torch.sigmoid(x)
        return x