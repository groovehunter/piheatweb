#!/usr/bin/python3

import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'piheatweb.settings'
django.setup()

from sensors.models import *
#from motors.models import *
from cntrl.models import *

sdata = {}





def sensor_cntrl_event():
  #revents = ReadingEvent.objects.all().order_by('id')
  revents = ReadingEvent.objects.all().order_by('id')[86950:]
  
  for re in revents:
    #print(re.id, re.dtime)
    ce = ControlEvent.objects.get_or_create(dtime=re.dtime)[0]
    print(ce)

    for i in range(4):
      sid = '0'+str(i+1)   
      evalstr = 're.sid'+sid+'.ctrl_event = ce'
      exec(evalstr)    
      evalstr = 're.sid'+sid+'.save()'
      exec(evalstr)    
      

sensor_cntrl_event()



