#!/usr/bin/python3

""" create random temperature entries in sensordata table 
    for debugging and testing
"""

import os
from time import sleep
import time, math
from decimal import Decimal
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'piheatweb.settings'
django.setup()
from django.utils import timezone 
from django.db.utils import IntegrityError
import logging
logger = logging.getLogger()

from sensors.models import *
from sensors.Thermistor import *
from sensors.TempCalc import TempCalc
from cntrl.models import ControlEvent


def out2(zahl_1, phasendiff):
    sinus = math.sin((zahl_1) + math.degrees(phasendiff))
    sinus_color = int((sinus + 1) * 127.5)   # Wertebereich 0 ... 255 für Farbcode
    sinus_graphic = sinus * 12 + 13          # Wertebereich für Darstellung mit Zeichen
    sinus_str = (int(sinus_graphic) * '=')
    return (sinus_color, sinus_graphic, sinus_str)


g = globals()
th = {
  0: 'ThermistorNT10',
  1: 'ThermistorNT10',
  2: 'ThermistorNT20',
  3: 'ThermistorVF20',
}
t = {}
for i in range(4):
  t[i] = g[th[i]]()

def read_adc():
  last_ce = ControlEvent.objects.latest('id')
  logger.debug("START READER ====================== last ce: %s", last_ce.id)
  tz_now = timezone.now() # TZ aware :)
  c = time.time()
  for i in range(4):
    sid = '0'+str(i+1)
    t[i].set_RTvalues()
    t[i].prep_abc()

    sdstr = 'SensorData_'+sid
    obj = g[sdstr]()
    obj.ctrl_event = last_ce
    value, ret, sinstr = out2(c, 60*i)
    obj.temperature = 0
    obj.resistance = 0
    obj.adc_out = value 
    try:
      obj.save()
    except IntegrityError:
      logger.debug('saving FAILED, probably control_event already used')

    r = obj.adc_out_to_resistance()
    f = t[i].resistance_to_temp(r)
    while f > 100:
      f -= 100
    obj.temperature = round(f, 2)
    obj.resistance = r
    obj.save()

if __name__ == '__main__':
  sleep(3)
  read_adc()





