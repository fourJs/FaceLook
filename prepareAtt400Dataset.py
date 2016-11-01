from sklearn import datasets
faces = datasets.fetch_olivetti_faces()
face = faces.images
import scipy.misc

for i in range(len(face)):
	f = face[i]
	scipy.misc.imsave('dataBase/attFaces/' + str(i) + '.jpg', f)
