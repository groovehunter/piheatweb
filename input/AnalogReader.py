
import conf
#from conf import *
from sensors.models import *
from datetime import datetime
import threading
import json


class AnalogReader:

    """ Ein reader empfängt sensordaten vom arduino
        dann speichert er sie in der DB
    """

    def __init__(self):
        self.sensors = []
        self.current = {}
        self.last = []
        self.init_sensors()


    def init_sensors(self):
        sensors_wanted = [0,1,2,3]
        sensors=[]
        print("loading sensors")
        for i in range(1,5):
            sensor = Sensor.objects.get(pk=i)
            sensors.append(sensor)
        self.sensors = sensors
        print(sensors)


    # XXX weg
    def sensors_loadall(self):
        for s in self.sensors:
            m = Measurement(resistance=res, temperature=0, dtime=now)
            m.sensor = s
            m.save()
            print(res)


    def readall(self):
        #self.sched.enter(10, 1, self.readall, )
        threading.Timer(60.0, self.readall).start()
        print(time.time())
        for s in self.sensors:
            now = datetime.now()
            m = Measurement(resistance=res, temperature=0, dtime=now)
            m.sensor = s
            m.save()


    def store(self, data):
        """ store all sensory data in db """
        now = datetime.now()
        
        for d in data:
            id = d['id']
            m = Measurement(resistance=0, dtime=now)
            m.sensor = self.sensors[id]
            m.temperature = d['temp']
            m.save()
            #print(m.temperature)
        print("stored values on ", now.strftime('%H:%m:%S'))


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

