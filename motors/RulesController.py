from django.shortcuts import get_object_or_404
from motors.rules import *

import motors.rules
from piheatweb.Controller import Controller
from motors.models import Rule, RuleHistory
from motors.tables import RulesListTable

from motors.KlassLoader import KlassLoader
from motors.forms import RuleEditForm


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
    self.template = 'rules/index.html'
    return self.render()

  def rule_delete(self, pk):
#    rule = Rule.objects.get(pk=pk)
    rule = get_object_or_404(Rule, pk=pk)
    rule.delete()
    return self.redirect('/actors/rules/list?msg=The rule was deleted')

  def rule_show(self, pk):
    self.object = get_object_or_404(Rule, pk=pk)
    self.context['title'] = 'Details für Regel ' + self.object.name
    self.context['object'] = self.object
    self.template = 'rules/show.html'
    return self.render()

  def rule_edit(self, pk):
    if not self.request.POST:
      self.object = get_object_or_404(Rule, pk=pk)
      self.context['title'] = 'Regel ' + self.object.name + ' bearbeiten'
      self.context['object'] = self.object
      form = RuleEditForm(instance = self.object)
    else:
      form = RuleEditForm(self.request.POST)
      form.save()
      
    self.context['form'] = form.as_table()
    self.template = 'rules/edit.html'
    return self.render()
