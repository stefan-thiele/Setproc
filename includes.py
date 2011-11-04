folder = "/home/romain/setproc/"
import sys
sys.path.append(folder+"lib/")

import numpy as np
from copy import deepcopy
import simplejson as json
import moving_average as mva
import extract_stat as exst
import cPickle   #used to save the data
import time
import os


execfile(folder+"Stat_point.py") #Load the Stat_point object used in sweep_set_open and cycle_process
execfile(folder+"filter.py") #contain the filer detecting the jump
execfile(folder+"functions.py")
execfile(folder+"openmeasures.py")
execfile(folder+"map.py")
execfile(folder+"g_b.py")
execfile(folder+"cycle_process.py")
