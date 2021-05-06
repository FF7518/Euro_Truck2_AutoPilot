import time

import cv2
import numpy as np
from PIL import ImageGrab
from mss import mss

from Keys import Direct

# 15 fps
from grab import Win32screen, convert2gray


def screen_mss():
    bounding_box = {
        'top': 40, 'left': 0,
        'width': 1024, 'height': 768
    }
    sct = mss()
    last_time = time.time()

    while True:
        sct_img = np.array(sct.grab(bounding_box))
        cvt_img, original_img = convert2gray(sct_img)
        # 原图
        cv2.imshow('original', original_img)
        # 灰度图
        # cv2.imshow('screen', cvt_img)
        # print('fps {} '.format(1 / (time.time() - last_time)))
        last_time = time.time()
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


# 10 fps
def screen_pil():
    last_time = time.time()
    bbox = Win32screen().window()
    while True:
        img = np.array(ImageGrab.grab(bbox=bbox))
        print('fps {} '.format(1 / (time.time() - last_time)))
        last_time = time.time()
        # cv2.resizeWindow('sync window', 640, 360)
        cv2.imshow('sync window', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    time.sleep(7)
    Direct.cruising()
    screen_mss()