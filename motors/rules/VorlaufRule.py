from motors.BaseRule import FixedGoalAdjustableActuator
from sensors.models import *
from motors.models import WarmwaterPumpHistory, MainValveHistory
from motors.models import RuleHistory
from piheatweb.util import *
from django.db.models import Avg, Max, Min, Sum
from piheatweb.settings import TMPPATH
import logging
from os import environ
from datetime import datetime, timedelta

logger = logging.getLogger()

if IS_RPi:
  from motors.MainValveCtrl import MainValveCtrl
  from motors.WarmwaterPump import WarmwaterPumpCtrl
if IS_PC:
  from motors.MainValveCtrlDummy import MainValveCtrlDummy
  from motors.WarmwaterPumpDummy import WarmwaterPumpCtrlDummy



class VorlaufRule(FixedGoalAdjustableActuator):
  multipli = 5
  min_base = 10
  depends_on = ('CalcVorlaufSoll')

  def setup(self):
    # prerequisites:
    #1
    self.must = 'self.main_cur > 4650' # etwa der 0-Strich of valve
    self.main_cur = MainValveHistory.objects.latest('dtime').result_openingdegree
    #2 - soll temp ready calculated?!
    #self.rule_event
    #RuleResultData_01.objects.filter(rule_event

    self.logic = float(self.rule.logic)
    #self.ctrl.vorlauf_soll_temp()
    self.vorlauf_soll_calc = self.ctrl.getVorlaufSollCalc()
    self.save_logic()
    self.goal = float(self.rule.logic)
    self.diff = abs(self.ctrl.cur_vorlauf - self.goal)
    self.cur = self.ctrl.cur_vorlauf
    #self.ctrl.lg.debug('end setup')
    #self.vorlauf_soll_calc = self.ctrl.getVorlaufSollCalc()

  def save_logic(self):
    # Is Soll to Ist difference more than 2
    if (abs(self.logic - self.vorlauf_soll_calc) > 2):
      logic_new = str(round(self.vorlauf_soll_calc))
      self.ctrl.lg.debug("ACT: setting rule logic to %s", logic_new)
      self.rule.logic = logic_new
      self.rule.save()
    else:
      self.ctrl.lg.debug('OK - leave rule logic as is: %s', self.rule.logic)
    return None


  def history_entry(self):
    entry = MainValveHistory(
      dtime = self.now,
      change_amount = 0,
      rule_event = self.ctrl.rule_event,
    )
    return entry

  def check(self):
    self.ctrl.lg.debug('vorlauf - check')
    is_must = eval(self.must)
    self.ctrl.lg.debug('is_must: %s', is_must)
    if not is_must:
      return True
    self.ctrl.lg.debug('vorlauf - CP2')
    return super().check()

  def action(self):
    amount = 0    # for safety, if not explicit set later
    direction = None
    entry = self.history_entry()

    if IS_RPi:
      ctrl = MainValveCtrl()
    if IS_PC:
      ctrl = MainValveCtrlDummy()
    ctrl.setup()

    self.ctrl.lg.debug('diff: %s', self.diff)
    diff_int = int(self.diff)
    #diff = abs(int(self.cur) - int(self.goal))
    latest = MainValveHistory.objects.latest('id')
    if diff_int <3:
      diff_int = 0  # dont change too much if come near goal
    amount = self.min_base + (self.multipli * diff_int)

    if (self.cur - self.goal) > 0:
      direction = 'dn'
      entry.change_dir = 'Close'
      entry.change_amount = amount
      tmp = latest.result_openingdegree - amount

    elif (self.cur - self.goal) < 0:
      direction = 'up'
      entry.change_dir = 'Open'
      entry.change_amount = amount
      tmp = latest.result_openingdegree + amount

    else:
      self.ctrl.lg.error("WARNING: none of both conditions was matched !??")
      return False

    entry.result_openingdegree = tmp
    entry.save()
    ### the actual work
    sa = str(amount)
    self.ctrl.lg.info("mainvalve amount %s (total:%s)- %s", sa, tmp, direction)
    ctrl.work(direction, amount)

    return True
