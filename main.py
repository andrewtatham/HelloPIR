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
        if state and state_at:
            last_detection = datetime.datetime.utcnow() - state_at
            seconds = last_detection.seconds
            print('seconds: {}'.format(seconds))
            if seconds > 15:
                state = False
                state_at = None
                goodbye()
        print('state: {}'.format(state))
        time.sleep(1)

except KeyboardInterrupt:
    print('Quit')
    GPIO.cleanup()
finally:
    light_off()
