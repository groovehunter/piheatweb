#!/usr/bin/python3

import os
import logging
from time import sleep
fn = os.environ['HOME'] + '/log/piheat.log'
logging.basicConfig(
  filename=fn,
  level=logging.INFO,
)
# create console handler and set level to debug
logger = logging.getLogger()

import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'piheatweb.settings'
django.setup()
from django.utils import timezone 

#import Adafruit_ADS1x15
from sensors.models import *
from sensors.Thermistor import *
from sensors.TempCalc import TempCalc
from cntrl.models import ControlEvent

#adc = Adafruit_ADS1x15.ADS1115()
from random import randint

smin = {}
smax = {}
smin = {
  0: 6000,
  1: 7000,
  2: 6000,
  3: 12000,
}
smax = {
  0: 8000,
  1: 9000,
  2: 8000,
  3: 14000,
}


def sensor_data_around(d1, diff, smin, smax):
  # switch tendency, probability = 1:10
  tendkeep = randint(0,10)
  # random change between 0 and 100
  change = randint(3, 100) + abs(diff)

  # tendency
  if diff > 0:
    change = -change
  else:
    pass

  if tendkeep == 0:
    logger.debug('tendkeep is 0: %s', tendkeep)
    change = -change

  logger.debug('change : %s', change)
  newd = d1 + change

  # keep between a min and max  
  if newd < smin: newd = smin
  if newd > smax: newd = smax
  return newd

def read_adc():
  #last_ce = ControlEvent.objects.latest('id')
  last = ControlEvent.objects.all().order_by('-id')[:4]
  last_ce     = last[0]
  secondlast_ce  = last[1]
  logger.debug("last ce: %s", last_ce.id)
  logger.debug("secondlast ce: %s", secondlast_ce.id)
  
  tz_now = timezone.now() # TZ aware :)

  event = ReadingEvent(dtime=tz_now)
  #ctrl_event = ControlEvent(dtime=tz_now)
  #ctrl_event.save()

  for i in range(4):
    sid = '0'+str(i+1)

    evalstr = 'SensorData_'+sid+'.objects.filter(ctrl_event__pk=last[1].id)'
    try:
      last_adc_out = eval(evalstr).first().adc_out
    except:
      last_adc_out = (smax[i] + smin[i]) / 2
      logger.debug("last[1] ### using mean value")

    evalstr = 'SensorData_'+sid+'.objects.filter(ctrl_event__pk=last[2].id)'
    try:
      seclast_adc_out = eval(evalstr).first().adc_out
    except:
      seclast_adc_out = last_adc_out
      logger.debug("last[2] ### using last[1]")

    logger.debug(" last: %s", last_adc_out)
    logger.debug("slast: %s", seclast_adc_out)
    diff = seclast_adc_out - last_adc_out 
    logger.debug('diff : %s', diff)
    value = sensor_data_around(last_adc_out, diff, smin[i], smax[i])
    logger.debug('NEW: %s', value)
    logger.debug('-----------------------------')

    obj = eval('SensorData_'+sid+'()')
    obj.dtime = tz_now
    obj.adc_out = value
    obj.temperature = 0
    obj.resistance = 0
    obj.ctrl_event = last_ce
    obj.save()
    evalstr = 'event.sid'+sid+'=obj'
    exec(evalstr)
 
  event.save()



# cron version
from calc_temp_latest_daemon import tempcalc
if __name__ == '__main__':
  sleep(3)
  logger.debug('START READER ======================')
  read_adc()
  tempcalc()



