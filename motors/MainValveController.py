from piheatweb.Controller import Controller
from datetime import datetime
from motors.models import Rule


def change2db(direction, amount, cur):
  # Save change to history table
  latest_degree = cur.result_openingdegree
  if direction == 'Open':
    result_openingdegree = latest_degree + amount
  if direction == 'Close':
    result_openingdegree = latest_degree - amount

  now = datetime.now()
  rule = Rule.objects.get(pk=DEFAULT_RULE)
  entry = MainValveHistory(
      dtime = now,
      change_amount = amount,
      change_dir = direction,
      result_openingdegree = result_openingdegree,
      rule = rule
  )
  entry.save()


class MainValveController(Controller):
  def __init__(self, request):
    Controller.__init__(self, request)
    self.template = 'motors/mainvalvectrl.html'

  def control_input(self):
    request = self.request
    cur = MainValveHistory.objects.latest('dtime')

    if request.method == 'POST':
        form = MVControlForm(request.POST)
        if form.is_valid():
            POST = self.request.POST
            direction = POST['direction']
            amount = int(POST['amount'])

            from platform import machine
            if machine() == 'armv7l':
              from motors.MainValveCtrl import MainValveCtrl
              mvc = MainValveCtrl()
            else:
              from motors.models import DEFAULT_RULE
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
    return render(self.request, self.template, self.context)

