from flask import Flask, render_template, redirect, url_for, request, flash, session
from datetime import timedelta

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(hours=5)

app.secret_key = "hello"

admin = False


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
    # FILL LISTS WITH DATA OF EVENTS FROM DATABASE
    search = None
    if request.method == "POST":
        search = request.form["searchbar"]
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
        userState = request.form.get("state")
        userEmail = request.form["email"]
        userNumber = request.form["phone"]
            
        # PUSH THE DATA TO THE DATABASE!!!!!!!!!
        return redirect(url_for("loginPage"))  # ????
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
        return redirect(url_for("user"))
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

        myEventImage = []  # FILL THESE
        myEventTitle = []
        myEventDetails = []

        attendingEventsTitle = []  # FILL WITH USERES EVENTS
        attendingEventsDate = []  # FILL WITH 6 popular EVENTS
        attendingEventsDeadline = []  # FILL WITH 6 NEAR BY EVENTS
        
        popEventImage = []
        popEventTitle = []
        popEventDetails = []
        if request.method == "POST":
            if "clicked" in request.form:
                eventID = request.form["eventID"]
                return  redirect(url_for("eventDetails", eventID = eventID))
            elif 'searchbar' in request.form:
                search = request.form["searchbar"]
                # DO A SEARCH
        else:
            return render_template("index_userLoggedIn.html", name=user, myEventImage=myEventImage,
                                   myEventTitle=myEventTitle, myEventDetails=myEventDetails,
                                   attendingEventsTitle=attendingEventsTitle, attendingEventsDate=attendingEventsDate,
                                   attendingEventsDeadline=attendingEventsDeadline, popEventTitle=popEventTitle,
                                   popEventDetails=popEventDetails, search=search, popEventImage=popEventImage)

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
def eventDetails(eventId):  # put application's code here
    # NEED TO PULL ALL THE VARIABLES THAT ARE BEING PASSED FROM THE DATABASE
    eventDate = []
    eventTitle = []
    eventPrice = []
    eventDescription = []
    eventAddress = []
    eventTags = []
    eventImage = []

    if "attend" in request.form and request.method == "POST":
        if "user" in session:
            user = session["user"]
            # ADD USER TO THE DATABASE LIST OF USERS ATTENDING THE EVENT
            return redirect(url_for("user"))
        else:
            return redirect(url_for("loginPage"))
    return render_template("eventDetails.html", eventDate=eventDate, eventTitle=eventTitle, eventPrice=eventPrice,
                           eventDescription=eventDescription, eventAddress=eventAddress, eventTags=eventTags,
                           eventImage=eventImage)


@app.route('/manageEvents.html', methods=["POST", "GET"])
@app.route('/manageEvents', methods=["POST", "GET"])
def manageEvents():  # put application's code here
    if "user" in session:
        user = session["user"]
        usersEvents = []  # FILL THESE WITH THE APPROPRIATE DATA
        userEventsDates = []
        userEventsTime = []
        userAttendingEvents = []  # I have no idea what the difference between the first one and this one is but it is requested
        eventsMaxPop = []

        if 'leaveEvent' in request.form and request.method == "POST":
            user = session["user"]
            # REMOVE THE USER FROM THE EVENT IN DATABASE
        return render_template("manageEvents.html", usersEvents=usersEvents, userEventsDates=userEventsDates,
                               userEventsTime=userEventsTime, userAttendingEvents=userAttendingEvents,
                               eventsMaxPop=eventsMaxPop)

    else:
        return redirect(url_for("login"))  # ????


@app.route('/search_browseEvents.html', methods=["POST", "GET"])
@app.route('/search_browseEvents', methods=["POST", "GET"])
def search_browseEvents():  # put application's code here
    events = []  # fill the info
    eventDates = []
    eventTimes = []
    eventLocations = []
    eventPrices = []
    eventImage = []
    #eventPopulation = []
    #eventMaxPop = []
    if request.method == "POST":
        search = request.form["searchbar"]
        # DO A SEARCH
    else:
        return render_template("search_browseEvents.html", events=events, eventDates=eventDates, eventTimes=eventTimes,
                               eventLocations=eventLocations, eventPrices=eventPrices, eventImage=eventImage)



@app.route('/editEvent.html', methods=["POST", "GET"])
@app.route('/editEvent.html', methods=["POST", "GET"])
def editEvent():
    eventTitle = []
    eventAddress = []
    eventCity = []
    eventState = []
    eventZip = []
    eventStartDate = []
    eventEndDate = []
    eventPrice = []
    eventCap = []
    eventDeadline = []
    eventDeadlineTime = []
    eventDes = []
    userToAdd = []
    userToDelete = []
    # GET FROM DATABASE!!!!!!!!!

    if request.method == "POST":
        if 'searchbar' in request.form:
            search = request.form["searchbar"]
            # DO A SEARCH
        else:
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
            eventDeadlineTime = request.form["deadlineTime"]
            eventDes = request.form["description"]
            userToAdd = request.form["addUser"]
            userToDelete = request.form["deleteUser"]
            # PUSH TO DATABASE
    else:
        return render_template("editEvent.html", eventTitle=eventTitle, eventAddress=eventAddress, eventCity=eventCity,
                               eventState=eventState, eventZip=eventZip, eventStartDate=eventStartDate, eventEndDate=
                               eventEndDate, eventPrice=eventPrice, eventCap=eventCap, eventDeadline=eventDeadline,
                               eventDeadlineTime=eventDeadlineTime, eventDes=eventDes, userToAdd=userToAdd,
                               userToDelete=userToDelete)

@app.route('/createEvent.html', methods=["POST", "GET"])
@app.route('/createEvent.html', methods=["POST", "GET"])
def createEvent():
    if 'user' in session:
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
            eventDeadlineTime = request.form["deadlineTime"]
            eventDes = request.form["description"]
            userToAdd = request.form["addUser"]
            userToDelete = request.form["deleteUser"]
            # PUSH TO DATABASE
            return redirect(url_for("user"))
        else:
            return render_template("createEvent.html")
    else:
        redirect(url_for("loginPage"))

@app.route('/updatePersonalInfo.html', methods=["POST", "GET"])
@app.route('/updatePersonalInfo', methods=["POST", "GET"])
def updatePersonalInfo():
    if 'user' in session:
        if request.method == "POST":
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            username = request.form["username"]
            password = request.form["password"]
            address = request.form["address"]
            city = request.form["city"]
            state = request.form["state"]
            email = request.form["email"]
            phone = request.form["phone"]
            # PUSH TO DATABASE!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return redirect(url_for("user"))
        else:
            firstName = []
            lastName = []
            username = []
            password = []
            address = []
            city = []
            state = []
            email = []
            phone = []
            return render_template("eventDetails.html", firstName=firstName, lastName=lastName, username=username, password=
                                   password, address=address, city=city, state=state, email=email, phone=phone)
    else:
        redirect(url_for("loginPage"))

if __name__ == '__main__':
    app.run(debug=True)
