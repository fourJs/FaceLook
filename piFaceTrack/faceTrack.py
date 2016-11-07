""" Experiment with face detection and image filtering using OpenCV """
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from math import sqrt, pi
# import serialout as st


class faceTrack(object):
    """class for face tracking algorithm"""
    def __init__(self, calibrateFlag = False):

        height,width,channel = frame.shape
        self.mid = (int(width/2),int(height/2))     
        self.calibrateFlag = calibrateFlag
        self.focus = 816 # px, webcam focal distance
        self.realWidth = 16  # cm, face width
        self.runFlag = True
        # self.serConn = st.serialConnect()


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
     

    def run(self):

        # if not self.serConn.isopen:
            # self.serConn.open()
        # if self.calibrateFlag:
        #     data = raw_input("please input the distance and face width: (example: distance, width)")
        #     [realDst, realWidth] = data.split(",")
        #     self.calibrate(float(realDst), float(realWidth))
        with picamera.PiCamera() as camera:
            with picamera.array.PiRGBArray(camera) as stream:
                camera.resolution = (320, 240)
        
                # self.serConn.sendSerialdata((0,0,0))
                while (self.runFlag):
                    camera.capture(stream, 'bgr', use_video_port=True)
                    # stream.array now contains the image data in BGR order
                    (theta,phi,realDist) = self.outputDistAng(stream.array)
                    stream.seek(0)
                    stream.truncate()

                    packet = "(" + '%03d'%int(theta) + "," + '%03d'%int(phi) + "," + '%03d'%int(realDist) + ")"
                    if packet == '(000,000,000)':
                        print "no face"
                    else:
                        # self.serConn.sendSerialdata(packet)
                        print packet

                # self.serConn.close()
                # self.close()


if __name__ == '__main__':
    faceTrack(calibrateFlag = False).run()
    