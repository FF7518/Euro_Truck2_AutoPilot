"""

control
2021/5/11 20:42

=========================

INTRODUCTIONS

=========================
"""
import time

from keys import PressKey, ReleaseKey, keys


# Direction Controller
class Direct:
    # 加油门
    @staticmethod
    def forward():
        PressKey(keys.W)

    # 起步至定速巡航
    @staticmethod
    def cruising():
        time.sleep(1)
        PressKey(keys.W)
        time.sleep(3)
        ReleaseKey(keys.W)
        PressKey(keys.C)
        ReleaseKey(keys.C)

    # left
    @staticmethod
    def left(delay=0):
        PressKey(keys.A)
        time.sleep(delay)
        ReleaseKey(keys.A)

    # right
    @staticmethod
    def right(delay=0):
        PressKey(keys.D)
        time.sleep(delay)
        ReleaseKey(keys.D)
