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



	
	
	#stories.paly(nao, ds)	

	jkp.play(nao, ds, 3)

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
	
	
	
	


	
