#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sys


status_map = {
  'ON' : GPIO.HIGH,
  'OFF' : GPIO.LOW,
}

class WarmwaterPumpCtrl(object):

    def __init__(self):
        self.count = 0

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        self.pins = {}
        self.pins['main'] = 5
        GPIO.setwarnings(False)
        for name, pin in self.pins.items():
            GPIO.setup(pin, GPIO.OUT)

    def work(self, status):
        self.status = status
        GPIO.output(self.pins['main'], status_map[status])

    def toggle(self):
        status = not self.status
        GPIO.output(self.pins['main'], status_map[status])

    def enable(self):
        PUL = self.pins['PUL']
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(sl)

    def disable(self):
        PUL = self.pins['PUL']
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(sl)

    def cleanup(self):
        pass
