# -*- coding: utf-8 -*-
"""
Created on 21/03/18

@author: dtozadore
"""

import sys
from modules import vars
from modules import dialog as diag
#from modules import motion as mt
from modules import vision as vs
from modules.Vision import predict
import time
import cv2



def main():
    
    info("Starting program ")            
    
    info("Connecting with NAO")    
    
    try:
        vars.initializer();
    except:
        info("Exception:" + sys.exc_info()[0])
    
    
    
    info("Starting vision system")
    
    
    
    
    colect_database("images/")
    
    
    info("DONE!\n\n")
    
    
    
    
    
    
    
    
    
    return True
    
    
    
    
    
    
    
    
    
    
    
    
    #diag.saynonblock("Olá. Estou inicializando meus sistemas. Logo brincaremos.")
    
    model=predict.load_model()
    #vars.behavior.runBehavior("right_hand_up-5bd8bd/behavior_1")
    
    counter=0
	
    while 1:
    
		#time.sleep(1)
		#c = raw_input("( " + str(counter) + " ) label:") 
		#if c == "x":
		    #break
		counter += 1
		
		im=vs.see()
		cv2.imshow("top-camera-320x240", im)
		
		if cv2.waitKey(1) == 1048603:
			break
		
		
		name = "images/c.jpeg"# + str(time.ctime()) + ".jpg"
		cv2.imwrite(name,im)
		#print("Image saved." + name)
	 	#cv2.destroyAllWindows()
		label=predict.predict_from_path(model,name)
		print counter
    	









def colect_database(path_name,max_imgs=100):

	for sh in range(0,3):
		
		diag.say( "Capturando imagens de " + vars.figures[sh] + " Digite ESC para começar ")
    	

		while 1:
			im=vs.see()
			cv2.imshow("top-camera-320x240", im)
			if cv2.waitKey(1) == 1048603:
				break
			
		counter=0
		while counter < max_imgs:
			
			counter += 1
			im=vs.see()
			cv2.imshow("top-camera-320x240", im)
		
			if cv2.waitKey(1) == 1048603:
				break
		
		
			name = path_name + str(sh) + "_" + str(counter) + ".jpeg"# + str(time.ctime()) + ".jpg"
			cv2.imwrite(name,im)
			
			info("Image saved." + name)	

		info("Captura concluida com sucesso!")
















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
            print("[INFO ] "+ stringToPrint)            

















    
if __name__ == "__main__":
    main()  
