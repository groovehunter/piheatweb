#!/usr/bin/python3
import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'piheatweb.settings'
django.setup()
from django.utils import timezone

from sensors.models import SensorInfo
from sensors.Thermistor import *
from sensors.TempCalc import TempCalc

import logging
fn = os.environ['HOME'] + '/log/pi_sim.log'
logging.basicConfig(
  filename=fn,
  #level=logging.INFO,
  level=logging.DEBUG,
)
# create console handler and set level to debug
logger = logging.getLogger()



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


### cron version
if __name__ == '__main__':
  tempcalc()

