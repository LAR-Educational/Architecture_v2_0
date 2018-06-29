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


def display_exercise(robot, exercise):
	print "Exercice:", exercise
	
	exercise_list = ['exercicio1-834e8c', 'exercicio2-d0939e', 'exercicio3-fb73bb', 'exercicio4-8b3442']
	
	robot.behavior.runBehavior(exercise_list[exercise]+"/behavior_1")
	pass

		
def play(robot, ds):
	ds.say("Vamos dar uma pausa para nos alongarmos um pouco")
	robot.behavior.runBehavior('wsafe-c66573/behavior_1')
	
	#Exercise 1
	ds.say("Vamos alongar os braços, levando-os para cima. Preste atenção, estou mostrando como você deve fazer", block=False)
	display_exercise(robot, 0)
	robot.behavior.runBehavior('wsafe-c66573/behavior_1')
	
	#Exercise 2
	ds.say("Agora vamos levar os braços para trás. Conforme você está vendo no exemplo", block=False)
	display_exercise(robot, 1)
	robot.behavior.runBehavior('wsafe-c66573/behavior_1')
	
	#Exercise 3
	ds.say("Para finalizar, vamos puxar o braço atrás da cabeça. Veja como é fácil", block=False)
	display_exercise(robot, 2)
	robot.behavior.runBehavior('wsafe-c66573/behavior_1')
	
	#Exercise 4
	ds.say("Agora vamos inverter os braços, para ficar os dois alongados por igual", block=False)
	display_exercise(robot, 3)
	robot.behavior.runBehavior('wsafe-c66573/behavior_1')
	
	#Ending
	ds.say("Creio que já estamos suficientemente alongados. Agora quero fazer outra coisa")
		
