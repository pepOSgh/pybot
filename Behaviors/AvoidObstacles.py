__author__ = 'pepOS'

import time
from Behaviors.baseBehavior import *


class AvoidObstacles(BaseBehavior):
    def __init__(self, factory):
        BaseBehavior.__init__(self, factory)

    def run_algorithm(self):

        leftBumper = self.factory.get_instance('LeftBumper')
        rightBumper = self.factory.get_instance('RightBumper')
        leftMotor = self.factory.get_instance('LeftMotor')
        rightMotor = self.factory.get_instance('RightMotor')
        horn = self.factory.get_instance('Speaker')

        velocity = 150
        leftMotor.setw(velocity)
        rightMotor.setw(velocity)

        while True:
            if rightBumper.getValue():
                horn.playSound()
                leftMotor.setw(-velocity)
                rightMotor.setw(-velocity)
                time.sleep(1.5)
                leftMotor.setw(-velocity)
                rightMotor.setw(velocity)
                time.sleep(0.5)
                leftMotor.setw(velocity)
                rightMotor.setw(velocity)

            if leftBumper.getValue():
                horn.playSound()
                leftMotor.setw(-velocity)
                rightMotor.setw(-velocity)
                time.sleep(1.5)
                leftMotor.setw(velocity)
                rightMotor.setw(-velocity)
                time.sleep(0.5)
                leftMotor.setw(velocity)
                rightMotor.setw(velocity)
            time.sleep(0.015)