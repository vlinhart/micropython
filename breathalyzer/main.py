from time import sleep

from machine import Pin, ADC, I2C
from neopixel import NeoPixel
import ssd1306

# well it's not 1V for LoLin NodeMCU/Wemos D1 - it's got voltage divider 3.1V -> 1V
# see http://www.thalin.se/2015/05/using-adc-on-nodemcu-esp8266.html
# http://pyladies.cz/v1/s016-micropython/index.html
# sudo screen  /dev/ttyUSB0 115200
digital = Pin(12, Pin.IN)  # D6
attempt = 0
adc = ADC(0)

leds = Pin(13, Pin.OUT)  # D7
LEDS = 8
np = NeoPixel(leds, LEDS)


i2c = I2C(sda=Pin(5), scl=Pin(4))
display = None
try:
    display = ssd1306.SSD1306_I2C(128,64,i2c)
except:
    pass

def lights_up():
    for one in range(LEDS):
        np[one] = (10, 40, 5)
    np.write()


def heat_up(seconds=60):
    detector_base_values = []
    countdown = LEDS - 1
    lights_up()
    ad_val = adc.read()
    for s in range(seconds):
        print('init: {}/{} AD={}'.format(s, seconds, ad_val))
        if (s + 1) % (seconds // LEDS) == 0:
            np[max(countdown, 0)] = (0, 0, 0)
            np.write()
            countdown -= 1
        if s > seconds - 10:
            detector_base_values.append(ad_val)

        sleep(1)
    return min(detector_base_values) + 3  # is the reading of zero ...


def show_lights(value):
    for i in range(LEDS):
        if value - detector_base > one_led_range * i:
            np[i] = (90, 14, 7)
        else:
            np[i] = (0, 0, 0)
    np.write()


def display_values():
    if display is None:
        return
    line_height = 12
    display.fill(0)
    display.text('Vylytej jako!',15,0)
    # display.text('D2 t:{:.1f} h:{:.1f}'.format(dht22.temperature(), dht22.humidity()),0, 5 + line_height)
    display.text('V:{}'.format(adc.read()),0,5 + line_height*3)
    display.text('GC free:{}'.format(gc.mem_free()),0,5 + line_height*4)
    display.show()

detector_base = heat_up()
detector_range = 1024 - detector_base
one_led_range = round(detector_range / LEDS)

while True:
    attempt += 1
    print('seconds:', attempt, 'digital:', digital.value(), 'analog:', adc.read(), 'base:', detector_base)
    show_lights(adc.read())
    display_values()
    sleep(1)
