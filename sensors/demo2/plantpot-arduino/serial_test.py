import serial
import time
from firebase import firebase
ser = serial.Serial('/dev/ttyACM0', 9600)

firebase = firebase.FirebaseApplication('https://solarbabesdb.firebaseio.com/bot/plant1')


while True:
        read_serial = ser.readline()
        cookedserial = read_serial.decode('utf-8')
        print cookedserial
        #print read_serial
        result = firebase.post('/moisture',{time.time():54})
