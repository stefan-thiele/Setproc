folder = "/home/romain/setproc/"
sys.path.append(folder+"lib/")

import numpy as np
from copy import deepcopy
import simplejson as json
import moving_average as mva
import extract_stat as exst
import cPickle   #used to save the data
import time



execfile(folder+"Stat_point.py") #Load the Stat_point object used in sweep_set_open and cycle_process
execfile(folder+"filter.py") #contain the filer detecting the jump
execfile(folder+"functions.py")
execfile(folder+"openmeasures.py")
execfile(folder+"g_b.py")
execfile(folder+"cycle_process.py")


"""
@uthor : Romain Vincent
This file is the one that gather all the files needed for the postprocessing of the data

folder = "/home/romain/setproc/"


import enthought.mayavi.mlab as emm
import simplejson as json
import matplotlib.lines as mpllines
import pickle
import cPickle
import enthought.mayavi.mlab as mayavi
import os 

from matplotlib.colors import LogNorm
from scipy import constants as pc
from scipy import*
from numpy import*
from pylab import *
from matplotlib.colors import LinearSegmentedColormap
from copy import deepcopy

#import sys
#sys.path.append(folder+"lib/")
#import dataprocess as dp

# import ipy_profile_sh

execfile(folder+"functions.py")
execfile(folder+"openmeasures.py")
execfile(folder+"map.py")
execfile(folder+"polar.py")
execfile(folder+"g_b.py")
execfile(folder+"HysteresisVg.py")
execfile(folder+"movingaverage.py")
execfile(folder+"dataprocess.py")
execfile(folder+"density_matrix.py")

"""
