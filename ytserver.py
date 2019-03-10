#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse 
import SocketServer
import sqlite3
import re
from datetime import datetime
global conn

def authenticateUser(id,password):
    # print 'id : ' + id + ', password : ' + password
    sqlobj = SQLoperations()
    data = sqlobj.fetchColumns("SELECT * from user WHERE login_id = \""+id+"\"") 
    if data=="[]":
        return "No user found!!"
    else:
        password_check = data.split(",")[3]
        if password_check!=password:
            return "Incorrect password!!"
        else:
            cityData = sqlobj.fetchColumns("SELECT * from city WHERE id = \""+data[-3]+"\"")
            # print cityData
            city = cityData.split(":")[1].split(",")[1][0:-2]

            return data[:-3] + city + "]}"

    # print "authenticateUser() response : "+data
def getSettingsData():
    sqlobj = SQLoperations()
    tournames = sqlobj.fetchColumns("SELECT * from tourname")
    tourtypes = sqlobj.fetchColumns("SELECT * from tourtype") 
    cities = sqlobj.fetchColumns("SELECT * from city")
    slots = sqlobj.fetchColumns("SELECT * from timeslot")
    channels = sqlobj.fetchColumns("SELECT * from channel") 
    paytypes = sqlobj.fetchColumns("SELECT * from paytype") 
    
    return tournames + "|" + tourtypes + "|" + cities + "|" + channels + "|" + paytypes + "|" + slots 
def getViewInventoryData():
    sqlobj = SQLoperations()
    inventories = sqlobj.fetchColumns("SELECT * from inventory")
    return inventories
def getInventoryData():    
    sqlobj = SQLoperations()
    tournames = sqlobj.fetchColumns("SELECT * from tourname")
    tourtypes = sqlobj.fetchColumns("SELECT * from tourtype") 
    cities = sqlobj.fetchColumns("SELECT * from city")
    slots = sqlobj.fetchColumns("SELECT * from timeslot")

    return tournames + "|" + tourtypes + "|" + cities + "|" + slots    
def getBookingsData(month,year,days):
    sqlobj = SQLoperations()
    if int(month)<9:
        Month = "0"+str(int(month)+1)
    else:
        Month = str(int(month)+1)
        
    status = ""    
    for x in xrange(1,int(days)+1):
        if x<10:
            X = "0"+str(x)
        else:
            X=str(x)

        Date = year+"-"+Month+"-"+X
        query = "SELECT COUNT(*) from booking WHERE date = \"" + Date + "\""
        data = sqlobj.getCountOfRows(query)
        print query
        no = re.findall(r'\d+',data)
        status += str(no) + ","

    # status+="]"
    return status
def getANBData1():
    sqlobj = SQLoperations()
    channels = sqlobj.fetchColumns("SELECT * from channel") 
    paytypes = sqlobj.fetchColumns("SELECT * from paytype") 
    inv_tourtypes = sqlobj.fetchColumns("SELECT DISTINCT(type_id) from inventory") 
    temp = inv_tourtypes.split(":")[1].split(";")
    ids = []
    for idx,x in enumerate(temp):
        if idx==len(temp)-1:
            x = x[1:len(x)-2] 
        else:
            x = x[1:len(x)-1] 
        
        ids.append(x)
        
    query = "SELECT * from tourtype WHERE "    
    for ID in ids:
        query += "id = " + ID + " OR "
    query = query[0:len(query)-4]                
    Types = sqlobj.fetchColumns(query)
    print Types
        
    inv_cities = sqlobj.fetchColumns("SELECT DISTINCT(city_id) from inventory") 
    temp = inv_cities.split(":")[1].split(";")
    ids = []
    for idx,x in enumerate(temp):
        if idx==len(temp)-1:
            x = x[1:len(x)-2] 
        else:
            x = x[1:len(x)-1] 
        
        ids.append(x)
        
    query = "SELECT * from city WHERE "    
    for ID in ids:
        query += "id = " + ID + " OR "
    query = query[0:len(query)-4]                
    Cities = sqlobj.fetchColumns(query)
    print Cities
    return channels + "|" + paytypes + "|" + Types + "|" + Cities  
def getANBData2(city_id,type_id):
    sqlobj = SQLoperations()
    inv_names = sqlobj.fetchColumns("SELECT DISTINCT(name_id) from inventory WHERE city_id = " + city_id + " AND type_id = " + type_id)
    temp = inv_names.split(":")[1].split(";")
    ids = []
    for idx,x in enumerate(temp):
        if idx==len(temp)-1:
            x = x[1:len(x)-2] 
        else:
            x = x[1:len(x)-1] 
        
        ids.append(x)
        
    query = "SELECT * from tourname WHERE "    
    for ID in ids:
        query += "id = " + ID + " OR "
    query = query[0:len(query)-4]                
    Names = sqlobj.fetchColumns(query)
    print Names
    return Names
def getANBData3(city_id,type_id,name_id):
    sqlobj = SQLoperations()
    inv_slots = sqlobj.fetchColumns("SELECT DISTINCT(slot_id) from inventory WHERE city_id = " + city_id + " AND type_id = " + type_id + " AND name_id = " + name_id)
    temp = inv_slots.split(":")[1].split(";")
    ids = []
    for idx,x in enumerate(temp):
        if idx==len(temp)-1:
            x = x[1:len(x)-2] 
        else:
            x = x[1:len(x)-1] 
        
        ids.append(x)
        
    query = "SELECT * from timeslot WHERE "    
    for ID in ids:
        query += "id = " + ID + " OR "
    query = query[0:len(query)-4]                
    Slots = sqlobj.fetchColumns(query)
    print Slots
    return Slots
def getANBData4(city_id,type_id,name_id,slot_id):
    sqlobj = SQLoperations()
    inv = sqlobj.fetchColumns("SELECT * from inventory WHERE city_id = " + city_id + " AND type_id = " + type_id + " AND name_id = " + name_id + " AND slot_id = " + slot_id)
    print inv
    return inv
def checkGuest(name,email,cc,phone):
    sqlobj = SQLoperations()
    guest_id = sqlobj.fetchColumns("SELECT id from guest WHERE name = \"" + name.lower() + "\" AND email = \"" + email.lower() + "\" AND phone = \"+" + cc + "-"  + phone + "\"")
    if guest_id!="[]":
        print guest_id
        return guest_id
    else :
        guest_id = sqlobj.getCountOfRows("SELECT COUNT(*) from guest")
        print guest_id
        return guest_id
def getViewBookingData(identifier):        
    sqlobj = SQLoperations()
    if identifier=="past" or identifier=="future" or identifier=="unallocated":        
        if identifier=="past":
            booking1 = sqlobj.fetchColumns("SELECT * from booking WHERE date < \""+ str(datetime.today()).split(" ")[0] + "\"")
            booking2 = sqlobj.fetchColumns("SELECT * from booking WHERE date = \""+ str(datetime.today()).split(" ")[0] + "\"")
        elif identifier=="future":
            booking1 = sqlobj.fetchColumns("SELECT * from booking WHERE date > \""+ str(datetime.today()).split(" ")[0] + "\"")
            booking2 = sqlobj.fetchColumns("SELECT * from booking WHERE date = \""+ str(datetime.today()).split(" ")[0] + "\"")
        elif identifier=="unallocated":
            booking1 = sqlobj.fetchColumns("SELECT * from booking WHERE st_id = 0 AND NOT(status == \"CN\") AND date > \""+ str(datetime.today()).split(" ")[0] + "\"")
            booking2 = sqlobj.fetchColumns("SELECT * from booking WHERE st_id = 0 AND NOT(status == \"CN\") AND date = \""+ str(datetime.today()).split(" ")[0] + "\"")
        
        if booking1!="[]":
            temp = booking1.split(":")[1]
            temp = temp[0:len(temp)-1]
            booking1 = temp

        # print booking2
        if booking2!="[]":
            temp = booking2.split(":")[1]
            temp = temp[0:len(temp)-1]
            booking2 = temp
            for booking in booking2.split(";"):
                booking = booking[1:len(booking)-1]
                elements = booking.split(",")
                invID = elements[2]
                slot_id = sqlobj.fetchColumns("SELECT slot_id from inventory WHERE id = " + str(invID))
                slot_id = slot_id.split(":")[1]
                slot_id = slot_id[1:len(slot_id)-2]
                start_time = sqlobj.fetchColumns("SELECT start_time from timeslot WHERE id = "+slot_id)
                start_time = start_time[13:len(start_time)-2]
                # print "Start time of booking : "+start_time
                HOUR = int(start_time.split(":")[0])
                MIN = int(start_time.split(":")[1])
                
                now = datetime.now()
                bookingTime = now.replace(hour=HOUR,minute=MIN)
                if identifier=="past":
                    if bookingTime<now:
                        booking1+=";["+booking+"]"
                elif identifier=="future" or identifier=="unallocated":
                    if bookingTime>now:
                        booking1+=";["+booking+"]"
        
        # print "|---> booking1 : "+booking1
        
        returnText = ""
        temp = booking1.split(";");
        for booking in temp:
            booking = booking[1:len(booking)-1]
            print "booking : "+booking
            elements = booking.split(",")
            print elements
            channel = (sqlobj.fetchColumns("SELECT name from channel WHERE id = "+elements[1])).split(":")[1]
            channel = channel[0:-1]
            inv = sqlobj.fetchColumns("SELECT * from inventory WHERE id = "+elements[2])
            inv = inv.split(":")[1]
            inv = inv[1:len(inv)-2]
            invElements = inv.split(",")
            tourname = (sqlobj.fetchColumns("SELECT name from tourname WHERE id = "+invElements[1])).split(":")[1]
            tourname = tourname[:len(tourname)-1]
            city = (sqlobj.fetchColumns("SELECT name from city WHERE id = "+invElements[2])).split(":")[1]                 
            city = city[:len(city)-1]
            tourtype = (sqlobj.fetchColumns("SELECT name from tourtype WHERE id = "+invElements[3])).split(":")[1]
            tourtype = tourtype[:len(tourtype)-1]
            timeslot = sqlobj.fetchColumns("SELECT * from timeslot WHERE id = "+invElements[4])
            timeslot = timeslot[12:len(timeslot)-1]
            paytype1 = (sqlobj.fetchColumns("SELECT name from paytype WHERE id = "+elements[6])).split(":")[1]
            paytype2 = (sqlobj.fetchColumns("SELECT name from paytype WHERE id = "+elements[9])).split(":")[1]
            paytype1 = paytype1[:len(paytype1)-1]
            paytype2 = paytype2[:len(paytype2)-1]                
            guest =  (sqlobj.fetchColumns("SELECT * from guest WHERE id = "+elements[11])).split(":")[1]
            guest = guest[:len(guest)-1]
            storyteller = sqlobj.fetchColumns("SELECT id,name from storyteller WHERE id = "+elements[-5])
            if storyteller=="[]":
                storyteller = "[unallocated]"
            else :
                storyteller = storyteller.split(":")[1]
                storyteller = storyteller[0:-1]    
            returnText  += "<" + channel +"|"+ tourname +"|"+ city +"|"+ tourtype +"|"+ timeslot +"|"+ paytype1 +"|"+ paytype2 +"|"+ guest + "|" + storyteller + ">"
        
        return "<"+booking1+">"+returnText
        #Check for time in booking2 and 
    elif len(identifier.split("-"))==3: #date : 2019-03-04
        booking1 = sqlobj.fetchColumns("SELECT * from booking WHERE (date = \""+ identifier + "\")")
        if booking1!="[]":
            temp = booking1.split(":")[1]
            temp = temp[0:len(temp)-1]
            booking1 = temp
            returnText = ""
            for booking in booking1.split(";"):
                booking = booking[1:-1]
                elements = booking.split(",")
                print booking
                
                channel = (sqlobj.fetchColumns("SELECT name from channel WHERE id = "+elements[1])).split(":")[1]
                channel = channel[0:-1]
                inv = sqlobj.fetchColumns("SELECT * from inventory WHERE id = "+elements[2])
                inv = inv.split(":")[1]
                inv = inv[1:-2]
                invElements = inv.split(",")
                tourname = (sqlobj.fetchColumns("SELECT name from tourname WHERE id = "+invElements[1])).split(":")[1]
                tourname = tourname[:-1]
                city = (sqlobj.fetchColumns("SELECT name from city WHERE id = "+invElements[2])).split(":")[1]                 
                city = city[:-1]
                tourtype = (sqlobj.fetchColumns("SELECT name from tourtype WHERE id = "+invElements[3])).split(":")[1]
                tourtype = tourtype[:-1]
                timeslot = sqlobj.fetchColumns("SELECT name,start_time from timeslot WHERE id = "+invElements[4])
                timeslot = timeslot[12:-1]
                paytype1 = (sqlobj.fetchColumns("SELECT name from paytype WHERE id = "+elements[6])).split(":")[1]
                paytype2 = (sqlobj.fetchColumns("SELECT name from paytype WHERE id = "+elements[9])).split(":")[1]
                paytype1 = paytype1[:-1]
                paytype2 = paytype2[:-1]                
                guest =  (sqlobj.fetchColumns("SELECT * from guest WHERE id = "+elements[11])).split(":")[1]
                guest = guest[:-1]
                storyteller = sqlobj.fetchColumns("SELECT id,name from storyteller WHERE id = "+str(elements[-5]))
                if storyteller=="[]":
                    storyteller = "[unallocated]"
                else :
                    storyteller = storyteller.split(":")[1]
                    storyteller = storyteller[0:-1]    
                returnText  += "<" + channel +"|"+ tourname +"|"+ city +"|"+ tourtype +"|"+ timeslot +"|"+ paytype1 +"|"+ paytype2 +"|"+ guest + "|" + storyteller + ">"
            
            return "<"+booking1+">"+returnText
def getRSBData1(booking_id):
    sqlobj = SQLoperations()
    booking = sqlobj.fetchColumns("SELECT * from booking WHERE id = " + booking_id) 
    booking = booking.split(":")[1]
    booking = booking[:-1]
    bookingData = booking[1:-1].split(",")
    channel = sqlobj.fetchColumns("SELECT * from channel WHERE id = "+bookingData[1])
    inventory = sqlobj.fetchColumns("SELECT * from inventory WHERE id = "+bookingData[2])
    inventory = inventory.split(":")[1]
    inventory = inventory[1:-2]
    invData = inventory.split(",")
    bookingSplit = booking.split(",")
    inv_id = bookingSplit[2]
    booking = ""
    for idx,val in enumerate(bookingSplit):
        if idx==2:
            booking += "["+invData[0]+"-"+invData[1]+"-"+invData[2]+"-"+invData[3]+"-"+invData[4] + "]" + ","
        else:
            booking += val + ","
    booking = booking[:-1]

    slot_id  = invData[4]
    tourname = sqlobj.fetchColumns("SELECT * from tourname WHERE id = "+invData[1])
    city = sqlobj.fetchColumns("SELECT * from city WHERE id = "+invData[2])
    tourtype = sqlobj.fetchColumns("SELECT * from tourtype WHERE id = "+invData[3])
    
    inv_slots = sqlobj.fetchColumns("SELECT DISTINCT(slot_id) from inventory WHERE city_id = " + invData[2] + " AND type_id = " + invData[3] + " AND name_id = " + invData[1])
    temp = inv_slots.split(":")[1].split(";")
    ids = []
    for idx,x in enumerate(temp):
        if idx==len(temp)-1:
            x = x[1:len(x)-2] 
        else:
            x = x[1:len(x)-1] 
        
        ids.append(x)
        
    query = "SELECT * from timeslot WHERE "    
    for ID in ids:
        query += "id = " + ID + " OR "
    query = query[0:len(query)-4]                
    timeslots = sqlobj.fetchColumns(query)
    
    paytype1 = sqlobj.fetchColumns("SELECT * from paytype WHERE id = " + bookingData[6])
    paytype2 = sqlobj.fetchColumns("SELECT * from paytype")
    guest = sqlobj.fetchColumns("SELECT * from guest WHERE id = "+bookingData[11])
    
    returnData = booking + "|" + channel + "|" + tourname + "|" + city + "|" + tourtype + "|" + timeslots + "|" + paytype1 + "|" + paytype2 + "|" + guest 
    
    return returnData
def getCNBData1(booking_id):
    sqlobj = SQLoperations()
    booking = sqlobj.fetchColumns("SELECT * from booking WHERE id = " + booking_id) 
    booking = booking.split(":")[1]
    booking = booking[:-1]
    bookingData = booking[1:-1].split(",")
    channel = sqlobj.fetchColumns("SELECT * from channel WHERE id = "+bookingData[1])
    inventory = sqlobj.fetchColumns("SELECT * from inventory WHERE id = "+bookingData[2])
    inventory = inventory.split(":")[1]
    inventory = inventory[1:-2]
    invData = inventory.split(",")
    bookingSplit = booking.split(",")
    inv_id = bookingSplit[2]
    booking = ""
    for idx,val in enumerate(bookingSplit):
        if idx==2:
            booking += "["+invData[0]+"-"+invData[1]+"-"+invData[2]+"-"+invData[3]+"-"+invData[4] + "]" + ","
        else:
            booking += val + ","
    booking = booking[:-1]

    slot_id  = invData[4]
    tourname = sqlobj.fetchColumns("SELECT * from tourname WHERE id = "+invData[1])
    city = sqlobj.fetchColumns("SELECT * from city WHERE id = "+invData[2])
    tourtype = sqlobj.fetchColumns("SELECT * from tourtype WHERE id = "+invData[3])
    timeslot = sqlobj.fetchColumns("SELECT * from timeslot WHERE id = "+invData[4])
    paytype1 = sqlobj.fetchColumns("SELECT * from paytype WHERE id = " + bookingData[6])
    paytype2 = sqlobj.fetchColumns("SELECT * from paytype WHERE id = " + bookingData[9])
    guest = sqlobj.fetchColumns("SELECT * from guest WHERE id = "+bookingData[11])
    
    returnData = booking + "|" + channel + "|" + tourname + "|" + city + "|" + tourtype + "|" + timeslot + "|" + paytype1 + "|" + paytype2 + "|" + guest 
    
    return returnData

def addtourname(name):
    sqlobj = SQLoperations()
    status = sqlobj.executeSQLquery("INSERT into tourname(name) VALUES(\""+ name +"\")")
    print status
    return status
def addtourtype(name):
    sqlobj = SQLoperations()
    status = sqlobj.executeSQLquery("INSERT into tourtype(name) VALUES(\""+ name +"\")")
    print status
    return status
def addcity(name):
    sqlobj = SQLoperations()
    status = sqlobj.executeSQLquery("INSERT into city(name) VALUES(\""+ name +"\")")
    print status
    return status
def addslot(name,start_time):
    sqlobj = SQLoperations()
    status = sqlobj.executeSQLquery("INSERT into timeslot(name,start_time) VALUES(\""+ name +"\",\""+start_time+"\")")
    print status
    return status
def addchannel(name):
    sqlobj = SQLoperations()
    status = sqlobj.executeSQLquery("INSERT into channel(name) VALUES(\""+ name +"\")")
    print status
    return status
def addpaytype(name):
    sqlobj = SQLoperations()
    status = sqlobj.executeSQLquery("INSERT into paytype(name) VALUES(\""+ name +"\")")
    print status
    return status    
def addinventory(name_id,city_id,type_id,slot_id):
    sqlobj = SQLoperations()
    data = sqlobj.fetchColumns("SELECT * from inventory WHERE name_id = "+name_id+" AND city_id = "+city_id+" AND type_id = "+type_id+" AND slot_id = "+slot_id)
    if data =='[]':
        status = sqlobj.executeSQLquery("INSERT into inventory(name_id,city_id,type_id,slot_id) VALUES("+ name_id +","+city_id+","+type_id+","+slot_id+")")
        print status
    else :
        status = "API Failed!! Duplicate Inventory Item!!"
    return status    
def addguest(name,email,phone):
    sqlobj = SQLoperations()
    status = sqlobj.executeSQLquery("INSERT into guest(name,email,phone) VALUES(\"" + name + "\",\"" + email + "\",\""+phone+"\")")
    print status
    return status
def addbooking(channel_id,inventory_id,date,people,amount,paytype1_id,discount,amount2,paytype2_id,amount2_reason,guest_id,reference,st_id,status):
    sqlobj = SQLoperations()
    data = sqlobj.executeSQLquery("INSERT into booking(channel_id,inventory_id,date,people,amount,paytype1_id,discount,amount2,paytype2_id,amount2_reason,guest_id,reference,st_id,status,lifecycle) VALUES(" + channel_id + "," + inventory_id + ",\"" + date + "\"," + people + "," + amount + "," + paytype1_id + "," + discount + "," + amount2 + "," + paytype2_id + ",\"" + amount2_reason + "\","+guest_id+",\""+reference+"\","+st_id+",\""+status+"\",\"S\")")
    print data
    return data
def rescheduleBooking(id,inventory_id,date,people,discount,amount2,paytype2_id,amount2_reason,reschedule_reason):
    sqlobj = SQLoperations()
    lifecycle = sqlobj.fetchColumns("SELECT lifecycle from booking WHERE id = " + id)
    lifecycle = lifecycle.split(":")[1]
    lifecycle = lifecycle[1:-2]
    query = "UPDATE booking set inventory_id = " + inventory_id + ",date = \"" + date + "\",people = " + people + ",discount = " + discount 
    query += ",amount2 = " + amount2 + ",amount2_reason = \"" + amount2_reason + "\",paytype2_id = " + paytype2_id 
    query += ",reschedule_reason = \""+reschedule_reason+"\",status = \"R\",lifecycle = \""+ lifecycle + "-R" +"\" WHERE id = " + id
    print "\n\n|||--------> Rescheduling Booking query : " + query
    data = sqlobj.executeSQLquery(query)
    return data
def cancelBooking(id,cancel_reason):
    sqlobj = SQLoperations()
    lifecycle = sqlobj.fetchColumns("SELECT lifecycle from booking WHERE id = " + id)
    lifecycle = lifecycle.split(":")[1]
    lifecycle = lifecycle[1:-2]
    query = "UPDATE booking set cancel_reason = \""+cancel_reason+"\",status = \"CN\",lifecycle = \""+ lifecycle + "-CN" +"\" WHERE id = " + id
    print "\n\n|||--------> Cancel Booking query : " + query
    data = sqlobj.executeSQLquery(query)
    return data

def edittourname(id,name):
    sqlobj = SQLoperations()
    status = sqlobj.executeSQLquery("UPDATE tourname set name =\""+ name +"\" WHERE id = " + str(id))
    print status
    return status
def edittourtype(id,name):
    sqlobj = SQLoperations()
    status = sqlobj.executeSQLquery("UPDATE tourtype set name =\""+ name +"\" WHERE id = " + str(id))
    print status
    return status
def editcity(id,name):
    sqlobj = SQLoperations()
    status = sqlobj.executeSQLquery("UPDATE city set name =\""+ name +"\" WHERE id = " + str(id))
    print status
    return status
def editslot(id,name,start_time):
    sqlobj = SQLoperations()
    status = sqlobj.executeSQLquery("UPDATE timeslot set name =\""+ name +"\",start_time = \""+start_time+"\" WHERE id = " + str(id))
    print status
    return status    
def editchannel(id,name):
    sqlobj = SQLoperations()
    status = sqlobj.executeSQLquery("UPDATE channel set name =\""+ name +"\" WHERE id = " + str(id))
    print status
    return status
def editpaytype(id,name):
    sqlobj = SQLoperations()
    status = sqlobj.executeSQLquery("UPDATE paytype set name =\""+ name +"\" WHERE id = " + str(id))
    print status
    return status
def deletetourname(id):
    sqlobj = SQLoperations()
    no_of_tournames = re.findall('\d+',sqlobj.getCountOfRows("SELECT * from tourname"))
    print "no of tournames ; "+ str(no_of_tournames[0])
    status = sqlobj.executeSQLquery("DELETE from tourname WHERE id = "+ str(id))
    print status
    for i in xrange(int(id)+1,int(no_of_tournames[0])+1):
        temp = sqlobj.executeSQLquery("UPDATE tourname set id = "+str(i-1)+" WHERE id = " + str(i))
    return status
def deletetourtype(id):
    sqlobj = SQLoperations()
    no_of_tourtypes = re.findall('\d+',sqlobj.getCountOfRows("SELECT * from tourtype"))
    print "no of tourtypes ; "+ str(no_of_tourtypes[0])
    status = sqlobj.executeSQLquery("DELETE from tourtype WHERE id = "+ str(id))
    print status
    for i in xrange(int(id)+1,int(no_of_tourtypes[0])+1):
        temp = sqlobj.executeSQLquery("UPDATE tourtype set id = "+str(i-1)+" WHERE id = " + str(i))
    return status
def deletecity(id):
    sqlobj = SQLoperations()
    no_of_cities = re.findall('\d+',sqlobj.getCountOfRows("SELECT * from city"))
    status = sqlobj.executeSQLquery("DELETE from city WHERE id = "+ str(id))
    print status
    for i in xrange(int(id)+1,int(no_of_cities[0])+1):
        temp = sqlobj.executeSQLquery("UPDATE city set id = "+str(i-1)+" WHERE id = " + str(i))
    return status
def deleteslot(id):
    sqlobj = SQLoperations()
    no_of_slots = re.findall('\d+',sqlobj.getCountOfRows("SELECT * from timeslot"))
    status = sqlobj.executeSQLquery("DELETE from timeslot WHERE id = "+ str(id))
    print status
    for i in xrange(int(id)+1,int(no_of_slots[0])+1):
        temp = sqlobj.executeSQLquery("UPDATE timeslot set id = "+str(i-1)+" WHERE id = " + str(i))
    return status      
def deletechannel(id):
    sqlobj = SQLoperations()
    no_of_chanels = re.findall('\d+',sqlobj.getCountOfRows("SELECT * from channel"))
    status = sqlobj.executeSQLquery("DELETE from channel WHERE id = "+ str(id))
    print status
    for i in xrange(int(id)+1,int(no_of_chanels[0])+1):
        temp = sqlobj.executeSQLquery("UPDATE city set id = "+str(i-1)+" WHERE id = " + str(i))
    return status
def deletepaytype(id):
    sqlobj = SQLoperations()
    no_of_types = re.findall('\d+',sqlobj.getCountOfRows("SELECT * from paytype"))
    status = sqlobj.executeSQLquery("DELETE from paytype WHERE id = "+ str(id))
    print status
    for i in xrange(int(id)+1,int(no_of_types[0])+1):
        temp = sqlobj.executeSQLquery("UPDATE paytype set id = "+str(i-1)+" WHERE id = " + str(i))
    return status
def deleteinventory(id):
    sqlobj = SQLoperations()
    no_of_tours = re.findall('\d+',sqlobj.getCountOfRows("SELECT * from inventory"))
    status = sqlobj.executeSQLquery("DELETE from inventory WHERE id = "+ str(id))
    print status
    for i in xrange(int(id)+1,int(no_of_tours[0])+1):
        temp = sqlobj.executeSQLquery("UPDATE inventory set id = "+str(i-1)+" WHERE id = " + str(i))
    return status

def getInvetoryIdFromData(type_id,city_id,name_id,slot_id):
    sqlobj = SQLoperations()
    data = sqlobj.fetchColumns("SELECT id from inventory WHERE type_id = " + type_id + " AND city_id = " + city_id + " AND name_id = " + name_id + " AND slot_id = " + slot_id)
    print data
    return data

class SQLoperations:
    def executeSQLquery(self, query):
        global conn
        try:
            conn.execute(query)
            conn.commit()
            status = "API executed successfully"
        except sqlite3.Error as e:
            status = "API failed : " + e.args[0]
        except Exception as e:
            status = "API failed : " + e.args[0]
            
        return status

    def getCountOfRows(self,query):
        global conn
        cursor = conn.execute(query)
        response =  ""
        for row in cursor:
            response += str(row)

        return response
        
    def fetchColumns(self,query):
        global conn
        print "Query : "+query    
        
        tablename = query.split(' ')[3]
        response = ""
            
        if (tablename == "booking"):
            response += "{\"booking\":"

        elif (tablename == "channel"):
            response += "{\"channel\":"
            
        elif (tablename == "city"):
            response += "{\"city\":"

        elif (tablename == "guest"):
            response += "{\"guest\":"

        elif (tablename == "paytype"):
            response += "{\"paytype\":"

        elif (tablename == "storyteller"):
            response += "{\"storyteller\":"
        
        elif (tablename == "st_avaliability"):
            response += "{\"st_avaliability\":"
        
        elif (tablename == "timeslot"):
            response += "{\"timeslot\":"

        elif (tablename == "inventory"):
            response += "{\"inventory\":"

        elif (tablename == "tourname"):
            response += "{\"tourname\":"

        elif (tablename == "tourtype"):
            response += "{\"tourtype\":"

        elif (tablename == "user"):
            response += "{\"user\":"
        
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        if len(rows)>0:
            for row in rows:
                response += "[" 
                for data in row:
                    response +=  ""+str(data)+","
            
                response = response[0:len(response)-1]
                response += "];"        
            
            response = response[0:len(response)-1]
            response += "}"
        else:
            response="[]"

        print("fetchColumns response : "+response+"\n")
        return response
    
class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        #self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', "*")
        self.send_header('Access-Control-Allow-Methods', "GET, OPTIONS, POST")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    def do_GET(self):
        print "path : "+self.path 

        if self.path == '/':
            self.path = '/index.html'
        
        try:
            print(self.path[1:])
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            print "Debugging Error!!"
            print self.path
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open))
    def do_HEAD(self):
        self._set_headers()
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_headers()
        
        func = post_data.split("?")[0]
        
        if func == 'authenticateUser()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            user = authenticateUser(params[0],params[1])
            self.wfile.write(user)
        elif func == 'addtourname()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = addtourname(params[0])
            self.wfile.write(data)
        elif func == 'addtourtype()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = addtourtype(params[0])
            self.wfile.write(data)
        elif func == 'addcity()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = addcity(params[0])
            self.wfile.write(data)
        elif func == 'addslot()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = addslot(params[0],params[1])
            self.wfile.write(data)
        elif func == 'addchannel()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = addchannel(params[0])
            self.wfile.write(data)
        elif func == 'addpaytype()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = addpaytype(params[0])
            self.wfile.write(data)    
        elif func == 'addinventory()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = addinventory(params[0],params[1],params[2],params[3])
            self.wfile.write(data)    
        elif func == 'addguest()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = addguest(params[0],params[1],"+" + params[2] + "-" + params[3])
            self.wfile.write(data)    
        elif func == 'addbooking()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            temp = getInvetoryIdFromData(params[1],params[2],params[3],params[4])
            temp = temp.split(":")[1]
            inv_id = re.findall(r"\d+",temp);
            print "Obtained Inventory Id : " + str(inv_id[0])
            if param[12]==None:
                param[12]=""
            data = addbooking(params[0],str(inv_id[0]),params[5],params[6],params[7],params[8],params[9],params[10],params[11],params[12],params[13],params[14],params[15],params[16])
            self.wfile.write(data)    
        elif func == 'edittourname()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = edittourname(params[0],params[1])
            self.wfile.write(data)
        elif func == 'edittourtype()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = edittourtype(params[0],params[1])
            self.wfile.write(data)
        elif func == 'editcity()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = editcity(params[0],params[1])
            self.wfile.write(data)
        elif func == 'editslot()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = editslot(params[0],params[1],params[2])
            self.wfile.write(data)
        elif func == 'editslotTime()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = editslotTime(params[0],params[1])
            self.wfile.write(data)
        elif func == 'editchannel()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = edittourtype(params[0],params[1])
            self.wfile.write(data)
        elif func == 'editpaytype()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = editcity(params[0],params[1])
            self.wfile.write(data)
        elif func == 'deletetourname()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = deletetourname(params[0])
            self.wfile.write(data)
        elif func == 'deletetourtype()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = deletetourtype(params[0])
            self.wfile.write(data)
        elif func == 'deletecity()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = deletecity(params[0])
            self.wfile.write(data)
        elif func == 'deleteslot()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = deleteslot(params[0])
            self.wfile.write(data)    
        elif func == 'deletepaytype()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = deletepaytype(params[0])
            self.wfile.write(data)
        elif func == 'deletechannel()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = deletechannel(params[0])
            self.wfile.write(data)
        elif func == 'deleteinventory()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = deleteinventory(params[0])
            self.wfile.write(data)
        elif func == 'getSettingsData()':
            data = getSettingsData()
            self.wfile.write(data)    
        elif func == 'getInventoryData()':
            data = getInventoryData()
            self.wfile.write(data)    
        elif func == 'getViewInventoryData()':
            data = getViewInventoryData()
            self.wfile.write(data)    
        elif func == 'getBookingsData()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = getBookingsData(params[0],params[1],params[2])
            self.wfile.write(data)              
        elif func == 'getAddNewBookingData()':
            data = getAddNewBookingData()
            self.wfile.write(data)
        elif func == 'getANBData1()':
            data = getANBData1()
            self.wfile.write(data)
        elif func == 'getANBData2()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = getANBData2(params[0],params[1])
            self.wfile.write(data)
        elif func == 'getANBData3()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = getANBData3(params[0],params[1],params[2])
            self.wfile.write(data)
        elif func == 'getANBData4()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = getANBData4(params[0],params[1],params[2],params[3])
            self.wfile.write(data)       
        elif func == 'checkGuest()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = checkGuest(params[0],params[1],params[2],params[3])
            self.wfile.write(data)       
        elif func == 'getViewBookingData()':
            param = post_data.split("?")[1]
            print func+': '+param
            data = getViewBookingData(param)
            self.wfile.write(data)
        elif func == 'getRSBData1()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = getRSBData1(params[0])
            self.wfile.write(data)
        elif func == 'rescheduleBooking()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = rescheduleBooking(params[0],params[1],params[2],params[3],params[4],params[5],params[6],params[7],params[8])
            self.wfile.write(data)
        elif func == 'getCNBData1()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = getCNBData1(params[0])
            self.wfile.write(data)
        elif func == 'cancelBooking()':
            param = post_data.split("?")[1]
            print func+': '+param
            params = param.split(",")
            data = cancelBooking(params[0],params[1])
            self.wfile.write(data)
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print str(datetime.today())
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
    global conn
    print("Database opened successfully")
    print
    conn = sqlite3.connect('ytdatabase.db')
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
    conn.close()
