from pylab import size
import numpy as np
cimport numpy as np

cdef extern from "numpy/arrayobject.h":
	int import_array "_import_array" () except -1
import_array() 




def sum(np.ndarray[np.float64_t, ndim = 1] data) :
	cdef int i
	cdef float s = 0
	for i in xrange(np.size(data)) :
		s+= data[i]
	return s

def mean(np.ndarray[np.float64_t, ndim = 1] data) :
	cdef float si_data = np.size(data)
	result = sum(data)/si_data
	return result

def moving_average(np.ndarray[np.float64_t, ndim = 1] A, int width):
	cdef int si_data = np.size(A)
	cdef int i
	cdef int sub_size = si_data - width +1
	cdef float span = width
	cdef np.ndarray[np.int32_t , ndim=1] iter_num
	cdef np.ndarray[np.float64_t, ndim =1 ] result = np.zeros(sub_size)
	iter_num = np.arange(0 , (si_data-width +1))
	for i in iter_num :
		result[i] = mean(A[i:i+width])
	return result


def old_moving_average(np.ndarray[np.float64_t, ndim =1] data, int width) :
	cdef int si_data = np.size(data)
	cdef int i
	cdef np.ndarray[np.float64_t, ndim =1] result = np.zeros(si_data-width+1)
	iter_num = xrange(si_data-width+1)
	for i in iter_num :
		result[i] = np.mean(data[i:i+width])
	return result

def fast_pic_detect(np.ndarray[np.float64_t, ndim = 1] data, int width) :
	cdef int si_data = np.size(data)
	cdef np.ndarray[np.float_t, ndim =1] step1
	cdef np.ndarray[np.float_t, ndim = 1] result
	cdef np.ndarray[np.float_t, ndim = 1] diff_sweep = np.zeros(si_data - (width +1))
	step1 = moving_average(data,width)
	diff_sweep = np.diff(data[width/2 +1 :si_data - width/2])
	result =  - np.power(moving_average(step1,width),[2]) + moving_average(np.power(step1,[2]),width)
	return diff_sweep * result
