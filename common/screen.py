"""

screen
2021/5/11 19:46

=========================

INTRODUCTIONS

=========================
"""
import cv2
import numpy as np

import win32gui, win32ui, win32con, win32api

from mss import mss
from PIL import ImageGrab
from config import ScreenConfig

DEFAULT_REGION = ScreenConfig.DEFAULT_REGION  # SCREEN ORIGINAL SIZE
# RESIZE
H = ScreenConfig.H
W = ScreenConfig.W
RESIZE_REGION = (W, H)


def screen_pywin32(region=None, color=None):
    hwin = win32gui.GetDesktopWindow()

    if region:
        left, top, x2, y2 = region
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
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    if color == 'gray' or color == 'GRAY':
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif color == 'rgb' or color == 'RGB':
        return img
    else:
        return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)


def screen_mss(region=None, color=None):
    if region is None:
        region = DEFAULT_REGION

    sct = mss()
    img = np.array(sct.grab(region))
    sct.close()

    if color == 'gray' or color == 'GRAY':
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif color == 'rgb' or color == 'RGB':
        return img
    else:
        return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)


def screen_PIL(region=None, color=None):
    if region is None:
        region = DEFAULT_REGION

    img = np.array(ImageGrab.grab(bbox=region))

    if color == 'gray' or color == 'GRAY':
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif color == 'rgb' or color == 'RGB':
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        return img


if __name__ == '__main__':
    while True:
        img = screen_mss(region=DEFAULT_REGION)
        cv2.imshow('test', img)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
