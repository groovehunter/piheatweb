#!/usr/bin/python3

import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'piheatweb.settings'
django.setup()

from sensors.models import *
from sensors.Thermistor import *
import time

# sensors
# 1 - Zulauf - VF20
# 2 - Rueckl - VF20
# 3 - kessel - unbek.
# 4 - aussen - nt10 (?)

class Welldone:

  def loop(self, sid):
    # choose sensor table here
    sstr = '0'+str(sid)
    evalstr = 'SensorData_'+sstr+'.objects.'
    if 0:
      evalstr += 'filter(temperature__gt=80)'
    else:
      evalstr += 'all()'
    evalstr += '.order_by("-dtime")'
    object_list = eval(evalstr)
    count = 0
    print("Anzahl Datensaetze: ", len(object_list))
    time.sleep(2)

    for obj in object_list:
      count +=1 

      r = obj.adc_out_to_resistance()
      temp = self.thermistor.resistance_to_temp(r)
      obj.resistance = r
      obj.temperature = temp
      obj.save()
      print(count, r, temp)


if __name__ == '__main__':
  si = SensorInfo.objects.all()
  updater =  Welldone()
  for s in si:
    print(s.name)
    evalstr = 'Thermistor'+s.thermistor+'()'
    updater.thermistor = eval(evalstr)
    updater.thermistor.set_RTvalues()
    updater.thermistor.prep_abc()
    updater.loop(s.id)


