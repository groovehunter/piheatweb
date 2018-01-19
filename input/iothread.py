# Reading an analogue sensor with
# a single GPIO pin
import conf
#from conf import *
from sensors.models import *
from datetime import datetime
import RPi.GPIO as GPIO, time
import threading

# Broadcom GPIO references
GPIO.setmode(GPIO.BCM)



# Define function to measure charge time
def RCtime (PiPin):
    measurement = 0
    # Discharge capacitor
    GPIO.setup(PiPin, GPIO.OUT)
    GPIO.output(PiPin, GPIO.LOW)
    time.sleep(0.2)

    GPIO.setup(PiPin, GPIO.IN)
    # Count loops until voltage across
    # capacitor reads high on GPIO
    while (GPIO.input(PiPin) == GPIO.LOW):
        measurement += 1

    return measurement

sensors_wanted = [5]
sensors=[]
print("loading sensors")
for i in range(1,5):
    sensor = Sensor.objects.get(pk=i)
    if sensor.pin_bcm in sensors_wanted:
        print('Loaded sensor on pin ', sensor.pin_bcm),
        sensors.append(sensor)


# Main program loop
now = datetime.now()
s = sensors[0]

mainTh = threading.Thread(target=None, name='main')
mainTh.daemon = True
mainTh.start()

sensTh = threading.Thread(target=RCtime, name='rc', args=(s.pin_bcm,))


while True:
    
    sensTh.start()

    #sensTh.join()

"""
    for s in sensors:
        res = RCtime(s.pin_bcm)
        m = Measurement(resistance=res, temperature=0, dtime=now)
        m.sensor = s
        m.save()
        print(res)
    print()
    time.sleep(1)
"""

