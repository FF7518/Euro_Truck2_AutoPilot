# -*- encoding: utf-8 -*-
"""
@File    :   data.py    

@Time             @Author    @Version    @Description
------------      -------    --------    -----------
2021/5/7 12:25   FF7518     1.0         None
"""
# 加载数据集
from torch.utils.data import DataLoader, Dataset, random_split
from torchvision.transforms import ToTensor, Lambda
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt


class EuroTruckDataset(Dataset):

    def __init__(self, filepath, transform=None, target_transform=None):
        data = np.load(filepath, allow_pickle=True)
        df = pd.DataFrame(data)
        self.images = df.iloc[:, 0]
        # self.labels = df.iloc[:, 1]
        labels = df.iloc[:, 1]
        self.labels = []
        for l in labels:
            if l == 3:
                self.labels.append(0)
            else:
                self.labels.append(1)
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        image = self.images[idx]
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        dict_data = {
            'image': image,
            'label': label
        }
        return dict_data


def load_data(filepath):
    ETDataset = EuroTruckDataset(filepath)
    ETDataLoader = DataLoader(ETDataset,
                              batch_size=100,
                              shuffle=False)

    return ETDataLoader


def crop(image):
    pass


if __name__ == '__main__':
    et = load_data('../EuroTruck_v6_highway_test.npy')
    # print(len(et))
    dict_data = next(iter(et))
    image = dict_data['image']
    label = dict_data['label']
    print(label)
    # print(image[0])
    # plt.imshow(image[0], cmap='gray')
