# -*- encoding: utf-8 -*-
"""
@File    :   data.py    

@Time             @Author    @Version    @Description
------------      -------    --------    -----------
2021/5/9 22:25   FF7518     1.0         None
"""
import numpy as np

CHANNEL_GRAY = 1
CHANNEL_RGB = 3


def load_dataset(dataset_path: str):
    data = np.load(dataset_path, allow_pickle=True)

    images = data[:, 0] / 255.0
    labels = data[:, 1]

    NUM_samples = images.size
    _S = images[0].shape
    H = _S[0]
    W = _S[1]
    C = CHANNEL_GRAY

    X = np.array([i for i in images]).reshape(NUM_samples, H, W, C)
    print(X.shape)
    Y = np.array([0 if i == 3 else 1 for i in labels])

    return X, Y, NUM_samples, H, W, C

