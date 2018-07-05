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
		#raise

	nao.motors.wakeUp()
	
	#jkp.play(nao, ds, 3)

	#ds.say("Continue sentado para próxima brincadeira", block=False)
	#attention = disattention.Th(1)
	#attention.start()
	#emo.play(nao, ds, attention)
	#attention._end_classification()

	#return 1
	
	
	personalize = True
	play_drugs = True
	play_ex = True
	play_shelf = True
	play_act = True
	play_jkp = True


	#'''
	userModel = fileHelper.fileHelper()
	ds.say('E aí, ser humaninho! Meu nome é tédi. E o você, qual é seu nome?')
	#print(u'Qual é seu nome?')
	#nome = ds.getFromMic_Pt()#raw_input()
	nome = raw_input()

	ds.say(nome + "?")

	ds.say("Que nome tópi!")

	userPath= "./Usuarios/" + nome + ".dat"
	
	
	
	
	
	print userPath
	
	if os.path.exists( userPath  ):
		ds.say("Já te conheço")
		
	
	else:
		ds.say('Qual é a sua idade?')
		#answer = ds.getFromMic_Pt()#raw_input()
		answer = raw_input()
		userModel.addPreference(nome, answer, 'idade')

		#print(u'Qual é o seu esporte favorito?')
		ds.say("Qual seu esporte favorito")
		#answer = ds.getFromMic_Pt()#raw_input()
		answer = raw_input()
		userModel.addSearchQueue([answer], nome, 'esporte favorito')

		#print(u'Qual é a sua comida favorita?')
		ds.say("Qual sua comida favorita?")
		#answer = ds.getFromMic_Pt()#raw_input()
		answer = raw_input()
		userModel.addSearchQueue([answer], nome, 'comida favorita')

		#print(u'Qual é a sua música favorita?')
		ds.say("Qual sua banda preferida?")
		#answer = ds.getFromMic_Pt()#raw_input()
		answer = raw_input()
		userModel.addSearchQueue([answer], nome, 'musica favorita')

		preferences = userModel.getPreferences(nome)
	
	
	#CONDITION 1
	ds.say(" Vamos fazer uma série de atividades agora. Está preparado? Vamos lá")
	
	
	if play_drugs:
		drugs.play(nao, ds)
	
	try:
		ds.say(u'Sobre seu esporte preferido: \n{}'.format(
		    userModel.searchFile([preferences['esporte favorito'].encode('utf-8')])).encode('utf-8'))
		
		print (u'Sobre seu esporte preferido: \n{}'.format(
		    userModel.searchFile([preferences['esporte favorito'].encode('utf-8')])).encode('utf-8'))
		    
		
	except Exception as e:
		print(e)
	
	
	ds.say("Gostei, " + nome + ". Essse será meu esporte preferido também. O que você acha?")
	raw_input("GO!")
	ds.say("Certo. Vamos seguir com a atividade")
	
	
	
	if play_shelf:
		shelf.play(nao, ds)
	
	if play_ex:
		ex.play(nao, ds)
	
	try:
		ds.say(u'Sobre o rango que tu mais curte: \n{}'.format(
		    userModel.searchFile([preferences['comida favorita'].encode('utf-8')])).encode('utf-8'))
		print(u'Sobre o rango que tu mais curte: \n{}'.format(
		    userModel.searchFile([preferences['comida favorita'].encode('utf-8')])).encode('utf-8'))
		
	except Exception as e:
		print(e)

	ds.say("Eca. Que nojo. Você tem gostos peculiares. sorte minha que não como")
	raw_input("GO!")
	#ds.say("Certo. Vamos seguir com a interação")
	


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


	userModel.join()
	userModel.close()

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
	
	return 1	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

	'''
	ds.say("Estou certo? ")
	
	userAns = ds.getFromMic_Pt()
	
	if userAns == "sim":
		ds.say("Manjo muito")	
	
	else:
		ds.say("Vou melhorar")
	'''
	
	
	
	
	'''

	ds.say("Estou certo? ")
	
	userAns = ds.getFromMic_Pt()
	
	if userAns == "sim":
		ds.say("Manjo muito")	
	
	else:
		ds.say("Vou melhorar")
	

	#
	'''
	'''
	try:
		ds.say(u'Sobre seu esporte preferido: \n{}'.format(
		    userModel.searchFile([preferences['esporte favorito'].encode('utf-8')])).encode('utf-8'))
		ds.say(u'\nSobre sua comida preferida: \n{}'.format(
		    userModel.searchFile([preferences['comida favorita'].encode('utf-8')])).encode('utf-8'))
		ds.say(u'\nSobre sua música preferida: \n{}'.format(
		    userModel.searchFile([preferences['musica favorita'].encode('utf-8')])).encode('utf-8'))
	
	except Exception as e:
		print(e)

	ds.say("Sobre Seu esporte: " + userModel.searchFile([preferences['musica favorita']]).encode('utf-8') )
	'''
	
	
	
	
	


	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	return 1
	
	

	
	closeAttention = disattention.Th(2)
	closeAttention.start()

	


	return 1

	ds.say("Qual seu nome?")



	userModel = fileHelper.fileHelper()
	print(u'Olá abiguinhos')
	print(u'Qual é seu nome?')
	nome = raw_input()

	print(u'Qual é a sua idade?')
	answer = raw_input()
	userModel.addPreference(nome, answer, 'idade')

	#print(u'Qual é o seu esporte favorito?')
	ds.say("Qual seu esporte favorito")
	answer = raw_input()
	userModel.addSearchQueue([answer], nome, 'esporte favorito')

	#print(u'Qual é a sua comida favorita?')
	ds.say("Qual sua comida favorita?")
	answer = raw_input()
	userModel.addSearchQueue([answer], nome, 'comida favorita')

	#print(u'Qual é a sua música favorita?')
	ds.say("Qual sua banda preferida?")
	answer = raw_input()
	userModel.addSearchQueue([answer], nome, 'musica favorita')

	preferences = userModel.getPreferences(nome)



	# Activities Core
	
	
	
	#stories.paly(nao, ds)	

	jkp.play(nao, ds, 1)


	#emo.play()


	#exercises.play()

	#remedy.play()
	
	#shelf.play()

	userModel.join()

	try:
		print(u'Sobre seu esporte preferido: \n{}'.format(
		    userModel.searchFile([preferences['esporte favorito'].encode('utf-8')])).encode('utf-8'))
		print(u'\nSobre sua comida preferida: \n{}'.format(
		    userModel.searchFile([preferences['comida favorita'].encode('utf-8')])).encode('utf-8'))
		print(u'\nSobre sua música preferida: \n{}'.format(
		    userModel.searchFile([preferences['musica favorita'].encode('utf-8')])).encode('utf-8'))
	
	except Exception as e:
		print(e)

	ds.say("Sobre Seu esporte: " + userModel.searchFile([preferences['musica favorita']]).encode('utf-8') )

	userModel.close()



























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
	
	
	
	


	
