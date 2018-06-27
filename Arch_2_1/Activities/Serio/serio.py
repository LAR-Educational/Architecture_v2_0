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

t_start = time.time()
t_last_intervention = t_start

while(True):
			
	if(time.time() - t_start > 30): 
		robot.tss.say("Ra,Ra,Ra,Ra. Parabéns. Você Venceu")
		break

	if(len(deviation_times) > 2 or emotions['happy'] > 2)
		robot.tss.say("Eba. Eu venci")
		break
	
	if(time.time() - t_last_intervention > 8):
		robot.tts.say(frase_dict[r[i]])
		i = i+1
		t_last_intervention = time.time()


print(emotions)
print(deviation_times)

closeAttention = disattention.Th(2)
closeAttention.start()





















