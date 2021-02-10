#!/usr/bin/python
import RPi.GPIO as GPIO


status_map = {
  'ON' : GPIO.HIGH,
  'OFF' : GPIO.LOW,
}

class WarmwaterPumpCtrl(object):

    def __init__(self):
        pass

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        self.pins = {}
        self.pins['main'] = 5
        GPIO.setwarnings(False)
        for name, pin in self.pins.items():
            GPIO.setup(pin, GPIO.OUT)
        self.pin = self.pins['main']

    def work(self, status):
        GPIO.output(self.pins['main'], status_map[status])
        self.status = status

    def toggle(self):
        status = not self.status
        GPIO.output(self.pins['main'], status_map[status])

    def enable(self):
        GPIO.output(self.pin, GPIO.LOW)

    def disable(self):
        GPIO.output(self.pin, GPIO.LOW)

    def cleanup(self):
        pass
