from BluetoothConnection import *
from WiFiConnection import *
from SecurityManager import *
from bluetooth import *
from threading import Thread
from time import *
from collections import deque
import json
import sys
import os

class ConnectivityManager:
   
    def __init__(self):
        self.queue = deque()
	self.token = None

        if self.isBluetoothEnabled:
            if sys.platform == "linux2":
                os.system("sudo hciconfig hci0 name Raspi") #quitar esto para el release
                os.system("sudo bluetooth-agent 1234 &")
            self.btConn = BluetoothConnection(PORT_ANY)
        else:
            self.btConn = None  
        if self.isWiFiEnabled:
            self.wfConn = WiFiConnection(8001)
        else:
            self.wfConn = None

        self.__securityManager = None
        self.__currentUser = None
        self.__isReadingOverBt = False
        self.__isReadingOverWf = False
        
    def currentUser(self):
        return self.__currentUser

    def startListening(self):
        bothChannels = True

        if self.btConn:
            bothChannels = False
            btThread = Thread(target = self.btConn.startListening, args = ())
            btThread.daemon = True
            btThread.start()

        if self.wfConn:
            bothChannels = True if not bothChannels else False
            wfThread = Thread(target = self.wfConn.startListening, args = ())
            wfThread.daemon = True
            wfThread.start()
        
        while ((bothChannels and btThread.isAlive() and wfThread.isAlive()) or 
               (self.btConn and btThread.isAlive()) or (self.wfConn and wfThread.isAlive())):
            sleep(1)

        if self.btConn and not btThread.isAlive():
            socket = self.btConn.__getSocket__()
        elif self.wfConn and not wfThread.isAlive():
            socket = self.wfConn.__getSocket__()

        self.sendCapabilities(socket)
        response = socket.recv(1024) #esperar por la respuesta del cliente
        data = json.loads(response)
        if "action" in data and data["action"] == "LOGIN":
            self.logIn(socket)
        else:
            raise Exception
    
    def join(self, client):
        try:
            a = client.getCapabilities()
        except Exception, e:
            print "Client not suitable"
            raise Exception, "Client dosen't match the specs"
        self.__client__ = client

    def sendCapabilities(self, socket):
        capabilities = self.__client__.getCapabilities()
        j = {"action":"intent", "target":"CAPABILITIES", "data":capabilities}
	a = json.dumps(j)
	socket.send(a)

    def startReading(self): 
        if self.btConn and not self.__isReadingOverBt:  
            socket = self.btConn.__getSocket__()
            self.__isReadingOverBt = True
            self.__read__ (socket)
        elif self.wfConn and not self.__isReadingOverWf:     
            socket = self.wfConn.__getSocket__()
            self.__isReadingOverWf = True
            self.__read__ (socket)
        
    def stopReading(self):
        self.__isReadingOverBt = False
        self.__isReadingOverWf = False

    def send(self, data):
        if self.btConn and len(data) < 1000:
            self.btConn.send(data)
        elif self.wfConn:
            self.wfConn.send(data)

    @property
    def isWiFiEnabled(self):
	if sys.platform == "linux2":
	    error = os.system("sudo iw list")
	    if error == 0:
	        return True
        return False

    @property
    def isBluetoothEnabled(self):
	if sys.platform == "linux2":
            error = os.system("sudo hciconfig hci0 -a")
            if error == 0:
                return True
        return False

    @property
    def isReading(self):
        return self.__isReadingOverBt or self.__isReadingOverWf
        
    def __read__(self, socket):
        print "Start Reading"
        #socket.setblocking(False)
        #socket.settimeout(5)
        while self.isReading:
            try:
                try:
                    buffer = socket.recv(1024)
                except timeout, e:
                    continue
                event = json.loads(buffer)
                self.queue.append(event)
                #print "Package added for filtering"
                if len(self.queue) > 1:
		    continue
                else:
                    t = Thread(target = self.__filter__, args = ())
                    t.daemon = True
                    t.start()      
		    #sleep(10)
            except Exception, e:
		print e
                print "GENERAL FAILURE. RESTARTING PROGRAM  ..."
                self.__reset__()
        raise Exception, e

    def __filter__(self):
        #print "Filter Started with ", len(self.queue), "packages"
        while len(self.queue) > 0:
            current = self.queue[0]
            try:
                event = current
                if "action" in event and event["action"] == "CREATE_USER":
                    try:
                        self.__securityManager.addUser(event["user"], event["password"], event["question"], event["answer"], event["permission"])
                    except NameError, e:
                        self.send(json.dumps({"action":"intent", "target":"MANAGE_USER", "message":e.__str__()}))
                elif "action" in event and event["action"] == "DEL_USER":
                    self.__securityManager.removeUser(event["user"])
                elif "action" in event and event["action"] == "GET_ALL_USERS":
                    all = self.__securityManager.getAllUser()
                    data = {"action":"ALL_USERS", "data":all}
                    client_socket.send(json.dumps(data))
                elif "action" in event and event["action"] == "CHANGE_USER_CREDENTIALS":
                    self.__securityManager.changeCredentials
                elif "action" in event and event["action"] == "LOGOUT":
                    self.__reset__()
                    raise Exception
                elif "action" in event and event["action"] == "CALL":
                    self.call(event["name"], event["params"])
            except Exception, e:
                print e
                if current != "":
                    print current
                continue
            self.queue.popleft()  

    def call(self, name, params):
        if name == "":
            return

        if params == "":
            data = {'action':name, 'params':(), 'token': self.token}
        else:
            p = eval(params)
            if type(p) == type(()):
                data = {'action': name, 'params': p, 'token': self.token}
            else:
                data = {'action': name, 'params': (p,), 'token': self.token}
       
	result = self.__client__.ApiRESTCall(data)
	
	if len(result) != 0 and name != 'register':
	    j = {"action":"RETURN", "from":name, "value":result[0]}
	    self.send(json.dumps(j))
	return result
			

    def logIn(self, socket):
        try: 
            security = SecurityManager()
            message = security.requestLogIn(socket)
            while message != "":
                message = security.requestLogIn(socket, message)
                if message == "abort":
                    raise Exception, "Log In canceled by user"
            
            self.token = self.call("register", "")[0]
	    
            succes = {"action":"LOGIN_OK", "permission":security.getCurrentPermissions()}
            socket.send(json.dumps(succes))
            self.__currentUser = security.getCurrentUser()
            self.__securityManager = security
            print self.__currentUser, " is now LogIn"
        except Exception, e:
            print e
            abort = {"action":"ABORT", "message":"Incorrect user name or password"}
            j = json.dumps(abort)
            socket.send(j)
            raise Exception, "Log In Failed"

    def __reset__(self):
        print "\n-----------------------Restarting Program--------------------------\n"
        self.__securityManager = None
        self.__currentUser = None
        if self.wfConn:
            self.wfConn.reset()
        if self.btConn:
            self.btConn.reset()
        self.stopReading()
        self.queue.clear()
