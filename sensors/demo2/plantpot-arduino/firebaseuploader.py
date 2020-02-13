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

#ser = serial.Serial('/dev/ttyACM0', 9600)
ser = serial.Serial('/dev/cu.usbmodem14201', 9600)




def update(name):
     while True:
            read_serial = ser.readline()
            
            cookedserial = read_serial.decode('utf-8').strip("\r\n ' '")            

            #print (cookedserial)

            #cookedserial = int(''.join([i for i in ite(1, cookedserial) if i in "123456890"]))

            datasplit = cookedserial.split(",")
            temperature = datasplit[0].strip('<')
            humidity = datasplit[1]
            moisture = datasplit[2].strip('>')
            print(temperature)
            print(humidity)
            print(moisture)
            
            ref.child("realtime").update({name: cookedserial})
            ref.child(name).update({str(round(time.time())): cookedserial})


cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://solarbabesdb.firebaseio.com/'})

plantName = "plant2"  # TODO change here for robot name
ref = db.reference('bot/'+plantName)
update(MOISTURE_STRING)   # TODO change here for sensor name and value
#update(TEMPERATURE_STRING)
#update(HUMIDITY_STRING)