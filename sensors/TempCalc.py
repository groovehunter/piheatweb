
from sensors.models import *
from sensors.Thermistor import *
import time
import logging

logger = logging.getLogger(__name__)


class TempCalc:

  def latest(self, sid):
    # choose sensor table here
    #logger.debug('sensor #%s', sid)
    sstr = '0'+str(sid)
    evalstr = 'SensorData_'+sstr+'.objects.'
    evalstr += "latest('id')"
    obj = eval(evalstr)
    time.sleep(1)

    r = obj.adc_out_to_resistance()
    temp = self.thermistor.resistance_to_temp(r)
    #logger.debug('TempCalc resistance %s', r)
    obj.resistance = r
    obj.temperature = temp
    obj.save()
    #obj.save(obj.id)


  def loop(self, sid):
    # choose sensor table here
    sstr = '0'+str(sid)
    evalstr = 'SensorData_'+sstr+'.objects.'
    if 1:
      evalstr += 'filter(temperature=0)'
    else:
      evalstr += 'all()'
    evalstr += '.order_by("-dtime")'
    object_list = eval(evalstr)
    count = 0
    logger.debug("Anzahl Datensaetze: %s", len(object_list))
    time.sleep(0.5)

    for obj in object_list:
      count +=1 

      r = obj.adc_out_to_resistance()
      temp = self.thermistor.resistance_to_temp(r)
      obj.resistance = r
      obj.temperature = temp
      obj.save()

