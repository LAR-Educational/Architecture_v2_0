#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wikipedia
import re
import database
import warnings

warnings.simplefilter("ignore", UserWarning)

debug = True

# Pesquisa a página mais próxima de query da wikipedia e procura a seção query, se não achado devolver o resumo.
def searchWiki(file, query, section='', sentences = 0):
	if query is '':
		info("Invalid string.", 3)

		return 'Por favor coloque algo para pesquisar.'

	DEFAULT_ANSWER = "Me desculpe amiguinho, mas não consigo te reponder isso."

	info("Searching for query in memory...")
	
	ret = file.search(query+section)

	if ret:
		info("Query found.")

		return ret
	else:
		if(query[0] == '_'):
			info("Personal query not found.")
			info("Please add answer afterwards.", 1)

			file.SaveQuery(query)
			return DEFAULT_ANSWER
	info("Query not found.")

	# Coloca a linguagem da wikipedia em português
	wikipedia.set_lang("pt")
	
	info("Searching web...")

	# Pega a página e as seções da página
	try:
		page = wikipedia.page(query)
		ret = wikipedia.summary(query, sentences=sentences)
	except:
		info("Ambiguous query.", 1)

		nquery = wikipedia.search(query, 2)[1]
		page = wikipedia.page(nquery)
		ret = wikipedia.summary(nquery, sentences=sentences)

	sections = page.sections
	found = None

	info("Searching sections...")

	# Procura a seção requesitada
	for sec in sections:
		if(sec.lower() == section.lower()):
			ret = page.section(sec)
			found = True
			break

	info("Parsing...")

	# Retira todos as partes que estão entre chaves de dentro para fora.
	while re.search('\{[^{}]*\}', ret):
		ret = re.sub('\{[^{}]*\}', '', ret)

	# Retira os espaços extras.
	ret = re.sub('\s{2,}|[\t\n\r\f\v]', ' ', ret)
	
	if(found):
		# Separa as sentenças que foram requisitado.
		temp = ret
		ret = ''
		for i in range(sentences):
			m = re.findall("([^.]*).(.*)", temp)
			if(len(m[0]) == 2):
				ret += m[0][0] + '.'
				temp = m[0][1]
			elif(len(m[0]) == 1):
				ret += m[0][0] + '.'
			else:
				break

	file.write(query+section, ret)

	return ret

class bcolors:
	RED   = "\033[1;31m"  
	BLUE  = "\033[1;34m"
	CYAN  = "\033[1;36m"
	GREEN = "\033[0;32m"
	HEADER = '\033[0;95m'
	WARNING = '\033[1;93m'
	FAIL = '\033[1;91m'
	ENDC = '\033[;0m'
	BOLD = '\033[;1m'
	UNDERLINE = '\033[;4m'
	REVERSE = "\033[;7m"

def info(stringToPrint, tag=0):
	if debug:
		if(tag == 0):
			print(bcolors.BOLD + "[INFO] " + bcolors.ENDC + stringToPrint)
		elif(tag == 1):
			print(bcolors.WARNING + "[WARNING] " + bcolors.ENDC + stringToPrint)
		elif(tag == 2):
			print(bcolors.BLUE + "[EXCEPTION] " + bcolors.ENDC + stringToPrint)
		elif(tag == 3):
			print(bcolors.FAIL + "[ERROR] " + bcolors.ENDC + stringToPrint)

f = database.File()
print(searchWiki(f, "", sentences=1))