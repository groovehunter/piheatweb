#!/usr/bin/python3
import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), '..'))

import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'piheatweb.settings'
django.setup()

from motors.models import MainValveHistory
from MainValveCtrl import MainValveCtrl

from MainValveController import change2db
  

if __name__=='__main__':
    print(sys.argv)
    direction   = sys.argv[1]
    amount      = int(sys.argv[2])   
    speed = 50.0
    if len(sys.argv) > 3:
      speed = int(sys.argv[3])
    if amount > 1000:
      input("So MUCH, are you sure?")
    vt = MainValveCtrl()
    vt.setup()
    vt.speed = speed
    ### WORK
    success = vt.work(direction, amount)

    if not success:
      print("ERROR occurred, valve work not done")
      sys.exit()
    cur = MainValveHistory.objects.latest('id')

    change2db(direction, amount, cur)


