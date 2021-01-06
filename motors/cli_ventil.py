#!/usr/bin/python
import sys
from MainValveCtrl import MainValveCtrl



if __name__=='__main__':
    print(sys.argv)
    direction   = sys.argv[1]
    amount      = sys.argv[2]   
    #speed       = sys.argv[3]
    speed = 50
    print('Amount of: ', amount)
    vt = MainValveCtrl()
    vt.setup()
    vt.speed = int(speed)
    vt.work(direction, amount)
    # Motor freigeben
    vt.release_motor()

