
import motors.rules

from motors import rules
from motors.rules import *
from motors.models import Rule, RuleHistory
from motors.models import RuleResultData_01
from motors.KlassLoader import KlassLoader
from cntrl.models import ControlEvent
from django.utils import timezone
from sensors.models import SensorData_01, SensorData_04
from django.db.models import Avg, Max, Min, Sum
from datetime import datetime, timedelta
import logging
logger = logging.getLogger(__name__)


from motors.Calc import Calc


class RulesCliCtrl(KlassLoader, Calc):
  """ non web controller """

  def __init__(self):
    self.now = timezone.now()
    self.latest_ctrl_event()

  def setup(self):
    self.klass_list = self.get_klasslist(motors.rules)
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
      else:
        #logger.debug("... rule inactive")
        pass

  ### rule = a object of db-entry, so find a better name
  def check_rule(self, rule_db):
    logger.debug("check rule %s", rule_db)
    self.create_rule_event(rule_db)
    # get object of initiated rule class
    rule_klass_obj = self.klass_obj_list[rule_db.name]
    # this object needs the DB rule entry, so set it
    rule_klass_obj.set_rule(rule_db)
    # rule_klass_obj.create_rule_event() # NOW ctrl method
    # the object needs access to self, the controller and its methods
    rule_klass_obj.ctrl = self

    # a few things to setup
    rule_klass_obj.setup()
    # log main values
    rule_klass_obj.report()

    ### NOW: check if rule is fulfilled --> No acting
    if not rule_klass_obj.check():
      rule_klass_obj.action()

  def latest_ctrl_event(self):
    self.ctrl_event = ControlEvent.objects.latest('dtime')

  # XXX create OR get existing rule_event
  def create_rule_event(self, rule_db):
    rule_event = RuleHistory()
    rule_event.dtime = self.now
    rule_event.rule = rule_db
    rule_event.ctrl_event = self.ctrl_event
    self.rule_event = rule_event
    ### XXX when is this saved?? 

  def setval(self, rulename, val):
    rule_db = self.rules_list_db[rulename]
    rule_db.logic = val
    rule_db.save()

  def test(self):
    name = 'VorlaufRule'
    rule = self.rules_list_db[name]

    rule_klass_obj = self.klass_obj_list[name]
    rule_klass_obj.set_rule(rule)

    rule_klass_obj.setup()
    rule_klass_obj.report()
    if not rule_klass_obj.check():
      rule_klass_obj.action()
