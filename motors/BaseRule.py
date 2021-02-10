
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


  def set_rule(self, rule):
    self.rule = rule
    rule_event = RuleHistory()
    rule_event.dtime = self.now
    rule_event.rule = self.rule
    self.rule_event = rule_event

  def check(self):
    print("latest temp: ", self.cur)

  def rule_false(self):
    print("result = FALSE")
    self.rule_event.result = 0
    self.rule_event.save()

