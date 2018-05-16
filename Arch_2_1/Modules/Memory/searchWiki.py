#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wikipedia
import re
import memory
import warnings

warnings.simplefilter("ignore", UserWarning)

def joinQuery(query):
	newquery = ''
	for x in query:
		newquery += x + ' '
	newquery = newquery[:-1]

	return newquery

# Pesquisa a página mais próxima de query da wikipedia e procura a seção query, se não achado devolver o resumo.
def searchWiki(file, query, section='', sentences = 0):
	query = joinQuery(query)

	try:
		query = query.decode('utf-8')
		section = section.decode('utf-8')
	except:
		pass

	if query is '':
		return 'Por favor coloque algo para pesquisar.'

	DEFAULT_ANSWER = "Me desculpe amiguinho, mas não consigo te reponder isso."
	
	ret = file.search(query+section)

	if ret:
		return ret
	else:
		if(query[0] == '_'):
			file.SaveQuery(query)
			return DEFAULT_ANSWER

	# Coloca a linguagem da wikipedia em português
	wikipedia.set_lang("pt")

	# Pega a página e as seções da página
	try:
		page = wikipedia.page(query)
		ret = wikipedia.summary(query, sentences=sentences)
	except:
		nquery = wikipedia.search(query, 2)[1]
		page = wikipedia.page(nquery)
		ret = wikipedia.summary(nquery, sentences=sentences)

	sections = page.sections
	found = None

	# Procura a seção requesitada
	for sec in sections:
		if(sec.lower() == section.lower()):
			ret = page.section(sec)
			found = True
			break

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