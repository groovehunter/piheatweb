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
fn = os.environ['HOME'] + '/log/piheat.log'
logging.basicConfig(
  filename=fn,
  level=logging.DEBUG,
)
# create console handler and set level to debug
logger = logging.getLogger()

logger.debug('----------------------------------------------')
logger.debug('RULE VALUE SET')


if __name__=='__main__':
  ### WORK
  val = sys.argv[1]
  ctrl = RulesCliCtrl()
  ctrl.load_rules_from_db()
  #rulename = 'VorlaufRule'
  rulename = 'PI_ControlRule'
  rule_db = ctrl.rules_list_db[rulename]
  logic = rule_db.logic
  goal, param = logic.split('__')
  newlogic = '__'.join( [val, param] )
  logger.info('set %s value to %s', rulename, val)
  ctrl.setval(rulename, newlogic)


