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
        self.servo_tilt = Servo(11)
        self.servo_r= Servo(5)
        self.servo_l= Servo(9)
        self.prePhi = 90
        self.q = Queue.LifoQueue()

    def initConnection(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        pi_address = ('192.168.33.182', 5001)
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
                except Exception as e:
                    print e
            self.q.task_done()

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