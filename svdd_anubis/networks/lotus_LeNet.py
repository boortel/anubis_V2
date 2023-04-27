#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 17:14:38 2022

@author: kratochvila
"""
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


class LOTUS_LeNet(BaseNet):

    def __init__(self, width, height, rep_dim = 128):
        super().__init__()

        self.rep_dim = rep_dim
        self.width = width
        self.height = height
        self.pool = nn.MaxPool2d(2, 2)

        self.conv11 = nn.Conv2d(3, 32, 5, bias=False, padding=2)
        self.bn2d11 = nn.BatchNorm2d(32, eps=1e-04, affine=False)
        self.conv21 = nn.Conv2d(32, 64, 5, bias=False, padding=2)
        self.bn2d21 = nn.BatchNorm2d(64, eps=1e-04, affine=False)
        self.conv31 = nn.Conv2d(64, 128, 5, bias=False, padding=2)
        self.bn2d31 = nn.BatchNorm2d(128, eps=1e-04, affine=False)
        
        self.conv12 = nn.Conv2d(3, 32, 5, bias=False, padding=2)
        self.bn2d12 = nn.BatchNorm2d(32, eps=1e-04, affine=False)
        self.conv22 = nn.Conv2d(32, 64, 5, bias=False, padding=2)
        self.bn2d22 = nn.BatchNorm2d(64, eps=1e-04, affine=False)
        self.conv32 = nn.Conv2d(64, 128, 5, bias=False, padding=2)
        self.bn2d32 = nn.BatchNorm2d(128, eps=1e-04, affine=False)
        
        self.fc1 = nn.Linear(128 * int(self.width/8) * int(self.height/8), self.rep_dim, bias=False) # 20 * 15 80 * 60

    def forward(self, x):
        x, y = torch.chunk(x,2,dim=-1)
        x = torch.squeeze(x,dim=-1)
        y = torch.squeeze(y,dim=-1)
        
        x = self.conv11(x)
        x = self.pool(F.leaky_relu(self.bn2d11(x)))
        x = self.conv21(x)
        x = self.pool(F.leaky_relu(self.bn2d21(x)))
        x = self.conv31(x)
        x = self.pool(F.leaky_relu(self.bn2d31(x)))
        x = x.view(x.size(0), -1)
        
        y = self.conv12(y)
        y = self.pool(F.leaky_relu(self.bn2d12(y)))
        y = self.conv22(y)
        y = self.pool(F.leaky_relu(self.bn2d22(y)))
        y = self.conv32(y)
        y = self.pool(F.leaky_relu(self.bn2d32(y)))
        y = y.view(y.size(0), -1)
        
        z = torch.concat((x,y), dim=1)
        z = self.fc1(z)
        return z


class LOTUS_LeNet_Autoencoder(BaseNet):

    def __init__(self, width, height, rep_dim = 128):
        super().__init__()
        

        self.rep_dim = rep_dim
        self.width = width
        self.height = height
        self.pool = nn.MaxPool2d(2, 2)

        # Encoder (must match the Deep SVDD network above)
        self.conv11 = nn.Conv2d(3, 32, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.conv11.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d11 = nn.BatchNorm2d(32, eps=1e-04, affine=False)
        self.conv21 = nn.Conv2d(32, 64, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.conv21.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d21 = nn.BatchNorm2d(64, eps=1e-04, affine=False)
        self.conv31 = nn.Conv2d(64, 128, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.conv31.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d31 = nn.BatchNorm2d(128, eps=1e-04, affine=False)
        
        
        self.conv12 = nn.Conv2d(3, 32, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.conv12.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d12 = nn.BatchNorm2d(32, eps=1e-04, affine=False)
        self.conv22 = nn.Conv2d(32, 64, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.conv22.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d22 = nn.BatchNorm2d(64, eps=1e-04, affine=False)
        self.conv32 = nn.Conv2d(64, 128, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.conv32.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d32 = nn.BatchNorm2d(128, eps=1e-04, affine=False)
        
        self.fc1 = nn.Linear(128 * int(self.width/8) * int(self.height/8), self.rep_dim, bias=False)
        self.bn1d = nn.BatchNorm1d(self.rep_dim, eps=1e-04, affine=False)

        # Decoder
        self.deconv11 = nn.ConvTranspose2d(int(self.rep_dim / (self.width/8 * self.height/8)), 128, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.deconv11.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d41 = nn.BatchNorm2d(128, eps=1e-04, affine=False)
        self.deconv21 = nn.ConvTranspose2d(128, 64, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.deconv21.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d51 = nn.BatchNorm2d(64, eps=1e-04, affine=False)
        self.deconv31 = nn.ConvTranspose2d(64, 32, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.deconv31.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d61 = nn.BatchNorm2d(32, eps=1e-04, affine=False)
        self.deconv41 = nn.ConvTranspose2d(32, 3, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.deconv41.weight, gain=nn.init.calculate_gain('leaky_relu'))
        
        self.deconv12 = nn.ConvTranspose2d(int(self.rep_dim / (self.width/8 * self.height/8)), 128, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.deconv12.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d42 = nn.BatchNorm2d(128, eps=1e-04, affine=False)
        self.deconv22 = nn.ConvTranspose2d(128, 64, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.deconv22.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d52 = nn.BatchNorm2d(64, eps=1e-04, affine=False)
        self.deconv32 = nn.ConvTranspose2d(64, 32, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.deconv32.weight, gain=nn.init.calculate_gain('leaky_relu'))
        self.bn2d62 = nn.BatchNorm2d(32, eps=1e-04, affine=False)
        self.deconv42 = nn.ConvTranspose2d(32, 3, 5, bias=False, padding=2)
        nn.init.xavier_uniform_(self.deconv42.weight, gain=nn.init.calculate_gain('leaky_relu'))

    def forward(self, x):
        x, y = torch.chunk(x,2,dim=-1)
        x = torch.squeeze(x,dim=-1)
        y = torch.squeeze(y,dim=-1)
        
        x = self.conv11(x)
        x = self.pool(F.leaky_relu(self.bn2d11(x)))
        x = self.conv21(x)
        x = self.pool(F.leaky_relu(self.bn2d21(x)))
        x = self.conv31(x)
        x = self.pool(F.leaky_relu(self.bn2d31(x)))
        x = x.view(x.size(0), -1)
        
        y = self.conv12(y)
        y = self.pool(F.leaky_relu(self.bn2d12(y)))
        y = self.conv22(y)
        y = self.pool(F.leaky_relu(self.bn2d22(y)))
        y = self.conv32(y)
        y = self.pool(F.leaky_relu(self.bn2d32(y)))
        y = y.view(y.size(0), -1)

        z = torch.concat((x,y), dim=1)
        z = self.bn1d(self.fc1(z))

        z = z.view(z.size(0), int(self.rep_dim / (self.width/8 * self.height/8)), int(self.width/8), int(self.height/8))
        z = F.leaky_relu(z)
        
        x = self.deconv11(z)
        x = F.interpolate(F.leaky_relu(self.bn2d41(x)), scale_factor=2)
        x = self.deconv21(x)
        x = F.interpolate(F.leaky_relu(self.bn2d51(x)), scale_factor=2)
        x = self.deconv31(x)
        x = F.interpolate(F.leaky_relu(self.bn2d61(x)), scale_factor=2)
        x = self.deconv41(x)
        x = torch.sigmoid(x)
        
        y = self.deconv12(z)
        y = F.interpolate(F.leaky_relu(self.bn2d42(y)), scale_factor=2)
        y = self.deconv22(y)
        y = F.interpolate(F.leaky_relu(self.bn2d52(y)), scale_factor=2)
        y = self.deconv32(y)
        y = F.interpolate(F.leaky_relu(self.bn2d62(y)), scale_factor=2)
        y = self.deconv42(y)
        y = torch.sigmoid(y)
        
        z = torch.stack((x,y), dim=-1)
        return z
