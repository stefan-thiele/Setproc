
def getposcolumn(data,string):
	"""
	This function allows to obtain the column number in a json file sweep given the name of the input
	"""
	result = 0
	for i in range(size(data["measures"][0]["columns"])) :
		if(data["measures"][0]["columns"][i] == string) :
			result = i+1
	return result

######################################


######################################


######################################



#######################################
def plotdata(data, x, y):
	"""
	This function plot a 2D curve given a json data and the column number of x and y axis.
	"""
	plot(colarray(data, x, 0), colarray(data, y, 0))
	return True


########################################
def getinputs(data):
	"""
	This function give the inputs used for a measurement given the corresponding json file.
	"""
	inputs = data["inputs"]
	result = []
	for x in inputs:
		result.append(str(data["inputs"][x]["name"]).replace("u", ""))
	return result

########################################
def getoutputs(data):
	"""
	This function give the outputs used for a measurement given the corresponding json file.
	"""

	inputs = data["outputs"]
	result = []
	for x in inputs:
		result.append(str(data["outputs"][x]["name"]).replace("u", ""))
	return result

########################################
def getcolumns(data, col_num, sweep_num):
	"""
	This function allows to access to one column of a json file sweep given the sweep and the column numbers.
	"""
	result = []
	for i in range(sweep_num):
		result.append(colarray(data["measures"][i]["data"],col_num , 0))
	return result

#######################################
def extract_pop(histo,nbr_pic,width) :
	result = []
	X = ginput(nbr_pic)
	size_hist = size(histo[1])
	Xmin = histo[1][0]
	Xmax = histo[1][-1]
	step = 1.0 * abs(Xmax-Xmin)/size_hist
	for i in range(nbr_pic) :
		center = floor(abs(X[i][0] - Xmin)/step)
		result.append(sum(histo[0][center-width:center+width]))
	return [result,1.0*array(result)/sum(result)]


#######################################
def plot_int(data):
	"""
	Given a array of data in the form [V, dI/dV], it comutes and plot the integral. This fonction can be used together with plot_profile
	to evaluate the gamma parameters of the sample.
	"""
	result = []
	for i in range(len(data[0])+1):
		if i > 0 :
			result.append(integrate.simps(data[0][0:i], data[1][0:i]))
	f=figure()
	result.reverse()
	vd =  array(data[1])
	vd = vd.tolist()
	vd.reverse()
	plot(vd, result)
	x= ginput()
	for i in range(len(result)) :
		result[i] = result[i] -x[0][1]
	f.clear()
	plot(vd, result)
	return result


######################################

#######################################


########################################
def merge_GB(GB_array) :
	GB_temp = deepcopy(GB_array[0])
	GB_nbr = size(GB_array)
	GB_order = range(1,GB_nbr,1)
	if( GB_nbr >1 ) :
		for i in GB_order :
			whole_size = size(GB_array[i]["data"])
			sweep_size = size(GB_array[i]["data"][1])
			current_array_size = whole_size/sweep_size
			for j in range(current_array_size) :
				GB_temp["data"].append(GB_array[i]["data"][j])
				GB_temp["date"].append(GB_array[i]["date"][j])
	GB_temp["sweep_number"] = len(GB_temp["data"])

	return GB_temp


