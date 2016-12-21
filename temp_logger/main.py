import time
import dht
import socket
import machine
import onewire
import ds18x20
import network
import esp
import ssd1306
import gc

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')
else:
    print('power on or hard reset')

dht_pin = machine.Pin(14, machine.Pin.IN) #5
dht22_pin = machine.Pin(13, machine.Pin.IN) #7
ds18_pin = machine.Pin(12) #6
dht11 = dht.DHT11(dht_pin)
dht22 = dht.DHT22(dht22_pin)

ds = ds18x20.DS18X20(onewire.OneWire(ds18_pin))
roms = ds.scan()

i2c = machine.I2C(sda=machine.Pin(5), scl=machine.Pin(4))
display = ssd1306.SSD1306_I2C(128,64,i2c)

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


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    #wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('UPC2529191', 'YVDDNGMF')
        #wlan.connect('Hnizdo', 'Holub1pristal')
        while not wlan.isconnected():
            time.sleep_ms(50)
    print('network config:', wlan.ifconfig())


def display_values():
    line_height = 12
    display.fill(0)
    display.text('Hi Lucinka!',20,0)
    display.text('D2 t:{:.1f} h:{:.1f}'.format(dht22.temperature(), dht22.humidity()),0, 5 + line_height)
    display.text('D1 t:{} h:{}'.format(dht11.temperature(), dht11.humidity()),0,5 + line_height*2)
    display.text('TE t:{:.1f}'.format(ds18_temp),0,5 + line_height*3)
    display.text('GC free:{}'.format(gc.mem_free()),0,5 + line_height*4)
    display.show()


ds.convert_temp()
time.sleep(2)
dht11.measure()
dht22.measure()
ds18_temp = ds.read_temp(roms[0])
if ds18_temp > 80: # first measurement is usually off
    esp.deepsleep(1000000*10)
print('dht11 t:', dht11.temperature(), 'dht11 h:', dht11.humidity(), 'dht22 t:', dht22.temperature(), 'dht22 h:',dht22.humidity(), 'temp:', ds18_temp)
do_connect()
http_get('http://api.thingspeak.com/update?api_key=QFII8JXOBUBJ4EVP&field1={}&field2={}&field3={}&field4={}&field5={}'.format(
    dht11.temperature(), dht11.humidity(), ds18_temp, dht22.temperature(), dht22.humidity()))
esp.deepsleep(1000000*60*2)
display_values()
print('GC alloc:{} free:{}'.format(gc.mem_alloc(), gc.mem_free()))
gc.collect()

