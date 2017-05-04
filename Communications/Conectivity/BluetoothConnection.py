from bluetooth import *
from threading import *

class BluetoothConnection:

    def __init__(self, port):
        self.isConnected = False
        self.listening = False
        
        if port < 0 or port > 30: raise BluetoothError, "BluetoothConnection >> __init__: Invalid Port"
        
        server_socket = BluetoothSocket(RFCOMM)
        server_socket.bind(("", port))
        server_socket.listen(1)
        print "Bluetooth Socket Created"

        uuid = "00000003-0000-1000-8000-00805F9B34FB"
        advertise_service( server_socket, "SampleServer",
                           service_id = uuid,
                           service_classes = [ uuid, SERIAL_PORT_CLASS ],
                           profiles = [ SERIAL_PORT_PROFILE ])

        self.__server_socket__ = server_socket
        self.__client_socket__ = None
        print "Bluetooth Service Advertised"

    def startListening(self):   
        print "Bluetooth Listener Starting"
        if sys.platform == "linux2":
            os.system("sudo hciconfig hci0 piscan")
        self.listening = True

        #TODO put this on a separated thread
        client_socket, address = self.__server_socket__.accept()
        print "Bluetooth Connection Stablished"
        self.listening = False
        #

        self.__client_socket__ = client_socket
        self.remoteAddr = address
        self.stopListening()
        
    def stopListening(self):
        if sys.platform == "linux2":
            os.system("sudo hciconfig hci0 noscan")
        currentThread()._Thread__stop()
        print "Bluetooth Listener Stoped"

    def send(self, data):
        self.__client_socket__.send(data)
        print "Data Sended Over Bluetooth"
    
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

    def isEnabled(self):
        return self.enabled

    def isListening(self):
        return self.listening

    def reset(self):
        self.__client_socket__.close()

    def __getSocket__(self):
        return self.__client_socket__