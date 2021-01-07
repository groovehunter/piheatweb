#!/usr/bin/python3
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))

import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'piheatweb.settings'
django.setup()

from motors.models import *

from motors.rules import *
  

if __name__=='__main__':
  print(sys.argv)
  ### WORK
  # ctrl = 

