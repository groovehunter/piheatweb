
from motors.Rules import *
import motors.Rules

from motors import rules
from motors.models import Rule, RuleHistory, RuleResultHistory
from motors.KlassLoader import KlassLoader
from django.utils.timezone import now

logger = logging.getLogger()

class Calc:
  def load_sensordata(self):
    some = SensorData_04.objects.order_by('-dtime')[1:30]
    cur = some.aggregate(Avg('temperature'))['temperature__avg']
    self.cur_outdoor = float(cur)

  def vorlauf_soll_temp(self):
    logger.debug("current outdoor temp %s", self.cur_outdoor)
    logger.debug("calculated Soll by outdoor temp %s", self.soll_calc)

    ### nachtabsenkung
    absenk = 0
    now = datetime.now()
    if (now.hour > 23 or now.hour < 5):
      absenk = -7
    self.soll_calc = self.soll_calc + absenk
    logger.debug('nachtabsenkung?: %s', absenk)
    logger.debug("calculated final Soll:  %s", self.soll_calc)

    # Is Soll to Ist difference more than 2
    if (abs(self.logic - self.soll_calc) > 2):
      logic_new = str(round(self.soll_calc))
      logger.debug("ACT: setting rule logic to %s", logic_new)
      self.rule.logic = logic_new
      self.rule.save()
    else:
      logger.debug('OK - leave rule logic as is: %s', self.rule.logic)


class RulesCliCtrl(KlassLoader, Calc):
  """ non web controller """

  def __init__(self):
    self.now = now()

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
    rule_klass_obj.ctrl = self
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
