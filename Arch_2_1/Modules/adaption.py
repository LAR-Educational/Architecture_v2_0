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
	Normalize two numbers between floor to roof
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

	def __init__(self, op, w, rv):
	
	    	#self.robot = robot
	    	#self.path = path
	    	self.op = op
	    	self.w = w #weights class
		self.rv = rv		
		flag_log=core.flag_log	

	def adp_function(self, adaptive_frame, fadp_previous_value = 0):
	
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
		core.info("fadp(t) = w.alpha*alpha + w.beta*beta + w.gama*gama")
		core.info(str(fadp) + " = " 
					+ str(self.w.alpha) + "*" + str(alpha) 
					+ " + " + str(self.w.beta) + "*" + str(beta) + " + "
					+  str(self.w.gama) + "*" + str(gama))
	
		# fadp(t) = fadp(t-1) + fadp(t)
		fadp =  fadp + fadp_previous_value
		core.info("Final: " + str(fadp))				
		
		if core.flag_log:
			filename = os.path.join("Log/AdaptiveLogs","vectors_int_" + str(core.interaction_id)+".dat")
			#print filename		
			#print "Log/AdaptiveLogs/vectors_int_" + str(core.interaction_id)+".dat"	

			log_file = open(filename, "a+" )
			log_file.write(str(adaptive_frame) 
					+ "," + str(alpha) 
					+ "," + str(beta) 
					+ "," + str(gama)
					+ "," + str(fadp)  
					+ "," + str( self.activation_function(fadp) ) )
			log_file.write("\n")
			log_file.close()

		return fadp
	
	
	
	def activation_function(self, fadp):	
		#Activation function
			
		if fadp > 0.65:
			return 1
		elif fadp < 0.33:	
			return -1
		else:
			return 0	
	
		
		
def change_behavior(self, robot, behavior):
	
	if behavior < 0:
		robot.tts.setParameter('volume', robot.volume+0.2)
		robot.tts.setParameter('speed',robot.speed-0.2)	
	
	if behavior > 0:
		robot.tts.setParameter('volume', robot.volume-0.2)
		robot.tts.setParameter('speed',robot.speed+0.2)	
	
		
		
		

def main():

	key = ""
	fa = 0

	w = Weights(0.5, 0.2, 0.3 )	
	#w = Weights(0.3, 0.1, 0.2 )	

	op = OperationalParameters (max_deviation=5.0, max_emotion_count=3, 
									min_number_word=1 , max_time2ans=10, min_suc_rate=1)
	
	adap_frame=0

	while(key!="e"):

		#print "test", normalize(1.75,5)

	
		rv= core.ReadValues(deviations=random.randint(0, 5), emotionCount=random.randint(0, 3), 
						numberWord=random.randint(0,1), time2ans=random.randint(0, 10),							sucRate=random.randint(0, 1)	)

	
		#print "on main", op.max_deviation
		#print "weights", w.alpha
		#print "rv.deviations", rv.deviations
			
	
	
		adpt = AdaptiveSystem(op=op, w=w, rv=rv)

		fc = adpt.adp_function(adap_frame)
		core.info( "Fadp: " + str(fc) )
		
		
		act = adpt.activation_function(fc)
		core.info( "Activation: " + str(act) )
		
		key=raw_input("Key: ")

		fa = fc
		adap_frame +=1

if __name__ == "__main__":
	main()














