from flask import Flask, render_template, redirect, url_for, request, flash, session
from datetime import timedelta
import databaseCode


app = Flask(__name__)
app.permanent_session_lifetime = timedelta(hours=5)

app.secret_key = "hello"

admin = False


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
# *NEW USER TO DATABASE--------------------------------
#STILL NEED TO CHECK IF DATA IS CORRECT(state is 2 letters, zip 5 numbers, etc)
        cU = getInputString([userUsername, userPassword, userFirstName,
                             userLastName, userEmail, userAddress,
                             userZipcode, userCity, userState, userNumber])
        #check if already exists
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
            "passwordId", str(password)) == False):
            print("Error: The username or password is incorrect")
        else:
            [uId, user, password, uFN, uLN, uEmail,
             uAd, uZip, uCity, uState,
             uPhone] = db.getUser(cursor, str(user), str(password))
#END GET USER-----------------------------------------------
        
        session["user:"] = user
        return redirect(url_for("user"))

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
        
#GET ALL USER EVENTS-------------------------------
        userEvents = db.getUEventsByUser(cursor, uId)
        for tupleEvent in userEvents:
            evInfo = db.getEventByEId(cursor, tupleEvent[2])

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
    if "user" in session:
        if "attend" in request.form:
            user = session["user"]
            #ADD USER TO THE DATABASE LIST OF USERS ATTENDING THE EVENT
    return render_template("eventDetails.html", eventDate = eventDate, eventTitle = eventTitle, eventPrice = eventPrice,
                           eventDescription = eventDescription, eventAddress = eventAddress, eventTags = eventTags)

@app.route('/manageEvents.html')
@app.route('/manageEvents')
def manageEvents():  # put application's code here
    if "user" in session:
        usersEvents = []  # FILL THESE WITH THE APPROPRIATE DATA
        userEventsDates = []
        userEventsTime = []
        userAttendingEvents = [] #I have no idea what the difference between the first one and this one is but it is requested
        eventsMaxPop = []

        if 'leave' in request.form:
            user = session["user"]
#REMOVE THE USER FROM THE EVENT IN DATABASE-------------
        if(checkAny(cursor, "attendantId", "user_events", "userId",
                    uId, "eventId", eventId) == True):
            removeUEvents(cnx, cursor, uId, eventId)
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
        ################## push to database!!!!!!!

        

    return render_template("create_editEvents.html", userInfo=userInfo)



if __name__ == '__main__':
    app.run(debug=True)
