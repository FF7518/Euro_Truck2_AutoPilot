# -*- encoding: utf-8 -*-
"""
@File    :   train.py    

@Time             @Author    @Version    @Description
------------      -------    --------    -----------
2021/5/11 13:57   FF7518     1.0         None
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from model import EuroTruckModel

from data import load_dataset


def main():

    X, Y, num_samples, H, W, C = load_dataset('../data/EuroTruck_v6_highway_direct-only_train.npy')
    input_shape = (H, W, C)
    train_x, test_x, train_y, test_y = train_test_split(X, Y, train_size=0.8, test_size=0.2, random_state=0)

    net = EuroTruckModel(input_shape=input_shape).m_compile()

    history = net.fit(train_x,
                      train_y,
                      epochs=4,
                      batch_size=64)

    loss, acc = net.evaluate(test_x, test_y)
    print('loss = {}'.format(loss))
    print('acc = {}'.format(acc))

    turn = net.predict(np.array(test_x[100]).reshape(1, H, W, 1))
    print(turn)


if __name__ == '__main__':
    main()