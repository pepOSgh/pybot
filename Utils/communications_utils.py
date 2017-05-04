__author__ = 'pepOS'

import struct
import json
import httplib2

def encode_msg(*data):
    #print data
    fmt = 'B' * len(data)
    #print fmt
    return struct.pack(fmt, *data)


def decode_msg(fmt, data):
    result = struct.unpack('>'+fmt, data)
    return result


class Modulator():

    def __init__(self, address, port):
        self.connection = httplib2.Http()
        self.serverAddr = 'http://' + address + ':' + str(port)
        self.avaliableServices = self.serverInfo()

    def serverInfo(self):
        (response, data) = self.connection.request(self.serverAddr+'/services', 'GET', json.dumps({}), headers={'Content-type':'application/json'})
        return json.loads(data)

    def getCapabilities(self):
        (response, data) = self.connection.request(self.serverAddr+'/services', 'GET', json.dumps({}), headers={'Content-type':'application/json'})
        # return json.loads(data)
        services = json.loads(data)
        result =[]
        for service in services['services']:
            temp = {}
            temp['name'] = service['name']
            temp['description'] = service['description']
            storedParams = []
            length = 0
            for param in service['params']:
                storedParams.append(param['type'])
                if length < len(service['params'])-1:
                    storedParams.append(',')
                length += 1

            strParams = ''.join(storedParams)
            temp['params'] = strParams

	    storedReturns = []
	    length = 0
	    temp['nature'] = 'in'
	    for returnValue in service['return']:
		temp['nature'] = 'out'
                storedReturns.append(returnValue['type'])
                if length < len(service['return'])-1:
                    storedReturns.append(',')
                length += 1
            
	    strReturn = ''.join(storedReturns)
	    temp['return'] = strReturn
            result.append(temp)
        return result

    def ApiRESTCall(self, data):
        header = {'Content-type': 'application/json'}
        #verficar si el token del usuario esta registrado
        if not data['action'] == 'register':
            url = self.serverAddr + '/services/verifyKey'
            method = 'GET'
            params = {'token': data['token']}
            (response, responseData) = self.connection.request(url, method, json.dumps(params, encoding='ISO-8859-1'), headers=header)

            jResponse = json.loads(responseData)
            if not jResponse['registered']:
                assert 0, 'User not registered'

        url = self.serverAddr + '/services/' + data['action']
        method = 'GET'
        servicesData = self.avaliableServices['services']
        desiredService = filter(lambda x: x['name'] == data['action'], servicesData)[0]
        if desiredService == ():
            assert 0, 'Service not defined'

        params = {}
        serviceParams = desiredService['params']

        if len(serviceParams) > 0:
            valuePos = 0
            for paramValue in data['params']:
                paramName = serviceParams[valuePos]['name']
                params[paramName] = paramValue
                valuePos += 1
        (response, data) = self.connection.request(url, method, json.dumps(params), headers=header)

	returnValues = json.loads(data)

        serviceReturn = desiredService['return']

        result = []
        if len(serviceReturn) > 0:
	    for serviceReturnValue in serviceReturn:
		result.append(returnValues[serviceReturnValue['name']])
        return result
