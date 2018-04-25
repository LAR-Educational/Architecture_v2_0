# coding=UTF-8


import vars 
import random
import distance
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy
#import speech2text as stt
import time
import pyaudio
import speech_recognition as sr
import time
from difflib import SequenceMatcher
import os



def open_file (file_name):
	with open(file_name) as f:
        	file_read = f.read().splitlines() 
        	f.close();
	return file_read 




class DialogSystem:

	def __init__(self, robot, path, language = "Brazilian"):
		self.robot=robot
		self.questions = open_file(os.path.join(path,'questions.txt'))
		self.answers = open_file(os.path.join(path,'answers.txt'))
		self.default_language = language
		self.setLang(self.default_language)
		# set the local configuration
		self.configuration = {"bodyLanguageMode":"contextual"}


	#funtion say
	def say(self, str2say, block=True, animated=True):
		""" Function to make the robot say (if connected) 
			str2say = string to say
			block = if the call will block next steps
		"""
		
		vars.nao_say(str2say)
		
		
		if animated:
			if block:
				self.robot.animatedSpeechProxy.say(str2say, self.configuration)
			else:
				self.robot.animatedSpeechProxy.post.say(str2say, self.configuration)
		
		else:
		
			if block:
				self.robot.tts.say(str2say)
			else:
				self.robot.tts.post.say(str2say)

		





	def setParameter(self, parameter, value):
	
		self.robot.tts.setParameter(parameter, value)

	
	
	def animated_say(self, str2say, block=True):
		
		""" Function to make the robot say (if connected) 
			str2say = string to say
			block = if the call will block next steps
		"""
		
		# say the text with the local configuration
		#animatedSpeechProxy.say("Hello, I am Nao", configuration)
		
		vars.nao_say(str2say)
		
		if block:
			self.robot.animatedSpeechProxy.say(str2say, configuration)
		else:
			self.robot.animatedSpeechProxy.post.say(str2say, configuration)

		  
		
	def setLang(self, lang):
		    if(vars.naoConeted):
		        self.robot.tts.setLanguage(lang)
		
		
		
	def load_from_file(self, filename):
		""" Fucntion to load a serie of dialog form file name """
		
		reader = open(filename,"r")
		ret = reader.read()
		reader.close()
		return ret
		
		
		
			



	def getFromMic(self):

		# obtain audio from the microphone
		r = sr.Recognizer()
		#f = open('string', 'w')

		st=""

		#while(not st):

		while st =="":
			with sr.Microphone() as source:
				self.say("ok. Ask Me.", block=True)
				r.adjust_for_ambient_noise(source)
				#r.dynamic_energy_adjustment_ratio = 5.0
				audio = r.listen(source)

			#print("Inside try")
			# recognize speech using Google Speech Recognition
			try:
				# for testing purposes, we're just using the default API key
				# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
				# instead of `r.recognize_google(audio)`
				self.say("I got you!. Let me think...")
				st = r.recognize_google(audio, language = "en-US").encode("utf8")
				#f.write(st)
				self.say("Good! ")
				print(st)
				
			except sr.UnknownValueError:
				self.say("I was not able to understand you. Could you repeat please?")
			except sr.RequestError as e:
				self.say("Could not request results from Google Speech Recognition service; {0}".format(e))

		return st
		
				



	def getFromMic_Pt(self):

		# obtain audio from the microphone
		r = sr.Recognizer()
		#f = open('string', 'w')

		st=""

		#while(not st):

		while st =="":
			with sr.Microphone() as source:
				r.adjust_for_ambient_noise(source)
				#self.say("Estou escutando.", block=True)
				#r.dynamic_energy_adjustment_ratio = 5.0
				audio = r.listen(source)

			#print("Inside try")
			# recognize speech using Google Speech Recognition
			try:
				# for testing purposes, we're just using the default API key
				# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
				# instead of `r.recognize_google(audio)`
				#self.say("Entendi.")
				st = r.recognize_google(audio, language = "pt-BR").encode("utf8")
				#f.write(st)
				self.say("Ok! ")
				
				print '\nRead sentence:', st
				#print(st)
				
			except sr.UnknownValueError:
				self.say("Não consegui entender o que você disse. Repita por favor")
			except sr.RequestError as e:
				self.say("Estou com um problema de conexão com a internet. Vou tentar de novo. ; {0}".format(e))

		return st
		
			
	# longest alignment
	def levenshtein_long(self, string_one, questions_list, print_flag=False):
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
		
		ans = frase, index			
		return ans	  



	#comparing_string = raw_input("Digite a a frase a ser comparada com as questoes no arquivo\n")
	def quiz(self):
		while True:
			start = time.time()    
			comparing_string = self.getFromMic()
			#comparing_string = raw_input("Digite a a frase a ser comparada com as questoes no arquivo\n")
			end = time.time()
		
			t1 = end-start
		
			print "Time to collect audio from mic:", t1, "\n\n"
		
			if comparing_string == 'exit':
				self.say("See you next time. Bye bye.")
				break
		
			#start = time.time()
			
			
			answer = self.levenshtein_long(comparing_string, self.questions )
			#end = time.time()
			print answer
			print "Read sentence: ", comparing_string
			print "Question: ", answer[0]
			self.say(self.answers[answer[1]])
			t2 = end-start
		
			print '\n\n'
			print "\n\nTime to calculate distance:", t2, "\n\n"
		
		try:
			print "The End! Total time: ", t1+t2, "seconds."
		except:
			print "Exit before t2 vriable being assigned"
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	'''	
	def repeat():
		rd=random.randint(0,2)
		
		if(rd==0):
		    return "Será que você já sabe qual animal que é? Ou se você quiser eu posso repetir a estoria. Você gostaria que eu repetisse?"
		    
		elif(rd==1):
		    return "Se ficou confuso eu posso repetir pra você. Quer que eu repita?"
		    
		else:
		    return "Essa foi fácil. Mas posso repetir pra você. Voce quer?"
	   

	   
	def sound():
		rd=random.randint(0,2)
		
		if(rd==0):
		    return "Escute o som que emite esse animal"
		    
		elif(rd==1):
		    return "Esse animal faz assim"
		    
		else:
		    return "O som dele é mais ou menos isso"
	'''		         
