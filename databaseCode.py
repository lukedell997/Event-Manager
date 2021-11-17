import mysql.connector
import datetime
import hashlib
#====================== OPEN DATABASE =========================================
def openDatabase():
    try:
        cnx = mysql.connector.connect(user='root', password='Intransig3ntM0nkey$',
                              host='127.0.0.1',
                              database='sys_schema')
        cursor = cnx.cursor()
    
        return cnx, cursor
    #display errors    
    except mysql.connector.Error as er:
        if (er.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            print("Database Username and password wrong")
        elif(er.errno == errorcode.ER_BAD_DB_ERROR):
            print("Database Does not Exist")
        else:
            print(er)
#==================END OPEN DATABASE =========================================

# Turn into hash
def hashIt(pas):
    hash_pas = hashlib.md5(pas.encode("utf-8")).hexdigest()
    return hash_pas
    
#====================== BASIC STATEMENTS ====================================
# INSERT
def insert(table, items, values):
    insert = "INSERT INTO {0} ({1}) VALUES ({2})".format(table, items, values)
    return insert

# GET:
def get(items, table):
    get = "SELECT {0} FROM {1}".format(items, table)
    return get

# SELECT WHERE EQUAL:
def selectEq(items, table, clm, sterm):
    selectEq = ''.join((get(items, table), " WHERE {0} = {1}".format(clm, sterm)))
    return selectEq

# SELECT IN RANGE:
def selectRng(clm, lwr, upr):
    selectRng = "WHERE {0} BETWEEN {1} AND {2}".format(clm, lwr, upr)
    return selectRng

#==================== END BASIC STATEMENTS =================================

#*****************************PAYMENT***************************************
def newPayment(cnx, cursor, data):
    items = "userId, card_name, cvc, expiration_date, number"
    np = ''.join((insert("user_payment", items, data)))
    cursor.execute(np)
    cnx.commit()
    return

def updatePayment(cnx, cursor, userId, data):
    removePayment(userId)
    newPayment(data)

def removePayment(cursor,userId):
    rp = ''.join(("DELETE FROM user_payment WHERE userId = '", userId,"'"))
    cursor.execute(rp)
    return
    
def getPayment(cursor,userId):
    if (cursor.execute("SELECT user_paymentId, userId IF(userId,)") == True):
        gp = ''.join(("SELECT * FROM user_payment WHERE userId = '",
                      userId, "'"))
        cursor.execute(gp)

        

    else:
        print("Not the proper access")
    
    

#****************************USER_EVENTS************************************
#      ++ add an if statement(if user and event already paired)++
# data needs to be "'12','3', 'email',...'12.50'"
def newAttendee(cnx, cursor, data):
    items = "userId, eventId, userEmail, paid, seat, price"
    at = ''.join((insert("user_events",items, data)))
    cursor.execute(at)
    cnx.commit()
    return

#delete whole attendant
def removeAttendee(cursor, userId, eventId):
    rt =''.join(("DELETE FROM user_events WHERE userId = '",
                 userId," AND eventId = ",eventId ,"'"))
    cursor.execute(rt)
    return

#get all events user is in
def getUsersEvents(cursor, userId):
    ue= ''.join(("SELECT * FROM user_events WHERE userId = '",userId ,"'"))
    cursor.execute(ue)
    allUsers = []
    for i in cursor:
       allUsers.append(i)
    return allUsers

#get all users in event
def getEventsUsers(cursor, eventId):
    eu= ''.join(("SELECT * FROM user_events WHERE eventId = '",eventId ,"'"))
    cursor.execute(eu)
    allEvents = []
    for i in cursor:
       allEvents.append(i)
    return allEvents
#****************************USER_EVENTS************************************


#****************************USER*******************************************
# =========================CREATE NEW USER=================================
#data needs to be "'Bob', 'Dole', '7013', ..."
#    ++ add password hash here or before entering data
def newUser(cnx, cursor, data):
    userClms = ''.join(("username, passwordId, first_name, last_name,",
                        "email, address, zipcode, state"))
    cursor.execute(insert("users", userClms, data))
    cnx.commit()
    return
#========================= END CREATE NEW USER==================================
#=========================  UPDATE USER  ========================================
def updateUser(cnx, cursor,userId, passwordId, clmchng, chng):
    try:
        #hash password
        if(clmchng == "passwordId"):
            chng = hashIt(chng)
        #update data: where userId and passwordId is equal
        ue =''.join(("UPDATE users SET ", clmchng, " = '", chng, "' WHERE userId = '",
          str(userId), "' AND passwordId = '", str(passwordId), "'"))
        #execute
        cursor.execute(ue)
        cnx.commit()
        return
    except:
        print("You do not have access")
    
    

#========================= END UPDATE USER ===================================
#==============================GET USER=======================================
def getUser(cursor, username, pswd):
    ur =''.join(("SELECT * FROM users WHERE username = '",
                 username,"' AND passwordId = '", pswd, "'"))
    cursor.execute(ur)
    for (idU) in cursor:
        user = [idU]
    return user
#=========================END GET USER=======================================
#*******************************USER*****************************************

#*******************************EVENTS***************************************

#======================GET EVENTS BY STATE=====================================
#(from outside: state)-> get events in state after 
def getEventsByState(cursor, state):
    events = []
    st = ''.join(("SELECT * FROM events WHERE state = '",state,
                  "' AND date >= '", str(datetime.date.today()), "'"))

    cursor.execute(st)

    for(event) in cursor:
        event = [event[0],event[1],event[2],event[3],event[4],event[5],
                 event[6],event[7],event[8],event[9], event[10], event[11]]
        events.append(event)
    return events
#====================== END GET EVENTS BY STATE=====================================
#=======================GET EVENTS BY DATE RANGE================================
#(from outside: lowerDate, upperDate)-> get events in date range
def getEventsByDate(cursor, lDate, uDate):
    events = []
    dt = ''.join(("SELECT * FROM events WHERE date BETWEEN '",
          str(lDate),"' AND '", str(uDate), "'"))
    cursor.execute(dt)
    
    for(event) in cursor:
        event = [event[0],event[1],event[2],event[3],event[4],event[5],
                 event[6],event[7],event[8],event[9], event[10], event[11]]
        events.append(event)
    return events

#======================= END EVENTS BY DATE RANGE================================
#=========================UPDATE EVENTS========================================
#(From outside: eventID, userID, column, change)-> where userId and eventID: update
def updateEvent(cnx, cursor, eventId,userId, clmchng, chng):
    try:
        ue =''.join(("UPDATE events SET ", clmchng, " = '", chng, "' WHERE eventId = '",
          str(eventId), "' AND userId = '", str(userId), "'"))
        cursor.execute(ue)
        cnx.commit()
        return
    except:
        print("You do not have access") 

def checkId(cursor, table, checkId):
    cU = ''.join(("SELECT ", table, " IF( userId = '", checkId,
                  "', 'True', 'False')"))
    cursor.execute(cU)
    for i in cursor:
        print(i)
#========================= END UPDATE EVENTS===================================
#=============================ADD EVENT=======================================
#       +++ STILL NEEDS WORK +++
def addEvent(cnx, cursor, data, userId):
    userClms = ''.join(("username, passwordId, first_name, last_name,",
                        "email, address, zipcode, state"))
    cursor.execute(insert("users", userClms, data))
    cnx.commit()
#******************************EVENTS****************************************

cnx, cursor = openDatabase()

#add new user
'''
newUserData = ''.join(("'PlanetSaver83', 'ab4c3d','Al', 'Gore',
'gore@wh.org', '2021 Penn ave.', '21012', 'VA'"))
newUser(cnx, cursor, newUserData)
'''
#get user
'''
username = "PlanetSaver83"
password = "ab4c3d"
user = getUser(cursor,username, password)
print(user)
'''
#get events by state
'''
userState = "IL"
eventsState = getEventsByState(cursor, userState)
'''

#get events in date range
'''
lDate = datetime.date(2021, 12, 1)
uDate = datetime.date(2021, 12, 30)
eventsDateRange = getEventsByDate(cursor,lDate, uDate)
'''

# update events 
'''
eventId = 4
userId = 5
eventClms = ["name", "date", "capacity"]
chngs = ["Ybagildorf", "2022-08-19","54"]
for i in range(0, len(eventClms)):
    print(i)
    updateEvent(cnx, cursor, eventId, userId, eventClms[i], chngs[i])
'''
#update users
'''
userId = 15
passwordId = "ab4c3d"
userClms = ["email", "address", "zipcode"]
chngs = ["goryal73@wh.org", "632 pershy ave", "50129"]
for i in range(0, len(userClms)):
    updateUser(cnx, cursor, userId, passwordId, userClms[i], chngs[i])
'''
checkId(cursor, "users", "2")
cursor.close()
cnx.close()


#LATER
def signIn(googleID):
    try:
        query = (get("*","user"), " ",selectEq("usernameId", username),
                 " AND ", selectEq("passwordId", googleID))
        cursor.execute()
    except:
        print("Error: username or password incorrect")


