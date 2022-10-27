#!/usr/bin/python3

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
    #updater.loop(s.id)
    updater.latest(s.id)



