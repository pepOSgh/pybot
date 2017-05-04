__author__ = 'pepOS'

from flask import Flask, request, jsonify
from flask.ext import restful
import json
import os


app = Flask(__name__)
api = restful.Api(app)
tokensID = []
providedServices = []

class REST_Server:

    def __init__(self, module, services, address='127.0.0.1', port=5000):
        self.address = address
        self.port = port
        self._addServices(module, services)
        global providedServices
        providedServices = self._serviceInfoBuilder(services)

    def getServiceInfo(self):
        return providedServices

    def run(self):
        app.run(host=self.address, port=self.port, debug=True)

    def _addServices(self, servicesModule, methods):
        for service in methods:
            url = self._urlComposer(service, methods[service])
            api.add_resource(getattr(servicesModule, methods[service][0]), url)

    def _urlComposer(self, service, info):
        url = '/services/%s' %(service)
        # if not info[1] == '':
        #     param = '/<%s>' % (info[1])
        #     url += param
        return url

    def _serviceInfoBuilder(self, methods):
        result = []
        regInfo = {'name': 'register',
                   'params': self.InfoBuilder(''),
                   'return': self.InfoBuilder('string:token'),
                   'description': 'Register a user in the Server.'
                   }
        result.append(regInfo)

        servInfo = {'name': 'services',
                    'params': self.InfoBuilder(''),
                    'return': self.InfoBuilder('list:services'),
                    'description': 'Description list of the available services'
                    }

        result.append(servInfo)

        verInfo = {'name': 'verifyKey',
                   'params': self.InfoBuilder('string:token'),
                   'return': self.InfoBuilder('bool:registered'),
                   'description': 'Verify if the provided token is registered in the server.'
                   }

        result.append(verInfo)

        for service in methods:
            temp = {}
            temp['name'] = service
            temp['params'] = self.InfoBuilder(methods[service][1])
            temp['return'] = self.InfoBuilder(methods[service][2])
            temp['description'] = methods[service][3]
            result.append(temp)
        return result

    def InfoBuilder(self, info):
        if info == '':
            return []
        else:
            result = []
            data = info.split(',')
            for elem in data:
                temp = elem.split(':')
                result.append({'type': temp[0], 'name': temp[1]})
            return result


class PybotService(restful.Resource):

    def get(self):
        assert 0, 'action must be define!'

    def post(self):
        assert 0, 'action must be define!'


@app.route('/services', methods=['GET'])
def avaliableServices():
    return json.dumps({'services': providedServices})
    # return jsonify({'services': providedServices})


@app.route('/services/register', methods=['GET'])
def addToken():
    token = os.urandom(24)
    while token in tokensID:
        token = os.urandom(24)

    tokensID.append(token)
    return json.dumps({'token': token}, encoding='ISO-8859-1')

@app.route('/services/verifyKey', methods=['GET'])
def verifyKey():
    key = request.json['token']
    #print 'KEY------------------>' + key
    key = key.encode('ISO-8859-1')

    result = key in tokensID
    return json.dumps({'registered': result}, encoding='ISO-8859-1')


#TODO poner los errores de app.
