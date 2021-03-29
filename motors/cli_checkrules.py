#!/usr/bin/python3
import sys
import os
os.chdir(os.environ['HOME']+'/pw/motors')
sys.path.append(os.path.join(os.getcwd(), '..'))

import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'piheatweb.settings'
django.setup()

from motors.models import *
from motors.rules import *
from motors.RulesCtrl import RulesCliCtrl
import piheatweb.util

import logging
logger = logging.getLogger(__name__)
logger.debug('---------------------------------------------- START CLI')

if __name__=='__main__':
  ### WORK
  ctrl = RulesCliCtrl()
  ctrl.setup()
  ctrl.initiate_klasses_obj()
  ctrl.load_rules_from_db()
#  ctrl.rules_list()
#  ctrl.test()
  ctrl.loop_rules()


