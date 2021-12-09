from flask import Flask, render_template, redirect, url_for, request, flash, session
from datetime import timedelta
from databaseCode import DataB

app = Flask(__name__)

app.permanent_session_lifetime = timedelta(hours=5)

app.secret_key = "hello"

db = DataB()
cnx, cursor = db.openDatabase()

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
########################################################################--INDEX--############
@app.route('/index' , methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
@app.route('/index.html', methods=["POST", "GET"])
def index():  # put application's code here
    #session.pop("user", None)
    if 'user' in session:
        return redirect(url_for('user'))
    else:
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
        nearEventsId = []
        nearEventsTitle = []
        nearEventsSDate = []
        nearEventsEDate = []
        nearEventsDetails = []
        nearEventsState = []

        locEvents = db.getEventsByLoc(cursor, str("IL"))
        for tEvent in locEvents:
            nearEventsId.append(tEvent[0])
            nearEventsTitle.append(tEvent[1])
            nearEventsSDate.append(tEvent[2])
            nearEventsEDate.append(tEvent[3])
            nearEventsDetails.append(tEvent[6])
            nearEventsState.append(tEvent[12])

    #END ALL LOCATION EVENTS----------------------------------------------
        search = None
        if request.method == "POST":
            search = request.form["searchbar"]
            # DO A SEARCH IDK HOW YET


        return render_template("index.html", popEventsTitle=popEventsTitle, popEventsDetails=popEventsDetails,
                               popEventsId=popEventsId, nearEventsTitle=nearEventsTitle,
                               nearEventsDetails=nearEventsDetails, nearEventsId=nearEventsId, search=search)

########################################################################--REGISTER PAGE--############
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
        userState = request.form.get("state")
        userZipcode = 123456
        userEmail = request.form["email"]
        userNumber = request.form["phone"]

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
            if 'user' in session:
                logedIn = True
            else:
                logedIn = False
            return render_template("registerPage.html", logedIn = logedIn)
#^END NEW USER^------------------------------------------------------^
        
        if 'submit' in request.form:
            # PUSH THE DATA TO THE DATABASE!!!!!!!!!
            return redirect(url_for("loginPage"))  # ????
    else:
        if 'user' in session:
            logedIn = True
        else:
            logedIn = False
        return render_template("registerPage.html", logedIn = logedIn)

########################################################################--LOG IN PAGE--############
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
            if 'user' in session:
                logedIn = True
            else:
                logedIn = False
            return render_template("loginPage.html", logedIn = logedIn)
            
#^END GET USER^-----------------------------------------------^
    else:
        if 'user' in session:
            logedIn = True
        else:
            logedIn = False
        return render_template("loginPage.html", logedIn = logedIn)

########################################################################--INDEX_USER LOGGED IN--############
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
        atEventsId = []
        atEventsTitle = []  # FILL WITH USERES EVENTS
        atEventsSDate = []  # FILL WITH 6 popular EVENTS
        atEventsEDate = []  # FILL WITH 6 NEAR BY EVENTS
        atEventsState = []
        
        
        #get user_events by userId
        userEvents = db.getUEventsByUser(cursor, str(userId))

        #for all user_events, get the event
        for tupleEvent in userEvents:
            evInfo = db.getEventsByEId(cursor, str(tupleEvent[2]))

            #add each section to list
            atEventsId.append(evInfo[0])
            atEventsTitle.append(evInfo[1])
            atEventsSDate.append(evInfo[2]) 
            atEventsEDate.append(evInfo[3])
            atEventsState.append(evInfo[12])


#END ALL USER EVENTS ATTENDING----------------------------------------    
#GET ALL USER EVENTS ADMINISTRATING----------------------------------
        adEventsId = []
        adEventsTitle = []
        adEventsSDate = []
        adEventsEDate = []
        adEventsState = []
        
        adminEvents = db.getEventsByUser(cursor, str(userId))
        for tupleEvent2 in adminEvents:
            adEventsId.append(tupleEvent2[0])
            adEventsTitle.append(tupleEvent2[1])
            adEventsSDate.append(tupleEvent2[2])
            adEventsEDate.append(tupleEvent2[3])
            adEventsState.append(tupleEvent2[12])
            
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

        if request.method == "POST":
            if "clicked" in request.form:
                eventID = request.form["eventID"]
                return  redirect(url_for("eventDetails", eventID = eventID))
            elif 'searchbar' in request.form:
                search = request.form["searchbar"]
                # DO A SEARCH
        else:
            return render_template("index_userLoggedIn.html", name=user,
                                   atEventsTitle=atEventsTitle, atEventsSDate=atEventsSDate, atEventsEDate=atEventsEDate, atEventsId=atEventsId,
                                   adEventsTitle=adEventsTitle, adEventsSDate=adEventsSDate, adEventsEDate=adEventsEDate, adEventsId=adEventsId,
                                   popEventsTitle=popEventsTitle, popEventsDetails=popEventsDetails,popEventsId=popEventsId,
                                   nearEventsTitle=locEventsTitle, nearEventsDetails=locEventsDetails, nearEventsId=locEventsId, search=search)

    else:
        return redirect(url_for("loginPage"))  # ????


# This is for a logout page that might be made
@app.route("/logout")
def logout():
    session.pop("user", None)
    # flash("You have been logged out!", "info")
    return redirect(url_for("loginPage"))  # ????

########################################################################--EVENT DETAILS--############
@app.route('/eventDetails.html', methods=["POST", "GET"])
@app.route('/eventDetails', methods=["POST", "GET"])
def eventDetails():  # put application's code here

    eventId = request.form.get("eventId")
    print(eventId)
#GET ALL EVENT INFO------------------------------------------------------------
    #check if event found by eventId
    if (db.checkAny(cursor, "eventId", "events", "eventId", str(eventId),
            "eventId", str(eventId)) == True):
        #get all variables in event
            event = db.getEventsByEId(cursor, str(eventId))
            eventId= event[0]
            eventTitle= event[1]
            eventStartDate= event[2]
            eventEndDate= event[3]
            eventDeadline= event[4]
            eventPrice= event[5]
            eventDescription= event[6]
            eventCap= event[7]
            eventOcp= event[8]
            eventITag= event[9]
            eventAddress= event[10]
            eventCity= event[11]
            eventState= event[12]
            eventZip= event[13]
    else:
        #otherwise send back to search
        if 'user' in session:
            logedIn = True
        else:
            logedIn = False
        return redirect(url_for('search_browseEvents', logedIn=logedIn))
    

#END ALL EVENT INFO------------------------------------------------------------

    if "attend" in request.form and request.method == "POST":
        if "user" in session:

            #get all info you need
            userId = session["userId"]
            user = session["user"]
            email = session["userEmail"]
            paid = 1
            seat = "O0"
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
                
                return redirect(url_for("user"))
            else:
                #give error(filled or user already signed up)
                print("ERROR: event filled or already signed up")
                if 'user' in session:
                    logedIn = True
                else:
                    logedIn = False
                return render_template("eventDetails.html", eventStartDate=eventStartDate, eventEndDate=eventEndDate,
                                       eventTitle=eventTitle, eventPrice=eventPrice, eventDescription=eventDescription,
                                       eventAddress=eventAddress, eventITag=eventITag, logedIn=logedIn)
# END ADD USER FROM ATTENDING EVENT--------------------------
            return redirect(url_for("index_userLoggedIn"))
        else:
            return redirect(url_for("loginPage"))

    if 'user' in session:
        logedIn = True
    else:
        logedIn = False
    return render_template("eventDetails.html", eventStartDate=eventStartDate, eventEndDate=eventEndDate,
                           eventTitle=eventTitle, eventPrice=eventPrice, eventDescription=eventDescription,
                           eventAddress=eventAddress, eventITag=eventITag, logedIn = logedIn)


########################################################################--MANAGE EVENTS--############
@app.route('/manageEvents.html', methods=["POST", "GET"])
@app.route('/manageEvents', methods=["POST", "GET"])
def manageEvents():  # put application's code here
    if "user" in session:
        logedIn = True
        user = session["user"]
        userId = session["userId"]
#GET ALL USER EVENTS ATTENDING-------------------------------
        atEventsId = []
        atEventsTitle = []  
        atEventsSDate = []  
        atEventsEDate = []  
        atEventsCap = []
        atEventsOcp = []

        #get user_events by userId
        userEvents = db.getUEventsByUser(cursor, str(userId))
        eventRangeAttend = len(userEvents)

        #for all user_events, get the event
        for tupleEvent in userEvents:
            evInfo = db.getEventsByEId(cursor, str(tupleEvent[2]))

            #add each section to list
            atEventsId.append(evInfo[0])
            atEventsTitle.append(evInfo[1])
            atEventsSDate.append(evInfo[2]) 
            atEventsEDate.append(evInfo[3])
            atEventsCap.append(evInfo[7])
            atEventsOcp.append(evInfo[8])


#END ALL USER EVENTS ATTENDING----------------------------------------    
#GET ALL USER EVENTS ADMINISTRATING----------------------------------
        adEventsId = []
        adEventsTitle = []
        adEventsSDate = []
        adEventsEDate = []
        adEventsCap = []
        adEventsOcp = []
        
        adminEvents = db.getEventsByUser(cursor, str(userId))
        eventRangeAdmin = len(adminEvents)
        for tupleE2 in adminEvents:
            adEventsId.append(tupleE2[0])
            adEventsTitle.append(tupleE2[1])
            adEventsSDate.append(tupleE2[2])
            adEventsEDate.append(tupleE2[3])
            adEventsCap.append(tupleE2[7])
            adEventsOcp.append(tupleE2[8])

            
#END ALL USER EVENTS ADMINISTRATING----------------------------------

        if 'leaveEvent' in request.form and request.method == "POST":
            user = session["user"]
            userId = session["userId"]
            
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

                if 'user' in session:
                    logedIn = True
                else:
                    logedIn = False

                return render_template("manageEvents.html",
                                       userAttendingEvents=atEventsTitle, atEventsSDate=atEventsSDate,
                                       atEventsEDate=atEventsEDate, atEventsId=atEventsId,
                                       atEventsCap=atEventsCap, atEventsOcp=atEventsOcp,
                                       usersEvents=adEventsTitle, adEventsSDate=adEventsSDate,
                                       adEventsEDate=adEventsEDate, adEventsId=adEventsId,
                                       eventsMaxPop=adEventsCap, adEventsOcp=adEventsOcp, logedIn= logedIn)
            
#END REMOVE USER FROM ATTENDING EVENT------------------------------------
        return render_template("manageEvents.html",
                               userAttendingEvents=atEventsTitle, atEventsSDate=atEventsSDate,
                               atEventsEDate=atEventsEDate, atEventsId=atEventsId,
                               atEventsCap=atEventsCap, atEventsOcp=atEventsOcp,
                               usersEvents=adEventsTitle, adEventsSDate=adEventsSDate,
                               adEventsEDate=adEventsEDate, adEventsId=adEventsId,
                               eventsMaxPop=adEventsCap, adEventsOcp=adEventsOcp, logedIn=logedIn, eventRange=eventRangeAttend,
                               eventRangeAdmin=eventRangeAdmin)

    else:
        return redirect(url_for("login"))  # ????

########################################################################--SEARCH_BROWSE EVENTS--############
@app.route('/search_browseEvents.html', methods=["POST", "GET"])
@app.route('/search_browseEvents', methods=["POST", "GET"])
def search_browseEvents():  # put application's code here
    eventTitle = []
    eventStartDate = []
    eventEndDate = []
    eventAddress = []
    eventPrice = []
    eventTime = []
    eventCapacity = []
    eventOccupants = []
    events = []  # fill the info
    eventDates = []
    eventTimes = []
    eventLocations = []
    eventPrices = []
    eventImage = []
    #eventPopulation = []
    #eventMaxPop = []

#SEARCH BY KEYWORD----------------------------------#needs an indication
    

#SEARCH BY KEYWORD----------------------------------
#SEARCH BY EVENT TAGS------------------------------#needs an indication
    tagName = "7"       #needs input from html
    tagEventsId = []
    tagEventsTitle = []  
    tagEventsSDate = []  
    tagEventsEDate = [] 
    tagEventsState = []
    
    
    #get user_events by userId
    # tagEvents = db.getEventTagByTagId(cursor, str(tagName))
    tagEvents = db.getEvents(cursor)
    eventRange = len(tagEvents)


    #for all user_events, get the event
    for tgEvent in tagEvents:
        # evInfo = db.getEventsByEId(cursor, str(tgEvent))
        evInfo = tgEvent


        if evInfo is not None:
            #add each section to list
            eventTitle.append(evInfo[1])
            eventStartDate.append(evInfo[2])
            eventEndDate.append(evInfo[3])
            eventTime.append(evInfo[4])
            eventPrice.append(evInfo[5])
            eventCapacity.append(evInfo[7])
            eventOccupants.append(evInfo[8])
            eventAddress.append(evInfo[10])

            tagEventsId.append(evInfo[0])
            tagEventsTitle.append(evInfo[1])
            tagEventsSDate.append(evInfo[2]) 
            tagEventsEDate.append(evInfo[3])
            tagEventsState.append(evInfo[12])
#END SEARCH BY EVENT TAGS-------------------------
    if request.method == "POST":
        search = request.form["searchbar"]
        # DO A SEARCH
    else:
        if 'user' in session:
            logedIn = True
        else:
            logedIn = False
        return render_template("search_browseEvents.html", events=events, eventDates=eventDates, eventTimes=eventTimes,
                               eventLocations=eventLocations, eventPrices=eventPrices, eventImage=eventImage, eventTitle=eventTitle,
                               eventStartDate=eventStartDate, eventEndDate=eventEndDate, eventAddress=eventAddress, eventPrice=eventPrice,
                               eventTime=eventTime, eventOccupants=eventOccupants, eventCapacity=eventCapacity, eventRange=eventRange, logedIn=logedIn)


###########################################################--EDIT EVENT--########################################
@app.route('/editEvent.html', methods=["POST", "GET"])
@app.route('/editEvent', methods=["POST", "GET"])
def editEvent():
    if 'user' in session:
        logedIn = True
        eventId = request.form.get("eventId")
        #eventId = 27
        userId = session["userId"]

        userToAdd = []
        userToDelete = []
    
        userId = session["userId"]
        
# GET EVENT----------------------------------------------------------------^
        #check if event found by eventId
        if (db.checkAny(cursor, "eventId", "events", "eventId", str(eventId),
                "userId", str(userId)) == True):
            #get all variables in event
            event = db.getEventsByEId(cursor, str(eventId))

            eventTitle = event[1]
            eventStartDate = event[2]
            eventEndDate = event[3]
            eventDeadline = event[4]
            eventPrice = event[5]
            eventDes = event[6]
            eventCap = event[7]
            eventOcp = event[8]
            eventITag = event[9]
            eventAddress = event[10]
            eventCity = event[11]
            eventState = event[12]
            eventZip = event[13]
            eventUId = event[14]
            eventDeadlineTime = 0

#GET ALL ATTENDING EVENT--------------------------------------
            usersId = []
            usersName = []
            usersEmail = []
            
            #get user_events by userId
            eventUsers = db.getUEventsByEvent(cursor, str(eventId))

            #for all user_events, get the event
            for tupleEvent in eventUsers:

                #add each section to list
                usersId.append(tupleEvent[1])
                usersName.append(tupleEvent[3])
                usersEmail.append(tupleEvent[4])
                
#END GET ALL ATTENDING EVENT--------------------------------------
              
        else:
            #otherwise send back to search
            print("You are not authorized to edit event")
            return redirect(url_for('index'))
# END GET EVENT-------------------------------------------------------------^
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

        if "saveEvent" in request.form and request.method == "POST":
            return f"{eventId}"


    #NEED USER TO DELETE BUTTON--------------------------------------------------*****(Not sure how to go about it)
    #NEED USER TO DELETE BUTTON--------------------------------------------------*****
        else:
            return render_template("editEvent.html", eventTitle=eventTitle,
                                   eventStartDate=eventStartDate, eventEndDate=eventEndDate,eventDeadline=eventDeadline,
                                   eventPrice=eventPrice, eventDes=eventDes, eventCap=eventCap,
                                   eventITag=eventITag, eventAddress=eventAddress, eventCity=eventCity,
                                   eventState=eventState, eventZip=eventZip,
                                   eventDeadlineTime=eventDeadlineTime, userToAdd=userToAdd, userToDelete=userToDelete,
                                   logedIn=logedIn,
                                   popEventsId = popEventsId, popEventsTitle = popEventsTitle,
                                   popEventsSDate= popEventsSDate, popEventsEDate=popEventsEDate,
                                   popEventsDetails= popEventsDetails,
                                   popEventsState = popEventsState)

    else:
        logedIn = False
        redirect(url_for('loginPage', logedIn=logedIn))
        




#########################################################################################################
@app.route('/createEvent.html', methods=["POST", "GET"])
@app.route('/createEvent.html', methods=["POST", "GET"])
def createEvent():
    if 'user' in session:
        if request.method == "POST":
            eventTitle = request.form["title"]
            eventAddress = request.form["address"]
            eventCity = request.form["city"]
            eventState = request.form.get("eventState")
            eventZip = request.form["zip"]
            eventStartDate = request.form["startDate"]
            eventStartTime = request.form["endTime"]
            eventEndDate = request.form["endDate"]
            eventEndTime = request.form["endTime"]
            eventPrice = request.form["price"]
            eventCap = request.form["maxCapacity"]
            eventDeadline = request.form["deadlineDate"]
            eventDeadlineTime = request.form["deadlineTime"]
            eventITag = request.form.get("eventTag")
            eventDes = request.form["description"]
            #userToAdd = request.form["addUser"]
            #userToDelete = request.form["deleteUser"]
            eventOcp = 0
            eventPoP = 0
            userId = session["userId"]
#NEW EVENT--------------------------------------------------------------^
            #turn to string
            cE = getInputString([eventTitle, eventStartDate, eventEndDate, eventDeadline, eventPrice, eventDes, eventCap,
                                 eventOcp, eventITag, eventAddress, eventCity, eventState, eventZip, userId])
            #check if already exists: if not, create new
            if (db.checkAny(cursor, "eventId", "events", "name", str(eventTitle)
                            , "userId", str(userId)) == False):
                
                rt = db.newEvent(cnx, cursor, cE)
                return redirect(url_for("user"))
            else:
                print("ERROR: event already created by you")
                if 'user' in session:
                    logedIn = True
                else:
                    logedIn = False
                return render_template("create_editEvents.html", logedIn = logedIn) #THIS PAGE DOES NOT EXSIT AND THIS NEEDS AND UPDATE
#END NEW EVENT--------------------------------------------------------------^
            return redirect(url_for("index_userLoggedIn"))
        else:
            return render_template("createEvent.html")
    else:
        redirect(url_for("loginPage"))
############################################################################UPDATE USER#######################
@app.route('/updatePersonalInfo.html', methods=["POST", "GET"])
@app.route('/updatePersonalInfo', methods=["POST", "GET"])
def updatePersonalInfo():
    if 'user' in session:
        user = session["user"]
        userId = session["userId"]
#^GET USER^-------------------------------------------------------------^   
        #: check if user found, then get user info into variables
        if (db.checkAny(cursor, "userId", "users", "username", str(user),
            "userId", str(userId)) == True):
            password = "password"                       #NEED TO GET PASSWORD(SESSION or LOGIN)
            [uId, user, passwordId, uFN, uLN, uEmail,
             uAd, uZip, uCity, uState,
             uPhone] = db.getUser(cursor, str(user), str(password)) 
            
        else:
            print("Error: The username does not match the userId")
            if 'user' in session:
                logedIn = True
            else:
                logedIn = False
            return render_template("index_userLoggedIn.html", logedIn=logedIn)
            
#^END GET USER^-----------------------------------------------^
        if request.method == "POST":
            firstName = request.form["fn"]
            lastName = request.form["ln"]
            username = request.form["nm"]
            #oldPassword = request.form["Opw"]&
            password = request.form["pw"]
            address = request.form["address"]
            city = request.form["city"]
            state = request.form["state"] #request.form.get("state")&
            #zipcode = request.form["zipcode"]&
            zipcode = "12345"
            email = request.form["email"]
            phone = request.form["phone"]
            
# UPDATE USER---------------------------------------------- ******NEEDS WORK*******
            eU =[username, password, firstName, lastName, email, address, zipcode, city, state, phone]
            #update user
            rt = db.updateUser(cnx, cursor, userId, passwordId, eU)
            return redirect(url_for("user"))
#END UPDATE USER-------------------------------------------
# NEED BUTTON TO REMOVE USER---------------------------------------****
        if 'remove' in request.form:

            userRemove(cnx, cursor, userId, passwordId)
            return redirect(url_for("index.html"))
# NEED BUTTON TO REMOVE USER---------------------------------------****)
        else:
            firstName = uFN
            lastName = uLN
            username = user
            password = passwordId
            address = uAd
            city = uCity
            state = uState
            zipcode = uZip
            email = uEmail
            phone = uPhone
            if 'user' in session:
                logedIn = True
            else:
                logedIn = False
            return render_template("updatePersonalInfo.html", firstName=firstName, lastName=lastName, username=username, password=
                                   password, address=address, city=city, state=state, email=email, phone=phone, logedIn=logedIn)
    else:
        redirect(url_for("loginPage"))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port="3000")
