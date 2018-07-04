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

play_book = ["pedra","papel","tesoura"]

behaviors = ["PedraAberto","PedraFechado", "PapelAberto","PapelFechado", "TesouraAberto","TesouraFechado" ]

mapped_behaviors = ['pedraaberto-98d60e', 'pedrafechado-3c68ba',  'papelaberto-ed3da0', 'papelfechado-c5cd99', 'tesouraaberto-723122', 'tesourafechado-167e3d']  

			
def jokenpo(primeira_jogada,segunda_jogada):

		
	ganhador = ''
	perdedor = ''
	result = ''

	if primeira_jogada == segunda_jogada:
		result = 0
		ganhador = primeira_jogada
		perdedor = primeira_jogada
	
	'''
	ganha_de = {
	'pedra': 'tesoura',
	'tesoura': 'papel',
	'papel': 'pedra',
	}

	if ganha_de[primeira_jogada] == segunda_jogada:
		ganhador = primeira_jogada
		perdedor = segunda_jogada
	else:
		ganhador = segunda_jogada
		perdedor = primeira_jogada
		

	  
	'''
	
	if primeira_jogada == 'pedra' and segunda_jogada == 'tesoura':
		ganhador = 'pedra'
		perdedor = 'tesoura'
		result = 1
		
	if primeira_jogada == 'tesoura' and segunda_jogada == 'pedra':
		ganhador = 'pedra'
		perdedor = 'tesoura'
		result = -1
		
	if primeira_jogada == 'tesoura' and segunda_jogada == 'papel':
		ganhador = 'tesoura'
		perdedor = 'papel'
		result = 1
		
	if primeira_jogada == 'papel' and segunda_jogada == 'tesoura':
		ganhador = 'tesoura'
		perdedor = 'papel'
		result = -1
		
	if primeira_jogada == 'papel' and segunda_jogada == 'pedra':
		ganhador = 'papel'
		perdedor = 'pedra'
		result = 1
		
		
	if primeira_jogada == 'pedra' and segunda_jogada == 'papel':
		ganhador = 'papel'
		perdedor = 'pedra'
		result = -1
	
	return result, ganhador, perdedor		





def play(robot, ds,round_numbers=3):
	
	
	'''
	info("Starting program ")            

	info("Connecting with NAO")
	nao = False

	try:
		#core.initializer();
	 	nao=core.Robot(core.teddy_ip, core.port)   
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
	'''



	##-------- Real Play
	player_robot = 0
	player_human = 0

	for turn in range(0,round_numbers):
			
			

		
		#time.sleep(15)
		#pass
		#print(core.emotions)
		ds.say("Rodada número " + str(turn+1))

		behave = np.random.randint(0,6)
	
		print "Behave", behave
	
		p1 = int(behave/2)
		#p2 = np.random.randint(0,2)


		
		
		robot_move = play_book[p1]
		
		#ds.say("Eu escolho " +  play_book[p1])
		
		#-- Generic function to execute jokenpo play
		execute_move(robot, behave)
		
		'''
		ds.say("Jó", animated = False, block=False)
		time.sleep(3)
		
		ds.say("quem", animated = False, block=False)
		time.sleep(3)
		
		ds.say("Pô", animated = False, block=False)
		#time.sleep(1)
		'''
		
		p2 = int(raw_input("Player play (1-3): ")) -1
		print "p1: " , play_book[p1]
		print "p2: ", play_book[p2]
		print "behave", behaviors[behave]
	
		play,w,l = jokenpo(play_book[p1],play_book[p2])
	
		#play=[a,b,c]
		
		#ds.say("")
		
		
		
		ds.say(" eu escolhi " +  play_book[p1] + " e você escolheu " + play_book[p2])
	
		print "result: ", play

		if play > 0:
			ds.say("Eu ganhei porque" +  w + " ganha de " + l)
			#print "Robô ganhou porque ", w ," ganha de ", l	
			player_robot+=1
		elif play < 0:	
			ds.say("Você ganhou porque" +  w + " ganha de " + l)
			#print "Player ganhou porque ", w ," ganha de ", l
			player_human+=1
		else:
			ds.say("Empatou porque escolhemos a mesma coisa")
			#print "empate porque ", w ," e ", l, "são iguais"


		print
		print
		
		#raw_input("Pause") 
	
	if player_robot > player_human:
		ds.say("Rá! Parece que eu ganhei, hein. Robôs Dominam!")
	
	elif player_robot < player_human:
		ds.say("é. Acho que os robôs estão longe de ganhar dessa sua racinha.")
	
	else:
		ds.say("Nem pra mim nem pra você. Empatamos no geral")



def execute_move(robot, chosen_behavior):
	'''
	Replace this function to use LARA's resoucers
	'''
	
	
	print "running behavior: ", behaviors[chosen_behavior] 
	robot.behavior.runBehavior(mapped_behaviors[chosen_behavior]+"/behavior_1")
	
			



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

