import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)




while True:
        read_serial = ser.readline()
        cookedserial = read_serial.decode('utf-8')
        print (cookedserial)
