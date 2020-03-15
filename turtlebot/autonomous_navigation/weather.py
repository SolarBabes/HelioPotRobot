# on turtlebot
# pip install requests
# pip install geocoder
# pip install apscheduler

import requests
from datetime import datetime
import geocoder

from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()

@sched.scheduled_job('interval', minutes=10)
def getWeather():
    goToBase = False

    # get location
    g = geocoder.ip('me')
    lat = g.latlng[0]
    lng = g.latlng[1]

    # request weather data
    api_address='http://api.openweathermap.org/data/2.5/weather?appid=e1e1259dbe6f94daad7d1321fc262688'
    # can use lat and lon or city
    latlngRequest = '&lat={}&lon={}'.format(lat, lng)
    cityRequest = '&q={}'.format(g.city)
    url = api_address + cityRequest + '&units=metric'
    json_data = requests.get(url).json()

    # get main weather description and temperature
    weatherID = json_data['weather'][0].get('id')
    weather = json_data['weather'][0].get('main')
    moreDescriptive = json_data['weather'][0].get('description')
    temp = json_data['main'].get('temp')

    # weather id
    # if id = 7xx (mist, smoke, fog etc)
    if int(str(weatherID)[:1]) == 7:
        print('{}, remain at base station?'.format(weather))
        goToBase = True

    # cloud percentage
    cloudy = json_data['clouds'].get('all')
    if cloudy > 90:
        print('Too cloudy, remain at base station?')
        goToBase = True

    # get sunrise and sunset times
    sunriseUnix = json_data['sys'].get('sunrise')
    sunrise = datetime.utcfromtimestamp(sunriseUnix)
    sunsetUnix = json_data['sys'].get('sunset')
    sunset = datetime.utcfromtimestamp(sunsetUnix)

    # if current time < sunrise || > sunset, go to base station
    now = datetime.now()
    if now < sunrise or now > sunset:
        print('Sun is currently set, remain at base station?')
        goToBase = True
    # output to test it's working
    #print('The weather today is {} with a temperature of: {}'.format(moreDescriptive, str(temp)))
    #print('Sunrise is at {} and sunset is at {}'.format(sunrise.strftime('%H:%M:%S'), sunset.strftime('%H:%M:%S')))

    # use movement teams go to goal method if goToBase = True

sched.start()

# use sched.shutdown() to stop

### available data ###
# {"coord":{"lon":-3.2,"lat":55.95},
# "weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}],
# "base": "stations",
# "main":{
# "temp":280.35,"feels_like":275.29,"temp_min":278.71,"temp_max":282.04,
# "pressure":1004,"humidity":75},
# "visibility":10000,
# "wind":{"speed":5.1,"deg":220},
# "clouds":{"all":21},
# "dt":1583500823,
# "sys":{"type":1,"id":1442,"country":"GB",
# "sunrise":1583477447,"sunset":1583517449},
# "timezone":0,"id":2650225,"name":"Edinburgh","cod":200}

### list of possible weather descriptions ###
# https://openweathermap.org/weather-conditions 
