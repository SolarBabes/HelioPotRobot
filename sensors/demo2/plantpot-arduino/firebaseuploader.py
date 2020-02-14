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

#ser = serial.Serial('/dev/ttyACM0', 9600) #uncomment for raspberry pi
ser = serial.Serial('/dev/cu.usbmodem14201', 9600) #just for azam's laptop

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://solarbabesdb.firebaseio.com/'})

plantName = "plant2"  # TODO change here for robot name
ref = db.reference('bot/'+plantName)


def sensor_reading():
    while True:
           read_serial = ser.readline()
           cookedserial = read_serial.decode('utf-8').strip("\r\n ' '")
           datasplit = cookedserial.split(",")
           temperature = float(datasplit[0].strip('<'))
           humidity = float(datasplit[1])
           moisture = int(datasplit[2].strip('>'))
           update(TEMPERATURE_STRING, temperature)
           update(HUMIDITY_STRING, humidity)
           update(MOISTURE_STRING, moisture)
           print(temperature)
           print(humidity)
           print(moisture)



def update(name, value):
        ref.child("realtime").update({name: value})
        ref.child(name).update({str(round(time.time())): value})


sensor_reading()
#update(MOISTURE_STRING)   # TODO change here for sensor name and value
