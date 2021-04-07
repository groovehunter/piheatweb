from django.shortcuts import render
from django.template import RequestContext
#from django import forms
from django.http import HttpResponseRedirect
from django.db.models.query import prefetch_related_objects

from django.views.generic import ListView, DetailView, CreateView
from piheatweb.ViewController import ViewControllerSupport
from piheatweb.Controller import Controller

from .models import Motor, Rule, RuleHistory, RuleResultData_01, RuleResultData_02
from .models import MainValveHistory, WarmwaterPumpHistory
from .tables import MotorListTable, MainValveListTable, WarmwaterPumpListTable
from motors.MainValveController import MainValveController
from motors.WarmwaterPumpController import WarmwaterPumpController
from motors.RulesController import RulesController
from cntrl.models import ControlEvent

from datetime import datetime, timedelta
from django.utils import timezone
now = timezone.now()
from random import randint
import logging
logger = logging.getLogger(__name__)

from plotly.offline import plot
#import plotly.graph_objs as go
from plotly.graph_objs import Scatter
import plotly.express as px


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
        self.object_list = MainValveHistory.objects.filter(dtime__range=(start_date, end_date)).order_by('-id')

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


class MotorController(Controller):
    def __init__(self, request):
        Controller.__init__(self, request)
        self.now = datetime.now()

    def show(self, pk):
      self.object = Motor.objects.filter(id=pk).first()
      self.template = 'motors/show.html'
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


    def graph(self):
      GET = self.request.GET
      sincehours = int(GET.get('sincehours', default=3))
      start_date = self.now - timedelta(hours=3)
      #events = ControlEvent.objects.filter(dtime__range=(start_date, self.now))

      logger.debug(self.now)
      logger.debug(start_date)
      myrule = Rule.objects.get(name='CalcVorlaufSollRule')
      rh = RuleHistory.objects.filter(rule=myrule, dtime__range=(start_date, self.now)).order_by('dtime')[30:]
      logger.debug(len(rh))
      #logger.debug(rh)
      #mv = MainValveHistory.objects.filter(dtime__range=(start_date, self.now))
      #info = Motor.objects.order_by('id').all()
      tempdict = {}
      timedict = {}
      c=0
      """
      for i in range(len(rh)):
        tempdict[i] = []
        timedict[i] = []
      """
      i = 0
      tempdict[i] = []
      timedict[i] = []

      for obj in rh:
        time = obj.dtime
#        logger.debug("object in looping : %s", obj)
        timedict[i].append(time)
        rrd = obj.ruleresultdata_01_set.first()

        if rrd == None:
          logger.debug(rrd)
          tempdict[i].append(50)
        else:
          tempdict[i].append(rrd.value)
        #tempdict[i].append(rrd.value)
        c+=1

      logger.debug(tempdict[i])
      logger.debug(timedict[i])
      logger.debug(len(tempdict[i]))
      logger.debug(len(timedict[i]))
      self.context['debug'] = c
      sc = {}
      col = {0:'green', 1:'blue', 2:'red', 3:'orange'}
      info = { 0: 'RRD', 1: 'RuleResultData_01' }
      """
      for i in range(1):
        logger.debug(i)
        sc[i] = Scatter(x=timedict[i], y=tempdict[i], \
                        mode='lines', name=info[i], \
                        opacity=0.8, marker_color=col[i])
      """
      i = 0
      sc[i] = Scatter(x=timedict[i], y=tempdict[i], \
                        mode='lines', name=info[i], \
                        opacity=0.8, marker_color=col[i])

      plt_div = plot([sc[0],], output_type='div')
      #plt_div = plot(sc, output_type='div')
      self.context['plt_div'] = plt_div
      #logger.debug(plt_div)
      self.template = 'motors/graph.html'
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
  ctrl = MotorController(request)
  return eval('ctrl.'+method+'()')

def show(request, pk):
  ctrl = MotorController(request)
  return ctrl.show(pk)
