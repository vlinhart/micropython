# screen  /dev/ttyUSB0 115200
import time
import dht
import socket
import machine
import onewire
import network
import esp
import ds18x20
import gc
import uos

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')
else:
    print('power on or hard reset')

#d2-4
#d5-14

ds18_pin = machine.Pin(14) #d5
ds = ds18x20.DS18X20(onewire.OneWire(ds18_pin))

dht11_pin = machine.Pin(4, machine.Pin.IN) #d2
dht11 = dht.DHT11(dht11_pin)


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
    wlan.active(True)
    attempt = 1
    wifis = []
    with open('wifi.txt') as f:
        wifis = f.readlines()
    print(wifis)
    wifi = lambda : int(uos.urandom(1)[0]) % len(wifis)

    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(*tuple(map(lambda x: x.strip(), wifis[wifi()].split())))
        while not wlan.isconnected():
            time.sleep_ms(350)
            attempt += 1
            if attempt > 25:
                attempt = 0
                wlan.connect(*tuple(map(lambda x: x.strip(), wifis[wifi()].split())))

    print('network config:', wlan.ifconfig())

def measure_dht():
    results = []
    for one in range(3):
        time.sleep(2)
        dht11.measure()
        results.append(dht11.humidity())
    print(results)
    return max(results)

print('measuring...')
roms = ds.scan()
ds.convert_temp()

dht_hum = measure_dht()
ds18_temp = ds.read_temp(roms[0])
print('t:', ds18_temp, 'h:', dht_hum)
do_connect()

http_get('http://api.thingspeak.com/update?api_key=RNZ28OEQAELE4ML9&field1={}&field2={}'.format(ds18_temp, dht_hum))

print('GC alloc:{} free:{}'.format(gc.mem_alloc(), gc.mem_free()))
gc.collect()
esp.deepsleep(1000000*60*3)
