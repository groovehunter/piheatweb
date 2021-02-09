from BaseRule import BaseRule
from sensors.models import *
from motors.models import WarmwaterPumpHistory, MainValveHistory
from motors.models import RuleHistory
from motors.util import *
#from django.utils import timezone
#now = timezone.now() # TZ aware :)

if IS_RPi:
  from MainValveCtrl import MainValveCtrl
  from WarmwaterPump import WarmwaterPumpCtrl
if IS_PC:
  from MainValveCtrlDummy import MainValveCtrlDummy
  from WarmwaterPumpDummy import WarmwaterPumpCtrlDummy


class WarmwasserRangeRule(BaseRule):
  """ keep temperatur in kessel on same level if possible """
  lower = 50
  upper = 65
  MSG_TO_LOW  = 'Brauchwasser: Temperatur fiel unter %s, Pumpe wird aktiviert.' %lower
  MSG_TO_HIGH = 'Brauchwasser: Temperatur stieg über %s, Pumpe wird deaktiviert.' %upper

  def history_entry(self):
      entry = WarmwaterPumpHistory(
        dtime = self.now,
        changed_status = 'UNDEFINED',
        rule = self.DEFAULT_RULE,
      )
      return entry

  def check(self):
    entry = None
    cur = SensorData_03.objects.latest('dtime').temperature

    if (cur > self.lower and cur < self.upper):
      self.rule_event.result = 0
      self.rule_event.save()
      return

    entry = self.history_entry()

    if IS_RPi:
      ctrl = WarmwaterPumpCtrl()
    if IS_PC:
      ctrl = WarmwaterPumpCtrlDummy()

    if cur < self.lower:
      ctrl.enable()
      entry.changed_status = 'ON'
      entry.change_descr = self.MSG_TO_LOW,

    elif cur > self.upper:
      ctrl.disable()
      entry.changed_status = 'OFF'
      entry.change_descr = self.MSG_TO_HIGH,

    entry.save()





class VorlaufGrenzwertRule(BaseRule):
  lower = 40
  upper = 60
  MSG_TO_LOW  = 'Vorlauf: Temperatur fiel unter %s, Ventil wird weiter geöffnet.' %lower
  MSG_TO_HIGH = 'Vorlauf: Temperatur stieg über %s, Ventil wird weiter geschlossen.' %upper

  def history_entry(self):
    entry = MainValveHistory(
      dtime = self.now,
      change_amount = 0,
      rule_event = self.rule_event,
    )
    return entry

  def check(self):
    super().check()
    cur = SensorData_01.objects.latest('dtime').temperature
    print("latest temp: ",cur)

    amount = 100    # fix for now
    entry = self.history_entry()
    entry.change_amount = amount

    if (cur > self.lower and cur < self.upper):
      self.rule_event.result = 0
      self.rule_event.save()
      return

    if IS_RPi:
      ctrl = MainValveCtrl()
    if IS_PC:
      ctrl = MainValveCtrlDummy()

    if cur < self.lower:
      dir = 'up'
      ctrl.work(dir, amount)
      entry.change_descr = self.MSG_TO_LOW,
    elif cur > self.upper:
      dir = 'dn'
      ctrl.work(dir, amount)
      entry.change_descr = self.MSG_TO_HIGH,

    print('saving entry')
    entry.save()
    self.rule_event.save()


