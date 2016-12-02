#!/usr/bin/python
from sklearn.externals import joblib
import cv2
from scipy.ndimage import zoom
import numpy as np
from PIL import Image, ImageChops
import socket
import cv2
import sys
from math import sqrt, pi

class LiveDetectPi(object):
    """ Detect specific smiling face from video feed of Pi """
    def __init__(self):

        processDataDir = "./processData/"
        
        spec1 = "SpecFinal"
        self.model1 = joblib.load(processDataDir + spec1 + 'DetectSVC.pkl')

        # spec2 = "Smile"
        # model2 = joblib.load(processDataDir + spec2 + 'DetectSVC.pkl')

        smilePath = "lib/haarcascade_smile.xml"
        self.smileCascade = cv2.CascadeClassifier(smilePath)
        
        pc_IP = "192.168.34.189"
        TCP_PORT = 1236

        self.s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s1.bind((pc_IP, TCP_PORT))
        self.s1.listen(True)
        self.conn, addr = self.s1.accept()

        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        pi_address = ('192.168.33.182', 5005)
        print >>sys.stderr, 'connecting to %s port %s' % pi_address
        self.s2.connect(pi_address)

        self.firstRun = True
        self.focus = 250 # px, webcam focal distance
        self.realWidth = 16  # cm, face width

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def detect_face(self, frame):
        cascPath = './lib/haarcascade_frontalface_alt.xml'
        faceCascade = cv2.CascadeClassifier(cascPath)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected_faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor= 1.05,
                minNeighbors=8,
                minSize=(70, 70),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )

        return gray, detected_faces


    def resize(self, image, size):
        image = Image.fromarray(np.uint8(image))
        image.thumbnail(size, Image.ANTIALIAS)
        image_size = image.size

        thumb = image.crop( (0, 0, size[0], size[1]) )

        offset_x = max( (size[0] - image_size[0]) / 2, 0 )
        offset_y = max( (size[1] - image_size[1]) / 2, 0 )

        thumb = ImageChops.offset(thumb, offset_x, offset_y)
        image = np.asarray(thumb)
        return image

    def extract_face_features(self, gray, detected_face):
        (x, y, w, h) = detected_face

        # extracted_face = gray[y+h/2:y+h, 
        #                   x:x+w]
        # new_extracted_face = self.resize(extracted_face, (64, 32))
        extracted_face = gray[y:y+h, 
                          x:x+w]
        new_extracted_face = self.resize(extracted_face, (64, 64))
        return new_extracted_face

    def normalize(self, arr):
        """
        Linear normalization
        http://en.wikipedia.org/wiki/Normalization_%28image_processing%29
        """
        arr = arr.astype('float')
        # Do not touch the alpha channel
        minval = arr.min()
        maxval = arr.max()
        if minval != maxval:
            arr -= minval
            arr *= (1.0/(maxval-minval))
        return arr

    def recognizeFace(self, extracted_face):
        return self.model1.predict(extracted_face.ravel())[0]

    def predictSmile(self, extracted_face):
        smile = self.smileCascade.detectMultiScale(
            extracted_face,
            scaleFactor= 3,
            minNeighbors=30,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )
        print "found smiles: ", len(smile)
        if len(smile) > 0:
            return 1
        else:
            return 0
        # return model2.predict(extracted_face.ravel())


    def getPredicts(self, frame, x, y, w, h, gray, face):
        
        # draw rectangle around face 
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        extracted_face = self.extract_face_features(gray, face) #(0.075, 0.05)

        roi_gray = gray[y:y+h, x:x+w]
        smileResult = self.predictSmile(roi_gray)

        extracted_face = self.normalize(extracted_face)
        faceResult = self.recognizeFace(extracted_face)

        print "faceResult, ",  faceResult
        print "smileResult, ",  smileResult

        return faceResult, smileResult

    def tag(self, frame, faceResult, smileResult, x, y):
        # annotate main image with a label
        if faceResult == 1:
            if smileResult == 1:
                cv2.putText(frame, "James Smiling",(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, 100, 5)
            else:
                cv2.putText(frame, "James",(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, 100, 5)
        else:
            if smileResult == 1:
                cv2.putText(frame, "Alien Smiling",(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, 100, 5)
            else:
                cv2.putText(frame, "Alien",(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, 100, 5)

    def rad2deg(self,ang):
        return ang*(180/pi)

    def getDistAng(self, x, y, w, h):
        theta,phi,realDist = 0, 0, 0

        #point on the center of the frame
        center = (x+int(w/2),y+int(h/2))
        #vector to middle of the frame from the center of the face in pix
        v2mid = (center[0]-self.mid[0],center[1]-self.mid[1])
        #distance to middle of the frame from the center of the face in pix
        d2mid = sqrt(v2mid[0]**2+v2mid[1]**2)
        #distance to the focal point
        d2f = sqrt(self.focus**2+d2mid**2)
        

        #theta is positive in ccw direction
        theta = self.rad2deg(np.arctan((float(v2mid[0]))/self.focus))
        #phi is positive in left direction (right hand rule)
        phi = -self.rad2deg(np.arctan((float(v2mid[1]))/self.focus))
        realDist = (self.realWidth*d2f)/w

        return (theta+90.0,phi+90.0,realDist)


    def run(self):
        while True:
            # Capture frame-by-frame
            length = self.recvall(self.conn,16)
            if length != None:
                stringData = self.recvall(self.conn, int(length))
                data = np.fromstring(stringData, dtype='uint8')
                frame = cv2.imdecode(data,1)
                
                if self.firstRun:
                    height,width,channel = frame.shape
                    self.mid = (int(width/2),int(height/2)) 
                    self.firstRun = False
                
                # detect faces
                gray, detected_faces = self.detect_face(frame)
                print "detected_faces ", detected_faces

                # predict output
                for face in detected_faces:
                    (x, y, w, h) = face
                    if w > 10:
                        (theta, phi, realDist) = self.getDistAng(x, y, w, h)
                        faceResult, smileResult = self.getPredicts(frame, x, y, w, h, gray, face)
                        self.tag(frame, faceResult, smileResult, x, y)

                        message = " ".join((str(faceResult), str(smileResult), str(int(theta)), str(int(phi)), str(int(realDist))))
                        self.s2.sendall(message)

                # Display the resulting frame
                cv2.imshow('Video', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        # When everything is done, release the capture
        self. video_capture.release()
        cv2.destroyAllWindows()
        self.s1.close()
        self.s2.close()   


if __name__ == '__main__':
    LiveDetectPi().run()