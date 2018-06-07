#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import log

class File(object):
	def __init__(self, filename='data', folder='Database'):
		self.filename = filename
		self.folder = folder

		if os.path.isdir('./' + self.folder) is False:
			os.mkdir('./' + self.folder)

		try:
			self.file = codecs.open('./' + self.folder + '/' + self.filename + '.dat', 'a+', encoding='utf-8')
		except:
			self.file = codecs.open('./' + self.folder + '/' + self.filename + '.dat', 'w+', encoding='utf-8')

	def __iter__(self):
		return self.file

	def next(self):
		self.file.readline()

	def goestostart(self):
		self.file.seek(0)

	def write(self, content):
		self.file.write(content + '\n')

	def clean(self):
		self.close()
		self.file = codecs.open('./' + self.folder + '/' + self.filename + '.dat', 'w+', encoding='utf-8')

	def close(self):
		self.file.close()