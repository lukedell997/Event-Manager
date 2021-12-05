from flask import Flask, render_template, redirect, url_for, request, flash, session
from datetime import timedelta
from databaseCode import DataB


app = Flask(__name__)
app.permanent_session_lifetime = timedelta(hours=5)

db = DataB()
cnx, cursor = db.openDatabase()

app.secret_key = "hello"

admin = False
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

@app.route('/index' , methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
@app.route('/index.html', methods=["POST", "GET"])
def index():  # put application's code here
    popEventsTitle = []
    popEventsDetails = []
    popEventsButton = []

    nearEventsTitle = []
    nearEventsDetails = []
    nearEventsButton = []
#GET ALL POPULAR EVENTS----------------------------------------------
    popEventsId = []
    popEventsTitle = []
    popEventsSDate = []
    popEventsEDate = []
    popEventsDetails = []
    popEventsState = []

    popEvents = db.getEventsByPop(cursor)
    for tupleEvent3 in popEvents:
        popEventsId.append(tupleEvent3[0])
        popEventsTitle.append(tupleEvent3[1])
        popEventsSDate.append(tupleEvent3[2])
        popEventsEDate.append(tupleEvent3[3])
        popEventsDetails.append(tupleEvent3[6])
        popEventsState.append(tupleEvent3[12])
        
    
#END ALL POPULAR EVENTS----------------------------------------------
#GET ALL LOCATION EVENTS----------------------------------------------
    locEventsId = []
    locEventsTitle = []
    locEventsSDate = []
    locEventsEDate = []
    locEventsDetails = []
    locEventsState = []

    locEvents = db.getEventsByLoc(cursor, str("IL"))
    for tEvent in locEvents:
        locEventsId.append(tEvent[0])
        locEventsTitle.append(tEvent[1])
        locEventsSDate.append(tEvent[2])
        locEventsEDate.append(tEvent[3])
        locEventsDetails.append(tEvent[6])
        locEventsState.append(tEvent[12])
        
#END ALL LOCATION EVENTS----------------------------------------------
    search = None
    if request.method == "POST":
        search = request.form
        # DO A SEARCH IDK HOW YET

    return render_template("index.html", popEventsTitle=popEventsTitle, popEventsDetails=popEventsDetails,
                           popEventsButton=popEventsButton, nearEventsTitle=nearEventsTitle,
                           nearEventsDetails=nearEventsDetails, nearEventsButton=nearEventsButton, search=search)


@app.route('/registerPage.html', methods=["POST", "GET"])
@app.route('/registerPage', methods=["POST", "GET"])
def registerPage():  # put application's code here


    # WE SHOULD ADD A BUTTON TO CREATE THE ACCOUNT then send them to the login page
    if request.method == "POST":
        userFirstName = request.form["fn"]
        userLastName = request.form["ln"]
        userUsername = request.form["nm"]
        userPassword = request.form["pw"]
        userAddress = request.form["address"]
        userCity = request.form["city"]
        userState = request.form["state"]
        userEmail = request.form["email"]
        userNumber = request.form["phone"]
        userZipcode = 12345
# ^NEW USER TO DATABASE^-------------------------------------------^
        #turn to string
        cU = getInputString([userUsername, userPassword, userFirstName,
                             userLastName, userEmail, userAddress,
                             userZipcode, userCity, userState, userNumber])
        #check if already exists: if not, create new
        if (db.checkAny(cursor, "userId", "users", "username", str(userUsername)
                        , "username", str(userUsername)) == False):
            #print(test)
            db.newUser(cnx, cursor, cU)
            return redirect(url_for("loginPage"))
        else:
            print("ERROR: username already exists")
            return render_template("registerPage.html")
#^END NEW USER^------------------------------------------------------^
        
    if 'submit' in request.form:
            # PUSH THE DATA TO THE DATABASE!!!!!!!!!
        return redirect(url_for("login"))  # ????
    else:
        return render_template("registerPage.html")


@app.route('/loginPage.html', methods=["POST", "GET"])
@app.route('/loginPage', methods=["POST", "GET"])
def loginPage():  # put application's code here

    if request.method == "POST":
        '''if 'remember' in request.form:
            app.permanent_session_lifetime = timedelta(weeks=10000)
        elif 'remember' not in request.form:
            app.permanent_session_lifetime = timedelta(seconds=0)'''
        session.permanent = True
        user = request.form["nm"]  # NEED TO CHECK THAT USER EXISTS
        password = request.form["pw"]
        session["user"] = user
#^GET USER^-------------------------------------------------------------^
        #: check if user found, then get user info into variables
        if (db.checkAny(cursor, "userId", "users", "username", str(user),
            "passwordId", str(password)) == True):
            
            [uId, user, password, uFN, uLN, uEmail,
             uAd, uZip, uCity, uState,
             uPhone] = db.getUser(cursor, str(user), str(password))
            
            #put user info into session...
            session["userId"] = uId
            session["userEmail"] = uEmail
            session["userState"] = uState
            #session["nm"] = user
            return redirect(url_for("user")) 
            
        else:
            print("Error: The username or password is incorrect")
            return render_template("loginPage.html")
            
#^END GET USER^-----------------------------------------------^
        
    else:
        return render_template("loginPage.html")


@app.route("/index_userLoggedIn.html", methods=["POST", "GET"])
@app.route("/index_userLoggedIn", methods=["POST", "GET"])
def user():
    if "user" in session:
        search = None
        if request.method == "POST":
            search = request.form
            # DO A SEARCH IDK HOW YET

        user = session["user"]
        userId = session["userId"]
        userLoc = session["userState"]
    


#GET ALL USER EVENTS ATTENDING------------------------------- NEEDS UPDATING
        attendingEventsId = []
        attendingEventsTitle = []  # FILL WITH USERES EVENTS
        attendingEventsSDate = []  # FILL WITH 6 popular EVENTS
        attendingEventsEDate = []  # FILL WITH 6 NEAR BY EVENTS
        attendingEventsState = []
        
        
        #get user_events by userId
        userEvents = db.getUEventsByUser(cursor, str(userId))

        #for all user_events, get the event
        for tupleEvent in userEvents:
            evInfo = db.getEventsByEId(cursor, str(tupleEvent[2]))

            #add each section to list
            attendingEventsId.append(evInfo[0])
            attendingEventsTitle.append(evInfo[1])
            attendingEventsSDate.append(evInfo[2]) 
            attendingEventsEDate.append(evInfo[3])
            attendingEventsState.append(evInfo[12])


#END ALL USER EVENTS ATTENDING----------------------------------------    
#GET ALL USER EVENTS ADMINISTRATING----------------------------------
        adminEventsId = []
        adminEventsTitle = []
        adminEventsSDate = []
        adminEventsEDate = []
        
        adminEvents = db.getEventsByUser(cursor, str(userId))
        for tupleEvent2 in adminEvents:
            adminEventsId.append(tupleEvent[0])
            adminEventsTitle.append(tupleEvent2[1])
            adminEventsSDate.append(tupleEvent2[2])
            adminEventsEDate.append(tupleEvent2[3])
            adminEventsState.append(tupleEvent2[12])
            
#END ALL USER EVENTS ADMINISTRATING----------------------------------
#GET ALL POPULAR EVENTS----------------------------------------------
        popEventsId = []
        popEventsTitle = []
        popEventsSDate = []
        popEventsEDate = []
        popEventsDetails = []
        popEventsState = []

        popEvents = db.getEventsByPop(cursor)
        for tupleEvent3 in popEvents:
            popEventsId.append(tupleEvent3[0])
            popEventsTitle.append(tupleEvent3[1])
            popEventsSDate.append(tupleEvent3[2])
            popEventsEDate.append(tupleEvent3[3])
            popEventsDetails.append(tupleEvent3[6])
            popEventsState.append(tupleEvent3[12])
            
        
#END ALL POPULAR EVENTS----------------------------------------------
#GET ALL LOCATION EVENTS----------------------------------------------
        locEventsId = []
        locEventsTitle = []
        locEventsSDate = []
        locEventsEDate = []
        locEventsDetails = []
        locEventsState = []

        locEvents = db.getEventsByLoc(cursor, str(userLoc))
        for tEvent in locEvents:
            locEventsId.append(tEvent[0])
            locEventsTitle.append(tEvent[1])
            locEventsSDate.append(tEvent[2])
            locEventsEDate.append(tEvent[3])
            locEventsDetails.append(tEvent[6])
            locEventsState.append(tEvent[12])
#END ALL LOCATION EVENTS----------------------------------------------
            
        popEventTitle = []
        popEventDetails = []
        if "clicked" in request.form and request.method == "POST":
            return  # NEED TO FIX THIS BY CHANGING EVENTDEAITLS.HTML TO CONTAIN NAME IN URL
        return render_template("index_userLoggedIn.html", name=user,
                               attendingEventsTitle=attendingEventsTitle, attendingEventsDate=attendingEventsSDate,
                               attendingEventsDeadline=attendingEventsEDate, popEventTitle=popEventsTitle,
                               popEventDetails=popEventsSDate, search=search)

    else:
        return redirect(url_for("loginPage"))  # ????


# This is for a logout page that might be made
@app.route("/logout")
def logout():
    session.pop("user", None)
    # flash("You have been logged out!", "info")
    return redirect(url_for("loginPage"))  # ????


@app.route('/eventDetails.html', methods=["POST", "GET"])
@app.route('/eventDetails', methods=["POST", "GET"])
def eventDetails():  # put application's code here
    # NEED TO PULL ALL THE VARIABLES THAT ARE BEING PASSED FROM THE DATABASE
    
#GET ALL EVENT INFO------------------------------------------------------------
    #check if event found by eventId
    if (db.checkAny(cursor, "eventId", "events", "eventId", str(eventId),
            "eventId", str(eventId)) == True):
        #get all variables in event
            [eventId, eventName, eventStartDate, eventEndDate, eventDeadline, eventPrice, eventDescription,
             eventCap, eventOcp, eventPoP, eventAddress,
             eventCity, eventState, eventZip] = db.getEventByEId(cursor, eventId)
    else:
        #otherwise send back to search
        return redirect(url_for('search_browseEvents'))
    

#END ALL EVENT INFO------------------------------------------------------------
    
    if "user" in session:
        if "attend" in request.form and request.method == "POST":

            #get all info you need
            userId = session["userId"]
            user = session["user"]
            paid = 1
            seat = O0
            price = eventPrice
            #if free, user has paid
            if (price != 0):
                paid = 0

# ADD USER FROM ATTENDING EVENT--------------------------
            #turn to string
            cUE = getInputString([userId, eventId, user, email, paid, seat, price])

            #check if not already exists: AND if not full
            if (db.checkAny(cursor, "attendantId", "user_events", "userId",
                            str(userId), "eventId", str(eventId)) == False
                and db.checkAvl(cursor, str(eventId)) == True):

                #create new user events
                db.newUEvents(cnx, cursor, cUE)
                
                #add occupant to event
                db.updateEventOcp(cnx, cursor, eventId, eventOcp)
                
                return redirect(url_for("manageEvents"))
            else:
                #give error(filled or user already signed up)
                print("ERROR: event filled or already signed up")
                return render_template("eventDetails.html", eventDate=eventDate, eventTitle=eventTitle,
                                       eventPrice=eventPrice, eventDescription=eventDescription,
                                       eventAddress=eventAddress, eventTags=eventTags)
# END ADD USER FROM ATTENDING EVENT--------------------------


        else:
           return render_template("eventDetails.html", eventDate=eventDate, eventTitle=eventTitle, eventPrice=eventPrice,
                               eventDescription=eventDescription, eventAddress=eventAddress, eventTags=eventTags) 


    else:
        print("Must be signed in to attend")
        return render_template("eventDetails.html", eventDate=eventDate, eventTitle=eventTitle, eventPrice=eventPrice,
                               eventDescription=eventDescription, eventAddress=eventAddress, eventTags=eventTags)


@app.route('/manageEvents.html', methods=["POST", "GET"])
@app.route('/manageEvents', methods=["POST", "GET"])
def manageEvents():  # put application's code here
    if "user" in session:
        usersEvents = []  # FILL THESE WITH THE APPROPRIATE DATA
        userEventsDates = []
        userEventsTime = []
        userAttendingEvents = []  # I have no idea what the difference between the first one and this one is but it is requested
        eventsMaxPop = []

        if 'leave' in request.form and request.method == "POST":
            user = session["user"]
# REMOVE USER FROM ATTENDING EVENT------------------------------------
            #if user found with event
            if (db.checkAny(cursor, "attendantId", "user_events", "userId",
                            str(userId), "eventId", str(eventId)) == True):

                #remove user from event attendance
                db.removeUEvents(cnx, cursor, userId, eventId)
                #update events occupants
                db.removeEventOcp(cnx, cursor, eventId)
                
                return redirect(url_for("manageEvents"))
            else:
                print("Attendant Not found for event")
                return render_template("manageEvents.html", usersEvents=usersEvents, userEventsDates=userEventsDates,
                               userEventsTime=userEventsTime, userAttendingEvents=userAttendingEvents,
                               eventsMaxPop=eventsMaxPop)
            
#END REMOVE USER FROM ATTENDING EVENT------------------------------------
        return render_template("manageEvents.html", usersEvents=usersEvents, userEventsDates=userEventsDates,
                               userEventsTime=userEventsTime, userAttendingEvents=userAttendingEvents,
                               eventsMaxPop=eventsMaxPop)

    else:
        return redirect(url_for("login"))  # ????


@app.route('/search_browseEvents.html')
@app.route('/search_browseEvents')
def search_browseEvents():  # put application's code here
    events = []  # fill the info
    eventDates = []
    eventTimes = []
    eventLocations = []
    eventPrices = []
    eventPopulation = []
    eventMaxPop = []

#SEARCH BY EVENT TAGS------------------------------#needs an indication
    tagName = "7"       #needs input from html
    tagEventsId = []
    tagEventsTitle = []  
    tagEventsSDate = []  
    tagEventsEDate = [] 
    tagEventsState = []
    
    
    #get user_events by userId
    tagEvents = db.getEventTagByTagId(cursor, str(tagName))

    #for all user_events, get the event
    for tgEvent in tagEvents:
        evInfo = db.getEventsByEId(cursor, str(tagEvents[1]))

        #add each section to list
        tagEventsId.append(evInfo[0])
        tagEventsTitle.append(evInfo[1])
        tagEventsSDate.append(evInfo[2]) 
        tagEventsEDate.append(evInfo[3])
        tagEventsState.append(evInfo[12])
#END SEARCH BY EVENT TAGS-------------------------
        
    return render_template("search_browseEvents.html", events=events, eventDates=eventDates, eventTimes=eventTimes,
                           eventLocations=eventLocations, eventPrices=eventPrices, eventPopulation=eventPopulation,
                           eventMaxPop=eventMaxPop)


@app.route('/create_editEvents.html', methods=["POST", "GET"])
@app.route('/create_editEvents', methods=["POST", "GET"])
def create_editEvents():
    userInfo = []  # list contating users names and their roles to pull from database
    if request.method == "POST":
        eventTitle = request.form["title"]
        eventAddress = request.form["address"]
        eventCity = request.form["city"]
        eventState = request.form["state"]
        eventZip = request.form["zip"]
        eventStartDate = request.form["startDate"]
        eventEndDate = request.form["endDate"]
        eventPrice = request.form["price"]
        eventCap = request.form["maxCap"]
        eventDeadline = request.form["deadline"]
        uploadedFile = request.form["uploadedFile"]
        eventDes = request.form["description"]
        userToAdd = request.form["addUser"]
        userToDelete = request.form["deleteUser"]
        eventOcp = 0
        userId = session["userId"]
#NEW EVENT--------------------------------------------------------------
        #turn to string
        cE = getInputString([eventTitle, eventStartDate, eventEndDate, eventDeadline, eventPrice, eventDes, eventCap,
                             eventOcp, eventPoP, eventAddress, eventCity, eventState, eventZip, userId])
        #check if already exists: if not, create new
        if (db.checkAny(cursor, "eventId", "events", "name", str(eventTitle)
                        , "userId", str(userId)) == False):
            #print(test)
            db.newEvent(cnx, cursor, cE)
            return redirect(url_for("manageEvents"))
        else:
            print("ERROR: event already created by you")
            return render_template("create_editEvents.html", userInfo=userInfo)
#END NEW EVENT--------------------------------------------------------------
    else:
        return render_template("create_editEvents.html", userInfo=userInfo)

    



#FOR USER EDIT------------------------------------

#USER UPDATE--------------------------------------------
#USER UPDATE--------------------------------------------

#USER REMOVE--------------------------------------------
#USER REMOVE--------------------------------------------

#EVENT UPDATE--------------------------------------------
#EVENT UPDATE--------------------------------------------

#EVENT REMOVE--------------------------------------------
#EVENT REMOVE--------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
