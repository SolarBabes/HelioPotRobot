import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import serial
from serial import Serial
TEMPERATURE_STRING = "temperature"
HUMIDITY_STRING = "humidity"
LIGHT_STRING = "light"
MOISTURE_STRING = "moisture"

ser = serial.Serial('/dev/ttyACM0', 9600)



def update(name):
     while True:
            read_serial = ser.readline()
            cookedserial = read_serial.decode('utf-8')
            print (cookedserial)
            #return cookedserial
            ref.child("realtime").update({name: cookedserial})
            ref.child(name).update({str(round(time.time())): cookedserial})


cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://solarbabesdb.firebaseio.com/'})

plantName = "plant2"  # TODO change here for robot name
ref = db.reference('bot/'+plantName)
update(MOISTURE_STRING)   # TODO change here for sensor name and value
