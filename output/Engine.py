#from conf import *
from datetime import datetime
import RPi.GPIO as GPIO, time

# Broadcom GPIO references
GPIO.setmode(GPIO.BCM)


#dry = True
dry = False

class Engine:

    def __init__(self):
        self.pins_pumps = {
            'ww'    : 5,
            'xy'    : 6,
            'free'  : 13,
            'heat'  : 19,
        }

    def load_pumps(self):
        pass

    def deactivate_pump(self, name):
        PiPin = self.pins_pumps[name]
        #if dry: return
        GPIO.setup(PiPin, GPIO.OUT)
        GPIO.output(PiPin, GPIO.HIGH)
        
	
    def activate_pump(self, name):
        PiPin = self.pins_pumps[name]
        #if dry: return
        GPIO.setup(PiPin, GPIO.OUT)
        GPIO.output(PiPin, GPIO.LOW)


    def get_state(self, name):
        PiPin = self.pins_pumps[name]
        GPIO.setup(PiPin, GPIO.IN)
        s = GPIO.input(PiPin)
        #print('State of ', name, 'is ', s) 
        return s


    def cleanup(self):
        GPIO.cleanup()




