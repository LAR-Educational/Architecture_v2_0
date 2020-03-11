#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs

<<<<<<< HEAD
import numpy as np
import time

st = time.time()

print "Started", st

out = open("out.txt", "w")

# f = np.loadtxt(open("Evaluations/weights_64.csv", "rb"), delimiter=",")
f = np.loadtxt(open("Evaluations/weights_72.csv", "rb"), delimiter=",")

print "loaded. Searching maximum", (st - time.time())/60


#i = np.where(f == np.amax(f))


row = f[np.where(f[:,6] == 72)]
# row = f[np.where(f[:,6] == 64)]


print "Done", (st - time.time())/60

#print row[0]

np.savetxt('72.csv', row, delimiter=',', fmt='%f')

#out.write(row[0])
#print f[np.where(f[:,6] == 64)]
out.close()
#f.close()











=======
>>>>>>> 8588090925555211825cca553f36ade5016ea42c
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