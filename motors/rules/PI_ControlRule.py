from motors.BaseRule import FixedGoalAdjustableActuator
from sensors.models import *
from motors.models import WarmwaterPumpHistory, MainValveHistory
from motors.models import RuleHistory
from piheatweb.util import *
from django.db.models import Avg, Max, Min, Sum
from piheatweb.settings import TMPPATH
from os import environ
from datetime import datetime, timedelta
from motors.PID import PID


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
    goal, pidparam = self.rule.logic.split('__')
    self.ctrl.lg.debug('PID params: %s', pidparam)
    p,i,d = pidparam.split(',')
    self.pid = PID(int(p), int(i), int(d))
    self.pid.setWindup(300.0)
    self.goal = float(goal)
    self.diff = abs(self.ctrl.cur_vorlauf - self.goal)
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
    # u_ vorherige stellgroesse
    latest = MainValveHistory.objects.latest('id')
    e_  = self.goal - float(self.ctrl.some_cur_vorlauf[1].temperature)
    #u_  = latest.change_amount
    last_time = self.ctrl.some_cur_vorlauf[0].dtime
    #logger.debug('CALL pid with e_=%s', e_)
    #logger.debug('last_time : %s', last_time)

    pid = self.pid
    pid.SetPoint = self.goal
    pid.setSampleTime(60)
    pid.setLastError(e_)
    pid.setLastTime(last_time)

    pid.update(self.cur)
    ctrl_val = pid.output
    self.ctrl.lg.debug('pid output: %s', ctrl_val)

    amount = abs(int(ctrl_val))
    if amount < 10:
      self.ctrl.lg.debug('TOO SMALL change to apply')
      return True

    direction = None
    entry = self.history_entry()

    if IS_RPi:
      ctrl = MainValveCtrl()
    if IS_PC:
      ctrl = MainValveCtrlDummy()
    ctrl.lg = self.ctrl.lg
    ctrl.setup()

    if ctrl_val < 0: 
      tmp = latest.result_openingdegree - amount
      if (tmp < ctrl.openingdegree_minimum):
        self.ctrl.lg.error("WARNING: below minimum opening_degree") 
        return False
      direction = 'dn'
      entry.change_dir = 'Close'
      entry.change_amount = amount

    elif ctrl_val > 0:
      tmp = latest.result_openingdegree + amount
      if (tmp > ctrl.openingdegree_maximum):
        self.ctrl.lg.error("WARNING: above maximum opening_degree") 
        return False
      direction = 'up'
      entry.change_dir = 'Open'
      entry.change_amount = amount

    else:
      logger.error("WARNING: none of both conditions was matched !??")
      return False


    entry.result_openingdegree = tmp
    entry.save()
    ### the actual work
    sa = str(amount)
    self.ctrl.lg.info("mainvalve amount %s (total:%s)- %s", sa, tmp, direction)
    ctrl.work(direction, amount)

    return True


