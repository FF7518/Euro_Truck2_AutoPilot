# -*- encoding: utf-8 -*-
"""
@File    :   PID.py

@Time             @Author    @Version    @Description
------------      -------    --------    -----------
2021/4/30 15:15   FF7518     1.0         None
"""
from Keys import Direct

def simpleCtrl(k1, k2):
    if k1 < 0 and k2 < 0:
        Direct.right(0.2)
    elif k1 > 0 and k2 > 0:
        Direct.left(0.2)
    else:
        pass

class PID:
    """
    PID Controller
    Piloting Direction Control
    """
    def __init__(self, k1, k2, P=0.2, I=0.0, D=0.0):

        self.k1 = k1
        self.k2 = k2

        self.Kp = P
        self.Ki = I
        self.Kd = D


