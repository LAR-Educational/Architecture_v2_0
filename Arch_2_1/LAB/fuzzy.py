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
        




class StatesFuzzyControl:

    def __init__(self,  max_gaze=10, #max_posture=10, 
                        max_words=10, max_emotions=10,
                        max_success=1, max_tta = 30,
                        auto = False, print_flag=False):

        self.print_flag = print_flag

        # New Antecedent/Consequent objects hold universe variables and membership
        # functions
        #self.posture = ctrl.Antecedent(np.arange(0, max_posture+1, 1), 'Posture')
        self.posture = ctrl.Antecedent(np.arange(0, 11, 1), 'Posture')
        self.gaze = ctrl.Antecedent(np.arange(0, max_gaze+1, 1), 'Gaze')
        self.attention = ctrl.Consequent(np.arange(0, 11, 1), 'Attention')

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        self.posture.automf(3)
        #self.gaze.automf(5)

        if auto:
            self.gaze.automf(3, names=["rare", "neutral", "frequent"])

        else:
            inf = max_gaze/3
            av = max_gaze/2
            sup = max_gaze*2/3

            self.gaze['rare'] = fuzz.trimf(self.gaze.universe, [0, 0, inf+1])
            self.gaze['neutral'] = fuzz.trimf(self.gaze.universe, [inf-1, av, sup+1])
            self.gaze['frequent'] = fuzz.trimf(self.gaze.universe, [sup-1, max_gaze, max_gaze])


        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        self.attention['distracted'] = fuzz.trimf(self.attention.universe, [0, 0, 4])
        self.attention['medium'] = fuzz.trimf(self.attention.universe, [2, 5, 8])
        self.attention['concentrated'] = fuzz.trimf(self.attention.universe, [6, 10, 10])

        #self.gaze.view()
        #self.attention.view()
        #print rules
        
        att_rule1 = ctrl.Rule(self.gaze['frequent'], self.attention['distracted'])
        att_rule2 = ctrl.Rule(self.gaze['neutral'], self.attention['medium'])
        att_rule3 = ctrl.Rule(self.gaze['rare'], self.attention['concentrated'])

        att_ctrl_sys = ctrl.ControlSystem([att_rule1, att_rule2, att_rule3])

        self.att_ctrl = ctrl.ControlSystemSimulation(att_ctrl_sys)

        #self.att_ctrl.


        #------------------ COMMUNICATION

        # New Antecedent/Consequent objects hold universe variables and membership
        # functions

        self.emotions = ctrl.Antecedent(np.arange(0, max_emotions, 1), 'Emotions')
        self.words = ctrl.Antecedent(np.arange(0, max_words+1, 1), 'Words')
        self.communication = ctrl.Consequent(np.arange(0, 11, 1), 'Communication')

       
        if auto:
            self.emotions.automf(5, names=["excited", "happy", "neutral", "sad", "frustrated"])
            self.words.automf(3, names=["contained", "regular", "talker"])
            self.communication.automf(3, names=["introverted", "neutral", "extroverted"])
        
        else:
        # Auto-membership function population is possible with .automf(3, 5, or 7)
            inf = max_emotions/3
            mid = max_emotions/2
            sup = max_emotions*2/3
            
            self.emotions['excited'] = fuzz.trimf(self.emotions.universe, [0, inf/2, inf])
            self.emotions['happy'] = fuzz.trimf(self.emotions.universe, [inf/2, inf, mid] )
            self.emotions['neutral'] = fuzz.trimf(self.emotions.universe, [inf, mid, sup])
            self.emotions['sad'] = fuzz.trimf(self.emotions.universe, [inf, sup/2, sup])
            self.emotions['frustrated'] = fuzz.trimf(self.emotions.universe, [sup/2, sup,max_emotions ])
        

            inf = (max_words/3)-1
            av = max_words/2
            sup = int(max_words*2/3)
            self.words['contained'] = fuzz.trimf(self.words.universe, [0, 1, 2] )
            self.words['regular'] = fuzz.trimf(self.words.universe, [1, 2, 3])
            self.words['talker'] = fuzz.trimf(self.words.universe, [3, 4, 5])

            # Custom membership functions can be built interactively with a familiar,
            # Pythonic API
            self.communication['introverted']   = fuzz.trimf(self.communication.universe,  [0, 2, 4] )
            self.communication['neutral']       =  fuzz.trimf(self.communication.universe, [2, 5, 8] )
            self.communication['extroverted']   = fuzz.trimf(self.communication.universe,  [6, 8, 10])

        rules = []

        rules.append( ctrl.Rule(self.emotions['frustrated'] , self.communication['neutral']) )
        rules.append( ctrl.Rule(self.emotions['frustrated'] & self.words['talker'] , self.communication['neutral']) )
        rules.append( ctrl.Rule(self.emotions['sad'] & self.words['contained'] , self.communication['introverted']) )
        rules.append( ctrl.Rule(self.emotions['neutral'] , self.communication['neutral']) )
        rules.append( ctrl.Rule(self.emotions['happy'] & self.words['regular'] , self.communication['extroverted']) )
        # rules.append( ctrl.Rule(self.emotions['excited'] | self.words['talker'] , self.communication['extroverted']) )
        rules.append( ctrl.Rule( self.words['talker'] , self.communication['extroverted']) )
        

        com_ctrl_sys = ctrl.ControlSystem(rules)

        self.com_ctrl = ctrl.ControlSystemSimulation(com_ctrl_sys)


        #self.emotions.view()
        #self.words.view()
        #self.communication.view()


        #return 

        #------------------ TASK

         # New Antecedent/Consequent objects hold universe variables and membership
        # functions
        self.success = ctrl.Antecedent(np.arange(0, 11, 1), 'Success')
        self.ans_time = ctrl.Antecedent(np.arange(0, max_tta+1, 1), 'Answer_Time')
        self.task = ctrl.Consequent(np.arange(0, 11, 1), 'Task')



        # Auto-membership function population is possible with .automf(3, 5, or 7)
        if auto:
            self.success.automf(2, names=["low","high"])
            self.ans_time.automf(3,names=["Slow", "Average", "Fast" ])
            self.task.automf(3, names=["inefficient", "regular", "efficient"])
        
        # Extremes for lower case (1.4) and higher (4.2) = 2.75
        
        else:
            self.success['low'] = fuzz.trimf(self.success.universe, [0, 1, 3] )
            #self.success['average'] = fuzz.trimf(self.success.universe, [4, 6, 7] )
            self.success['high'] = fuzz.trimf(self.success.universe, [7, 10, 10] )

            #hahahahahah
            # self.success.automf(2, an)

            low = max_tta/3.0
            mid = 0.67 * max_tta
            high = max_tta


            self.ans_time['Fast']       = fuzz.trimf(self.ans_time.universe,  [0, low/2.0, low] )
            self.ans_time['Average']    = fuzz.trimf(self.ans_time.universe,  [low, mid, high] )
            self.ans_time['Slow']       = fuzz.trimf(self.ans_time.universe,  [ mid , high, max_tta])
            
        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
            self.task['inefficient']= fuzz.trimf(self.task.universe, [0, 2, 4] )
            self.task['regular']    = fuzz.trimf(self.task.universe, [2, 5, 8] )
            self.task['efficient']  = fuzz.trimf(self.task.universe, [6, 8, 10] )


        rules = []

        #print rules

        rules.append( ctrl.Rule(self.success['high'], self.task['efficient']) )
        rules.append( ctrl.Rule(self.success['high'] & self.ans_time['Fast'] , self.task['efficient']) )
        rules.append( ctrl.Rule(self.success['high'] & self.ans_time['Average'] , self.task['efficient']) )
        rules.append( ctrl.Rule(self.success['high'] & self.ans_time['Slow'], self.task['regular']) )
        rules.append( ctrl.Rule(self.success['low'] & self.ans_time['Slow'], self.task['inefficient']) )
        rules.append( ctrl.Rule(self.success['low'] & self.ans_time['Average'], self.task['inefficient']) )
        rules.append( ctrl.Rule(self.success['low'] & self.ans_time['Fast'], self.task['inefficient']) )
            
        #rules.append( ctrl.Rule(self.success['high'], self.task['efficient']) )

        # rules.append( ctrl.Rule(self.success['high'] , self.task['efficient']) )
        # rules.append( ctrl.Rule(self.success['average'] & self.ans_time['Slow'], self.task['regular']) )
        # rules.append( ctrl.Rule(self.success['low'] & self.ans_time['Slow'], self.task['inefficient']) )
        # rules.append( ctrl.Rule(self.success['low'] | self.ans_time['Average'], self.task['inefficient']) )
        # rules.append( ctrl.Rule(self.success['low'] & self.ans_time['Fast'], self.task['inefficient']) )
        #print rules
        # rules.append( ctrl.Rule(self.success['high'] & self.ans_time['Fast'] , self.task['efficient']) )
        # rules.append( ctrl.Rule(self.success['high'] & self.ans_time['Average'] , self.task['efficient']) )
        # rules.append( ctrl.Rule(self.success['high'] & self.ans_time['Slow'] , self.task['efficient']) )


        # rules.append( ctrl.Rule(self.success['average'] & self.ans_time['Fast'] , self.task['efficient']) )
        # rules.append( ctrl.Rule(self.success['average'] & self.ans_time['Average'] , self.task['regular']) )
        # rules.append( ctrl.Rule(self.success['average'] & self.ans_time['Slow'] , self.task['regular']) )

        # rules.append( ctrl.Rule(self.success['low'] & self.ans_time['Fast'] , self.task['inefficient']) )
        # rules.append( ctrl.Rule(self.success['low'] & self.ans_time['Average'] , self.task['inefficient']) )
        # rules.append( ctrl.Rule(self.success['low'] & self.ans_time['Slow'] , self.task['inefficient']) )


        # rules.append( ctrl.Rule(self.success['high'] ,      self.task['efficient']) )
        # rules.append( ctrl.Rule(self.success['average'],    self.task['regular']) )
        # rules.append( ctrl.Rule(self.success['low'] ,       self.task['inefficient']) )
       

        # rules.append( ctrl.Rule(self.success['good'] ,      self.task['efficient']) )
        # # rules.append( ctrl.Rule(self.success['average'],    self.task['regular']) )
        # rules.append( ctrl.Rule(self.success['poor'] ,       self.task['inefficient']) )
        
        #print rules
        self.success.view()
         

        task_ctrl_sys = ctrl.ControlSystem(rules)

        self.task_ctrl = ctrl.ControlSystemSimulation(task_ctrl_sys)

        if print_flag:
            self.gaze.view()
            self.posture.view()
            self.attention.view()

            self.emotions.view()
            self.words.view()
            self.communication.view()


            self.success.view()
            self.ans_time.view()
            self.task.view()

        # #raw_input()

        # time.sleep(1)

        # self.task_ctrl.input['Success'] = 90
        # self.task_ctrl.input['Answer Time'] = 1

        # self.task_ctrl.compute()

        # print self.task_ctrl.output['Task']


        # self.task.view(sim=self.task_ctrl)


        #raw_input()
        #return 

    def compute_states(self, read_values):

        # --- ALPHA --- 
        self.att_ctrl.input['Gaze'] = read_values.deviations
        #self.att_ctrl.input['Posture'] = read_values.deviations

        self.att_ctrl.compute()

        alpha = self.att_ctrl.output['Attention']

        if self.print_flag:
            self.attention.view(sim=self.att_ctrl)


        # --- BETA --- 
        self.com_ctrl.input['Emotions'] = read_values.emotionCount
        self.com_ctrl.input['Words'] = read_values.numberWord

        self.com_ctrl.compute()

        beta = self.com_ctrl.output['Communication']

        if self.print_flag:
            self.communication.view(sim=self.com_ctrl)


        # --- GAMA --- 
        self.task_ctrl.input['Answer_Time'] = read_values.time2ans
        self.task_ctrl.input['Success'] = read_values.sucRate

        self.task_ctrl.compute()

        gama = self.task_ctrl.output['Task']

        if self.print_flag:
            self.task.view(sim=self.task_ctrl)


        return alpha, beta, gama




class Adaptive():

    def __init__(self, print_flag=False ):

        self.print_flag = print_flag

        # New Antecedent/Consequent objects hold universe variables and membership
        # functions
        self.attention = ctrl.Antecedent(np.arange(0, 11, 1), 'Attention')
        
        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        # self.attention['distracted'] = fuzz.trimf(self.attention.universe, [0, 0, 4])
        # self.attention['medium'] = fuzz.trimf(self.attention.universe, [2, 5, 8] )
        # self.attention['concentrated'] = fuzz.trimf(self.attention.universe, [6, 10, 10])

        self.attention.automf(3, names=['distracted','medium', 'concentrated' ])


        #------------------ COMMUNICATION
        self.communication = ctrl.Antecedent(np.arange(0, 11, 1), 'Communication')
      
        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        # self.communication['introverted'] = fuzz.trimf(self.attention.universe, [0, 2, 4])
        # self.communication['neutral'] = fuzz.trimf(self.attention.universe,  [2, 5, 8] )
        # self.communication['extroverted'] = fuzz.trimf(self.attention.universe,  [6, 8, 10])
        self.communication.automf(3, names= ["introverted", "neutral","extroverted" ] )

        #------------------ TASK

         # New Antecedent/Consequent objects hold universe variables and membership
        # functions
        self.task = ctrl.Antecedent(np.arange(0, 11, 1), 'Task')
        
        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        # self.task['inefficient']= fuzz.trimf(self.attention.universe, [0, 2, 4])
        # self.task['regular']    = fuzz.trimf(self.attention.universe, [2, 5, 8] )
        # self.task['efficient']  = fuzz.trimf(self.attention.universe, [6, 8, 10])

        self.task.automf(3, names=["inefficient", "regular", "efficient"] )


        # ADAPTATION

        self.adaptation = ctrl.Consequent(np.arange(1, 5, 1), 'Adaptation')

        self.adaptation.automf(5)


        #self.adaptation.view()


        rules = []

        #print rules

        rules.append( ctrl.Rule(self.task['efficient'] , self.adaptation['good']) )
        rules.append( ctrl.Rule(self.attention['concentrated'] & self.communication['extroverted']  & self.task['efficient'] , self.adaptation['good']) )
        rules.append( ctrl.Rule(self.attention['concentrated'] & self.task['efficient'] , self.adaptation['decent']) )
        rules.append( ctrl.Rule(self.attention['medium'] & self.communication['neutral']  & self.task['regular'] , self.adaptation['average']) )
        rules.append( ctrl.Rule(self.attention['distracted'] & self.task['efficient'] , self.adaptation['decent']) )
        rules.append( ctrl.Rule(self.attention['distracted'] & self.communication['introverted']  & self.task['inefficient'] , self.adaptation['poor']) )
        #rules.append( ctrl.Rule(self.success['low'] | self.ans_time['Slow'], self.task['inefficient']) )


        if self.print_flag:
            self.attention.view()
            self.communication.view()
            self.task.view()


        ctrl_sys = ctrl.ControlSystem(rules)

        self.adp_func = ctrl.ControlSystemSimulation(ctrl_sys)




    # def compute_fvalue(self, values):
        
    #     self.adp_func.input['Attention'] = values[0]
    #     self.adp_func.input['Communication'] = values[1]
    #     self.adp_func.input['Task'] = values[2]


    #     self.adp_func.compute()



    #     if print_flag:
    #         print "VALUE", self.adp_func.output['Adaptation']
    #         self.adaptation.view(sim=self.adp_func)

    #     #raw_input()
    #     return










    def compute_fvalue(self, measures):

        self.adp_func.input['Attention'] = measures[0]
        self.adp_func.input['Communication'] = measures[1]
        self.adp_func.input['Task'] = measures[2]


        self.adp_func.compute()


        if self.print_flag:
            print "Value", self.adp_func.output['Adaptation']

            self.adaptation.view(sim=self.adp_func)

        return self.adp_func.output['Adaptation']






# def exemple():


#     # New Antecedent/Consequent objects hold universe variables and membership
#     # functions
#     quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
#     service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
#     tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

#     # Auto-membership function population is possible with .automf(3, 5, or 7)
#     quality.automf(3)
#     service.automf(5)

#     # Custom membership functions can be built interactively with a familiar,
#     # Pythonic API
#     tip['low'] = fuzz.trimf(tip.universe, [0, 5, 20])
#     tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
#     tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])


#     tip.view()
    
    
    
#     raw_input()





# def adap():


#     # New Antecedent/Consequent objects hold universe variables and membership
#     # functions
#     self.posture = ctrl.Antecedent(np.arange(0, 11, 1), 'self.posture')
#     self.gaze = ctrl.Antecedent(np.arange(0, 11, 1), 'self.gaze')
#     self.attention = ctrl.Consequent(np.arange(0, 11, 1), 'self.attention')

#     # Auto-membership function population is possible with .automf(3, 5, or 7)
#     self.posture.automf(3)
#     #self.gaze.automf(5)

#     self.gaze['rare'] = fuzz.trimf(self.gaze.universe, [0, 2, 4])
#     self.gaze['neutral'] = fuzz.trimf(self.gaze.universe, [2, 5, 7])
#     self.gaze['frequent'] = fuzz.trimf(self.gaze.universe, [5, 10, 10])
#     #self.gaze[''] = fuzz.trimf(self.gaze.universe, [0, 0, 4])
#     #self.gaze[''] = fuzz.trimf(self.gaze.universe, [0, 0, 4])

#     # Custom membership functions can be built interactively with a familiar,
#     # Pythonic API
#     self.attention['distracted'] = fuzz.trimf(self.attention.universe, [0, 0, 4])
#     self.attention['medium'] = fuzz.gaussmf(self.attention.universe, 5, 2.3 )
#     self.attention['concentrated'] = fuzz.trimf(self.attention.universe, [6, 10, 10])

#     self.gaze.view()
#     self.attention.view()
    
#     rule1 = ctrl.Rule(self.gaze['rare'] | self.posture['poor'], self.attention['distracted'])
#     rule2 = ctrl.Rule(self.gaze['neutral'], self.attention['medium'])
#     rule3 = ctrl.Rule(self.gaze['frequent'] | self.posture['good'], self.attention['concentrated'])


#     #rule1.view()
    

#     adp_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

#     adp = ctrl.ControlSystemSimulation(adp_ctrl)


#     adp.input['self.gaze'] = 1
#     adp.input['self.posture'] = 1

#     adp.compute()

#     print adp.output['self.attention']


#     self.attention.view(sim=adp)


#     raw_input()









if __name__=="__main__":
    # pass
    fz = StatesFuzzyControl( max_gaze=30,
                            max_emotions=400,
                            max_words=5,
                            max_tta=22,
                            auto= True,
                            print_flag=False)

    for a in range(10):

        r = ReadValues(30, 500, 3, 22.2, a)

        # measures =  fz.compute_states(r)
        try:
            print a,  fz.compute_states(r)
            pass
        except:
            print "Problems in ", a 
        #raw_input("Press any button")

    #exit()


    fz = Adaptive(print_flag=False)


    for a in range(1,10):
        for b in range(1,10):
            for c in range(1,10):

                values = [a,b,c]
                try:
                    print a,b,c, "%.2f"%fz.compute_fvalue(values)
                except:
                    print "No good at", values


    time.sleep(5)









































