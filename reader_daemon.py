#!/usr/bin/python3

GAIN = 1

import os
import logging
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

import Adafruit_ADS1x15
from sensors.models import *
from sensors.Thermistor import *
from sensors.TempCalc import TempCalc
from cntrl.models import ControlEvent

adc = Adafruit_ADS1x15.ADS1115()

def read_adc():
  from django.utils import timezone 
  # Read all the ADC channel values in a list.
  values = [0]*4
  tz_now = timezone.now() # TZ aware :)

  event = ReadingEvent(dtime=tz_now)
  ctrl_event = ControlEvent(dtime=tz_now)
  ctrl_event.save()

  for i in range(4):
    values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
    sid = '0'+str(i+1)
    
    obj = eval('SensorData_'+sid+'()')
    obj.dtime = tz_now
    obj.adc_out = values[i]
    obj.temperature = 0
    obj.resistance = 0
    obj.ctrl_event = ctrl_event
    obj.save()
    #logger.info(obj.ctrl_event.id)
    #logger.info(obj.ctrl_event_id)
    evalstr = 'event.sid'+sid+'=obj'
    exec(evalstr)
 
  event.save()



# cron version
from calc_temp_latest_daemon import tempcalc
if __name__ == '__main__':
  read_adc()
  tempcalc()



