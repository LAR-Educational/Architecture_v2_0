# -*- coding: utf-8 -*-
import naoqi
import time, random
import numpy as np
from Modules import dialog, disattention
from Modules.vars import Robot, robotIp, port, emotions, deviation_times

robot = Robot(robotIp, port)

attention = disattention.Th(1)
attention.run()

animatedSpeech = naoqi.ALProxy("ALAnimatedSpeech", ip, port)
speech = naoqi.ALProxy("ALTextToSpeech", ip, port)
speech.setLanguage("Brazilian")

with open('Activities/Serio/frases.txt', 'r') as arq:
	frases = arq.read().split('\n')
	frases = frases[:7]

frase_dict = {}
for i, frase in enumerate(frases):
	frase_dict[i] = frase

r = random.sample(range(7), 3)
print("aqui")
speech.say("O jogo do sério é uma brincadeira onde eu e você iremos ficar sérios. Quem rir primeiro ou olhar para o lado perde. Chegue mais perto para que eu possa te ver. Vamos começar!")

intial_time = time.time()

while True:
	if(initial_time - time.time() < 7):
		animatedSpeech.say(frase_dict[r[0]])
	elif(initial_time - time.time() < 20):
		animatedSpeech.say(frase_dict[r[1]])
	elif(initial_time - time.time() < 30):	
		animatedSpeech.say(frase_dict[r[2]])
	elif(initial_time - time.time() < 40):
		break


print(emotions)
print(deviations)

closeAttention = disattention.Th(2)
closeAttention.run()





















