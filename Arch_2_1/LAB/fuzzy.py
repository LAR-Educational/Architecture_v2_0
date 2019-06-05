#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import sys # We need sys so that we can pass argv to QApplication
# import csv
# import os
# import cv2
import time
# import pandas as pd
# from utils import *
# import random
# import threading
# from datetime import datetime
# import utils
	
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
  

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
        



class FuzzyControl:

    def __init__(self):

        # New Antecedent/Consequent objects hold universe variables and membership
        # functions
        self.posture = ctrl.Antecedent(np.arange(0, 11, 1), 'Posture')
        self.gaze = ctrl.Antecedent(np.arange(0, 11, 1), 'Gaze')
        self.attention = ctrl.Consequent(np.arange(0, 11, 1), 'Attention')

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        self.posture.automf(3)
        #self.gaze.automf(5)

        self.gaze['rare'] = fuzz.trimf(self.gaze.universe, [0, 2, 4])
        self.gaze['neutral'] = fuzz.trimf(self.gaze.universe, [2, 5, 7])
        self.gaze['frequent'] = fuzz.trimf(self.gaze.universe, [5, 10, 10])
        
        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        self.attention['distracted'] = fuzz.trimf(self.attention.universe, [0, 0, 4])
        self.attention['medium'] = fuzz.gaussmf(self.attention.universe, 5, 2.3 )
        self.attention['concentrated'] = fuzz.trimf(self.attention.universe, [6, 10, 10])

        #self.gaze.view()
        #self.attention.view()
        
        att_rule1 = ctrl.Rule(self.gaze['rare'] | self.posture['poor'], self.attention['distracted'])
        att_rule2 = ctrl.Rule(self.gaze['neutral'], self.attention['medium'])
        att_rule3 = ctrl.Rule(self.gaze['frequent'] | self.posture['good'], self.attention['concentrated'])

        att_ctrl_sys = ctrl.ControlSystem([att_rule1, att_rule2, att_rule3])

        self.att_ctrl = ctrl.ControlSystemSimulation(att_ctrl_sys)




        #------------------ COMMUNICATION

        # New Antecedent/Consequent objects hold universe variables and membership
        # functions
        self.emotions = ctrl.Antecedent(np.arange(0, 11, 1), 'Emotions')
        self.words = ctrl.Antecedent(np.arange(0, 11, 1), 'Words')
        self.communication = ctrl.Consequent(np.arange(0, 11, 1), 'Communication')

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        
        self.emotions['frustrated'] = fuzz.sigmf(self.emotions.universe, 1, -4)
        self.emotions['sad'] = fuzz.gaussmf(self.emotions.universe, 3, 1 )
        self.emotions['neutral'] = fuzz.gaussmf(self.emotions.universe, 5, 1)
        self.emotions['happy'] = fuzz.gaussmf(self.emotions.universe, 7, 1)
        self.emotions['excited'] = fuzz.sigmf(self.emotions.universe, 9, 4)
        #self.gaze[''] = fuzz.trimf(self.gaze.universe, [0, 0, 4])
        #self.gaze[''] = fuzz.trimf(self.gaze.universe, [0, 0, 4])

        

        self.words['contained'] = fuzz.sigmf(self.words.universe, 3.5, -1)
        self.words['regular'] = fuzz.gaussmf(self.words.universe, 5, 1)
        self.words['talker'] = fuzz.sigmf(self.words.universe, 7.5, 1)


        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        self.communication['introverted'] = fuzz.sigmf(self.attention.universe, 2, -1)
        self.communication['neutral'] = fuzz.gaussmf(self.attention.universe, 5, 0.5 )
        self.communication['extroverted'] = fuzz.sigmf(self.attention.universe, 8, 1)

        rules = []

        rules.append( ctrl.Rule(self.emotions['frustrated'] , self.communication['introverted']) )
        rules.append( ctrl.Rule(self.emotions['frustrated'] | self.words['talker'] , self.communication['neutral']) )
        rules.append( ctrl.Rule(self.emotions['sad'] | self.words['contained'] , self.communication['introverted']) )
        rules.append( ctrl.Rule(self.emotions['neutral'] , self.communication['neutral']) )
        rules.append( ctrl.Rule(self.emotions['happy'] | self.words['talker'] , self.communication['extroverted']) )
        rules.append( ctrl.Rule(self.emotions['excited'] | self.words['talker'] , self.communication['extroverted']) )
        

        com_ctrl_sys = ctrl.ControlSystem(rules)

        self.com_ctrl = ctrl.ControlSystemSimulation(com_ctrl_sys)


        # self.emotions.view()
        # self.words.view()
        # self.communication.view()



        #------------------ TASK

         # New Antecedent/Consequent objects hold universe variables and membership
        # functions
        self.success = ctrl.Antecedent(np.arange(0, 6, 1), 'Success')
        self.ans_time = ctrl.Antecedent(np.arange(0, 20, 1), 'Answer Time')
        self.task = ctrl.Consequent(np.arange(0, 11, 1), 'Task')



        # Auto-membership function population is possible with .automf(3, 5, or 7)
        
        # Extremes for lower case (1.4) and higher (4.2) = 2.75
        self.success['high'] = fuzz.gaussmf(self.success.universe, 1.4, 1)#[1.4, 4.2, 4.2] )
        #self.success['average'] = fuzz.gaussmf(self.success.universe, 2.75, 1)#[1.4, 4.2, 4.2] )
        self.success['low'] = fuzz.gaussmf(self.success.universe, 4.2, 1)#[1.4, 4.2, 4.2] )



        self.ans_time['Slow'] = fuzz.gaussmf(self.ans_time.universe, 17, 3)
        self.ans_time['Average'] = fuzz.gaussmf(self.ans_time.universe, 10, 4)
        self.ans_time['Fast'] = fuzz.gaussmf(self.ans_time.universe, 3, 2 )
        
        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        self.task['inefficient']= fuzz.sigmf(self.attention.universe, 2, -1)
        self.task['regular']    = fuzz.gaussmf(self.attention.universe, 5, 3 )
        self.task['efficient']  = fuzz.sigmf(self.attention.universe, 8, 1)


        rules = []

        #print rules

        rules.append( ctrl.Rule(self.success['high'] | self.ans_time['Fast'] , self.task['efficient']) )
        #rules.append( ctrl.Rule(self.success['high'] | self.ans_time['Fast'] , self.task['efficient']) )
        rules.append( ctrl.Rule(self.success['low'] | self.ans_time['Slow'], self.task['inefficient']) )
            

        task_ctrl_sys = ctrl.ControlSystem(rules)

        self.task_ctrl = ctrl.ControlSystemSimulation(task_ctrl_sys)


        self.gaze.view()
        self.posture.view()
        self.attention.view()

        self.emotions.view()
        self.words.view()
        self.communication.view()


        self.success.view()
        self.ans_time.view()
        self.task.view()

        raw_input()


        # self.task_ctrl.input['Success'] = 90
        # self.task_ctrl.input['Answer Time'] = 1

        # self.task_ctrl.compute()

        # print self.task_ctrl.output['Task']


        # self.task.view(sim=self.task_ctrl)


        raw_input()
        return 






class Adaptive():

    def __init__(self):

        # New Antecedent/Consequent objects hold universe variables and membership
        # functions
        self.attention = ctrl.Antecedent(np.arange(0, 11, 1), 'Attention')
        
        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        self.attention['distracted'] = fuzz.trimf(self.attention.universe, [0, 0, 4])
        self.attention['medium'] = fuzz.gaussmf(self.attention.universe, 5, 2.3 )
        self.attention['concentrated'] = fuzz.trimf(self.attention.universe, [6, 10, 10])


        #------------------ COMMUNICATION
        self.communication = ctrl.Antecedent(np.arange(0, 11, 1), 'Communication')
      
        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        self.communication['introverted'] = fuzz.sigmf(self.attention.universe, 2, -1)
        self.communication['neutral'] = fuzz.gaussmf(self.attention.universe, 5, 0.5 )
        self.communication['extroverted'] = fuzz.sigmf(self.attention.universe, 8, 1)


        #------------------ TASK

         # New Antecedent/Consequent objects hold universe variables and membership
        # functions
        self.task = ctrl.Antecedent(np.arange(0, 11, 1), 'Task')
        
        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        self.task['inefficient']= fuzz.sigmf(self.attention.universe, 2, -1)
        self.task['regular']    = fuzz.gaussmf(self.attention.universe, 5, 3 )
        self.task['efficient']  = fuzz.sigmf(self.attention.universe, 8, 1)



        # ADAPTATION

        self.adaptation = ctrl.Consequent(np.arange(0, 6, 1), 'Adaptation')

        self.adaptation.automf(5)


        self.adaptation.view()




        rules = []

        #print rules

        #rules.append( ctrl.Rule(self.task['efficient'] , self.adaptation['decent']) )
        rules.append( ctrl.Rule(self.attention['concentrated'] | self.communication['extroverted']  | self.task['efficient'] , self.adaptation['good']) )
        rules.append( ctrl.Rule(self.attention['concentrated'] | self.task['efficient'] , self.adaptation['decent']) )
        rules.append( ctrl.Rule(self.attention['medium'] | self.communication['neutral']  | self.task['regular'] , self.adaptation['average']) )

        rules.append( ctrl.Rule(self.attention['distracted'] | self.task['inefficient'] , self.adaptation['mediocre']) )
        rules.append( ctrl.Rule(self.attention['distracted'] | self.communication['introverted']  | self.task['inefficient'] , self.adaptation['poor']) )
        #rules.append( ctrl.Rule(self.success['low'] | self.ans_time['Slow'], self.task['inefficient']) )





        self.attention.view()
        self.communication.view()
        self.task.view()


        ctrl_sys = ctrl.ControlSystem(rules)

        self.adp_func = ctrl.ControlSystemSimulation(ctrl_sys)

        self.adp_func.input['Attention'] = 9
        self.adp_func.input['Communication'] = 9
        self.adp_func.input['Task'] = 10


        self.adp_func.compute()


        print self.adp_func.output['Adaptation']

        self.adaptation.view(sim=self.adp_func)

        raw_input()
        return












def exemple():


    # New Antecedent/Consequent objects hold universe variables and membership
    # functions
    quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
    service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
    tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

    # Auto-membership function population is possible with .automf(3, 5, or 7)
    quality.automf(3)
    service.automf(5)

    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    tip['low'] = fuzz.trimf(tip.universe, [0, 5, 20])
    tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
    tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])


    tip.view()
    
    
    
    raw_input()





def adap():


    # New Antecedent/Consequent objects hold universe variables and membership
    # functions
    self.posture = ctrl.Antecedent(np.arange(0, 11, 1), 'self.posture')
    self.gaze = ctrl.Antecedent(np.arange(0, 11, 1), 'self.gaze')
    self.attention = ctrl.Consequent(np.arange(0, 11, 1), 'self.attention')

    # Auto-membership function population is possible with .automf(3, 5, or 7)
    self.posture.automf(3)
    #self.gaze.automf(5)

    self.gaze['rare'] = fuzz.trimf(self.gaze.universe, [0, 2, 4])
    self.gaze['neutral'] = fuzz.trimf(self.gaze.universe, [2, 5, 7])
    self.gaze['frequent'] = fuzz.trimf(self.gaze.universe, [5, 10, 10])
    #self.gaze[''] = fuzz.trimf(self.gaze.universe, [0, 0, 4])
    #self.gaze[''] = fuzz.trimf(self.gaze.universe, [0, 0, 4])

    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    self.attention['distracted'] = fuzz.trimf(self.attention.universe, [0, 0, 4])
    self.attention['medium'] = fuzz.gaussmf(self.attention.universe, 5, 2.3 )
    self.attention['concentrated'] = fuzz.trimf(self.attention.universe, [6, 10, 10])

    self.gaze.view()
    self.attention.view()
    
    rule1 = ctrl.Rule(self.gaze['rare'] | self.posture['poor'], self.attention['distracted'])
    rule2 = ctrl.Rule(self.gaze['neutral'], self.attention['medium'])
    rule3 = ctrl.Rule(self.gaze['frequent'] | self.posture['good'], self.attention['concentrated'])


    #rule1.view()
    

    adp_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

    adp = ctrl.ControlSystemSimulation(adp_ctrl)


    adp.input['self.gaze'] = 1
    adp.input['self.posture'] = 1

    adp.compute()

    print adp.output['self.attention']


    self.attention.view(sim=adp)


    raw_input()







if __name__=="__main__":
    
    #fz = FuzzyControl()
    fz = Adaptive()











































