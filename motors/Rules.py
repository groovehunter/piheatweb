from motors.BaseRule import BaseRule, ThresholdRule
from sensors.models import *
from motors.models import WarmwaterPumpHistory, MainValveHistory
from motors.models import RuleHistory
from motors.util import *

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
    self.lower = 43.0
    self.upper = 53.0
    self.MSG_TO_LOW  = 'Temp. ist unter %s, Pumpe wird/bleibt aktiviert.' %self.lower
    self.MSG_TO_HIGH = 'Temp. ist über %s, Pumpe wird/bleibt deaktiviert.' %self.upper
    cur = SensorData_03.objects.latest('dtime').temperature
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
      if not ctrl.get_status():
        ctrl.enable()
        entry.change_status = 'SWITCH ON'
      else:
        entry.change_status = 'STAY ON'
      entry.change_descr = self.MSG_TO_LOW,

    if self.cur > self.upper:
      if ctrl.get_status():
        ctrl.disable()
        entry.change_status = 'SWITCH OFF'
      else:
        entry.change_status = 'STAY OFF'
      entry.change_descr = self.MSG_TO_HIGH,

    self.rule_event.save()
    entry.save()


class VorlaufGrenzwertRule(ThresholdRule):
  """ check if vorlauf is between thresholds """

  def setup(self):
    self.lower = 42.0
    self.upper = 49.0
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
    amount = 50    # fix for now
    entry = self.history_entry()
    entry.change_amount = amount

    if IS_RPi:
      ctrl = MainValveCtrl()
    if IS_PC:
      ctrl = MainValveCtrlDummy()

    latest = MainValveHistory.objects.latest('id')

    if self.cur > self.upper:
      direction = 'dn'
      entry.change_dir = 'Close'
      entry.result_openingdegree = latest.result_openingdegree - amount
    elif self.cur < self.lower:
      direction = 'up'
      entry.change_dir = 'Open'
      entry.result_openingdegree = latest.result_openingdegree + amount
    else:
      print("WARNING: none of both conditions was matched !??")
      return

    ### the actual work
    ctrl.work(direction, amount)

    print('saving entry')
    self.rule_event.result = 1
    self.rule_event.save()
    entry.save()

