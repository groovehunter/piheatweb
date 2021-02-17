from motors.BaseRule import BaseRule, ThresholdRule, FixedGoalAdjustableActuator
from sensors.models import *
from motors.models import WarmwaterPumpHistory, MainValveHistory
from motors.models import RuleHistory
from motors.util import *
from django.db.models import Avg, Max, Min, Sum
import logging
from os import environ

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
        rule_event = self.rule_event,
      )
      return entry


  def action(self):
    """ act because rule was not fulfilled """
    self.rule_event.result = 1

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


class VorlaufGrenzwertRule(ThresholdRule):
  """ check if vorlauf is between thresholds """

  def setup(self):
    self.lower = 41.0
    self.upper = 48.0
    cur = SensorData_01.objects.latest('dtime').temperature
    self.cur = float(cur)

  def history_entry(self):
    entry = MainValveHistory(
      dtime = self.now,
      change_amount = 0,
      rule_event = self.rule_event,
    )
    return entry


  def action(self):
    amount = 0    # for safety, if not explicit set later 
    direction = None
    entry = self.history_entry()

    if IS_RPi:
      ctrl = MainValveCtrl()
    if IS_PC:
      ctrl = MainValveCtrlDummy()
    ctrl.setup()

    latest = MainValveHistory.objects.latest('id')

    if self.cur > self.upper:
      diff = int(self.cur) - int(self.upper)
      amount = 20 + (5 * diff)
      direction = 'dn'
      entry.change_dir = 'Close'
      entry.change_amount = amount
      entry.result_openingdegree = latest.result_openingdegree - amount

    elif self.cur < self.lower:
      diff = int(self.lower) - int(self.cur)
      amount = 20 + (5 * diff)
      direction = 'up'
      entry.change_dir = 'Open'
      entry.change_amount = amount
      entry.result_openingdegree = latest.result_openingdegree + amount

    else:
      print("WARNING: none of both conditions was matched !??")
      return False

    ### the actual work
    logger.debug("mainvalve dir: %s amount: %i", direction, amount)
    logger.debug("new openingdegree: %i", entry.result_openingdegree)
    ctrl.work(direction, amount)

    entry.save()
    return True


class VorlaufRule(FixedGoalAdjustableActuator):
  multipli = 5
  min_base = 10

  def setup(self):
    some = SensorData_01.objects.order_by('-dtime')[1:5]
    cur = some.aggregate(Avg('temperature'))['temperature__avg']
    self.cur = float(cur)
    logger.debug('setup self.cur %s', self.cur)
    logic = self.rule.logic
    try:
      self.goal = float(logic)
    except:
      # fallback
      self.goal= 48.0
    self.diff = abs(self.cur - self.goal)

    # prerequisites:
    self.must = 'self.main_cur > 4650' # etwa der 0-Strich of valve
    self.main_cur = MainValveHistory.objects.latest('dtime').result_openingdegree


  def history_entry(self):
    entry = MainValveHistory(
      dtime = self.now,
      change_amount = 0,
      rule_event = self.rule_event,
    )
    return entry

  def check(self):
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
      entry.result_openingdegree = latest.result_openingdegree - amount

    elif (self.cur - self.goal) < 0:
      direction = 'up'
      entry.change_dir = 'Open'
      entry.change_amount = amount
      entry.result_openingdegree = latest.result_openingdegree + amount

    else:
      print("WARNING: none of both conditions was matched !??")
      return False

    ### the actual work
    sa = str(amount)
    logger.info("mainvalve amount %s - %s", sa, direction)
    #logger.debug("work on mainvalve an amount of %s in direction: %s", amount, direction)
    ctrl.work(direction, amount)

    entry.save()
    return True



