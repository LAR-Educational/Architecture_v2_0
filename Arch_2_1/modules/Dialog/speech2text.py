# -*- coding: utf-8 -*-
#!/usr/bin/env python3


# NOTE: this example requires PyAudio because it uses the Microphone class
import pyaudio
import speech_recognition as sr
import time
from difflib import SequenceMatcher


def getFromMic():

	# obtain audio from the microphone
	r = sr.Recognizer()
	#f = open('string', 'w')

	st=""

	#while(not st):

	while st =="":
		with sr.Microphone() as source:
		    r.adjust_for_ambient_noise(source)
		    print("Ok. Ask Me.")
		    #r.dynamic_energy_adjustment_ratio = 5.0
		    audio = r.listen(source)

		#print("Inside try")
		# recognize speech using Google Speech Recognition
		try:
		    # for testing purposes, we're just using the default API key
		    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		    # instead of `r.recognize_google(audio)`
		    print("I got you!. Let me think...")
		    st = r.recognize_google(audio, language = "en-US").encode("utf8")
		    #f.write(st)
		    print("Good! ")
		    print(st)
		    
		except sr.UnknownValueError:
		    print("I was not able to understand you. Could you repeat please?")
		except sr.RequestError as e:
		    print("Could not request results from Google Speech Recognition service; {0}".format(e))

	return st
		
				



def getFromMic_Pt():

	# obtain audio from the microphone
	r = sr.Recognizer()
	#f = open('string', 'w')

	st=""

	#while(not st):

	while st =="":
		with sr.Microphone() as source:
		    r.adjust_for_ambient_noise(source)
		    print("Estou escutando.")
		    #r.dynamic_energy_adjustment_ratio = 5.0
		    audio = r.listen(source)

		#print("Inside try")
		# recognize speech using Google Speech Recognition
		try:
		    # for testing purposes, we're just using the default API key
		    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		    # instead of `r.recognize_google(audio)`
		    print("Entendi.")
		    st = r.recognize_google(audio, language = "pt-BR").encode("utf8")
		    #f.write(st)
		    print("Ok! ")
		    
		    print '\n\nRead sentence:'
		    print(st)
		    
		except sr.UnknownValueError:
		    print("Não consegui entender o que você disse Poderia repeditr assim que eu estiver escutando novamente?")
		except sr.RequestError as e:
		    print("Estou com um problema de conexão com a internet. Vou tentar de novo. ; {0}".format(e))

	return st
		
				









				
				
