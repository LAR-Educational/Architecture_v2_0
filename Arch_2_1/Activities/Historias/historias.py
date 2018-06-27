# -*- coding: utf-8 -*-
import naoqi
import time
import numpy as np
from Modules import dialog
from Modules import vars as core
from Modules import disattention

def read_hist():
	arq = open("Activities/Historias/indices.txt" , "r")
	historiasfile = arq.read().split("\n")
	historiasfile = historiasfile[0:10]
	historias= []
	for x in xrange(0,3):
		r = np.random.randint(0,10)
		arq = open("Activities/Historias/" + historiasfile[r] + ".txt", "r")
		historias.append(arq.read().split("\n"))
		historias[x] = historias[x][0:len(historias[x])-1]
	return historias

ip = "169.254.178.70"
port = 9559
speed = 70

robot = core.Robot(ip,port)

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

r = np.random.randint(0,2)
for i in range(0,3):
	totalWords =  0
	totalSec =  0
	print(postures[r])
	#posture.goToPosture("Sit", speed)
	for j in range(1,int(hist_dict[i][0])+1):
		animatedSpeech.say(hist_dict[i][j])
		speech.say("Agora farei uma pergunta sobre esta parta da historia ")
		indice = j + int(hist_dict[i][0])
		speech.say(hist_dict[i][indice])
		dial = dialog.DialogSystem(robot,"respostas")
		print hist_dict[i][j]
		start = time.time()		
		answer = dial.getFromMic_Pt()
		totalSec += time.time() - start
		print dial.levenshtein_long_two_strings(answer, hist_dict[i][indice])
		print dial.levenshtein_short_two_strings(answer, hist_dict[i][indice])
		print answer
		print core.emotions
		print core.deviation_times
		totalWords += dial.coutingWords(answer)
	totalWords = np.ceil(totalWords/int(hist_dict[i][0]))
	totalWSec = np.ceil(totalSec/int(hist_dict[i][0]))
	core.ReadValues(numberWord=totalWords, time2ans=totalSec)

closeAttention = disattention.Th(2)
closeAttention.start()

posture.goToPosture("Sit", speed)
motion.rest()








