import RPi.GPIO as GPIO


status_map = {
  'ON' : GPIO.HIGH,
  'OFF' : GPIO.LOW,
}

class HeatPumpCtrl:

    def __init__(self):
        pass

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        self.pins = {}
        self.pins['main'] = 19
        GPIO.setwarnings(False)
        for name, pin in self.pins.items():
            GPIO.setup(pin, GPIO.OUT)
        self.pin = self.pins['main']

    def get_status(self):
        cur = GPIO.input(self.pin)
        if cur == GPIO.LOW:
          return 'OFF'
        if cur == GPIO.HIGH:
          return 'ON'
        return 'UNDEF'

    def work(self, status):
        GPIO.output(self.pins['main'], status_map[status])
        self.status = status

    def enable(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def disable(self):
        GPIO.output(self.pin, GPIO.LOW)

    def cleanup(self):
        pass


