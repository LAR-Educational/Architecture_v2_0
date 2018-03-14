#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class
#import pyaudio
#import speech_recognition as sr
import time
from difflib import SequenceMatcher

'''
def enigmas():

    # obtain audio from the microphone
    r = sr.Recognizer()
    f = open('string', 'w')

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
'''


questions_all = []
questions = []
answers = []

with open('all_questions.textile') as f:
    questions_all = f.read().splitlines() 

with open('questions.textile') as f:
    questions = f.read().splitlines() 

with open('awnsers.textile') as f:
    awnsers = f.read().splitlines()


print questions_all    
print questions    
print awnsers    

 #print st.lower()
 #print q
'''
for i in range(len(questions)):
    #print "searching in " + q
    if questions[i] in st.lower():
        print "FOUND IT!"
        print answers[i]
        return True
    
print "I was not able to answer this question. Sorry, can we try again?"    
return False    


#def main():

for att in range(0,3):
    if enigmas():
        break
    
    
print "Sorry. No answer right in the three attempts."  
'''