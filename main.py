import time
from blinkstick import blinkstick
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)

bs = blinkstick.find_first()


def MOTION(pir_pin):
    print('Motion Detected!')
    bs.set_random_color()
    time.sleep(0.5)
    bs.turn_off()


print('PIR Module Test (CTRL+C to exit)')
time.sleep(2)
print('Ready')

try:
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=MOTION)
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print('Quit')
    GPIO.cleanup()
