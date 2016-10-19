import time
from time import sleep

import uos
from machine import Pin, PWM, Timer
from neopixel import NeoPixel

# http://pyladies.cz/v1/s016-micropython/index.html
# sudo screen  /dev/ttyUSB0 115200
# http://docs.micropython.org/en/v1.8/esp8266/esp8266/tutorial/neopixel.html

"""
The buzzer buzzes at random time and the players try to press their
buttons as fast as possible. Who is first wins a point. If the button
is pressed too soon and last point belongs to the same player,
she loses the point.

To restart the game just press reset on the board.
"""

butt_1 = Pin(2, Pin.OUT)
butt_1.value(1)
butt_2 = Pin(4, Pin.OUT)
butt_2.value(1)

leds = Pin(5, Pin.OUT)
LEDS = 8
np = NeoPixel(leds, LEDS)
for one in range(LEDS):
    np[one] = (0, 0, 0)
np.write()

buzz_timer = Timer(-1)

rand_sleep = 3000
butt_1_pressed = False
butt_2_pressed = False
timer_running = True
player_1_color = (25, 155, 15)
player_2_color = (155, 25, 80)  # (155, 25, 15)
current_round = 0
MAX_ROUNDS = 7

# this holds the game result
result = [0, 0, 0, 0, 0, 0, 0, 0]


def handle_butt_1(event):
    """ callback function when button 1 is pressed """
    global butt_1_pressed
    butt_1_pressed = True


def handle_butt_2(event):
    """ callback function when button 2 is pressed """
    global butt_2_pressed
    butt_2_pressed = True


# register the callbacks
butt_1.irq(trigger=Pin.IRQ_FALLING, handler=handle_butt_1)
butt_2.irq(trigger=Pin.IRQ_FALLING, handler=handle_butt_2)


def buzz(what):
    """ callback function for the timer """
    global timer_running
    buzz = Pin(12, Pin.OUT)
    pwm = PWM(buzz, freq=500, duty=770)
    sleep(0.05)
    pwm.deinit()
    timer_running = False


def init_buzz():
    """ calculate and init new buzz timer """
    global rand_sleep
    global timer_running
    rand_sleep = min(max(1000, int(uos.urandom(1)[0]) * 20), 5000)
    print(rand_sleep)
    buzz_timer.init(period=rand_sleep, mode=Timer.ONE_SHOT, callback=buzz)
    timer_running = True


def indicate_winner():
    """ just blink leds 3 times """
    for i in range(3):
        for one in range(LEDS):
            np[one] = (0, 0, 0)
        np.write()
        time.sleep_ms(150)

        for one in range(LEDS):
            np[one] = player_1_color if result[one] == 1 else player_2_color
        np.write()
        time.sleep_ms(350)


def give_point(player, positive=True):
    """ award/remove a point to the player """
    global current_round
    global result
    color = player_1_color if player == 1 else player_2_color
    if not positive: # remove point if the last one is from the same player
        if result[max(current_round - 1, 0)] == player:
            np[current_round - 1] = (0, 0, 0)
            np.write()
            current_round = max(current_round - 1, 0)
        return
    np[current_round] = color
    np.write()
    result[current_round] = player
    current_round = min(current_round + 1, MAX_ROUNDS)
    # sleep for a while to prevent double presses
    sleep(0.2)
    if all(result):  # we have a winner:
        indicate_winner()


init_buzz()
# main loop
while True:
    if butt_1_pressed:
        print('*** player 1 {} !***'.format('failed' if timer_running else 'wins'))
        give_point(1, not timer_running)
        butt_1_pressed = False
        init_buzz()

    if butt_2_pressed:
        print('*** player 2 {} !***'.format('failed' if timer_running else 'wins'))
        give_point(2, not timer_running)
        butt_2_pressed = False
        init_buzz()
