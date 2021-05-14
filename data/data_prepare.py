# -*- encoding: utf-8 -*-
"""
@File    :   data_prepare.py

@Time             @Author    @Version    @Description
------------      -------    --------    -----------
2021/5/6 18:45   FF7518     1.0         准备训练数据
"""
# ----------------- INSTRUCTIONS FOR THIS CODE -------------------<
# 本代码用以制作自动驾驶数据集。
# 数据集格式： '{世界名称}_{版本 v1...}_{类型 direct-only,speed-only}_{size small,normal}.npy'
# 数据集为numpy文件，第1列：图像特征，[第2列：方向标签，第2列：速度标签]
# ----------------------------------------------------------------<


import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
import time

from common.screen import screen_pywin32
from common.keys import get_key, convertKey2ValDirectionOnly

from common.config import ScreenConfig, KeyConfig

# ----------------- CONFIGURATIONS -----------------------------<

"""
load configurations
"""
# SCREEN SIZE
DEFAULT_REGION = ScreenConfig.DEFAULT_REGION
# RESIZE
H = ScreenConfig.H
W = ScreenConfig.W
RESIZE_REGION = (W, H)


DEFAULT_DATA_SAVE_PATH = 'EuroTruck_v0_direct-only_small(auto).npy'


DEFAULT_DATA_SIZE_TINY = 300
DEFAULT_DATA_SIZE_SMALL = 1000
DEFAULT_DATA_SIZE_MIDDLE = 5000
DEFAULT_DATA_SIZE_LARGER = 10000


TRAIN_CONFIG = {
    'DATA_PATH': 'EuroTruck_v1_direct-only_normal.npy',
    'DATA_LENGTH': DEFAULT_DATA_SIZE_SMALL,
}
TEST_CONFIG = {
    'DATA_PATH': 'testtest.npy',
    'DATA_LENGTH': DEFAULT_DATA_SIZE_TINY,
}


# ------------------------------------------------------------------------<
#
#
# MAIN FUNCTIONS OF THE DATA PREPARING
#
#
# -------------------------------------------------------------------------<
def record(data_path=DEFAULT_DATA_SAVE_PATH, data_length=DEFAULT_DATA_SIZE_SMALL):
    print('RECORD will start in 3 sec\n'
          'instructions: Please keep car speed 50-60 km/h\n'
          'Press Z to pause\nPress Q to quit (will save)')
    i = 10
    while i != 0:
        print("time:", i, ", ", end="")
        time.sleep(0.5)
        i -= 1
    print(end='\n')

    training_data = []

    paused = False

    print('RECORD STARTING!!!')
    while True:
        if paused:
            # extra 包含了任务有关的按键，需要进行检查
            _, extra = get_key()
            if extra == KeyConfig.CMD_QUIT:
                np.save(data_path, np.array(training_data), allow_pickle=True)
                print('RECORD KEYBOARD INTERRUPT! DATA HAS BEEN SAVED')
                break
            if extra == KeyConfig.CMD_PAUSE:
                print('RECORD CONTINUE!')
                time.sleep(0.5)
                paused = False
        if not paused:
            screen = np.array(screen_pywin32(region=DEFAULT_REGION))

            # run a color convert:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            # resize to something a bit more acceptable for a CNN
            screen = cv2.resize(screen, RESIZE_REGION)
            # 只截取图像的下班部分（只保留道路信息）
            cut_start = H // 2 - 1
            cut_end = H - 1
            screen = screen[cut_start:cut_end, :]

            # 现在只考虑方向控制
            now_key, extra = get_key()

            if extra == KeyConfig.CMD_QUIT:
                np.save(data_path, np.array(training_data), allow_pickle=True)
                print('RECORD KEYBOARD INTERRUPT! DATA HAS BEEN SAVED')
                break
            if extra == KeyConfig.CMD_PAUSE:
                print('RECORD PAUSED!')
                time.sleep(0.5)
                paused = True

            output = convertKey2ValDirectionOnly(now_key)
            if output == 0:
                continue
            training_data.append([screen, output])

            print(len(training_data))

            if len(training_data) % data_length == 0 and len(training_data) > 0:
                np.save(data_path, np.array(training_data), allow_pickle=True)
                print('RECORD FINISHED!')
                break
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                print('RECORD EXIT')
                break


def read(data_path):
    train = np.load(data_path, allow_pickle=True)
    # fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    # path = 'EuroTruck_v6_highway_test.avi'
    # fps = 15
    # imgsize = (800, 300)
    # 灰度图要False
    # vw = cv2.VideoWriter(path, fourcc, fps, imgsize, False)

    for data in train:
        img = data[0]
        ctrl = data[1]
        print(img.shape, ctrl)
        img = cv2.resize(img, (8*W, 4*H))
        cv2.imshow('resized window', img)
        # vw.write(img)
        # print(vw.isOpened())

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    # vw.release()
    cv2.destroyAllWindows()


def main():
    print('collecting training data...')
    record(TRAIN_CONFIG['DATA_PATH'], TRAIN_CONFIG['DATA_LENGTH'])
    print('collecting testing data...')
    record(TEST_CONFIG['DATA_PATH'], TEST_CONFIG['DATA_LENGTH'])
    print('display after 2 sec')
    time.sleep(2)
    print('training data')
    read(TRAIN_CONFIG['DATA_PATH'])
    print('testing data')
    read(TEST_CONFIG['DATA_PATH'])


def display():
    read(TRAIN_CONFIG['DATA_PATH'])


if __name__ == '__main__':
    # main()
    display()
    pass
    STR = ''
