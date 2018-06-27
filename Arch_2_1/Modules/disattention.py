# external imports
import os
import cv2
import sys
import time
import numpy as np
from threading import Thread
from naoqi import ALProxy

# internal imports
import emotion
from vars import info, war, error, robotIp, port, input_shape, attention, emotions, deviation_times

# subscribe top camera
AL_kTopCamera = 0
AL_kQVGA = 1            # 320x240
AL_kBGRColorSpace = 13

# global string that sets the running state of the system
run_state = 'running'
# NAO camera device
camera = ALProxy("ALVideoDevice", robotIp, port)

# Threading class for parallel control of this module alongside the whole system
class Th(Thread):
	def __init__ (self, num):
		Thread.__init__(self)
		self.num = num

	def run(self):
		if self.num == 1:
			start_classification(0)
			
		elif self.num == 2:
			end_classification()

# set run_state to stop the classification 
def end_classification():
	global run_state
	run_state = 'stop'

# count number of deviation, time on attention and disattention and classify emotion on faces
def start_classification(camId, minNeighbors=5):
	# "import" global variables
	global run_state, camera
	
	# start the classifier
	classifier = emotion.Classifier()
	info("Emotion Classifier initialized")

	# subscribe NAO's camera
	nameId = camera.subscribeCamera("Emotion_Classifier7", camId, AL_kQVGA, AL_kBGRColorSpace, 10)
	info("Subscribed in {}".format(nameId))

	# load the Haar Cascade
	face_cascade = cv2.CascadeClassifier('Modules/haarcascade_frontalface_alt.xml')
	info("Cascade Loaded")

	# start some variables
	# number of deviations, time on disattention
	n_deviations = time_disattention = 0
	# static measuring time, dynamic measuring time, time on atention, time for emotion classifier
	static_time = dynamic_time = time_attention = time_emotion = time.time()

	arq = open('all_statistics.dat', 'a');
	
	info("All set. Obtaining images!")
	c = open('emotion_imgs/classifications.txt', 'a+')
	face = None
	
	while True:
		result = camera.getImageRemote(nameId)
		
		#create image
		width = result[0]
		height = result[1]
		image = np.zeros((height, width, 3), np.uint8)

		# get image
		result = camera.getImageRemote(nameId)

		'''if result == None:
		print 'cannot capture.'
		elif result[6] == None:
		print 'no image data string.'
		else:
		'''
				
		# translate value to mat
		values = map(ord, list(result[6]))
		i = 0
		for y in range(0, height):
			for x in range(0, width):
				image.itemset((y, x, 0), values[i + 0])
				image.itemset((y, x, 1), values[i + 1])
				image.itemset((y, x, 2), values[i + 2])
				i += 3
		
		# convert image to grayscale			
		image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                                    

		# detect faces using Haar Cascade, last parameter: min_neighbors
		faces = face_cascade.detectMultiScale(image_gray, 1.3, minNeighbors)

		# if no faces are detected, updates deviation time
		if len(faces) == 0:                    
			dynamic_time = time.time()
		
		# else, shows on screen the detected face, store the face on
		# a variable to be emotion-classified, and counts deviation time
		else:
			# runs through all faces found (expected only one, but runs on a loop just to be sure)
			for (x, y, w, h) in faces:
				# draws rectangle around the face
				cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
				
				# store the detected face with a few extra pixels, because
				# the cascade classifier cuts a litte too much
				face = image_gray[y-10:y+h+10, x-10:x+w+10]
				
				# if a time difference of 0.3 seconds is met, classify the emotion on a face
				time_diff = dynamic_time-time_emotion
				try:
					if(time_diff >= 0.3 and face is not None):
						info("Face detected. Classifying emotion.")
						# reshape image to meet the input dimensions
						face_to_classify = np.stack([face, face, face], axis=2)
						face_to_classify = cv2.resize(face_to_classify, input_shape[:2], interpolation=cv2.INTER_AREA) * 1./255
						# get inference from classifier
						classified_emotion = classifier.inference(face_to_classify)
						# writes emotion on the image, to be shown on screen
						cv2.putText(image, classified_emotion, (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)			
						# store image on a folder, for future analysis
						cv2.imwrite("emotion_imgs/{}.png".format(dynamic_time), face)
						c.write("{} {}\n".format(dynamic_time, classified_emotion))
						# reset time
						time_emotion = time_diff
						info("Emotion classified: {}".format(classified_emotion))
						emotions[classified_emotion] += 1
				except Exception as e:
					pass
			# if the time difference meets a threshold, count it as a deviation
			diff = dynamic_time - static_time
			if diff > 0.7:
				# increase the number of deviations detected
				n_deviations += 1
				# stores the time of this deviation
				arq.write("Tempo do desvio: {:.2f}\n".format(diff))
				deviation_times.append(diff)
				#increases total disattention time
				time_disattention += diff
				info("Deviation detected")
			static_time = dynamic_time = time.time()

		# show image on screen
		cv2.imshow('img',image)

		# check if running will continue
		if cv2.waitKey(1) and run_state == 'stop':
			info("Stop detected. Breaking execution!")
			break;
	
	c.close()
	
	# clear opencv windows
	cv2.destroyAllWindows()
	# release camera
	camera.unsubscribe(nameId)

	# calculate total attention time
	time_attention = time.time() - time_attention - time_disattention
	# write info about the whole session
	totals = "Total number of deviations:{}. Total time on disattention: {:.2f}. Time on attention: {:.2f}\n".format(
		n_deviations, time_disattention, time_attention)
	arq.write(totals)
	arq.close()
	info("Verbose deviation file written.")

	if n_deviations >= 2:
		attention = False
	
	# write on raw data file
	arq_ret = open('statistics.dat', 'w');
	data = "{}\n{:.2f}\n{:.2f}\n".format(n_deviations, time_disattention, time_attention)
	arq_ret.write(data)
	arq_ret.close()
	string = 'running'
	info("Raw data deviation file written")
