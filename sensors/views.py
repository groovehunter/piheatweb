from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template

from django.views.generic import ListView, DetailView, CreateView
from .models import SensorData_01, SensorData_02, SensorData_03, SensorData_04
from .models import SensorInfo
from .tables import SensorDetailTable, SensorListTable, SensorDataTable
from piheatweb.ViewController import ViewControllerSupport
from piheatweb.Controller import Controller

import datetime

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
