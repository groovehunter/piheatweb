from motors.CalcMethod import CalcMethod
from motors.models import MainValveHistory 
from motors.models import RuleResultData_02, RuleResultData_03, RuleResultData_04, RuleResultData_05
from piheatweb.util import *
from motors.PID import PID
import logging
logger = logging.getLogger(__name__)



class CalcPI_ControlRule(CalcMethod):
  """ prop-integr-control;
      two distinct points in time, a)now and b)one period before and their values
      are needed for calculation.
  """
  def setup(self):
    self.vorlauf_soll_calc = self.ctrl.getVorlaufSollCalc()
    self.goal = self.vorlauf_soll_calc
    pidparam = self.rule.logic
    logger.debug('PID params: %s', pidparam)
    p,i,d = pidparam.split(',')
    self.pid = PID(int(p), int(i), int(d))
    self.pid.setWindup(300.0)
    self.diff = abs(self.ctrl.cur_vorlauf - self.goal)
    self.cur = self.ctrl.cur_vorlauf

  # action will be renamed to calc 
  def action(self):
    latest = MainValveHistory.objects.latest('id')
    e_  = self.goal - float(self.ctrl.some_cur_vorlauf[1].temperature)
    last_time = self.ctrl.some_cur_vorlauf[0].dtime
    #logger.debug('last_time : %s', last_time)

    pid = self.pid
    pid.SetPoint = self.goal
    pid.setSampleTime(60)
    pid.setLastError(e_)
    pid.setLastTime(last_time)
    # Calc next control value
    self.pid_terms = pid.update(self.cur)
    self.result = pid.output
    logger.debug('pid CALC output: %s', self.result)
    self.save()

  def save(self):
    data = RuleResultData_02()
    data.value = self.result
    data.dtime = self.now
    data.rule_event = self.ctrl.rule_event
    data.save()

    data = RuleResultData_03()
    data.value = self.pid_terms[0]
    data.rule_event = self.ctrl.rule_event
    data.save()

    data = RuleResultData_04()
    data.value = self.pid_terms[1]
    data.rule_event = self.ctrl.rule_event
    data.save()

    data = RuleResultData_05()
    data.value = self.pid_terms[2]
    data.rule_event = self.ctrl.rule_event
    data.save()

