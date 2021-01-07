
from motors.rules import *

import motors.rules
import inspect
from piheatweb.Controller import Controller
from motors.models import Rule, RuleHistory
from motors.tables import RulesListTable


class KlassLoader:

  def get_klasslist(self, module):
    klass_list = []
    for name, obj in inspect.getmembers(module):
      if inspect.isclass(obj):
        #print(name, obj)
        klass_list.append(obj.__name__)
#    if 'LightPattern' in pattern_list:
#        pattern_list.remove('LightPattern')
    return klass_list


class RulesController(Controller, KlassLoader):
  def __init__(self, request):
    Controller.__init__(self, request)
    self.klass_list = self.get_klasslist('rules')

  def loop_klasses(self):
    for klass_name in self.klass_list:
      # create class object
      constructor = globals()[klass_name]
      self.klass = constructor(self)

  def rules_check(self):
    self.template = 'motors/index.html'
    return self.render()


  def rules_list(self):

    object_list = Rule.objects.all()
    table = RulesListTable(object_list)
    self.context['table'] = table
    self.template = 'motors/index.html'
    return self.render()
