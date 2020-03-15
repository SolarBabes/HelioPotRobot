from firebase import firebase
from datetime import datetime, date

# Get current time
currentDate = date.today()

print(currentDate)

# Create link to our database
dataBase = firebase.FirebaseApplication('https://solarbabesdb.firebaseio.com/', None)

# Get all data stored as a dictionary (Ignore this error it still works)
dictMain = dataBase.get('/heliopots/', None)

# Collect all potIDs
potIDS = []

# Collect all readingtypes for 
readingTypes = []

# Populate all the pot IDS 
def getPotIDS():
    potIDS.clear()
    for key in dictMain:
        potIDS.append(key)

# Populate all the types of reading for a pot with id = 'potID'
def getReadingTypes(potID):
    readingTypes.clear()
    for key in dictMain[potID]['data']:
        readingTypes.append(key)

# Get a certain type of data
# Returns a dictionary
def getData(potID, readingType):
    getPotIDS()
    getReadingTypes(potID)

    # Make sure we are searching for data with valid potID and readingType
    if (potID in potID) and (readingType in readingTypes):
        return dictMain[potID]['data'][readingType]
    # Return None if wrong potID or readingType
    else:
        return None 

# Convert timestamp to readable date and time object
def timestampConv(timestamp):
    return(datetime.fromtimestamp(int(timestamp)))

# Get a list of readings on a specified day of a specified month 
# day ranges from 1 -> 31 (int)
# month ranges from 1 -> 12 (int)
def getReadingByDay(potID, day, month, readingType):
    readings = getData(potID, readingType)
    daysReadings = []

    # Ensure data is pulled correctly
    if readings != None:
        for reading in readings:
            # Only collect data from relevant day and month
            # Ignore 0 values, they are useless
            timeOfReading = timestampConv(reading)
            if ((timeOfReading.day == day) 
            and (timeOfReading.month == month)
            and readings[reading] != 0):
                daysReadings.append(readings[reading])
    return daysReadings

# Get all the different days we have readings for in a specified month
# We will use this to get the x most recent daily averages to determine when to refill
def getReadingDates(potID, month, readingType):
    readings = getData(potID, readingType)
    days = []
    if readings != None:
        for reading in readings:
            timeOfReading = timestampConv(reading)
            if ((timeOfReading.month == month) 
            and (timeOfReading.day not in days)):
                days.append(timeOfReading.day)        
    return days

# Get list of daily averages
def getDailyAVGS(potID, month, readingType):

    dailyAVGS = []

    # Find the days we have readings for
    days = getReadingDates(potID, month, readingType)

    # Store each day and its corresponding average moisture reading
    for day in days:
        readings = getReadingByDay(potID, day, month, readingType)
        avgDayPair = (day, AVG(readings))
        dailyAVGS.append(avgDayPair)

    return dailyAVGS


# Average of values in a list
def AVG(lst):
    return(sum(lst) / len(lst))

# Becuase data is sparse we cant use our current month (No March data recorded)
# In theory we shouldnt need to pass month to this method
def refill(potID, month):
    
    dailyAVGS = getDailyAVGS(potID, month, 'moisture')
    sampleSize = len(dailyAVGS)

    # Without sparse data the first 2 conditions will never be triggered
    # I have left them as a safeguard
    if (sampleSize < 2):
        return False 
    elif (sampleSize == 3):
        mostRecentAVG = dailyAVGS[-1]
        oldAVGS = dailyAVGS[-3 : -1]
        readings = [reading for (day, reading) in oldAVGS]
        if(AVG(readings) - mostRecentAVG[1]) > 20:
            return True
        else:
            return False

    # Main condition:
    # Find the difference between the most recent days readings
    # And the average of the 3 days before the most recent reading
    # If it differs by more than 20:
    # User should look to refill (May not be completely empty)
    else:
        mostRecentAVG = dailyAVGS[-1]
        oldAVGS = dailyAVGS[-4:-1]
        readings = [reading for (day, reading) in oldAVGS]
        if(AVG(readings) - mostRecentAVG[1]) > 20:
            return True
        else:
            return False

# Helper method to get most recent reading for a reading type
def getMostRecent(readingDict):
    tempList = []
    for key in readingDict:
        tempList.append(readingDict[key])
    return tempList[-1]

def isPlantHealthy(potID):
    # Pull relevant data for plant health
    lightData = getData(potID, 'light')
    tempData = getData(potID, 'temperature')
    humidData = getData(potID, 'humidity')

    # Store most recent values for each reading type
    currentStats = []

    currentStats.append(getMostRecent(lightData))
    currentStats.append(getMostRecent(tempData))
    currentStats.append(getMostRecent(humidData))

    # Now that we have all plant stats, determine if its healthy



################# TESTING #################################################

# print(getReadingByDay('0001', 12, 2, 'moisture'))

# # print(getReadingDates('0001', 2, 'moisture'))

# print(getDailyAVGS('0001', 2, 'moisture'))

#isPlantHealthy('0001')
