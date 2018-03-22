# -*- coding: utf-8 -*-

import distance
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy
import speech2text as stt
import time

class Answer:#(object):
	frase = ""
	index = -1
	#score = -1

	def __init__(self, frase, index):
		self.frase = frase
		self.index = index



def open_file (file_name):
	with open(file_name) as f:
        	file_read = f.read().splitlines() 
        	f.close();
	return file_read 

# shortest alignment
'''def levenshtein_short(string_one, all_questions):
	bigger = -1
	answer = ""
	i=
	for element in all_questions:
		compare = distance.nlevenshtein(string_one, element.lower() , method=1)
		#Esses prints sao para verificar a similidarida entre todas as palavras da lista
		#caso nao haja interesse pode ser apagado
		print "Score: " + str(distance.levenshtein(string_one, element))
		print "Normalizado: " + str(compare)
		print "Sentence: " + element + "\n"
		if compare > bigger:
			bigger = compare
			answer = element
			#
	return answer	  						
'''


		
# longest alignment
def levenshtein_long(string_one, questions_list, print_flag=False):
	bigger = 1
	frase = ""
	index = -1
	i=0
	for element in questions_list:
		
		compare = distance.nlevenshtein(string_one, element.lower(), method=2)
		#print "Score: " + str(distance.levenshtein(string_one, element))
		
		if print_flag:
			print "Normalizado: " + str(compare) 
			print "Sentence: " + element 
			print "Index number: ", i , "\n"
		
		if compare < bigger:
			bigger = compare
			frase = element
			index = i
		i+=1
		
	ans = Answer(frase, index)			
	return ans	  




all_questions = open_file('all_questions.textfile')
answers = open_file('answer_file')

#comparing_string = raw_input("Digite a a frase a ser comparada com as questoes no arquivo\n")

while True:
    start = time.time()    
    comparing_string = stt.getFromMic()
    #comparing_string = raw_input("Digite a a frase a ser comparada com as questoes no arquivo\n")
    end = time.time()
    
    t1 = end-start
    
    print "Time to collect audio from mic:", t1, "\n\n"
    
    if comparing_string == 'exit':
        break
    
    start = time.time()    
    answer = levenshtein_long(comparing_string, all_questions)
    end = time.time()
    
    print "Read sentence: ", comparing_string
    print "Question: ", answer.frase
    print "Answer: ", answers[answer.index]
    t2 = end-start
    
    print '\n\n'
    #print "\n\nTime to calculate distance:", t2, "\n\n"
    
    
print "The End! Total time: ", t1+t2, "seconds."


