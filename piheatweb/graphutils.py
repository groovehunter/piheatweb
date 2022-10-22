from plotly.offline import plot
#import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Figure, Bar
import plotly.express as px
from plotly.subplots import make_subplots

from piheatweb.forms import GraphAttributesForm
import datetime


class GraphMixin:

  def graph_form(self):
    sincehours = 3
    self.resolution = False
    if self.request.GET.get('go'):
      form = GraphAttributesForm(self.request.GET)
      if form.is_valid():
        sincehours = form.cleaned_data['sincehours']
        self.resolution = form.cleaned_data['resolution']
    else:
      form = GraphAttributesForm()
    self.start_date = self.now-datetime.timedelta(hours=int(sincehours))
    self.context['form'] = form

  def setup_graph(self, nl):
    self.tempdict = {}
    self.timedict = {}
    self.info = {}
    for i in range(nl):
      self.tempdict[i] = []
      self.timedict[i] = []
      self.info[i] = 'any'

  def pl2(self, nl):
    title_text = 'test'
    fig = make_subplots(
    rows=nl, cols=1, shared_xaxes=False,
    vertical_spacing=0.04)
    #nl = 3
    sc = {}
    for i in range(nl):
      sc[i] = Scatter(
        x=self.timedict[i], y=self.tempdict[i],
        mode='lines+markers',
        name=self.info[i],
        opacity=0.99,
      )
      fig.add_trace(sc[i], row=i+1, col=1)

    fig.update_layout(height=1200, width=1400,
        title_text=title_text)
    """
    fig['layout']['yaxis1'].update(domain=[0, 0.2])
    fig['layout']['yaxis2'].update(domain=[0.3, 0.7])
    fig['layout']['yaxis3'].update(domain=[0.8, 1])
    """
    plot(fig, filename='output.html')

  def create_scatter(self, timedict, tempdict, info):
    sc = Scatter(
      x=timedict, y=tempdict,
      mode='lines+markers',
      name=info,
      opacity=0.99,
      #marker_color=col[i],
      #marker=dict(size=[40, 60], color=[0, 1,])
    )
    return sc

  def plotter(self, nl):
    sc = {}
    col = {0:'green', 1:'blue', 2:'red', 3:'orange', 4:'black'}
    #fig = Figure()

    plotlist = []
    for i in range(nl):
      sc[i] = self.create_scatter(
          self.timedict[i],
          self.tempdict[i],
          self.info[i]
      )
      plotlist.append(sc[i])

    #fig.add_trace(sc[1])
    plt_div = plot(plotlist, output_type='div')
    self.context['plt_div'] = plt_div
