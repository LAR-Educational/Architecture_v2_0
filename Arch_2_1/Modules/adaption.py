# coding=UTF-8

from __future__ import division

import vars  as core
import random
import numpy as np
import time
import time
import os

def normalize(read_val, max_val, min_val=0, floor=0, roof=1):
	"""
	Normalize two numbers betwenn 0 to 1
	"""
	#return float((read_val*roof)/max_val)
	return float ( (roof-floor)/(max_val-min_val)*(read_val-max_val)+ roof )




class OperationalParameters:
	"""
	 Class to hold OP
	
	"""
	
	def __init__(self, max_deviation, max_emotion_count, 
					min_number_word, max_time2ans, min_suc_rate	):
					
		self.max_deviation = max_deviation 
		self.max_emotion_count = max_emotion_count  
		self.min_number_word =  min_number_word
		self.max_time2ans = max_time2ans
		self.min_suc_rate = min_suc_rate
		
		
		

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

		

	def adp_function(self, fadp_previous_value = 0):
		
		#calculating the alpha vector
		
		alpha = normalize(self.rv.deviations, self.op.max_deviation)
		core.info("Alpha :" + str(alpha)) 
		
		#calculating the beta vector
		beta = (normalize(self.rv.emotionCount, self.op.max_emotion_count) + 
							 normalize(self.rv.numberWord, self.op.min_number_word) )/2
		core.info("Beta :" + str(beta)) 
		
		#calculating the gama vector
		gama = (normalize(self.rv.time2ans, self.op.max_time2ans) 
							+ normalize(self.rv.sucRate, self.op.min_suc_rate) )/2
		core.info("Gama :" + str(gama)) 
		
		
		fadp = self.w.alpha*alpha + self.w.beta*beta + self.w.gama*gama
		core.info("fadp = w.alpha*alpha + w.beta*beta + w.gama*gama")
		core.info(str(fadp) + " = " 
		 			+ str(self.w.alpha) + "*" + str(alpha) 
		 			+ " + " + str(self.w.beta) + "*" + str(beta) + " + "
		 			+  str(self.w.gama) + "*" + str(gama))
		
		# fadp(t) = fadp(t-1) + fadp(t)
		fadp =  fadp + fadp_previous_value
		core.info("Final: " + str(fadp))				
			
		return fadp
		
		
		
	def activation_function(self, fadp):	
		#Activation function
				
		if fadp > 0.65:
			return 1
		elif fadp < 0.33:	
			return -1
		else:
			return 0	
		
		
		
		
		
		

def main():

	key = ""
	fa = 0

	w = Weights(0.5, 0.2, 0.3 )	
	#w = Weights(0.3, 0.1, 0.2 )	

	op = OperationalParameters (max_deviation=5.0, max_emotion_count=3, 
									min_number_word=1 , max_time2ans=10, min_suc_rate=1)
	
	while(key!="e"):

		#print "test", normalize(1.75,5)

	
		rv= core.ReadValues(deviations=random.randint(0, 5), emotionCount=random.randint(0, 3), 
						numberWord=random.randint(0,1), time2ans=random.randint(0, 10), 						sucRate=random.randint(0, 1)	)

	
		#print "on main", op.max_deviation
		#print "weights", w.alpha
		#print "rv.deviations", rv.deviations
	
	
	
		adpt = AdaptiveSystem(robot=1,path=2, op=op, w=w, rv=rv)

		fc = adpt.adp_function()
		core.info( "Fadp: " + str(fc) )
		
		
		act = adpt.activation_function(fc)
		core.info( "Activation: " + str(act) )
		
		key=raw_input("Key: ")

		fa = fc


if __name__ == "__main__":
	main()














