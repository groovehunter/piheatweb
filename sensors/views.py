from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import ListView, DetailView, CreateView
from django.utils import timezone

from .models import SensorData_01, SensorData_02, \
SensorData_03, SensorData_04
from cntrl.models import ControlEvent
from .models import SensorInfo
from .tables import SensorDetailTable, SensorListTable, \
SensorDataTable, AllSensorTable
from djflow.ViewController import ViewControllerSupport
from djflow.Controller import Controller
from piheatweb.forms import GraphAttributesForm
from piheatweb.graphutils import GraphMixin

import datetime
from plotly.offline import plot
#import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Figure
import plotly.express as px

import logging
logger = logging.getLogger(__name__)


class SensorListView(ListView, ViewControllerSupport):
    model = SensorInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = self.listview_helper()
        context.update(c)
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        self.fields_noshow = []
        table = SensorListTable(self.object_list)
        self.init_ctrl()
        self.context['table'] = table
        self.context['object_list'] = self.object_list
        self.template_name = 'sensors/index.html'
        self.context.update(self.get_context_data())
        return self.render()


class SensorDetailView(DetailView, ViewControllerSupport):
    """ show info of sensor

        maybe only in header and recent measurements in table below
    """
    model = SensorInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = self.listview_helper()
        context.update(c)
        return context

    def get(self, request, *args, **kwargs):
        self.init_ctrl()
#        self.lg.debug(kwargs)
        self.object = self.get_object() #labelterm=kwargs['pk'])
        self.template_name = 'show.html'
        self.fields_noshow = []
        self.context.update(self.get_context_data())
        return self.render()


class SensorDataView(Controller, GraphMixin):
    """ data of sensor """

    def __init__(self, request):
        Controller.__init__(self, request)
        self.now = timezone.now()

    def all_sensors(self, *args):
      """ all sensors temp next to each other
          parameter daterange
      """
      self.graph_form()

      cevents = ControlEvent.objects.all().order_by('-id').select_related()
      #cevents = ControlEvent.objects.filter(dtime__minute=0).order_by('-id').select_related()
      object_list = []
      logger.debug(len(cevents))
      line = []
      for obj in cevents:
        logger.debug(obj.id)
        try:
          s01 = obj.sensordata_01.temperature
        except ControlEvent.sensordata_01.RelatedObjectDoesNotExist:
          logger.debug('s01 not found')
          s01 = 77.7
        try:
          s02 = obj.sensordata_02.temperature
        except ControlEvent.sensordata_02.RelatedObjectDoesNotExist:
          s02 = None
          logger.debug('s02 not found')
        try:
          s03 = obj.sensordata_03.temperature
        except ControlEvent.sensordata_03.RelatedObjectDoesNotExist:
          s03 = None
          logger.debug('s03 not found')
        try:
          s04 = obj.sensordata_04.temperature
        except ControlEvent.sensordata_04.RelatedObjectDoesNotExist:
          s04 = None
          logger.debug('s04 not found')
        d = {
          'dtime':obj.dtime,
          'sid01':s01,
          'sid02':s02,
          'sid03':s03,
          'sid04':s04,
              }
        line.append(d)
      object_list = line

      table = AllSensorTable(object_list)
      self.context['table'] = table
      self.template = 'sensors/data.html'
      #self.context['object_list'] = object_list
      #self.context['data'] = object_list
      keys = ['dtime', 'temp', 'resistance']
      self.context['keys'] = keys
      return self.render()

    def dict_for_ces(self, ces):
      for obj in ces:
        time = obj.dtime.astimezone(tz=tz)
        li = 3
        for i in range(li):
          sstr = '0'+str(i+1)
          ss = 'sensordata_'+sstr
          s = getattr(obj, ss, None)
          if s:
            temp = s.temperature
            self.tempdict[i].append(temp)
            self.timedict[i].append(time)


    def graph(self):
      self.graph_form()

      if self.resolution:
        #logger.debug('resolution of graph: %s', self.resolution)
        revents = ControlEvent.objects.filter(dtime__minute__endswith=0, dtime__range=(self.start_date, self.now))
      else:
        revents = ControlEvent.objects.filter(dtime__range=(self.start_date, self.now))

      tz = timezone.get_current_timezone()
      li = 3             # number of graphs
      self.setup_graph(li)
      self.info = [s.name for s in SensorInfo.objects.order_by('id').all()]

      for obj in revents:
        time = obj.dtime.astimezone(tz=tz)
        for i in range(li):
          sstr = '0'+str(i+1)
          ss = 'sensordata_'+sstr
          s = getattr(obj, ss, None)
          if s:
            temp = s.temperature
            self.tempdict[i].append(temp)
            self.timedict[i].append(time)

      self.plotter(li)

      self.template_name = 'sensors/graph.html'
      return self.render()


    def list(self, sid):
        sensorinfo = SensorInfo.objects.get(pk=sid)
        self.context['sensorinfo'] = sensorinfo
        modelname = eval('SensorData_'+'0'+str(sid))
        self.init_ctrl()
        start_date = datetime.date(2021, 1, 1)
        end_date = datetime.date(2021, 1, 3)
        #object_list = eval('modelname.objects.filter(dtime__minute=0).order_by("-dtime")')
        object_list = SensorData_01.objects.filter(dtime__minute=0)
        object_list = object_list.filter(dtime__range=(start_date, end_date))
        object_list = object_list.order_by('-dtime')

#        object_list = SensorData_01.objects.filter(resistance__gt=6500).order_by("-dtime")
#        object_list = SensorData_01.objects.dates('dtime', 'day')
        self.lg.debug(len(object_list))

        table = SensorDataTable(object_list)
        self.context['table'] = table

        self.template_name = 'sensors/data.html'
        #self.context['object_list'] = object_list
        #self.context['data'] = object_list
        keys = ['dtime', 'temp', 'resistance']
        self.context['keys'] = keys
        return self.render()


def data(request, sid, action):
  ctrl = SensorDataView(request)
  return eval('ctrl.'+action+'('+str(sid)+')')

def data2(request, action):
    ctrl = SensorDataView(request)
    return eval('ctrl.'+action+'()')
