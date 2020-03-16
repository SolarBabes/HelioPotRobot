# on turtlebot
# pip install requests
# pip install geocoder
# pip install apscheduler

import requests
from datetime import datetime
import geocoder

from apscheduler.schedulers.background import BackgroundScheduler

global goToBase

sched = BackgroundScheduler()

@sched.scheduled_job('interval', minutes=60)
def getWeather():
    
    global goToBase
    # get location
    g = geocoder.ip('me')

    # request weather data
    api_address='http://api.openweathermap.org/data/2.5/weather?appid=e1e1259dbe6f94daad7d1321fc262688'
    cityRequest = '&q={}'.format(g.city)
    url = api_address + cityRequest + '&units=metric'
    json_data = requests.get(url).json()

    # get main weather description and temperature
    weatherID = json_data['weather'][0].get('id')

    # weather id
    # if id = 7xx (mist, smoke, fog etc)
    if int(str(weatherID)[:1]) == 7:
        atmosphere = True

    # cloud percentage
    cloud = json_data['clouds'].get('all')
    if cloud > 90:
        cloudy = True

    # get sunrise and sunset times
    sunriseUnix = json_data['sys'].get('sunrise')
    sunrise = datetime.utcfromtimestamp(sunriseUnix)
    sunsetUnix = json_data['sys'].get('sunset')
    sunset = datetime.utcfromtimestamp(sunsetUnix)

    # if current time < sunrise || > sunset, go to base station
    now = datetime.now()
    if now < sunrise or now > sunset:
        sunHasSet = True

    if not sunHasSet and not cloudy and not atmosphere:
        goToBase = False
    else:
        goToBase = True

sched.start()

# use sched.shutdown() to stop
