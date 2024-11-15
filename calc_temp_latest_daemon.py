#!/usr/bin/python3

from sensors.models import SensorInfo
from sensors.Thermistor import *
from sensors.TempCalc import TempCalc

import logging
logger = logging.getLogger()


def tempcalc():
  """ calc from adc values the resistance and temp """

  si = SensorInfo.objects.all()
  updater =  TempCalc()
  #logger.debug('tempcalc')
  for s in si:
    #logger.debug(s)
    kls = 'Thermistor'+s.thermistor
    g = globals()
    updater.thermistor = g[kls]()
    updater.thermistor.set_RTvalues()
    updater.thermistor.prep_abc()
    #updater.loop(s.id)
    updater.latest(s.id)



