#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import csv
import unicodedata
from dialog_components import searchWiki
from dialog_components import database
from textblob import TextBlob
from translate import Translator




def readFile(fileName):
	with open(fileName) as f:
		content = f.read().splitlines()
	
	f.close()
	return content

def numberWords(sentence):
	print("Calculating number of words")
	return len(sentence.split())	


def isQuestion(sentence):	
	for x in range(0, len(temp_list_question)):
		found = re.findall('\\b' + temp_list_question[x] + '\\b', sentence, flags=re.IGNORECASE)
		if (len(found) > 0):
			print("Matches: " + str(found))
			return True
			break

			
	return False


def isNegative(sentence):	
	for x in range(0, len(temp_list_negative)):
		found = re.findall('\\b' + temp_list_negative[x] + '\\b', sentence, flags=re.IGNORECASE)
		if (len(found) > 0):
			print("Matches: " + str(found))
			return True
			break

			
	return False


def isPositive(sentence):	
	for x in range(0, len(temp_list_positive)):
		found = re.findall('\\b' + temp_list_positive[x] + '\\b', sentence, flags=re.IGNORECASE)
		if (len(found) > 0):
			print("Matches: " + str(found))
			return True
			break

			
	return False


def isPositive(sentence):	
	for x in range(0, len(temp_list_positive)):
		found = re.findall('\\b' + temp_list_positive[x] + '\\b', sentence, flags=re.IGNORECASE)
		if (len(found) > 0):
			print("Matches: " + str(found))
			return True
			break

			
	return False


def findNoun(sentence):
	result = []
	flag = False
	phrase = sentence.split(" ")
	for x in range(0, len(phrase)):
		flag = False
		for y in range(0, len(temp_list_noun)):
			if(temp_list_noun[y] == phrase[x]):
				flag = True
		
		if(flag == False):
			result.append(phrase[x])	

	return result


def creat_Dict_stopWord(filtred_words):
	translate_dict = {}

	for x in range(0, len(filtred_words)):
		word = TextBlob(filtred_words[x])
		try:
			translate_dict[filtred_words[x]] = word.translate(to='en').tags
		except:
			aux = TextBlob(filtred_words[x])
			translate_dict[filtred_words[x]] = aux.tags

	return translate_dict

def find_Nouns_stopWord(dictc, filtred_words):
	touple_List = []
	result = []
	for word in filtred_words:
		touple_List.append(dictc[word])

	
	for x in touple_List:
		if x[0][1] == "NNS" or x[0][1] == "NN":
			result.append(x[0][0])   			
   			 	
   	return result


def creat_Dict(sentence):
	splitted_sentence = sentence.split()
	translate_dict = {}

	for x in range(0, len(splitted_sentence)):
		word = TextBlob(splitted_sentence[x])
		try:
			translate_dict[splitted_sentence[x]] = word.translate(to='en').tags
		except:
			aux = TextBlob(splitted_sentence[x])
			translate_dict[splitted_sentence[x]] = aux.tags

	return translate_dict

def find_Nouns(dictc, sentence):
	split = sentence.split()
	touple_List = []
	result = []
	for word in split:
		touple_List.append(dictc[word])

	
	for x in touple_List:
		if x[0][1] == "NNS" or x[0][1] == "NN":
			result.append(x[0][0])   			
   			 	
   	return result

def csv_Getter(name):
	with open('teste.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		result =[]
		for row in reader:
			result.append(row[name])

	return result


def match(result, sentence):
	match = [] 
	for x in range(0, len(result)):
		found = (re.findall('\\b' + result[x] + '\\b', sentence, flags=re.IGNORECASE))
		if (len(found) > 0):
			match.append(found[0])
		#print(match)
		#print(len(match))
	if len(match) > 2:
		return len(match)
	return len(match)






"""
A remoção de acentos foi baseada em uma resposta no Stack Overflow.
http://stackoverflow.com/a/517974/3464573
"""

def removerAcentosECaracteresEspeciais(palavra):

    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)

def tagger(sentence):
	list_tagger = ["voce", "seu", "sua"]
	for x in range(0, len(list_tagger)):
		found = re.findall('\\b' + list_tagger[x] + '\\b', sentence, flags=re.IGNORECASE)
		if (len(found) > 0):
			#print(string)
			return True
			break



	# Identifica o perguntas afirmações e duvidas 
print("Loading data base from files...")
	
temp_list_question = readFile("doubt.txt")
temp_list_negative = readFile("negation.txt")
temp_list_positive = readFile("afirmation.txt")
temp_list_noun  = readFile("noun.txt")
f = database.File()
print("Data base loaded!\n")
	 

sentence = raw_input("Receving sentence from NAO:")
input_copy = sentence
sentence = sentence.lower()
#print(sentence)

print("\nProcessing Sentece\n")


encoding = "utf-8" # or iso-8859-15, or cp1252, or whatever encoding you use
byte_string = sentence  # or simply "café" before python 3.
unicode_string = byte_string.decode(encoding)

awnser = removerAcentosECaracteresEspeciais(unicode_string)
sentence = awnser.encode(encoding)
#print(sentence)


translator = Translator(from_lang = "pt", to_lang = "en")
translation = translator.translate("Vamos ver se vai agora essa desçraca filha da puta")

print(translation)



s = numberWords(sentence)
print("Number of words: " + str(s))
print("\n")

print("Checking for doubts...")
d = isQuestion(sentence)
print("Doubt found: " + str(d))
print("\n")

if d == False:
	print("Checking for negation...")
	d = isNegative(sentence)
	print("Negation found: " + str(d))
	print("\n")

if d == False:
	print("Checking for afirmation...")
	d = isPositive(sentence)
	print("Afirmation found: " + str(d))


print("Stopwords filter:")
print(findNoun(sentence))
print "\n"

print("Just translate:")

dictc =  creat_Dict(sentence)
result = find_Nouns(dictc, sentence)
print(result)
print "\n"

print("All:")

filtred_words = findNoun(sentence)
dictc =  creat_Dict_stopWord(filtred_words) 
result = find_Nouns_stopWord(dictc, filtred_words)
print(dictc)

x = 0
all_nouns = []

while(x < len(result)):
	for key, value in dictc.iteritems():
		if value[0][0] == result[x]:
			 all_nouns.append(key)
	x = (x + 1)
print(all_nouns)	
print "\n"

if (len(all_nouns) > 1):
	print ("Encontrei mais de uma palavra que pode ser pesquisada")

elif(tagger(sentence) == True):
	tagged = all_nouns[0]
	tagged = "_" + tagged
	print(searchWiki.searchWiki(f, tagged))
else:
	wiki_awnser = searchWiki.searchWiki(f, all_nouns[0])
	#print(wiki_awnser)

	a = csv_Getter(all_nouns[0])
	if (match(a, wiki_awnser) >= 3):
		print(wiki_awnser)
	else:
		print(match(a, wiki_awnser))
		print("Too Bad!")