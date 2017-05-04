__author__ = 'pepOS'


from Behaviors.baseBehavior import *
from Applications.differentialMotor import *
import time

class AvoidObstaclesDiffMotor(BaseBehavior):
    def __init__(self, factory):
        BaseBehavior.__init__(self, factory)

    def run_algorithm(self):
        diffMotor = DifferentialMotor(self.factory)
        leftBumper = self.factory.get_instance('LeftBumper')
        rightBumper = self.factory.get_instance('RightBumper')
        horn = self.factory.get_instance('Speaker')

        velocity = 150
        diffMotor.forward(velocity)


        while True:
            if rightBumper.getValue():
                horn.playSound()
                diffMotor.backward(velocity)
                time.sleep(1.5)
                diffMotor.turnLeft(velocity)
                time.sleep(0.5)
                diffMotor.forward(velocity)

            if leftBumper.getValue():
                horn.playSound()
                diffMotor.backward(velocity)
                time.sleep(1.5)
                diffMotor.turnRight(velocity)
                time.sleep(0.5)
                diffMotor.forward(velocity)
            time.sleep(0.015)

