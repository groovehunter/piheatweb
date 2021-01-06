#!/usr/bin/python3
import sys
import os
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
    amount      = sys.argv[2]   
    speed = 50
    vt = MainValveCtrl()
    vt.setup()
    vt.speed = int(speed)
    vt.work(direction, amount)
    # Motor freigeben
    vt.release_motor()
    cur = MainValveHistory.objects.latest('dtime')

    change2db(amount, direction, cur)


