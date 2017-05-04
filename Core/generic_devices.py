__author__ = 'pepOS'


class Device(object):
    def __init__(self, address):
        self.address = address
        self.protocol = None

    def write(self, data):
        assert 0, 'action must be defined!'

    def read(self, size):
        assert 0, 'action must be defined!'

    def protocol(self):
        assert 0, 'action must be defined!'


class Component(object):
    def __init__(self, name):
        self.__name = name

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    Name = property(getName, setName)


class Motor(Component):
    def __init__(self, name):
        Component.__init__(self, name)
        self.w = 0
        self.pwm = 128  #TODO ver con que se inicializa
        self.current = 0

    def getw(self):
        return self.w

    def setw(self, value):
        assert 0, 'action must be defined!'

    def getpwm(self):
        return self.pwm

    def setpwm(self, value):
        assert 0, 'action must be defined!'

    def getcurrent(self):
        assert 0, 'action must be defined!'


class Sensors(Component):
    def __init__(self, name):
        Component.__init__(self, name)

    def getValue(self):
        assert 0, 'action must be defined!'


class Ranger(Sensors):
    def __init__(self):
        self.var = 0

    def tflight(self):
        return self.var

    def angle(self):
        return self.var


class Ultrasonic:
    def __init__(self):
        self.var = 0

    def tflight(self):
        return self.var


class Button(Component):
    def __init__(self, name):
        Component.__init__(self, name)
        self.isPressed = False

    def isPressed(self):
        assert 0, 'action must be defined!'


class Led(Component):
    def __init__(self, name):
        Component.__init__(self, name)
        self.power = 0
        self.intensity = 0

    def getIntensity(self):
        return self.intensity

    def setIntensity(self, value):
        self.intensity = value

    def getPower(self):
        return self.power

    def setPower(self, value):
        self.power = value


class Speaker(Component):
    def __init__(self, name):
        Component.__init__(self, name)

    def playSound(self):
        assert 0, 'action must be defined!'


class Camera:
    def __init__(self):
        self.frame = 0

    def get_frame(self):
        assert 0, 'action must be defined!'