from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from piheatweb.ViewController import ViewControllerSupport

class DashboardView(DetailView, ViewControllerSupport):

    def get(self, request, *args, **kwargs):
        self.fields_noshow = []
        self.init_ctrl()
        self.template_name = 'home.html'
        return self.render()



def index(request):

    #t = get_template('base.html')
    return render(request, 'index.html')
