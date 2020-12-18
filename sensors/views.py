from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template

from django.views.generic import ListView, DetailView, CreateView
from .models import Sensor, Measurement
from .tables import SensorTable
from piheatweb.ViewController import ViewControllerSupport



class SensorListView(ListView, ViewControllerSupport):
    model = Sensor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = self.listview_helper()
        context.update(c)
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        self.fields_noshow = []
        self.init_ctrl()
        table = SensorTable(self.object_list)
        self.context['table'] = table
        self.template_name = 'index.html'
        self.context.update(self.get_context_data())
        return self.render()


class SensorDetailView(DetailView, ViewControllerSupport):
    model = Sensor

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


def last_measures(request, sensor_id):
    resp = "You're looking at sensor %s." % sensor_id
    m = Measurement.objects.filter(order_by(dtime))[:20]
    sensor = Sensor.m
    return HttpResponse(resp)
