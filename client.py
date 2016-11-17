from picamera.array import PiRGBArray
import picamera
import socket
import cv2
import sys

runFlag = True



with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (160, 128) 

        while (runFlag):
            camera.capture(stream, 'bgr', use_video_port=True)
            # stream.array now contains the image data in BGR order
            frame = stream.array
            cv2.imshow('frame',frame)
            
            stream.seek(0)
            stream.truncate()

            k = cv2.waitKey(1)
            if k == ord('q'):
                runFlag = False
                cv2.destroyAllWindows() 


        

##
### Create a TCP/IP socket
##sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##
### Connect the socket to the port where the server is listening
##server_address = ('192.168.33.237', 1234)
##print >>sys.stderr, 'connecting to %s port %s' % server_address
##sock.connect(server_address)
##
##try:
##    
##    # Send data
##    message = 'This is the message.  It will be repeated.'
##    print >>sys.stderr, 'sending "%s"' % message
##    sock.sendall(message)
##
##    # Look for the response
##    amount_received = 0
##    amount_expected = len(message)
##    
##    while amount_received < amount_expected:
##        data = sock.recv(16)
##        amount_received += len(data)
##        print >>sys.stderr, 'received "%s"' % data
##
##finally:
##    print >>sys.stderr, 'closing socket'
##    sock.close()
