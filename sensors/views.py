from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import ListView, DetailView, CreateView
from django.utils import timezone

from .models import SensorData_01, SensorData_02, \
SensorData_03, SensorData_04
from .models import SensorInfo, ReadingEvent
from .tables import SensorDetailTable, SensorListTable, \
SensorDataTable, AllSensorTable
from piheatweb.ViewController import ViewControllerSupport
from piheatweb.Controller import Controller
from piheatweb.forms import GraphAttributesForm

import datetime
from plotly.offline import plot
#import plotly.graph_objs as go
from plotly.graph_objs import Scatter
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


class SensorDataView(Controller):
    """ data of sensor 01 only """

    # generalize later
    def __init__(self, request):
        Controller.__init__(self, request)
        self.now = timezone.now()

    def all_sensors(self, *args):
      """ all sensors temp next to each other
          parameter daterange
      """
#      SensorData_01.obj
      start_date = datetime.date(2021, 1, 2)
      end_date = datetime.date(2021, 1, 5)
      revents = ReadingEvent.objects.filter(dtime__minute=0).order_by('-id')  #, dtime__range=(start_date, end_date))
      object_list = []
      #self.lg.debug(len(revents))
      line = []
      for obj in revents:
        d = {
          'dtime':obj.dtime,
          'sid01':obj.sid01.temperature,
          'sid02':obj.sid02.temperature,
          'sid03':obj.sid03.temperature,
          'sid04':obj.sid04.temperature,
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

    def graph(self):
      sincehours = 3
      resolution = False
      if self.request.GET.get('go'):
        form = GraphAttributesForm(self.request.GET)
        if form.is_valid():
          sincehours = form.cleaned_data['sincehours']
          resolution = form.cleaned_data['resolution']
      else:
        form = GraphAttributesForm()

      start_date = self.now - datetime.timedelta(hours=int(sincehours))
      if resolution:
        logger.debug('resolution of graph: %s', resolution)
        revents = ReadingEvent.objects.filter(dtime__minute__endswith=0, dtime__range=(start_date, self.now))
        #revents = ReadingEvent.objects.filter(dtime__minute=0, dtime__range=(start_date, self.now))
      else:
        revents = ReadingEvent.objects.filter(dtime__range=(start_date, self.now))

      sinfo = SensorInfo.objects.order_by('id').all()
 #     self.lg.debug(len(revents))
      tempdict = {}
      timedict = {}
      c=0
      tz = timezone.get_current_timezone()
      li = 3              # number of graphs
      for i in range(li):
        tempdict[i] = []
        timedict[i] = []
      for obj in revents:
        time = obj.dtime.astimezone(tz=tz)
        for i in range(li):
          sstr = '0'+str(i+1)
          temp = eval('obj.sid'+sstr+'.temperature')
          tempdict[i].append(temp)
          timedict[i].append(time) #obj.dtime)
        #c+=1
      sc = {}
      col = {0:'red', 1:'blue', 2:'green', 3:'orange'}

      sc_list = []
      for i in range(li):
        sc[i] = Scatter(x=timedict[i], y=tempdict[i], \
                        mode='lines', name=sinfo[i].name, \
                        opacity=0.8, marker_color=col[i])
#        sc[i].update_yaxes(range=[40, 80])
        sc_list.append(sc[i])
      plt_div = plot(sc_list, output_type='div')

      self.context['plt_div'] = plt_div
      self.context['form'] = form
      self.template = 'sensors/graph.html'
      #self.somedata()
      return self.render()


    def daterange(self):
      start_date = datetime.date(2021, 1, 1)
      end_date = datetime.date(2021, 1, 2)
      return SensorData_01.objects.filter(dtime__range=(start_date, end_date))

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
        #object_list = self.daterange()

        table = SensorDataTable(object_list)
        self.context['table'] = table

        self.template = 'sensors/data.html'
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
