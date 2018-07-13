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

	#nao.motors.wakeUp()
	
	#jkp.play(nao, ds, 3)

	#ds.say("Continue sentado para próxima brincadeira", block=False)
	#attention = disattention.Th(1)
	#attention.start()
	#emo.play(nao, ds, attention)
	#attention._end_classification()

	#return 1
	
	nao.posture.goToPosture("Crouch", 1)

	prefferences = False #True
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
		ans= ds.get_input()
		
		if ans=="sim" or ans=="é" or ans=="isso":
			right_name=True
			ds.say("Que nome tópi!")
		
		else:
			ds.say("Vamos tentar de novo então. Espere e Repita.")
	
	
	userPath= "./Usuarios/" + nome + ".dat"
	
	
	
	
	if prefferences:	
		print userPath
		
		if os.path.exists( userPath  ):
			ds.say("Já te conheço")
			
		
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
	
	
	if play_drugs:
		drugs.play(nao, ds)
	

	if prefferences:
		try:
			ds.say(u'Sobre seu esporte preferido: \n{}'.format(
			    userModel.searchFile([preferences['esporte favorito'].encode('utf-8')])).encode('utf-8'))
			
			#print (u'Sobre seu esporte preferido: \n{}'.format(
			    #userModel.searchFile([preferences['esporte favorito'].encode('utf-8')])).encode('utf-8'))
	
			#raw_input("GO!")
			
			#'''
			ds.say("Estou certo? ")
			
			userAns = ds.get_input()
			
			if userAns == "sim":
				ds.say("Manjo muito")	
			
				ds.say("Gostei, " + nome + ". Essse será meu esporte preferido também. O que você acha?")
				time.sleep(3)
			else:
				ds.say("Droga. Vou melhorar minha busca. Nunca fui bom com coisas de humanos mesmo.")
			#'''
			ds.say("Certo. Vamos seguir com a atividade")
		
		except Exception as e:
			print(e)
	
	
	
	if play_shelf:
		shelf.play(nao, ds)
	
	if play_ex:
		ex.play(nao, ds)
	
	userModel.join()
	userModel.close()
	

	#ds.say("Certo. Vamos seguir com a interação")
	


	# ------------------------ Stories ----------------------------------

	if play_hist:
		attention = disattention.Th(1)
		attention.start()
		historias.play(nao, ds, attention)
		attention._end_classification()
	

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

	if prefferences:
		try:
			ds.say(u'Sobre o rango que tu mais curte: \n{}'.format(
			    userModel.searchFile([preferences['comida favorita'].encode('utf-8')])).encode('utf-8'))
			#print(u'Sobre o rango que tu mais curte: \n{}'.format(
			   # userModel.searchFile([preferences['comida favorita'].encode('utf-8')])).encode('utf-8'))
			
			ds.say("Eca. Que nojo. Você tem gostos peculiares. sorte minha que não como")
		except Exception as e:
			print(e)

	#raw_input("GO!")

	if prefferences:
		try:
			ds.say(u'\nSobre sua Banda preferida: \n{}'.format(
			    userModel.searchFile([preferences['musica favorita'].encode('utf-8')])).encode('utf-8'))
		
		except Exception as e:
			print(e)

	
	ds.say("Então é isso. Foi um prazer interagir com você, "+ nome +" . Espero te ver em breve. Até mais.", block=False)
	
	nao.motors.rest()

	
	
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
	
	
	
	


	
