# -*- coding: utf-8 -*-
import naoqi
import time
import numpy as np
from Modules import dialog
from Modules import vars
from Modules import disattention



def read_hist():
	arq = open("Activities/Historias/indices.txt" , "r")
	historiasfile = arq.read().split("\n")
	historiasfile = historiasfile[0:10]
	historias= []
	for x in xrange(0,3):
		r = np.random.randint(0,10)
		arq = open("Activities/Historias/" + historiasfile[r] , "r")
		historias.append(arq.read().split("\n"))
		historias[x] = historias[x][0:len(historias[x])-1]
	return historias

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

hist_dict = read_hist()

# posture.goToPosture("Stand", speed)
speech.say("Olá amiguinho! O meu nome é Teddy. Chega mais perto que eu tenho umas histórias pra contar pra você")

for i in range(0, 3)
	r = np.random.randint(0,2)
	print(postures[r])
	posture.goToPosture("Sit", speed)
	for j in range(1,hist_dict[i][0]):
		animatedSpeech.say(hist_dict[i][j])
		speech.say("Agora farei uma pergunta sobre esta parta da historia ")
		speech.say(hist_dict[i][j+hist_dict[i][0]])
		dial = dialog.DialogSystem(robot,"respostas")
		print hist_dict[i][j]		
		answer = dial.getFromMic_Pt()
		print dial.levenshtein_long_two_strings(answer, hist_dict[i][j+(2*hist_dict[i][0])])
		print dial.levenshtein_short_two_strings(answer, hist_dict[i][j+(2*hist_dict[i][0])])
		print dial.coutingWords(answer)

#closeAttention = disattention.Th(2)
#closeAttention.start()

posture.goToPosture("Sit", speed)
motion.rest()
