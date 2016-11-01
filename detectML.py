from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
import os
from PIL import Image, ImageChops
import cv2
import numpy as np
import pickle
from random import shuffle
from sklearn.externals import joblib
from scipy.ndimage import zoom
from sklearn.decomposition import PCA
import random
from pylab import array, uint8 

class DetectML(object):
    def __init__(self):         
        self.clf = SVC(kernel='rbf', C = 1, gamma =0.001)

        # self.posDir = "./dataBase/gi/smiling/"
        # self.negaDir = "./dataBase/gi/noSmiling/"

        self.posDir = "./dataBase/specFaceRecogDB/target/"
        self.negaDir = "./dataBase/specFaceRecogDB/nonTarget/"

        self.posFiles = os.listdir(self.posDir)
        self.negaFiles = os.listdir(self.negaDir)

        self.processDataDir = "./processData/"
        self.debug = False
        # self.spec = "Smile"
        self.spec = "SpecFinal"
        self.generateNum = 1
        self.counter = 0

    def decompose(self, xTrain, xTest):
        ################################################################################
        # Compute a PCA (eigenfaces) on the face dataset (treated as unlabeled
        # dataset): unsupervised feature extraction / dimensionality reduction
        print "xTrain.shape ", xTrain.shape
 
        n_components = 150

        print "Extracting the top %d eigenfaces" % n_components
        pca = PCA(n_components=n_components, whiten=True).fit(xTrain)

        eigenfaces = pca.components_.T.reshape((n_components, 64, 32))

        # project the input data on the eigenfaces orthonormal basis
        xTrainPCA= pca.transform(xTrain)
        xTestPCA = pca.transform(xTest)

        print "xTrainPCA.shape ", xTrainPCA.shape

        return xTrainPCA, xTestPCA



    def saveModel(self):
        joblib.dump(self.clf, self.processDataDir + self.spec + 'DetectSVC.pkl') 

    def loadModel(self):
        svc_1 = joblib.load(self.processDataDir + self.spec + 'DetectSVC.pkl') 

    def detect_face(self, frame):
        cascPath = './lib/haarcascade_frontalface_alt.xml'
        faceCascade = cv2.CascadeClassifier(cascPath)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected_faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=6,
                minSize=(100, 100),
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
????
不应该这样normalize，而应该直接除以255来normalize？？？？？


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

    def contrastBrightess(self, image):
        contrast = random.uniform(0.5, 2)
        brightness = random.uniform(-20, 50)
        # contrast = 2
        # brightness = 50

        maxIntensity = 255.0 # depends on dtype of image data
        phi = 1
        theta = 1
        image = ((maxIntensity/phi)*(image/(maxIntensity/theta))**contrast) + brightness
        image = np.asarray(image)
        top_index = np.where(image > 255)
        bottom_index = np.where(image < 0)
        image[top_index] = 255
        image[bottom_index] = 0
        image = array(image,dtype=uint8)
        return image


    def scale(self, image):
        (h, w) = image.shape
        ratio = random.uniform(0.5, 1)
        size = (int(w*ratio), int(h*ratio))
        image = Image.fromarray(np.uint8(image))
        image.thumbnail(size, Image.ANTIALIAS)
        image_size = image.size
        thumb = image.crop( (0, 0, w, h) )

        offset_x = max( (w - image_size[0]) / 2, 0 )
        offset_y = max( (h - image_size[1]) / 2, 0 )

        thumb = ImageChops.offset(thumb, offset_x, offset_y)
        image = np.asarray(thumb)
        return image

    def rotate(self, image):
        w, h = image.shape
        degree = random.uniform(-45, 45)

        M = cv2.getRotationMatrix2D((w/2, h/2),degree,1)
        image = cv2.warpAffine(image,M,(w, h))
        return image

    def generateMoreImg(self, num, img):
        imgs = []
        for i in range(num):
            img1 = self.contrastBrightess(img)
            img2 = self.scale(img)
            print img1.shape
            print img2.shape

            imgs.append(img1.ravel())
            imgs.append(img2.ravel())
        return imgs

    def display(self, img, label):
        if self.debug:
            cv2.imshow('img', img)
            k = cv2.waitKey(100) 
            print "label: ", label

    def fetchData(self, files, directory, label):
        X = []
        Y = []
        for file in files:
            if file != ".DS_Store":
                # try:
                # print file
                img = cv2.imread( directory + file, 1)
                # cv2.imshow('frame0',img)
                # k = cv2.waitKey(0) 

                # normalize each picture by centering brightness
                # img -= img.mean(axis=1)[:, np.newaxis]

                gray, detected_faces = self.detect_face(img)
                if len(detected_faces) > 0:
                    (x,y,w,h) = detected_faces[0]
                else:
                    w = 0
                if w > 10:
                    # if self.debug:
                    #     cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255))
                    #     cv2.imshow('frame1',img)

                    extracted_face = self.extract_face_features(gray, detected_faces[0])

                    for i in range(self.generateNum):
                        contrastBrightessImg = self.contrastBrightess(extracted_face)
                        self.display(contrastBrightessImg, label)
                        contrastBrightessImg = self.normalize(contrastBrightessImg)

                        scaleImage = self.scale(extracted_face)
                        self.display(scaleImage, label)                    
                        scaleImage = self.normalize(scaleImage)

                        rotateImage = self.rotate(extracted_face)
                        self.display(rotateImage, label)                    
                        rotateImage = self.normalize(rotateImage)

                        X.append(contrastBrightessImg.ravel())
                        X.append(scaleImage.ravel())
                        X.append(rotateImage.ravel())
                        
                        Y.append(label)                        
                        Y.append(label)                        
                        Y.append(label)                        
                        
                        self.counter += 1
                        self.counter += 1
                        self.counter += 1


                    extracted_face = self.normalize(extracted_face)
                    self.display(extracted_face, label)
                    X.append(extracted_face.ravel())
                    Y.append(label)                        
                    self.counter += 1

                    if self.counter %100 == 0:
                        print self.counter


                # except Exception as e:
                #     print "."
                #     if self.debug:
                #         print e
                    # print detected_faces
                    # cv2.imshow('frame1',img)
                    # cv2.waitKey(0)
                    # raise "debug"
        X = np.asarray(X)
        Y = np.asarray(Y)

        print X.shape
        print Y.shape
        print np.mean(Y)

        return X, Y

    def shuffleSplit(self, xPos, yPos, xNega, yNega):
        x, y = [], []
        x.extend(xPos) 
        x.extend(xNega)

        y.extend(yPos) 
        y.extend(yNega)

        data = zip(x, y)
        shuffle(data)
        x, y = zip(*data)

        x = np.asarray(x)
        y = np.asarray(y)

        print "x.shape ", x.shape
        print "y.shape ", y.shape
        
        xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.25, random_state=0)
        
        # xTrain, xTest = self.decompose(xTrain, xTest)  

        print np.mean(yTrain)
        print np.mean(yTest)

        return xTrain, yTrain, xTest, yTest

    def saveData(self, xTrain, yTrain, xTest, yTest):
        pickle.dump( xTrain, open( self.processDataDir + "xTrain" + self.spec + ".p", "wb" ) )
        pickle.dump( yTrain, open( self.processDataDir + "yTrain" + self.spec + ".p", "wb" ) )
        pickle.dump( xTest, open( self.processDataDir + "xTest" + self.spec + ".p", "wb" ) )
        pickle.dump( yTest, open( self.processDataDir + "yTest" + self.spec + ".p", "wb" ) )

    def loadData(self):
        xTrain = pickle.load( open( self.processDataDir + "xTrain" + self.spec + ".p", "rb" ) )
        yTrain = pickle.load( open( self.processDataDir + "yTrain" + self.spec + ".p", "rb" ) )
        xTest = pickle.load( open( self.processDataDir + "xTest" + self.spec + ".p", "rb" ) )
        yTest = pickle.load( open( self.processDataDir + "yTest" + self.spec + ".p", "rb" ) )
        
        print xTrain.shape
        print yTrain.shape
        print xTest.shape
        print yTest.shape
        
        return xTrain, yTrain, xTest, yTest 

    def preProcess(self):
        xPos, yPos = self.fetchData(self.posFiles, self.posDir, 1)
        xNega, yNega = self.fetchData(self.negaFiles, self.negaDir, 0)
        xTrain, yTrain, xTest, yTest = self.shuffleSplit(xPos, yPos, xNega, yNega)
        self.saveData(xTrain, yTrain, xTest, yTest )

    def trainDeep(self):
        xTrain, yTrain, xTest, yTest = self.loadData()


    def train(self):
        xTrain, yTrain, xTest, yTest = self.loadData()
        self.clf.fit(xTrain, yTrain)

        print ("Accuracy on training set:")
        print (self.clf.score(xTrain, yTrain))
        print ("Accuracy on testing set:")
        print (self.clf.score(xTest, yTest))

    def investigateImage(self):
        xTrain, yTrain, xTest, yTest = self.loadData()
        # randomly select a few of the test instances
        # for i in np.random.randint(0, len(yTrain), size = 100):
        for i in range(0, len(yTrain), 10):
            # classify the digit
            # pred = dbn.predict(np.atleast_2d(testX[i]))
         
            # reshape the feature vector to be a 28x28 pixel image, then change
            # the data type to be an unsigned 8-bit integer
            print yTrain[i]
            image = (xTrain[i] * 255).reshape((64, 64)).astype("uint8")
         
            # show the image and prediction
            # print "Actual digit is {0}, predicted {1}".format(testY[i], pred[0])
            cv2.imshow("test image", image)
            cv2.waitKey(0)


    def run(self):
        self.preProcess()
        self.train()
        self.saveModel()
        # self.investigateImage()

if __name__ == '__main__':
    DetectML().run()


