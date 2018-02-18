
import conf
#from conf import *
from sensors.models import *
from datetime import datetime
import RPi.GPIO as GPIO, time
import sched, time
import threading


class Reader:

    """ Ein reader liest sensorsignale, wandelt die gemessene dauer
        in temperatur um. 
        dann speichert er sie in der DB
    """

    def __init__(self):
        self.sensors = []
        GPIO.setmode(GPIO.BCM)
        self.current = {}
        self.last = []
        self.init_sensors()

#        self.sched = sched.scheduler(time.time, time.sleep)
#        self.sched.enter(10, 1, self.readall)
#        self.sched.run()


    def init_sensors(self):
        sensors_wanted = [3]
        sensors=[]
        print("loading sensors")
        for i in range(1,5):
            sensor = Sensor.objects.get(pk=i)
            if sensor.pin_bcm in sensors_wanted:
                print('Loaded sensor on pin ', sensor.pin_bcm),
        sensors.append(sensor)
        self.sensors = sensors


    # XXX weg
    def sensors_loadall(self):
        for s in self.sensors:
            res = RCtime(s.pin_bcm)
            m = Measurement(resistance=res, temperature=0, dtime=now)
            m.sensor = s
            m.save()
            print(res)


    def readall(self):
        #self.sched.enter(10, 1, self.readall, )
        threading.Timer(60.0, self.readall).start()
        print(time.time())
        for s in self.sensors:
            res = self.RCtime(s.pin_bcm)
            now = datetime.now()
            m = Measurement(resistance=res, temperature=0, dtime=now)
            m.sensor = s
            m.temperature = self.res_to_temp(res)
            m.save()
            print(res, m.temperature, s.pin_bcm)
            self.current[s.pin_bcm] = m.temperature


    def from_db(self):
        sens = {}
        for s in self.sensors:
            s.val = Measurement.objects.latest('dtime').s
            print(s.val)
            sens[s.name] = s
        return sens


    def get_approx(self, pin):
        """ average of last measures """
        res = self.read(pin)
        self.last.insert(0, res)
        if len(self.last) > 10:
            self.last.pop()
        print(self.last)
        avg = round(sum(self.last) / len(self.last), 2)
        return avg

    def res_to_temp(self, res):
        """ calc temp from resistance """
        fac_temp = self.cfg['fac_temp'] 
        return round(res / fac_temp, 2)


    def get_res_temp(self, pin):
        GPIO.setup(pin, GPIO.IN)
        t = self.RCtime(pin)
        fac_temp = self.cfg['fac_temp'] 
        temp = round(t / fac_temp, 2)
        return t, temp


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


