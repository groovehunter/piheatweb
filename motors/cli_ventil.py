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
    if amount > 1000:
      input("So MUCH, are you sure?")
    speed = 50
    vt = MainValveCtrl()
    vt.setup()
    vt.speed = 50
    ### WORK
    vt.work(direction, amount)

    # Motor freigeben
    vt.release_motor()
    cur = MainValveHistory.objects.latest('id')

    change2db(direction, amount, cur)


