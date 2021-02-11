
from datetime import datetime
from motors.models import Rule, RuleHistory

from django.utils import timezone
#now = timezone.now() # TZ aware :)


class BaseRule:
  """ maybe:
      provide access to SensorInfo
  """
  def __init__(self):
    """ common things to do in init. """
    self.now = timezone.now()
    self.DEFAULT_RULE = Rule.objects.get(pk=1)
    print('init base rule', self.__class__.__name__)

  def setup(self):
    """ stub if subclass does not need it """
    pass

  def report(self):
    pass

  def set_rule(self, rule):
    """ just need to set rule obj as a member of the subclass 
        so we can access it; 
        And also create a new RuleHistory entry pointing to the rule obj """
    self.rule = rule

    rule_event = RuleHistory()
    rule_event.dtime = self.now
    rule_event.rule = self.rule
    self.rule_event = rule_event


  def check(self):
    raise NotImplemented

#  def rule_false(self):
#    print("result = FALSE")
#    self.rule_event.result = 0
#    self.rule_event.save()


class ThresholdRule(BaseRule):
  """ rule which checks one value if between 2 thresholds """

  def report(self):
    print("CURRENT: ", self.cur)
    print("Lower and upper: ", self.lower, self.upper)

  def check(self):
    cur = self.cur
    if (cur > self.lower and cur < self.upper):
      print("conditions are OKAY - no action needed")
      self.rule_event.result = 0
      self.rule_event.save()
      return True

    elif (cur < self.lower or cur > self.upper):
      print("correct conditions not fulfilled - going to ACT")
      return False



