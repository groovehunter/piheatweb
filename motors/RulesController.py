
from motors.rules import *

import motors.rules
from piheatweb.Controller import Controller
from motors.models import Rule, RuleHistory
from motors.tables import RulesListTable

from motors.KlassLoader import KlassLoader


class RulesController(Controller, KlassLoader):
  """ web ui controller """
  def __init__(self, request):
    Controller.__init__(self, request)

  def rules_check(self):
    if self.request.method=='GET' and 'start' in self.request.GET:
      pass
    else:
      pass
    self.template = 'motors/rules.html'
    return self.render()

  def rules_list(self):
    object_list = Rule.objects.all()
    table = RulesListTable(object_list)
    self.context['table'] = table
    self.template = 'motors/index.html'
    return self.render()
