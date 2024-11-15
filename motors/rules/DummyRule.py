from motors.models import RuleHistory
from motors.BaseRule import BaseRule
from piheatweb.util import *
import logging
logger = logging.getLogger(__name__)
from random import random


class DummyRule(BaseRule):
  """ does nothing / Random results """

  def setup(self):
    logic = self.rule.logic

  def history_entry(self):
    return None

  def check(self):
    matched = int(random())
    #logger.debug("matched %s", matched)
    self.ctrl.rule_event.rule_matched = matched
    self.ctrl.rule_event.save()

    return matched


  def action(self):
    """ act because rule was not fulfilled """
    result = int(100*random())
    self.ctrl.rule_event.result = result
    self.ctrl.rule_event.save()

    return True


