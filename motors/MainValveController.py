from django.shortcuts import render
from django.http import HttpResponseRedirect
from djflow.ViewController import ViewControllerSupport
from datetime import datetime
from motors.models import MainValveHistory
from motors.forms import MVControlForm
from django.utils.timezone import now

from piheatweb.util import *

def change2db(direction, amount, cur):
  from motors.models import Rule, RuleHistory
  from motors.models import DEFAULT_RULE
  # Save change to history table
  latest_degree = cur.result_openingdegree
  if direction == 'up':
    result_openingdegree = latest_degree + amount
  if direction == 'dn':
    result_openingdegree = latest_degree - amount

  #now = datetime.now()  # non tz aware!
  rule = Rule.objects.get(pk=DEFAULT_RULE)
  db_dir = {
    'dn': 'Close',
    'up': 'Open',
  }
  rule_event = RuleHistory(
    rule = rule,
    result = 1,
  )
  rule_event.save()

  entry = MainValveHistory(
      change_amount = amount,
      change_dir = db_dir[direction],
      result_openingdegree = result_openingdegree,
      rule_event = rule_event,
  )
  entry.save()


class MainValveController(ViewControllerSupport):
  def __init__(self, request):
    self.request = request
    self.init_ctrl()
    self.template_name = 'motors/mainvalvectrl.html'

  def control_input(self):
    request = self.request
    cur = MainValveHistory.objects.latest('id')

    if request.method == 'POST':
        form = MVControlForm(request.POST)
        if form.is_valid():
            POST = self.request.POST
            direction = POST['direction']
            amount = int(POST['amount'])

            if IS_RPi:
              from motors.MainValveCtrl import MainValveCtrl
              mvc = MainValveCtrl()
            if IS_PC:
              from motors.MainValveCtrlDummy import MainValveCtrlDummy
              mvc = MainValveCtrlDummy()

            ### Activate the controller hardware
            mvc.setup()
            mvc.work(direction, amount)

            change2db(direction, amount, cur)

            # redirect to a new URL:
            return HttpResponseRedirect('/actors/mainvalve')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MVControlForm()

    self.context['cur'] = cur
    self.context['form'] = form
    return render(self.request, self.template_name, self.context)
