from django.shortcuts import render
from django.template import RequestContext
#from django import forms
from django.http import HttpResponseRedirect
from django.db.models.query import prefetch_related_objects

from django.views.generic import ListView, DetailView, CreateView
from piheatweb.ViewController import ViewControllerSupport
from piheatweb.Controller import Controller
from piheatweb.forms import GraphAttributesForm

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
from plotly.graph_objs import Scatter, Figure
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
      start_date = self.now - timedelta(hours=sincehours)

      logger.debug('graph start date: %s', start_date)
      myrule = Rule.objects.get(name='CalcVorlaufSollRule')
#      rh = RuleHistory.objects.filter(rule=myrule, dtime__range=(start_date, self.now)).order_by('dtime')[30:]
      ### query all CE, I guess those without corresponding RH
      # we need to skip later
      ce = ControlEvent.objects.filter(dtime__range=(start_date, self.now)).order_by('dtime')
      logger.debug('CE len: %s', len(ce))
      # init graph data dict
      tempdict = {}
      timedict = {}
      rrd = {}
      l = 2
      nl = 5
      for i in range(nl):
        tempdict[i] = []
        timedict[i] = []

      tz = timezone.get_current_timezone()
      rule0 = Rule.objects.filter(name='CalcVorlaufSollRule').first()
      rule1 = Rule.objects.filter(name='CalcPI_ControlRule').first()

      ce = []
      logger.debug('ce', ce)
      for obj in ce:
        #time = obj.dtime.astimezone(tz=tz)
        #logger.debug('X')
        #logger.debug('time', type(time))
        """
        rhs = obj.rulehistory_set
        logger.debug('rhs', rhs)
        skipped = 0
        if rhs.count() == 0:
          skipped += 1
          continue
        """
        for i in range(nl):
          timedict[i].append(time)

        val = 13 #dummy
        rh = rhs.filter(rule=rule0).first()
        #logger.debug(rh)
        if rh:
          rrd = rh.ruleresultdata_01_set.first()
          if rrd:
            val = rrd.value
        tempdict[0].append(val)

        val = 0
        rh = rhs.filter(rule=rule1).first()
        logger.debug('rh', rh)
        if rh:
          for i in range(1,5):
            si = '0'+str(i+1)
            evalstr = 'rh.ruleresultdata_'+si+'_set.first()'
            rrd = eval(evalstr)
            if rrd:
              logger.debug('rrd.value', rrd.value)
              tempdict[i].append(rrd.value)

      logger.debug('Rhs count==0 so skipped  %s events', skipped)

      logger.debug('len tempdict: %s', len(tempdict[i]))
      logger.debug('tempdict: %s', tempdict[i])
      logger.debug('len timedict: %s', len(timedict[i]))

      sc = {}
      col = {0:'green', 1:'blue', 2:'red', 3:'orange', 4:'black'}
      info = {
        0: 'RRD1 / CalcSoll', 
        1: 'PID output ---------', 
        2: 'P-faktor',
        3: 'I-faktor',
        4: 'D-faktor',
      }

      fig = Figure()
      for i in range(5):
        sc[i] = Scatter(
                    #title = 'PID values',
                    x=timedict[i], y=tempdict[i],
                    mode='lines+markers', 
                    name=info[i],
                    opacity=0.99, 
                    #marker_color=col[i],
                    #marker=dict(size=[40, 60], color=[0, 1,])
        )
      fig.add_trace(sc[1])

      plt_div = plot([ sc[1], sc[2], sc[3], sc[4]], output_type='div')
      #plt_div = plot(sc, output_type='div')
      self.context['plt_div'] = plt_div

      form = GraphAttributesForm()
      self.context['form'] = form
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
  logger.debug('views action', method)
  ctrl = MotorController(request)
  return eval('ctrl.'+method+'()')

def show(request, pk):
  ctrl = MotorController(request)
  return ctrl.show(pk)

def graph(request):
  ctrl = MotorController(request)
  return ctrl.graph()

