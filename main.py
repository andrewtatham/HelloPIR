import colorsys
import datetime
import time
from blinkstick import blinkstick
import RPi.GPIO as GPIO


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

    def tick(self):
        print('tick')

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
                self.tick()
                self.detect_timeout()
                # print('state: {}'.format(self.state))
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
        self.light_off()
        self._hsv = (0, 1.0, 0)

    def hello(self):
        super(BlinkstickPIR, self).hello()
        self.light_on()

    def movement(self):
        super(BlinkstickPIR, self).movement()
        self.light_blink()

    def tick(self):
        super(BlinkstickPIR, self).tick()
        self.light_dim()

    def goodbye(self):
        super(BlinkstickPIR, self).goodbye()
        self.light_off()

    def light_on(self):
        print('light_on')
        try:
            h, s, v = self._hsv
            v = 0.5
            self._hsv = (h, s, v)
            self.set_colour()
        except Exception as e:
            print(e)

    def light_blink(self):
        print('light_blink')
        try:
            h, s, v = self._hsv
            v = 1.0
            self._hsv = (h, s, v)
            self.set_colour()
            time.sleep(0.1)
        except Exception as e:
            print(e)

    def light_dim(self):
        print('light_dim')
        try:
            h, s, v = self._hsv
            h = (h + 0.025) % 1.0
            v = max(0.05, v * 0.85)
            self._hsv = (h, s, v)
            self.set_colour()
        except Exception as e:
            print(e)

    def light_off(self):
        print('light_off')
        try:
            h, s, v = self._hsv
            v = 0.0
            self._hsv = (h, s, v)
            self.set_colour()
            self.bs.turn_off()
        except Exception as e:
            print(e)

    def set_colour(self):
        h, s, v = self._hsv
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r = int(255 * r)
        g = int(255 * g)
        b = int(255 * b)
        print("Setting Colour rgb: {}, hsv: {}".format((r, g, b), (h, s, v)))
        self.bs.set_color(0, 0, r, g, b)
        self.bs.set_color(0, 1, r, g, b)


if __name__ == '__main__':
    pir = BlinkstickPIR()
    pir.run()
