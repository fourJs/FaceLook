import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
from nanpy import Servo
import time
import threading
import Queue
from nanpy import ArduinoApi
from nanpy import SerialManager
# import pyowm
# from os import system


class PiControl(object):
    """receieve data from pc and contril pi to tilt and pan"""
    def __init__(self):
        self.initConnection()
        connection = SerialManager(device='/dev/ttyACM0')

        self.a = ArduinoApi(connection = connection)
        self.servo_tilt = Servo(3)
        self.prePhi = 90
        # self.q = Queue.LifoQueue()
        self.q = Queue.Queue()
        self.a.pinMode(8, self.a.OUTPUT)
        self.a.pinMode(9, self.a.OUTPUT)
        self.a.pinMode(10, self.a.OUTPUT)
        self.a.pinMode(11, self.a.OUTPUT)
        self.a.pinMode(5, self.a.OUTPUT)
        self.a.pinMode(6, self.a.OUTPUT)

    def initConnection(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        pi_address = ('192.168.34.110', 5002)
        print >>sys.stderr, 'starting up on %s port %s' % pi_address
        self.sock.bind(pi_address)

        # Listen for incoming connections
        self.sock.listen(10)

        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        self.connection, client_address = self.sock.accept()

        print >>sys.stderr, 'connection from', client_address

    def getWeather(self):
        owm = pyowm.OWM("1304584f22b294d48aae0bfff0fe655f")  # You MUST provide a valid API key

        # Search for current weather in Needham, MA
        observation = owm.weather_at_place('Needham,MA')
        w = observation.get_weather()
        # <Weather - reference time=2013-12-18 09:20, status=Clouds>

        # Weather details
        summary = w.get_detailed_status()
        wind = w.get_wind()                  # {'speed': 4.6, 'deg': 330}
        humidity = w.get_humidity()              # 87
        temperature = w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
        pressure = w.get_pressure()
        text = "say hello my majesty, today the weather is " + str(summary) + ", the wind speed is " + str(wind["speed"]) + ", the humidity is " + str(humidity) + ", the temperature is around " + str(temperature["temp"]) + " and the pressure is " + str(pressure["press"])
        return text

             

    def panCar(self, theta):
        theta = theta - 90

        if abs(theta)<=5:
            self.a.analogWrite(5,0)
            self.a.analogWrite(6,0)
        elif theta>5:
            print "theta is larger than 2"
            self.a.digitalWrite(8, self.a.HIGH)
            self.a.digitalWrite(9, self.a.LOW)
            self.a.digitalWrite(10, self.a.LOW)
            self.a.digitalWrite(11, self.a.HIGH)
            self.a.analogWrite(5,110)
            self.a.analogWrite(6,110)

        elif theta<-5:
            print "theta is larger than -2"
            self.a.digitalWrite(8, self.a.LOW)
            self.a.digitalWrite(9, self.a.HIGH)
            self.a.digitalWrite(10, self.a.HIGH)
            self.a.digitalWrite(11, self.a.LOW)
            self.a.analogWrite(5,110)
            self.a.analogWrite(6,110)

    def tiltmotor(self, phi):
        nPhi = int(self.prePhi + (phi-90))

        if abs(phi-90) < 7:
            pass
        elif abs(nPhi-90)>50:
            print "too big nPhi: ", nPhi
            print "pass"
        else:
            print "inside nPhi: ", nPhi
            self.servo_tilt.write(nPhi)
            self.prePhi = nPhi

    def control(self):
        while True:
            while not self.q.empty():
                data = self.q.get()
                print "pop out from queue: ", data
                try:
                    data = data.split(" ")
                    [faceResult, smileResult, theta, phi, realDist] = int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4])
                    
                    # self.tiltmotor(phi)                   
                    # self.panCar(theta)

                    if faceResult == 0:
                        system("go away! alien")
                        if smileResult == 1:
                            system("do not smile! alien")
                    else:
                        # self.tiltmotor(phi)                   
                        # self.panCar(theta)
                        if smileResult == 1:
                            system(self.getWeather())
                        else:
                            system("Good to see you! my man")

                    while not self.q.empty():
                        waste = self.q.get() 
                    
                    self.q.task_done()
                except Exception as e:
                    print e
                    self.q.task_done()
                # self.q.task_done()

    def cmdReceiver(self):
        while True:
            try:
                data = self.connection.recv(16).strip()
                print >>sys.stderr, 'received "%s"' % data
                self.q.put(data)
                self.q.join()
            except Exception as e:
                print e
                pass

        # Clean up the connection
        self.connection.close()

    def run(self):
        t1 = threading.Thread(target = self.cmdReceiver)
        t1.start()
        t2 = threading.Thread(target = self.control)
        t2.start()

if __name__ == '__main__':
    PiControl().run()