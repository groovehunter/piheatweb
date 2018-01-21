#from conf import *

# Broadcom GPIO references
from Engine import Engine

e = Engine()
s1 = e.get_state('ww')
s2 = e.get_state('heat')

print(s1, s2)
e.activate_pump('ww')
#e.activate_pump('heat')


