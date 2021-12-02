from flask import Flask, render_template, redirect, url_for, request, flash, session
from datetime import timedelta
from databaseCode import DataB


app = Flask(__name__)
app.permanent_session_lifetime = timedelta(hours=5)
db = DataB()
app.secret_key = "hello"

admin = False

#turn list of objects into proper string for database
def getInputString(ItemList):
    try:
       #for all items in input, add ' data '
        info = ""
        for i in range (len(ItemList)):
            if ItemList[i] == "" or ItemList[i] == "None":
                info += "'None'"
            else:
                info += "'"
                info += str(ItemList[i])
                info += "'"

            #add comma unless last item
            if(i != len(ItemList)-1):
                info += ","
            else:
                return info
        return info
    except:
        return -99

@app.route('/index')
@app.route('/')
@app.route('/index.html')
def index():  # put application's code here
    popEventsTitle = []
    popEventsDetails = []
    popEventsButton = []

    nearEventsTitle = []
    nearEventsDetails = []
    nearEventsButton = []
    # FILL LISTS WITH DATA OF EVENTS FROM DATABASE
    
    search = None
    if request.method == "POST":
        search = request.form
        # DO A SEARCH IDK HOW YET

    return render_template("index.html", popEventsTitle = popEventsTitle, popEventsDetails = popEventsDetails,
                           popEventsButton = popEventsButton, nearEventsTitle = nearEventsTitle,
                           nearEventsDetails = nearEventsDetails, nearEventsButton = nearEventsButton, search=search)

@app.route('/registerPage.html')
@app.route('/registerPage')
def registerPage():  # put application's code here
    userFirstName = request.form["fn"]
    userLastName = request.form["ln"]
    userUsername = request.form["nm"]
    userPassword = request.form["pw"]
    userAddress = request.form["address"]
    userCity = request.form["city"]
    userState = request.form["state"]
    userEmail = request.form["email"]
    userNumber = request.form["phone"]

    # WE SHOULD ADD A BUTTON TO CREATE THE ACCOUNT then send them to the login page
    if 'submit' in request.form:
        #STILL NEED TO CHECK IF DATA IS CORRECT(state is 2 letters, zip 5 numbers, etc)
        
# *NEW USER TO DATABASE----------------------------------
        #turn to string
        cU = getInputString([userUsername, userPassword, userFirstName,
                             userLastName, userEmail, userAddress,
                             userZipcode, userCity, userState, userNumber])
        #check if already exists: if not, create new
        if (db.checkAny(cursor, "userId", "users", "username", str(userUsername)
                        , "username", str(userUsername)) == True):
            print("ERROR: username already exists")
        else:
            db.newUser(cnx, cursor, cU)
#END NEW USER---------------------------------------
            
        return redirect(url_for("login")) #????
    return render_template("registerPage.html")


@app.route('/loginPage.html', methods=["POST", "GET"])
@app.route('/loginPage', methods=["POST", "GET"])
def loginPage():  # put application's code here
    if 'remeber' in request.form:
        app.permanent_session_lifetime = timedelta(weeks=10000)
    elif 'remeber' not in request.form:
        app.permanent_session_lifetime = timedelta(seconds=0)
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]       # NEED TO CHECK THAT USER EXISTS
        password = request.form["pw"]
#GET USER--------------------------------------------------
        #: check if user found, then get user info into variables
        if (db.checkAny(cursor, "userId", "users", "username", str(user),
            "passwordId", str(password)) == True):
            [uId, user, password, uFN, uLN, uEmail,uAd, uZip, uCity, uState,uPhone] = db.getUser(cursor, str(user), str(password))

            #put user info into session...
            #session["userId:"] = uId
            #session["nm"] = user
            
            return redirect(url_for("user"))
        else:
            print("Error: The username or password is incorrect")
            
#END GET USER-----------------------------------------------
        
        #session["user:"] = user
        

    return render_template("loginPage.html")



@app.route("/index_userLoggedIn.html")
@app.route("/index_userLoggedIn")
def user():

    if "user" in session:
        search = None
        if request.method == "POST":
            search = request.form
            #DO A SEARCH IDK HOW YET

        user = session["user"]
        userId = session["userId"]

        myEventImage = []  # FILL THESE
        myEventTitle = ""
        myEventDetails = ""

        
        
        attendingEventsTitle = [] # FILL WITH USERES EVENTS
        attendingEventsDate= [] # FILL WITH 6 popular EVENTS
        attendingEventsDeadline = [] # FILL WITH 6 NEAR BY EVENTS

        attendingEventsId = []
        attendingEventsUId = []
        attendingEventsPrice = []
        attendingEventsDesc = []
        attendingEventsCap = []
        attendingEventsOcp = []
        attendingEventsAd = []
        attendingEventsZip = []
        attendingEventsState = []
        
#GET ALL USER EVENTS------------------------------- NEEDS UPDATING
        #get user_events by userId
        userEvents = db.getUEventsByUser(cursor, userId)

        #for all user_events, get the event
        for tupleEvent in userEvents:
            evInfo = db.getEventByEId(cursor, tupleEvent[2])

            #add each section to list
            attendingEventsId.append(evInfo[0])
            
            attendingEventsTitle.append(evInfo[1]) 
            attendingEventsDate.append(evInfo[2]) 
            attendingEventsDeadline.append(evInfo[3])

            attendingEventsPrice.append(evInfo[4])
            attendingEventsDesc.append(evInfo[5])
            attendingEventsCap.append(evInfo[6])
            attendingEventsOcp.append(evInfo[7])
            attendingEventsAd.append(evInfo[9])
            attendingEventsZip.append(evInfo[10])
            attendingEventsState.append(evInfo[11])
            attendingEventsUId.append(evInfo[12])
#GET ALL USER EVENTS----------------------------------------

        popEventTitle = []
        popEventDetails = []
        if "clicked" in request.form:
            return # NEED TO FIX THIS BY CHANGING EVENTDEAITLS.HTML TO CONTAIN NAME IN URL
        return render_template("index_userLoggedIn.html", name = user, myEventImage = myEventImage,
                               myEventTitle = myEventTitle, myEventDetails = myEventDetails,
                               attendingEventsTitle = attendingEventsTitle, attendingEventsDate = attendingEventsDate,
                               attendingEventsDeadline = attendingEventsDeadline, popEventTitle= popEventTitle,
                               popEventDetails = popEventDetails, search = search)

    else:
        return redirect(url_for("login")) #????



# This is for a logout page that might be made
@app.route("/logout")
def logout():
    session.pop("user", None)
    #flash("You have been logged out!", "info")
    return  redirect(url_for("login")) #????


@app.route('/add_editEvents.html')
@app.route('/add_editEvents')
def add_editEvents():  # put application's code here  
    return render_template("add_editEvents.html")

@app.route('/eventDetails.html')
@app.route('/eventDetails')
def eventDetails(eventId):  # put application's code here
    #NEED TO PULL ALL THE VARIABLES THAT ARE BEING PASSED FROM THE DATABASE
    eventDate = []
    eventTitle = []
    eventPrice = []
    eventDescription = []
    eventAddress = []
    eventTags = []

#GET EVENT------------------------------
    
    #: check if event found, if True get user info into variables
    if (db.checkAny(cursor, "eventId", "events", "eventId", str(eventId),
        "eventId", str(eventId)) == False):
        print("Error: The username or password is incorrect")
    else:
        [eId, eTitle, eSDate, eEDate, eDeadline, ePrice,
         eDesc, eCap, eOcp, ePoP, eAddress, eCity, eSate, eZip,
         eUID] = db.getEventByEId(cursor, str(eventId))
        #add info for display(if need be)...

#END GET EVENT----------------------------------

        
    if "user" in session:
        if "attend" in request.form:
            user = session["user"]
            
#ADD USER TO ATTENDING THE EVENT-------------------------------------
            #check if userId and eventId match, if not add them
            if (db.checkAny(cursor, "attendantId", "user_events", "userId",
                            str(userId), "eventId", str(eventId)) == True):
                print("Error: You are already attending event")
            #check if user is event creator
            elif(db.checkAny(cursor, "name", "events", "userId", str(userId),
                             "eventId", str(eventId))):
                print("Error: You are the event creator. You cannot mark as attending")
            else:
                #get data for info, turn into string, then make new attendee
                userEmail = session["userEmail:"]
                paid = 0
                seat = -99
                uE = getInputString([userId, eventId, userEmail,
                                     paid, seat, ePrice])
                newUEvents(cnx, cursor, uE)
                #*add event 1 occupant
                
#END ADD USER TO ATTENDING THE EVENT----------------------------------

            
    return render_template("eventDetails.html", eventDate = eventDate, eventTitle = eventTitle, eventPrice = eventPrice,
                           eventDescription = eventDescription, eventAddress = eventAddress, eventTags = eventTags)

@app.route('/manageEvents.html')
@app.route('/manageEvents')
def manageEvents():  # put application's code here
    if "user" in session:

#GET USER_EVENTS AGAIN----------------------------
#END GET USER_EVENTS-----------------------------
        usersEvents = []  # FILL THESE WITH THE APPROPRIATE DATA
        userEventsDates = []
        userEventsTime = []
        userAttendingEvents = [] #I have no idea what the difference between the first one and this one is but it is requested
        eventsMaxPop = []

        if 'leave' in request.form:
            user = session["user"]
            userId = session["userId:"]

#REMOVE THE USER FROM THE EVENT IN DATABASE-------------
        if(checkAny(cursor, "attendantId", "user_events", "userId",
                    uId, "eventId", eventId) == True):
            removeUEvents(cnx, cursor, userId, eventId)
            #subtract event by 1 occupant
        else:
            print("ERROR: USER EVENT NOT FOUND")
#REMOVE USER_EVENT-------------------------------------

        return render_template("manageEvents.html", usersEvents = usersEvents, userEventsDates = userEventsDates,
                               userEventsTime = userEventsTime, userAttendingEvents = userAttendingEvents,
                               eventsMaxPop = eventsMaxPop)

    else:
        return  redirect(url_for("login")) #????

@app.route('/search_browseEvents.html')
@app.route('/search_browseEvents')
def search_browseEvents():  # put application's code here
#SEARCH BY KEYWORDS

#SEARCH BY DATES

#SEARCH BY TAG

#SEARCH BY LOCATION

#SEARCH BY PRICE
    events = [] #fill the info
    eventDates = []
    eventTimes = []
    eventLocations = []
    eventPrices = []
    eventPopulation = []
    eventMaxPop = []
    return render_template("search_browseEvents.html", events = events, eventDates = eventDates, eventTimes = eventTimes,
                           eventLocations = eventLocations, eventPrices= eventPrices, eventPopulation = eventPopulation,
                           eventMaxPop = eventMaxPop)

@app.route('/create_editEvents.html', methods=["POST", "GET"])
@app.route('/create_editEvents', methods=["POST", "GET"])
def create_editEvents():
    userInfo = [] #list contating users names and their roles to pull from database
    if request.method == "POST":
        eventTitle = request.form["title"]#
        eventAddress = request.form["address"]#
        eventCity = request.form["city"]#
        eventState = request.form["state"]#
        eventZip = request.form["zip"]#
        eventStartDate = request.form["startDate"]
        eventEndDate = request.form["endDate"]
        eventPrice = request.form["price"]#
        eventCap = request.form["maxCap"]#
        eventDeadline = request.form["deadline"]#
        uploadedFile = request.form["uploadedFile"]
        eventDes = request.form["description"]#
        userToAdd = request.form["addUser"]
        userToDelete = request.form["deleteUser"]
        ################## push to database!!!!!!!
        eventOccupants = 0
        eUserId = session["userId:"]
#CREATE NEW EVENT---------------------------------
        #create string of all variables
        cE = getInputString([eventTitle, eventStartDate, eventEndDate,
                             eventDeadline, eventPrice, eventDes, eventCap,
                             eventOccupants, eventPoP, eventAddress,
                             eventCity, eventState, eventZip, eUserId])
        
        #check if event name and ID exists
        if (db.checkAny(cursor, "eventId", "events", "name", str(eventTitle)
                        , "userId", str(user)) == True):
            print("ERROR: username already exists")
        else:
            db.newEvent(cnx, cursor, cE)

#END CREATE NEW EVENT----------------------------------------

    return render_template("create_editEvents.html", userInfo=userInfo)



if __name__ == '__main__':
    app.run(debug=True)
