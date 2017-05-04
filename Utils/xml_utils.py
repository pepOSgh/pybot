__author__ = 'pepOS'

from xml.etree.ElementTree import ElementTree


def xml_loader(data):
    tree = ElementTree()
    tree.parse(data)
    return tree.getroot()


def robot_config_validator(file_root, fileformat):
    if not file_root.tag == 'robotConfig':
        return False, 'No robotConfig file loaded'
    else:
        for group in file_root:
            if not group.tag in fileformat:
                return False, '"%s" does`t exits in the desired format' % (group.tag)
            else:
                temp = fileformat[group.tag]
                for elem in group:
                    if not elem.tag in temp:
                        return False, 'The element "%s"  does`t belong to a robotConfig file.' %elem.tag
                    if not len(temp[elem.tag]) == len(elem.attrib):
                        return False, '"%s" and "%s" has different length '% (temp, str(elem.tag))
                    for att in elem.attrib:
                        if not att in temp[elem.tag]:
                            return False, '"%s" not found in "%s"' % (att, str(elem.tag))
        return True, ''


def robot_config_parser(file_root):
    fact_arg = {}
    methods = {}
    for group in file_root:
        for elem in group:
            if elem.tag == 'method':
                methods[elem.attrib['name']] = [elem.attrib['class'], elem.attrib['params'], elem.attrib['returns'], elem.attrib['description'], elem.attrib['dependencies']]
                #TODO sale string
            elif elem.tag == 'component':
                fact_arg[elem.attrib['name']] = [elem.attrib['class'], elem.attrib['genericDevice']]
            elif elem.tag == 'sensor':
                fact_arg[elem.attrib['name']] = [elem.attrib['class'], elem.attrib['genericDevice']]
    return fact_arg, methods


def pybot_config_validator(file_root, fileformat):
    if not file_root.tag == 'pybotConfig':
        return False, 'No pybotConfig file loaded'
    else:
        for element in file_root:
            if not element.tag in fileformat:
                return False, '"%s" does`t exits in the desired format' % (element.tag)
            if not len(fileformat[element.tag]) == len(element.attrib):
                return False, '"%s" and "%s" has different length '% (fileformat[element], str(element.tag))
            for att in element.attrib:
                if not att in fileformat[element.tag]:
                    return False, '"%s" not found in "%s"' % (att, str(element.tag))

        return True, ''


def pybot_config_parser(file_root):
    result = {}
    for element in file_root:
        if element.tag == 'Server':
            result[element.tag] = {'address': element.attrib['address'],
                                   'port': int(element.attrib['port']),
                                   'services': element.attrib['services']
                                   }
        else:
            result[element.tag] = {'name': element.attrib['name']}
    return result