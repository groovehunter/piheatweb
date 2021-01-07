from sensors.models import *
from motors.models import *
from motors.WarmwaterPump import WarmwaterPumpCtrl

from datetime import datetime


class BaseRule(Rule):
  """ maybe:
      provide access to SensorInfo
  """
  def __init__(self):
    """ common things to do in init. """
    self.now = datetime.now()
    self.DEFAULT_RULE = Rule.objects.get(pk=1)


class WarmwasserRangeRule(BaseRule):
  """ keep temperatur in kessel on same level if possible """
  lower = 50 
  upper = 65  
  MSG_TO_LOW  = 'Brauchwasser: Temperatur fiel unter %s, Pumpe wird aktiviert.' %lower
  MSG_TO_HIGH = 'Brauchwasser: Temperatur stieg über %s, Pumpe wird deaktiviert.' %upper

  def check(self):
    entry = None
    cur = SensorData_03.objects.latest('dtime').temperature
    
    if cur < self.lower:
      WarmwaterPumpCtrl.enable()
      entry = self.history_entry()  
      entry.changed_status = 'ON' 
      entry.change_descr = self.MSG_TO_LOW,
      
    elif cur > self.upper:
      WarmwaterPumpCtrl.disable()
      entry = self.history_entry()  
      entry.changed_status = 'OFF' 
      entry.change_descr = self.MSG_TO_HIGH,
      
    else:
      # XXX write to logfile, rule not matches
      pass

    if entry:
      entry.save()
    

  def history_entry(self):
      entry = WarmwaterPumpHistory(
        dtime = self.now,
        changed_status = 'UNDEFINED', 
        rule = self.DEFAULT_RULE,
      )
      return entry
      





