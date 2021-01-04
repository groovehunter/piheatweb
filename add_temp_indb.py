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

  def loop(self):
    # XXX choose sensor table here
    object_list = SensorData_04.objects.all() #filter(temperature=0).order_by('-dtime')
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

  updater =  Welldone()
  # XXX Change thermistor type here
  #updater.thermistor = ThermistorVF20()
  updater.thermistor = ThermistorNT10()
  updater.thermistor.set_RTvalues()
  updater.thermistor.prep_abc()
  updater.loop()


