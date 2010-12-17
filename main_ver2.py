
"""
@uthor : Romain Vincent
This file is the one that gather all the files needed for the postprocessing of the data
"""
#import enthought.mayavi.mlab as emm
import simplejson as json
import matplotlib.lines as mpllines
import pickle
import cPickle
from scipy import constants as pc
from scipy import*
from numpy import*
from pylab import *
from matplotlib.colors import LinearSegmentedColormap
# import ipy_profile_sh
execfile("/home/romain/setproc/functions_ver2.py")
#execfile("/home/dilu-d103/NanoQtScripts/RomainV/Python/map.py")
#execfile("/home/romain/setproc/polar_ver2.py")
execfile("/home/romain/setproc/g_b.py")
execfile("/home/romain/setproc/dataprocess.py")
execfile("/home/romain/setproc/openmeasures.py")
