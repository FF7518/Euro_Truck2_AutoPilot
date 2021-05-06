# -*- encoding: utf-8 -*-
"""
@File    :   data_prepare.py

@Time             @Author    @Version    @Description
------------      -------    --------    -----------
2021/5/6 18:45   FF7518     1.0         准备训练数据
"""
# X : 图像
# Y : 控制流

import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
import time

# 使用pywin32获取窗口
def screen_pywin32(region=None):
    """
    :param region: 区域
    :return:
    """
    hwin = win32gui.GetDesktopWindow()

    if region:
        left,top,x2,y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

# 获取控制信息
keyList = ["\b"]

for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
    keyList.append(char)

def key_check():
    keys = []
    for key in keyList:
        if win32api.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys

# 控制流应该包含2类信息：
# 1.加速、减速
# 2.左转、右转
def get_key():
    key = key_check()

    ctrl = np.zeros([2,2])
    #  [ [ w s ]
    #    [ a d ] ]
    # w [0][0]
    # s [0][1]
    # a [1][0]
    # d [1][1]
    if 'W' in key:
        ctrl[0][0] = 1
    if 'S' in key:
        ctrl[0][1] = 1
    if 'A' in key:
        ctrl[1][0] = 1
    if 'D' in key:
        ctrl[1][1] = 1

    return ctrl

def screen_record():
    i = 3
    while i != 0:
        print("time:", i)
        time.sleep(0.5)
        i -= 1
    training_data = []
    last_time = time.time()
    paused = False
    print('RECORD STARTING!!!')
    while True:
        if not paused:
            screen = np.array(screen_pywin32(region=(0, 40, 1024, 768)))
            last_time = time.time()

            # run a color convert:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            # resize to something a bit more acceptable for a CNN
            # screen = cv2.resize(screen, (80, 60))
            # get key datamat
            output = get_key()
            training_data.append([screen, output])
            print(len(training_data))
            # cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
            if len(training_data) % 500 == 0:
                np.save('test.npy', np.array(training_data), allow_pickle=True)
                print('ok')
                break
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

def read_test():
    train = np.load('test.npy', allow_pickle=True)
    cv2.resizeWindow('good', 1024, 40)
    for data in train:
        img = data[0]
        ctrl = data[1]
        cv2.imshow('frame ctrl {}'.format(ctrl), img)
        print(img.shape, ctrl)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    cv2.destroyAllWindows()



if __name__ == '__main__':
    # screen_record()
    read_test()