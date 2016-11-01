import cv2
import datetime


camera = cv2.VideoCapture(0)
path = "./dataBase/specFaceRecogDB/target/"
# counter = 0

while True:
    return_value,image = camera.read()
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    cv2.imshow('image',gray)
    # counter += 1  
    cv2.imwrite(path + 'James_' + str(datetime.datetime.now()) + '.jpg',gray) 
    print path + 'James_' + str(datetime.datetime.now()) + '.jpg'
    # if counter%100 == 0:
    	# print counter

    if cv2.waitKey(1)& 0xFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()