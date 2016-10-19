# -*- coding: utf-8 -*-

import network
import time
import socket
import neopixel
import machine

def start_AP():
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='blinkblink')


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('UPC2529191', 'YVDDNGMF')
        while not wlan.isconnected():
            time.sleep_ms(50)
    print('network config:', wlan.ifconfig())


def server_init():
    s = socket.socket()
    s.bind(('', 31337))
    s.listen(1)
    c, a = s.accept()
    print("Client connected")
    return c


def remoteRGB(s):
    n = neopixel.NeoPixel(machine.Pin(2, machine.Pin.OUT), 8)
    data = s.recv(3)
    for one in range(n.n):
        n[one] = data
    n.write()


do_connect()
server = server_init()

while True:
    remoteRGB(server)

"""
import socket
c = socket.socket()
c.connect( ('192.168.0.19', 31337) )
c.send("\x10\x2A\x0F")
c.send(chr(16) + chr(42) + chr(15))
"""
