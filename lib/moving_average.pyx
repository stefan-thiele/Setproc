import numpy as np
cimport numpy as np

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t


def moving_average_c(np.ndarray[DTYPE_t, ndim =1] f, int w) :
	cdef int size_f = f.shape[0]
	cdef int width = w
	cdef int size_result =  size_f - w + 1
	cdef int s_from , s_to
	cdef int i,j #This integer will be used to loop
	cdef np.ndarray[DTYPE_t, ndim = 1] result = np.zeros(size_result, dtype = DTYPE)
	cdef DTYPE_t value
	
	for i in range(size_result) :
		s_to = i + width
		s_from = i
		if i == 0:
			value = 0
			for j in range(s_from,s_to):
				value += f[j]
			result[i] = value / width
		else :
			value = value - f[i-1] +f[s_to-1]
			result[i] = value / width

	return result
		
