#!/usr/bin/python3

FREQ=30 # zyklus der abfrage in sekunden

import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'piheatweb.settings'
django.setup()

import time
import schedule
from sensors.models import SensorInfo
from sensors.Thermistor import *
from sensors.TempCalc import TempCalc

def tempcalc():
  """ calc from adc values the resistance and temp """
  si = SensorInfo.objects.all()
  updater =  TempCalc()
  for s in si:
    #print(s.name)
    evalstr = 'Thermistor'+s.thermistor+'()'
    updater.thermistor = eval(evalstr)
    updater.thermistor.set_RTvalues()
    updater.thermistor.prep_abc()
    updater.loop(s.id)


schedule.every(FREQ).seconds.do(tempcalc)

while True:  
  schedule.run_pending()  

