from django.shortcuts import render
from django.template import RequestContext
from django import forms
from django.http import HttpResponseRedirect

from .models import Motor, Rule, RuleHistory, MainValveHistory

from .tables import MotorListTable, MainValveListTable

from django.views.generic import ListView, DetailView, CreateView
from piheatweb.ViewController import ViewControllerSupport
from piheatweb.Controller import Controller

from datetime import datetime


class MotorListView(ListView, ViewControllerSupport):
    model = Motor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = self.listview_helper()
        context.update(c)
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        self.fields_noshow = []
        table = MotorListTable(self.object_list)
        self.init_ctrl()
        self.context['table'] = table
        self.template_name = 'motors/index.html'
        self.context.update(self.get_context_data())
        return self.render()


class MotorDetailView(DetailView, ViewControllerSupport):
    model = Motor
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = self.listview_helper()
        context.update(c)
        return context

    def get(self, request, *args, **kwargs):
        self.init_ctrl()
#        self.lg.debug(kwargs)
        self.object = self.get_object() #labelterm=kwargs['pk'])
        self.template_name = 'motors/show.html'
        self.fields_noshow = []
        self.context.update(self.get_context_data())
        return self.render()


class MainValveHistoryView(ListView, ViewControllerSupport):
    """ history table of main valve changes """
    model = MainValveHistory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = self.listview_helper()
        context.update(c)
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        self.init_ctrl()
        self.fields_noshow = []
        table = MainValveListTable(self.object_list)
        self.context['table'] = table
        self.context.update(self.get_context_data())
        self.template_name = 'motors/index.html'
        return self.render()



amountlist = (
  (200, 200),
  (300, 300),
  (400, 400),
  (500, 500),
  (800, 800),
  (1000, 1000),
)
class MVControlForm(forms.Form):
  amount    = forms.ChoiceField(label='Amount',
    choices = amountlist
    )
  direction = forms.ChoiceField(label='Direction',
    choices = (('Open', 'up'), ('Close', 'dn'))
    )

class MainValveController(Controller):
  def __init__(self, request):
    Controller.__init__(self, request)
    self.template = 'motors/mainvalvectrl.html'

  def control(self):
    pass

  def control_input(self):
    request = self.request
    cur = MainValveHistory.objects.latest('dtime')

    self.context['cur'] = cur
    if request.method == 'POST':
        form = MVControlForm(request.POST)
        if form.is_valid():
            from platform import machine
            if machine() == 'armv7l':
              from motors.MainValveCtrl import MainValveCtrl
              mvc = MainValveCtrl()
            else:
              from motors.models import DEFAULT_RULE
              from motors.MainValveCtrlDummy import MainValveCtrlDummy
              mvc = MainValveCtrlDummy()
              POST = self.request.POST
              direction = POST['direction']
              amount = int(POST['amount'])
              mvc.work(direction, amount)
              latest = MainValveHistory.objects.latest('dtime')
              latest_degree = latest.result_openingdegree
              if direction == 'Open':
                result_openingdegree = latest_degree + amount
              if direction == 'Close':
                result_openingdegree = latest_degree - amount
              now = datetime.now()
              rule = Rule.objects.get(pk=DEFAULT_RULE)
              entry = MainValveHistory(
                dtime = now,
                change_amount = amount,
                change_dir = direction,
                result_openingdegree = result_openingdegree,
                rule = rule
              )
              entry.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/actors/mainvalve')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MVControlForm()

    self.context['form'] = form
    return render(self.request, self.template, self.context)




def control(request):
  ctrl = MainValveController(request)
  return ctrl.control_input()
