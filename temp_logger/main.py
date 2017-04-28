# screen  /dev/ttyUSB0 115200
import time
import dht
import socket
import machine

import network
import esp
import ssd1306
import gc

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')
else:
    print('power on or hard reset')

dht22_pin = machine.Pin(14, machine.Pin.IN)  # 5
dht22 = dht.DHT22(dht22_pin)

i2c = machine.I2C(sda=machine.Pin(5), scl=machine.Pin(4))
display = ssd1306.SSD1306_I2C(128, 64, i2c)


def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.1\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break


def display_text(text):
    display.fill(0)
    display.text(text, 0, 0)
    display.show()


def display_values(first_line=('Oh Hi Temp!', 20, 0)):
    line_height = 12
    display.fill(0)
    display.text(first_line[0], first_line[1], first_line[2])
    display.text('Temp: {:.1f} C'.format(dht22.temperature()), 0, 5 + line_height)
    display.text('Humi: {:.1f} %'.format(dht22.humidity()), 0, 5 + line_height * 2)
    display.text('GC free:{}'.format(gc.mem_free()), 0, 5 + line_height * 3)
    display.show()


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    attempt = 1
    if not wlan.isconnected():
        with open('wifi.txt') as f:
            wname, wpass = f.readline().split()

        print('connecting to network...')
        display_values(first_line=('{} log to {}'.format(attempt, wname), 0, 0))
        wlan.connect(wname, wpass)
        while not wlan.isconnected():
            time.sleep_ms(100)
            attempt += 1
            display_values(first_line=('{} log to {}'.format(attempt, wname), 0, 0))
    display_values(first_line=('net:{}'.format(wlan.ifconfig()), 0, 0))
    print('network config:', wlan.ifconfig())
    time.sleep(1)


display_text('measuring...')
time.sleep(1)
dht22.measure()
print('t:', dht22.temperature(), 'h:', dht22.humidity())
do_connect()
display_values()
http_get('http://api.thingspeak.com/update?api_key=QFII8JXOBUBJ4EVP&field4={}&field5={}'.format(
    dht22.temperature(), dht22.humidity()))

print('GC alloc:{} free:{}'.format(gc.mem_alloc(), gc.mem_free()))
gc.collect()
esp.deepsleep(1000000 * 60 * 3)
