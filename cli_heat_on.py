#!/usr/bin/python3
import os
import django
import sys
os.environ["DJANGO_SETTINGS_MODULE"] = 'piheatweb.settings'
django.setup()


from motors.HeatPump import HeatPumpCtrl
from motors.models import Mode


def switch(status):
  ctrl = HeatPumpCtrl()
  ctrl.setup()
  print( ctrl.get_status() )
  mode_w = Mode.objects.filter(name='WarmwaterOnly').first()
  mode_h = Mode.objects.filter(name='HeatingMode').first()
  print('mode h / w ', mode_h.active, mode_w.active)

  if status == 'ON':
    if ctrl.get_status() == 'OFF':
      ctrl.enable()
      print('heat pump enabled')
    print('HeatingMode ?')
    if not mode_h.active:
      mode_h.active = True
      mode_w.active = False
      mode_h.save()
      mode_w.save()

  if status == 'OFF':
    if ctrl.get_status() == 'ON':
      ctrl.disable()
      print('heat pump disabled')

    print('WalmwaterOnly ?')
    if not mode_w.active:
      mode_w.active = True
      mode_h.active = False
      mode_h.save()
      mode_w.save()

  print('mode h / w ', mode_h.active, mode_w.active)

if __name__ == '__main__':
  status = sys.argv[1]
  switch(status)

