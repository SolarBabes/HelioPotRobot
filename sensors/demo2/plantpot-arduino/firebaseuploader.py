import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
TEMPERATURE_STRING = "temperature"
HUMIDITY_STRING = "humidity"
LIGHT_STRING = "light"
MOISTURE_STRING = "moisture"


def update(name, value):
    ref.child("realtime").update({name: value})
    ref.child(name).update({str(round(time.time())): value})


cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://solarbabesdb.firebaseio.com/'})

plantName = "plant2"  # TODO change here for robot name
ref = db.reference('bot/'+plantName)
update(HUMIDITY_STRING, 123)   # TODO change here for sensor name and value
