__author__ = 'pepOS'

from comms import *
from Conectivity.ConnectivityManager import *
import time

conn = ConnectivityManager()
time.sleep(4)
a = Modulator('127.0.0.1', 5000)
conn.join(a)

while True:
    try:
        conn.startListening()
        conn.startReading()
    except Exception, e:
        print e
        print "Wait a seconds ..."
        sleep(1)
