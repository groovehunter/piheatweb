
from motors.Rules import *
import motors.Rules

from motors import rules
from motors.models import Rule, RuleHistory
from motors.models import RuleResultData_01
from motors.KlassLoader import KlassLoader
from django.utils.timezone import now

logger = logging.getLogger()

class CalcMethod:
  pass

class CalcVorlaufSoll(CalcMethod):
  def work(self):
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
    #data = RuleResultData_01()
    #data.rule_event = self.


class Calc:
  def load_sensordata(self):
    self.cur_vorlauf  = float(SensorData_01.objects.latest('dtime').temperature)
    logger.debug('load_sensordata: cur_vorlauf: %s', int(self.cur_vorlauf))
    if int(self.cur_vorlauf) == 0:
      logger.error('vorlauf was 0.0 - recalc average of latest 5')
      some_cur_vorlauf  = SensorData_01.objects.order_by('-dtime')[1:5]
      self.cur_vorlauf = float(some_cur_vorlauf.aggregate(Avg('temperature'))['temperature__avg'])
    logger.debug('load_sensordata: cur_vorlauf: %s', self.cur_vorlauf)


    some = SensorData_04.objects.order_by('-dtime')[1:30]
    cur = some.aggregate(Avg('temperature'))['temperature__avg']
    self.cur_outdoor = float(cur)
    # daily average temp
    start_date = self.now - timedelta(hours=24)
    h24 = SensorData_04.objects.filter(dtime__minute=0, dtime__range=(start_date, self.now))
    avg24 = h24.aggregate(Avg('temperature'))['temperature__avg']
    self.avg24_outdoor = float(avg24)

  def load_calcdata(self):
    self.soll_calc_db = RuleResultData_01.objects.latest('-dtime').value

  def getVorlaufSollCalc(self):
    if not hasattr(self, 'soll_calc_db'):
      self.load_calcdata()
    return self.soll_calc_db

  # XXX Move this to rule subclass??? Dann sind alle werte
  # weiterhin nur als ctrl attribute zugänglich,
  # ziemliches kuddelmuddel
  def calc_vorlauf_soll_temp(self):
    # calc soll by outdoor - heating kennlinie
    soll_calc = (( (self.avg24_outdoor+self.cur_outdoor)/2 ) * -1.1) + 52
    ### nachtabsenkung
    absenk = 0
    now = datetime.now()
    if (now.hour > 23 or now.hour < 5):
      absenk = -7
      logger.debug('nachtabsenkung!!: %s', absenk)
    self.soll_calc = int(soll_calc + absenk)
    logger.debug("calculated final Soll:  %s", self.soll_calc)
    data = RuleResultData_01()
    data.value = self.soll_calc
    data.dtime = self.now
    data.rule_event = self.rule_event
    # XXX only AVAIL. when Rule object running
    #data.rule_event = self.
    data.save()




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
    for rule_name, rule_db in self.rules_list_db.items():
      #logger.debug('checking rule: %s ', rule_name)
      if rule_db.active:
        self.check_rule(rule_db)
        logger.debug('checking rule: %s ', rule_name)
      else:
        #logger.debug("... rule inactive")
        pass

  ### rule = a object of db-entry, so find a better name
  def check_rule(self, rule_db):
    self.create_rule_event(rule_db)
    # get object of initiated rule class
    rule_klass_obj = self.klass_obj_list[rule_db.name]
    # this object needs the DB rule entry, so set it
    rule_klass_obj.set_rule(rule_db)
    # the object needs access to self, the controller and its methods
    rule_klass_obj.ctrl = self

    # a few things to setup
    rule_klass_obj.setup()
    # log main values
    rule_klass_obj.report()

    ### NOW: check if rule is fulfilled --> No acting
    if not rule_klass_obj.check():
      rule_klass_obj.action()


  # XXX create OR get existing rule_event
  def create_rule_event(self, rule_db):
    rule_event = RuleHistory()
    rule_event.dtime = self.now
    rule_event.rule = rule_db
    self.rule_event = rule_event


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
