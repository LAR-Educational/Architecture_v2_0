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
from pprint import pprint
import numpy as np

# ----- R-CASTLE Modules imports -----

from Modules import vars as core
from Modules import dialog #as diag
#from Modules import motion as mt
from Modules import vision #as vs
from Modules.Vision import predict
from Modules.Vision import data_process #as dp
from Modules import content as ct


teddy_ip="169.254.178.70"
robotIp=teddy_ip
port = 9559


def main():
    
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
    
    act = load_Activity("Par_Impar")

    #create_Activity(act,vs)
    
    
    
    pi = ParImpar("Par_Impar", "Atividade de teste")
    
    
    pi.print_Attributes()
    
    pi.play(ds)
    
    
    
    
    
    
    
    
    
    
    
    
    return 1    
    
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
	
	with open(os.path.join(act.path,'activity.data'), 'wb') as f:
		pickle.dump(act, f, pickle.HIGHEST_PROTOCOL)
	
	info("Writining successfull" )
	
	
	
	if act.vision:
		info("Starting Vision Componets for activity: " + act.name)
		#act.classes = vs.collect_database(act.name, camId=1)
		
		dp = data_process.Data_process(act.path )
		#dp.buildTrainValidationData()
		#dp.data_aug()		
		#dp.generate_model()
		#dp.print_classes()
	
	else:
		war("Activity <<" + act.name + ">> has no Vision system required")	
	
		
	
	
	
		
		
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
	


	
	def play(self, ds, nmax=3):
	
	
		#print "PATH", self.path
		ans = ""
		
		while ans != "sim":
			str2say = ds.load_from_file(os.path.join(self.path,"Dialog",'instruction.txt'))
			ds.say(str2say, block=True, animated=True)
			ds.say("Você entendeu?" , block=True, animated=True)
			ans = ds.getFromMic_Pt()
		
		#print ans
		
		ds.say("Certo, que os jogos comecem!")
		
		
		
		for turn in range(0,nmax):
		
			if par(turn):
				ds.say("Eu escolho")
			else:
				ds.say("Você escolhe")	
		
		ds.say("Fim da porra toda")
		
		
		
		
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



