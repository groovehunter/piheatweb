
import logging
logger = logging.getLogger(__name__)

from motors.Calc import Calc
from motors.CalcMethod import CalcMethod
from datetime import datetime



class CheckSensorIntegrityRule(CalcMethod, Calc):

  def check(self):
    return False


  def action(self):
    logger.debug("CheckSensorIntegrityRule")
    self.sensordata = {}
    for i in range(3):
      cls = 'SensorData_0'+str(i+1)
      res = getattr(cls, 'objects', None)
      if res:
        logger.debug('YEP')

      self.sensordata[i] = float(SensorData_01.objects.latest('id').temperature)
    self.cur_vorlauf  = float(SensorData_01.objects.latest('id').temperature)


  def save(self):
    value = round(self.soll_calc, 2)
    # XXX only AVAIL. when Rule object running
    ### 2022-10 
    self.ctrl.rule_event.result = value
    self.ctrl.rule_event.save()
