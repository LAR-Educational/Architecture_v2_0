#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wikipedia
import re
import database
import settings
import warnings

warnings.simplefilter("ignore", UserWarning)

# Pesquisa a página mais próxima de query da wikipedia e procura a seção query, se não achado devolver o resumo.
def searchWiki(file, query, section='', sentences = 0):
	if query is '':
		settings.info("Invalid string.", 3)

		return 'Por favor coloque algo para pesquisar.'

	DEFAULT_ANSWER = "Me desculpe amiguinho, mas não consigo te reponder isso."

	settings.info("Searching for query in memory...")
	
	ret = file.search(query+section)

	if ret:
		settings.info("Query found.")

		return ret
	else:
		if(query[0] == '_'):
			settings.info("Personal query not found.")
			settings.info("Please add answer afterwards.", 1)

			file.SaveQuery(query)
			return DEFAULT_ANSWER
	settings.info("Query not found.")

	# Coloca a linguagem da wikipedia em português
	wikipedia.set_lang("pt")
	
	settings.info("Searching web...")

	# Pega a página e as seções da página
	try:
		page = wikipedia.page(query)
		ret = wikipedia.summary(query, sentences=sentences)
	except:
		settings.info("Ambiguous query.", 1)

		nquery = wikipedia.search(query, 2)[1]
		page = wikipedia.page(nquery)
		ret = wikipedia.summary(nquery, sentences=sentences)

	sections = page.sections
	found = None

	settings.info("Searching sections...")

	# Procura a seção requesitada
	for sec in sections:
		if(sec.lower() == section.lower()):
			ret = page.section(sec)
			found = True
			break

	settings.info("Parsing...")

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