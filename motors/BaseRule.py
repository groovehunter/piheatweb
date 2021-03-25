
from datetime import datetime
from motors.models import Rule, RuleHistory

from django.utils import timezone
#now = timezone.now() # TZ aware :)
import logging
logger = logging.getLogger()


class BaseRule:
  """ maybe:
      provide access to SensorInfo
      Base for 'main' rules = create an own rule_event
  """
  def __init__(self):
    """ common things to do in init. """
    self.now = timezone.now()
    self.DEFAULT_RULE = Rule.objects.get(pk=1)

  def setup(self):
    """ stub if subclass does not need it """
    pass

  def report(self):
    """ stub if subclass does not need it """
    pass

  def set_rule(self, rule):
    """ just need to set rule obj as a member of the subclass
        so we can access it;
        And also create a new RuleHistory entry pointing to the rule obj """
    self.rule = rule
    logger.debug('--- RULE INIT : %s', self.rule.name)

  def check(self):
    raise NotImplemented


class FixedGoalAdjustableActuator(BaseRule):
  """ try to keep one fixed value
      can adjust actuating values es"""

  def report(self):
    logger.debug("CUR: %s -- GOAL %s", self.cur, self.goal)

  # rename to "check_condition"
  def check(self):
    """ false only if very near.
    otherwise adjust in some way """

    if self.diff < 1:
      logger.debug("conditions are OKAY - no action needed")
      self.ctrl.rule_event.result = 0
      self.ctrl.rule_event.save()
      return True
    else:
      self.ctrl.rule_event.result = 1
      self.ctrl.rule_event.save()
      return False

  def action(self):
    raise NotImplemented



class ThresholdRule(BaseRule):
  """ rule which checks one value if between 2 thresholds """

  def report(self):
    #logger.debug("CURRENT: %s", self.cur)
    #logger.debug("Lower and upper: %s %s", self.lower, self.upper)
    pass

  def check(self):
    cur = self.cur
    if (cur > self.lower and cur < self.upper):
      logger.debug("conditions are OKAY - no action needed")
      self.ctrl.rule_event.result = 0
      self.ctrl.rule_event.save()
      return True

    elif (cur < self.lower or cur > self.upper):
      self.ctrl.rule_event.result = 1
      self.ctrl.rule_event.save()
      return False

    else:
      logger.error("threshold check somehow is out any rule!??")
