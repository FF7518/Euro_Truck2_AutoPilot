"""

run
2021/5/11 22:30

=========================

INTRODUCTIONS

=========================
"""
import time

import cv2
import numpy as np

from common.config import ScreenConfig, KeyConfig
from common.screen import screen_pywin32
from common.keys import get_key
from common.control import Direct

from keras.models import load_model


MODEL_PATH = './tf_model/EuroTruck-alexnet-p1-normal-DirectOnly-6-epochs.h5'

SUCCESS_FLAG = True
FAIL_FLAG = False


def start(model_path=MODEL_PATH):
    try:
        model = load_model(model_path)
    except Exception as e:
        print('Model Loading Failed!')
        return FAIL_FLAG

    paused = False

    while True:
        if paused:
            _, extra = get_key()

            if extra == KeyConfig.CMD_QUIT:
                print('AUTO PILOT STOPPED!!!')
                cv2.destroyAllWindows()
                break

            if extra == KeyConfig.CMD_PAUSE:
                print('CONTINUE')
                time.sleep(0.5)
                paused = False

        if not paused:
            screen = screen_pywin32(region=ScreenConfig.DEFAULT_REGION)
            screen = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
            screen = cv2.resize(screen, ScreenConfig.RESIZE_REGION)
            cut_start = ScreenConfig.H // 2 - 1
            cut_end = ScreenConfig.H - 1
            screen = screen[cut_start:cut_end, :]
            cv2.imshow('original', screen)

            x = np.array(screen / 255.0).reshape(1, ScreenConfig.H // 2, ScreenConfig.W, 1)

            # 获得概率值
            P = model.predict(x)[0][0]
            # 回归的方向
            # _Y = 0 if P < 0.5 else 1
            _Y = 0
            if P > 0.5:
                _Y = 1
            # elif P > 0.0:
            #     _Y = -1
            # 控制w
            if _Y == 0:
                print(P, ' left')
                Direct.left(0.06)
            elif _Y == 1:
                print(P, ' right')
                Direct.right(0.06)

            _, extra = get_key()

            if extra == KeyConfig.CMD_PAUSE:
                print('PAUSED, PRESS Z TO CONTINUE')
                time.sleep(0.5)
                paused = True

            if extra == KeyConfig.CMD_QUIT:
                print('AUTO PILOT STOPPED!!!')
                cv2.destroyAllWindows()
                break

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    return SUCCESS_FLAG
