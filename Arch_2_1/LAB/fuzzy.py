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
  



def adap():


    # New Antecedent/Consequent objects hold universe variables and membership
    # functions
    quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
    service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
    tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

    # Auto-membership function population is possible with .automf(3, 5, or 7)
    quality.automf(3)
    service.automf(3)

    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
    tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
    tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])


    tip.view()
    #time.sleep(5)
    













if __name__=="__main__":
    adap()






































