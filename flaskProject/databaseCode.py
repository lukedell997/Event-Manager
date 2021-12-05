import mysql.connector
import datetime
import hashlib
class DataB:
    
    #====================== OPEN DATABASE =========================================
    def openDatabase(self):
        try:
            cnx = mysql.connector.connect(user='sql5455144',
                                          password='5C5RDzrAZ5',
                                  host='sql5.freemysqlhosting.net',
                                  database='sql5455144')
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

    def openDatabase1(self):
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
    #encrypt

    #decrypt

    #
        
    #====================== BASIC STATEMENTS ====================================
    # INSERT
    def insert(self, table, items, values):
        insert = "INSERT INTO {0} ({1}) VALUES ({2})".format(table, items, values)
        return insert
    #UPDATE
    def update(self, table, clm, value, uId, user, pId, pswd ):
        update = "UPDATE {0} SET {1} = '{2}' WHERE {3} = '{4}' AND {5} = '{6}'".format(table,
                                                                                       clm,
                                                                                       value,
                                                                                       uId,
                                                                                       user,
                                                                                       pId,
                                                                                       pswd)
        return update
    #REMOVE
    def remove(self, table, uId, user, pId, pswd):
        remove = "DELETE FROM {0} WHERE {1} = '{2}' AND {3} = '{4}'".format(table, uId, user,
                                                                        pId, pswd)
        return remove

    # GET:
    def get(self, items, table):
        get = "SELECT {0} FROM {1}".format(items, table)
        return get

    # SELECT WHERE EQUAL:
    def selectEq(self, items, table, clm, sterm):
        selectEq = ''.join((get(items, table), " WHERE {0} = {1}".format(clm, sterm)))
        return selectEq

    # SELECT IN RANGE:
    def selectRng(self, clm, lwr, upr):
        selectRng = "WHERE {0} BETWEEN {1} AND {2}".format(clm, lwr, upr)
        return selectRng

#==================== END BASIC STATEMENTS =================================
    #*****************************USER_EVENTS*****************************************
    # CREATE USER EVENTS
    def newUEvents(self, cnx, cursor, data):
        try:
            userClms = ''.join(("userId, eventId, userName, userEmail, paid, seat, price"))
            cursor.execute(db.insert("user_events", userClms, data))
            cnx.commit()
            return
        except:
            return -99

    #REMOVE USER EVENTS
    def removeUEvents(self, cnx, cursor, userId, eventId):
        try:
            cursor.execute(db.remove("user_events", "userId", userId, "eventId", eventId))
            cnx.commit()
            return
        except:
            return -99

        
    # UPDATE USER EVENTS
    def updateUEvents(self, cnx, cursor, userId, eventId, clms, chng):
        try:
            #for all elements in list: if password hash password given
            for i in range (0, len(clms)):
                #update the column
                cursor.execute(db.update("user_events", str(clms[i]), str(chng[i]), "userId",
                                      str(userId), "eventId", str(eventId)))
                cnx.commit()
                return
        except:
            return -99

    #GET USER EVENTS
    def getUEvents(self, cursor, userId, eventId, name):
        ur =''.join(("SELECT * FROM user_events WHERE userId = '",
                     userId,"' AND eventId = '", eventId, "'"))
        cursor.execute(ur)
        user = []
        for (idU) in cursor:
            user.append(idU)
        return user
    
    #GET USER EVENTS BY USERID
    def getUEventsByUser(self, cursor, userId):
        ur =''.join(("SELECT * FROM user_events WHERE userId = '",userId, "'"))
        cursor.execute(ur)
        usersEvents = []
        for (idU) in cursor:
            usersEvents.append(idU)
        return usersEvents
    
    #GET USER EVENTS BY EVENTID
    def getUEventsByEvent(self, cursor, eventId, name):
        ur =''.join(("SELECT * FROM user_events WHERE eventId = '", eventId, "'"))
        cursor.execute(ur)
        eventUser = []
        for (idU) in cursor:
            eventUsers.append([idU])
        return eventUsers

    #***************************USER PAYMENT************************************
    # CREATE USER PAYMENT
    def newUPay(self, cnx, cursor, data):
        try:
            userClms = ''.join(("userId, card_name, cvc, expiration date, number"))
            cursor.execute(db.insert("user_payment", userClms, data))
            cnx.commit()
            return
        except:
            return -99

    #REMOVE USER PAYMENT
    def removeUPay(self, cnx, cursor, userId, name):
        try:
            cursor.execute(db.remove("user_payment", "userId", userId, "card_name", name))
            cnx.commit()
            return
        except:
            return -99

        
    # UPDATE USER PAYMENT
    def updateUPay(self, cnx, cursor,userId, name, clms, chng):
        try:
            #for all elements in list: if password hash password given
            for i in range (0, len(clms)):
                #update the column
                cursor.execute(db.update("user_payment", str(clms[i]), str(chng[i]), "userId",
                                      str(userId), "card_name", str(name)))
                cnx.commit()
                return
        except:
            return -99


    #GET USER PAYMENT
    def getUPay(self, cursor, userId, name):
        ur =''.join(("SELECT * FROM user_payment WHERE userId = '",
                     userId,"' AND card_name = '", name, "'"))
        cursor.execute(ur)
        for (idU) in cursor:
            uPay = [idU]
        return uPay

        


    #****************************USER*******************************************

    # CREATE NEW USER
    def newUser(self, cnx, cursor, data):
        userClms = ''.join(("username, passwordId, first_name, last_name,",
                            "email, address, zipcode, city, state, phone"))
        cursor.execute(DataB.insert(self, "users", userClms, data))
        cnx.commit()
        return

  

    #REMOVE USER
    def removeUser(self, cnx, cursor, userId, passwordId):
        try:
            cursor.execute(db.remove("users", "userId", userId, "passwordId", passwordId))
            cnx.commit()
            return
        except:
            return -99

        
    # UPDATE USER: List of coulmns, and list of changes
    def updateUser(self, cnx, cursor,userId, passwordId, clms, chng):
        try:
            #for all elements in list: if password hash password given
            for i in range (0, len(clms)):
                if (clms[i] == "passwordId"):
                    chng[i] = hashIt(chng[i])
                #update the column
                cursor.execute(db.update("users", str(clms[i]), str(chng[i]), "userId",
                                        str(userId), "passwordId", str(passwordId)))
                cnx.commit()
                return
        except:
            return -99


    #GET USER
    def getUser(self, cursor, username, pswd):
        ur =''.join(("SELECT * FROM users WHERE username = '",
                     username,"' AND passwordId = '", pswd, "'"))
        cursor.execute(ur)
        for (idU) in cursor:
            user = idU
        return user


    #*******************************EVENTS***************************************
    #ADD EVENT
    def newEvent(self, cnx, cursor, data):
        try:
            eventClms = ''.join(("name, date, deadlineDate, price, desc, capacity,",
                                "pub_pri, address, zipcode, state, userId"))
            cursor.execute(db.insert("events", eventClms, data))
            cnx.commit()
            return
        except:
            return -99

    #REMOVE EVENT
    def removeEvent(self, cnx, cursor, eventId, userId):
        try:
            cursor.execute(db.remove("events", "eventId", eventId, "userId", userId))
            cnx.commit()
            return
        except:
            return -99

    #UPDATE EVENTS
    def updateEvent(self, cnx, cursor, eventId, userId, clms, chng):
        try:
            #for all elements in list
            for i in range (0, len(clms)):
                #update the column
                cursor.execute(db.update("events", str(clms[i]), str(chng[i]), "eventId",
                                      str(eventId), "userId", str(userId)))
                cnx.commit()
                return
        except:
            return -99


    #UPDATE OCCUPANTS BY 1
    def updateEventOcp(self, cnx, cursor, eventId, pastOcp):
        try:
            #get occupant as old plus 1
            ocp = int(pastOcp) + 1
            #update
            cursor.execute(db.update("events", "occupants", str(ocp), "eventId",
                                      str(eventId), "eventId", str(eventId)))
            cnx.commit()
            return
        except:
            return -99

    #UPDATE OCCUPANTS BY -1
    def removeEventOcp(self,cnx, cursor, eventId):
        try:
            #get event info
            event = db.getEventByEId(cursor, eventId)
            if(event[8] == 0):
                return
            else:
                #get occupant as old minus 1
                ocp = int(event[8]) - 1
                #update
                cursor.execute(db.update("events", "occupants", str(ocp),
                                         "eventId", str(eventId),
                                         "eventId", str(eventId)))
                cnx.commit()
            return
        except:
            return -99

    #GET EVENT
    def getEventByUser(self, cursor, userId):
        ur =''.join(("SELECT * FROM events WHERE userId = '", userId, "'"))
        cursor.execute(ur)
        event = []
        for (idU) in cursor:
            event.append(idU)
        return event
        
        #GET EVENT BY EVENT ID
    def getEventByEId(self, cursor, eId):
        ur =''.join(("SELECT * FROM events WHERE eventId = '", eId, "'"))
        cursor.execute(ur)
        for (idU) in cursor:
            event = idU
        return event
    
    #GET EVENTS BY STATE
    #(from outside: state)-> get events in state after 
    def getEventsByState(self, cursor, state):
        events = []
        st = ''.join(("SELECT * FROM events WHERE state = '",state,
                      "' AND date >= '", str(datetime.date.today()), "'"))

        cursor.execute(st)

        for(event) in cursor:
            events.append(event)
        return events

    #GET EVENTS BY DATE RANGE
    #(from outside: lowerDate, upperDate)-> get events in date range
    def getEventsByDate(self, cursor, lDate, uDate):
        events = []
        dt = ''.join(("SELECT * FROM events WHERE date BETWEEN '",
              str(lDate),"' AND '", str(uDate), "'"))
        cursor.execute(dt)
        
        for(event) in cursor:
            events.append(event)
        return events


    #*****************************EVENT_TAGS*****************************************
    # CREATE EVENT TAGS
    def newEventTag(self, cnx, cursor, data):
        try:
            userClms = ''.join(("eventId, tagId"))
            cursor.execute(db.insert("event_tags", userClms, data))
            cnx.commit()
            return
        except:
            return -99


    #REMOVE EVENT TAGS
    def removeEventTag(self, cnx, cursor, eventId, tagId):
        try:
            cursor.execute(db.remove("event_tags", "eventId", eventId, "tagId", tagId))
            cnx.commit()
            return
        except:
            return -99


    #GET EVENT TAGS BY EVENT
    def getEventByEvent(self, cursor, eventId, name):
        ur =''.join(("SELECT * FROM event_tags WHERE eventId = '",eventId))
        cursor.execute(ur)
        for (idU) in cursor:
            tags = [idU]
        return tags

    def getEventByTag(self, cursor, tagId, name):
        ur =''.join(("SELECT * FROM event_tags WHERE tagId = '",tagId))
        cursor.execute(ur)
        for (idU) in cursor:
            events = [idU]
        return events
    #*****************************EVENT_SEATING*****************************************
    # CREATE EVENT SEATING
    def newEventSeating(self, cnx, cursor, data):
        try:
            userClms = ''.join(("seatingId, eventId, seatCat1, cat1Price,",
                                " seatCat2, cat2Price, seatCat3, cat3Price,",
                                " seatCat4, cat4Price, seatCat5, cat5Price,",
                                " seatCat6, cat6Price,"))
            cursor.execute(db.insert("event_seating", userClms, data))
            cnx.commit()
            return
        except:
            return -99

    #UPDATE EVENT SEATING
    def updateEventSeating(self, cnx, cursor, seatingId, eventId,  clms, chng):
        try:
            #for all elements in list
            for i in range (0, len(clms)):
                #update the column
                cursor.execute(db.update("event_seating", str(clms[i]), str(chng[i]), "seatingId",
                                      str(seatingId), "eventId", str(eventId)))
                cnx.commit()
                return
        except:
            return -99
        
    #REMOVE EVENT SEATING
    def removeEventSeating(self, cnx, cursor, seatingId, eventId):
        try:
            cursor.execute(db.remove("event_seating", "seatingId", seatingId, "eventId", eventId))
            cnx.commit()
            return
        except:
            return -99


    #GET EVENT SEATING
    def getEventSeating(self, cursor, eventId, name):
        ur =''.join(("SELECT * FROM event_seating WHERE eventId = '",eventId))
        cursor.execute(ur)
        for (idU) in cursor:
            eventSeating = [idU]
        return eventSeating


    #-------------------------------------------------------


    def checkAny(self, cursor, clm, tbl, cd1, ans1, cd2, ans2):
        anyC = ''.join(("SELECT ALL ", clm," FROM ", tbl," WHERE ",cd1 ," = '",ans1 ,
                        "' AND ", cd2," = '",ans2 ,"'"))
        cursor.execute(anyC)
        it = 0
        #if i is found, return normal
        for i in cursor:
            it += 1
            return True
        #if not found, return not normal
        if it == 0:
            return False

    def checkAvl(self, cursor, eId):
        anyC = ''.join(("SELECT ALL eventId FROM events WHERE eventId = '",eId ,
                        "' AND occupants < capacity"))
        cursor.execute(anyC)
        it = 0
        #if i is found, return normal
        for i in cursor:
            it += 1
            return True
        #if not found, return not normal
        if it == 0:
            return False


##
#db = DataB() 
#cnx, cursor = db.openDatabase()

#adminEventsId = []
#adminEventsTitle = []
#adminEventsSDate = []
#adminEventsEDate = []
#adminEvents = db.getEventByUser(cursor, str(1))
#for tupleEvent in adminEvents:
#    adminEventsId.append(tupleEvent[0])
#    adminEventsTitle.append(tupleEvent[1])
#    adminEventsSDate.append(tupleEvent[2])
#    adminEventsEDate.append(tupleEvent[3])
#print(adminEventsId)

#print(db.removeEventOcp(cnx, cursor, "1"))

##        #turn to string
#cU = "'userUsername', 'userPassword', 'userFirstName', 'userLastName', 'userEmail', 'userAddress', 'userZipcode', 'userCity', 'userState', 'userNumber'"

#db.newUser(cnx, cursor, cU)
##        

###add new user
##
##newUserData = ''.join(("'PlanetSaver83', 'ab4c3d','Al', 'Gore', ",
##"'gore@wh.org', '2021 Penn ave.', '21012', 'VA'"))
###db.newUser(cnx, cursor, newUserData)
##t = db.updateUser(cnx, cursor, '2', 'ab4c3d',['first_name', 'last_name'], ['Max', 'Zillion'] )
##print(t)
###t2 = db.removeUser(cnx, cursor, '2', 'ab4c3d')
###print(t2)
##
###get user
##'''
##username = "PlanetSaver83"
##password = "ab4c3d"
##user = getUser(cursor,username, password)
##print(user)
##'''
###get events by state
##'''
##userState = "IL"
##eventsState = getEventsByState(cursor, userState)
##'''
##
###get events in date range
##'''
##lDate = datetime.date(2021, 12, 1)
##uDate = datetime.date(2021, 12, 30)
##eventsDateRange = getEventsByDate(cursor,lDate, uDate)
##'''
##
### update events 
##'''
##eventId = 4
##userId = 6
##eventClms = ["name", "date", "capacity"]
##chngs = ["Ybagildorf", "2022-08-20","55"]
##
##updateEvent(cnx, cursor, eventId, userId, eventClms, chngs)
##'''
###update users
##'''
##userId = 15
##passwordId = "ab4c3d"
##userClms = ["passwordId", "address", "zipcode"]
##chngs = ["gory", "632 pershy ave", "50129"]
##
##updateUser(cnx, cursor, userId, passwordId, userClms, chngs)
##'''
##
##print(db.checkAny(cursor, "userId", "users", "username","John","passwordId", "password"))
##cursor.close()
##cnx.close()
##


