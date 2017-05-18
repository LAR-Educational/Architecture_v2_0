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
    
   
    vs.initializate(vars. training_path, vars.classifierType)
    

   # mt.run("Right_hand_up")       
    rs.initializate()    
    while True:

        time.sleep(1)       
        c = raw_input("label:") 
        
        if c == "x":
            break
        
        im=vs.see()    
        
        
#        cv2.imshow("top-camera-320x240", im)
#        cv2.waitKey()
#        cv2.destroyAllWindows()
#        
        
        ret = vs.classify(im, vars.classifierType)   
        ret['csv']['class'] = c
        rs.write_row(ret['csv'])
        
        vs.print_proba(ret, full=True, classifier=vars.classifierType)
        
    #diag.say("")    
    
    #vars.posture.goToPosture("Crouch", 1.0)
    
    
    #vars.finisher()
    
    
    #vars.motors.rest()








    
    
    
    
    
def info(stringToPrint):   
    
    
    if vars.debug:
            print("[INFO ] "+ stringToPrint)            

















    
if __name__ == "__main__":
    main()  