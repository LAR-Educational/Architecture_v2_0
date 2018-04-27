# -*- coding: utf-8 -*-
import naoqi
import numpy as np
from Modules import dialog
from Modules import vars

ip = "169.254.178.70"
port = 9559
speed = 80

robot = vars.Robot(ip,port)

animatedSpeech = naoqi.ALProxy("ALAnimatedSpeech", ip, port)
posture = naoqi.ALProxy("ALRobotPosture", ip, port)
speech = naoqi.ALProxy("ALTextToSpeech", ip, port)
speechRecognition = naoqi.ALProxy("ALSpeechRecognition", ip, port)

posture.goToPosture("Stand", speed)
animatedSpeech.say("Ola amiguinho! Vamos brincar de sério? Fique na minha frente para que possa te ver")

