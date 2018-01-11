# Reading an analogue sensor with
# a single GPIO pin
import conf
#from conf import *
from sensors.models import *
from datetime import datetime
import RPi.GPIO as GPIO, time

# Broadcom GPIO references
GPIO.setmode(GPIO.BCM)

# Define function to measure charge time
def RCtime (PiPin):
    measurement = 0
    # Discharge capacitor
    GPIO.setup(PiPin, GPIO.OUT)
    GPIO.output(PiPin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(PiPin, GPIO.IN)
    # Count loops until voltage across
    # capacitor reads high on GPIO
    while (GPIO.input(PiPin) == GPIO.LOW):
        measurement += 1

    return measurement

sensors=[]
print("loading sensors")
for i in range(1,5):
    print(i),
    sensor = Sensor.objects.get(pk=i)
    sensors.append(sensor)


# Main program loop
while True:
    now = datetime.now()
    for s in sensors:
        res = RCtime(s.pin_bcm)
        m = Measurement(resistance=res, temperature=0, dtime=now)
        m.sensor = s
        m.save()
        print(res)
    print()
    time.sleep(2)


