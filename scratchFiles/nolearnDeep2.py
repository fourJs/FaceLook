# import the necessary packages
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn import datasets
from nolearn.dbn import DBN
import numpy as np
import cv2
import pickle

processDataDir = "./processData/"

def loadData():
    xTrain = pickle.load( open( processDataDir + "xTrain1.p", "rb" ) )
    yTrain = pickle.load( open( processDataDir + "yTrain1.p", "rb" ) )
    xTest = pickle.load( open( processDataDir + "xTest1.p", "rb" ) )
    yTest = pickle.load( open( processDataDir + "yTest1.p", "rb" ) )
    # print xTrain[0].shape
    print xTrain.shape
    print yTrain.shape
    # print xTest[0].shape
    # print yTest.shape
    return xTrain, yTrain, xTest, yTest 

# print "[X] downloading data..."
# dataset = datasets.fetch_mldata("MNIST Original")

# (xTrain, xTest, yTrain, yTest) = train_test_split(
# 	dataset.data / 255.0, dataset.target.astype("int0"), test_size = 0.33)

xTrain, yTrain, xTest, yTest = loadData()
# yTrain = np.reshape((yTrain.shape[0], 1))
# print xTrain.shape
# print yTrain.shape
print np.mean(yTrain)
print np.mean(yTest)

# raise "debug"



dbn = DBN(
	[xTrain.shape[1], 1000, 500, 500, 2],
	learn_rates = 0.3,
	learn_rate_decays = 0.01,
	epochs = 10,
	verbose = 1)
print "xTrain.shape ", xTrain.shape
print "yTrain.shape ", yTrain.shape
dbn.fit(xTrain, yTrain)
preds = dbn.predict(xTest)
print classification_report(yTest, preds)




