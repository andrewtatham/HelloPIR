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
        PIR_PIN = 4  # NB BCM PIN NUMBER
        GPIO.setup(PIR_PIN, GPIO.IN)

        print('PIR Module Test (CTRL+C to exit)')
        time.sleep(2)
        print('Ready')

        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=self.callback)

    def hello(self):
        print('hello')
        self.state = True

    def goodbye(self):
        print('goodbye')
        self.state = False
        self.state_at = None

    def callback(self, pir_pin):
        print('callback')
        self.state_at = datetime.datetime.utcnow()
        if not self.state:
            self.hello()

    def detect_timeout(self):
        if self.state and self.state_at:
            last_detection = datetime.datetime.utcnow() - self.state_at
            seconds = last_detection.seconds
            print('seconds: {}'.format(seconds))
            if seconds > 300:
                self.goodbye()

    def run(self):
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
        super().__init__()
        self.bs = blinkstick.find_first()

    def hello(self):
        super().hello()
        self.light_on()

    def goodbye(self):
        super().goodbye()
        self.light_off()

    def light_on(self):
        print('light_on')
        try:
            self.bs.set_random_color()
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
