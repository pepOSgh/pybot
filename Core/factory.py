__author__ = 'pepOS'


class Factory:
    def __init__(self, classesmodule, data):
        self._storage = {}

        for elem in data:
            self._storage[elem] = getattr(classesmodule, data[elem][0])(elem)

    def get_instance(self, name):
        return self._storage[name]

    def avaliableRobotParts(self):
        return self._storage.keys()

    def ValidateDependencies(self, servicesData):
        compliantMethods = {}
        noCompliantMethods = {}
        for service in servicesData:
            dependencies = servicesData[service][-1].split(',')
            missing = []
            for dep in dependencies:
                if not self._storage.has_key(dep):
                    missing.append(dep)

            if len(missing) == 0:
                compliantMethods[service] = [servicesData[service][0],  servicesData[service][1],  servicesData[service][2], servicesData[service][3]]
            else:
                noCompliantMethods[service] =missing

        return compliantMethods, noCompliantMethods