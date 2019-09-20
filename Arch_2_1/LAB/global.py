# -*- coding: utf-8 -*-
"""
Created on 21/03/18

@author: dtozadore
"""

# ----- System imports -----

import sys
import time
import cv2
import csv
import os
import pickle
import random
from pprint import pprint
import numpy as np

# ----- R-CASTLE Modules imports -----

from Modules import vars as core
#from Modules import dialog #as diag
#from Modules import motion as mt
from Modules import vision #as vs
from Modules.Vision import predict
from Modules.Vision import data_process #as dp
from Modules import content as ct


teddy_ip="169.254.178.70"
robotIp=teddy_ip
port = 9559


def main():
    




	act = ct.Activity("X")

	act.print_Attributes()

	#ct.create_Activity(act)




	actmain = load_Activity("Par_Impar2")

	actmain.print_Attributes()

	act.name = actmain.name
	act.description = actmain.description
	act.vision = actmain.vision
	act.dialog = actmain.dialog
	act.adapt = actmain.adapt
	act.path = actmain.path
	act.classes = actmain.classes
	act.ncl = actmain.ncl
	
	
	act.print_Attributes()
	
	act.save()


	return 1


def old():
    
	info("Starting program ")            

	info("Connecting with NAO")
	nao = False

	try:
		#core.initializer();
	 	nao=core.Robot(teddy_ip, port)   
	except:
		info("Exception:" + str(sys.exc_info()[0]))
		
		print "Robô: ", nao
		
		
		raise

	info(" ----- Starting Vision System -----")
	try:
		vs = vision.VisionSystem(nao) 
	except:
		error(" ----- Error loading Vision System -----")
		war("Exception type:" + str(sys.exc_info()[0]))
		raise


	info(" ----- Starting Dialogue System -----")
	try:
		ds = dialog.DialogSystem(nao,'Modules/Dialog') 
	except:
		error(" ----- Error loading Dialogue System -----")
		war("Exception type:" + str(sys.exc_info()[0]))
		#raise




    
    
    
    
    
    #ds.say("VAI CATAR COQUINHO", True, T)
    
    
    #act = Activity("Par_Impar", "Atividade de teste", vision=True)
    

    #act = load_Activity("Par_Impar")
    
    
    #pi = ParImpar("Par_Impar2", "Atividade de teste", vision=True)
    #create_Activity(pi,vs)
    
	pi = load_Activity("Par_Impar2")

	pi.print_Attributes()

	#vs.increase_database(pi,max_imgs=10, camId=1)
	dp = data_process.Data_process(pi.path )
	dp.buildTrainValidationData()
	dp.data_aug()		
	dp.generate_model()
	dp.save_best()
	dp.print_classes()

	#pi.play(ds,vs)
    
	return 1    
    






	act = pi




	act.print_Attributes()
	classes = core.load_classes(os.path.join(act.path, "file_classes.csv"))

	model = predict.load_model(model_name=os.path.join("Activities", act.name, "model.h5"))
	#core.behavior.runBehavior("right_hand_up-5bd8bd/behavior_1")

	#counter=0

	while 1:

		#time.sleep(1)
		#c = raw_input("( " + str(counter) + " ) label:") 
		#if c == "x":
			#break
		#counter += 1
	
		im=vs.get_img(1)
		cv2.imshow("top-camera-320x240", im)
	
		if cv2.waitKey(1) == core.ENTER:
			break
	
	
		name = "images/0.jpeg"# + str(time.ctime()) + ".jpg"
		cv2.imwrite(name,im)
		#print("Image saved." + name)
	 	#cv2.destroyAllWindows()
		label=predict.predict_from_path(model,name)
		print label
	
		print "Label:", classes [np.argmax(label[0])]







	info("DONE!\n")









	return True




#--------------------------------------------------------------------------------------------------

class Activity():
	'''
	Class for activity attributes

	'''

	def __init__(self, name, description = "", vision = False, dialog = True, 
					adapt = False, path = "./Activities" ):
		self.name = name
		self.description = description
		self.vision = vision
		self.dialog = dialog
		self.adapt = adapt
		self.path = os.path.join(path,name)
		self.classes = []
		self.ncl = 0
		
	def save(self):
		info("Writing activity attributes" )
		
		with open(os.path.join(self.path,'activity.data'), 'wb') as f:
			pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
		
		info("Write successfull" )


	def print_Attributes(self,):
		pprint(vars(self))





def create_Activity(act, vs):
	'''    
	Create a new activity and set all directories
	'''



	if os.path.exists(act.path):
		war("Path activity exists")        
		
	else:
		info("Starting new activity folder in " + act.path )
		os.makedirs(act.path)
		os.makedirs(os.path.join(act.path,"Vision" ))
		os.makedirs(os.path.join(act.path, "Dialog" ))
		os.makedirs(os.path.join(act.path, "Users" ))
		os.makedirs(os.path.join(act.path, "Logs" ))
	
	info("Writing activity attributes" )
	
	
	
	if act.vision:
		info("Starting Vision Componets for activity: " + act.name)
		act.classes = vs.collect_database(act, camId=1)
		act.ncl = len(act.classes)
		#act.save()
		dp = data_process.Data_process(act.path )
		#dp.buildTrainValidationData()
		#dp.data_aug()		
		#dp.generate_model()
		dp.save_best()
		dp.print_classes()
	
	else:
		war("Activity <<" + act.name + ">> has no Vision system required")	
	
		
	
	with open(os.path.join(act.path,'activity.data'), 'wb') as f:
		pickle.dump(act, f, pickle.HIGHEST_PROTOCOL)
	
	info("Writining successfull" )
	
	
	
		
		
#def process_Activity_data(path):

			





def load_Activity(name):
		core.info("Loading activity attributes" )
		
		with open(os.path.join(core.current_path, "Activities", name, 'activity.data'), 'rb') as f:
			return pickle.load(f)
		
		core.info("Loaded successfull" )
    
#"""    

    





class ParImpar(Activity):
	'''
	
	'''

	def __init__(self, name, description = "", vision = False, dialog = True, 
					adapt = False, path = "./Activities" ):
		
		Activity.__init__(self, name, description,  vision, dialog, adapt, path )
	


	
	def play(self, ds, vs, nmax=3):
	
		self.classes = core.load_classes(os.path.join(self.path, "file_classes.csv"))
		
		model = predict.load_model(model_name=os.path.join("Activities", self.name, "model.h5"))

		ans = ""
		'''
		while ans != "sim":
			str2say = ds.load_from_file(os.path.join(self.path,"Dialog",'instruction.txt'))
			ds.say(str2say, block=True, animated=True)
			ds.say("Você entendeu?" , block=True, animated=True)
			ans = ds.getFromMic_Pt()
		
		#print ans
		
		ds.say("Certo, que os jogos comecem!")
		
		'''
		
		for turn in range(0,nmax):
		
			robotChoice = ""
			userChoice = ""
			
			
			options = ["par", "ímpar"]
			phrases = ["eu escolho par", "eu escolho ímpar"]
			
			
			if not par(turn):
				ds.say("Minha vez de escolher")
				ran = random.randint(0,1)
				if par(ran):
					robotChoice = "par"
					userChoice = "ímpar"
				else:	
					robotChoice = "ímpar"
					userChoice = "par"
					
				ds.say("Eu escolho " + robotChoice)
				ds.say("Você fica com " + userChoice)	
			else:
				

				while userChoice not in ["par", "ímpar"]:
					ds.say("Sua vez. Você escolhe par ou ímpar?")	
					print "Antes função"
					foo = ds.getFromMic_Pt()
					
					userChoice = options[phrases.index(foo)]
					
					print "depois função"	
								
				if userChoice == "par":
					robotChoice = "ímpar"
				else:
					robotChoice = "par"		
				
			
			
			
			
			ds.say("Então eu fico com " + robotChoice + " e você fica com " + userChoice)
			
			im=vs.get_img(1)
			name = "images/0.jpeg"# + str(time.ctime()) + ".jpg"
			cv2.imwrite(name,im)
			#print("Image saved." + name)
		 	#cv2.destroyAllWindows()
			label=predict.predict_from_path(model,name)
			
			print label
			
			userValue = self.classes [np.argmax(label[0])]
			
			print "read:", userValue
			
			ds.say("Você colocou o valor " + str(userValue))
			
			
			robotValue = random.randint(0,1)
			
			total = int(userValue)+robotValue
			
			print total
			
			if par(total):
				result = 'par'
			else:
				result = 'impar'
			

			ds.say("Eu coloquei " + str(robotValue) + " e você colocou " + userValue)



			if robotChoice == result:
				ds.say("Eu ganhei porque "+ str(robotValue) + " com " + userValue + " são " + str(robotValue+int(userValue)) + "que é " + result)
			else:
				ds.say("Você ganhou porque "+ str(robotValue) + " com " + userValue + " são " + str(robotValue+int(userValue)) + "que é " + result)
			
			
			ds.say("Vamos outra vez?")
		
		ds.say("Fim da Brincadeira")
		
		
		
		
		#print str2say
	
	











def par(n):
	if n%2==0:
		return True
	else:
		return False




















#--------------------------------------------------------------------------------------------------
    
    
def info(stringToPrint):   
    if core.debug:
            core.info(stringToPrint)            

    
def war(stringToPrint):   
    if core.debug:
            core.war(stringToPrint)            

    
def error(stringToPrint):   
    if core.debug:
            core.error(stringToPrint)            


    
if __name__ == "__main__":
    main()      

#--------------------------------------------------------------------------------------------------

'''
    
def old():
    
        
    #rs.initializate('teste_com_ruidos_pesados_'+ str(time.ctime()) +'.csv')
    
    while 1:
    
		#time.sleep(1)
		c = raw_input("( " + str(counter) + " ) label:") 
		if c == "x":
		    break
		counter += 1
		
		#cv2.imshow("top-camera-320x240", im)
		#cv2.waitKey(0)
		name = "newimg/" + c + "_" + str(time.ctime()) + ".jpg"

		cv2.imwrite(name,im)
		print("Image saved." + name)
	 	#cv2.destroyAllWindows()
		

		
		ret = vs.classify(im, core.classifierType)   
		#print 'oi'
		#ret['csv']['class'] = c
		#rs.write_row(ret['csv'])
		#print ret
		vs.print_proba(ret, full=True, classifier=core.classifierType)
        
		#print 'Input classified as ', core.figures[ret['all']['label']]
        
		if(ret['all']['label']==-1):
			diag.say("Não consegui reconhecer")
		else:            
			diag.say("Achei a figura " + core.figures[ret['all']['label']])
    	
    
    while True:
        
        time.sleep(1)
        c = raw_input("( " + str(counter) + " ) label:") 
        counter += 1
        if c == "x":
            break
        
        im=vs.see()    
        
       # cv2.imshow("top-camera-320x240", im)
      #  cv2.waitKey(0)
        name = "newimg/" + c + "_" + str(time.ctime()) + ".jpg"

        cv2.imwrite(name,im)
        print("Image saved." + name)
     #   cv2.destroyAllWindows()
        

        
        
        ret = vs.classify(im, core.classifierType)   
        ret['csv']['class'] = c
        rs.write_row(ret['csv'])
        
        vs.print_proba(ret, full=True, classifier=core.classifierType)
        
    diag.say("Obrigado por participar.")    
    
    
    
    core.finisher()
    
    
    core.motors.rest()
    info("FINISHED")



	PREDICTIONS:
	
	
    
    
    
    
    
    
    
    #diag.saynonblock("Olá. Estou inicializando meus sistemas. Logo brincaremos.")
    
    model=predict.load_model(model_name="Modules/Vision/data/garrafa_carteira/model.h5")
    #core.behavior.runBehavior("right_hand_up-5bd8bd/behavior_1")
    
    counter=0
	
    while 1:
    
		#time.sleep(1)
		#c = raw_input("( " + str(counter) + " ) label:") 
		#if c == "x":
		    #break
		counter += 1
		
		im=vs.see(1)
		cv2.imshow("top-camera-320x240", im)
		
		if cv2.waitKey(1) == core.ENTER:
			break
		
		
		name = "images/0.jpeg"# + str(time.ctime()) + ".jpg"
		cv2.imwrite(name,im)
		#print("Image saved." + name)
	 	#cv2.destroyAllWindows()
		label=predict.predict_from_path(model,name)
		print counter
    	

'''



