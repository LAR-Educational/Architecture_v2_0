# -*- coding: utf-8 -*-
import naoqi
import time
from Modules import dialog
from Modules import vars as core
from Modules import disattention

# ----- System imports -----

import sys
import time
import cv2
import csv
import os
import random
import numpy as np






def display_emotion(robot, emotion):
	
	print "Emotion:", emotion
	
	behaviors_list = ['alegria-ddf47b', 'triste-6cf5ae', 'raiva-728b93', 'nojo-53170f', 'surpresa-5d36f6', 'medo-7a3069']
	
	robot.behavior.runBehavior(behaviors_list[emotion]+"/behavior_1")
	pass




def play(robot, ds, att):
	
	
	emotions_list = ['Alegria', 'Triste', 'Raiva', 'Nojo',
 	'Surpresa', 'Medo', 'Neutral']
		

	#nao pede emoções
	
	#rand_emo = random.randint(0,6)

	#ds.say("Agora vou te mostrar minhas habilidades como ator. Mostre uma expressão entre Alegria, Tristeza, Raiva, Nojo, Surpresa ou Medo que eu vou imitar
	
	ds.say("inicio") 		
	
	for i in range(0,2):
		
		att._continue()
		#print(core.emotions)
		
		#print "Faça para mim a expressão facial de" , emotions_list[i]
		#print "Agora vou te mostrar minhas habilidades como ator. Mostre uma expressão entre Alegria, Tristeza, Raiva, Nojo, Surpresa ou Medo que eu vou imitar"
		
		#Reconhecimento de emoções
		# Intervalo de tempo I, escolhe a emoção amis detectada 
		time.sleep(4)
		att._halt()
		
		print "Mais detectada",  max(core.emotions, key=core.emotions.get)
		
		#ds.say("A expressão que eu detectei foi, " + max(core.emotions, key=core.emotions.get))
		
		ds.say("Ok, detectei uma emoção. Veja se descobre qual é")
		
		print core.emotions
	
		
		
		
		core.clear_emo_variables()
		
		#print "Emo:", emotions_list[i]
		#print core.emotions
	
	#pessoa adivinha emoções do nao
	
	#for i in range(0,6):
		
		#display_emotion(robot, max(core.emotions, key=core.emotions.get))
		
	#	display_emotion(robot, i)
	



















