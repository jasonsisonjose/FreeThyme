'''
Functions to convert to various formats
'''

from datetime import datetime

#Convert to web display format for flask
def webDisplayFormat(finalList):
    revisedFinalList = []
    for freeThyme in finalList:

        #converts numDay to wordDay
        stringDate = freeThyme[1].strftime("%A, %B %d, %Y   ~   ")

        #creates startTime by parsing
        startTime = freeThyme[1].strftime("%I:%M %p")

        #creates entTime by parsing

        endTime = freeThyme[2].strftime("%I:%M %p")

        #creates time interval
        timeInterval =  startTime + " - " + endTime

        #Create an output string
        outString = stringDate + timeInterval


        #adds "freethyme event" into bigger list of "freethyme events"
        revisedFinalList.append(outString)

    #Pop first element
    revisedFinalList.pop(0)

    return revisedFinalList

#Function to convert input time to minutes
def convertTimetoMinute(timeLength):
    try:
        hours, minutes = timeLength.split(":")
        hours = int(hours)
    except:
        try:
            hours = int(timeLength)
            minutes = 0
        except:
            hours = 3
            minutes = 0
    return(hours*60 + int(minutes))

#Function to convert tring to dateTime
def convertDateTime(inputString):
    #parses the first event by "T"
    #so day1 = YEAR-MONTH-DAY, and wholetime = HOUR:MINUTES:SECONDS-TIMEZONE
    date, wholeTime = inputString.split('T')
    
    year, month, day = date.split("-")
    
    #using the whole time we parse it by the "-" symbol meaning that
    #time1 = HOURS:MINUTES:SECONDS, and timezone1 = TIMEZONE
    time, timezone = wholeTime.split("-")
    
    #now that we have the time format as HOUR:MINUTES:SECONDS
    #we can once again parse it to get the HOURs, MINUTEs, and SECONDs 
    #and store them in dedicated variables 
    #hour1 = hours, minutes1 = minutes, seconds1 = seconds, 
    hour, minutes, seconds= time.split(":")
    #we must convert the parsed quantities into integers so that
    #they can be used by the "timedelta" function
    year = int(year)
    month = int(month)
    day = int(day)
    hour = int(hour)
    minute = int(minutes)
    second = int(seconds)
    
    outputDateTime = datetime(year, month, day, hour, minute, second)
    
    return outputDateTime

#Function that converts datetime objects to google api time format
def convertDateTimeToGoogle(dateTime, _timezone = ["America/Los_Angeles","07:00"]):
    year = dateTime.year
    month = dateTime.month
    day = dateTime.day
    hour = dateTime.hour
    minute = dateTime.minute
    second = dateTime.second
    #Format '2019-05-01T03:00:00-07:00'
    outputString = f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}-{_timezone[1]}"
    
    return str(outputString)