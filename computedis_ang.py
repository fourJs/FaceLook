""" Experiment with face detection and image filtering using OpenCV """

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
#Initial read of the frame size
ret,frame = cap.read()
height,width,channel = frame.shape
mid = (int(width/2),int(height/2))

print("printing height and width:",height,width)

print("Stand and Press C")

tf = True
while(tf):
	face_cascade = cv2.CascadeClassifier('/home/jong/Desktop/softdes/SoftwareDesignFall15/toolbox/image_processing/haarcascade_frontalface_alt.xml')
	ret, frame = cap.read()	
	#faces = [[x,y,w,d]], (x,y) is the top left corner		
	faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
	#Need something to buffer x,y,w,d since sometimes it does not detect face
	for (x,y,w,d) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+d),(0,0,255))
		#point on the center of the frame
		center = (x+int(w/2),y+int(d/2))
		cv2.circle(frame,center,5,(0,0,255),-1)
		cv2.circle(frame,mid,5,(0,255,0),-1)
		#distance from the center
		# xdis = 
	cv2.imshow('frame',frame)
	k = cv2.waitKey(1)
	if k == ord('c') and faces !=():
		print faces[0]
		print (x,y,w,d)
		tf = False





cap.release()
cv2.destroyAllWindows()

#face = [[x,y,w,d]], framesize=[pix width, pix height]
# def computedis(faces,framesize):
	




# while(True):
# 	face_cascade = cv2.CascadeClassifier('/home/jong/Desktop/softdes/SoftwareDesignFall15/toolbox/image_processing/haarcascade_frontalface_alt.xml')
# 	ret, frame = cap.read()
# 	faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
# 	for (x,y,w,h) in faces:
# 		frame[y:y+h,x:x+w,:] = cv2.dilate(frame[y:y+h,x:x+w,:], kernel)
# 		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
# 		cv2.circle(frame,(x+int(w/2),y+int(h/2)),int(h/2.5),(255,255,255),-1)
# 		cv2.circle(frame,(x+int(w/3)*2,y+int(h/3)),10,(0,0,0),-1)
# 		cv2.circle(frame,(x+int(w/3),y+int(h/3)),10,(0,0,0),-1)
# 		cv2.rectangle(frame,(x+int(w/3),y+int(h/3)*2),(x+int(w/3)*2,y+int(h/3)*2),(0,0,0),10)
# 	# Display the resulting frame
# 	cv2.imshow('frame',frame)
# 	if cv2.waitKey(1) & 0xFF == ord('q'):
# 	    break

