from PIL import ImageGrab
import cv2

def grab():
    im = ImageGrab.grab()
    print(im.size)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    grab()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
