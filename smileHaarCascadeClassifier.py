import cv2
import numpy as np
import sys

facePath = "lib/haarcascade_frontalface_alt.xml"
smilePath = "lib/haarcascade_smile.xml"
faceCascade = cv2.CascadeClassifier(facePath)
smileCascade = cv2.CascadeClassifier(smilePath)

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

sF = 1.05

while True:

    ret, frame = cap.read() # Capture frame-by-frame
    img = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor= sF,
        minNeighbors=8,
        minSize=(70, 70),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    # ---- Draw a rectangle around the faces

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        smile = smileCascade.detectMultiScale(
            roi_gray,
            scaleFactor= 3,
            minNeighbors=50,
            minSize=(50, 50),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )

        # Set region of interest for smiles
        # for (x, y, w, h) in smile:
        print "Found", len(smile), "smiles!"
        if len(smile) > 0:
            (x, y, w, h) = smile[0]
            cv2.rectangle(roi_color, (x, y), (x+w, y+h), (255, 0, 0), 1)

    #cv2.cv.Flip(frame, None, 1)
    cv2.imshow('Smile Detector', frame)
    c = cv2.cv.WaitKey(7) % 0x100
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()