from motors.models import RuleHistory
from motors.BaseRule import BaseRule
from piheatweb.util import *
import logging
from os import environ
logger = logging.getLogger(__name__)
from random import random


class DummyRule(BaseRule):
  """ does nothing """

  def setup(self):
    logic = self.rule.logic

  def history_entry(self):
    return None

  def check(self):
    return int(random())

  def action(self):
    """ act because rule was not fulfilled """
    self.ctrl.rule_event.result = 1

    return True


