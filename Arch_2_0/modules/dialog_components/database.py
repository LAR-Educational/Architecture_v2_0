#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import settings

# Classe criada para gerenciar os arquivos que servirão para guardar as perguntas e repostas.
class File(object):
	def __init__(self, filename='knowledge'):
		# Inicializa as varáveis usadas no código.
		self.filename = filename
		self.ram = {}

		# Confere se existe o folder que será salvo os arquivos.
		if os.path.isdir("./Database") is False:
			settings.info("Creating folder...")
			os.mkdir("./Database")

		# Confere se já existe algo guardado e o coloca na ram se não só criar um arquivo novo.
		try:
			settings.info("Reloading memory...")
			self.file = codecs.open('./Database/' + self.filename + '.dat', 'r+', encoding="utf-8")

			# Le as entradas do arquivo.
			for line in self.file:
				temp = self.file.readline().splitlines()
				line = line.splitlines()
				self.ram[line[0]] = temp[0]
		except:
			settings.info("Memory not found.", 1)
			self.file = codecs.open('./Database/' + self.filename + '.dat', 'w+', encoding="utf-8")

		# Abre o arquivo das perguntas não respondidas.
		self.nans = codecs.open('./Database/' + self.filename + '.nans', 'w+', encoding="utf-8")

	# Escreve a entrada no arquivo.
	def write(self, key, content):
		if(self.file == None):
			self.file = codecs.open('./Database/' + self.filename + '.dat', 'a+', encoding="utf-8")
		
		if key not in self.ram:
			settings.info("Saving on file...")
			
			self.ram[key] = content
			
			self.file.write(key + '\n')
			self.file.write(content + '\n')


	# Procura uma pergunta na ram, retorna a resposta ou nada se não ele não tiver ela.
	def search(self, query):
		if query in self.ram:
			return self.ram[query]
		else:
			return None

	def SaveQuery(self, query):
		settings.info("Saving on file...")
		
		self.nans.write(query + '\n')

	# Limpa todos os arquivos utilizados.
	def clean(self):
		settings.info("Cleaning files...")

		self.close()
		self.file = codecs.open('./Database/' + self.filename + '.dat', 'w+', encoding="utf-8")
		self.nans = codecs.open('./Database/' + self.filename + '.nans', 'w+', encoding="utf-8")

	# Fecha todos os arquivos utilizados.
	def close(self):
		settings.info("Closing files...")

		self.file.close()
		self.nans.close()