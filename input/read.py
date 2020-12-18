import serial, time

port = '/dev/ttyACM0'
arduino = serial.Serial(port, 9600, timeout=.1)
time.sleep(1) #give the connection a second to settle
num = 2000

result = {}
ser = arduino

for i in range(0, num):
    #result[i] = ser.readline()
    ser_bytes = ser.readline()
    result[i] = ser_bytes
    time.sleep(0.5)
    print(result[i])

for i in range(0, num):
    print(result[i])

#print(result)
arduino.close()

