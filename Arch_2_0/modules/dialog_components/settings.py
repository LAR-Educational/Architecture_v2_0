#!/usr/bin/env python
# -*- coding: utf-8 -*-

debug = True

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

def init(bool):
	global debug
	debug = bool

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
