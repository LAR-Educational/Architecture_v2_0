# -*- coding: utf-8 -*-
"""
Created on Thu May  4 16:14:07 2017

@author: dtozadore
"""

import sys
from modules import vars
from modules import dialog as diag
from modules import motion as mt
from modules import vision as vs

from modules.vision_components import results as rs
import time

import cv2
#import time


def main():
    
    info("Starting program ")            
    
    info("Connecting with NAO")    
    
    try:
        vars.initializer();
    except:
        info("Exception:" + sys.exc_info()[0])
    
    
    
    info("Starting vision system")
    
    
    
    diag.saynonblock("Olá. Estou inicializando meus sistemas. Logo brincaremos.")
    
    
   
    vs.initializate(vars. training_path, vars.classifierType)
    counter = 0
    
    diag.say("Vamos começar")   

    #vars.behavior.runBehavior("right_hand_up-5bd8bd/behavior_1")  
    
    
    
    diag.saynonblock('estou um pouco tímido')
    
    vars.behavior.runBehavior('dialog_move_hands/animations/HandsOnEyes') 
    
    print 'BEHAV \n', vars.behavior.getInstalledBehaviors()    
    


    
    
    
        
    #rs.initializate('teste_com_ruidos_pesados_'+ str(time.ctime()) +'.csv')
    
    while 1:
    
		#time.sleep(1)
		c = raw_input("( " + str(counter) + " ) label:") 
		if c == "x":
		    break
		counter += 1
		
		im=vs.see()
		#cv2.imshow("top-camera-320x240", im)
		#cv2.waitKey(0)
		name = "newimg/" + c + "_" + str(time.ctime()) + ".jpg"

		cv2.imwrite(name,im)
		print("Image saved." + name)
	 	#cv2.destroyAllWindows()
		

		
		ret = vs.classify(im, vars.classifierType)   
		#print 'oi'
		#ret['csv']['class'] = c
		#rs.write_row(ret['csv'])
		#print ret
		vs.print_proba(ret, full=True, classifier=vars.classifierType)
        
		#print 'Input classified as ', vars.figures[ret['all']['label']]
        
		if(ret['all']['label']==-1):
			diag.say("Não consegui reconhecer")
		else:            
			diag.say("Achei a figura " + vars.figures[ret['all']['label']])
    	
    '''
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
        

        
        
        ret = vs.classify(im, vars.classifierType)   
        ret['csv']['class'] = c
        rs.write_row(ret['csv'])
        
        vs.print_proba(ret, full=True, classifier=vars.classifierType)
    '''    
    diag.say("Obrigado por participar.")    
    
    
    
    vars.finisher()
    
    
    vars.motors.rest()
    info("FINISHED")






    
    
    
    
    
def info(stringToPrint):   
    
    
    if vars.debug:
            print("[INFO ] "+ stringToPrint)            

















    
if __name__ == "__main__":
    main()  
