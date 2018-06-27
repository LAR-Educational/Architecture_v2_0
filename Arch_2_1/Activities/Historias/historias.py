# -*- coding: utf-8 -*-
import naoqi
import time
import numpy as np
from Modules import dialog
from Modules import vars
from Modules import disattention

def read_hist():
	for x in xrange(0,3):

		historiasfile = arq.read().split("\n")
		historiasfil = historias[0:10]
		r = np.random.randint(0,10)
		arq = open("Activities/Historias/" + str(r) , "r")
	
		historias.append(arq.read().split("\n"))
		historias[x] = historias[0:10]


ip = "169.254.178.70"
port = 9559
speed = 70

robot = vars.Robot(ip,port)

attention = disattention.Th(1)
attention.start()
time.sleep(10)

animatedSpeech = naoqi.ALProxy("ALAnimatedSpeech", ip, port)
posture = naoqi.ALProxy("ALRobotPosture", ip, port)
speech = naoqi.ALProxy("ALTextToSpeech", ip, port)
speechRecognition = naoqi.ALProxy("ALSpeechRecognition", ip, port)
motion = naoqi.ALProxy("ALMotion", ip, port)

motion.wakeUp()
speech.setLanguage("Brazilian")
speechRecognition.setLanguage("Brazilian")

postures = ["Sit", "Stand"]



i = 0
for hist in historias:
	hist_dict[str(i)] = hist
	i += 1

# posture.goToPosture("Stand", speed)
speech.say("Olá amiguinho! O meu nome é Teddy. Chega mais perto que eu tenho umas histórias pra contar pra você")

for i in range(0,1):
	
	r = np.random.randint(0,2)
	print(postures[r])
	posture.goToPosture("Sit", speed)
	r = np.random.randint(0,10)
	animatedSpeech.say(hist_dict[str(r)])
	
	speech.say("Você pode resumir essa história pra mim?")
	dial = dialog.DialogSystem(robot,"respostas")
	print hist_dict[str(r)]
	answer = dial.getFromMic_Pt()
	print dial.levenshtein_long_two_strings(answer, hist_dict[str(r)])
	print dial.levenshtein_short_two_strings(answer, hist_dict[str(r)])

closeAttention = disattention.Th(2)
closeAttention.start()

posture.goToPosture("Sit", speed)
motion.rest()
