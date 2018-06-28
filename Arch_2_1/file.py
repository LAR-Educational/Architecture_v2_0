#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs

class File(object):
	def __init__(self, filename='data', folder='Database'):
		self.filename = filename
		self.folder = folder

		if os.path.isdir('./{}'.format(self.folder)) is False:
			os.mkdir('./{}'.format(self.folder))

		try:
			self.file = codecs.open('./{}/{}.dat'.format(self.folder, self.filename), 'a+', encoding='utf-8')
		except FileNotFoundError:
			self.file = codecs.open('./{}/{}.dat'.format(self.folder, self.filename), 'w+', encoding='utf-8')

	def __iter__(self):
		return self.file

	def next(self):
		self.file.readline()

	def goestostart(self):
		self.file.seek(0)

	def write(self, content):
		self.file.write('{}\n'.format(content))

	def clean(self):
		self.close()
		self.file = codecs.open('./{}/{}.dat'.format(self.folder, self.filename), 'w+', encoding='utf-8')

	def close(self):
		self.file.close()