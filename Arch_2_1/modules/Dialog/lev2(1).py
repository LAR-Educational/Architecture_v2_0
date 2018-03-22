import distance
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy

class Anwser(object):
	frase = ""
	index = -1
	score = -1

	def __init__(self, frase, index, score):
		self.frase = frase
    	#self.index = index
    	#self.score = score



def make_Anwser(frase, index):
	anwser = Anwser(frase, index)
	return anwser

def open_file ():
	with open('all_questions.textfile') as f:
        	questions_all = f.read().splitlines() 
        	f.close();
	return questions_all

# shortest alignment
def levenshtein_short(string_one, all_questions):
	bigger = -1
	anwser = ""
	for element in all_questions:
		compare = distance.nlevenshtein(string_one, element , method=1)
		#Esses prints sao para verificar a similidarida entre todas as palavras da lista
		#caso nao haja interesse pode ser apagado
		print "Score: " + str(distance.levenshtein(string_one, element))
		print "Normalizado: " + str(compare)
		print "Sentence: " + element + "\n"
		if compare > bigger:
			bigger = compare
			awnser = element
			#
	return awnser	  						
		
# longest alignment
def levenshtein_long(string_one, all_questions):
	bigger = -1
	anwser = ""
	for element in all_questions:
		#Esses prints sao para que possa verificar a similidarida entre todas as palavras da lista
		#caso nao haja interesse pode ser apagado
		compare = distance.nlevenshtein(string_one, element, method=2)
		print "Score: " + str(distance.levenshtein(string_one, element))
		print "Normalizado: " + str(compare) 
		print "Sentence: " + element + "\n"
		if compare > bigger:
			bigger = compare
			awnser = element
	return awnser	  




all_questions = open_file()
comparing_string = raw_input("Digite a a frase a ser comparada com as questoes no arquivo\n")

awnser = levenshtein_long(comparing_string, all_questions)
print "\nFinal awnser: " + awnser

