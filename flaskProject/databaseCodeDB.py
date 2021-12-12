import mysql.connector
import datetime
import hashlib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
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
    def hashIt(self, pas):
        hash_pas = hashlib.sha256(pas.encode("utf-8")).hexdigest()
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
    def newUEvents(self, data):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            userClms = ''.join(("userId, eventId, userName, userEmail,",
                                " paid, seat, price"))
            cursor.execute(self.insert("user_events", userClms, data))
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return
        except Exception as e:
            return e

    #REMOVE USER EVENTS
    def removeUEvents(self, userId, eventId):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            cursor.execute(self.remove("user_events", "userId", str(userId), "eventId", str(eventId)))
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return
        except Exception as e:
            return e

    #REMOVE USER EVENTS BY EVENT
    def removeUEventsByEvent(self, eventId):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            cursor.execute(self.remove("user_events", "eventId", eventId, "eventId", eventId))
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return
        except Exception as e:
            return e
        

        
    # UPDATE USER EVENTS
    def updateUEvents(self, userId, eventId, clms, chng):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            
            #for all elements in list: if password hash password given
            for i in range (0, len(clms)):
                #update the column
                cursor.execute(self.update("user_events", str(clms[i]), str(chng[i]), "userId",
                                      str(userId), "eventId", str(eventId)))
                cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return
        except Exception as e:
            return e

    # UPDATE USER EVENTS
    def updateUEventsByUId(self, userId, chng):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()

            #for all elements in list: if password hash password given
            #update the column
            uUE = ''.join(("UPDATE user_events SET",
                           " userName = '%s', userEmail = '%s'"%(str(chng[0]), str(chng[1])),
                           "WHERE userId = '%s'"%(str(userId))))

            cursor.execute(uUE)
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return True
        except Exception as e:
            return e

    #GET USER EVENTS
    def getUEvents(self, userId, eventId, name):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            ur =''.join(("SELECT * FROM user_events WHERE userId = '",
                         userId,"' AND eventId = '", eventId, "'"))
            cursor.execute(ur)
            user = []
            for (idU) in cursor:
                user.append(idU)
            #close
            cursor.close()
            cnx.close()
            return user
        except Exception as e:
            return e
    
    #GET USER EVENTS BY USERID
    def getUEventsByUser(self, userId):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            cursor.execute("SELECT * FROM user_events WHERE userId = %s",(str(userId),))
            usersEvents = []
            for (idU) in cursor:
                usersEvents.append(idU)
            #close
            cursor.close()
            cnx.close()
            return usersEvents
        except Exception as e:
            return e
    
    #GET USER EVENTS BY EVENTID
    def getUEventsByEvent(self, eventId):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            cursor.execute("SELECT * FROM user_events WHERE eventId = %s",(str(eventId),))
            eventUser = []
            for (idU) in cursor:
                eventUser.append(idU)
            #close
            cursor.close()
            cnx.close()
            return eventUser
        except Exception as e:
            return e

#***************************USER PAYMENT************************************
    # CREATE USER PAYMENT
    def newUPay(self, data):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            userClms = ''.join(("userId, card_name, cvc, expiration date, number"))
            cursor.execute(self.insert("user_payment", userClms, data))
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return
        except Exception as e:
            return e

    #REMOVE USER PAYMENT
    def removeUPay(self, userId, name):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            cursor.execute(self.remove("user_payment", "userId", userId, "card_name", name))
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return
        except Exception as e:
            return e

        
    # UPDATE USER PAYMENT
    def updateUPay(self, userId, name, clms, chng):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            #for all elements in list: if password hash password given
            for i in range (0, len(clms)):
                #update the column
                cursor.execute(self.update("user_payment", str(clms[i]), str(chng[i]), "userId",
                                      str(userId), "card_name", str(name)))
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return
        except Exception as e:
            return e


    #GET USER PAYMENT
    def getUPay(self, userId, name):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            ur =''.join(("SELECT * FROM user_payment WHERE userId = '",
                         userId,"' AND card_name = '", name, "'"))
            cursor.execute(ur)
            for (idU) in cursor:
                uPay = [idU]
            #close
            cursor.close()
            cnx.close()
            return uPay
        except Exception as e:
            return e

        


#****************************USER*******************************************

    # CREATE NEW USER
    def newUser(self, data):
        try:
            #DataB
            cnx, cursor = self.openDatabase()
            userClms = ''.join(("username, passwordId, first_name, last_name,",
                            "email, address, zipcode, city, state, phone"))
            cursor.execute(self.insert( "users", userClms, data))
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            
            return
        except Exception as e:
            return e
        

  

    #REMOVE USER
    def removeUser(self, userId, passwordId):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            cursor.execute(self.remove("users", "userId", userId, "passwordId", passwordId))
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return
        except Exception as e:
            return e

    #UPDATE USER    
    def updateUser(self, userId, passwordId, uC):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            uU = ''.join(("UPDATE users SET username = '%s', passwordId = '%s',"%(str(uC[0]),str(uC[1])),
                      " first_name = '%s', last_name = '%s',"%(str(uC[2]),str(uC[3])),
                      " email = '%s', address = '%s', zipcode = '%s',"%(str(uC[4]),str(uC[5]), str(uC[6])),
                      " city = '%s', state = '%s', phone = '%s'"%(str(uC[7]),str(uC[8]), str(uC[9])),
                      " WHERE userId ='%s' AND passwordId = '%s'"%(str(userId),str(passwordId))))
            cursor.execute(uU)
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return True
        except Exception as e:
            return e        

    #GET USER
    def getUser(self, username, pswd):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            ur =''.join(("SELECT * FROM users WHERE username = '",
                         username,"' AND passwordId = '", pswd, "'"))
            cursor.execute(ur)
            user = []
            for (idU) in cursor:
                user = idU
            #close
            cursor.close()
            cnx.close()
            return user
        except Exception as e:
            return e
        
    def getUserById(self, user):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            ur = ''.join(("SELECT * FROM users WHERE userId = '",
                         user,"'"))
            cursor.execute(ur)
            user = []
            for (idU) in cursor:
                user = idU
            #close
            cursor.close()
            cnx.close()
            return user
        except Exception as e:
            return e


#*******************************EVENTS***************************************
    #ADD EVENT
    def newEvent(self, data):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            eventClms = ''.join(("name, sDate, eDate, deadlineDate, price, des,",
                                 " capacity, occupants, iTag, address,",
                                 " city, state, zipcode, userId, sTime, eTime, dTime"))
            ts = self.insert("events", eventClms, data)
            cursor.execute(ts)
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return
        except Exception as e:
            return e

    #REMOVE EVENT
    def removeEvent(self, eventId, userId):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            cursor.execute(self.remove("events", "eventId", eventId, "userId", userId))
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return
        except Exception as e:
            return e

        
    def removeEventsByUId(self, userId):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            cursor.execute(self.remove("events", "userId", str(userId), "userId", str(userId)))
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return
        except Exception as e:
            return e
        
    #UPDATE EVENT    
    def updateEvent(self, eventId, userId, uC):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            uU = ''.join(("UPDATE events SET name = '%s', sDate = '%s',"%(str(uC[0]),str(uC[1])),
                      " eDate = '%s', deadlineDate = '%s',"%(str(uC[2]),str(uC[3])),
                      " price = '%s', des = '%s', capacity = '%s',"%(str(uC[4]),str(uC[5]), str(uC[6])),
                      " iTag = '%s', address = '%s',"%(str(uC[7]),str(uC[8])),
                      " city = '%s', state = '%s', zipcode = '%s',"%(str(uC[9]),str(uC[10]), str(uC[12])),
                          " sTime = '%s', eTime = '%s', dTime = '%s'"%(str(uC[13]),str(uC[14]), str(uC[15])),
                      " WHERE eventId ='%s' AND userId = '%s'"%(str(eventId),str(userId))))
            cursor.execute(uU)
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return True
        except Exception as e:
            return e

    #UPDATE OCCUPANTS BY 1
    def addEventOcp(self, eventId, pastOcp):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            #get occupant as old plus 1
            ocp = int(pastOcp) + 1
            #update
            cursor.execute(self.update("events", "occupants", str(ocp), "eventId",
                                      str(eventId), "eventId", str(eventId)))
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return
        except Exception as e:
            return e

    #UPDATE OCCUPANTS BY -1
    def removeEventOcp(self, eventId):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            #get event info
            event = self.getEventsByEId(eventId)
            if(event[8] == 0):
                #close
                cursor.close()
                cnx.close()
                return
            else:
                #get occupant as old minus 1
                ocp = int(event[8]) - 1
                #update
                cursor.execute(self.update("events", "occupants", str(ocp),
                                         "eventId", str(eventId),
                                         "eventId", str(eventId)))
                cnx.commit()
                #close
                cursor.close()
                cnx.close()
            return
        except Exception as e:
            return e

    #GET EVENT
    def getEventsByUser(self, userId):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            ur =''.join(("SELECT * FROM events WHERE userId = '", userId, "'"))
            cursor.execute(ur)
            event = []
            for (idU) in cursor:
                event.append(idU)
            #close
            cursor.close()
            cnx.close()
            return event
        except Exception as e:
            return e
        
    #GET EVENT BY EVENT ID
    def getEventsByEId(self, eId):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            ur =''.join(("SELECT * FROM events WHERE eventId = '", eId, "'"))
            cursor.execute(ur)
            for (idU) in cursor:
                event = idU
            #close
            cursor.close()
            cnx.close()
            return event
        except Exception as e:
            return e

    #GET EVENTS
    def getEvents(self):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            events = []
            # ur =''.join(("SELECT * FROM events WHERE eventId = '", eId, "'"))
            ur = "SELECT * FROM events;"
            cursor.execute(ur)
            memes = cursor.fetchall()
            for meme in memes:
                events.append(meme)
            #close
            cursor.close()
            cnx.close()
            return events
        except Exception as e:
            return e
    #GET EVENTS BY STATE
    #(from outside: state)-> get events in state after 
    def getEventsByLoc(self, state):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            events = []
            st = ''.join(("SELECT * FROM events WHERE state = '",state,
                          "' AND deadlineDate >= '", str(datetime.date.today()),"'"))
             

            cursor.execute(st)

            for(event) in cursor:
                events.append(event)
            #close
            cursor.close()
            cnx.close()
            return events
        except Exception as e:
            return e

    #GET EVENT BY POPULARITY MOST TO LEAST
    def getEventsByPop(self):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            events = []
            po = ''.join(("SELECT * FROM events WHERE deadlineDate >= '",str(datetime.date.today()),
                          "' ORDER BY (capacity - occupants) "))
            cursor.execute(po)

            for(event) in cursor:
                events.append(event)
            #close
            cursor.close()
            cnx.close()
            return events
        except Exception as e:
            return e
        
    #GET EVENTS BY DATE RANGE
    #(from outside: lowerDate, upperDate)-> get events in date range
    def getEventsByUpcoming(self):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            events = []
            dt = ''.join(("SELECT * FROM events WHERE eDate >= '",str(datetime.date.today()),
                 "' ORDER BY eDate"))
            cursor.execute(dt)
            
            for(event) in cursor:
                events.append(event)
            #close
            cursor.close()
            cnx.close()
            return events
        except Exception as e:
            cursor.close()
            cnx.close()
            return e
    
    #GET EVENTS BY DATE RANGE
    #(from outside: lowerDate, upperDate)-> get events in date range
    def getEventsByDate(self, lDate, uDate):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            events = []
            dt = ''.join(("SELECT * FROM events WHERE date BETWEEN '",
                  str(lDate),"' AND '", str(uDate), "'"))
            cursor.execute(dt)
            
            for(event) in cursor:
                events.append(event)
            #close
            cursor.close()
            cnx.close()
            return events
        except Exception as e:
            #close
            cursor.close()
            cnx.close()
            return e

    #GET EVENTS BY ADVANCED KEYWORD SEARCH
    def getEventsAdvanced(self, wordS):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            
            ps = PorterStemmer()
            stopWords = set(stopwords.words('English'))

            wordTokens = word_tokenize(wordS)
            eventDc = {}
            finalList = []
            #if word greater than 1
            if len(wordTokens) > 1:
                #for all words in string. if not stopword get all events words: if found add 1, else create new
                for w in wordTokens:
                    if not w.lower() in stopWords:
                        setEvent = self.getEventsByKeyword(ps.stem(w))
                        for ev in setEvent:
                            if ev in eventDc:
                                eventDc[ev] += 1
                            else:
                                eventDc[ev] = 1

                while eventDc:
                    maxKey = max(eventDc, key = eventDc.get)
                    finalList.append(maxKey)
                    eventDc.pop(maxKey)
                #close
                cursor.close()
                cnx.close()
                return(finalList)
            else:
                finalList = self.getEventsByKeyword( ps.stem(wordS))
                #close
                cursor.close()
                cnx.close()
                return(finalList)
                
        except Exception as e:
            #close
            cursor.close()
            cnx.close()
            return e

    
    def getEventsByKeyword(self, word):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            events = []
            word = "%" + str(word) + "%"
            cursor.execute("SELECT * FROM events WHERE name LIKE '%s'"%(word,))
            for (event) in cursor:
                events.append(event)
            #close
            cursor.close()
            cnx.close()
            return events
        except Exception as e:
            #close
            cursor.close()
            cnx.close()
            return e

#*****************************EVENT_TAGS*****************************************
    # CREATE EVENT TAGS
    def newEventTag(self, data):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            userClms = ''.join(("eventId, tagId"))
            cursor.execute(self.insert("event_tags", userClms, data))
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return
        except Exception as e:
            #close
            cursor.close()
            cnx.close()
            return e


    #REMOVE EVENT TAGS
    def removeEventTag(self, eventId, tagId):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            cursor.execute(self.remove("event_tags", "eventId", eventId, "tagId", tagId))
            cnx.commit()
            #close
            cursor.close()
            cnx.close()
            return
        except Exception as e:
            #close
            cursor.close()
            cnx.close()
            return e


    #GET EVENT TAGS BY EVENT
    def getEventTagByEvent(self, eventId):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            ur =''.join(("SELECT * FROM event_tags WHERE eventId = %s"%(str(eventId),)))
            cursor.execute(ur)
            for (idU) in cursor:
                tags = [idU]
            #close
            cursor.close()
            cnx.close()
            return tags
            
        except Exception as e:
            #close
            cursor.close()
            cnx.close()
            return e

    def getEventTagByTagId(self, tagId):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            ur =''.join(("SELECT * FROM event_tags WHERE tagId = %s"%(str(tagId),)))
            cursor.execute(ur)
            for (idU) in cursor:
                events = idU
            cursor.close()
            cnx.close()
            return events
        except Exception as e:
            cursor.close()
            cnx.close()
            return e
     #-------------------------------------------------------

    #check to see if in table
    def checkAny(self, clm, tbl, cd1, ans1, cd2, ans2):
        try:
            db = DataB()
            cnx, cursor = self.openDatabase()
            anyC = ''.join(("SELECT ALL ", clm," FROM ", tbl," WHERE ",cd1 ," = '",ans1 ,
                            "' AND ", cd2," = '",ans2 ,"'"))
            cursor.execute(anyC)
            it = 0
            #if i is found, return normal
            for i in cursor:
                it += 1
                #close
                cursor.close()
                cnx.close()
                return True
            #if not found, return not normal
            if it == 0:
                #close
                cursor.close()
                cnx.close()
                return False
        except Exception as e:
            #close
            cursor.close()
            cnx.close()
            return e

    #check if occupants is less than capacity
    def checkAvl(self, eId):
        try:
            #db = DataB()
            cnx, cursor = self.openDatabase()
            
            anyC = ''.join(("SELECT ALL eventId FROM events WHERE eventId = '",eId ,
                            "' AND occupants < capacity"))
            cursor.execute(anyC)
            it = 0
            #if i is found, return normal
            for i in cursor:
                it += 1
                #close
                cursor.close()
                cnx.close()
                return True
            #if not found, return not normal
            if it == 0:
                #close
                cursor.close()
                cnx.close()
                return False
        except Exception as e:
            return e



    
##
#db = DataB()

#print(db.getEventsAdvanced("thank you christ mas"))
#cnx, cursor = db.openDatabase()

#print(db.getEventsByUpcoming(cursor))
#wordS = "thank giving and christ mas are here to test you"
#print(db.getEventsAdvanced(cursor, "t"))
                
            
    
#print(db.getEventsByKeyword(cursor,'t'))
      
##uU = ''.join(("UPDATE events SET name = 'Code Class#2', sDate = '2021-12-11',",
##              " eDate = '2021-12-11', deadlineDate = '2021-12-11', price = '0.0',",
##              " des = 'code class', capacity = '14', iTag = '4', address = '123 Main St',",
##              " city = 'Town', state = 'IL', zipcode = '12345'",
##              " WHERE eventId ='24' AND userId = '1'"))
##cursor.execute(uU)
##print(cursor)
##cnx.commit()
#cE = "'Test', '2022-04-04', '2022-04-04', '2022-04-04', '0', 'test', '23', '18', '3', '123 main st', 'Town', 'IL', '12345', '30'"
#print(db.newEvent(cnx, cursor, cE))

#userId = "7"
#passwordId = "hohoho"
#eU =["Santa", "hohoho", "Santa", "Claus", "HOHOHO@cheers.cheers", "01 North Pole", "00001", "North Pole", "NP", 1234567890]
#uC =["username","passwordId", "first_name", "last_name", "email", "address", "zipcode",
                # "city", "state", "phone"]
            #update user
#rt = db.updateUser(cnx, cursor, userId, passwordId, eU)
#print(rt)
#cursor.execute(db.updateOld("users", "phone", "1234567890", "userId", "6", "passwordId", "12345"))
#cnx.commit()
#print(db.getEventsByKeyword(cursor, "%t%"))
#tagEvents = db.getEventTagByTagId(cursor, str(7))
#evInfo = db.getEventsByEId(cursor, str(tagEvents[1]))
#print(evInfo)
#print(db.getEventsByPop(cursor))
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


