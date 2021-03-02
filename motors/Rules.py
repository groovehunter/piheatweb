from motors.BaseRule import BaseRule, ThresholdRule, FixedGoalAdjustableActuator
from sensors.models import *
from motors.models import WarmwaterPumpHistory, MainValveHistory
from motors.models import RuleHistory
from piheatweb.util import *
from django.db.models import Avg, Max, Min, Sum
import logging
from os import environ
from django.utils.timezone import now
from datetime import datetime, timedelta

logger = logging.getLogger()

if IS_RPi:
  from motors.MainValveCtrl import MainValveCtrl
  from motors.WarmwaterPump import WarmwaterPumpCtrl
if IS_PC:
  from motors.MainValveCtrlDummy import MainValveCtrlDummy
  from motors.WarmwaterPumpDummy import WarmwaterPumpCtrlDummy

class DummyRule(BaseRule):
  def check(self):
    return
  def action(self):
    pass

class WarmwaterRangeRule(ThresholdRule):
  """ keep temperatur in kessel on same level if possible """

  def setup(self):
    logic = self.rule.logic
    p = ['','']
    try:
      p = logic.split('__')
      self.lower = float(p[0])
      self.upper = float(p[1])
    except:
      # fallback
      self.lower = 43.0
      self.upper = 48.0
    self.MSG_TO_LOW  = 'Temp. ist unter %s, Pumpe wird/bleibt aktiviert.' %self.lower
    self.MSG_TO_HIGH = 'Temp. ist über %s, Pumpe wird/bleibt deaktiviert.' %self.upper
    some = SensorData_03.objects.order_by('-dtime')[1:5]
    cur = some.aggregate(Avg('temperature'))['temperature__avg']
    self.cur = float(cur)

  def history_entry(self):
      entry = WarmwaterPumpHistory(
        dtime = self.now,
        change_status = 'UNDEFINED',
        rule_event = self.ctrl.rule_event,
      )
      return entry


  def action(self):
    """ act because rule was not fulfilled """
    self.ctrl.rule_event.result = 1

    entry = self.history_entry()

    if IS_RPi:
      ctrl = WarmwaterPumpCtrl()
    if IS_PC:
      ctrl = WarmwaterPumpCtrlDummy()
    # set pins
    ctrl.setup()

    if self.cur < self.lower:
      if ctrl.get_status() == 'OFF':
        ctrl.enable()
        entry.change_status = 'SWITCH ON'
      else:
        entry.change_status = 'STAY ON'
      entry.change_descr = self.MSG_TO_LOW,

    elif self.cur > self.upper:
      if ctrl.get_status() == 'ON':
        ctrl.disable()
        entry.change_status = 'SWITCH OFF'
      else:
        entry.change_status = 'STAY OFF'
      entry.change_descr = self.MSG_TO_HIGH,

    else:
      logger.error("WARNING: none of both conditions was matched !??")
      return False

    logger.info(entry.change_descr)
    entry.save()
    return True


class PI_ControlRule(BaseRule):
  """ prop-integr-control;
      two distinct points in time, a)now and b)one period before and their values
      are needed for calculation.
      Wo wie speichern? erstmal quick a file
  """
  def setup(self):
    fn = settings.TMPPATH + 'pi_vals.txt'
    f = open(fn, 'rw')
    vals = f.read()
    logger.debug(vals)

  def check(self):
    pass
  def action(self):
    pass



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
    #logger.debug('end setup')

  def save_logic(self):
    # Is Soll to Ist difference more than 2
    if (abs(self.logic - self.vorlauf_soll_calc) > 2):
      logic_new = str(round(self.vorlauf_soll_calc))
      logger.debug("ACT: setting rule logic to %s", logic_new)
      self.rule.logic = logic_new
      self.rule.save()
    else:
      logger.debug('OK - leave rule logic as is: %s', self.rule.logic)
    return None


  def history_entry(self):
    entry = MainValveHistory(
      dtime = self.now,
      change_amount = 0,
      rule_event = self.ctrl.rule_event,
    )
    return entry

  def check(self):
    logger.debug('vorlauf - check')
    is_must = eval(self.must)
    logger.debug('is_must: %s', is_must)
    if not is_must:
      return True
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

    logger.debug('diff: %s', self.diff)
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
      logger.error("WARNING: none of both conditions was matched !??")
      return False

    entry.result_openingdegree = tmp
    entry.save()
    ### the actual work
    sa = str(amount)
    logger.info("mainvalve amount %s (total:%s)- %s", sa, tmp, direction)
    ctrl.work(direction, amount)

    return True
