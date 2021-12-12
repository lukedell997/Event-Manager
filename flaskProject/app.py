from flask import Flask, render_template, redirect, url_for, request, flash, session
from datetime import timedelta
from databaseCode import DataB

app = Flask(__name__)

#app.permanent_session_lifetime = timedelta(minutes=1)

app.secret_key = "This is a super duper secret key 431321"


# This is for a logout page that might be made
@app.route("/logout", methods=["POST", "GET"])
@app.route("/logout.html", methods=["POST", "GET"])
def logout():
    session.clear()
    print("YOU HAVE LOGGED OUT. NICE!!!!!")
    # flash("You have been logged out!", "info")
    return redirect(url_for("index"))  # ????
try:
    db = DataB()
    cnx, cursor = db.openDatabase()


    def imageReturn(imageNumber):

        if imageNumber == 1:
            pic = 'img/concertEvent.jpg'
        elif imageNumber == 2:
            pic = 'img/conferenceEvent.jpg'
        elif imageNumber == 3:
            pic = 'img/dinnerEvent.jpg'
        elif imageNumber == 4:
            pic = 'img/festivalEvent.jpg'
        elif imageNumber == 5:
            pic = 'img/movieEvents.jpg'
        else:
            pic = 'img/basicEventPicture.jpg'

        return pic

    def getInputString(ItemList):
        try:
            # for all items in input, add ' data '
            info = ""
            for i in range(len(ItemList)):
                if ItemList[i] == "" or ItemList[i] == "None":
                    info += "'None'"
                else:
                    info += "'"
                    info += str(ItemList[i])
                    info += "'"

                # add comma unless last item
                if (i != len(ItemList) - 1):
                    info += ","
                else:
                    return info
            return info
        except:
            return -99


    ########################################################################--INDEX--############
    @app.route('/index', methods=["POST", "GET"])
    @app.route('/', methods=["POST", "GET"])
    @app.route('/index.html', methods=["POST", "GET"])
    def index():  # put application's code here
        # session.pop("user", None)
        if 'user' in session:
            return redirect(url_for('user'))
        else:
            popEventsTitle = []
            popEventsDetails = []
            popEventsButton = []

            nearEventsTitle = []
            nearEventsDetails = []
            nearEventsButton = []
            # GET ALL POPULAR EVENTS----------------------------------------------
            popEventsId = []
            popEventsTitle = []
            popEventsSDate = []
            popEventsEDate = []
            popEventsDetails = []
            popEventsState = []
            popEventsItag = []

            popEvents = db.getEventsByPop(cursor)
            popEventRange = 0
            for tupleEvent3 in popEvents:
                popEventsId.append(tupleEvent3[0])
                popEventsTitle.append(tupleEvent3[1])
                popEventsSDate.append(tupleEvent3[2])
                popEventsEDate.append(tupleEvent3[3])
                popEventsDetails.append(tupleEvent3[6])
                popEventsItag.append(imageReturn(tupleEvent3[9]))
                popEventsState.append(tupleEvent3[12])
                popEventRange += 1

            # END ALL POPULAR EVENTS----------------------------------------------
            # GET ALL LOCATION EVENTS----------------------------------------------
            nearEventsId = []
            nearEventsTitle = []
            nearEventsSDate = []
            nearEventsEDate = []
            nearEventsDetails = []
            nearEventsState = []
            nearEventsItag = []

            locEvents = db.getEventsByUpcoming(cursor)
            locEventRange = 0
            for tEvent in locEvents:
                nearEventsId.append(tEvent[0])
                nearEventsTitle.append(tEvent[1])
                nearEventsSDate.append(tEvent[2])
                nearEventsEDate.append(tEvent[3])
                nearEventsDetails.append(tEvent[6])
                nearEventsItag.append(imageReturn(tEvent[9]))
                nearEventsState.append(tEvent[12])
                locEventRange += 1

            # END ALL LOCATION EVENTS----------------------------------------------

            return render_template("index.html", popEventsTitle=popEventsTitle, popEventsDetails=popEventsDetails,
                                   popEventsId=popEventsId, nearEventsTitle=nearEventsTitle,
                                   nearEventsDetails=nearEventsDetails, nearEventsId=nearEventsId,
                                   popEventRange=popEventRange, locEventRange=locEventRange, nearEventsItag=nearEventsItag, popEventsItag=popEventsItag)


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
            # turn to string
            cU = getInputString([userUsername, userPassword, userFirstName,
                                 userLastName, userEmail, userAddress,
                                 userZipcode, userCity, userState, userNumber])
            # check if already exists: if not, create new
            if (db.checkAny(cursor, "userId", "users", "username", str(userUsername)
                    , "username", str(userUsername)) == False):
                # print(test)
                db.newUser(cnx, cursor, cU)
                return redirect(url_for("loginPage"))
            else:
                print("ERROR: username already exists")
                if 'user' in session:
                    logedIn = True
                else:
                    logedIn = False
                return render_template("registerPage.html", logedIn=logedIn)
            # ^END NEW USER^------------------------------------------------------^

            if 'submit' in request.form:
                # PUSH THE DATA TO THE DATABASE!!!!!!!!!
                return redirect(url_for("loginPage"))  # ????
        else:
            if 'user' in session:
                logedIn = True
            else:
                logedIn = False
            return render_template("registerPage.html", logedIn=logedIn)


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
            # ^GET USER^-------------------------------------------------------------^
            #: check if user found, then get user info into variables
            if (db.checkAny(cursor, "userId", "users", "username", str(user),
                            "passwordId", str(password)) == True):

                [uId, user, password, uFN, uLN, uEmail,
                 uAd, uZip, uCity, uState,
                 uPhone] = db.getUser(cursor, str(user), str(password))

                # put user info into session...
                session["userId"] = uId
                session["userEmail"] = uEmail
                session["userState"] = uState
                # session["nm"] = user
                return redirect(url_for("user"))

            else:
                print("Error: The username or password is incorrect")
                return render_template("loginPage.html")

        # ^END GET USER^-----------------------------------------------^
        else:
            return render_template("loginPage.html")


    ########################################################################--INDEX_USER LOGGED IN--############
    @app.route("/index_userLoggedIn.html", methods=["POST", "GET"])
    @app.route("/index_userLoggedIn", methods=["POST", "GET"])
    def user():
        if "user" in session:
            logedIn = True
            search = None

            user = session["user"]
            userId = session["userId"]
            userLoc = session["userState"]

            # GET ALL USER EVENTS ATTENDING------------------------------- NEEDS UPDATING
            atEventsId = []
            atEventsTitle = []  # FILL WITH USERES EVENTS
            atEventsSDate = []  # FILL WITH 6 popular EVENTS
            atEventsEDate = []  # FILL WITH 6 NEAR BY EVENTS
            atEventsState = []
            atEventsRange = 0

            # get user_events by userId
            userEvents = db.getUEventsByUser(cursor, str(userId))

            # for all user_events, get the event
            for tupleEvent in userEvents:
                evInfo = db.getEventsByEId(cursor, str(tupleEvent[2]))

                # add each section to list
                atEventsId.append(evInfo[0])
                atEventsTitle.append(evInfo[1])
                atEventsSDate.append(evInfo[2])
                atEventsEDate.append(evInfo[3])
                atEventsState.append(evInfo[12])
                atEventsRange += 1

            # END ALL USER EVENTS ATTENDING----------------------------------------
            # GET ALL USER EVENTS ADMINISTRATING----------------------------------
            adEventsId = []
            adEventsTitle = []
            adEventsSDate = []
            adEventsEDate = []
            adEventsState = []
            adEventsItag = []
            adEventsRange = 0

            adminEvents = db.getEventsByUser(cursor, str(userId))
            for tupleEvent2 in adminEvents:
                adEventsId.append(tupleEvent2[0])
                adEventsTitle.append(tupleEvent2[1])
                adEventsSDate.append(tupleEvent2[2])
                adEventsEDate.append(tupleEvent2[3])
                adEventsItag.append(imageReturn(tupleEvent2[9]))
                adEventsState.append(tupleEvent2[12])
                adEventsRange += 1

            # END ALL USER EVENTS ADMINISTRATING----------------------------------
            # GET ALL POPULAR EVENTS----------------------------------------------
            popEventsId = []
            popEventsTitle = []
            popEventsSDate = []
            popEventsEDate = []
            popEventsDetails = []
            popEventsState = []
            popEventsItag = []
            popEventRange = 0

            popEvents = db.getEventsByPop(cursor)

            for tupleEvent3 in popEvents:
                popEventsId.append(tupleEvent3[0])
                popEventsTitle.append(tupleEvent3[1])
                popEventsSDate.append(tupleEvent3[2])
                popEventsEDate.append(tupleEvent3[3])
                popEventsDetails.append(tupleEvent3[6])
                popEventsItag.append(imageReturn(tupleEvent3[9]))
                popEventsState.append(tupleEvent3[12])
                popEventRange += 1

            # END ALL POPULAR EVENTS----------------------------------------------
            # GET ALL LOCATION EVENTS----------------------------------------------
            locEventsId = []
            locEventsTitle = []
            locEventsSDate = []
            locEventsEDate = []
            locEventsDetails = []
            locEventsState = []
            locEventsItag = []
            locEventRange = 0

            locEvents = db.getEventsByLoc(cursor, str(userLoc))
            for tEvent in locEvents:
                locEventsId.append(tEvent[0])
                locEventsTitle.append(tEvent[1])
                locEventsSDate.append(tEvent[2])
                locEventsEDate.append(tEvent[3])
                locEventsItag.append(imageReturn([tEvent[9]]))
                locEventsDetails.append(tEvent[6])

                locEventsState.append(tEvent[12])
                locEventRange += 1
            # END ALL LOCATION EVENTS----------------------------------------------

            if request.method == "POST":
                if "clicked" in request.form:
                    eventID = request.form["eventID"]
                    return redirect(url_for("eventDetails", eventID=eventID))
                elif 'searchbar' in request.form:
                    search = request.form["searchbar"]
                    # DO A SEARCH
            else:
                return render_template("index_userLoggedIn.html", name=user,
                                       atEventsTitle=atEventsTitle, atEventsSDate=atEventsSDate,
                                       atEventsEDate=atEventsEDate, atEventsId=atEventsId,
                                       adEventsTitle=adEventsTitle, adEventsSDate=adEventsSDate,
                                       adEventsEDate=adEventsEDate, adEventsId=adEventsId,
                                       popEventsTitle=popEventsTitle,
                                       popEventsDetails=popEventsDetails, popEventsId=popEventsId,
                                       nearEventsTitle=locEventsTitle,
                                       nearEventsDetails=locEventsDetails, nearEventsId=locEventsId,
                                       adEventRange=adEventsRange, atEventRange=atEventsRange,
                                       search=search, popEventRange=popEventRange, locEventRange=locEventRange,
                                       popEventsItag=popEventsItag,nearEventsItag=locEventsItag,adEventsItag=adEventsItag )

        else:
            logedIn = False
            return redirect(url_for("loginPage"))  # ????





    ########################################################################--EVENT DETAILS--############
    @app.route('/eventDetails.html', methods=["POST", "GET"])
    @app.route('/eventDetails', methods=["POST", "GET"])
    def eventDetails():  # put application's code here
        if "user" in session:
            logedIn = True
        else:
            logedIn = False

        # GET ALL POPULAR EVENTS----------------------------------------------
        popEventsId = []
        popEventsTitle = []
        popEventsSDate = []
        popEventsEDate = []
        popEventsDetails = []
        popEventsState = []
        popEventsItag = []
        popEventRange = 0

        popEvents = db.getEventsByPop(cursor)
        for tupleEvent3 in popEvents:
            popEventsId.append(tupleEvent3[0])
            popEventsTitle.append(tupleEvent3[1])
            popEventsSDate.append(tupleEvent3[2])
            popEventsEDate.append(tupleEvent3[3])
            popEventsDetails.append(tupleEvent3[6])
            popEventsDetails.append(tupleEvent3[6])
            popEventsItag.append(imageReturn(tupleEvent3[6]))
            popEventsState.append(tupleEvent3[12])
            popEventRange += 1

        # END ALL POPULAR EVENTS----------------------------------------------

        eventId = request.form.get("eventId")

        # GET ALL EVENT INFO------------------------------------------------------------
        # check if event found by eventId
        if (db.checkAny(cursor, "eventId", "events", "eventId", str(eventId),
                        "eventId", str(eventId)) == True):
            # get all variables in event
            event = db.getEventsByEId(cursor, str(eventId))
            eventId = event[0]
            eventTitle = event[1]
            eventStartDate = event[2]
            eventEndDate = event[3]
            eventDeadline = event[4]
            eventPrice = event[5]
            eventDescription = event[6]
            eventCap = event[7]
            eventOcp = event[8]
            eventITag = imageReturn(event[9])
            eventAddress = event[10]
            eventCity = event[11]
            eventState = event[12]
            eventZip = event[13]
        else:
            print("Problem finding event in server")
            return redirect(url_for("index"))
        # END ALL EVENT INFO------------------------------------------------------------

        if request.method == "POST":

            if "attend" in request.form:

                # ADD USER FROM ATTENDING EVENT--------------------------
                # get all info you need
                userId = session["userId"]
                user = session["user"]
                email = session["userEmail"]
                paid = 1
                seat = "O0"
                price = eventPrice
                atEventId = request.form["eventId"]

                # if free, user has paid
                if (price != 0):
                    paid = 0

                # turn to string
                cUE = getInputString([userId, eventId, user, email, paid, seat, price])

                # check if not already exists: AND if not full
                if (db.checkAny(cursor, "attendantId", "user_events", "userId",
                                str(userId), "eventId", str(atEventId)) == False
                        and db.checkAvl(cursor, str(eventId)) == True):

                    # create new user events
                    db.newUEvents(cnx, cursor, cUE)

                    # add occupant to event
                    rt = db.addEventOcp(cnx, cursor, eventId, eventOcp)

                    return redirect(url_for("user"))
                else:
                    print("Event Filled or you are already attending")
                    return redirect(url_for("eventDetails"))

            # END ADD USER FROM ATTENDING EVENT--------------------------
            elif "attendPayinfo" in request.form:
                # ADD USER FROM ATTENDING EVENT--------------------------
                # get all info you need
                userId = session["userId"]
                user = session["user"]
                email = session["userEmail"]
                paid = 1
                seat = "O0"
                price = eventPrice
                atEventId = request.form["eventId"]
                creditCardNum = request.form["creditCardNum"]
                csv = request.form["csv"]
                expiration = request.form["expiration"]
                billAdd = request.form["billAdd"]
                cardName = request.form["cardName"]

                print("AND AGAIN: ", creditCardNum, csv, expiration, billAdd, cardName)
                # if free, user has paid
                if (price != 0):
                    paid = 0

                # turn to string
                cUE = getInputString([userId, eventId, user, email, paid, seat, price])

                # check if not already exists: AND if not full
                if (db.checkAny(cursor, "attendantId", "user_events", "userId",
                                str(userId), "eventId", str(atEventId)) == False
                        and db.checkAvl(cursor, str(eventId)) == True):

                    # create new user events
                    db.newUEvents(cnx, cursor, cUE)

                    # add occupant to event
                    rt = db.addEventOcp(cnx, cursor, eventId, eventOcp)

                    return redirect(url_for("user"))
                else:
                    print("Event Filled or you are already attending")
                    return redirect(url_for("eventDetails"))

            else:
                # give error(filled or user already signed up)
                print("ERROR: event filled or already signed up")
                return render_template("eventDetails.html", eventStartDate=eventStartDate, eventEndDate=eventEndDate,
                                       eventTitle=eventTitle, eventPrice=eventPrice, eventDescription=eventDescription,
                                       eventAddress=eventAddress, eventITag=eventITag,
                                       eventCity=eventCity, eventZip=eventZip, eventState=eventState,
                                       eventCap=eventOcp, eventMaxPop=eventCap,
                                       logedIn=logedIn, eventId=eventId, popEventsId=popEventsId,
                                       popEventsTitle=popEventsTitle,
                                       popEventsSDate=popEventsSDate, popEventsDetails=popEventsDetails,
                                       popEventsState=popEventsState, popEventRange=popEventRange, popEventsItag=popEventsItag)
        # END POST
        else:
            return render_template("eventDetails.html", eventStartDate=eventStartDate, eventEndDate=eventEndDate,
                                   eventTitle=eventTitle, eventPrice=eventPrice, eventDescription=eventDescription,
                                   eventAddress=eventAddress, eventITag=eventITag,
                                   eventCity=eventCity, eventZip=eventZip, eventState=eventState,
                                   eventCap=eventOcp, eventMaxPop=eventCap,
                                   logedIn=logedIn, eventId=eventId, popEventsId=popEventsId, popEventsTitle=popEventsTitle,
                                   popEventsSDate=popEventsSDate, popEventsDetails=popEventsDetails,
                                   popEventsState=popEventsState, popEventRange=popEventRange, popEventsItag=popEventsItag)


    ########################################################################--MANAGE EVENTS--############
    @app.route('/manageEvents.html', methods=["POST", "GET"])
    @app.route('/manageEvents', methods=["POST", "GET"])
    def manageEvents():  # put application's code here
        if "user" in session:
            logedIn = True
            user = session["user"]
            userId = session["userId"]
            eventId = request.form.get("eventId")
            # GET ALL USER EVENTS ATTENDING-------------------------------
            atEventsId = []
            atEventsTitle = []
            atEventsSDate = []
            atEventsEDate = []
            atEventsDDate = []
            atEventsCap = []
            atEventsOcp = []
            atEventsItag = []

            # get user_events by userId
            userEvents = db.getUEventsByUser(cursor, str(userId))
            eventRangeAttend = len(userEvents)

            # for all user_events, get the event
            for tupleEvent in userEvents:
                evInfo = db.getEventsByEId(cursor, str(tupleEvent[2]))

                # add each section to list
                atEventsId.append(evInfo[0])
                atEventsTitle.append(evInfo[1])
                atEventsSDate.append(evInfo[2])
                atEventsEDate.append(evInfo[3])
                atEventsDDate.append(evInfo[4])
                atEventsCap.append(evInfo[7])
                atEventsOcp.append(evInfo[8])
                atEventsItag.append(imageReturn(evInfo[9]))

            # END ALL USER EVENTS ATTENDING----------------------------------------
            # GET ALL USER EVENTS ADMINISTRATING----------------------------------
            adEventsId = []
            adEventsTitle = []
            adEventsSDate = []
            adEventsEDate = []
            adEventsCap = []
            adEventsOcp = []
            adEventsItag = []

            adminEvents = db.getEventsByUser(cursor, str(userId))
            eventRangeAdmin = len(adminEvents)
            for tupleE2 in adminEvents:
                adEventsId.append(tupleE2[0])
                adEventsTitle.append(tupleE2[1])
                adEventsSDate.append(tupleE2[2])
                adEventsEDate.append(tupleE2[3])
                adEventsCap.append(tupleE2[7])
                adEventsOcp.append(tupleE2[8])
                adEventsItag.append(imageReturn(tupleE2[8]))

            # END ALL USER EVENTS ADMINISTRATING----------------------------------

            if request.method == "POST":

                user = session["user"]
                userId = session["userId"]
                leaveEventId = []
                print("This is the eventID: ", eventId)

                # REMOVE USER FROM ATTENDING EVENT------------------------------------
                if 'leaveEvent' in request.form:
                    leaveEventId = request.form.get("leaveEventId")
                    print("This is the leave eventID: ", leaveEventId)
                    print("TEST!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    # if user found with event
                    if (db.checkAny(cursor, "attendantId", "user_events", "userId",
                                    str(userId), "eventId", str(leaveEventId)) == True):

                        # remove user from event attendance
                        db.removeUEvents(cnx, cursor, userId, str(leaveEventId))
                        db.removeEventOcp(cnx, cursor, str(leaveEventId))

                        return redirect(url_for("manageEvents"))
                    else:
                        print("Attendant Not found for event")
                        return render_template("manageEvents.html", eventId=eventId,
                                               userAttendingEvents=atEventsTitle, atEventsSDate=atEventsSDate,
                                               atEventsEDate=atEventsEDate, atEventsId=atEventsId,
                                               atEventsDDate=atEventsDDate,
                                               atEventsCap=atEventsCap, atEventsOcp=atEventsOcp,
                                               usersEvents=adEventsTitle, adEventsSDate=adEventsSDate,
                                               adEventsEDate=adEventsEDate, adEventsId=adEventsId,
                                               eventsMaxPop=adEventsCap, adEventsOcp=adEventsOcp, logedIn=logedIn,
                                               eventRange=eventRangeAttend,
                                               eventRangeAdmin=eventRangeAdmin, adEventsItag= adEventsItag, atEventsItag=atEventsItag)

            # END REMOVE USER FROM ATTENDING EVENT------------------------------------
            else:
                return render_template("manageEvents.html", eventId=eventId,
                                       userAttendingEvents=atEventsTitle, atEventsSDate=atEventsSDate,
                                       atEventsEDate=atEventsEDate, atEventsId=atEventsId, atEventsDDate=atEventsDDate,
                                       atEventsCap=atEventsCap, atEventsOcp=atEventsOcp,
                                       usersEvents=adEventsTitle, adEventsSDate=adEventsSDate,
                                       adEventsEDate=adEventsEDate, adEventsId=adEventsId,
                                       eventsMaxPop=adEventsCap, adEventsOcp=adEventsOcp, logedIn=logedIn,
                                       eventRange=eventRangeAttend,
                                       eventRangeAdmin=eventRangeAdmin, adEventsItag= adEventsItag, atEventsItag=atEventsItag)

        else:
            logedIn = False
            return redirect(url_for("loginPage"))


    ########################################################################--SEARCH_BROWSE EVENTS--############
    @app.route('/search_browseEvents.html', methods=["POST", "GET"])
    @app.route('/search_browseEvents', methods=["POST", "GET"])
    def search_browseEvents():  # put application's code here
        eventId = []
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
        eventItag = []
        # eventPopulation = []
        # eventMaxPop = []

        # SEARCH BY KEYWORD----------------------------------#needs an indication
        if request.method == "POST":
            word = request.form["searchbar"]
            print(word)
            eventsK = db.getEventsAdvanced(cursor, str(word))
            eventRange = len(eventsK)

            for eK in eventsK:
                eventId.append(eK[0])
                eventTitle.append(eK[1])
                eventStartDate.append(eK[2])
                eventEndDate.append(eK[3])
                eventDates.append(eK[4])
                eventPrice.append(eK[5])
                eventCapacity.append(eK[7])
                eventOccupants.append(eK[8])
                eventItag.append(imageReturn(eK[9]))
                eventAddress.append(eK[10])
                eventLocations.append(eK[12])
                eventTime = []
                events = []
                eventTimes = []
                eventPrices = []


        # SEARCH BY KEYWORD----------------------------------
        else:
            # SEARCH BY EVENT TAGS------------------------------#needs an indication
            tagName = "7"  # needs input from html
            tagEventsId = []
            tagEventsTitle = []
            tagEventsSDate = []
            tagEventsEDate = []
            tagEventsState = []

            # get user_events by userId
            # tagEvents = db.getEventTagByTagId(cursor, str(tagName))
            tagEvents = db.getEvents(cursor)
            eventRange = len(tagEvents)

            # for all user_events, get the event
            for tgEvent in tagEvents:
                # evInfo = db.getEventsByEId(cursor, str(tgEvent))
                evInfo = tgEvent

                if evInfo is not None:
                    # add each section to list
                    eventId.append(evInfo[0])
                    eventTitle.append(evInfo[1])
                    eventStartDate.append(evInfo[2])
                    eventEndDate.append(evInfo[3])
                    eventTime.append(evInfo[4])
                    eventPrice.append(evInfo[5])
                    eventCapacity.append(evInfo[7])
                    eventItag.append(imageReturn(evInfo[9]))
                    eventOccupants.append(evInfo[8])
                    eventAddress.append(evInfo[10])

                    tagEventsId.append(evInfo[0])
                    tagEventsTitle.append(evInfo[1])
                    tagEventsSDate.append(evInfo[2])
                    tagEventsEDate.append(evInfo[3])
                    tagEventsState.append(evInfo[12])
        # END SEARCH BY EVENT TAGS-------------------------

        if 'user' in session:
            logedIn = True
        else:
            logedIn = False
        return render_template("search_browseEvents.html", events=events, eventDates=eventDates, eventTimes=eventTimes,
                               eventLocations=eventLocations, eventPrices=eventPrices, eventItag=eventItag,
                               eventTitle=eventTitle,
                               eventStartDate=eventStartDate, eventEndDate=eventEndDate, eventAddress=eventAddress,
                               eventPrice=eventPrice,
                               eventTime=eventTime, eventOccupants=eventOccupants, eventCapacity=eventCapacity,
                               eventRange=eventRange, logedIn=logedIn, eventId=eventId)


    ###########################################################--EDIT EVENT--########################################
    @app.route('/editEvent.html', methods=["POST", "GET"])
    @app.route('/editEvent', methods=["POST", "GET"])
    def editEvent():
        if 'user' in session:
            logedIn = True
            eventId = request.form.get("eventId")
            userId = session["userId"]
            usersId = []
            usersName = []
            usersEmail = []

            # GET EVENT----------------------------------------------------------------^
            # check if event found by eventId
            if (db.checkAny(cursor, "eventId", "events", "eventId", str(eventId),
                            "userId", str(userId)) == True):
                # get all variables in event
                event = db.getEventsByEId(cursor, str(eventId))

                eventTitle = event[1]
                eventStartDate = event[2]
                eventEndDate = event[3]
                eventDeadline = event[4]
                eventPrice = event[5]
                eventDes = event[6]
                eventCap = event[7]
                eventOcp = event[8]
                eventITag = imageReturn(event[9])
                eventAddress = event[10]
                eventCity = event[11]
                eventState = event[12]
                eventZip = event[13]
                eventUId = event[14]
                eventDeadlineTime = 0

                # GET ALL ATTENDING EVENT--------------------------------------^

                # get user_events by userId
                eventUsers = db.getUEventsByEvent(cursor, str(eventId))
                userRange = 0

                # for all user_events, get the event
                for tupleEvent in eventUsers:
                    # add each section to list
                    usersId.append(tupleEvent[1])
                    usersName.append(tupleEvent[3])
                    usersEmail.append(tupleEvent[4])
                    userRange += 1

            # END GET ALL ATTENDING EVENT--------------------------------------^

            userId = session["userId"]
            if request.method == "POST":

                # UPDATE EVENT---------------------------------------------------
                if "saveEvent" in request.form:

                    eventTitle = request.form["title"]
                    eventAddress = request.form["address"]
                    eventCity = request.form["city"]
                    eventState = request.form.get("state")  # NOT GETTING ANY VALUE
                    eventZip = request.form["zip"]
                    eventStartDate = request.form["startDate"]
                    eventStartTime = request.form["startTime"]
                    eventEndDate = request.form["endDate"]
                    eventEndTime = request.form["endTime"]
                    eventPrice = request.form["price"]
                    eventCap = request.form["maxCapacity"]

                    eventDeadline = request.form["deadlineDate"]
                    eventDeadlineTime = request.form["deadlineTime"]
                    eventITag = request.form.get("eventTag")  # NEEDS CHECKING
                    eventDes = request.form["description"]

                    # change price back to 0, if none entered
                    if eventPrice == '':
                        eventPrice = 0.0

                    # check if event found by eventId
                    if (db.checkAny(cursor, "eventId", "events", "eventId", str(eventId),
                                    "userId", str(userId)) == True):
                        # get list of all variables
                        eE = [str(eventTitle), str(eventStartDate), str(eventEndDate), str(eventDeadline),
                              str(eventPrice), str(eventDes), str(eventCap), str(eventITag), str(eventAddress),
                              str(eventCity), str(eventState), str(eventZip), str(userId)]
                        # update all variables
                        db.updateEvent(cnx, cursor, str(eventId), str(userId), eE)

                        return redirect(url_for('manageEvents'))
                    # if userId doesnt match, send to manage events
                    else:
                        print("Sorry, you are not authorized to edit this event")
                        return redirect(url_for('manageEvents'))
                # END UPDATE EVENT---------------------------------------------------^

                # DELETE EVENT AND USER EVENTS----------------------------------------------
                if "deleteEvent" in request.form:

                    # check if user is admin
                    if (db.checkAny(cursor, "eventId", "events", "eventId", str(eventId),
                                    "eventId", str(eventId)) == True):

                        # remove all users from event
                        db.removeUEventsByEvent(cnx, cursor, str(eventId))

                        # remove event
                        db.removeEvent(cnx, cursor, str(eventId), str(userId))

                        return redirect(url_for('manageEvents'))

                    else:
                        print("You are not able to delete this event")
                        return redirect(url_for('manageEvents'))
                # DELETE EVENT AND USER EVENTS----------------------------------------------
    #DELETE USER IN EVENT--------------------------------------------------------
                if "del" in request.form:
                    print("Event id before pull is: ", eventId)
                    uEID = request.form.get("userDel")
                    eventId = request.form.get('eventDelUserId')
                    print("GOT HERE WITH THIS U ID:", uEID, "and this event Id: ", eventId)

                    if (db.checkAny(cursor, "attendantId", "user_events", "eventId", str(eventId),
                                    "userId", str(userId))):
                        db.removeUEvents(cnx, cursor, str(uEID), str(eventId))
                    else:
                        print("User not found in Event")
                        return render_template("editEvent.html", eventId=eventId, eventTitle=eventTitle,
                                               eventStartDate=eventStartDate, eventEndDate=eventEndDate,
                                               eventDeadline=eventDeadline,
                                               eventPrice=eventPrice, eventDes=eventDes, eventCap=eventCap,
                                               eventITag=eventITag, eventAddress=eventAddress, eventCity=eventCity,
                                               eventState=eventState, eventZip=eventZip,
                                               eventDeadlineTime=eventDeadlineTime,
                                               userId=usersId, usersName=usersName,
                                               logedIn=logedIn, usersEmail=usersEmail, userRange=userRange)
    #DELETE USER IN EVENT--------------------------------------------------------

                else:
                    return render_template("editEvent.html", eventId=eventId, eventTitle=eventTitle,
                                           eventStartDate=eventStartDate, eventEndDate=eventEndDate,
                                           eventDeadline=eventDeadline,
                                           eventPrice=eventPrice, eventDes=eventDes, eventCap=eventCap,
                                           eventITag=eventITag, eventAddress=eventAddress, eventCity=eventCity,
                                           eventState=eventState, eventZip=eventZip,
                                           eventDeadlineTime=eventDeadlineTime,
                                           userId=usersId, usersName=usersName,
                                           logedIn=logedIn, usersEmail=usersEmail, userRange=userRange)

                return render_template("editEvent.html", eventId=eventId, eventTitle=eventTitle,
                                       eventStartDate=eventStartDate, eventEndDate=eventEndDate,
                                       eventDeadline=eventDeadline,
                                       eventPrice=eventPrice, eventDes=eventDes, eventCap=eventCap,
                                       eventITag=eventITag, eventAddress=eventAddress, eventCity=eventCity,
                                       eventState=eventState, eventZip=eventZip,
                                       eventDeadlineTime=eventDeadlineTime,
                                       userId=usersId, usersName=usersName,
                                       logedIn=logedIn, usersEmail=usersEmail, userRange=userRange)

            # END GET EVENT-------------------------------------------------------------^

            else:
                print("You are not authorized to edit Event")
                return redirect(url_for('user', logedIn=logedIn))

        else:
            logedIn = False
            redirect(url_for('loginPage', logedIn=logedIn))


    #########################################################################################################
    @app.route('/createEvent.html', methods=["POST", "GET"])
    @app.route('/createEvent.html', methods=["POST", "GET"])
    def createEvent():
        if 'user' in session:
            logedIn = True

            if request.method == "POST":
                eventTitle = request.form["title"]
                eventAddress = request.form["address"]
                eventCity = request.form["city"]
                eventState = request.form.get("state")
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
                # userToAdd = request.form["addUser"]
                # userToDelete = request.form["deleteUser"]
                eventOcp = 0
                eventPoP = 0
                userId = session["userId"]
                # NEW EVENT--------------------------------------------------------------^
                # turn to string
                cE = getInputString(
                    [eventTitle, eventStartDate, eventEndDate, eventDeadline, eventPrice, eventDes, eventCap,
                     eventOcp, eventITag, eventAddress, eventCity, eventState, eventZip, userId])

                # check if already exists: if not, create new
                if (db.checkAny(cursor, "eventId", "events", "name", str(eventTitle)
                        , "userId", str(userId)) == False):

                    rt = db.newEvent(cnx, cursor, cE)
                    return redirect(url_for("user"))
                # else return to userIndex
                else:
                    print("ERROR: event already created by you")
                    return redirect(url_for("user", logedIn=logedIn))
            # END NEW EVENT--------------------------------------------------------------^

            else:  # render if button not clicked
                return render_template("createEvent.html")
        else:
            logedIn = False
            redirect(url_for("loginPage"))


    ############################################################################UPDATE USER#######################
    @app.route('/updatePersonalInfo.html', methods=["POST", "GET"])
    @app.route('/updatePersonalInfo', methods=["POST", "GET"])
    def updatePersonalInfo():
        if 'user' in session:
            logedIn = True
            user = session["user"]
            userId = session["userId"]
            # ^GET USER^-------------------------------------------------------------^
            #: check if user found, then get user info into variables
            if (db.checkAny(cursor, "userId", "users", "username", str(user),
                            "userId", str(userId)) == True):
                userE = db.getUserById(cursor, str(userId))

                username = userE[1]
                password = userE[2]
                firstName = userE[3]
                lastName = userE[4]
                email = userE[5]
                address = userE[6]
                zipcode = userE[7]
                city = userE[8]
                state = userE[9]
                phone = userE[10]

            else:
                print("Error: The username does not match the userId")
                return redirect(url_for("user"))

            # ^END GET USER^-----------------------------------------------^
            if request.method == "POST":

                nfirstName = request.form["fn"]
                nlastName = request.form["ln"]
                nusername = request.form["nm"]
                oPassword = request.form["opw"]
                npassword = request.form["pw"]
                naddress = request.form["address"]
                ncity = request.form["city"]
                nstate = request.form.get("state")
                nzipcode = request.form["zip"]
                nemail = request.form["email"]
                nphone = request.form["phone"]

                if 'remove' in request.form:
                    # REMOVE USER------------------------------------------------
                    # password must match
                    if (oPassword != password):
                        print("Please enter correct password")
                        return redirect(url_for("updatePersonalInfo"))

                    # remove all user events
                    uEvents2 = db.getUEventsByUser(cursor, str(userId))
                    for uET2 in uEvents2:
                        db.removeUEvents(cnx, cursor, str(userId), str(uET2[2]))
                        db.removeEventOcp(cnx, cursor, str(uET2[2]))

                    # remove all events created by user
                    uAdmin = db.getEventsByUser(cursor, str(userId))
                    for uAE in uAdmin:
                        db.removeUEventsByEvent(cnx, cursor, str(uAE[0]))
                        db.removeEvent(cnx, cursor, str(uAE[0]), str(userId))

                    # remove user from users
                    db.removeUser(cnx, cursor, str(userId), str(oPassword))

                    # set session to None
                    logout()
                    return redirect(url_for("index"))
                # REMOVE USER------------------------------------------------
                # UPDATE USER---------------------------------------------- ------------------------^
                elif 'submit' in request.form:
                    # password must match
                    if (oPassword != password):
                        print("Please enter correct password")
                        return redirect(url_for("updatePersonalInfo"))

                    # get all new values in list
                    eU = [str(nusername), str(npassword), str(nfirstName),
                          str(nlastName), str(nemail), str(naddress),
                          str(nzipcode), str(ncity), str(nstate), str(nphone)]

                    # update user
                    rt = db.updateUser(cnx, cursor, str(userId), str(oPassword), eU)

                    # update session info
                    session["user"] = nusername
                    session["userEmail"] = nemail
                    session["userState"] = nstate

                    # update user in user_events if username or email change
                    if (str(username) != str(nusername) or str(email) != str(nemail)):
                        chng = [str(nusername), str(nemail)]
                        rt = db.updateUEventsByUId(cnx, cursor, str(userId), chng)

                    return redirect(url_for("user"))
                # END UPDATE USER------------------------------------------------------------------^
                else:
                    return render_template("updatePersonalInfo.html", firstName=firstName, lastName=lastName,
                                           username=username, password=password, address=address,
                                           city=city, state=state, email=email, phone=phone,
                                           zipcode=zipcode, logedIn=logedIn)

            else:
                return render_template("updatePersonalInfo.html", firstName=firstName, lastName=lastName,
                                       username=username, password=password, address=address,
                                       city=city, state=state, email=email, phone=phone,
                                       zipcode=zipcode, logedIn=logedIn)


        else:
            logedIn = False
            redirect(url_for("loginPage"))

except:
    logout()
    try:
        cnx.close()
        cursor.close()
        db = DataB()
        cnx, cursor = db.openDatabase()
    except:
        db = DataB()
        cnx, cursor = db.openDatabase()
    redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
