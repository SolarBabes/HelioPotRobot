import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import serial
from serial import Serial
LIGHT_0_PIN = "lightN"
LIGHT_1_PIN = "lightS"
LIGHT_2_PIN = "lightE"
LIGHT_3_PIN = "lightW"

ser = serial.Serial('/dev/ttyACM0', 9600) 
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://solarbabesdb.firebaseio.com/'})

plantName = "plant2"  # TODO change here for robot name
ref = db.reference('bot/'+plantName)


def sensor_reading():
    while True:
           read_serial = ser.readline()
           cookedserial = read_serial.decode('utf-8').strip("\r\n ' '")
           datasplit = cookedserial.split(",")
           lightN = float(datasplit[0].strip('<'))
           lightS = float(datasplit[1])
           lightE = int(datasplit[2])
           lightW = int(datasplit[3].strip('>'))
           update(LIGHT_0_PIN, lightN)
           update(LIGHT_1_PIN, lightS)
           update(LIGHT_2_PIN, lightE)
           update(LIGHT_3_PIN, lightW)
           print(lightN)
           print(lightS)
           print(lightE)
           print(lightW)


def update(name, value):
        ref.child("realtime").update({name: value})
        ref.child(name).update({str(round(time.time())): value})


sensor_reading()