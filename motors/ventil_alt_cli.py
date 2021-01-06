#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sys



class Ventiltrieb(object):

    def __init__(self):
        self.fn = 'ventilstand.txt'
        self.count = 10000

    def save(self):
        with open('ventilstand.txt', 'w') as f:
            f.save(self.count)

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


    def work(self, direction, amount):
        DIR_Left = GPIO.HIGH
        DIR_Right = GPIO.LOW
        PUL = self.pins['PUL']
        DIR = self.pins['DIR']
        steps = int(amount)*100

        if direction=='up':
            print('waermer')
            GPIO.output(DIR, DIR_Right)
            self.count += steps
        if direction == 'dn':
            print('kaelter')
            GPIO.output(DIR, DIR_Left)
            self.count -= steps
        
        sl = 0.01 / self.speed 
        print('speed: ', self.speed)
        print('sl', sl)


        for i in range(steps):
            GPIO.output(PUL, GPIO.HIGH)
            time.sleep(sl)
            GPIO.output(PUL, GPIO.LOW)
            time.sleep(sl)
            #print('.')



if __name__=='__main__':
    print(sys.argv)
    direction   = sys.argv[1]
    amount      = sys.argv[2]   
    #speed       = sys.argv[3]
    speed = 50
    print('Amount of: ', amount)
    vt = Ventiltrieb()
    vt.setup()
    vt.speed = int(speed)
    vt.work(direction, amount)
    # Motor freigeben
    ENA_Released = GPIO.HIGH
    GPIO.output(vt.pins['ENA'], ENA_Released)
    print('vt count', vt.count)

