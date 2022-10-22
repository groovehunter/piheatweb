#from django.db.models.query import prefetch_related_objects

from piheatweb.ViewController import ViewControllerSupport
#from piheatweb.forms import GraphAttributesForm

#from cntrl.models import ControlEvent

#from datetime import datetime, timedelta
from django.utils import timezone
#from random import randint
import logging
logger = logging.getLogger(__name__)
from piheatweb.graphutils import GraphMixin
from motors.models import RuleHistory
from django.db.models import OuterRef, Exists
from .models import ControlEvent
"""
from plotly.offline import plot
#import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Figure
import plotly.express as px
"""



class CntrlController(ViewControllerSupport, GraphMixin):
  def __init__(self, request):
    self.request = request
    self.now = timezone.now()
    self.init_ctrl()

  def home(self):
    self.template_name = 'motors/graph.html'
    return self.render()

  # combo plot. for sensors, actors
  # Needs same timedict for all Scatters
  # so use only ControlEvents which have rule_event associated
  def combined_graph(self):
    self.graph_form()
    ces = self.get_latest_ce_of_rh(self.start_date)
    nl = 5 # 3xsensor, 2xactor
    self.setup_graph(nl)
    # populate all timedicts at once
    for obj in ces:
      for i in range(nl):
        self.timedict[i].append(obj.dtime)

    # collect all values for ces
    self.dict_for_ces(ces, [0,1,2])
    self.motor_dict_for_ces(ces, [3,4])
    # call GraphMixin.pl2()
    self.pl2(4)
    self.template_name = 'motors/graph.html'
    return self.render()

  def get_latest_ce_of_rh(self, start_date):
    rh = RuleHistory.objects.filter(ctrl_event=OuterRef('id'))
    ces = ControlEvent.objects.filter(Exists(rh), dtime__range=(start_date, self.now)).order_by('-dtime')
    return ces

  def dict_for_ces(self, ces, li_list):
    for obj in ces:
      #time = obj.dtime.astimezone(tz=tz)
      #li = 3
      for i in li_list:
        sstr = '0'+str(i+1)
        ss = 'sensordata_'+sstr
        s = getattr(obj, ss, None)
        if s:
          temp = s.temperature
          self.tempdict[i].append(temp)
          #self.timedict[i].append(time)

  def motor_dict_for_ces(self, ces, li_list):
    for obj in ces:
      rh = obj.rulehistory_set.first()
      if hasattr(rh, 'warmwaterpumphistory_set'):
        val = rh.warmwaterpumphistory_set.first()
        if val:
          self.tempdict[li_list[0]].append(val.change_status)
      if hasattr(rh, 'mainvalvehistory_set'):
        val = rh.mainvalvehistory_set.first()
        if val:
          self.tempdict[li_list[1]].append(val.result_openingdegree)



def action(request, method):
  ctrl = CntrlController(request)
  return eval('ctrl.'+method+'()')

def home(request):
  ctrl = CntrlController(request)
  return ctrl.home()

def combined_graph(request):
  ctrl = CntrlController(request)
  return ctrl.combined_graph()
