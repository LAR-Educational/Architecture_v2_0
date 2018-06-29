# -*- coding: utf-8 -*-
import naoqi
import time
import numpy as np
import random
from Modules import dialog
from Modules import vars as core
from Modules import disattention

def read_hist():
	arq = open("Activities/Historias/indices.txt" , "r")
	historiasfile = arq.read().split("\n")
	historiasfile = historiasfile[0:10]
	historias= []
	r = random.sample(range(10), 3)
	for x in xrange(0,3):
		arq = open("Activities/Historias/" + historiasfile[r[x]] + ".txt", "r")
		historias.append(arq.read().split("\n"))
		historias[x] = historias[x][0:len(historias[x])-1]
	return historias

ip = core.robotIp #"169.254.178.70"
port = 9559
speed = 70

robot = core.Robot(ip,port)

#disattention.Th.load_classifier()

animatedSpeech = naoqi.ALProxy("ALAnimatedSpeech", ip, port)
speech = naoqi.ALProxy("ALTextToSpeech", ip, port)
motion = naoqi.ALProxy("ALMotion", ip, port)
leds = naoqi.ALProxy("ALLeds", ip, port)
group = ['FaceLed0', 'FaceLed1', 'FaceLed2', 'FaceLed3', 'FaceLed4',
	'FaceLed5', 'FaceLed6', 'FaceLed7']
leds.createGroup('eyes', group)

#motion.wakeUp()
#speech.setLanguage("Brazilian")

hist_dict = read_hist()

#speech.say("Olá amiguinho! O meu nome é Teddy. Chega mais perto que eu tenho umas histórias pra contar pra você")

def play(att):

	r = np.random.randint(0,2)
	for i in range(0,3):
		#attention = disattention.Th(1)
		#attention.start()
	
		att._continue()
		
		totalWords =  0
		totalSec =  0
		#if i == 0:
			#animatedSpeech.say("Agora vou contar a primeira história")
		#if i == 1:
			#animatedSpeech.say("Agora vou contar a segunda história")
		#if i == 2:
			#animatedSpeech.say("Agora vou contar a terceira história")
		for j in range(1,int(hist_dict[i][0])+1):
			#animatedSpeech.say(hist_dict[i][j])
			#speech.say("Agora farei uma pergunta sobre esta parte da historia ")
			indice = j + int(hist_dict[i][0])
			speech.say(hist_dict[i][indice])
			leds.post.fadeRGB('eyes', 'green', 2.5)
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
			leds.fadeRGB('eyes', 'white', 0.1)		
		totalWords = np.ceil(totalWords/int(hist_dict[i][0]))
		totalWSec = np.ceil(totalSec/int(hist_dict[i][0]))
		core.ReadValues(numberWord=totalWords, time2ans=totalSec)
	
		att._halt()
		
		
		core.clear_emo_variables()
		
		#closeAttention = disattention.Th(2)
		#closeAttention.start()
		
		
	leds.fadeRGB('eyes', 'white', 0.1)

	#motion.rest()








