__author__ = 'pepOS'

import serial


class SerialPort():
    def __init__(self, port='/dev/ttyUSB0', baudrate=57600):
        self.serialconn = serial.Serial(port=port, baudrate=baudrate)
        self.open()

    def open(self):
        if not self.serialconn.isOpen():
            self.serialconn.open()

    def send(self, data):
        self.serialconn.write(data)

    def read(self, size):
        return self.serialconn.read(size=size)

    def close(self):
        if self.serialconn.isOpen():
            self.serialconn.close()

