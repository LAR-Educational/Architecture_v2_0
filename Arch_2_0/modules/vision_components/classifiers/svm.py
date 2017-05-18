# import the necessary packages
from sklearn import svm
from sklearn.calibration import CalibratedClassifierCV

# from sklearn.cross_validation import train_test_split
# resolvendo problemas de compatibilidade
from sklearn.model_selection import train_test_split

from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import os

data_path = "modules/vision_components/classifiers/DBIM/alldb"

model_pxl = CalibratedClassifierCV(svm.LinearSVC())
model_hst = CalibratedClassifierCV(svm.LinearSVC())


def image_to_feature_vector(image, size=(32, 32)):
	# resize the image to a fixed size, then flatten the image into
	# a list of raw pixel intensities
	return cv2.resize(image, size).flatten()

def extract_color_histogram(image, bins=(8, 8, 8)):
	# extract a 3D color histogram from the HSV color space using
	# the supplied number of `bins` per channel
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	hist = cv2.calcHist([hsv], [0, 1, 2], None, bins,
		[0, 180, 0, 256, 0, 256])
 
	# handle normalizing the histogram if we are using OpenCV 2.4.X
	if imutils.is_cv2():
		hist = cv2.normalize(hist)
 
	# otherwise, perform "in place" normalization in OpenCV 3 (I
	# personally hate the way this is done
	else:
		cv2.normalize(hist, hist)
 
	# return the flattened histogram as the feature vector
	return hist.flatten()



def initializate(data_p):
	global data_path 
	data_path = data_p
     
	model_pxl = CalibratedClassifierCV(svm.LinearSVC())
	model_hst = CalibratedClassifierCV(svm.LinearSVC())

def fit(info=False):
	# grab the list of images that we'll be describing
	if(info):
		print("[INFO] describing images...")
	imagePaths = list(paths.list_images(data_path))
	 
      # initialize the raw pixel intensities matrix, the features matrix,
	# and labels list
	rawImages = []
	features = []
	labels = []

	# loop over the input images
	for (i, imagePath) in enumerate(imagePaths):
		# load the image and extract the class label (assuming that our
		# path as the format: /path/to/dataset/{class}/{image_num}.jpg
		image = cv2.imread(imagePath)
  
		
		label = imagePath.split(os.path.sep)[5]
	 	
		# extract raw pixel intensity "features", followed by a color
		# histogram to characterize the color distribution of the pixels
		# in the image
		pixels = image_to_feature_vector(image)
		hist = extract_color_histogram(image)
	 
		# update the raw images, features, and labels matricies,
		# respectively
		rawImages.append(pixels)
		features.append(hist)
		labels.append(label)
	 
		# show an update every 1,000 images
		if i > 0 and i % 1000 == 0 and info:
			print("[INFO] processed {}/{}".format(i, len(imagePaths)))

	# show some information on the memory consumed by the raw images
	# matrix and features matrix
	rawImages = np.array(rawImages)
	features = np.array(features)
	labels = np.array(labels)
	if(info):
		print("[INFO] pixels matrix: {:.2f}MB".format(
			rawImages.nbytes / (1024 * 1000.0)))
		print("[INFO] features matrix: {:.2f}MB".format(
			features.nbytes / (1024 * 1000.0)))

	(trainRI, testRI, trainRL, testRL) = train_test_split(
		rawImages, labels, test_size=0, random_state=42)
	(trainFeat, testFeat, trainLabels, testLabels) = train_test_split(
		features, labels, test_size=0, random_state=42)

	model_pxl.fit(trainRI, trainRL)
	model_hst.fit(trainFeat, trainLabels)



def get_predict_proba(model, input):
	prob = model.predict_proba(input)
	label = model.predict(input)[0]
	return {'label':label, '0':prob[0][0] ,'1':prob[0][1], '2': prob[0][2] }

def print_proba(ret, full=False):
	if(full):
		print("SVM")
		print("\n PIXEL")
		print("Probability:")
		print("label 0: " + str(ret['pxl']['0']) )
		print("label 1: " + str(ret['pxl']['1']))
		print("label 2: " + str(ret['pxl']['2']))

		print("image label:" + str(ret['pxl']['label']))
		print("")

		print("\n HISTOGRAM")
		print("Probability:")
		print("label 0: " + str(ret['hst']['0']) )
		print("label 1: " + str(ret['hst']['1']))
		print("label 2: " + str(ret['hst']['2']))

		print("image label:" + str(ret['hst']['label']))
		print("")
		
	else:
		print("SVM\n")
		print("Label: " + str(ret['pxl']['label']) +
				" prob:" + str(ret['pxl'][str(ret['pxl']['label'])]))
		print("Label: " + str(ret['hst']['label']) +
				" prob:" + str(ret['hst'][str(ret['hst']['label'])]))


def classify(img, imshow=False):

	#img = cv2.imread(img_path)

	if(imshow):
		cv2.imshow('image',img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	pxl = image_to_feature_vector(np.array(img)).reshape(1,-1)
	hst = extract_color_histogram(np.array(img)).reshape(1,-1)
	
	pxl_c = get_predict_proba(model_pxl, pxl)
	hst_c = get_predict_proba(model_hst, hst)
	
	return {'pxl':pxl_c, 'hst':hst_c }