from motors.BaseRule import BaseRule
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

class WarmwaterRangeRule(BaseRule):
  """ keep temperatur in kessel on same level if possible """
  lower = 43
  upper = 53
  MSG_TO_LOW  = 'Temperatur ist unter %s, Pumpe wird/bleibt aktiviert.' %lower
  MSG_TO_HIGH = 'Temperatur ist über %s, Pumpe wird/bleibt deaktiviert.' %upper

  def history_entry(self):
      entry = WarmwaterPumpHistory(
        dtime = self.now,
        change_status = 'UNDEFINED',
        rule_event = self.rule_event,
      )
      return entry

  def check(self):
    self.cur = SensorData_03.objects.latest('dtime').temperature
    super().check()
    cur = self.cur
    
    if (cur > self.lower and cur < self.upper):
      self.rule_event.result = 0
      self.rule_event.save()
      return

    self.rule_event.result = 1

    entry = self.history_entry()

    if IS_RPi:
      ctrl = WarmwaterPumpCtrl()
    if IS_PC:
      ctrl = WarmwaterPumpCtrlDummy()
    ctrl.setup()

    if cur < self.lower:
      ctrl.enable()
      entry.change_status = 'ON'
      entry.change_descr = self.MSG_TO_LOW,

    if cur > self.upper:
      ctrl.disable()
      entry.change_status = 'OFF'
      entry.change_descr = self.MSG_TO_HIGH,

    self.rule_event.save()
    entry.save()


class VorlaufGrenzwertRule(BaseRule):
  lower = 42
  upper = 55

  def history_entry(self):
    entry = MainValveHistory(
      dtime = self.now,
      change_amount = 0,
      rule_event = self.rule_event,
    )
    return entry

  def check(self):
    self.cur = SensorData_01.objects.latest('dtime').temperature
    super().check()
    cur = self.cur

    if (cur > self.lower and cur < self.upper):
      self.rule_false()
      return

    amount = 50    # fix for now
    entry = self.history_entry()
    entry.change_amount = amount

    if IS_RPi:
      ctrl = MainValveCtrl()
    if IS_PC:
      ctrl = MainValveCtrlDummy()

    ctrl.setup()
    latest = MainValveHistory.objects.latest('id')

    if cur < self.lower:
      dir = 'up'
      entry.change_dir = 'Open'
      entry.result_openingdegree = latest.result_openingdegree + amount
    if cur > self.upper:
      dir = 'dn'
      entry.change_dir = 'Close'
      entry.result_openingdegree = latest.result_openingdegree - amount

    ctrl.work(dir, amount)

    print('saving entry')
    self.rule_event.result = 1
    self.rule_event.save()
    entry.save()

