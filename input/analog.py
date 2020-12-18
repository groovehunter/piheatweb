# Reading an analogue sensor with
# a single GPIO pin
import conf
#from conf import *
from sensors.models import *
from datetime import datetime
import RPi.GPIO as GPIO, time

# Broadcom GPIO references
GPIO.setmode(GPIO.BCM)

pins = [2,3,4,5]
sensor_map = {
        3 : 'Aussenfühler',
        2 : 'Vorlauf',
        4 : 'Kessel',
        5 : 'Rücklauf',
        }


# Define function to measure charge time
def RCtime (PiPin):
    measurement = 0
    # Discharge capacitor
    GPIO.setup(PiPin, GPIO.OUT)
    GPIO.output(PiPin, GPIO.LOW)
    time.sleep(0.2)

    t_beg = datetime.now()
    GPIO.setup(PiPin, GPIO.IN)
    # Count loops until voltage across
    # capacitor reads high on GPIO
    while (GPIO.input(PiPin) == GPIO.LOW):
        measurement += 1

    t_end = datetime.now()
    dur = t_end - t_beg
    print(dur)
    return measurement

sensors_wanted = [3]
sensors=[]
print("loading sensors")
for i in range(1,5):
    sensor = Sensor.objects.get(pk=i)
    if sensor.pin_bcm in sensors_wanted:
        print('Loaded sensor on pin ', sensor.pin_bcm),
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
    time.sleep(1)


