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
	r = random.sample(range(10), 4)
	
	for x in xrange(0,4):
		arq = open("Activities/Historias/" + historiasfile[r[x]] + ".txt", "r")
		historias.append(arq.read().split("\n"))
		historias[x] = historias[x][0:len(historias[x])]
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

def play(robot, ds, att, max_hist=3):


	fileLog = open ("Log/Complete_Hist_" + str(core.interaction_id), "w+")
	
	w = adaption.Weights(0.2, 0.2, 0.6 )	
	op = adaption.OperationalParameters (max_deviation=3, max_emotion_count=125, 
		min_number_word=11 , max_time2ans=40, min_suc_rate=1)
	
	
	adp = adaption.AdaptiveSystem(robot, op,w,core.userPar)
	
	
	r = np.random.randint(0,2)
	for i in range(0,max_hist):
		#attention = disattention.Th(1)
		#attention.start()
	
		att._continue()
		
		
		fileLog.write("Round history " + str(i)) 
		
		ds.say("Preste atenção para estória número " + str(i+1))
		
		totalWords =  0
		totalSec =  0
		




		'''
		if i == 0:
			ds.say("Agora vou contar a primeira história")
		if i == 1:
			ds.say("Agora vou contar a segunda história")
		if i == 2:
			ds.say("Agora vou contar a terceira história")
		'''
		total_rate = 0


		for j in range(1,int(hist_dict[i][0])+1):
			
			# Conta a historia	
			ds.say(hist_dict[i][j])
			
			print hist_dict[i][j]

			gap = int(hist_dict[i][0])

			fileLog.write("\nSorted story: "+ hist_dict[i][j])
			fileLog.write("\n")
			
			# Apenas para resetar postura
			adp.change_behavior(0)
                        
                        # Parando a thread
                        att._halt()
			
                        ds.say("Agora farei uma pergunta sobre esta parte da historia ", animated=False)
			indice = j + int(hist_dict[i][0])
			
			# Faz a pergunta
			ds.say(hist_dict[i][indice], animated=False)
			
			
			fileLog.write("\nQuestion " + str(j) +" : " + hist_dict[i][indice] )
			#fileLog.write("\n")
			
			
			#leds.post.fadeRGB('eyes', 'green', 2.5)
			#dial = dialog.DialogSystem(robot,"respostas")
			start = time.time()		
			
			#print "length: ", len(hist_dict[i]) 
			#print "indece: ", indice 
			#print "gap: ", gap 
			#print "Question: ",  hist_dict[i][indice]
			print "expected answer: ", hist_dict[i][gap+indice] 
			answer = ds.get_input()#dial.getFromMic_Pt()

			#raw_input("Digite a resposta: ")#
			
			totalSec += time.time() - start
			
			success_rate = ds.levenshtein_long_two_strings(answer, hist_dict[i][gap+indice])

			real_rate = 1 - success_rate
			print "Real Rate: ", real_rate
			
			ds.say("Entendi uma resposta correta em, " + str(np.ceil(real_rate*100) ) + "por cento.", animated=False )

			#print "longest", success_rate
			#print "short", dial.levenshtein_short_two_strings(answer, hist_dict[i][indice])
			print answer
			fileLog.write("\nExpected Answer " + hist_dict[i][gap+indice])
			fileLog.write("\nUser Answer " + answer)
		        
                        ds.say("A resposta que eu esperava é: "+ hist_dict[i][gap+indice] )

			total_rate+=real_rate
						
			fileLog.write("\n")
			
                        #att._continue()
			
                        #print core.emotions
			#print core.deviation_times
			totalWords += ds.coutingWords(answer)
			#leds.fadeRGB('eyes', 'white', 0.1)		
		totalWords = np.ceil(totalWords/int(hist_dict[i][0]))
		totalWSec = np.ceil(totalSec/int(hist_dict[i][0]))
		#core.ReadValues(numberWord=totalWords, time2ans=totalSec)
		

		total_rate = total_rate / j

		core.userPar.set( deviations= len(core.deviation_times), 
							emotionCount= core.getBadEmotions(),
							numberWord= 10 - totalWords, 
							time2ans=totalWSec, 
							sucRate= 1- total_rate)
	
		fvalue = adp.adp_function(i)
	
		ds.say("Fim dessa estória. Posso mudar meu comportamento para tentar me adaptar melhor à nossa conversa.")

		ds.say("Não se assuste. Deixe-me ver se econtro uma posição e volume melhor.", block=False)

		# changing robot's behavior
		adp.change_behavior(adp.activation_function(fvalue))
		

		fileLog.write("\nFValue "  +" : " + str(fvalue) )
		fileLog.write("\n")
		print "FVALUE", fvalue
			
		
		#fileLog.write(pprint(vars(core.userPar)))
		pprint(vars(core.userPar))
		
		pprint(vars(core.userPar), fileLog)
		
		fileLog.write("\n\n --------- END OF STORY--------------\n\n\n\n")
		
		att._halt()
		
		core.clear_emo_variables()
		
		#closeAttention = disattention.Th(2)
		#closeAttention.start()
		
		
	leds.fadeRGB('eyes', 'white', 0.1)
	
	#motion.rest()

	fileLog.close()






