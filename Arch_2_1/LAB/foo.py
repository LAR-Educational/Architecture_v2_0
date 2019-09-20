
# ----- System imports -----

import sys
import time
import cv2
import csv
import os
import pickle
import random
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














#def main():

#act = ct.Activity("NOVA")



act = ct.load_Activity("./Activities/Par_Impar2/activity.data")

act.print_Attributes()

#ct.create_Activity(act)





   








