from django.utils import timezone

class CalcMethod:
  def __init__(self, dry=False):
    self.now = timezone.now()
    self.dry = dry
  def setup(self):
    self.load_sensordata()
  def check(self):
    """ always execute calculations """
    self.ctrl.rule_event.rule_matched = 1
    self.ctrl.rule_event.save()
    return False # always do action because rule "not fulfilled"

  def report(self):
    pass

  def set_rule(self, rule):
    """ just need to set rule obj as a member of the subclass
        so we can access it;
        And also create a new RuleHistory entry pointing to the rule obj """
    self.rule = rule
