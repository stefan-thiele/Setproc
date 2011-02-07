
"""
@uthor : Romain Vincent
This file is the one that gather all the files needed for the postprocessing of the data
"""
#import enthought.mayavi.mlab as emm
import simplejson as json
import matplotlib.lines as mpllines
import pickle
import cPickle
from matplotlib.colors import LogNorm
from scipy import constants as pc
from scipy import*
from numpy import*
from pylab import *
from matplotlib.colors import LinearSegmentedColormap
# import ipy_profile_sh
execfile("/home/romain/setproc/functions.py")
execfile("/home/romain/setproc/openmeasures.py")
execfile("/home/romain/setproc/map.py")
execfile("/home/romain/setproc/polar.py")
execfile("/home/romain/setproc/g_b.py")
execfile("/home/romain/setproc/HysteresisVg.py")
execfile("/home/romain/setproc/dataprocess.py")
