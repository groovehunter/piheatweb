from motors.BaseRule import BaseRule, ThresholdRule
from motors.models import HeatPumpHistory
from sensors.models import SensorData_04
from piheatweb.util import *
import logging
#from django.utils import timezone
from django.db.models import Avg
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)


if IS_RPi:
  from motors.HeatPump import HeatPumpCtrl
if IS_PC:
  from motors.HeatPumpDummy import HeatPumpCtrlDummy


class HeatPumpActivityRule(ThresholdRule): #BaseRule):
  """ (de)activation of heatpump """

  def setup(self):
    logic = self.rule.logic
    p = ['','']
    p = logic.split('__')
    self.lower = float(p[0])
    self.upper = float(p[1])
    self.MSG_TO_LOW  = 'outdoor temp ist unter %s, Pumpe wird/bleibt deaktiviert.' %self.lower
    self.MSG_TO_HIGH = 'outdoor Temp. ist über %s, Pumpe wird/bleibt aktiviert.' %self.upper
    some = SensorData_04.objects.order_by('-dtime')[1:5]
    cur = some.aggregate(Avg('temperature'))['temperature__avg']
    self.cur = float(cur)



  def history_entry(self):
      entry = HeatPumpHistory(
        dtime = self.now,
        change_status = 'UNDEFINED',
        rule_event = self.ctrl.rule_event,
      )
      return entry


  def action(self):
    """ act because rule was not fulfilled """
    logger.debug('action HP')
    self.ctrl.rule_event.result = 1

    entry = self.history_entry()

    if IS_RPi:
      ctrl = HeatPumpCtrl()
    if IS_PC:
      ctrl = HeatPumpCtrlDummy()
    # set pins
    ctrl.setup()

    if self.cur < self.lower:
      logger.debug('enable / keep enabled')
      if ctrl.get_status() == 'OFF':
        ctrl.enable()
        entry.change_status = 'SWITCH ON'
      else:
        entry.change_status = 'STAY ON'
      entry.change_descr = self.MSG_TO_LOW,

    elif self.cur > self.upper:
      logger.debug('disable / keep disabled')
      if ctrl.get_status() == 'ON':
        ctrl.disable()
        entry.change_status = 'SWITCH OFF'
      else:
        entry.change_status = 'STAY OFF'
      entry.change_descr = self.MSG_TO_HIGH,

    else:
      logger.error("WARNING: none of both conditions was matched !??")
      return False

    entry.save()
    return True


