#!/usr/bin/python
import RPi.GPIO as GPIO
import time, os
import logging
logger = logging.getLogger(__name__)
from django.conf import settings
from datetime import datetime

class MainValveCtrl(object):

    def __init__(self):
        self.count = 0
        self.speed = 100
        self.openingdegree_minimum = 3000
        self.openingdegree_maximum = 32000
        self.lock_fn = settings.BASE_DIR+'/valve.lock'

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        # Raspberry Pi Pin-Belegung fuer TB6600 Treiber
        self.pins = {}
        self.pins['DIR'] = 20
        self.pins['PUL'] = 21
        self.pins['ENA'] = 16
        GPIO.setwarnings(False)
        for name, pin in self.pins.items():
            GPIO.setup(pin, GPIO.OUT)

        ENA_Locked = GPIO.LOW
        ENA_Released = GPIO.HIGH

        # Motor aktivieren und halten
        GPIO.output(self.pins['ENA'], ENA_Locked)


    def is_running(self):
        if os.path.exists(self.lock_fn):
          return True
        return False

    def remove_lock(self):
        os.remove(self.lock_fn)
        logger.debug('CLEARED valve LOCK file: %s', self.lock_fn)

    def set_lock(self):
        logger.debug('Write valve LOCK file: %s', self.lock_fn)
        f = open(self.lock_fn, 'w')
        f.write(datetime.now().isoformat())
        f.close()

    def work(self, direction, amount):
        if not direction in ('dn', 'up'):
          print("wrong direction: use dn/up")
          return False
        if self.is_running():
          logger.error('Valve Engine already running')
          print('LOCKFILE exists - is still running - NOT DONE')
          return False

        self.set_lock()

        DIR_Left = GPIO.HIGH
        DIR_Right = GPIO.LOW
        PUL = self.pins['PUL']
        DIR = self.pins['DIR']
        steps = int(amount)*100

        if direction == 'up':
            #logger.debug('direction up: warmer')
            GPIO.output(DIR, DIR_Right)
            self.count += steps
        if direction == 'dn':
            #logger.debug('direction dn: colder')
            GPIO.output(DIR, DIR_Left)
            self.count -= steps

        sl = 0.01 / self.speed


        for i in range(steps):
            GPIO.output(PUL, GPIO.HIGH)
            time.sleep(sl)
            GPIO.output(PUL, GPIO.LOW)
            time.sleep(sl)

        time.sleep(0.5)
        self.release_motor()
        self.remove_lock()

        return True   # Success

    def release_motor(self):
        ENA_Released = GPIO.HIGH
        GPIO.output(self.pins['ENA'], ENA_Released)

