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
    try:
        bs.set_random_color()
    except Exception as e:
        print(e)


def light_off():
    print('light_off')
    try:
        bs.turn_off()
    except Exception as e:
        print(e)


def hello():
    global state, state_at
    print('hello')
    state = True
    light_on()


def goodbye():
    global state, state_at
    print('goodbye')
    state = False
    state_at = None
    light_off()


def callback(pir_pin):
    global state, state_at
    print('callback')
    state_at = datetime.datetime.utcnow()
    if not state:
        hello()


def detect_timeout():
    global state, state_at
    if state and state_at:
        last_detection = datetime.datetime.utcnow() - state_at
        seconds = last_detection.seconds
        print('seconds: {}'.format(seconds))
        if seconds > 15:
            goodbye()


print('PIR Module Test (CTRL+C to exit)')
time.sleep(2)
print('Ready')

GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=callback)

try:
    while True:
        detect_timeout()
        print('state: {}'.format(state))
        time.sleep(1)

except KeyboardInterrupt:
    print('Quit')
    GPIO.cleanup()
finally:
    light_off()
