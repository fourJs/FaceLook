import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
from nanpy import Servo
import time

class PiControl(object):
    """receieve data from pc and contril pi to tilt and pan"""
    def __init__(self):
        self.initConnection()
        self.servo_tilt = Servo(11)
        self.servo_r= Servo(5)
        self.servo_l= Servo(9)
        self.prePhi = 90

    def initConnection(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('192.168.34.162', 5000)
        print >>sys.stderr, 'starting up on %s port %s' % server_address
        self.sock.bind(server_address)

        # Listen for incoming connections
        self.sock.listen(10)

        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        self.connection, client_address = self.sock.accept()

        print >>sys.stderr, 'connection from', client_address

    def pancar(self,theta):
        if abs(theta)<=2:
            self.servo_r.write(0)
            self.servo_l.write(0)
        elif theta>2:
            print "theta is larger than 2"
            self.servo_l.write(98)
            self.servo_r.write(98)
            time.sleep(0.05*(abs(theta)-2))
            self.servo_r.write(0)
            self.servo_l.write(0)
        elif theta<-2:
            print "theta is larger than -2"
            self.servo_l.write(20)
            self.servo_r.write(20)
            time.sleep(0.01*(abs(theta)-2))
            self.servo_r.write(0)
            self.servo_l.write(0)

    def tiltmotor(self,phi):
        nphi = int(self.prePhi-(phi-90))
        print nphi
        self.servo_tilt.write(nphi)
        self.prePhi = nphi


    def run(self):
        while True:
            data = self.connection.recv(16)
            print >>sys.stderr, 'received "%s"' % data
            faceResult, smileResult, theta, phi, realDist = data.split(" ")
            self.pancar(int(theta) - 90)
            self.tiltmotor(int(phi))
  

        # Clean up the connection
        self.connection.close()


if __name__ == '__main__':
    PiControl().run()