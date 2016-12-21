import network
import socket

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('UPC2529191', 'YVDDNGMF')
        while not wlan.isconnected():
            time.sleep_ms(50)
    print('network config:', wlan.ifconfig())

def http_get(url):
    proto, _, host, path = url.split('/', 3)
    port = 80
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SEC)
    if proto == "https:":
        import ussl
        s = ussl.wrap_socket(s)
        port = 443
    addr = socket.getaddrinfo(host, port)[0][-1]
    s.connect(addr)
    print(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break

do_connect()
# resp = urequests.get('http://www.lavdis.cz/meteorologicke-podminky/vltava-prehled-merenych-meteo-udaju')
resp = http_get('https://docs.google.com/spreadsheets/d/1YVnK5572HxdzzMlONuv6i7bZmlejPZvWU5WWRUd1sNU/pub?gid=0&single=true&output=csv')

