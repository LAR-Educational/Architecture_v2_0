#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# Classe criada para gerenciar os arquivos que servirão para guardar as perguntas e repostas.
class File(object):
	def __init__(self, filename='knowledge'):
		# Inicializa as varáveis usadas no código.
		self.filename = filename
		self.ram = {}
		self.temp = None

		# Confere se já existe algo guardado e o coloca na ram se não só criar um arquivo novo.
		try:
			self.file = open('./Database/' + self.filename + '.dat', 'r+')

			# Le as entradas do arquivo.
			for line in self.file:
				temp = self.file.readline().splitlines()
				line = line.splitlines()
				self.ram[line[0]] = temp[0]
		except:
			self.file = open('./Database/' + self.filename + '.dat', 'w+')

		# Confere se o programa foi terminado abruptamente.
		try:
			self.temp = open('./Database/' + self.filename + '.temp', 'r+')

			# Salvar o arquivo temporário na ram e no arquivo permanente.
			for line in self.temp:
				temp = self.temp.readline().splitlines()
				line = line.splitlines()
				self.ram[line[0]] = temp[0]

				self.file.write(line[0] + '\n')
				self.file.write(temp[0] + '\n')

			# Reinicia o arquivo temporário.
			self.temp.close()
			self.temp = open('./Database/' + self.filename + '.temp', 'w+')
			self.temp.close()
			self.temp = None			
		except:
			pass

		# Arquivo das perguntas não respondidas.
		self.nans = open('./Database/' + self.filename + '.nans', 'w+')

	# Escreve a entrada no arquivo.
	def write(self, key, content=''):
		if(self.temp == None):
			self.temp = open('./Database/' + self.filename + '.temp', 'w+')	
		
		if(content != ''):
			if key not in self.ram:
				self.ram[key] = content
				
				self.temp.write(key + '\n')
				self.temp.write(content + '\n')
		else:
			self.nans.write(key + '\n')


	# Procura uma pergunta na ram, retorna a resposta ou nada se não ele não tiver ela.
	def search(self, query):
		if query in self.ram:
			return self.ram[query]
		else:
			return None

	# Limpa todos os arquivos utilizados.
	def clean(self):
		self.close()
		self.file = open('./Database/' + self.filename + '.dat', 'w+')
		self.nans = open('./Database/' + self.filename + '.nans', 'w+')
		try:
			self.temp = open('./Database/' + self.filename + '.temp', 'w+')
		except:
			pass

	# Fecha todos os arquivos utilizados.
	def close(self):
		self.file.close()
		self.nans.close()
		try:
			self.temp.close()
		except:
			pass

	# Termina a execução corretamente.
	def end(self):
		self.close()

		# Salva todas as respostas e perguntas guardadas no arquivo permanente.
		self.file = open('./Database/' + self.filename + '.dat', 'w+')
		for x, y in self.ram.items():
			self.file.write(x + '\n')
			self.file.write(y + '\n')
		
		# Remove o arquivo temporário.
		try:
			os.remove('./Database/' + self.filename + '.temp')
		except:
			pass
