# -*- coding: utf-8 -*-
# http://pyladies.cz/v1/s016-micropython/index.html
# sudo screen /dev/ttyUSB0 115200
# http://docs.micropython.org/en/v1.8/esp8266/esp8266/tutorial/neopixel.html

from machine import Pin
from time import sleep
from machine import Pin, PWM

pin = Pin(14, Pin.OUT)
button = Pin(0, Pin.IN)

while True:
    print(button.value())

from time import sleep

while True:
    pin.value(0)
    sleep(one)
    pin.value(1)
    sleep(one)

pwm = PWM(pin, freq=50, duty=512)

import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.scan()
wlan.isconnected()
wlan.connect('borka', 'tohlejeheslo1')
wlan.isconnected()
wlan.ifconfig()

import socket


def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break


from machine import Pin, PWM
from time import sleep

pin_motorku = Pin(2, Pin.OUT)
pwm = PWM(pin_motorku, freq=50, duty=77)
pwm.duty(35)





