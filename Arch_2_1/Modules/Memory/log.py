#!/usr/bin/env python
# -*- coding: utf-8 -*-

import file
import datetime

debug = True

class bcolors:
	RED   = '\033[1;31m'  
	BLUE  = '\033[1;34m'
	CYAN  = '\033[1;36m'
	GREEN = '\033[0;32m'
	HEADER = '\033[0;95m'
	WARNING = '\033[1;93m'
	FAIL = '\033[1;91m'
	ENDC = '\033[;0m'
	BOLD = '\033[;1m'
	UNDERLINE = '\033[;4m'
	REVERSE = '\033[;7m'

class Log(object):
	def __init__(self, debug=False):
		self.debug = debug
		self.file = file.File('log', 'LogFiles')

	def log(self, stringToPrint, module='General', tag=0):
		if self.debug:
			if(tag == 0):
				print(bcolors.BOLD + '[INFO] ' + bcolors.BOLD + '[' + module + '] ' + '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '] ' + bcolors.ENDC + stringToPrint)
			elif(tag == 1):
				print(bcolors.WARNING + '[WARNING] ' + bcolors.BOLD + '[' + module + '] ' + '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '] ' + bcolors.ENDC + stringToPrint)
			elif(tag == 2):
				print(bcolors.BLUE + '[EXCEPTION] ' + bcolors.BOLD + '[' + module + '] ' + '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '] ' + bcolors.ENDC + stringToPrint)
			elif(tag == 3):
				print(bcolors.FAIL + '[ERROR] ' + bcolors.BOLD + '[' + module + '] ' + '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '] ' + bcolors.ENDC + stringToPrint)
		if(tag == 0):
			self.file.write('INFO, ' + module + ', ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + ', ' + stringToPrint)
		elif(tag == 1):
			self.file.write('WARNING, ' + module + ', ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + ', ' + stringToPrint)
		elif(tag == 2):
			self.file.write('EXCEPTION, ' + module + ', ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + ', ' + stringToPrint)
		elif(tag == 3):
			self.file.write('ERROR, ' + module + ', ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + ', ' + stringToPrint)
