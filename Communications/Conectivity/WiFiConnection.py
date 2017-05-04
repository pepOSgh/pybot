from socket import *
from select import *
from threading import *

class WiFiConnection:

    def __init__(self, port):
        self.isConnected = False
        self.listening = False
        
        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.bind(("", port))
        server_socket.setblocking(False)

        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.bind(("192.168.1.7", 8000))
        client_socket.listen(1)
        self.__broadcast_socket__ = server_socket
        self.__server_socket__ = client_socket
        self.__client_socket__ = None
        print "WiFi Server Socket Created"

    def startListening(self):   
        print "WiFi Listener Starting"
        self.listening = True

        self.__advertiseThread__ = Thread(target = self.__startAdvertising__, args = ())
        self.__advertiseThread__.daemon = True
        self.__advertiseThread__.start()

        conn, addr = self.__server_socket__.accept()
        print "WiFi Connection Stablished with ", addr
        self.listening = False
        self.__stopAdvertising__()

        self.__client_socket__ = conn
        self.remoteAddr = addr
        currentThread()._Thread__stop()
        print "WiFi Listener Finished"
        
    def stopListening(self):
        currentThread()._Thread__stop()
        print "WiFi Listener Stoped"

    def send(self, data):
        self.__client_socket__.send(data)
        print "Data Sended Over WiFi"
    
    def isConnected(self):
        try:
            self.send("Hi")
            return True
        except IOError, e:
            print e
            return False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    @property
    def isEnabled(self):
        return self.enabled

    def isListening(self):
        return self.listening

    def reset(self):
        self.__client_socket__.close()

    def __startAdvertising__(self):
        print "WiFi Service Advertised"

        while self.__advertiseThread__.isAlive():
            result = select([self.__broadcast_socket__], [], [])
            msg = result[0][0].recvfrom(1024)
            print "Identification Requested by ", msg      
            self.__broadcast_socket__.sendto("WFRaspi", msg[1])

    def __stopAdvertising__(self):
        self.__advertiseThread__._Thread__stop()

    def __getSocket__(self):
        return self.__client_socket__