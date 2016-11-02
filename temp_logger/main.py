import time
import dht
import socket
import machine
import onewire
import ds18x20
import network

pin = machine.Pin(14, machine.Pin.OUT)
dat_pin = machine.Pin(12)
dht = dht.DHT11(pin)

ds = ds18x20.DS18X20(onewire.OneWire(dat_pin))
roms = ds.scan()


def http_get(url):
    _, _, host, path = url.split('/', 3)
    host, port = host.split(':')
    port = int(port)
    s = socket.socket()
    s.connect((host, port))
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('UPC2529191', 'YVDDNGMF')
        while not wlan.isconnected():
            time.sleep_ms(50)
    print('network config:', wlan.ifconfig())


do_connect()
while True:
    ds.convert_temp()
    dht.measure()
    time.sleep(30)
    print(dht.temperature(), dht.humidity(), 'temp:', ds.read_temp(roms[0]))
    http_get('http://46.28.110.124:8111/{}/{}/{}/'.format(dht.temperature(), ds.read_temp(roms[0]), dht.humidity()))
