# -*- coding: utf-8 -*-
import naoqi
import time
import numpy as np
import random
from pprint import pprint
from Modules import dialog
from Modules import vars as core
from Modules import disattention
from Modules import adaption


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


	fileLog = open ("Log/adaptive_" + str(time.time()), "w+")
	
	w = adaption.Weights(0.5, 0.2, 0.3 )	
	op = adaption.OperationalParameters (max_deviation=2, max_emotion_count=25, 
									min_number_word=1 , max_time2ans=10, min_suc_rate=1)
	
	
	adp = adaption.AdaptiveSystem(op,w,core.userPar)
	
	
	r = np.random.randint(0,2)
	for i in range(0,2):
		#attention = disattention.Th(1)
		#attention.start()
	
		att._continue()
		
		
		fileLog.write("Round history" + str(i)) 
		
		
		
		totalWords =  0
		totalSec =  0
		#if i == 0:
			#animatedSpeech.say("Agora vou contar a primeira história")
		#if i == 1:
			#animatedSpeech.say("Agora vou contar a segunda história")
		#if i == 2:
			#animatedSpeech.say("Agora vou contar a terceira história")
		

		for j in range(1,int(hist_dict[i][0])+1):
			
			
			animatedSpeech.say(hist_dict[i][j])
			
			
			fileLog.write("Sorted story"+ hist_dict[i][j])
			fileLog.write("\n")
			
			speech.say("Agora farei uma pergunta sobre esta parte da historia ")
			indice = j + int(hist_dict[i][0])
			speech.say(hist_dict[i][indice])
			
			fileLog.write("Question " + str(i) +" : " + hist_dict[i][indice] )
			fileLog.write("\n")
			
			
			leds.post.fadeRGB('eyes', 'green', 2.5)
			dial = dialog.DialogSystem(robot,"respostas")
			print hist_dict[i][j]
			start = time.time()		
			
			
			answer = core.get_input()#dial.getFromMic_Pt()
			#raw_input("Digite a resposta: ")#
			
			totalSec += time.time() - start
			
			success_rate = dial.levenshtein_long_two_strings(answer, hist_dict[i][indice])
			
			print "longest", success_rate
			print "short", dial.levenshtein_short_two_strings(answer, hist_dict[i][indice])
			print answer
			fileLog.write("Answer " + answer)
			fileLog.write("\n")
			
			#print core.emotions
			#print core.deviation_times
			totalWords += dial.coutingWords(answer)
			leds.fadeRGB('eyes', 'white', 0.1)		
		totalWords = np.ceil(totalWords/int(hist_dict[i][0]))
		totalWSec = np.ceil(totalSec/int(hist_dict[i][0]))
		#core.ReadValues(numberWord=totalWords, time2ans=totalSec)
	
		core.userPar.set( deviations= len(core.deviation_times), 
							emotionCount= core.getBadEmotions(),
							numberWord=totalWords, 
							time2ans=totalWSec, 
							sucRate= success_rate)
	
		fvalue = adp.adp_function()
	
	
		fileLog.write("F Value "  +" : " + str(fvalue) )
		fileLog.write("")
		print "FVALUE", fvalue
		fileLog.write("\n\n\n --------- END OF STORY--------------\n\n\n\n")
			
		
		#fileLog.write(pprint(vars(core.userPar)))
		pprint(vars(core.userPar))
		
		pprint(vars(core.userPar), fileLog)
		
		
		att._halt()
		
		core.clear_emo_variables()
		
		#closeAttention = disattention.Th(2)
		#closeAttention.start()
		
		
	leds.fadeRGB('eyes', 'white', 0.1)
	
	#motion.rest()

	fileLog.close()






