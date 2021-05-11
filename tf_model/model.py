# -*- encoding: utf-8 -*-
"""
@File    :   model.py    

@Time             @Author    @Version    @Description
------------      -------    --------    -----------
2021/5/9 21:33   FF7518     1.0         None
"""
from keras import layers
from keras import models
from keras import optimizers


class EuroTruckModel:

    def __init__(self, input_shape=None):
        H = 30
        W = 80
        C = 1
        if input_shape is None:
            input_shape = (H, W, C)

        model = models.Sequential()
        model.add(layers.Conv2D(filters=32, kernel_size=(5, 5), activation='relu', input_shape=input_shape))
        model.add(layers.MaxPooling2D((2, 2)))
        # model.add(layers.Conv2D(filters=64, kernel_size=(5, 5), activation='relu'))
        # model.add(layers.MaxPooling2D((2, 2)))

        model.add(layers.Flatten())
        model.add(layers.Dense(32, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))

        self.model = model

    def m_compile(self, p_loss=None, p_optimizer=None, p_lr=None, p_metrics=None):
        LR = 1e-4
        LOSS = 'binary_crossentropy'
        OPTIMIZER = optimizers.RMSprop(LR)
        METRICS = 'acc'

        self.model.compile(loss=LOSS,
                           optimizer=OPTIMIZER,
                           metrics=[METRICS])

        return self.model

    # def m_fit(self, train_x, train_y, epoch, batch_size):
    #     self.model.fit(train_x, train_y, epochs=epoch, batch_size=batch_size)