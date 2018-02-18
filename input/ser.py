#!/usr/bin/python3

import serial
import json

from AnalogReader import AnalogReader


ser = serial.Serial(
    port='/dev/ttyACM0',
    #baudrate = 115200,
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


reader = AnalogReader()
# first received line is probably incomplete, throw away
res = ser.read_until()

while 1:
    res = ser.read_until()
    r = res.decode('utf-8').strip()
    #print(len(r))
    if len(r) < 2:
        continue
    j = json.loads(r)
    data = j['data']
    reader.store(data)

