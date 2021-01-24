
from sensors.models import *
from sensors.Thermistor import *
import time


class TempCalc:

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
    print("Anzahl Datensaetze: ", len(object_list))
    time.sleep(1)

    for obj in object_list:
      count +=1 

      r = obj.adc_out_to_resistance()
      temp = self.thermistor.resistance_to_temp(r)
      obj.resistance = r
      obj.temperature = temp
      obj.save()
      #print(count, r, temp)

