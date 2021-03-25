#!/usr/bin/python3
import sys
import os
os.chdir(os.environ['HOME']+'/pw/cntrl')
sys.path.append(os.path.join(os.getcwd(), '..'))

import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'piheatweb.settings'
django.setup()

from motors.models import *
from motors.rules import *
from motors.RulesCtrl import RulesCliCtrl
from cntrl.models import *
from cntrl.CntrlCliCtrl import CntrlCliCtrl
import piheatweb.util

import logging
fn = os.environ['HOME'] + '/log/piheat.log'
logging.basicConfig(
  filename=fn,
  level=logging.DEBUG,
)
# create console handler and set level to debug
logger = logging.getLogger()
logger.debug('----------------------------------------------')
logger.debug('START CLI CNTRL')

if __name__=='__main__':
  ### WORK
  ctrl = CntrlCliCtrl()
  ctrl.setup()
  ctrl.initiate_control_event()
