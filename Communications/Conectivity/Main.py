from ConnectivityManager import * 
import struct 
from serial_utils import * 
from threading import Thread

serialport = newSerialPort()

class iRobotControler:

    def __init__(self):
        serialport.send(self.encode_msg(128, 131))
        sleep(1.5)
        serialport.send(self.encode_msg(140, 1, 4, 88, 32, 30, 32, 30, 32, 30, 32))
        pass

    def getCapabilities(self):
        caps = [{"name":"forward", "params":"int", "nature":"in", "description":"Move forward"}, 
                 {"name":"backward", "params":"int", "nature":"in", "description":"Move backward"},
        		 {"name":"stop", "params":"", "nature":"in", "description":"Stop"},
        		 {"name":"turnRight", "params":"", "nature":"in", "description":"Turn right"},
        		 {"name":"turnLeft", "params":"", "nature":"in", "description":"Turn left"}]
        return caps

    def encode_msg(self, *data):
        print data
        fmt = 'B' * len(data)
        print fmt
        return struct.pack(fmt, *data)

    def bytehl(self, number, nbits):
    	val = (number + (1 << nbits)) % (1 << nbits)
    	temp = bin(val)[-len(bin(val))+2:]
    	hg = temp[:-nbits/2]
    	if hg == '':
            hg = '0b0'
        lw = '0b' + temp[-nbits/2:]
    	return int(hex(int(hg, 2)), 16), int(hex(int(lw, 2)), 16)

    def forward(self, vel):
        h, l = self.bytehl(vel, 16)
        serialport.send(self.encode_msg(137, h, l, 127, 255))
            
    def backward(self, vel):
        h, l = self.bytehl(-vel, 16)
        serialport.send(self.encode_msg(137, h, l, 127, 255))

    def stop(self):
        serialport.send(self.encode_msg(145, 0, 0, 0, 0))

    def turnLeft(self, vel, direction):
        velocity = vel
        if direction == -1:
            velocity = -vel
        h, l = self.bytehl(velocity, 16)
        h1, l1 = self.bytehl(velocity/2, 16)
        serialport.send(self.encode_msg(145, h, l, h1, l1))

    def turnRight(self, vel, direction):
        velocity = vel
        if direction == -1:
            velocity = -vel
        h, l = self.bytehl(velocity, 16)
        h1, l1 = self.bytehl(velocity/2, 16)
        serialport.send(self.encode_msg(145, h1, l1, h, l))
        

conn = ConnectivityManager()
controler = iRobotControler()
conn.join(controler)

while True:
    try:
        conn.startListening()
        conn.startReading()
    except Exception, e:
        print e
        print "Wait a seconds ..."
        sleep(1)
