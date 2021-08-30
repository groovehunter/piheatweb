
import logging
logger = logging.getLogger(__name__)

from motors.BaseRule import BaseRule
from motors.HeatPump import HeatPumpCtrl
from motors.WarmwaterPump import WarmwaterPumpCtrl

from motors.models import Mode  #, HeatPumpHistory, WarmwaterPump
from datetime import datetime

class ModeExecutionRule(BaseRule): pass

class ModeConstraintsRule(ModeExecutionRule):

  def __init__(self):
    pass

  def setup(self):
    self.hp_ctrl = HeatPumpCtrl()
    self.hp_ctrl.setup()
    self.ww_ctrl = WarmwaterPumpCtrl()
    self.ww_ctrl.setup()

  def check(self):
    pass

  def action(self):
    mode_name = self.ctrl.mode.name
    logger.debug('mode actions for %s', mode_name)
    if mode_name == 'WarmwaterOnly':
      self.ww_ctrl.enable()
      self.hp_ctrl.disable()

    if mode_name == 'HeatingMode':
      self.hp_ctrl.enable()

    if mode_name == 'AllOff':
      # XXX close main valve first!!
      #self.ww_ctrl.disable()
      #self.hp_ctrl.disable()
      pass


  def save(self):
    pass
