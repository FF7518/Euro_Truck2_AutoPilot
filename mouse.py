# -*- encoding: utf-8 -*-
'''
@File    :   mouse.py    

@Time             @Author    @Version    @Description
------------      -------    --------    -----------
2021/4/30 13:00   FF7518     1.0         None
'''
import pyautogui as pag
import time

while True:
    time.sleep(0.5)
    x, y = pag.position()
    print(x, y)

