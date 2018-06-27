# -*- coding: utf-8 -*-
import naoqi
import time, random
import numpy as np
from Modules import dialog, disattention
from Modules.vars import Robot, robotIp, port, emotions, deviation_times

robot = Robot(robotIp, port)

attention = disattention.Th(1)
attention.start()


robot.tts.setLanguage("Brazilian")

with open('Activities/Serio/frases.txt', 'r') as arq:
	frases = arq.read().split('\n')
	frases = frases[:7]

frase_dict = {}
for i, frase in enumerate(frases):
	frase_dict[i] = frase

r = random.sample(range(7), 3)

robot.tts.say("O jogo do sério é uma brincadeira onde eu e você iremos ficar sérios. Quem rir primeiro ou olhar para o lado perde. Chegue mais perto para que eu possa te ver. Vamos começar!")


while(deviation_times.size()<2):
			
	if()
for i in range(3):
	robot.tts.say(frase_dict[r[i]])

lost = False



print(emotions)
print(deviation_times)

closeAttention = disattention.Th(2)
closeAttention.start()





















