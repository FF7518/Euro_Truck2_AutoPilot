"""

keys
2021/5/11 20:31

=========================

INTRODUCTIONS

=========================
"""
import win32gui, win32ui, win32con, win32api
import ctypes
import time
import numpy as np

from config import KeyConfig

"""
~~~~~~~~~~~~~~~~~~~~~~~~~
        sensor
~~~~~~~~~~~~~~~~~~~~~~~~~
"""

keyList = ["\b"]

for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
    keyList.append(char)


def key_check():

    keys = []
    for key in keyList:
        if win32api.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys


def get_key():

    key = key_check()

    ctrl = list(np.zeros([4]).astype(np.uint8))
    # [w s a d]
    # [0,0,0,0]

    # 其他按键，如有关退出的按键q
    extra = None

    if 'W' in key:
        ctrl[0] = 1
    if 'S' in key:
        ctrl[1] = 1
    if 'A' in key:
        ctrl[2] = 1
    if 'D' in key:
        ctrl[3] = 1

    if 'Z' in key:
        extra = 'Pause'
    if 'Q' in key:
        extra = 'Quit'

    return ctrl, extra


# 将ctrl转成整数 只考虑转向
def convertKey2ValDirectionOnly(key: list) -> int:
    # 按下A
    if key[2]:
        return KeyConfig.A
    # 按下D
    elif key[3]:
        return KeyConfig.D
    else:
        return KeyConfig.RELEASED


def convertKey2ValSpeedOnly(key: list) -> int:
    # 按下W
    if key[0]:
        return KeyConfig.W
    # 按下S
    elif key[1]:
        return KeyConfig.S
    else:
        return KeyConfig.RELEASED


"""
~~~~~~~~~~~~~~~~~~~~~~~~~
        control
~~~~~~~~~~~~~~~~~~~~~~~~~
"""

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
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# control functions
def PressKey(hexKeyCode):
    """
    :param hexKeyCode: W A S D
    :return:
    """
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    """
    :param hexKeyCode: W A S D
    :return:
    """
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


