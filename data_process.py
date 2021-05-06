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
    data = np.load('test.npy', allow_pickle=True)

    df = pd.DataFrame(data)
    print(df)



if __name__ == '__main__':
    preProcess()
