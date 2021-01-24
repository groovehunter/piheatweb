from django.shortcuts import render
from django.http import HttpResponseRedirect
from piheatweb.Controller import Controller
from datetime import datetime
from motors.models import WarmwaterPumpHistory
from motors.forms import MotorControlGenericForm
from django.utils.timezone import now


def change2db(status, cur):
  from motors.models import Rule
  from motors.models import DEFAULT_RULE
  # Save change to history table

  rule = Rule.objects.get(pk=DEFAULT_RULE)
  entry = WarmwaterPumpHistory(
      dtime = now(),
      change_status = status,
      rule = rule
  )
  entry.save()


class WarmwaterPumpController(Controller):
  def __init__(self, request):
    Controller.__init__(self, request)
    self.template = 'motors/warmwaterctrl.html'

  def control_input(self):
    request = self.request
    cur = WarmwaterPumpHistory.objects.latest('dtime')

    if request.method == 'POST':
        form = MotorControlGenericForm(request.POST)
        if form.is_valid():
            POST = self.request.POST
            status = POST['status']

            from platform import machine
            if machine() == 'armv7l':
              from motors.WarmwaterPump import WarmwaterPumpCtrl
              ctrl = WarmwaterPumpCtrl()
            else:
              from motors.WarmwaterPumpDummy import WarmwaterPumpCtrlDummy
              ctrl = WarmwaterPumpCtrlDummy()

            ### Activate the controller hardware
            ctrl.setup()
            ctrl.work(status)

            change2db(status, cur)

            # redirect to a new URL:
            return HttpResponseRedirect('/actors/ww')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MotorControlGenericForm()

    self.context['cur'] = cur
    self.context['form'] = form
    return render(self.request, self.template, self.context)
