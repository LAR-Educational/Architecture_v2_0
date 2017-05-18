# -*- coding: utf-8 -*-
"""
Created on Thu May  4 16:06:04 2017

@author: dtozadore
"""

robotIp="169.254.206.242"
port = 9559
#robotIp="169.254.186.197"

from naoqi import ALProxy
import vision_definitions

#variable to check if the robot is conected
naoConeted= True

if(naoConeted):
    tts = ALProxy("ALTextToSpeech", robotIp, port)
    behavior = ALProxy("ALBehaviorManager", robotIp, port)
    motors =  ALProxy("ALMotion", robotIp, port)
    posture = ALProxy("ALRobotPosture", robotIp, port)
    camera = ALProxy("ALVideoDevice", robotIp, port)

# System Variables
debug = True
Ykey = 'y'
classifierType = "all"
training_path = "modules/vision_components/classifiers/DBIM/alldb"


# Default Language
defaultLanguage = 'Brazilian'

path = "/home/dtozadore/Projects/Arc_2/ICs"
    



def initializer():
    
    if(naoConeted):
        #tts = ALProxy("ALTextToSpeech", robotIp, 9559)
#        tts = ALProxy("ALTextToSpeech", robotIp, 9559)
#        behavior = ALProxy("ALBehaviorManager", robotIp, 9559)
#        motors =  ALProxy("ALMotion", robotIp, 9559)
#        posture = ALProxy("ALRobotPosture", robotIp, 9559)

        tts.setLanguage(defaultLanguage)
        #motors.wakeUp()




def finisher():
    
    
    if(naoConeted):
        motors.rest()
        

   
def info(stringToPrint):   
    
    
    if debug:
            print("[INFO ] "+ stringToPrint)            





