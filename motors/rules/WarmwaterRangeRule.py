from motors.BaseRule import ThresholdRule 
from motors.models import WarmwaterPumpHistory
from motors.models import RuleHistory
from sensors.models import SensorData_03
from piheatweb.util import *
from django.db.models import Avg, Max, Min, Sum
from piheatweb.settings import TMPPATH
import logging
from os import environ
#from django.utils import timezone
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)


if IS_RPi:
  from motors.WarmwaterPump import WarmwaterPumpCtrl
if IS_PC:
  from motors.WarmwaterPumpDummy import WarmwaterPumpCtrlDummy


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
    some = SensorData_03.objects.order_by('-id')[1:5]
    cur = some.aggregate(Avg('temperature'))['temperature__avg']
    self.cur = float(cur)

  def history_entry(self):
      entry = WarmwaterPumpHistory(
        change_status = 'UNDEFINED',
        rule_event = self.ctrl.rule_event,
      )
      return entry


  def action(self):
    """ act because rule was not fulfilled """
    # wenn kessel warm genug OK return
    # wenn kessel lower, dann check ob vorlauf höher als kessel
    # nur dann pumpe an
    # Ansonsten calc vorlauf entsprechend PI regelung zb 
    # 
    # also vllt, eine rule fuer pumpe an und aus wie hier schon 
    # und eine andere rule für vorlauf, wenn mode fuer nur warmwater


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
      self.ctrl.lg.error("WARNING: none of both conditions was matched !??")
      return False

    entry.save()
    result = entry.change_status
    self.ctrl.rule_event.result = result
    self.ctrl.rule_event.save()

    return True


