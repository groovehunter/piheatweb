#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sys



class WarmwaterPumpCtrl(object):

    def __init__(self):
        self.count = 0

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        self.pins = {}
        self.pins['relay'] = 0
        self.pins['sth'] = 0
        GPIO.setwarnings(False)
        for name, pin in self.pins.items():
            GPIO.setup(pin, GPIO.OUT)



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
