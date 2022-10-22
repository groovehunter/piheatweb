from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from motors.rules import *

import motors.rules
from djflow.ViewController import ViewControllerSupport, DjMixin
from motors.models import Rule, RuleHistory
from motors.tables import RulesListTable

from motors.KlassLoader import KlassLoader
from motors.forms import RuleEditForm

import logging
logger = logging.getLogger()

class RuleListView(ListView, DjMixin):
  model = Rule
  fields_noshow = []
  #self.context['table'] = table
  template_name = 'rules/index.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    c = self.djflow_context_data()
    table = RulesListTable(self.object_list)
    c['table'] = table
    context.update(c)
    return context

class RuleDetailView(DetailView, DjMixin):
  model = Rule
  template_name = 'rules/show.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    c = self.djflow_context_data()
    context.update(c)
    return context


class RulesController(ViewControllerSupport, KlassLoader):
  """ web ui controller """
  def __init__(self, request):
    self.request = request
    self.init_ctrl()
    logger.debug(self.context)

  def rules_check(self):
    if self.request.method=='GET' and 'start' in self.request.GET:
      pass
    else:
      pass
    self.template_name = 'motors/rules.html'
    return self.render()

  def rule_delete(self, pk):
#    rule = Rule.objects.get(pk=pk)
    rule = get_object_or_404(Rule, pk=pk)
    rule.delete()
    return self.redirect('/actors/rules/list?msg=The rule was deleted')

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
    self.template_name = 'rules/edit.html'
    return self.render()
