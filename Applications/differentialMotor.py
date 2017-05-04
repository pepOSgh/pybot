__author__ = 'pepOS'

from Applications.base_app import BaseApp
import time


class DifferentialMotor(BaseApp):

    def __init__(self, factory):
        BaseApp.__init__(self, factory)
        self.leftMotor = factory.get_instance('LeftMotor')
        self.rightMotor = factory.get_instance('RightMotor')

    def forward(self, velocity):
        self.leftMotor.setw(velocity)
        self.rightMotor.setw(velocity)

    def backward(self, velocity):
        self.leftMotor.setw(-velocity)
        self.rightMotor.setw(-velocity)

    def turnLeft(self, velocity):
        self.leftMotor.setw(velocity)
        self.rightMotor.setw(-velocity)

    def turnRight(self, velocity):
        self.leftMotor.setw(-velocity)
        self.rightMotor.setw(velocity)

    def stop(self):
        self.leftMotor.setw(0)
        self.rightMotor.setw(0)