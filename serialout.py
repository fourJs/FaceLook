import time
import serial

class serialConnect(object):
    def __init__(self, calibrateFlag = False):
        self.ser = serial.Serial(
        port='/dev/ttyACM1',
        baudrate=9600,
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
        self.ser.write(str(packet)+';')
        time.sleep(0.05)
