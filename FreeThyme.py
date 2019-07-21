import flask, httplib2, uuid, collections
from flask import request, session
from flask_socketio import SocketIO
from googleapiclient import discovery
from oauth2client import client
from support_calendar import getCalendarIDs, freeBusyQueryFunc
from support_conversion import convertTimetoMinute, webDisplayFormat
from support_freethyme import unavailableTime, findFreeThyme, sortSchedule

#The instance objects that stores information while running program
app = flask.Flask(__name__)
socketio = SocketIO(app)
globalSchedule = []
emailList = []


#This is the beginning of the flask route
#PROGRAM STARTS HERE
@app.route('/')
def index():
    #If credentials do not exist, redirect to login page
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    #Set credentials
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    #Case if credentials have expired, redirect to login page
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    
    try:
        credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    #When credential error
    except:
        print("Did not properly assign credentials")
    
    return flask.render_template('thyme-website.html', emails = emailList)


#ADD CALENDAR BUTTON RUNS BUT STAYS ON SAME PAGE:
@app.route("/add-calendar", methods=['GET', 'POST'])
def addCalendar():
    if request.method == 'POST':
        _hours = request.form.get('thyme', None)
        _days = request.form.get('search', None)
        session['_hours'] = _hours
        session['_days'] = _days
        return flask.redirect(flask.url_for('resultScreen'))
    print("Adding calendar")
    #If credentials do not exist, redirect to login page
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    #Set credentials
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    #Case if credentials have expired, redirect to login page
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    try:
        credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    #When credential error
    except:
        print("Did not properly assign credentials")
    #Create Http authentication
    http_auth = credentials.authorize(httplib2.Http())
    #Create service for Google Calendar API
    service = discovery.build('calendar', 'v3', http_auth)
    page_token = None
    #Create a list of Calendar ID's
    calendarIDs = getCalendarIDs(service, page_token)
    #Append calendarIDs in emailString
    for x in calendarIDs:
        if ('.com' in x['name']):
            if x['name'] not in emailList:
                emailList.append(x['name'])
    #Run freeBusyQueryFunc
    bigSchedule = freeBusyQueryFunc(calendarIDs, service)
    globalSchedule.extend(bigSchedule) 
    return flask.render_template('thyme-website.html', emails = emailList)
        
#RESET BUTTON RUNS BUT STAYS ON SAME PAGE  
@app.route("/reset-calendar")
def resetCalendarScreen():   
    resetCalendar()
    return flask.render_template('thyme-website.html', emails = emailList)

#Running when the page is redirected to the results page
@app.route("/thyme-results.html")
def resultScreen():
    if(not emailList):
        return flask.render_template('thyme-website.html', emails = emailList, error = "No Calendars were Added") 

    bigSchedule = globalSchedule
    #TEMP ASSIGNMENTS
    default_thyme = '3'
    _hours = session.get('_hours', default_thyme)
    default_search = '14'
    try: _days = int(session.get('_days', default_search))
    except: _days = 14
    
    #Add unavailableTimeList to big Schedule
    bigSchedule.extend(unavailableTime(_days))
    
    #Convert hours to minutes
    _min = convertTimetoMinute(_hours)

    #Make final list by finding time with given minute input
    finalList = findFreeThyme(list(collections.deque(sortSchedule(bigSchedule))), _min)

    finalList = webDisplayFormat(finalList)

    return flask.render_template('thyme-results.html', minutes = _min, days = _days, freeThymes = finalList, emails = emailList), resetCalendar()

#When user clicks on the contact page   
@app.route("/thyme-website-contact.html")
def contactPage():    
    return flask.render_template('thyme-website-contact.html')

#When user clicks on the about page
@app.route("/thyme-website-about.html")
def aboutPage():    
    return flask.render_template('thyme-website-about.html')

#This is the beginning of the oauth callback route (/login page)
@app.route('/oauth2callback')
def oauth2callback():
    #Call Google OAuth
    flow = client.flow_from_clientsecrets(
        #Load Google Cloud Client ID and Secret
        'client_secrets.json',
        #OAuth Consent Scope (Sensitive Scope)
        scope='https://www.googleapis.com/auth/calendar.readonly email',
        #Redirect to /login to complete request
        redirect_uri=flask.url_for('oauth2callback', _external=True))
    #Redirect if auth code is not in request
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    #Create credentials from auth code
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        
    #Redirect back to index.html
    return flask.redirect(flask.url_for('index'))

#Function resets calendar
def resetCalendar():   
    print("Resetting calendar")
    globalSchedule.clear()
    emailList.clear()

#Server setup
if __name__ == '__main__':
    app.secret_key = str(uuid.uuid4())
    print('Server started')
    socketio.run(
    app,
    host='localhost',
    port=int(8080),
    )

