'''
Functions that manage the calendars
'''

from datetime import datetime
from support_conversion import convertDateTimeToGoogle
from support_freethyme import addTimeScan


#Google Calendar API to collect calendarID's
def getCalendarIDs(service, page_token):
    calendarIDs = []
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            calendarIDs.append({"name": calendar_list_entry['summary'], "id": calendar_list_entry['id']})
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    return calendarIDs

#Google Calendar API query function
def freeBusyQueryFunc(calendarIDs, service, _days = 14, _timezone = ["America/Los_Angeles","07:00"]):
    bigSchedule = []
    freeBusyQuery = []
    #Query each calendar from list of Calendar ID's
    for x in calendarIDs:
        calID = x.get('id')
        PARAMS = {'timeMin': convertDateTimeToGoogle(datetime.now()),
                  "timeMax": addTimeScan(_days),
                  "timeZone": _timezone[0],
                  "items":[{"id": calID}]
                  }
        
        freeBusyQuery = (service.freebusy().query(body=PARAMS).execute())
        
        #Add all start and end times to bigSchedule
        for elem in freeBusyQuery['calendars'][calID]['busy']:
            bigSchedule.append(elem)
    return bigSchedule