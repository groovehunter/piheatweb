#from conf import *
from datetime import datetime
import RPi.GPIO as GPIO, time

# Broadcom GPIO references
GPIO.setmode(GPIO.BCM)




def blink(PiPin):
    GPIO.setup(PiPin, GPIO.OUT)
    # Discharge capacitor
    GPIO.output(PiPin, GPIO.LOW)
    time.sleep(15)
    GPIO.output(PiPin, GPIO.HIGH)
    time.sleep(5)



# Main program loop
i = 0
while True:
    i += 1
    now = datetime.now()
    blink(26)
    print("Zyklus #",i)


"""
"""
GPIO.cleanup()
