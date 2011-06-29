from pylab import size
import numpy as np
cimport numpy as np


"""
@@@@@@@@@@@@@@@@@@@@@@@@@
This file contains all the functions needed for the different classes
@@@@@@@@@@@@@@@@@@@@@@@@@
"""

cdef extern from "numpy/arrayobject.h":
	int import_array "_import_array" () except -1
import_array() 

cdef inline float f_x(double i):
	return 1/(i*i)

def function(double i) :
	return f_x(i)

cdef voir(object) :
	

def max_local(np.ndarray[np.float64_t, ndim = 1] X, np.ndarray[np.float64_t, ndim = 1] Y, int span):
	cdef int size_array = size(Y)
	cdef int size_X = size(X)
	cdef int i
	cdef int pointer_max = 0
	cdef int pointer_min = 0
	cdef int span_m = span - 1
	cdef long max_local
	cdef long min_local
	cdef int arg_min_loc
	cdef int arg_max_loc
	cdef resultX_min = np.zeros(size_X)
	cdef resultY_min = np.zeros(size_X)
	cdef resultX_max = np.zeros(size_X)
	cdef resultY_max = np.zeros(size_X)
	cdef temp_max = [0.,0]
	cdef temp_min = [0.,0]

	#used funtions
	maxi = np.max
	mini = np.min
	max_arg = np.argmax
	min_arg = np.argmin

	for i in xrange(0,size_array):
		if (i + span_m > size_array ) :
			span_m = span_m - 1
		Vect = Y[i:i+span_m]
		max_loc = np.max(Vect)
		arg_max_loc = np.argmax(Vect)
		min_loc = maxi(Vect)
		arg_min_loc = min_arg(Vect)

		#max local
		if temp_max[0] < i-span and temp_max[0] != 0 :
			resultX_max[pointer_max] = temp_max[0]
			resultY_max[pointer_max] = temp_max[1]
			pointer_max = pointer_max + 1
			temp_max[0] = i
			temp_max[1] = 0
		if max_loc > temp_max[1] :
			temp_max[0] = i+arg_max_loc
			temp_max[1] = max_loc
	
		#min local
		if temp_min[0] < i-span and temp_min[0] != 0 :
			resultX_min[pointer_min] = temp_min[0]
			resultY_min[pointer_min] = temp_min[1]
			pointer_min = pointer_min + 1
			temp_min[0] = i
			temp_min[1] = 0
		if max_loc < temp_min[1] :
			temp_min[0] = i+arg_min_loc
			temp_min[1] = min_loc
	return [resultX_min[0:pointer_min],resultY_min[0:pointer_min]], [resultX_max[0:pointer_max],resultY_max[0:pointer_max]]





