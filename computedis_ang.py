""" Experiment with face detection and image filtering using OpenCV """

import cv2
import numpy as np


class faceTrack(object):
    """class for face tracking algorithm"""
    def __init__(self, calibrateFlag = False):
        self.cap = cv2.VideoCapture(0)
        #Initial read of the frame size
        ret,frame = self.cap.read()
        height,width,channel = frame.shape
        self.mid = (int(width/2),int(height/2))     
        self.calibrateFlag = calibrateFlag
        self.focus = 816 # px, webcam focal distance
        self.realWidth = 16  # cm, face width

    def calibrate(self, realDst, realWidth):
        self.realWidth = realWidth
        # function for calibrating focus of webcam
        print("Stand and Press C")
        tf = True

        while(tf):
            face_cascade = cv2.CascadeClassifier('/Users/zhecanwang/Project/haarcascades/haarcascade_frontalface_alt.xml')
            ret, frame = self.cap.read() 
            #faces = [[x,y,w,d]], (x,y) is the top left corner      
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
            #Need something to buffer x,y,w,d since sometimes it does not detect face
            for (x,y,w,d) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+d),(0,0,255))
                #point on the center of the frame
                center = (x+int(w/2),y+int(d/2))
                cv2.circle(frame,center,5,(0,0,255),-1)
                cv2.circle(frame,self.mid,5,(0,255,0),-1)

            cv2.imshow('frame',frame)
            k = cv2.waitKey(1)
            if k == ord('c') and faces !=():
                self.focus = (float(w) * realDst)/self.realWidth
                print "The webcam focal distance is: ", self.focus
                tf = False

        cap.release()
        cv2.destroyAllWindows() 
    
    # def outputDist(self):


    def run(self):
        if self.calibrateFlag:
            data = raw_input("please input the distance and face width: (example: distance, width)")
            [realDst, realWidth] = data.split(",")
            self.calibrate(realDst, realWidth)

if __name__ == '__main__':
    faceTrack(calibrateFlag = True).run()