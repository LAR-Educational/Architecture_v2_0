# -*- coding: utf-8 -*-

import naoqi
import time
#import numpy as np
from Modules import dialog
from Modules import vars as core
from Modules import disattention
from Modules import vision
#import os
#import sys
#ip = "169.254.178.70"
#port = 9559

# ----- System imports -----

import sys
import time
import cv2
import csv
import os
import pickle
import random
from pprint import pprint
import numpy as np


# ---------- Activities Imports -------
from Activities.Jokenpo import jokenpo_main as jkp
from Activities.Atores import atores as emo
from Activities.Historias import historias
from Activities.Exercicio import exercicio as ex 
from Activities.Prateleira import shelf
from Activities.Drogas import drugs
from Modules.Memory import fileHelper

def main():
 	
	time_count = time.time()

	info("Starting program ")            

	info("Connecting with NAO")
 	nao = False

	try:
		#core.initializer();
	 	nao=core.Robot(core.robotIp, core.port)   
	except:
		info("Exception:" + str(sys.exc_info()[0]))
		print "Robô: ", nao
		raise


	info(" ----- Starting Vision System -----")
	try:
		vs = vision.VisionSystem(nao) 
	except:
		error(" ----- Error loading Vision System -----")
		war("Exception type:" + str(sys.exc_info()[0]))
		raise


	info(" ----- Starting Dialogue System -----")
	try:
		ds = dialog.DialogSystem(nao,'Modules/Dialog') 
	except:
		error(" ----- Error loading Dialogue System -----")
		war("Exception type:" + str(sys.exc_info()[0]))
		raise

	nao.motors.wakeUp()
	
	#jkp.play(nao, ds, 3)

	#ds.say("Continue sentado para próxima brincadeira", block=False)
	#attention = disattention.Th(1)
	#attention.start()
	#emo.play(nao, ds, attention)
	#attention._end_classification()

	
        #ds.say("Falando alguma coisa para testar o volume")
        
        #nao.tts.setVolume(1.0)
        
        #ds.say("Falando alguma coisa para testar o volume")
        

	nao.posture.goToPosture("StandInit",1)
	#return 1

	emo_file_log = open("Log/Emotions_log_"+str(core.interaction_id), "w+")





	prefferences = True
	play_drugs = False  #True
	play_ex =  False #True
	play_shelf =  False #True
	play_act =  False #True
	play_jkp =  False #True
	play_hist = True

	#'''
	userModel = fileHelper.fileHelper()
	ds.say('E aí, ser humaninho! Meu nome é tédi. E o você, qual é seu nome?')
	#print(u'Qual é seu nome?')
	#nome = ds.getFromMic_Pt()#raw_input()
	#nao.leds.post.fadeRGB('eyes', 'green', 2.5)
	
	right_name=False

	while not right_name:
		nome = ds.get_input() #raw_input()
		ds.say("Eu entendi, " + nome + ". Estou certo?")
		userAns= ds.get_input()
		
		if ("sim" in userAns) or ("está" in userAns) or ("esta" in userAns) or ("certo" in userAns) or ("isso" in userAns) or ("é" in userAns):
		
			right_name=True
			ds.say("Que nome tópi!")
		
		else:
			ds.say("Vamos tentar de novo então. Espere e Repita.")
	
	
	userPath= "./Usuarios/" + nome + ".dat"
	
	
	
	
	if prefferences:	
		print userPath
		
		if os.path.exists( userPath  ):
			ds.say("Já te conheço")
			preferences = userModel.getPreferences(nome)
		
		else:
			ds.say('Qual é a sua idade?')
			#answer = ds.getFromMic_Pt()#raw_input()
			answer = ds.get_input()#raw_input()
			userModel.addPreference(nome, answer, 'idade')

			#print(u'Qual é o seu esporte favorito?')
			ds.say("Qual seu esporte favorito")
			#answer = ds.getFromMic_Pt()#raw_input()
			answer = ds.get_input()#aw_input()
			if answer =="volei" or answer == "vôlei":
				answer = "voleibol"
			
			userModel.addSearchQueue([answer], nome, 'esporte favorito')

			#print(u'Qual é a sua comida favorita?')
			ds.say("Qual sua comida favorita?")
			#answer = ds.getFromMic_Pt()#raw_input()
			answer = ds.get_input()#aw_input()
			userModel.addSearchQueue([answer], nome, 'comida favorita')

			#print(u'Qual é a sua música favorita?')
			ds.say("Qual sua banda preferida?")
			#answer = ds.getFromMic_Pt()#raw_input()
			answer = ds.get_input()#aw_input()
			userModel.addSearchQueue([answer], nome, 'musica favorita')

			preferences = userModel.getPreferences(nome)
		
	
	#CONDITION 1
	#ds.say(" Vamos fazer uma série de atividades agora. Está preparado? Vamos lá")


	# Starting threads
	attention = disattention.Th(1)
	attention.start()

	
	attention._halt()

	if play_drugs:
		drugs.play(nao, ds)
	
	if prefferences:
		try:
			ds.say(u'Sobre seu esporte preferido: \n{}'.format(
			    userModel.search([preferences['esporte favorito'].encode('utf-8')])).encode('utf-8'))
			
			#print (u'Sobre seu esporte preferido: \n{}'.format(
			    #userModel.searchFile([preferences['esporte favorito'].encode('utf-8')])).encode('utf-8'))
	
			#raw_input("GO!")
			
			#'''
			
			attention._continue()
			
			ds.say("Estou certo? ")
			
			userAns = ds.get_input()
                        
			if ("sim" in userAns) or ("está" in userAns) or ("esta" in userAns) or ("certo" in userAns):
				ds.say("Manjo muito")	
			
				ds.say("Gostei, " + nome + ". Se um dia eu conseguir escapar desse laboratório, Essse será o esporte pra deixar minha saúde em dia. ")
				
			else:
				ds.say("Droga. Vou melhorar minha busca. Nunca fui bom com coisas de humanos mesmo.")
			#'''
		

			attention._halt()
			
			pprint("Esporte favorito: " , emo_file_log) 
			pprint(userModel.search([preferences['esporte favorito'].encode('utf-8')]).encode('utf-8'), emo_file_log)
			pprint(core.emotions, emo_file_log)
			pprint("", emo_file_log)
			print(core.emotions)
			core.clear_emo_variables()

			ds.say("Certo. Vamos seguir com a atividade")

		except Exception as e:
			print(e)
	
	
	
	if play_shelf:
		shelf.play(nao, ds)
	
	if play_ex:
		ex.play(nao, ds)
	
	#ds.say("Certo. Vamos seguir com a interação")
	


	# ------------------------ Stories ----------------------------------

	if play_hist:
		#attention = disattention.Th(1)
		#attention.start()
		#attention._continue()
		historias.play(nao, ds, attention)
		#attention._end_classification()
	

	# ------------------------ Jokenpo ----------------------------------

	if play_jkp:
		#nao.behavior.post.runBehavior('wsafe-c66573/behavior_1')
		ds.say("Vamos jogar um pouco. Que tal Jó quem pô? Tenha paciência comigo, eu demoro um pouco para definir as jogadas. Puxe uma cadeira e sente na minha frente. Me avise quando estiver pronto", animated=True)
		raw_input("GO!")
		ds.say("Então vamos lá")
		jkp.play(nao, ds, 3)



	# ------------------------ ACTORS ----------------------------------
	
	if play_act:
		ds.say("Continue sentado para próxima brincadeira", block=False)
		attention = disattention.Th(1)
		attention.start()
		emo.play(nao, ds, attention)
		attention._end_classification()


	nao.posture.goToPosture("StandInit", 1)




	if prefferences:
		try:


			ds.say(u'Sobre o rango que tu mais curte: \n{}'.format(
			    userModel.search([preferences['comida favorita'].encode('utf-8')])).encode('utf-8'))
			#print(u'Sobre o rango que tu mais curte: \n{}'.format(
			   # userModel.searchFile([preferences['comida favorita'].encode('utf-8')])).encode('utf-8'))
			
			attention._continue()
			ds.say("Eca. Que nojo. Você tem gostos peculiares. sorte minha que não como")
			
			
			attention._halt()
			pprint("Comida favorito: " , emo_file_log) 
			pprint(userModel.search([preferences['comida favorita'].encode('utf-8')]).encode('utf-8'), emo_file_log)
			pprint(core.emotions, emo_file_log)
			pprint("", emo_file_log)
			print(core.emotions)
			core.clear_emo_variables()
		
		
		except Exception as e:
			print(e)

	#raw_input("GO!")

	if prefferences:
		try:
			
			ds.say(u'Sobre sua Banda preferida: {}'.format(userModel.search([preferences['musica favorita'].encode('utf-8')])).encode('utf-8'))
			
			attention._continue()
			ds.say("Nossa. Nunca nem vi. Como eu sou robô, pra mim é só metal. Risos.")
				
			attention._halt()
			pprint("Musica favorita: " , emo_file_log) 
			pprint(userModel.search([preferences['musica favorita'].encode('utf-8')]).encode('utf-8'), emo_file_log)
			pprint(core.emotions, emo_file_log)
			pprint("", emo_file_log)
			print(core.emotions)
			core.clear_emo_variables()
		
		
		except Exception as e:
			print(e)


	#Closing threads
        userModel.close()
	attention._end_classification()
	emo_file_log.close()

	#CONDITION 2
	#jkp.play(nao, ds, 3)
	#emo.play(nao, ds, attention)
	#attention._end_classification()
	#ex.play(nao, ds)
	#shelf.play(nao, ds)
	#drugs.play(nao, ds)
	



	time_log = open("Times.csv", "a+")
	time_log.write(str(core.interaction_id) + " , " +  nome + " , " + str((time.time()-time_count)/60)+ " , "+  str((time.time()-time_count)%60) + "\n")
	time_log.close()

	nao.posture.goToPosture("Crounch",1)
        ds.say("Então é isso. Foi um prazer interagir com você, "+ nome +" . Espero te ver em breve. Até mais.", block=False)
	
        nao.motors.rest()
	
        
        
        return 1	
	
	
	





def info(stringToPrint):   
    if core.debug:
            core.info(stringToPrint)            

    
def war(stringToPrint):   
    if core.debug:
            core.war(stringToPrint)            

    
def error(stringToPrint):   
    if core.debug:
            core.error(stringToPrint)            






if __name__=="__main__":
	main()
	
	
	
	


	
