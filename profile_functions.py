def max_local(X,Y,span) :
	result_max = [[],[]]
	result_min = [[],[]]
	size_array = size(Y)
	#max local
	maxi = np.max
	max_arg = np.argmax
	temp_max = [0,-inf]
	#min local
	mini = np.min
	mini_arg = np.argmin
	temp_min = [0,inf]

	span = span -1
	span_m = span
	for i in xrange(0,size_array):
		if (i + span_m > size_array ) :
			span_m = span_m - 1
		Vec = Y[i:i+span_m]
		max_loc = maxi(Vec)
		max_loc_arg = max_arg(Vec)
		min_loc = mini(Vec)
		min_loc_arg = mini_arg(Vec)

		#max local
		if temp_max[0] < i-span and temp_max[0] != -inf :
			result_max[0].append(X[temp_max[0]])
			result_max[1].append(temp_max[1])
			temp_max[0] = i
			temp_max[1] = -inf
		if max_loc > temp_max[1] :
			temp_max[0] = max_loc_arg + i
			temp_max[1] = max_loc

		#min local
		if temp_min[0] < i-span and temp_min[0] != inf :
			result_min[0].append(X[temp_min[0]])
			result_min[1].append(temp_min[1])
			temp_min[0] = i
			temp_min[1] = inf
		if min_loc < temp_min[1] :
			temp_min[0] = min_loc_arg + i
			temp_min[1] = min_loc

	return result_min ,result_max
			
