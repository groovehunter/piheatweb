from django.db.models.query import prefetch_related_objects

from piheatweb.ViewController import ViewControllerSupport
from piheatweb.Controller import Controller
from piheatweb.forms import GraphAttributesForm

from motors.models import Rule, RuleHistory, RuleResultData_01, RuleResultData_02
from cntrl.models import ControlEvent

from datetime import datetime, timedelta
from django.utils import timezone
from random import randint
import logging
logger = logging.getLogger(__name__)

from plotly.offline import plot
#import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Figure
import plotly.express as px


class CntrlController(Controller):
    def __init__(self, request):
      Controller.__init__(self, request)
      self.now = timezone.now()

    def graph(self):
      GET = self.request.GET
      sincehours = int(GET.get('sincehours', default=3))
      resolution = int(GET.get('resolution', default=False))
      start_date = self.now - timedelta(hours=sincehours)

      logger.debug('graph start date: %s', start_date)
      myrule = Rule.objects.get(name='CalcVorlaufSollRule')
      ### query all CE, I guess those without corresponding RH
      # we need to skip later
      if resolution:
        ce = ControlEvent.objects.filter(dtime_minute__endswith=0, dtime__range=(start_date, self.now)).order_by('dtime')
      else:
        ce = ControlEvent.objects.filter(dtime__range=(start_date, self.now)).order_by('dtime')
      logger.debug('CE len: %s', len(ce))
      # init graph data dict
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
        #logger.debug('=== NEXT: %s', time)
        rhs = obj.rulehistory_set
        skipped = 0
        if rhs.count() == 0:
          skipped += 1
          continue

        for i in range(l):
          timedict[i].append(time)

          val = randint(1,20)
          tempdict[1].append(val)

      logger.debug('Rhs count==0 so skipped  %s events', skipped)

      N = 1000
      t = np.linspace(0, 10, 100)
      y = {}
      y[0] = np.sin(t)
      y[1] = np.cos(t)

      sc = {}
      col = {0:'green', 1:'blue', 2:'red', 3:'orange'}
      info = {
        0: 'RRD1 / CalcSoll', 
        1: 'RRD2 / ANY', 
      }


      for i in range(l):
        sc[i] = Scatter(
                    x=t, y=y[i],
                    #x=timedict[i], y=tempdict[i],
                    mode='markers', 
                    name=info[i],
                    opacity=0.8, 
                    marker_color=col[i],
                    marker_size=20,
        )

      plt_div = plot([sc[0], sc[1]], output_type='div')
      self.context['plt_div'] = plt_div

      form = GraphAttributesForm()
      self.context['form'] = form
      self.template = 'motors/graph.html'
      return self.render()

    def home(self):
      self.template = 'motors/graph.html'
      return self.render()



def action(request, method):
  ctrl = CntrlController(request)
  return eval('ctrl.'+method+'()')

def home(request):
  ctrl = CntrlController(request)
  return ctrl.home()



