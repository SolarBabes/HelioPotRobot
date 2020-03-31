from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
from random import random
TEMPERATURE_STRING = "temperature"
HUMIDITY_STRING = "humidity"
MOISTURE_STRING = "moisture"
tdiff=0
# tdiff=1582731453-time.time()

def update(name, value):
    print(name + " " + str(value))
    ref.child("realtime").update({name: value})
    ref.child(name).update({str(round(time.time()+tdiff)): value})

def updateWithTime(name, value, time):
    print(name+" "+str(value)+" "+str(time))
    ref.child("realtime").update({name: value})
    ref.child(name).update({str(time): value})

def uploadRandomFor2Days():
    last_temp = 15
    last_hum = 30
    last_moi = 30
    j = round(time.time())

    i = 0
    while i < 172800:
        t = j - i
        print(t)
        i = i + 600
        last_temp = last_temp + round(random() * 10 - 5)
        last_hum = last_hum + round(random() * 20 - 10)
        last_moi = last_moi + round(random() * 50 - 25)
        if last_temp < 0:
            last_temp = 1
        if last_temp > 30:
            last_temp = 28
        if last_hum < 0:
            last_hum = 3
        if last_hum > 95:
            last_hum = 90
        if last_moi < 0:
            last_moi = 3
        if last_moi > 800:
            last_moi = 760
        updateWithTime(TEMPERATURE_STRING, last_temp, t)
        updateWithTime(HUMIDITY_STRING, last_hum, t)
        updateWithTime(MOISTURE_STRING, last_moi, t)
        updateWithTime('light', last_moi, t)

def uploadEvery5Seconds(s):
    last_temp = 15
    last_hum = 30
    last_moi = 30
    last_light = 100

    for i in range(s):
        last_temp = last_temp + round(random() * 5 - 2.5)
        last_hum = last_hum + round(random() * 20 - 10)
        last_moi = last_moi + round(random() * 80 - 40)
        last_light = last_light + round(random() * 100 - 50)
        if last_temp < 0:
            last_temp = 1
        if last_temp > 30:
            last_temp = 28

        if last_hum < 0:
            last_hum = 3
        if last_hum > 95:
            last_hum = 90

        if last_moi < 0:
            last_moi = 3
        if last_moi > 800:
            last_moi = 760

        if last_light < 0:
            last_light = 5
        if last_light > 800:
            last_light = 760
        update(TEMPERATURE_STRING, last_temp)
        update(HUMIDITY_STRING, last_hum)
        update(MOISTURE_STRING, last_moi)
        update("light", last_light)
        time.sleep(2)


cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://solarbabesdb.firebaseio.com/'})
plantName = "0002"
ref = db.reference('heliopots/'+plantName+'/data')
#
# update(HUMIDITY_STRING, 12)
# uploadEvery5Seconds(100000000)
uploadRandomFor2Days()
