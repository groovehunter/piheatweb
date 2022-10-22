from django.shortcuts import render
from django.template import RequestContext
#from django import forms
from django.http import HttpResponseRedirect
from django.db.models.query import prefetch_related_objects
from django.db.models import Exists, OuterRef

from django.views.generic import ListView, DetailView, CreateView
from piheatweb.ViewController import ViewControllerSupport
from piheatweb.Controller import Controller
from piheatweb.forms import GraphAttributesForm

from .models import Motor, Rule, RuleHistory
from .models import MainValveHistory, WarmwaterPumpHistory
from .tables import MotorListTable, MainValveListTable, WarmwaterPumpListTable
from motors.MainValveController import MainValveController
from motors.WarmwaterPumpController import WarmwaterPumpController
from motors.RulesController import RulesController
from cntrl.models import ControlEvent
from piheatweb.graphutils import GraphMixin

#from datetime import datetime, timedelta
from django.utils import timezone
now = timezone.now()
from random import randint
import logging
logger = logging.getLogger(__name__)



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
#        logger.debug(kwargs)
        self.object = self.get_object() #labelterm=kwargs['pk'])
        self.template_name = 'motors/show.html'
        self.fields_noshow = []
        self.context['title'] = "Motor / Aktor - Detail view"
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
        self.init_ctrl()
        start_date = now - timedelta(hours=3)
        end_date = now
        mvh = MainValveHistory.objects.all().order_by('-id')
        self.object_list = mvh

        self.fields_noshow = []
        table = MainValveListTable(self.object_list)
        self.context['table'] = table
        self.context.update(self.get_context_data())
        self.template_name = 'motors/index.html'
        return self.render()


class WarmwaterPumpHistoryView(ListView, ViewControllerSupport):
    """ history table of WarmwaterPump changes """
    model = WarmwaterPumpHistory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = self.listview_helper()
        context.update(c)
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = WarmwaterPumpHistory.objects.order_by('-id')
        self.init_ctrl()
        self.fields_noshow = []
        table = WarmwaterPumpListTable(self.object_list)
        self.context['table'] = table
        self.context.update(self.get_context_data())
        self.template_name = 'motors/index.html'
        return self.render()


class MotorController(ViewControllerSupport, GraphMixin):
    def __init__(self, request):
        self.request = request
        self.now = timezone.now()
        self.init_ctrl()

    def show(self, pk):
      self.object = Motor.objects.filter(id=pk).first()
      self.template_name = 'motors/show.html'
      history = True
      self.context.update( {'history': history} )

#      klass_name = self.object.ctrl_class
      #self.context['debug'] = kn
#      constructor = globals()[klass_name]
#      self.motor_ctrl = constructor()
      self.object_list = MainValveHistory.objects.all()[:100]
      table = MainValveListTable(self.object_list)
      self.context['table'] = table
      return self.render()

    def graphmv(self):
      self.graph_form()

      mvh = MainValveHistory.objects.filter(rule_event=OuterRef('id'))
      rh = RuleHistory.objects.filter(ctrl_event=OuterRef('id'))
      ce = ControlEvent.objects.filter(Exists(rh), dtime__range=(self.start_date, self.now)).order_by('-dtime')
      nl = 2

      self.setup_graph(nl)

      logger.debug(len(ce))
      for obj in ce:
        for i in range(nl):
          self.timedict[i].append(obj.dtime)
        #val = obj.rulehistory_set.first().mainvalvehistory_set.first()
        rh = obj.rulehistory_set.first()
        if hasattr(rh, 'warmwaterpumphistory_set'):
          val = rh.warmwaterpumphistory_set.first()
          if val:
            self.tempdict[0].append(val.change_status)
        if hasattr(rh, 'mainvalvehistory_set'):
          val = rh.mainvalvehistory_set.first()
          if val:
            self.tempdict[1].append(val.result_openingdegree)

      self.plotter(nl)

      self.template_name = 'motors/graph.html'
      return self.render()


    def graph_results(self):
      self.graph_form()

      rules = Rule.objects.filter(active=True).all()
      rh = RuleHistory.objects.filter(ctrl_event=OuterRef('id')).order_by('-id')
      ce = ControlEvent.objects.filter(Exists(rh), dtime__range=(start_date, self.now)).order_by('-dtime')

      logger.debug('CE len: %s', len(ce))
      # init graph data dict
      nl = len(rules)
      self.setup_graph(nl)

      for i in range(nl):
        self.info[i] = rules[i].name

      tz = timezone.get_current_timezone()
      for obj in ce:
        for i in range(nl):
          self.timedict[i].append(obj.dtime)

        c = 0
        rhs = obj.rulehistory_set.all().order_by('rule')
        if len(rhs) == nl:    # all expected rh entries available
          for i in range(nl):
            rh = rhs[i]
            self.tempdict[c].append(rh.result)
            c+=1

        else:
          for i in range(nl):
            if not i >= len(rhs):
              rh = rhs[i]
              self.tempdict[c].append(rh.result)
            else:
              logger.debug('RH entry missing at ')
              logger.debug(obj.dtime)
              self.tempdict[c].append(None)
            c+=1

      #self.plotter(nl)
      self.pl2()
      self.template_name = 'motors/graph.html'
      return self.render()



def control(request):
  ctrl = MainValveController(request)
  return ctrl.control_input()

def ww_control(request):
  ctrl = WarmwaterPumpController(request)
  return ctrl.control_input()

def rules_check(request):
  ctrl = RulesController(request)
  return ctrl.rules_check()

def rules_list(request):
  ctrl = RulesController(request)
  return ctrl.rules_list()

def rule_delete(request, pk):
  ctrl = RulesController(request)
  return ctrl.rule_delete(pk)

def rule_show(request, pk):
  ctrl = RulesController(request)
  return ctrl.rule_show(pk)

def rule_edit(request, pk):
  ctrl = RulesController(request)
  return ctrl.rule_edit(pk)

#### Motor
def action(request, method):
  logger.debug('views action', method)
  ctrl = MotorController(request)
  return eval('ctrl.'+method+'()')

def show(request, pk):
  ctrl = MotorController(request)
  return ctrl.show(pk)

def graph_results(request):
  ctrl = MotorController(request)
  return ctrl.graph_results()

def graphmv(request):
  ctrl = MotorController(request)
  return ctrl.graphmv()
