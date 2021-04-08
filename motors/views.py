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
      start_date = self.now - timedelta(hours=sincehours)

      logger.debug('graph start date: %s', start_date)
      myrule = Rule.objects.get(name='CalcVorlaufSollRule')
#      rh = RuleHistory.objects.filter(rule=myrule, dtime__range=(start_date, self.now)).order_by('dtime')[30:]
      ### query all CE, I guess those without corresponding RH
      # we need to skip later
      ce = ControlEvent.objects.filter(dtime__range=(start_date, self.now)).order_by('dtime')
#      logger.debug('RH len %s', len(rh))
      logger.debug('CE len: %s', len(ce))
#      mv = MainValveHistory.objects.filter(dtime__range=(start_date, self.now))
      tempdict = {}
      timedict = {}
      rrd = {}
      l = 2
      for i in range(l):
        tempdict[i] = []
        timedict[i] = []

      tz = timezone.get_current_timezone()

      for obj in ce:

        time = obj.dtime.astimezone(tz=tz)
        logger.debug('=== NEXT: %s', time)
        rhs = obj.rulehistory_set
        if rhs.count() == 0:
          logger.debug('Rhs count==0 for this ce %s -- skipping!', obj)
          continue

        for i in range(l):
          timedict[i].append(time)

        val = 0
        rh = rhs.filter(rule_id=9).first()
        if rh:
          rrd = rh.ruleresultdata_01_set.first()
          if rrd:
            val = rrd.value
        tempdict[0].append(val)

        val = 0
        rh = rhs.filter(rule_id=4).first()
        if rh:
          res = rh.mainvalvehistory_set.first()
          if res:
            val = res.result_openingdegree
            val = val / 1000
            logger.debug("val: %s", val)
            if val > 3000:
              val = val / 100
          else:
            logger.debug('NO mv entry')
        tempdict[1].append(val)

        """
        rule_ids = [4, 9] # len must match "l"
        i = 0
        for rid in rule_ids:
          rh = rhs.filter(rule_id=rid).first()
          logger.debug('rh %s', rh)
          if rh == None:
            tempdict[i].append(20) #dummy
            i += 1
            continue
          if rid == 4:
            rrd = rh.ruleresultdata_01_set.first()
          if rid == 9:
            rrd = None

          if rrd == None:
            logger.debug("RRD: %s", rrd)
            tempdict[i].append(50)
          else:
            tempdict[i].append(rrd.value)
            logger.debug("RRD: %s", i, rrd.value)
          i += 1
        """

      for i in range(l):
        logger.debug('len tempdict: %s', len(tempdict[i]))
        logger.debug('len timedict: %s', len(timedict[i]))
#      logger.debug('tempdict-1: %s', tempdict[1])
#      logger.debug('len timedict: %s', len(timedict[i]))

#      self.context['debug'] = c
      sc = {}
      col = {0:'green', 1:'blue', 2:'red', 3:'orange'}
      info = {
        0: 'RRD1 / CalcSoll', 1: 'RRD2 / ANY', 2: 'RRD3',
      }

      for i in range(l):
        logger.debug(i)
        sc[i] = Scatter(x=timedict[i], y=tempdict[i], \
                        mode='lines', name=info[i], \
                        opacity=0.8, marker_color=col[i])

      plt_div = plot([sc[0], sc[1]], output_type='div')
      #plt_div = plot(sc, output_type='div')
      self.context['plt_div'] = plt_div
      #logger.debug(plt_div)
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
  ctrl = MotorController(request)
  return eval('ctrl.'+method+'()')

def show(request, pk):
  ctrl = MotorController(request)
  return ctrl.show(pk)
