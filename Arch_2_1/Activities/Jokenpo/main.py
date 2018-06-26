# -*- coding: utf-8 -*-
import naoqi
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




def main():
	
	
	
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




	##-------- Real Play

	for turn in range(0,5):
			
			attention = disattention.Th(1)
			attention.start()
	
			#pass

			print "Rodada numero ", turn+1

			behave = np.random.randint(0,5)
		
			print "Behave", behave
		
			p1 = int(behave/2)
			p2 = np.random.randint(0,2)
	
			print "p1: ", play_book[p1]
			print "p2: ", play_book[p2]
			print "behave", behaviors[behave]
		
	
			play,w,l = jokenpo(play_book[p1],play_book[p2])
		
			#play=[a,b,c]
		
		
			print "result: ", play
	
			if play > 0:
				print "Player 1 ganhou porque ", w ," ganha de ", l	
	
			elif play < 0:	
				print "Player 2 ganhou porque ", w ," ganha de ", l
		
			else:
				print "empate porque ", w ," e ", l, "são iguais"


			print
			print
			
			raw_input("Pause") 
		
			closeAttention = disattention.Th(2)
			closeAttention.start()

















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

