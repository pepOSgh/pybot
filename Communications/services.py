__author__ = 'pepOS'


import API_REST
import json


factory = None


def init(factoryArg):
    global factory
    factory = factoryArg


class ForwardService(API_REST.PybotService):
    def get(self):
        velocity = API_REST.request.json['velocity']

        leftMotor = factory.get_instance('LeftMotor')
        rightMotor = factory.get_instance('RightMotor')

        leftMotor.setw(velocity)
        rightMotor.setw(velocity)


class BackwardService(API_REST.PybotService):
    def get(self):
        velocity = API_REST.request.json['velocity']

        leftMotor = factory.get_instance('LeftMotor')
        rightMotor = factory.get_instance('RightMotor')

        leftMotor.setw(-velocity)
        rightMotor.setw(-velocity)


class TurnLeftService(API_REST.PybotService):
    def get(self):
        velocity = API_REST.request.json['velocity']
        direction = API_REST.request.json['direction']

        if direction == -1:
            velocity = -velocity

        leftMotor = factory.get_instance('LeftMotor')
        rightMotor = factory.get_instance('RightMotor')

        leftMotor.setw(velocity/2)
        rightMotor.setw(velocity)


class TurnRightService(API_REST.PybotService):
    def get(self):
        velocity = API_REST.request.json['velocity']
        direction = API_REST.request.json['direction']
        if direction == -1:
            velocity = -velocity

        leftMotor = factory.get_instance('LeftMotor')
        rightMotor = factory.get_instance('RightMotor')

        leftMotor.setw(velocity)
        rightMotor.setw(velocity/2)


class StopService(API_REST.PybotService):
    def get(self):
        leftMotor = factory.get_instance('LeftMotor')
        rightMotor = factory.get_instance('RightMotor')

        leftMotor.setw(0)
        rightMotor.setw(0)


class BatteryChargeLevelService(API_REST.PybotService):
    def get(self):
        batteryCL = factory.get_instance('BatteryChargeLevel')
        value = batteryCL.getValue()
        return {'value': value}


class LeftBumperService(API_REST.PybotService):
    def get(self):
        lBumber = factory.get_instance('LeftBumper')
        value = lBumber.getValue()
        return {'value': value}


class RightBumperService(API_REST.PybotService):
    def get(self):
        rBumber = factory.get_instance('RightBumper')
        value = rBumber.getValue()
        return {'value': value}
