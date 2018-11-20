import time
from blinkstick import blinkstick
import RPi.GPIO as GPIO
import datetime

GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)

bs = blinkstick.find_first()

state = False
state_at = None


def light_on():
    print('light_on')
    bs.set_random_color()


def light_off():
    print('light_off')
    bs.turn_off()


def callback(pir_pin):
    global state, state_at
    print('callback')
    if not state:
        hello()
    # state = GPIO.input(PIR_PIN)
    state = True
    state_at = datetime.datetime.utcnow()


def hello():
    print('hello')
    light_on()


def goodbye():
    print('goodbye')
    light_off()


print('PIR Module Test (CTRL+C to exit)')
time.sleep(2)
print('Ready')

GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=callback)
try:
    while True:
        if state_at:
            last_detection = datetime.datetime.utcnow() - datetime.datetime(state_at)
            seconds = last_detection.seconds
            print(f'seconds: {seconds}')
            if seconds > 15:
                state = False
                goodbye()
        print(f'state: {state}')
        time.sleep(1)

except KeyboardInterrupt:
    print('Quit')
    GPIO.cleanup()
