from __future__ import print_function
import cv2
import numpy as np
import time
import requests

import settings

command = ''
def setCommand(cmd):
	global command
	command = cmd

class EmotionClassifier(object):
	def __init__(self):
		self._url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
		self._key = '2169da679d364ccea62752b245cb5fe1'
		self._maxNumRetries = 10
		self.headers = dict()
		self.headers['Ocp-Apim-Subscription-Key'] = self._key
		self.headers['Content-Type'] = 'application/octet-stream'
		self.json = None
		self.params = None

	# Function that sends the image to the server for classification
	# Returns the result as a dict, with the emotions and their probabilities.
	def processRequest(self, data):
		retries = 0
		result = None

		while True:
			# makes a request to the server
			response = requests.request('post', self._url, json = self.json, data = data, headers = self.headers, params = self.params)

			# if the server response is negative, retries up to a max number of retries
			if(response.status_code == 429):
				settings.info("MC API: message: %s" % (response.json()['error']['message']), 1)
				if(retries <= self._maxNumRetries):
					time.sleep(1) 
					retries += 1
					continue
				else: 
					settings.info('MC API error: failed after retrying!', 3)
					break
			# if the response is positive, treats it
			elif(response.status_code == 200 or response.status_code == 201):
				if('content-length' in response.headers and int(response.headers['content-length']) == 0):
					result = None 
				elif('content-type' in response.headers and isinstance(response.headers['content-type'], str)):
					if('application/json' in response.headers['content-type'].lower()):
						result = response.json() if response.content else None 
					elif('image' in response.headers['content-type'].lower()):
						result = response.content
			# if an the response is an error, shows it on the screen
			else:
				settings.info("MC API error code: %d" % (response.status_code), 3)
				settings.info("MC API message: %s" % (response.json()['error']['message']), 3)
			break
		
		return result

	# Functions that calls request to read and process images
	# Receives an opencv image
	# Returns the most likely expression and a dict with all the emotions and their likelihood
	def read_emotions(self, image, n):
		# converts the image to a data string
		data = cv2.imencode('.jpg', image)[1].tostring()

		# gets the result
		result = self.processRequest(data)

		# if a valid result is returned, then we rearrange it by values, instead of emotions
		# and find the maximum value, which is the most likely expressed emotion on the image
		if result:
			vals = {result[0]['scores']['neutral']:'neutral'}
			vals[result[0]['scores']['sadness']] = 'sadness'
			vals[result[0]['scores']['disgust']] = 'disgust'
			vals[result[0]['scores']['anger']] = 'anger'
			vals[result[0]['scores']['fear']] = 'fear'
			vals[result[0]['scores']['contempt']] = 'contempt'
			vals[result[0]['scores']['surprise']] = 'surprise'
			vals[result[0]['scores']['happiness']] = 'happiness'
			vals[result[0]['scores']['sadness']] = 'sadness'
			
			# store on the file the predominant emotion on the first line
			# and the dict with all the emotions on the next line
			emotion = str(max(vals)) + ': ' + vals[max(vals)]

		return emotion, vals

	def write(self, main_emotions, all_emotions):
		i = 1
		file = open(str(time.time())+'.txt', 'w')
		for main_emotion, all_emotion in zip(main_emotions, all_emotions):
			file.write("Image "+str(i)+"\n")
			file.write("Predominant emotion: " + str(main_emotion) + "\n")
			file.write(str(all_emotion) + "\n\n")
			i+=1
		file.close()

	# Starts the execution
	def start(self):
		global command
		imgCounter = 0
		notImgCounter = 0
		main_emotions = []
		all_emotions = []

		settings.info('EC: starting execution of emotion classifier')

		while True:
			if(command == 'write'):
				settings.info('EC: writing information aquired up to this point')
				self.write(main_emotions, all_emotions)
				command = ''
				main_emotion = []
				all_emotions = []
			elif(command == 'end'):
				self.write(main_emotions, all_emotions)
				settings.info('EC: finishing execution of emotion classifier')
				break
	
			img = cv2.imread(str(imgCounter)+'.jpg', 0)
	
			if(img is None):
				notImgCounter += 1
			else:
				lists = [main_emotions, all_emotions]
				appenders = self.read_emotions(img, imgCounter)
				
				for x, lst in zip(appenders, lists):
					lst.append(x)
				imgCounter += 1

			#stops the execution if no image is found in a certain amount of time
			if notImgCounter == 500000:
				self.write(main_emotions, all_emotions)
				break
