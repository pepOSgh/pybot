__author__ = 'pepOS'

from Core.factory import *
from Utils.xml_utils import *
from importlib import import_module
from Utils.communications_utils import Modulator
from Communications.API_REST import *
from Communications.Conectivity.ConnectivityManager import *

import time


PYBOT_TELECOMMAND = 0
PYBOT_AUTONOMIC = 1

def start_Pybot_Platform(mode=PYBOT_AUTONOMIC):


    pybotXMLData = xml_loader('pybotConfig.xml')

    pybotfileformat = {'RobotConfigFile': ['name'],
                       'ControllersModule': ['name'],
                       'Behavior': ['name'],
                       'Server': ['address', 'port', 'services']
                       }

    correct, errorNote = pybot_config_validator(pybotXMLData, pybotfileformat)

    if not correct:
        raise Exception(errorNote)

    pybotParams = pybot_config_parser(pybotXMLData)


    robotXMLData = xml_loader(pybotParams['RobotConfigFile']['name'])

    robotfileformat = {'components': {'component': ['name', 'class', 'genericDevice']},
                       'sensors': {'sensor': ['name', 'class', 'genericDevice']},
                       'publicMethods': {'method': ['name', 'class', 'params', 'returns', 'description', 'dependencies']}
                       }

    correct, errorNote = robot_config_validator(robotXMLData, robotfileformat)

    if not correct:
        raise Exception(errorNote)


    robotParts, methods = robot_config_parser(robotXMLData)

    controllersModule = import_module('..' + pybotParams['ControllersModule']['name'], 'Controllers.subpkg')


    factory = Factory(controllersModule, robotParts)

    if mode == PYBOT_AUTONOMIC:
        behaviorModule = import_module('..' + pybotParams['Behavior']['name'], 'Behaviors.subpkg')
        behaviorClass = getattr(behaviorModule, pybotParams['Behavior']['name'])
        behavior = behaviorClass(factory)
        behavior.run_algorithm()

    if mode == PYBOT_TELECOMMAND:
        supportedMethods, unSupportedMethods = factory.ValidateDependencies(methods)

        if not len(unSupportedMethods) == 0:
            for unsuppMethod in unSupportedMethods:
                print 'Unsupported Method '+ unsuppMethod + ' .The following dependencies are missing: ' + str(unSupportedMethods[unsuppMethod])

        serviceModule = import_module('..services', 'Communications.subpkg')
        serviceModule.init(factory)
        server = REST_Server(serviceModule, supportedMethods)

        th = Thread(target=runConnectionManagers, args=(server.address, server.port,))
        th.daemon = True
        th.start()

        server.run()


def runConnectionManagers(serverAddress, serverPort):
    time.sleep(5)
    conn = ConnectivityManager()
    a = Modulator(serverAddress, serverPort)
    conn.join(a)

    while True:
        try:
            conn.startListening()
            conn.startReading()
        except Exception, e:
            print e
            print "Wait a seconds ..."
            sleep(1)

start_Pybot_Platform(PYBOT_TELECOMMAND)
