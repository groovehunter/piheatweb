
import conf
#from conf import *
from sensors.models import *
from datetime import datetime
import RPi.GPIO as GPIO, time


class Reader:

    """ Ein reader liest sensorsignale, wandelt die gemessene dauer
        in temperatur um. 
        dann speichert er sie in der DB
    """

    def __init__(self):
        self.sensors = []
        GPIO.setmode(GPIO.BCM)
        self.last = []

    def sensors_loadall(self):
        for s in self.sensors:
            res = RCtime(s.pin_bcm)
            m = Measurement(resistance=res, temperature=0, dtime=now)
            m.sensor = s
            m.save()
            print(res)

    def readall(self):
        for s in sensors:
            res = RCtime(s.pin_bcm)
            m = Measurement(resistance=res, temperature=0, dtime=now)
            m.sensor = s
            m.save()
            print(res)


    def get_approx(self, pin):
        """ average of last measures """
        res = self.read(pin)
        self.last.insert(0, res)
        if len(self.last) > 10:
            self.last.pop()
        print(self.last)
        avg = round(sum(self.last) / len(self.last), 2)

        return avg


    def read(self, pin):
        """ fetch RCtime and calc temp """
        #print('reading pin ', pin)
        GPIO.setup(pin, GPIO.IN)

        t = self.RCtime(pin)
        fac_temp = self.cfg['fac_temp'] 
        temp = round(t / fac_temp, 2)

        return temp


    def RCtime(self, pin):
        """ measure charge time """
        measurement = 0
        # Discharge capacitor
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.2)

        t_beg = datetime.now()
        GPIO.setup(pin, GPIO.IN)
        # Count loops until voltage across
        # capacitor reads high on GPIO
        while (GPIO.input(pin) == GPIO.LOW):
            measurement += 1

        t_end = datetime.now()
        dur = t_end - t_beg
        #print(dur)
        return measurement


