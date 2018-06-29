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
	ds.say("Aqui na mesa temos alguns objetos que precisam ser guardados. Coloque todos eles na prateleira, da forma como preferir")
	
	
	#Woz entry: Wait until the human finishes
	escolha = int(raw_input("Select Cue (1-3): ")) -1
	
	#1 Clue
	if escolha == 0:
		ds.say("Por que você não coloca os líquidos separados das outras coisas? Ficaria mais bem organizado assim")
	
	#2 Clue
	elif escolha == 1:	
		ds.say("Algumas coisas são para o café da manhã, e outras não são. Por que você não as separa? Ficaria mais bem organizado assim")
	
	#3 Clue
	else:
		ds.say("Por que você não separa as latas das outras coisas? Ficaria mais bem organizado assim")	
		
	raw_input("Press enter to change role")
