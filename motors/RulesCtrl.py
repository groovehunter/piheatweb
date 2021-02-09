
from motors.Rules import *
import motors.Rules

from motors import rules
from motors.models import Rule, RuleHistory
from motors.KlassLoader import KlassLoader


class RulesCliCtrl(KlassLoader):
  """ non web controller """
  def setup(self):
    self.klass_list = self.get_klasslist(motors.Rules)
    self.klass_obj_list = {}
    self.list = {}

  def loop_klasses(self):
    count = 0
    for klass_name in self.klass_list:
      print(klass_name)
      # create class object

      constructor = globals()[klass_name]
      self.klass_obj_list[klass_name] = constructor()
#      self.klass = constructor(self)
      count += 1
      # XXX Check if rule already in DB?

  def loop_rules(self):
    self.rules_list()
    for rule in self.list:
      pass

  def rules_list(self):
    #self.list[] = Rule.objects.all()
    pass

  def getRuleByName(self, name):
    rule = Rule.objects.filter(name=name).first()
    return rule

  def test(self):
    name = 'VorlaufGrenzwertRule'
    rule = self.getRuleByName(name)
    if name != rule.name:
      print('mismatch in name, EXIT')
      raise NameError

    rule_klass_obj = self.klass_obj_list[name]
    rule_klass_obj.set_rule(rule)
    rule_klass_obj.check()


