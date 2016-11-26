#!/usr/bin/python
import socket
import cv2
import numpy
from picamera.array import PiRGBArray
import picamera

TCP_IP = "192.168.32.132"
TCP_PORT = 5001

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (320, 256) 
        
        while True:

            camera.capture(stream, 'bgr', use_video_port=True)
            frame = stream.array

            # capture = cv2.VideoCapture(0)
            # ret, frame = capture.read()

            # encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),10] 
            result, imgencode = cv2.imencode('.jpg', frame, encode_param)
            data = numpy.array(imgencode)
            stringData = data.tostring()

            sock.send( str(len(stringData)).ljust(16));
            sock.send( stringData );
            
            stream.seek(0)
            stream.truncate()
            
            # decimg=cv2.imdecode(data,1)
            # cv2.imshow('CLIENT',decimg)
            # cv2.waitKey(1)

sock.close()    
cv2.destroyAllWindows()