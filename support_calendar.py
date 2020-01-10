'''
Functions that manage the calendars
'''

from datetime import datetime
from support_freethyme import addTimeScan


#Google Calendar API to collect calendarID's
def getCalendarIDs(service, page_token):
    print("grabbing calendars")
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
        print("calendar id:", x)
        calID = x.get('id')
        #We can send python datetime objects to Google API by doing ".isoformat + 'Z'", Z = UTC(universal time clock) time zone
        PARAMS = {'timeMin': datetime.now().isoformat() + 'Z',
                  "timeMax": addTimeScan(_days),
                  "timeZone": _timezone[0],
                  "items":[{"id": calID}]
                  }

        freeBusyQuery = (service.freebusy().query(body=PARAMS).execute())

        #Add all start and end times to bigSchedule
        for elem in freeBusyQuery['calendars'][calID]['busy']:
            print("Type of elem: ", type(elem["start"]), elem)
            bigSchedule.append(elem)
    print("Big Schedule: ", bigSchedule)
    return bigSchedule
