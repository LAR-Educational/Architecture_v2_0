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
		
	def save(self):
		core.info("Writing activity attributes" )
		
		with open(os.path.join(self.path,'activity.data'), 'wb') as f:
			pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
		
		core.info("Write successfull" )


	def print_Attributes(self,):
		pprint(vars(self))




    
    
