#!/usr/bin/python3

GAIN = 1

import os
import logging

import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'piheatweb.settings'
django.setup()
logger = logging.getLogger(__name__)

import Adafruit_ADS1x15
from sensors.models import *
from sensors.Thermistor import *
from sensors.TempCalc import TempCalc
from cntrl.models import ControlEvent
from time import sleep

adc = Adafruit_ADS1x15.ADS1115()
logging.getLogger("root").setLevel(logging.DEBUG)

def read_adc():
  from django.utils import timezone
  # Read all the ADC channel values in a list.
  values = [0]*4
  tz_now = timezone.now() # TZ aware :)

  ctrl_event = ControlEvent.objects.latest('dtime')

  for i in range(4):
    values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
    sid = '0'+str(i+1)

    obj = eval('SensorData_'+sid+'()')
    obj.adc_out = values[i]
    obj.temperature = 0
    obj.resistance = 0
    obj.ctrl_event = ctrl_event
    obj.save()
    #logger.debug(obj.ctrl_event.id)


# cron version
from calc_temp_latest_daemon import tempcalc
if __name__ == '__main__':
  sleep(1)
  read_adc()
  tempcalc()

