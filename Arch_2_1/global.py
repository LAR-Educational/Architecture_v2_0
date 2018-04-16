# -*- coding: utf-8 -*-
"""
Created on 21/03/18

@author: dtozadore
"""

import sys
from modules import vars
from modules import dialog #as diag
#from modules import motion as mt
from modules import vision #as vs
from modules.Vision import predict
import time
import cv2
import csv

teddy_ip="169.254.178.70"
robotIp=teddy_ip
port = 9559


def main():
    
    info("Starting program ")            
    
    info("Connecting with NAO")    
    try:
        #vars.initializer();
     	nao=vars.Robot(teddy_ip, port)   
    except:
        info("Exception:" + str(sys.exc_info()[0]))
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
    	ds = dialog.DialogSystem(nao,'modules/Dialog') 
    except:
        error(" ----- Error loading Dialogue System -----")
    	war("Exception type:" + str(sys.exc_info()[0]))
        raise
    
    
    
    ds.quiz()
    
    
    
    #collect_database("images_new/")
    
    
    #vs.see(1)
    #ds.setParameter('speed', 70)
    #ds.setParameter('volume', 100)
    #ds.say("estás pis to li tu?", animated=True)
    
    
    #vs.collect_database("modules/Vision/data/", camId=1)
    
    #print vars.shapes
    
    
    
    info("DONE!\n")
    
    
    
    
    
    
    
    
    
    return True
    
    
    
    
    
    
    
    
    
    
    
    
    #diag.saynonblock("Olá. Estou inicializando meus sistemas. Logo brincaremos.")
    
    model=predict.load_model(model_name="modules/Vision/data/garrafa_carteira/model.h5")
    #vars.behavior.runBehavior("right_hand_up-5bd8bd/behavior_1")
    
    counter=0
	
    while 1:
    
		#time.sleep(1)
		#c = raw_input("( " + str(counter) + " ) label:") 
		#if c == "x":
		    #break
		counter += 1
		
		im=vs.see(1)
		cv2.imshow("top-camera-320x240", im)
		
		if cv2.waitKey(1) == vars.ENTER:
			break
		
		
		name = "images/0.jpeg"# + str(time.ctime()) + ".jpg"
		cv2.imwrite(name,im)
		#print("Image saved." + name)
	 	#cv2.destroyAllWindows()
		label=predict.predict_from_path(model,name)
		print counter
    	




















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
        
    diag.say("Obrigado por participar.")    
    
    
    
    vars.finisher()
    
    
    vars.motors.rest()
    info("FINISHED")


'''



    
    
    
    
    
def info(stringToPrint):   
    if vars.debug:
            vars.info(stringToPrint)            

    
def war(stringToPrint):   
    if vars.debug:
            vars.war(stringToPrint)            

    
def error(stringToPrint):   
    if vars.debug:
            vars.error(stringToPrint)            


    
if __name__ == "__main__":
    main()  
