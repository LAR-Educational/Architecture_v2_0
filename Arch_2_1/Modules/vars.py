# -*- coding: utf-8 -*-

import csv
from naoqi import ALProxy
import vision_definitions
import pickle
import os
from pprint import pprint

"""
Created on Thu May  4 16:06:04 2017

@author: dtozadore
"""

teddy_ip="169.254.178.70"

robotIp=teddy_ip
port = 9559
robotIp="169.254.178.70"


#variable to check if the robot is conected
naoConeted= True

# System Variables
debug = True
Ykey = 'y'
classifierType = "all"
training_path = "modules/vision_components/classifiers/DBIM/alldb"

emotions = []
deviation_times = []
# Default Language
defaultLanguage = 'Brazilian'

ESC = 1048603 #27
ENTER = 1048586 #13

attention=False

current_path= os.getcwd()

#emotion vars
labels_dict = {
    0: 'happy', 1: 'neutral', 2: 'surprise',
    3: 'fear', 4: 'disgust', 5: 'angry', 6: 'sad'}
input_shape = (224,224,3)


def load_classes(file_name):

	with open(file_name, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in spamreader:
			return row
	

  



class Robot:
	
	#naoConected = 

	def __init__(self, roboIp, port, robot_name = "Tédi", defaultLanguage = 'Brazilian'):
		try:
			self.tts = ALProxy("ALTextToSpeech", robotIp, port)
			self.behavior = ALProxy("ALBehaviorManager", robotIp, port)
			self.motors =  ALProxy("ALMotion", robotIp, port)
			self.posture = ALProxy("ALRobotPosture", robotIp, port)
			self.camera = ALProxy("ALVideoDevice", robotIp, port)
			self.disattention = False
			self.name = robot_name
			self.tts.setLanguage(defaultLanguage)
			self.animatedSpeechProxy = ALProxy("ALAnimatedSpeech", robotIp, port)
			self.speechSpeed = 70
		except:
			print "Unexpected error conneting NAO"
			#return False
    		#raise
    		
  		
    		
    		
    		
'''
if(naoConeted):
    tts = ALProxy("ALTextToSpeech", robotIp, port)
    behavior = ALProxy("ALBehaviorManager", robotIp, port)
    motors =  ALProxy("ALMotion", robotIp, port)
    posture = ALProxy("ALRobotPosture", robotIp, port)
    camera = ALProxy("ALVideoDevice", robotIp, port)

def initializer():
	
	#vars.shapes = load_classes('shapes.csv')
    
	#if(naoConeted):
        #tts = ALProxy("ALTextToSpeech", robotIp, 9559)
#        tts = ALProxy("ALTextToSpeech", robotIp, 9559)
#        behavior = ALProxy("ALBehaviorManager", robotIp, 9559)
#        motors =  ALProxy("ALMotion", robotIp, 9559)
#        posture = ALProxy("ALRobotPosture", robotIp, 9559)

		
		#motors.wakeUp()

def finisher():
    
    
    if(naoConeted):
        motors.rest()

'''        





class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

   
   
def info(stringToPrint):   
    
    if debug:
            print bcolors.OKBLUE + "[I] " + stringToPrint + bcolors.ENDC

def war(stringToPrint):   
    
    if debug:
            print bcolors.WARNING + "[W] " + stringToPrint + bcolors.ENDC

def error(stringToPrint):   
    
    if debug:
            print bcolors.FAIL + "[E] " + stringToPrint + bcolors.ENDC

def nao_say(stringToPrint):   
    
    if debug:
            print bcolors.OKGREEN + "[Saying] " + stringToPrint + bcolors.ENDC



class ReadValues:
    """
     Class to hold read values
    
    """
    
    def __init__(self, deviations=5, emotionCount=3, 
                    numberWord=1, time2ans=20, sucRate=1        ):
                    
        self.deviations = deviations 
        self.emotionCount = emotionCount  
        self.numberWord =  numberWord
        self.time2ans = time2ans
        self.sucRate = sucRate
        


class Weights:

    def __init__(self, alpha, beta, gama):
        self.alpha = alpha
        self.beta = beta
        self.gama =  gama



class AdaptiveSystem:

    def __init__(self, robot, path, op, w, rv):
    
        self.robot = robot
        self.path = path
        self.op = op
        self.w = w #weights class
        self.rv = rv