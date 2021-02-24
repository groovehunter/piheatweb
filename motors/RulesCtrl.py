
from motors.Rules import *
import motors.Rules

from motors import rules
from motors.models import Rule, RuleHistory
#from motors.models import RuleResultHistory
from motors.KlassLoader import KlassLoader
from django.utils.timezone import now

logger = logging.getLogger()

class Nachtabsenkung(BaseRule):
  pass

class IntermediateRule:
  """ rule that calcs some intermediate values from sensor date
      and stores them, ie as logic for other rules """
  def work(self):
    pass

class CalcVorlaufSoll(IntermediateRule):
  def work(self):
    # 2 steps: use outdoor wisely
    # apply nightabsenk    
    pass

class Calc:
  def load_sensordata(self):
    some = SensorData_04.objects.order_by('-dtime')[1:30]
    cur = some.aggregate(Avg('temperature'))['temperature__avg']
    self.cur_outdoor = float(cur)

  def vorlauf_soll_temp(self):
    # daily average temp
    start_date = self.now - timedelta(hours=24)
    h24 = SensorData_04.objects.filter(dtime__minute=0, dtime__range=(start_date, self.now))
    avg24 = h24.aggregate(Avg('temperature'))['temperature__avg']
    self.avg24_outdoor = float(avg24)

    # calc soll by outdoor - heating kennlinie
    self.soll_calc = (( (self.avg24_outdoor+self.cur_outdoor)/2 ) * -1.1) + 52

    ### nachtabsenkung
    absenk = 0
    now = datetime.now()
    if (now.hour > 23 or now.hour < 5):
      absenk = -7
      logger.debug('nachtabsenkung!!: %s', absenk)
    self.soll_calc = self.soll_calc + absenk
    logger.debug("calculated final Soll:  %s", self.soll_calc)

    # XXX save to DB


class RulesCliCtrl(KlassLoader, Calc):
  """ non web controller """

  def __init__(self):
    self.now = now()

  def setup(self):
    self.klass_list = self.get_klasslist(motors.Rules)
    self.load_sensordata()

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
