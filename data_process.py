# -*- encoding: utf-8 -*-
"""
@File    :   data_process.py    

@Time             @Author    @Version    @Description
------------      -------    --------    -----------
2021/5/6 20:54   FF7518     1.0         None
"""
import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle


# 对数据进行预处理
def preProcess():
    data = np.load('EuroTruck_v6_highway_sunny.npy', allow_pickle=True)
    print(data.shape)

    df = pd.DataFrame(data)
    images = df.iloc[:, 0]
    labels = df.iloc[:, 1]
    turn = []
    speed = []
    for i in labels:
        speed.append(i[0])
        turn.append(i[1])
    print(labels[1313])
    # print(df[1].value_counts())



if __name__ == '__main__':
    preProcess()
