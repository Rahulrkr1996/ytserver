#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse 
import SocketServer
import sqlite3
import re

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
    
def getAddNewBookingData():
    sqlobj = SQLoperations()
    channels = sqlobj.fetchColumns("SELECT * from channel") 
    paytypes = sqlobj.fetchColumns("SELECT * from paytype") 
    tourtypes = sqlobj.fetchColumns("SELECT * from tourtype") 
    cities = sqlobj.fetchColumns("SELECT * from city")

    return channels + "|" + paytypes + "|" + tourtypes + "|"+ cities

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
    data = sqlobj.fetchColumns("SELECT * from tour WHERE name_id = "+name_id+" AND city_id = "+city_id+" AND type_id = "+type_id+" AND slot_id = "+slot_id)
    if data =='[]':
        status = sqlobj.executeSQLquery("INSERT into tour(name_id,city_id,type_id,slot_id) VALUES("+ name_id +","+city_id+","+type_id+","+slot_id+")")
        print status
    else :
        status = "API Failed!! Duplicate Inventory Item!!"
    return status    

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

# def getANBTours(type_id,city_id):
#     sqlobj = SQLoperations()
#     data = sqlobj.fetchColumns("SELECT * inventory user WHERE login_id = \""+id+"\"") 
    # query = "SELECT COUNT(*) from "+tablename
        
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
        # elif func == 'getANBTours()':
        #     param = post_data.split("?")[1]
        #     print func+': '+param
        #     params = param.split(",")
        #     data = getANBTours(int(param[0]),int(param[1]))  #both are ids
        #     self.wfile.write(data)    
        # elif (post_data.find('SELECT') != -1): 
        #     print ("Performing SELECT operation")
        #     post_data_list = post_data.split()
        #     status = sqlobj.fetchColumns(post_data)                
        #     self.wfile.write(status)
        # elif (post_data.find('INSERT') != -1): 
        #     print ("Performing INSERT operation")
        #     self.wfile.write("Performing INSERT operation")
            
        #     status = sqlobj.executeSQLquery(post_data)
        #     self.wfile.write(status)
        # elif (post_data.find('UPDATE') != -1): 
        #     print ("Performing UPDATE operation")
        #     self.wfile.write("Performing UPDATE operation")
        #     status = sqlobj.executeSQLquery(post_data)
        #     self.wfile.write(status)
        # elif (post_data.find('DELETE') != -1): 
        #     print ("Performing DELETE operation")
        #     self.wfile.write("Performing DELETE operation")
        #     status = sqlobj.executeSQLquery(post_data)
        #     self.wfile.write(status)
        # else: 
        #     print ("Invalid Query")
        #     self.wfile.write("Invalid Query")
        

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
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
