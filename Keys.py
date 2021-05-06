# -*- encoding: utf-8 -*-
"""
@File    :   Keys.py

@Time             @Author    @Version    @Description
------------      -------    --------    -----------
2021/4/30 12:35   FF7518     1.0         None
"""
import ctypes
import win32api as wapi
import time

SendInput = ctypes.windll.user32.SendInput

# define Direction Control
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

class keys:
    W = 0x11
    A = 0x1E
    S = 0x1F
    D = 0x20
    C = 0x2E


# redefine c structs
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Export Funtions
# Note that you need to use two together
def PressKey(hexKeyCode):
    """
    :param hexKeyCode: W A S D
    :return:
    """
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    """
    :param hexKeyCode: W A S D
    :return:
    """
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ClickKey(hexKeyCode):
    """
    Press and Release
    :param hexKeyCode: W A S D
    :return:
    """
    PressKey(hexKeyCode)
    ReleaseKey(hexKeyCode)

# Here is an example
def example_control():
    """
    1. run code
    2. switch into game in 5s
    """
    time.sleep(5)
    print('start')
    PressKey(W)
    time.sleep(10)
    ReleaseKey(W)
    print('stop')

# 方向控制
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
        time.sleep(3.5)
        ReleaseKey(keys.W)
        ClickKey(keys.C)

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

