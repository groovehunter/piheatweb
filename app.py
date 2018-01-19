#!/usr/bin/python3

import yaml
import sys
import os
cwd = os.getcwd()
sys.path.append(cwd+'/input')
sys.path.append(cwd+'/output')

from Reader import Reader
from Engine import Engine
import time


HOME='/home/pi/piheat/piheatweb/'

class App:

    def __init__(self):
        self.reader = Reader()
        self.engine = Engine()
        self.load_conf()


    def load_conf(self):
        fn = HOME + 'conf.yml'
        self.cfg = yaml.load(open(fn,'r'))
        self.reader.cfg = self.cfg

        #cfg = self.cfg
        

    def set_mode(self, mode):
        self.mode = mode


    def regulate_ww(self):
        self.set_mode('ww')
        threshhold_max = self.cfg['threshhold_max']
        threshhold_min = self.cfg['threshhold_min']
        temp = self.reader.get_approx(3)
        print(temp)
        state = self.engine.get_state('ww')
        map_activity = {0:'active', 1:'DEACTIVE'}
        print(map_activity[state])

        if temp > threshhold_max:
            print('temp in kessel >> threshold')
            if state == 0:
                self.engine.deactivate_pump('ww')
                print('deactivate pump ww')
            else:
                print('pump already deactivated')

        elif temp < threshhold_min:
            print('temp in kessel << threshold min')
            if state == 1:
                self.engine.activate_pump('ww')
                print('enable pump ww')
            else:
                print('pump already enabled')

        else:
            print('temp okay', temp)


    def loop(self):
        #self.engine.cleanup()
        while True:
            time.sleep(5)
            self.regulate_ww()
            print()


app = App()
#app.regulate_ww()
app.loop()


