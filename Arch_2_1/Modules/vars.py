# -*- coding: utf-8 -*-

import csv
from naoqi import ALProxy
import vision_definitions
import pickle
import os
from pprint import pprint
import operator



"""
Created on Thu May  4 16:06:04 2017

@author: dtozadore
"""


teddy_ip="169.254.178.70"
dolores_ip="169.254.65.171"
actual_ip="169.254.201.16"

robotIp=teddy_ip
port = 9559
#robotIp=current_ip

flag_log = True



scname = ".system_control.dat"
if os.path.exists(scname):
	sys_ctrl = open(scname, "a+")
	lines = sys_ctrl.readlines()
	interaction_id = int(lines[-1])
	sys_ctrl.write(str(interaction_id + 1) + "\n")
	sys_ctrl.close()
	print ("Loading system control variables!")

else:
	sys_ctrl = open( scname, "w+")
	#lines = sys_ctrl.readlines()
	interaction_id =  0 #int(lines[-1])
	sys_ctrl.write(str(interaction_id) + "\n")
	sys_ctrl.close()
	print("Creating  system control file!")





class ReadValues:
    """
     Class to hold read values
    
    """
    def __init__(self, deviations=0, emotionCount=0,
                 numberWord=0, time2ans=0, sucRate=0):
        self.deviations = deviations 
        self.emotionCount = emotionCount  
        self.numberWord =  numberWord
        self.time2ans = time2ans
        self.sucRate = sucRate
    
    def set(self, deviations=0, emotionCount=0,
                 numberWord=0, time2ans=0, sucRate=0):
        self.deviations = deviations 
        self.emotionCount = emotionCount  
        self.numberWord =  numberWord
        self.time2ans = time2ans
        self.sucRate = sucRate
        


userPar = ReadValues()

     

#variable to check if the robot is conected
naoConeted= True

# System Variables
debug = True
Ykey = 'y'
classifierType = "all"
training_path = "modules/vision_components/classifiers/DBIM/alldb"

emotions = {'happy': 0, 'sad': 0, 'angry': 0, 'disgust': 0,
 	'surprise': 0, 'fear': 0, 'neutral': 0}

#emotions = {'felicidade': 0, 'tristeza': 0, 'raiva': 0, 'nojo': 0,
 	#'surpresa': 0, 'fear': 0, 'neutra': 0}




deviation_times = []



def getBadEmotions():
	
	emo =  emotions['sad'] + emotions['angry'] +  emotions['disgust'] + emotions['fear']     
	print "Number of bad emotions", emo

	return emo


def clear_emo_variables():

	global emotions
	for i in emotions.keys():
		emotions[i] = 0
	
	#print "DEVIATION", deviation_times
	global deviation_times
	del deviation_times[:]
	

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


translated_emotions = {
    'happy': 'Feliz', 'neutral': 'neutro', 'surprise': 'surpresa',
    'fear': 'medo', 'disgust': 'nojo', 'angry': 'raiva', 'sad': 'tristeza'}



input_shape = (224,224,3)



input_option_list = {'mic': 1 , 'key':-1}

input_option = input_option_list['mic'] 

'''
def get_input(ds):
	Get input from mic or keyboard
	
	global input_option
	sentence = ''

	if input_option>0: #mic
		sentence = ds.getFromMic_Pt()
	elif input_option<0: #keyboard
		sentence = raw_input("Waiting keyboard entry: ")
	
	return sentence

'''




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
			self.speechSpeed = 0.5
			self.volume = 0.4
			self.tts.setVolume(self.volume)

			self.leds = ALProxy("ALLeds", robotIp, port)
			self.group = ['FaceLed0', 'FaceLed1', 'FaceLed2', 'FaceLed3', 'FaceLed4',
			              'FaceLed5', 'FaceLed6', 'FaceLed7']
			self.leds.createGroup('eyes', self.group)
			 

		except:
			print "Unexpected error conneting NAO"
			#return False
    		#raise
    		
  		
'''
    		
class Sys_Control:

	def __init__(self):
		
		
		ctrl_file = open("system_control.dat", "a+")
		
		core.info("Writing activity attributes" )
 
                 with open(os.path.join(,'activity.data'), 'wb') as f:
                        pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
 
                 core.info("Write successfull" )








def load_class():
	

	 with open(name, 'rb+') as f:
 		return pickle.load(f)
  
 	core.info("Loaded successfull" )
    		
    		
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


   
        
