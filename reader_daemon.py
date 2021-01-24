#!/usr/bin/python3

FREQ=60 # zyklus der abfrage in sekunden
GAIN = 1

import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'piheatweb.settings'
django.setup()

import time
import schedule

# from datetime import datetime   # non timezone aware obj, deprec.
import Adafruit_ADS1x15
from sensors.models import *
from sensors.Thermistor import *
from sensors.TempCalc import TempCalc

adc = Adafruit_ADS1x15.ADS1115()

#print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
#print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
#print('-' * 37)

def read_adc():
  #from django.utils.timezone import now
  from django.utils import timezone 
  # Read all the ADC channel values in a list.
  values = [0]*4
  tz_now = timezone.now() # TZ aware :)
  #print(tz_now)
  #print(timezone.is_aware(tz_now))

  temp = 0

  event = ReadingEvent(dtime=tz_now)
  for i in range(4):
    values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
    sid = '0'+str(i+1)
    
    obj = eval('SensorData_'+sid+'()')
    obj.dtime = tz_now
    obj.adc_out = values[i]
    obj.temperature = 0
    obj.resistance = 0
    obj.save()
    evalstr = 'event.sid'+sid+'=obj'
    exec(evalstr)
 
  event.save()





schedule.every(FREQ).seconds.do(read_adc) 


while True:  
  schedule.run_pending()  


