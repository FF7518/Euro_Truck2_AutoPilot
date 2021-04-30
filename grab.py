import numpy as np
from PIL import ImageGrab
import cv2
import time
import win32gui
from mss import mss


class Win32screen:
    def __init__(self):
        self.toplist, self.winlist = [], []

    def enum_cb(self, hwnd, results):
        self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    def window(self):
        win32gui.EnumWindows(self.enum_cb, self.toplist)
        truck = [(hwnd, title) for hwnd, title in self.winlist if 'euro truck' in title.lower()]
        truck = truck[0]
        hwnd = truck[0]

        win32gui.SetForegroundWindow(hwnd)
        bbox = win32gui.GetWindowRect(hwnd)
        return bbox


# 返回mask区域
def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

# 绘制道路线条
def roadline(img, lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(img=img, pt1=(coords[0], coords[1]),
                     pt2=(coords[2], coords[3]), color=[255, 255, 255],
                     thickness=3)
    except Exception as e:
        print(e)

# 边缘检测
# masked
'''
masked area

    400,280-------------------730,280
     /                            \
    /                              \
250,410-------------------------880,410
    |                               |
    |                               |
250,520-------------------------880,520

'''
def convert2gray(img):
    # gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # canny
    gray = cv2.Canny(gray, threshold1=100, threshold2=200)
    # 高斯模糊
    gray = cv2.GaussianBlur(gray, ksize=(5,5), sigmaX=0)
    # mask
    vertices = np.array([
        [250, 520],
        [250, 410],
        [400, 280],
        [730, 280],
        [880, 410],
        [880, 520],
    ])
    gray = roi(gray, [vertices])
    # 霍夫变换
    lines = cv2.HoughLinesP(gray, rho=1, theta=np.pi / 180, threshold=180,
                           minLineLength=30, maxLineGap=10)
    roadline(gray, lines)

    return gray


# 15 fps
def screen_mss():
    bounding_box = {
        'top': 40, 'left': 0,
        'width': 1024, 'height': 768
    }
    sct = mss()
    last_time = time.time()

    while True:
        sct_img = np.array(sct.grab(bounding_box))
        gray_img = convert2gray(sct_img)
        cv2.imshow('screen', gray_img)
        print('fps {} '.format(1 / (time.time() - last_time)))
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
    screen_mss()
