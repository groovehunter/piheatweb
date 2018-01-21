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
from datetime import datetime
import threading


HOME='/home/pi/piheat/piheatweb/'

class App:

    def __init__(self):
        self.reader = Reader()
        self.engine = Engine()
        self.load_conf()


    def load_conf(self):
        """ load cfg file and set reader+engine cfg """
        # XXX replace HOME with cwd
        fn = HOME + 'conf.yml'
        self.cfg = yaml.load(open(fn,'r'))
        self.reader.cfg = self.cfg

        #cfg = self.cfg

    def start(self):
        self.reader.readall()
        self.check_constraints()


    def check_constraints(self):
        """ check if all obey the rule """
        threading.Timer(20.0, self.check_constraints).start()
        now = datetime.now()
        print("checking constraints...", now)
        #sens = self.from_db()
        # kessel temp - warmwater between 35 and 55
        self.regulate_ww()


    def set_mode(self, mode):
        self.mode = mode


    def from_db(self):
        sens = self.reader.from_db()


    def regulate_ww(self):
        """ regulate warmwater templ """
        temp = self.reader.current[2]
        self.set_mode('ww')
        threshhold_max = self.cfg['threshhold_max']
        threshhold_min = self.cfg['threshhold_min']
        state = self.engine.get_state('ww')
        map_activity = {0:'active', 1:'DEACTIVE'}
        print(temp, map_activity[state])

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
app.start()
#app.loop()

