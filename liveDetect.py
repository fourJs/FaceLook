from sklearn.externals import joblib
import cv2
from scipy.ndimage import zoom
import numpy as np
from PIL import Image, ImageChops

# svc_1 = joblib.load('./data/faceDetectSVC.pkl')

processDataDir = "./processData/"

spec1 = "SpecFinal"
model1 = joblib.load(processDataDir + spec1 + 'DetectSVC.pkl')

# spec2 = "Smile"
# model2 = joblib.load(processDataDir + spec2 + 'DetectSVC.pkl')


smilePath = "lib/haarcascade_smile.xml"
smileCascade = cv2.CascadeClassifier(smilePath)


def detect_face(frame):
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


def resize(image, size):
    image = Image.fromarray(np.uint8(image))
    image.thumbnail(size, Image.ANTIALIAS)
    image_size = image.size

    thumb = image.crop( (0, 0, size[0], size[1]) )

    offset_x = max( (size[0] - image_size[0]) / 2, 0 )
    offset_y = max( (size[1] - image_size[1]) / 2, 0 )

    thumb = ImageChops.offset(thumb, offset_x, offset_y)
    image = np.asarray(thumb)
    return image

def extract_face_features(gray, detected_face):
    (x, y, w, h) = detected_face

    # extracted_face = gray[y+h/2:y+h, 
    #                   x:x+w]
    # new_extracted_face = self.resize(extracted_face, (64, 32))
    extracted_face = gray[y:y+h, 
                      x:x+w]
    new_extracted_face = resize(extracted_face, (64, 64))
    return new_extracted_face

def normalize(arr):
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

def recognizeFace(extracted_face):
    return model1.predict(extracted_face.ravel())

def predictSmile(extracted_face):
    smile = smileCascade.detectMultiScale(
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

video_capture = cv2.VideoCapture(0)


while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # detect faces
    gray, detected_faces = detect_face(frame)
    print "detected_faces ", detected_faces

    face_index = 0
    
    # predict output
    for face in detected_faces:
        (x, y, w, h) = face
        if w > 10:
            # draw rectangle around face 
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            extracted_face = extract_face_features(gray, face) #(0.075, 0.05)

            roi_gray = gray[y:y+h, x:x+w]
            smileResult = predictSmile(roi_gray)
                        
            extracted_face = normalize(extracted_face)
            faceResult = recognizeFace(extracted_face)

            print "faceResult, ",  faceResult
            print "smileResult, ",  smileResult



            # draw extracted face in the top right corner
            # frame[face_index * 64: (face_index + 1) * 64, -65:-1, :] = cv2.cvtColor(extracted_face * 255, cv2.COLOR_GRAY2RGB)
            # frame[face_index * 64: (face_index + 1) * 64, -65:-1, :] = cv2.cvtColor((1 - extracted_face) * 255, cv2.COLOR_GRAY2RGB)

            # annotate main image with a label
            if faceResult == 1:
                if smileResult == 1:
                    cv2.putText(frame, "James Smiling",(x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, 155, 10)
                else:
                    cv2.putText(frame, "James",(x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, 155, 10)
            else:
                if smileResult == 1:
                    cv2.putText(frame, "Alien Smiling",(x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, 155, 10)
                else:
                    cv2.putText(frame, "Alien",(x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, 155, 10)

            # increment counter
            face_index += 1
                

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
