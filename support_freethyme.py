'''
Functions that are essential to the freethyme application
'''

from datetime import datetime, timedelta
from support_conversion import convertDateTime, convertDateTimeToGoogle

#Function to sort schedule; this is the sorting algorithm
def sortSchedule(bigSchedule):
    startTimeList = []
    endTimeList = []
    for x in bigSchedule:
        startTimeList.append(convertDateTime(x["start"]))
        endTimeList.append(convertDateTime(x["end"]))
    startTimeList.sort()
    endTimeList.sort()
    outputList = []
    for x in startTimeList:
        tempDict = {"start":x,"end":endTimeList[startTimeList.index(x)]}
        outputList.append(tempDict)
    return outputList

#Function for to add unavailable time to bigSchedule given start and end time (add this daily)
#Useful to adding bedtimes where it is not a good idea to suggest events in the middle of the night
def unavailableTime(_days,_sHr=0,_sMin=00,_eHr=9,_eMin=00):
    #input an int of days
    unavailableTimeList = []
    for x in range(_days):
       timeDeltaDays = timedelta(days = x) 

       currentDay = datetime.now()

       currentDate = datetime(year = currentDay.year, month = currentDay.month, day=currentDay.day, hour=_sHr, minute=_sMin)
       currentDate = currentDate + timeDeltaDays
       startUn = convertDateTimeToGoogle(currentDate)

       currentDate = datetime(year = currentDay.year, month = currentDay.month, day=currentDay.day, hour=_eHr, minute=_eMin)
       currentDate = currentDate + timeDeltaDays
       endUn = convertDateTimeToGoogle(currentDate)

       unavailableTimeList.append({"start":startUn,"end":endUn})
    return unavailableTimeList

#Functions that add time scans    
def addTimeScan(_days,_eHr = 9,_eMin = 00):
    timeDeltaDays = timedelta(days = _days) 
    timeScan = datetime.now() + timeDeltaDays
    timeScan.replace(hour = _eHr)
    timeScan.replace(minute = _eMin)
    timeScan = convertDateTimeToGoogle(timeScan)
    return timeScan

#Given sorted schedule and minimum appointment length find FreeThyme
def findFreeThyme(eventList, appointmentLength):
    #Format for input eventList, 180 (time in minutes)
    listOfFreeThyme = []
    timeDeltaAppointmentLength = timedelta(minutes = appointmentLength)
    for event1,event2 in zip(eventList, eventList[1:])    :
        freeThyme = findDiffTime(event1,event2)
        if freeThyme[0] >= timeDeltaAppointmentLength:
            listOfFreeThyme.append(freeThyme)
    return listOfFreeThyme

#Function to find difference in time
def findDiffTime(event1, event2):
    
    eventdelta1 = (event1["end"])
    eventdelta2 = (event2["start"])

    lengthOfFreeThyme = eventdelta2 - eventdelta1
    return [lengthOfFreeThyme, event1["end"], event2["start"]]

    