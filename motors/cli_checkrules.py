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
#logger.debug('---------------------------------------------- START CLI')

if __name__=='__main__':
  ctrl = RulesCliCtrl()
  ctrl.setup()
  ctrl.initiate_klasses_obj()
  ctrl.load_rules_from_db()
  if len(sys.argv) > 1:
    rulename = sys.argv[1]
    if len(sys.argv) > 2:
      dry = sys.argv[2]
      ctrl.dry = dry
      # XXX unused
    if not rulename in ctrl.rules_list_db.keys():
      print("Rule with this name does not exist!")
    rule_db = ctrl.rules_list_db[rulename]
    ctrl.check_rule(rule_db)
  else:
    ctrl.loop_rules()
#  ctrl.rules_list()
#  ctrl.test()


