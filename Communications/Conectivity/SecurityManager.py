import sys
import io
import json
import sets
import array
from time import *

class SecurityManager:

    def __init__(self):
        self.currentUser = ""
        self.currentPermission = -1

    def requestLogIn(self, socket, message = ""):
        serial = "";
        data = self.__requestLogin(socket, message)        

        if data["action"] == "login":
            login = data["user"]    #extraer las credenciales del cliente
            password = data["password"]
            serial = data["serial"]
            #cargar el fichero de los perfiles
            users = self.__getProfiles()
            try:
                user = users[login]
                self.currentUser = user
                self.currentPermission = user["permissions"]
            except:
                print "El nombre de usuario es incorrecto"
                return "El nombre de usuario es incorrecto"
                            
            if password != user["password"]:
                print "El password es incorrecto"
                return "El password es incorrecto"
            elif serial not in user["devices"]:
                data = self.__requestExLogin(socket)
                answer = "";
                if data["action"] == "exlogin":
                    answer = data["answer"]
                if user["answer"] == answer:
                    user["devices"].append(serial)
                    users[login] = user
                    self.__setProfiles(users)
                    print "Extended LogIn Ok"
                    return "";
                else:
                    print "El respuesta de seguridad es incorrecta"
                    raise Exception, "SecurityManager >> requestLogIn: La respuesta de seguridad es incorrecta"
            else:
                print "LogIn Ok"
                return "" 
        if data["action"] == "abort":
            return "abort"
        return "Invalid Action"

    #agregar un usuario
    def addUser(self, newLogin, newPass, newSQ, newAnswer, permission = 0):
        print "New User Request"
        if self.currentPermission < 1:
            raise Exception, "SecurityManager >> addUser: Not Enough Privileges"
        users = self.__getProfiles()

        if newLogin in users:
            raise NameError, "This user name already exsist"

        p = Profile(newLogin, newPass, newSQ, newAnswer, [], permission)
        
        users[newLogin] = p.getDict()
       
        self.__setProfiles(users)
        print "User Added Succesfully"
        
    #quitar un usuario
    def removeUser(self, user):
        print "Remove User Request"
        if self.currentPermission < 1:
            raise Exception, "SecurityManager >> removeUser: Not Enough Privileges"
        users = self.__getProfiles()

        if user in users:
            users.pop(user)

        self.__setProfiles(users)
        print "User Removed Succesfully"

    def changePermissions(self, user, permissions):
        print "Change Permissions Request"
        if self.currentPermission < 1:
            raise Exception, "Not Enough Privileges"
        users = self.__getProfiles()

        users[user]["permissions"] = permission

        self.__setProfiles(users)

    #cambiar las credenciales de un usuario
    def changeCredentials(self, newLogin, newPass, newSQ, newAnswer):
        print "Change Credentials Request"
        users = self.__getProfiles()

        p = users[self.currentUser]
        p["user"] = newLogin
        p["password"] = newPass
        p["question"] = newSQ
        p["answer"] = newAnswer
        users.pop(currentUser)
        users[newLogin] = p

        self.__setProfiles(users)
        
    def getCurrentUser(self):
        return self.currentUser["user"]

    def getCurrentPermissions(self):
        return self.currentUser["permissions"]

    def getAllUser(self):
        if self.currentPermission < 1:
            raise Exception, "SecurityManager >> getAllUsers: Not Enough Privileges"
        users = self.__getProfiles()

        all = []
        for i in users:
            all.append(i)
        return all

    def __requestLogin(self, socket, message = ""):
        print "LogIn Request"
        request = {"action":"intent", "target":"LOGIN", "message":message}
        str = json.dumps(request)
        socket.send(str) #enviar la peticion de seguridad al cliente
        print "LogIn request sended"
        response = socket.recv(1024) #esperar por la respuesta del cliente
        print "LogIn response received"
        data = json.loads(response)
        return data

    def __requestExLogin(self, socket):
        print "Extended LogIn Request"
        request = {"action":"intent", "target":"EXLOGIN", "question":self.currentUser["question"]}
        str = json.dumps(request)
        socket.send(str)
        print "Extended LogIn request sended"
        response = socket.recv(1024)
        data = json.loads(response)
        return data

    def __getProfiles(self):
        file = open("profiles.txt", 'r')
        str = file.readline()
        file.close()
        users = json.loads(str)
        return users

    def __setProfiles(self, users):
        str = json.dumps(users)
        file = open("profiles.txt", 'w')
        file.write(str)
        file.close()

class Profile:

    def __init__(self, name, password, question, answer, devices = [], permission = 0):
        self.UserName = name
        self.Password = password
        self.SecutityAnswer = answer
        self.SecurityQuestion = question
        self.AllowedDevices = devices
        self.Permissions = permission

    @property
    def UserName(self):
        return self.__login

    @UserName.setter
    def UserName(self, name):
        self.__login = name

    @property
    def Permissions(self):
        return self.__permissions

    @Permissions.setter
    def Permissions(self, permissions):
        self.__permissions = permissions
    
    @property
    def Password(self):
        return self.__pass                  

    @Password.setter
    def Password(self, password):
        self.__pass = password

    @property
    def SecurityQuestion(self, question):
        self.__question = question

    @SecurityQuestion.setter
    def getSecurityQuestion(self):
        return self.__question

    @property
    def SecutityAnswer(self, answer):
        self.__answer = answer

    @SecutityAnswer.setter
    def SecurityAnswer(self):
        return self.__answer

    @property
    def AllowedDevices(self):
        return self.__devices

    @AllowedDevices.setter
    def AllowedDevices(self, devices):
        self.__devices = devices

    def getDict(self):
        dict = {"user":self.UserName, "password":self.Password, "question":self.SecurityQuestion, 
                "answer":self.SecutityAnswer, "devices":self.AllowedDevices, "permissions":self.Permissions}
        return dict