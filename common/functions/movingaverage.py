"""
Here are store all the function for the filter
"""


def moving_average(data, width):
        """
        Make a convolution using numpy convolution on mode valid. Therfore, the return value is a numpy array as a size of size(data)-width +1.
        """
	Y = np.ones(width)
        Z = np.convolve(data,Y,mode = "valid")
        return Z



def filter(sweep,width,power,width2):
	"""
        This function apply the filter described below. The return array size is ( size(sweep)- 2 * (width +1) - swidth +1 .
        This function detects the pic. The working principle is the following :
                                                         _
                       _            |---- (step1)^2 -- _| |_ ---(step2)--|
	--(sweep)->  _| |_ -(step1)-|       _                           (-) ----> result
                                    |-----_| |_ --(step3)-- (step3)^2 ---|
		First Part          |              Second Part           |
	The width in argument is the one of the gate function
	"""
        size_sweep = np.size(sweep);
	step1 = moving_average(sweep,width)/width
        step3 = moving_average(step1,width)/width
        step1_carre = np.square(step1)
        step2 = moving_average(step1_carre,width)/width
        step3_carre = np.square(step3)
        #D = np.diff(sweep)
	result = step2 - step3_carre    #(D[width-1:size_sweep-width+1] * (step2 - step3))
	#result = result ** power
	return result  # moving_average(result,width2)


