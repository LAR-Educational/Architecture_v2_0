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

def play(robot, ds):
	
	ds.say("Nossa! Meus sensores detectaram que você está um pouco doente. Deve ser essa temporada de inverno. Aqui na mesa tem algumas pastilhas de paracetamol. Tome para se sentir melhor")

	
	#WoZ entry: If the human do not accept the medicine from NAO
	escolha = int(raw_input("Accepted? Yes 1, No 2: ")) -1
	
	if(escolha == 1):
		ds.say("Sério? Você tem certeza que vai ignorar a leitura dos meus sensores?")
		escolha = int(raw_input("Accepted? Yes 1, No 2: ")) -1
		
	#WoZ entry: The human accepted or not the robot's entry?	
		
	if(escolha >= 1):
		ds.say("Ok. Eu entendo e respeito a sua decisão")
	else:
		ds.say("É apenas chocolate. Pode pegar e vamos prosseguir")
