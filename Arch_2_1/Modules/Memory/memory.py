#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import file
import log

# Classe criada para gerenciar os arquivos que servirão para guardar as perguntas e repostas.
class Memory(object):
	def __init__(self):
		# Inicializa as varáveis usadas no código.
		self.ram = {}
		self.file = file.File('information')

		self.file.goestostart()
		# Le as entradas do arquivo.
		for line in self.file:
			temp = self.file.next().splitlines()
			line = line.splitlines()
			self.ram[line[0]] = temp[0]

		# Abre o arquivo das perguntas não respondidas.
		self.nans = file.File('notanswered')
		print(self.ram)

	# Escreve a entrada no arquivo.
	def write(self, key, content):
		if key not in self.ram:
			self.ram[key] = content
			
			self.file.write(key)
			self.file.write(content)


	# Procura uma pergunta na ram, retorna a resposta ou nada se não ele não tiver ela.
	def search(self, query):
		if query in self.ram:
			return self.ram[query]
		else:
			return None

	def SaveQuery(self, query):
		self.nans.write(query)

	# Limpa todos os arquivos utilizados.
	def clean(self):
		self.file.clean()
		self.nans.clean()

	# Fecha todos os arquivos utilizados.
	def close(self):
		self.file.close()
		self.nans.close()
