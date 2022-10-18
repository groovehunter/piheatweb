

from motors.models import Rule, RuleHistory
from motors.models import RuleResultData_01
from motors.KlassLoader import KlassLoader
from django.utils import timezone
from sensors.models import SensorData_01, SensorData_04
from django.db.models import Avg, Max, Min, Sum
from datetime import datetime, timedelta
import logging
logger = logging.getLogger(__name__)


class Calc:
  def load_sensordata(self):
    # vorlauf temp
    self.cur_vorlauf  = float(SensorData_01.objects.latest('id').temperature)
    self.some_cur_vorlauf  = SensorData_01.objects.order_by('-id')[1:5]
    #logger.debug('load_sensordata: cur_vorlauf: %s', int(self.cur_vorlauf))
    if int(self.cur_vorlauf) == 0:
      logger.error('vorlauf was 0.0 - recalc average of latest 5')
      self.cur_vorlauf = float(self.some_cur_vorlauf.aggregate(Avg('temperature'))['temperature__avg'])
    #logger.debug('load_sensordata: cur_vorlauf: %s', self.cur_vorlauf)

    # outdoor temp
    some = SensorData_04.objects.order_by('-id')[1:30]
    cur = some.aggregate(Avg('temperature'))['temperature__avg']
    self.cur_outdoor = float(cur)
    # daily average temp
    start_date = self.now - timedelta(hours=24)
    h24 = SensorData_04.objects.filter(ctrl_event__dtime__minute=0, ctrl_event__dtime__range=(start_date, self.now))
    avg24 = h24.aggregate(Avg('temperature'))['temperature__avg']
    self.avg24_outdoor = float(avg24)

  def load_latest_db_soll_calc(self):
    # get latest rule event for rule CalcVorlaufSollRule
    try:
      re = RuleHistory.objects.filter(rule__name='CalcVorlaufSollRule').latest('id')
      self.soll_calc_db = re.result
    except:
      self.soll_calc_db = 40
    #self.soll_calc_db = RuleResultData_01.objects.latest('dtime').value
    ### XXX rule result from rulehistory table

  def getVorlaufSollCalc(self):
    if not hasattr(self, 'soll_calc_db'):
      self.load_latest_db_soll_calc()
    return self.soll_calc_db
