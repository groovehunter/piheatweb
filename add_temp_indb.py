#!/usr/bin/python3

import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'piheatweb.settings'
django.setup()

from sensors.models import SensorInfo
from sensors.Thermistor import *
from sensors.TempCalc import TempCalc


if __name__ == '__main__':
  si = SensorInfo.objects.all()
  updater =  TempCalc()
  for s in si:
    print(s.name)
    print(s.thermistor)
    evalstr = 'Thermistor'+s.thermistor+'()'
    updater.thermistor = eval(evalstr)
    updater.thermistor.set_RTvalues()
    updater.thermistor.prep_abc()
    updater.loop(s.id)


