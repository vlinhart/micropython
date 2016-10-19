from time import sleep

from machine import Pin, ADC
from neopixel import NeoPixel

# well it's not 1V for LoLin NodeMCU - it's got voltage divider 3.1V -> 1V
# see http://www.thalin.se/2015/05/using-adc-on-nodemcu-esp8266.html
# sudo screen  /dev/ttyUSB0 115200
digital = Pin(12, Pin.IN)  # D6
attempt = 0
adc = ADC(0)

leds = Pin(13, Pin.OUT)  # D7
LEDS = 8
np = NeoPixel(leds, LEDS)


def lights_up():
    for one in range(LEDS):
        np[one] = (40, 180, 40)
    np.write()


def heat_up(seconds=60):
    detector_base_values = []
    countdown = LEDS - 1
    lights_up()
    for s in range(seconds):
        print('init: {} out of {}'.format(s, seconds))
        if (s + 1) % (seconds // LEDS) == 0:
            np[max(countdown, 0)] = (0, 0, 0)
            np.write()
            countdown -= 1
        if s > seconds - 10:
            detector_base_values.append(adc.read())

        sleep(1)
    return min(detector_base_values) + 3  # is the reading of zero ...


def show_lights(value):
    for i in range(LEDS):
        if value - detector_base > one_led_range * i:
            np[i] = (185, 25, 15)
        else:
            np[i] = (0, 0, 0)
    np.write()


detector_base = heat_up()
detector_range = 1024 - detector_base
one_led_range = round(detector_range / LEDS)

while True:
    attempt += 1
    print('seconds:', attempt, 'digital:', digital.value(), 'analog:', adc.read(), 'base:', detector_base)
    show_lights(adc.read())
    sleep(1)
