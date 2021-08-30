
import logging
logger = logging.getLogger(__name__)

from motors.Calc import Calc
from motors.CalcMethod import CalcMethod
from motors.models import RuleResultData_01
from datetime import datetime



class CalcVorlaufSollRule(CalcMethod, Calc):
  charac_add = 54.0
  charac_fac = -1.4
  night_base = 5.0

  def action(self):
    if self.ctrl.mode.name == 'WarmwaterOnly':
      self.soll_calc = float(self.rule.logic)
      logger.debug("FIXED Vorlauf Soll:  %s", self.soll_calc)
      self.save()
      return

    # calc soll by outdoor - heating kennlinie
    #[Vorlauftemperatur] = Neigung * 1.8317984 * ([Raumtemperatur Soll] - ([Außentemperatur Gedämpft]*0,7 + [Außentemperatur Ist]*0,3) )^0.8281902 + Niveau + [Raumtemperatur Soll]

    temp = (self.avg24_outdoor+3*self.cur_outdoor) / 4
    #vl= 0.5 * 1.8317984 * (21.0 - temp)**0.8281902 + 1.0 + 21.0
#    logger.debug('vl %s', vl)

#    logger.debug('outdoor avg %s', temp)
#    logger.debug('temp - 20 %s', temp-20)
    w = ((temp-20) * self.charac_fac)
#    logger.debug('after fac %s', w)
    self.soll_calc = w + 32
    #self.soll_calc = ((temp-20) * self.charac_fac) + 25

#    self.soll_calc = (temp * self.charac_fac) + self.charac_add
    ### nachtabsenkung
    absenk = self.get_night_decrease()
    logger.debug('nachtabsenkung!!: %s', absenk)
    self.soll_calc = self.soll_calc - absenk
    if self.soll_calc < 35.0:
      self.soll_calc = 35.0

    logger.debug("calculated final Soll:  %s", self.soll_calc)
    self.save()

  def get_night_decrease(self):
    #now = self.now
    now = datetime.now()  # = time of user, between 23 and 5 o'clock
    #logger.debug(now.hour)
    if (now.hour < 23 and now.hour > 6):
      return 0.0
    if now.hour == 23:
      return now.minute * self.night_base / 60.0
    if now.hour == 5:
      return (60 - now.minute) * self.night_base / 60.0
    return self.night_base

  def save(self):
    data = RuleResultData_01()
    data.value = round(self.soll_calc, 2)
    data.dtime = self.now
    data.rule_event = self.ctrl.rule_event
    # XXX only AVAIL. when Rule object running
    #data.rule_event = self.
    data.save()
