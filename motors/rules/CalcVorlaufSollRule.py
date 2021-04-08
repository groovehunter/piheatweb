
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)

from motors.Calc import Calc
from motors.models import RuleResultData_01


class CalcMethod:
  def __init__(self):
    self.now = timezone.now()
  def setup(self):
    self.load_sensordata()
  def report(self):
    pass
  def set_rule(self, rule):
    """ just need to set rule obj as a member of the subclass
        so we can access it;
        And also create a new RuleHistory entry pointing to the rule obj """
    self.rule = rule


class CalcVorlaufSollRule(CalcMethod, Calc):
  def check(self):
    """ always execute calculations """
    self.ctrl.rule_event.result = 1
    self.ctrl.rule_event.save()
    return False

  def action(self):
    # calc soll by outdoor - heating kennlinie
    self.soll_calc = (( (self.avg24_outdoor+self.cur_outdoor)/2 ) * -1.1) + 52
    ### nachtabsenkung
    absenk = 0
    if (self.now.hour > 23 or self.now.hour < 5):
      absenk = -7
      logger.debug('nachtabsenkung!!: %s', absenk)
    self.soll_calc = self.soll_calc + absenk
    logger.debug("calculated final Soll:  %s", self.soll_calc)
    self.save()

  def save(self):
    data = RuleResultData_01()
    data.value = self.soll_calc
    data.dtime = self.now
    data.rule_event = self.ctrl.rule_event
    # XXX only AVAIL. when Rule object running
    #data.rule_event = self.
    data.save()
