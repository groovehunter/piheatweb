
from motors.Rules import *
import motors.Rules

from motors import rules
from motors.models import Rule, RuleHistory
from motors.KlassLoader import KlassLoader

logger = logging.getLogger()

class RulesCliCtrl(KlassLoader):
  """ non web controller """
  def setup(self):
    self.klass_list = self.get_klasslist(motors.Rules)

  def initiate_klasses_obj(self):
    """ initiate all classes of Rules.py module """
    self.klass_obj_list = {}
    for klass_name in self.klass_list:
      constructor = globals()[klass_name]
      self.klass_obj_list[klass_name] = constructor()

  def load_rules_from_db(self):
    self.rules_list_db = {}
    rules = Rule.objects.all()
    for rule in rules:
      self.rules_list_db[rule.name] = rule

  def loop_rules(self):
    """ load all rules from db and loop them """
    for rule_name, rule in self.rules_list_db.items():
      #logger.debug('checking rule: %s ', rule_name)
      if rule.active:
        self.check_rule(rule)
        logger.debug('checking rule: %s ', rule_name)
      else:
        #logger.debug("... rule inactive")
        pass

  def check_rule(self, rule):
    rule_klass_obj = self.klass_obj_list[rule.name]
    rule_klass_obj.set_rule(rule)

    rule_klass_obj.setup()
    rule_klass_obj.report()
    if not rule_klass_obj.check():
      rule_klass_obj.action()

  def setval(self, rulename, val):
    rule_db = self.rules_list_db[rulename]
    rule_db.logic = val
    rule_db.save()

  def test(self):
    name = 'VorlaufRule'
    logger.debug('check Rule %s', name)
    rule = self.rules_list_db[name]

    rule_klass_obj = self.klass_obj_list[name]
    rule_klass_obj.set_rule(rule)

    rule_klass_obj.setup()
    rule_klass_obj.report()
    if not rule_klass_obj.check():
      rule_klass_obj.action()


