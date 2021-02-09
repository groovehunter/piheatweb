
#import platform
#mach_str = platform.machine()
#if mach_str.startswith('arm'):
#  pass

import os
import sys


try:
    machine = os.uname().machine
except Exception:
    machine = os.name

IS_PC = machine.startswith('x86_64') or machine.startswith('nt')
IS_RPi = machine.startswith('armv')
IS_ESP8266 = machine.startswith('ESP8266')
IS_ESP32 = machine.startswith('ESP32')
IS_MICROPYTHON = (sys.implementation.name == 'micropython')


