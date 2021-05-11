# -*- encoding: utf-8 -*-
"""
@File    :   model.py    

@Time             @Author    @Version    @Description
------------      -------    --------    -----------
2021/5/8 13:38   FF7518     1.0         None
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

class EuroTruckModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 10, (5, 5))
        self.conv2 = nn.Conv2d(10, 20, (5, 5))
        self.pool = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(65960, 2)

    def forward(self, x):
        batch_size = x.size(0)
        # print('[#1]')
        # print(x.shape)
        x = self.pool(self.conv1(x))
        # print('[#2]')
        # print(x.shape)
        x = F.relu(self.pool(self.conv2(x)))
        x = x.view(batch_size, -1)
        print(x.shape)
        x = torch.squeeze(self.fc1(x), 1)
        print(x.shape, x)
        # x = torch.relu(x)
        # print(x.shape)
        return x
