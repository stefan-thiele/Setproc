"""
Here are store all the function for data processing
"""

def pic_detect(sweep,width):
	"""This function detects the pic. The working principle is the following :
                                                         _
                       _            |---- (step1)^2 -- _| |_ ---(step2)--|
	--(sweep)->  _| |_ -(step1)-|       _                           (-) ----> result
                                    |-----_| |_ --(step3)-- (step3)^2 ---|

	The width in argument is the one of the gate function
	"""
	type(sweep)
	si_sweep = size(sweep)
	step1 = []
	step1carre = []
	result = []
	iter_nbr = 0

	step1_tmp = movingaverage(sweep, width, data_is_list = None, avoid_fp_drift = False)
	for i in step1_tmp :
		step1.append(i)
		step1carre.append(i**2)
	
	step2_temp = movingaverage(step1carre, width, data_is_list = None, avoid_fp_drift = False)
	step3_tmp = movingaverage(step1, width, data_is_list = None, avoid_fp_drift = False)

	for j in step3_tmp :
		result.append(step2_temp.next() - j**2)
		

	return result



def old_pic_detect(sweep,width):
	"""This function detects the pic. The working principle is the following :
                                                         _
                       _            |---- (step1)^2 -- _| |_ ---(step2)--|
	--(sweep)->  _| |_ -(step1)-|       _                           (-) ----> result
                                    |-----_| |_ --(step3)-- (step3)^2 ---|

	The width in argument is the one of the gate function
	"""
	step1 = []
	step2 = []
	step3 = []
	result = array([])

	for i in range(len(sweep)):
		if i >= width-1 :
			step1.append(mean(sweep[(i+1-width):i+1]))


	for i in range(len(step1)):
		step1 = array(step1)
		if i >= (width-1):
			step2.append(mean(step1[(i+1-width):i+1]**2))


	for i in range(len(step1)):
		if i >= width-1 :
			step3.append(mean(step1[(i+1-width):i+1]))

	result = array(step2) - (array(step3))**2
	
	return result.tolist()

def old_pic_detect_2(sweep,width):
	"""This function detects the pic. The working principle is the following :
                                                         _
                       _            |---- (step1)^2 -- _| |_ ---(step2)--|
	--(sweep)->  _| |_ -(step1)-|       _                           (-) ----> result
                                    |-----_| |_ --(step3)-- (step3)^2 ---|

	The width in argument is the one of the gate function
	"""
	step1 = []
	step2 = []
	step3 = []
	result = array([]) 
	si_sweep = size(sweep)

	for i in range(len(sweep)):
		if i >= width-1 :
			step1.append(mean(sweep[(i+1-width):i+1]))


	for i in range(len(step1)):
		step1 = array(step1)
		if i >= (width-1):
			step2.append(mean(step1[(i+1-width):i+1]**2))


	for i in range(len(step1)):
		if i >= width-1 :
			step3.append(mean(step1[(i+1-width):i+1]))

	diff_sweep = diff(sweep[width/2 +1 :si_sweep - width/2])
	
	result = diff_sweep * (array(step2) - (array(step3))**2 )
	
	return result.tolist()



def pic_detect_2(sweep,width):
	"""This function detects the pic. The working principle is the following :
                                                         _
                       _            |---- (step1)^2 -- _| |_ ---(step2)--|
	--(sweep)->  _| |_ -(step1)-|       _                           (-) ----> result
                                    |-----_| |_ --(step3)-- (step3)^2 ---|

	The width in argument is the one of the gate function
	"""
	type(sweep)
	si_sweep = size(sweep)
	step1 = []
	step1carre = []
	result = []
	iter_nbr = 0

	step1_tmp = movingaverage(sweep, width, data_is_list = None, avoid_fp_drift = False)
	for i in step1_tmp :
		step1.append(i)
		step1carre.append(i**2)
	
	step2_temp = movingaverage(step1carre, width, data_is_list = None, avoid_fp_drift = False)
	step3_tmp = movingaverage(step1, width, data_is_list = None, avoid_fp_drift = False)

	for j in step3_tmp :
		result.append(step2_temp.next() - j**2)
		
	diff_sweep = diff(sweep[width/2 +1 :si_sweep - width/2])
	
	for i in range(size(result)) :
		result[i] = result[i] * diff_sweep[i]

	return result

