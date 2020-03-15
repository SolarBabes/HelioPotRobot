import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://solarbabesdb.firebaseio.com/'})

plantName = "0001"
ref = db.reference('heliopots/'+plantName)
ref.update({"message": "here is a sample message"})
