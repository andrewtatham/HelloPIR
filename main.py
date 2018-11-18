import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)


def MOTION(pir_pin):
    print('Motion Detected!')


print('PIR Module Test (CTRL+C to exit)')
time.sleep(2)
print('Ready')

try:
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=MOTION)
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print('Quit')
    GPIO.cleanup()
