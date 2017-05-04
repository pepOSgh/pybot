__author__ = 'pepOS'

from Core.generic_devices import *
from Utils.communications_utils import *
from Utils.convertion_utils import *
from Protocols.serial_protocol import *

import time
import threading


serialport = SerialPort()
serialport.send(encode_msg(128, 131))
time.sleep(1.5)


class IRobotSensorsBag:

    def __init__(self, updateInterval):
        self._storage = ()
        self.updateInterval = updateInterval
        self.thread = None

    def update_values(self):
        serialport.send(encode_msg(142, 6))
        result = serialport.read(52)
        self._storage = decode_msg('B??????BxxBBhhBHhbHHHHHHHBHBBB?Bhhhh', result)

    def getvalues(self):
        return self._storage

    def startAutoUpdate(self):
        self.update_values()
        self.thread = threading.Timer(self.updateInterval, self.startAutoUpdate)
        self.thread.daemon = True
        self.thread.start()

    def stopAutoUpdate(self):
        self.thread.cancel()

class IrobotMotor(Motor):

    def __init__(self, name):
        Motor.__init__(self, name)

    def setw(self, value):
        if value < -500:
            value = -500

        elif value > 500:
            value = 500

        return bytehl(value, 16)

    def setpwm(self, value):
        self.pwm = value
        serialport.send((144, value))  #TODO ver lo del valueo los bits. y si se pasa a los herederos.


class IrobotLeftMotor(IrobotMotor):

    def __init__(self, name):
        Motor.__init__(self, name)

    def setw(self, value):
        self.w = value
        high, low = IrobotMotor.setw(self, value)


        serialport.send((encode_msg(142, 41)))
        actualRightVelocity = int(decode_msg('h', serialport.read(2))[0])
        
        rvHigh, rvLow = IrobotMotor.setw(self, actualRightVelocity)

        serialport.send(encode_msg(145, rvHigh, rvLow, high, low))


    def setpwm(self, value):
        self.pwm = value
        porcent = (value*128)/100
        serialport.send(encode_msg(144, porcent, porcent, porcent))


class IrobotRightMotor(IrobotMotor):

    def __init__(self, name):
        Motor.__init__(self, name)

    def setw(self, value):
        self.w = value
        high, low = IrobotMotor.setw(self, value)

        serialport.send((encode_msg(142, 42)))
        actualLeftVelocity = int(decode_msg('h', serialport.read(2))[0])
        
        lvHigh, lvLow = IrobotMotor.setw(self, actualLeftVelocity)

        serialport.send(encode_msg(145, high, low, lvHigh, lvLow))

    def setpwm(self, value):
        assert 0, 'action must be defined!'


class Speaker(Speaker):
    def __int__(self, name):
        Speaker.__init__(self, name)

    def playSound(self):
        serialport.send(encode_msg(140, 1, 1, 88, 32))
        serialport.send(encode_msg(141, 1))


class LeftBumper(Sensors):
    def __init__(self, name):
        Sensors.__init__(self, name)

    def getValue(self):
        serialport.send(encode_msg(142, 7))
        return int(stdlen8(decode_msg('B', serialport.read(1))[0])[-2], 2) #ver por que sale una tupla y no el nu solo.


class RightBumper(Sensors):
    def __init__(self, name):
        Sensors.__init__(self, name)

    def getValue(self):
        serialport.send(encode_msg(142, 7))
        return int(stdlen8(decode_msg('B', serialport.read(1))[0])[-1], 2)
        # return  bin(decode_msg('B', serialport.read(1)))[-1]


class LeftWheeldrop(Sensors):
    def __init__(self, name):
        Sensors.__init__(self, name)

    def getValue(self):
        serialport.send(encode_msg(142, 7))
        return int(stdlen8(decode_msg('B', serialport.read(1))[0])[-4], 2)
        # return  bin(decode_msg('B', serialport.read(1)))[-4]


class CasterWheeldrop(Sensors):
    def __init__(self, name):
        Sensors.__init__(self, name)

    def getValue(self):
        serialport.send(encode_msg(142, 7))
        return int(stdlen8(decode_msg('B', serialport.read(1))[0])[-5], 2)


class RightWheeldrop(Sensors):
    def __init__(self, name):
        Sensors.__init__(self, name)

    def getValue(self):
        serialport.send(encode_msg(142, 7))
        return int(stdlen8(decode_msg('B', serialport.read(1))[0])[-3], 2)
        # return bin(decode_msg('B', serialport.read(1)))[-3]


class Wall(Sensors):

    def __init__(self, name):
         Sensors.__init__(self, name)

    def getValue(self):
        serialport.send(encode_msg(142, 8))
        return decode_msg('?', serialport.read(1))[0]


class CliffLeft(Sensors):

    def __init__(self, name):
        Sensors.__init__(self, name)

    def getValue(self):
        serialport.send(encode_msg(142, 9))
        return decode_msg('?', serialport.read(1))[0]


class CliffFrontLeft(Sensors):

    def __init__(self, name):
        Sensors.__init__(self, name)

    def getValue(self):
        serialport.send(encode_msg(142, 10))
        return decode_msg('?', serialport.read(1))[0]


class CliffFrontRight(Sensors):

    def __init__(self, name):
        Sensors.__init__(self, name)

    def getValue(self):
        serialport.send(encode_msg(142, 11))
        return decode_msg('?', serialport.read(1))[0]


class CliffRight(Sensors):

    def __init__(self, name):
        Sensors.__init__(self, name)

    def getValue(self):
        serialport.send(encode_msg(142, 12))
        return decode_msg('?', serialport.read(1))[0]


class VirtualWall(Sensors):

    def __init__(self, name):
        Sensors.__init__(self, name)

    def getValue(self):
        serialport.send(encode_msg(142, 13))
        return decode_msg('?', serialport.read(1))[0]


class Infrared(Sensors):# TODO ver lo de la separacion de boolsensors y rangesensors

    def __init__(self, name):
        Sensors.__init__(self, name)

    def getValue(self):
        serialport.send(encode_msg(142, 17))
        return decode_msg('B', serialport.read(1))[0]


class PlayButton(Button):

    def __init__(self, name):
        Button.__init__(self, name)

    def isPressed(self):
        serialport.send(encode_msg(142, 18))
        return bin(stdlen8(decode_msg('B', serialport.read(1))[0]))[-1] #TODO idem abajo


class AdvanceButton(Button):

    def __init__(self, name):
        Button.__init__(self, name)

    def isPressed(self):
        serialport.send(encode_msg(142, 18))
        return bin(stdlen8(decode_msg('B', serialport.read(1))[0]))[-3]


class Distance(Sensors):

    def __init__(self, name):
        Sensors.__init__(self, name)

    def getValue(self):
        serialport.send(encode_msg(142, 19))
        return decode_msg('h', serialport.read(2))[0]


class Angle(Sensors):
    def __init__(self, name):
        Sensors.__init__(self, name)

    def getValue(self):
        serialport.send(encode_msg(142, 20))
        return decode_msg('h', serialport.read(2))[0]


class BatteryChargeLevel(Sensors):
    def __init__(self, name):
        Sensors.__init__(self, name)

    def getValue(self):
        serialport.send(encode_msg(142, 25))
        level = decode_msg('H', serialport.read(2))[0]
	return (level * 100) / 65535


def getallvalues():
    serialport.send(encode_msg(142, 6)) #Solicitando los valores de todos los sensores
    result = serialport.read(52) #Leyendo los valores de todos los sensores
    return decode_msg('B??????BxxBBhhBHhbHHHHHHHBHBBB?Bhhhh', result)







