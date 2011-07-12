
"""
@uthor : Romain Vincent
This file is the one that gather all the files needed for the postprocessing of the data
"""

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
