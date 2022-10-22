from motors.BaseRule import FixedGoalAdjustableActuator
from sensors.models import *
from motors.models import MainValveHistory
from piheatweb.util import *
from django.db.models import Avg, Max, Min, Sum
from motors.PID import PID
import logging
logger = logging.getLogger(__name__)


if IS_RPi:
  from motors.MainValveCtrl import MainValveCtrl
if IS_PC:
  from motors.MainValveCtrlDummy import MainValveCtrlDummy



class PI_ControlRule(FixedGoalAdjustableActuator):
  """ prop-integr-control;
      two distinct points in time, a)now and b)one period before and their values
      are needed for calculation.
      Wo wie speichern? erstmal quick a file
  """
  def setup(self):
    self.main_cur = MainValveHistory.objects.latest('dtime').result_openingdegree
    self.vorlauf_soll_calc = self.ctrl.getVorlaufSollCalc()
    self.goal = self.vorlauf_soll_calc
    pidparam = self.rule.logic
    logger.debug('PID params: %s', pidparam)
    p,i,d = pidparam.split(',')
    self.pid = PID(int(p), int(i), int(d))
    self.pid.setWindup(300.0)
    self.diff = abs(self.ctrl.cur_vorlauf - self.vorlauf_soll_calc)
    self.cur = self.ctrl.cur_vorlauf

  def history_entry(self):
    entry = MainValveHistory(
      dtime = self.now,
      change_amount = 0,
      rule_event = self.ctrl.rule_event,
    )
    return entry

  def check(self):
    return super().check()

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
    pid.update(self.cur)
    ctrl_val = pid.output
    #data = RuleResultData_02()
    # XXX get data from rulehistory.result
    data.value = ctrl_val
    data.dtime = self.now
    data.rule_event = self.ctrl.rule_event
    data.save()
    logger.debug('pid output: %s', ctrl_val)

    amount = abs(int(ctrl_val))
    if amount < 10:
      logger.debug('TOO SMALL change to apply')
      return True

    direction = None
    entry = self.history_entry()

    if IS_RPi:
      ctrl = MainValveCtrl()
    if IS_PC:
      ctrl = MainValveCtrlDummy()
    ctrl.setup()

    ### calculate if valve conditions are met
    logger.debug('latest.result_openingdegree: %s', latest.result_openingdegree)

    if ctrl_val < 0: 
      tmp_resulting_degrees = latest.result_openingdegree - amount

      if (tmp_resulting_degrees < ctrl.openingdegree_minimum):
        logger.error('MIN opening degree of valve: %s', ctrl.openingdegree_minimum)

        # change for the maximum possible
        amount = latest.result_openingdegree - ctrl.openingdegree_minimum 
        logger.warning('WARNING: amount set to max possible: %s', amount)
        total_resulting = latest.result_openingdegree - amount
      else:
        total_resulting = tmp_resulting_degrees

      direction = 'dn'
      entry.change_dir = 'Close'
      entry.change_amount = amount


    elif ctrl_val > 0:
      tmp_resulting_degrees = latest.result_openingdegree + amount

      if (tmp_resulting_degrees > ctrl.openingdegree_maximum):
        logger.error('MAX opening degree of valve: %s', ctrl.openingdegree_maximum)

        # change for the maximum possible
        amount = ctrl.openingdegree_maximum - latest.result_openingdegree
        logger.warning('WARNING: amount set to max possible: %s', amount)
        total_resulting = latest.result_openingdegree + amount
      else:
        total_resulting = tmp_resulting_degrees
      direction = 'up'
      entry.change_dir = 'Open'
      entry.change_amount = amount

    else:
      logger.error("WARNING: none of both conditions was matched !??")
      return False


    entry.result_openingdegree = total_resulting

    ### the actual work
    sa = str(amount)

    logger.info("mainvalve amount %s (total:%s)- %s", sa, total_resulting, direction)
    succesful_done = ctrl.work(direction, amount)
    if succesful_done:
      entry.save()

    return True


