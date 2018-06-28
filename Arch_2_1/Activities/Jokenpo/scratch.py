
# -*- coding: utf-8 -*-
import naoqi
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

	for turn in range(0,5):
		#pass

		print "Rodada numero ", turn

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
		
if __name__=="__main__":
	main()	
	
	












