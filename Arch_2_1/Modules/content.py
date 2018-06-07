import vars as core
import os
from pprint import pprint
import numpy as np
import pickle




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
		core.info("Writing activity attributes" )
		
		with open(os.path.join(self.path,'activity.data'), 'wb') as f:
			pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
		
		core.info("Write successfull" )


	def print_Attributes(self,):
		pprint(vars(self))





def create_Activity(act, vs=False):
	'''    
	Create a new activity and set all directories
	'''



	if os.path.exists(act.path):
		core.war("Path activity exists")        
		
	else:
		core.info("Starting new activity folder in " + act.path )
		os.makedirs(act.path)
		os.makedirs(os.path.join(act.path,"Vision" ))
		os.makedirs(os.path.join(act.path, "Dialog" ))
		os.makedirs(os.path.join(act.path, "Users" ))
		os.makedirs(os.path.join(act.path, "Logs" ))
	
	core.info("Writing activity attributes" )
	
	
	
	if act.vision:
		core.info("Starting Vision Componets for activity: " + act.name)
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
		core.war("Activity <<" + act.name + ">> has no Vision system required")	
	
		
	
	with open(os.path.join(act.path,'activity.data'), 'wb') as f:
		pickle.dump(act, f, pickle.HIGHEST_PROTOCOL)
	
	core.info("Writining successfull" )
	
	
	
		
		
#def process_Activity_data(path):

			





def load_Activity(name):
		core.info("Loading activity attributes" )
		

	
		with open(name, 'rb+') as f:
			return pickle.load(f)
		
		core.info("Loaded successfull" )
    
#"""    

    



  
    
