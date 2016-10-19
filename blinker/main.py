# -*- coding: utf-8 -*-
import time
from machine import Pin, Timer
from neopixel import NeoPixel
import uos

refresh_freq = 2000
random_freqs = []
butt = Pin(0, Pin.IN)
POCET_LED = 8
pin = Pin(2, Pin.OUT)
np = NeoPixel(pin, POCET_LED)
timer = Timer(-1)


def redraw(what):
    for i in range(POCET_LED):
        color = [max(15, int(r) - 50) for r in uos.urandom(3)]  # -50 not so bright
        if abs(color[0] - color[1]) < 15:
            color[0] += 20
        max_val = max(color)
        if color.index(max_val) == 2:
            color[2] = int(color[2] / 2)
        color[2] = max(15, color[2] - 40)  # ease on the blue
        # print(i, color)
        np[i] = color
    np.write()
    timer.init(period=refresh_freq, mode=Timer.PERIODIC, callback=redraw)


def set_refresh_freq(event):
    global refresh_freq
    refresh_freq -= 50
    if refresh_freq < 0:
        refresh_freq = 2000
    print(refresh_freq)


butt.irq(trigger=Pin.IRQ_FALLING, handler=set_refresh_freq)
timer.init(period=refresh_freq, mode=Timer.PERIODIC, callback=redraw)
timer.init(period=refresh_freq, mode=Timer.ONE_OFF, callback=redraw)
