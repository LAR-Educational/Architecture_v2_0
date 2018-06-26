# coding=UTF-8

from __future__ import division

import vars  as core
import random
import numpy as np
import time
import time
import os

def normalize(read_val, max_val, roof=1):
	"""
	Normalize two numbers betwenn 0 to 1
	"""
	return float((read_val*roof)/max_val)
	




class OperationalParameters:
	"""
	 Class to hold OP
	
	"""
	
	def __init__(self, max_deviation, max_emotion_count, 
					min_number_word, max_time2ans, min_suc_rate	):
					
		self.max_deviation = max_deviation, 
		self.max_emotion_count = max_emotion_count  
		self.min_number_word =  min_number_word
		self.max_time2ans = max_time2ans
		self.min_suc_rate = min_suc_rate
		
		
		
		
class ReadValues:
	"""
	 Class to hold read values
	
	"""
	
	def __init__(self, deviations=5, emotionCount=3, 
					numberWord=1, time2ans=20, sucRate=1		):
					
		self.deviations = deviations, 
		self.emotionCount = emotionCount  
		self.numberWord =  numberWord
		self.time2ans = time2ans
		self.sucRate = sucRate
		


class Weights:

	def __init__(self, alpha, beta, gama):
		self.alpha = alpha
		self.beta = beta
		self.gama =  gama



class AdaptiveSystem:

	def __init__(self, robot, path, op, w, rv):
	
		self.robot = robot
		self.path = path
		self.op = op
		self.w = w #weights class
		self.rv = rv
		print rv.deviations


	def adp_function(self):
		
		#calculating the alpha vector
		print self.op.max_deviation
		
		alpha = normalize(self.rv.deviations, self.op.max_deviation)
		core.info("Alpha :" + str(alpha)) 
		
		#calculating the beta vector
		beta = normalize( (normalize(self.rv.emotion_count,self.op.max_emotion_count) 
							+ normalize(self.rv.number_word,self.op.min_number_word) )/2)
		core.info("Beta :" + str(beta)) 
		
		#calculating the gama vector
		gama = normalize( (normalize(self.rv.time2ans, self.op.max_time2ans) 
							+ normalize(self.rv.suc_rate, self.op.min_suc_rate) )/2)
		core.info("Gama :" + str(gama)) 
		
		
		fadp = self.w.alpha*alpha + self.w.beta*beta + self.w.gama*gama
		core.info("fadp = w.alpha*alpha + w.beta*beta + w.gama*gama")
		core.info(str(fadp) + " = " 
		 			+ str(self.w.alpha) + "*" + str(alpha) 
		 			+ "+" + str(self.w.beta) + "*" + str(beta) + " + "
		 			+  str(self.w.gama) + "*" + str(gama))
		 
		
		
		
		
		

def main():


	#print "test", normalize(1.75,5)

	w = Weights(0.15, 0.05, 1.5 )	
	op = OperationalParameters (max_deviation=5.0, max_emotion_count=3, 
								min_number_word=1 , max_time2ans=20, min_suc_rate=1)
	rv= ReadValues(deviations=5, emotionCount=3, 
					numberWord=1, time2ans=20, sucRate=1	)

	
	print "on main", op.max_deviation
	print "weights", w.alpha
	print "rv.deviations", rv.deviations
	
	
	
	adpt = AdaptiveSystem(robot=1,path=2, op=op, w=w, rv=rv)


	adpt.adp_function()




if __name__ == "__main__":
	main()














