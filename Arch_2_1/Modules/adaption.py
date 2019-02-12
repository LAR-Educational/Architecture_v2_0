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
	Normalize two numbers betwenn floor to roof
	"""
	#return float((read_val*roof)/max_val)
	if max_val == 0 :
		return  0
	return float ( (roof-floor)/(max_val-min_val)*(read_val-max_val)+ roof )




class ReadValues:
    """
     Class to hold read values
    
    """
    def __init__(self, deviations=0, emotionCount=0,
                 numberWord=0, time2ans=0, sucRate=0):
        self.deviations = deviations 
        self.emotionCount = emotionCount  
        self.numberWord =  numberWord
        self.time2ans = time2ans
        self.sucRate = sucRate
    
    def set(self, deviations=0, emotionCount=0,
                 numberWord=0, time2ans=0, sucRate=0):
        self.deviations = deviations 
        self.emotionCount = emotionCount  
        self.numberWord =  numberWord
        self.time2ans = time2ans
        self.sucRate = sucRate
        



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

	def __init__(self, robot, op_par, w, read_values, out_path=None):
	
		self.robot = robot
		#self.path = path
		self.op_par = op_par
		self.w = w #weights class
		self.read_values = read_values		
		#flag_log=core.flag_log
		self.robot_communication_profile_list=['Sit','Sit','Crouch','StandInit','Stand']
		self.robot_communication_profile = 2
		self.deviation_times = []
		
		self.out_path = str(out_path) #Path to write the output

		self.emotions = {'happy': 0, 'sad': 0, 'angry': 0, 'disgust': 0,
	 	'surprise': 0, 'fear': 0, 'neutral': 0}




	def adp_function(self, adaptive_frame, fadp_previous_value = 0):
	
		#calculating the alpha vector
	
		alpha = normalize(self.read_values.deviations, self.op_par.max_deviation)
		core.info("Alpha :" + str(alpha)) 
	
		#calculating the beta vector
		beta = (normalize(self.read_values.emotionCount, self.op_par.max_emotion_count) + 
			normalize(self.read_values.numberWord, self.op_par.min_number_word) )/2
		
		core.info("Beta :" + str(beta)) 
	
		#calculating the gama vector
		# gama = (normalize(self.read_values.time2ans, self.op_par.max_time2ans) + 
		# 	 normalize(self.read_values.sucRate, self.op_par.min_suc_rate) )/2
		
		gama = normalize(self.read_values.sucRate, self.op_par.min_suc_rate) 
		

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
		
		if self.out_path is not None:
			path_name = os.path.join( "Log", "AdaptiveLogs", self.out_path + "_reads.txt") 
			print "Vectors PATH: ", path_name
			log_file = open(path_name, "a+" )
			log_file.write(str(adaptive_frame) 
					+ "," + str(fadp)  
					+ "," + str(alpha) 
					+ "," + str(beta) 
					+ "," + str(gama) )
			log_file.write("\n")
			log_file.close()

		return fadp
	
	
	
	def activation_function(self, fadp):	
		#Activation function
			
		if fadp > 0.65:
			return -1
		elif fadp < 0.33:	
			return 1
		else:
			return 0	
	
		
		
	def change_behavior(self, behavior):
		

		if behavior == 0:
			core.info("Communication profile held!")
			#self.robot.posture.goToPosture(self.robot_communication_profile_list[self.robot_communication_profile-1],1)
			return 0

		if behavior < 0:
			core.info("Decreasing communication profile!")
			if self.robot.volume < 1:
				self.robot.volume+=0.1
			
			if self.robot_communication_profile > 0: 
				self.robot_communication_profile-=1
		
		if behavior > 0:
			core.info("Increasing communication profile!")
			if self.robot.volume > 0.2:
				self.robot.volume-=0.1
			
			if self.robot_communication_profile < 5: 
				self.robot_communication_profile+=1
	
		#self.robot.posture.goToPosture(self.robot_communication_profile_list[self.robot_communication_profile-1],1)
		core.info("Adapting to communication profile " + str(self.robot_communication_profile) +" in position " + str(self.robot_communication_profile_list[self.robot_communication_profile-1]))
		self.robot.tts.setVolume(self.robot.volume)
		core.info("Volume set to " + str(self.robot.volume))
		
		
		if self.out_path is not None:
			path_name = os.path.join("Log", "AdaptiveLogs", self.out_path + "_behaviors.txt") 
			#print "PATH: ", path_name
			log_file = open(path_name, "a+" )
			log_file.write(str(behavior) 
					+ "," + str(self.robot_communication_profile) )
			log_file.write("\n")
			log_file.close()





	def getBadEmotions(self):
		
		emo =  self.emotions['sad'] + self.emotions['angry'] +  self.emotions['disgust'] + self.emotions['fear']     
		core.info( "Number of bad emotions" +  str(emo))

		return emo


	def clear_emo_variables(self):

		self.emotions
		for i in self.emotions.keys():
			self.emotions[i] = 0
		
		#print "DEVIATION", deviation_times
		#global deviation_times
		del self.deviation_times[:]
			





# def main():


# 	key = ""
# 	fa = 0

# 	w = Weights(0.5, 0.2, 0.3 )	
# 	#w = Weights(0.3, 0.1, 0.2 )	

# 	op = OperationalParameters (max_deviation=5.0, max_emotion_count=3, 
# 									min_number_word=1 , max_time2ans=10, min_suc_rate=1)
	
# 	while(key!="e"):

# 		#print "test", normalize(1.75,5)

	
# 		read_values= core.ReadValues(deviations=random.randint(0, 5), emotionCount=random.randint(0, 3), 
# 						numberWord=random.randint(0,1), time2ans=random.randint(0, 10),							sucRate=random.randint(0, 1)	)

	
# 		#print "on main", op.max_deviation
# 		#print "weights", w.alpha
# 		#print "read_values.deviations", read_values.deviations
	
	
	
# 		adpt = AdaptiveSystem(op=op, w=w, read_values=read_values)

# 		fc = adpt.adp_function()
# 		core.info( "Fadp: " + str(fc) )
		
		
# 		act = adpt.activation_function(fc)
# 		core.info( "Activation: " + str(act) )
		
# 		key=raw_input("Key: ")

# 		fa = fc


def test():
	print normalize(3,5,1)

if __name__ == "__main__":

	 test()


# 	main()














