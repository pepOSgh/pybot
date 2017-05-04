__author__ = 'Rauly'

from bluetooth import *
from time import *
from threading import Thread
import json
from SecurityManager import *

global client_socket, address, buffer
client_socket = None
address = None
buffer = None

def create_bluetooth_server_socket(port):
    if port < 0 or port > 30: return None
    socket = BluetoothSocket(RFCOMM)
    socket.bind(("", port))
    socket.listen(1)
    return socket

def read():
    global buffer
    while True:
        try:
            buffer = client_socket.recv(1024)
            try:
                event = json.loads(buffer)
                if "action" in event and event["action"] == "CREATE_USER":
                    security.addUser(event["user"], event["password"], event["question"], event["answer"])
                elif "action" in event and event["action"] == "DEL_USER":
                    security.removeUser(event["user"])
                elif "action" in event and event["action"] == "GET_ALL_USERS":
                    all = security.getAllUser()
                    data = {"action":"ALL_USERS", "data":all}
                    client_socket.send(json.dumps(data))
                elif "action" in event and event["action"] == "CHANGE_USER_CREDENTIALS":
                    security.changeCredentials
            except:
                if buffer != "":
                    print name + ":", buffer
        except:
            pass

#a = Profile("raul", "raul", 1, "none")
#d = {"raul":a.getDict()}
#j = json.dumps(d)
#file = open("profiles.txt", 'w')
#file.write(j)
#file.close()

port = PORT_ANY
server_socket = create_bluetooth_server_socket(port)

uuid = "00000003-0000-1000-8000-00805F9B34FB"
advertise_service( server_socket, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ])

while True:    
    print "waiting for incoming connections"

    client_socket, address = server_socket.accept()
    ##TODO Security
    try:
        security = SecurityManager(client_socket)
        break
    except Exception:
        print "log in canceled by user"
        abort = {"action":"ABORT", "message":"Incorrect user name or password"}
        j = json.dumps(abort)
        client_socket.send(j)


succes = {"action":"LOGIN_OK"}
client_socket.send(json.dumps(succes))

name = "Rauly"
print "connected to", "("+address[0]+")"

#file1 = os.open("C:\Users\Rauly\Desktop\shakir1.jpg", os.O_RDONLY|os.O_BINARY)
#file2 = os.open("C:\Users\Rauly\Desktop\shakir2.jpg", os.O_RDONLY|os.O_BINARY)
#file = file1
#j = {"action":"STORE", "name":"Bail.jpg", "append":False}
#client_socket.send(json.dumps(j))
#succes = {"action":"EOF"}

#while True:
#    s = "go"
#    while s != "":        
#        s = os.read(file, 5000)
#        #h = {"action":"STORE", "name":"Bail.avi", "append":False}
#        client_socket.send(s)
#        #client_socket.send(s)
#        #print "s"        
#        sleep(0.05)
    
#    print "done"    
#    client_socket.send(json.dumps(succes))
#    sleep(5)
#    client_socket.send(json.dumps(j))
#    file = file1 if file == file2 else file2

#print "done"
#succes = {"action":"EOF"}
#client_socket.send(json.dumps(succes))

t = Thread(target=read, args=())
t.daemon = True
t.start()
while True:
    try:
        client_socket.send("Hi")
    except IOError, e:
        print e
        print "disconnected"
        print "waiting for reconnect"
        client_socket, address = server_socket.accept()
        succes = {"action":"LOGIN_OK"}
        client_socket.send(json.dumps(succes))
        print "reconnected to", "("+address[0]+")"
        t = Thread(target=read, args=())
        t.daemon = True
        t.start()
    sleep(2)
