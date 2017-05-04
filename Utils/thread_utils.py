__author__ = 'pepOS'

import threading

class ThreadManager:
    def __init__(self):
        self.activeThreads = {}

    #TODO: Controlar los hilos con los nombres que no exista dos hilos a una misma cosa por el mismo controller
    def runOnNewThread(self, name=None, target=None, args=(), kwargs={}):
        temp = threading.Thread(name=name, target=target, args=args, kwargs=kwargs)
        if temp.name in self.activeThreads:
            raise Exception('The thread is already running')
        else:
            self.activeThreads[temp.name] = temp
            temp.start()

    def runTimedTask(self, target=None, args=(), kwargs={}, time=0.5):
        temp = threading.Timer(time, target, args, kwargs)
        temp.start()


    def runSyncThread(self, name=None, target=None, args=(), kwargs={}, blocking=0):
        temp = threading.Thread(name=name, target=target, args=args, kwargs=kwargs)
        threadLock = threading.Lock()
        threadLock.acquire(blocking)
        temp.start()
        threadLock.release()

    def getThread(self, name):
        return self.activeThreads[name]

    def getThreads(self):
        return threading.enumerate()