from picamera.array import PiRGBArray
import picamera
import socket
import cv2
import sys
import pickle

runFlag = True

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('192.168.32.132', 1234)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
data = ""

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (160, 128) 

        while (runFlag):
            camera.capture(stream, 'bgr', use_video_port=True)
            # stream.array now contains the image data in BGR order
            frame = stream.array
            cv2.imshow('frame',frame)

            
            # try:   
                # Send data
            message = pickle.dumps(frame)
            sock.sendall(struct.pack("H", len(message))+ message) ### new code

                # print sys.getsizeof(message)
                # sock.sendall(message)       
               # while data!="I got it":
               #     data = sock.recv(8) 
               #     print >>sys.stderr, 'received "%s"' % data
            # except Exception as e:
            #     pass

            data = ""
            
            stream.seek(0)
            stream.truncate()

            k = cv2.waitKey(1)
            if k == ord('q'):
                runFlag = False
                cv2.destroyAllWindows()
                
print >>sys.stderr, 'closing socket'
sock.close()

