import time
from blinkstick import blinkstick
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)

bs = blinkstick.find_first()


def light_on():
    print('light_on')
    bs.set_random_color()


def light_off():
    print('light_off')
    bs.turn_off()


def on_rising(pir_pin):
    print('on_rising')
    light_on()


def on_falling(pir_pin):
    print('on_falling')
    light_off()


print('PIR Module Test (CTRL+C to exit)')
time.sleep(2)
print('Ready')

GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=on_rising)
GPIO.add_event_detect(PIR_PIN, GPIO.FALLING, callback=on_falling)
try:
    while True:
        print('zzz')
        time.sleep(1)

except KeyboardInterrupt:
    print('Quit')
    GPIO.cleanup()
