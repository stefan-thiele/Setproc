import numpy as np
cimport numpy as np

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t


def extract_stat( np.ndarray[DTYPE_t, ndim =1] sweep, double seuil1, double seuil2, int span) :
	#hold final min value
	cdef float in_min = 0
	cdef int in_min_arg = -1
	cdef int in_min_write = 1 #1 = True, 0 = False
	#hold the temp min value
	cdef float temp_min = 0
	cdef int temp_min_arg = -1
	# hold the final max value
	cdef float in_max = 0
	cdef int in_max_arg = -1
	cdef in_max_write = 1 #1 =True, O =False
	#hold the temp max value
	cdef float temp_max = 0
	cdef int temp_max_arg = -1
	cdef int sweep_size = sweep.shape[0]
	cdef int i #this is for looping

	for i in range(sweep_size) :
		value = sweep[i]
		#check if we are below the threshold, if yes, next point
		if abs(value) < seuil1 :
			if in_max_write == 0 :
				in_max_write = 1
				if temp_max < in_max :
					temp_max = in_max
					temp_max_arg = in_max_arg
			if in_min_write == 0 :
				in_min_write = 1
				if temp_min > in_min :
					temp_min = in_min
					temp_min_arg = in_min_arg
			continue
		#if we are in beetween the two threshold
		if abs(value) > seuil1 and abs(value) < seuil2 :
			if value < in_min and in_min_write == 1 :
				in_min = value
				in_min_arg = i
			if value > in_max and in_max_write == 1:
				in_max = value
				in_max_arg = i
		#if we are above the threshold
		if abs(value) > seuil2 :
			#Make sure than min and max cannot be accessed before going back below seuil1
			if value < - seuil2 :
				in_min_write = 0
				if(in_min_arg + span > i) :
					in_min = 0
					in_min_arg = -1
			if value > seuil2 :
				in_max_write = 0
				if(in_max_arg + span > i) :
					in_max = 0
					in_max_arg = -1
	
	if in_min > temp_min :
		in_min = temp_min
		in_min_arg = temp_min_arg
	
	if in_max < temp_max :
		in_max = temp_min
		in_max_arg = temp_max_arg
	
	return in_min, in_min_arg, in_max, in_max_arg		
	
















