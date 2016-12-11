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

class PiControl(object):
    """receieve data from pc and contril pi to tilt and pan"""
    def __init__(self):
        self.initConnection()
        self.connection = SerialManager(device='/dev/ttyACM0')

        self.a = ArduinoApi(connection = connection)
        self.servo_tilt = Servo(3)
        self.prePhi = 90
        # self.q = Queue.LifoQueue()
        self.q = Queue.Queue()
        self.a.pinMode(8, a.OUTPUT)
        self.a.pinMode(9, a.OUTPUT)
        self.a.pinMode(10, a.OUTPUT)
        self.a.pinMode(11, a.OUTPUT)
        self.a.pinMode(5, a.OUTPUT)
        self.a.pinMode(6, a.OUTPUT)

    def initConnection(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        pi_address = ('192.168.32.73', 5005)
        print >>sys.stderr, 'starting up on %s port %s' % pi_address
        self.sock.bind(pi_address)

        # Listen for incoming connections
        self.sock.listen(10)

        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        self.connection, client_address = self.sock.accept()

        print >>sys.stderr, 'connection from', client_address

    def pancar(self):
        while True:
            while not self.q.empty():
                data = self.q.get()
                print "pop out from queue: ", data
                try:
                    data = data.split(" ")
                    [faceResult, smileResult, theta, phi, realDist] = int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4])
                    
                    theta = theta - 90

                    if abs(theta)<=2:
                        self.a.analogWrite(5,0)
                        self.a.analogWrite(6,0)
                    elif theta>2:
                        print "theta is larger than 2"
                        self.a.digitalWrite(8, a.HIGH)
                        self.a.digitalWrite(9, a.LOW)
                        self.a.digitalWrite(10, a.HIGH)
                        self.a.digitalWrite(11, a.LOW)
                        self.a.analogWrite(5,120)
                        self.a.analogWrite(6,120)

                    elif theta<-2:
                        print "theta is larger than -2"
                        self.a.digitalWrite(8, a.LOW)
                        self.a.digitalWrite(9, a.HIGH)
                        self.a.digitalWrite(10, a.LOW)
                        self.a.digitalWrite(11, a.HIGH)
                        self.a.analogWrite(5,120)
                        self.a.analogWrite(6,120)

                    # while not self.q.empty():
                    #     waste = self.q.get() 
                    self.q.task_done()
                except Exception as e:
                    print e
                    self.q.task_done()
                # self.q.task_done()
             


    def tiltmotor(self, phi):
        nphi = int(self.prePhi-(phi-90))
        print nphi
        self.servo_tilt.write(nphi)
        self.prePhi = nphi


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
        t2 = threading.Thread(target = self.pancar)
        t2.start()


if __name__ == '__main__':
    PiControl().run()