import time
import serial

class serialConnect(object):
    def __init__(self, calibrateFlag = False):
        self.ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=9600,
        timeout=None,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
        )
        self.isopen = self.ser.isOpen()

    def open(self):
        self.ser.open()

    def close(self):
        self.ser.close()

    def sendSerialdata(self,packet):
        self.ser.flushOutput()
        self.ser.flushInput()
        self.ser.write(packet)
        self.ser.flush()
        out = ''
        line = ''
        print "waiting for data"
        while out!='\n':
            out = self.ser.read(1)
            line +=out
        print line