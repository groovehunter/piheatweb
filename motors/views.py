from django.shortcuts import render
from django.template import RequestContext

from .models import Motor, Rule, RuleHistory
from .tables import MotorListTable

from django.views.generic import ListView, DetailView, CreateView
from piheatweb.ViewController import ViewControllerSupport


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
