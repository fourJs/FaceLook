""" Experiment with face detection and image filtering using OpenCV """
# import the necessary packages
from picamera.array import PiRGBArray
import picamera
import time
import cv2
import numpy as np
from math import sqrt, pi
from nanpy import Servo
import time

# import serialout as st


class faceTrack(object):
    """class for face tracking algorithm"""
    def __init__(self, calibrateFlag = False):
        self.calibrateFlag = calibrateFlag
        self.focus = 250 # px, webcam focal distance
        self.realWidth = 16  # cm, face width
        self.runFlag = True
        self.firstRun = True
        self.servo_tilt = Servo(11)
        self.servo_r= Servo(5)
        self.servo_l= Servo(9)
        self.prePhi = 90


    def calibrate(self, realDst, realWidth):
        self.realWidth = realWidth
        # function for calibrating focus of webcam
        print("Stand and Press C")
        runFlag = True

        while(runFlag):
            face_cascade = cv2.CascadeClassifier('./lib/haarcascade_frontalface_alt.xml')
            ret, frame = self.cap.read() 
           #faces = [[x,y,w,d]], (x,y) is the top left corner      
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
            #Need something to buffer x,y,w,d since sometimes it does not detect face
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
                #point on the center of the frame
                center = (x+int(w/2),y+int(h/2))
                cv2.circle(frame,center,5,(0,0,255),-1)
                cv2.circle(frame,self.mid,5,(0,255,0),-1)

            cv2.imshow('frame',frame)
            k = cv2.waitKey(1)
            if k == ord('c') and faces !=():
                self.focus = (w * realDst)/self.realWidth
                print "The webcam focal distance is: ", self.focus
                runFlag = False
            elif k == ord('q'):
            	runFlag = False

        self.cap.release()
        cv2.destroyAllWindows() 

    def rad2deg(self,ang):
        return ang*(180/pi)
    
    def outputDistAng(self, frame):
        theta,phi,realDist = 0, 0, 0
        # use camerca video feed to calculate distance and angle of face referenced to the camera
        face_cascade = cv2.CascadeClassifier('./lib/haarcascade_frontalface_alt.xml')

       #faces = [[x,y,w,d]], (x,y) is the top left corner      
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
        #Need something to buffer x,y,w,d since sometimes it does not detect face
        
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
            #point on the center of the frame
            center = (x+int(w/2),y+int(h/2))
            #vector to middle of the frame from the center of the face in pix
            v2mid = (center[0]-self.mid[0],center[1]-self.mid[1])
            #distance to middle of the frame from the center of the face in pix
            d2mid = sqrt(v2mid[0]**2+v2mid[1]**2)
            #distance to the focal point
            d2f = sqrt(self.focus**2+d2mid**2)
            cv2.circle(frame,center,5,(0,0,255),-1)
            cv2.circle(frame,self.mid,5,(0,255,0),-1)
            #theta is positive in ccw direction
            theta = self.rad2deg(np.arctan((float(v2mid[0]))/self.focus))
            #phi is positive in left direction (right hand rule)
            phi = -self.rad2deg(np.arctan((float(v2mid[1]))/self.focus))
            realDist = (self.realWidth*d2f)/w

        cv2.imshow('frame',frame)

        k = cv2.waitKey(1)
        if k == ord('q'):
        	self.runFlag = False
        return (theta+90.0,phi+90.0,realDist)
    	
    def close(self):
        self.cap.release()
        cv2.destroyAllWindows() 
     
    def tiltmotor(self,phi):
        nphi = int(self.prePhi+(phi-90))
        print nphi
        self.servo_tilt.write(nphi)
        self.prePhi = nphi


    #Servo.write(20)=> move clockwise (full speed)
    #120 => move counterclockwise (full speed)
    #0 => stop car
    def controlcar(self,theta,dist):
        if dist<=10:
            self.servo_r.write(0)
            self.servo_l.write(0)
        else:
            #if angle diff is less than 2 degrees, go straight
            if abs(theta)<=2:
                self.servo_r.write(20)
                self.servo_l.write(120)
            elif theta>2:
                self.servo_l.write(120)
                self.servo_r.write(0)
                time.sleep(0.01*(abs(theta)-2))
                self.servo_r.write(20)
            elif theta<-2:
                self.servo_r.write(20)
                self.servo_l.write(0)
                time.sleep(0.01*(abs(theta)-2))
                self.servo_l.write(120)
                
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

            

    def run(self): 
        # if self.calibrateFlag:
        #     data = raw_input("please input the distance and face width: (example: distance, width)")
        #     [realDst, realWidth] = data.split(",")
        #     self.calibrate(float(realDst), float(realWidth))
        with picamera.PiCamera() as camera:
            with picamera.array.PiRGBArray(camera) as stream:
                camera.resolution = (320, 240)   

                while (self.runFlag):
                    camera.capture(stream, 'bgr', use_video_port=True)
                    # stream.array now contains the image data in BGR order
                    frame = stream.array
 
                    if self.firstRun:
                        height,width,channel = frame.shape
                        self.mid = (int(width/2),int(height/2)) 
                        self.firstRun = False
    
                    (theta,phi,realDist) = self.outputDistAng(frame)
                    
            
                    # time.sleep(1)

                    stream.seek(0)
                    stream.truncate()

                    packet = "(" + '%03d'%int(theta) + "," + '%03d'%int(phi) + "," + '%03d'%int(realDist) + ")"
                    if packet == '(090,090,000)':
                        print "no face"
                    else:
                        print packet
                        print "phi ", phi - 90
                        #print "theta", theta - 90
                        self.tiltmotor(phi)
                        #self.controlcar(theta-90,realDist)
                        self.pancar(theta-90)




if __name__ == '__main__':
    faceTrack(calibrateFlag = False).run()
    
