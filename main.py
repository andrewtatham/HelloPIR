import time
from blinkstick import blinkstick
import RPi.GPIO as GPIO
import datetime


class MyPIR(object):
    def __init__(self):
        self.state = False
        self.state_at = None

    def initialize(self):
        GPIO.setmode(GPIO.BCM)
        pir_pin = 4  # NB BCM PIN NUMBER
        GPIO.setup(pir_pin, GPIO.IN)

        print('PIR Module Test (CTRL+C to exit)')
        time.sleep(2)
        print('Ready')

        GPIO.add_event_detect(pir_pin, GPIO.RISING, callback=self.callback)

    def hello(self):
        print('hello')

    def movement(self):
        print('movement')

    def goodbye(self):
        print('goodbye')

    def callback(self, pir_pin):
        print('callback')
        if not self.state:
            self.hello()
        self.movement()
        self.state = True
        self.state_at = datetime.datetime.utcnow()

    def detect_timeout(self):
        if self.state and self.state_at:
            last_detection = datetime.datetime.utcnow() - self.state_at
            seconds = last_detection.seconds
            print('seconds: {}'.format(seconds))
            if seconds > 900:
                self.goodbye()
                self.state = False
                self.state_at = None

    def run(self):
        self.initialize()
        try:
            while True:
                self.detect_timeout()
                print('state: {}'.format(self.state))
                time.sleep(1)

        except KeyboardInterrupt:
            print('Quit')
        finally:
            self.goodbye()
            GPIO.cleanup()


class BlinkstickPIR(MyPIR):
    def __init__(self):
        super(BlinkstickPIR, self).__init__()
        self.bs = blinkstick.find_first()

    def hello(self):
        super(BlinkstickPIR, self).hello()
        self.light_on()

    def movement(self):
        super(BlinkstickPIR, self).movement()
        self.light_blink()

    def goodbye(self):
        super(BlinkstickPIR, self).goodbye()
        self.light_off()

    def light_on(self):
        print('light_on')
        try:
            self.bs.set_color(0, 1, 0, 8)
        except Exception as e:
            print(e)

    def light_blink(self):
        print('light_blink')
        try:
            self.bs.blink(0, 1, 8)
        except Exception as e:
            print(e)

    def light_off(self):
        print('light_off')
        try:
            self.bs.turn_off()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pir = BlinkstickPIR()
    pir.run()
