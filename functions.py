"""
@@@@@@@@@@@@@@@@@@@@@@@@@
This file contains all the functions needed for the different classes
@@@@@@@@@@@@@@@@@@@@@@@@@
"""


"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Flag colormap
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
cdict3 = {'red':  ((0.0, 0.0, 0.0),
                   (0.25,0.5, 0.5),
                   (0.5, 1.0, 1.0),
                   (0.75,1.0, 1.0),
                   (1.0, 1.0, 1.0)),

         'green': ((0.0, 0.0, 0.0),
                   (0.25,0.5, 0.5),
                   (0.5, 1.0, 1.0),
                   (0.75,0.5, 0.5),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 1.0, 1.0),
                   (0.25,1.0, 1.0),
                   (0.5, 1.0, 1.0),
                   (0.75,0.5, 0.5),
                   (1.0, 0.0, 0.0))
        }



cdict2 = {'red':  ((0.0, 0.0, 0.0),
		   (0.125,0.25,0.25),
                   (0.25,0.5, 0.5),
		   (0.375,0.75,0.75),
                   (0.5, 1.0, 1.0),
		   (0.625,1.0,1.0),	
                   (0.75,1.0, 1.0),
		   (0.875,1.0,1.0),
                   (1.0, 1.0, 1.0)),

         'green': ((0.0, 0.0, 0.0),
		   (0.125,0.25,0.25),
                   (0.25,0.5, 0.5),
		   (0.375,0.75,0.75),
                   (0.5, 1.0, 1.0),
		   (0.625,0.75,0.75),
                   (0.75,0.5, 0.5),
		   (0.875,0.25,0.25),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 1.0, 1.0),
		   (0.125,1.0,1.0),
                   (0.25,1.0, 1.0),
		   (0.375,1.0,1.0),
                   (0.5, 0.1, 0.1),
		   (0.625,0.75,0.75),
                   (0.75,0.5, 0.5),
		   (0.875,0.25,0.25),
                   (1.0, 0.0, 0.0))
        }


french = LinearSegmentedColormap('french', cdict3)







"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Opening of the files
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""



class SciData :
	"""
	This class extracts the data from a text file generated using the old scilab procedure. NB : the scilab procedure has to be revised since it inserts a line of zero in the middle of the matrix
	"""
	def __init__(self, filename) :
		temp = loadtxt(filename)
		self.data = extractScilab(temp)





"""
*****************************************************************************************
Functions that handle the formatting of the figure
*****************************************************************************************
"""

def get_json(filename) :
	result =  json.load(open(filename,'r'))
	return  result

def cb_format(cb) :
	"""
	This function formats the colorbar
        """
	cb.ax.set_position([0.,0.08,0.385,0.06])
	cb.ax.set_aspect(0.25)

	cb.ax.title.set_fontsize(16)
	cb.ax.title.set_position([1.7,-0.3])
	cb.ax.title.set_text(r"$log(dI$/$dV)$ $(\rm{S})$")

	return cb

def f_format(f):
	"""
	This function formats the figure
	"""
	f.subplots_adjust(left = 0.16, bottom = 0.22, right = 0.98, top = 0.96, wspace = 0.2, hspace = 0.2)
	f.set_size_inches([4.5,4.5],forward = "true")
	return f

def ax_format(ax,string):
	"""
	This function formats the axis
	"""
	#The three next lines have to be improved to handle the zoom...
	#ax.set_aspect("auto")
	#ax.set_xticklabels(floor(ax.get_xticks()),fontsize = 11)
	#ax.set_yticklabels(ax.get_yticks(),fontsize = 11)
	ax.set_ylabel(r"$V_{\rm{sd}}$ $(\rm{mV})$",fontsize = 16, fontweight = "regular", position = (1,0.5), horizontalalignment = "center")
	if(string == "Vg_Vds_Map"):
		ax.set_xlabel(r"$V_{\rm{g}}$ $(\rm{V})$",fontsize = 16, verticalalignment = "top", horizontalalignment = "right", position = (0.9,1) )
	if(string == "B") :
		ax.set_xlabel(r"$B$ $(\rm{T})$",fontsize = 16, verticalalignment = "top", horizontalalignment = "right", position = (0.9,1) )

	
	"""
	This part handle the position of the ticks
	"""
	xlines = ax.get_xticklines()
	ylines = ax.get_yticklines()

	for line in xlines :
		line.set_marker(mpllines.TICKDOWN)

	for line in ylines :
		line.set_marker(mpllines.TICKLEFT)

	xlabels = ax.get_xticklabels()
	ylabels = ax.get_yticklabels()
	
	for label in xlabels :
		label.set_y(-0.01)
	for label in ylabels :
		label.set_x(-0.01) 

	ax.xaxis.set_ticks_position("bottom")
        ax.yaxis.set_ticks_position("left")


	return ax


def plot_format(f,ax,cb,string) :
	"""
	This fonction handles the final plot given the figure, the axes, the colorbar and a string ("Vg_Vds_Map" or "B" )
	"""
	cb_format(cb)
	f_format(f)
	ax_format(ax,string)
	return True
		

"""
*********************************************************************************
*		Data processing:
*This part contains all the functions dedicated to the data processing
"""



def get_coupling():
	"""	
	This function gives the coupling of the sample to the gate source and drain as weel as the alpha factor given by Cg/Ct . 
	One has to give four point, starting with the slope defined by Cg/Cs and then the one defined by Cg / (Cd +Cg). It retunrs the result 
	as Cs Cd and alpha.
	"""
	temp = ginput(4)
	Cs = abs( (temp[0][0] - temp[1][0]) / (temp[0][1] - temp[1][1])) * 1e3
	tp = abs( ( temp[2][1] - temp[3][1] )/(temp[2][0] - temp[3][0])) * 1e-3
	Cd = (1 - tp)/ tp
	alp = 1 / (Cs + 1 +Cd)
	return [Cs,Cd,alp] 



def get_slope():
	"""
	Given two points, give the slope a line
	"""
	temp = ginput(2)
	return (temp[0][1] - temp[1][1])/(temp[0][0] - temp[1][0])




def getposcolumn(data,string):
	"""
	This function allows to obtain the column number in a json file sweep given the name of the input
	"""
	result = 0
	for i in range(size(data["measures"][0]["columns"])) :
		if(data["measures"][0]["columns"][i] == string) :
			result = i+1
	return result



def json_data(jsonobject,i,column) :
	"""
	Given a json object generated by NanoQt, it extracts the column of a the data nbr i
	"""
	try :
		data_temp = jsonobject["measures"][i]["data"]
	except :
		print "Problem using data_json function"

	if type(column) == str:
		try :
			column = getposcolumn(data_temp,column)	
		except :
			print "There is not such a column name, taking column = 1"
			column = 1
	temp = []

	for j in range(len(data_temp)):
		temp.append(data_temp[j][column-1])

	return temp



def colarray(data, colnum, rem):
	"""
	This function give back the column of an array given the array and the column number to be extracted. 
	The third parameter allow to get ride of the first terms of the column.
	"""
	temp = []
	for i in range( len(data) - rem):
		temp.append(data[i+rem][colnum-1])
	return temp


def colarray_pol(data,A,B,theta):
	"""
	This function is dedicated to the polarplot in oder to take into account the signe of the magnetic field in the trace - retrace pot
	"""		
	temp = []
	for i in range( len(data)):
		temp.append(data[i][1] * sign(data[i][0]) - A*abs(sin(theta)) - B*abs(cos(theta)))
	return temp




def plotdata(data, x, y):
	"""
	This function plot a 2D curve given a json data and the column number of x and y axis.
	"""
	plot(colarray(data, x, 0), colarray(data, y, 0))
	return True


def getinputs(data):
	"""
	This function give the inputs used for a measurement given the corresponding json file.
	"""
	inputs = data["inputs"]
	result = []
	for x in inputs:
		result.append(str(data["inputs"][x]["name"]).replace("u", ""))
	return result

def getoutputs(data):
	"""
	This function give the outputs used for a measurement given the corresponding json file.
	"""
	
	inputs = data["outputs"]
	result = []
	for x in inputs:
		result.append(str(data["outputs"][x]["name"]).replace("u", ""))
	return result

def getcolumns(data, col_num, sweep_num):
	"""
	This function allows to access to one column of a json file sweep given the sweep and the column numbers.
	"""
	result = []
	for i in range(sweep_num):
		result.append(colarray(data["measures"][i]["data"],col_num , 0))
	return result


"""

With the new json style, this function becomes useless
def get_GB(data, col_num, sweep_num):
This function allows to access to one column of a json file sweep given the sweep and the column numbers.
result = []
result.append(colarray(data["measures"][sweep_num]["data"],col_num , 0))
return result[0]
"""



def export_data(filename, data):
	savetxt(filename,matrix(data).transpose(),delimiter = " , ")
	return True



def extractScilab(data):
	"""
	This function allows to extract the data from a CSV like file. This is the function that should be used for the old transfrom data.
	"""
	
	raw = size(data) / size(data[1])
	result = []
	for i in range(raw-1) :
		result.append(data[ (i+1) , 1: ])
	return result


def plot_profile_h(im):
	"""
	Given a point on the Coulomb Map, this function plot the corresponding profile and returns a array of two columns [V,dI/dV]
	"""
	y = ginput()[0][1]
	xm,  Xm = im.get_extent()[0:2]
	ym,  Ym = im.get_extent()[2:4]
	sweep_n = size(im.get_array()) / size(im.get_array()[0])
	nbr =  (1. * sweep_n / abs(Ym - ym)) * (y-ym) 
	figure()
	data = im.get_array()
	plot(linspace(xm, Xm, size(im.get_array()[0])) ,  data[nbr])
	return [linspace(xm, Xm, size(im.get_array()[0]))  , data[nbr]]




def plot_profile(im):
	"""
	Given a point on the Coulomb Map, this function plot the corresponding profile and returns a array of two columns [V,dI/dV]
	"""
	x = ginput()[0][0]
	xm,  Xm = im.get_extent()[0:2]
	ym,  Ym = im.get_extent()[2:4]
	sweep_n = size(im.get_array()[0])
	nbr =  (1. * sweep_n / abs(Xm - xm)) * (x-xm)
	Vg = xm + nbr * (Xm-xm)/sweep_n 		
	figure()
	data = im.get_array()
	plot( linspace(ym, Ym, size(colarray(data,floor(nbr),0))) ,  colarray(data,floor(nbr),0))
	return [linspace(ym, Ym, size(colarray(data,floor(nbr),0))) ,  colarray(data,floor(nbr),0),Vg]

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


def co_above(data,seuil):
	data.sort(reverse = True)
	for i in range(size(data)):
		if data[i]< seuil :
			result = i
			break
	return result

def sum_over(data) :
	result = []
	for i in range(len(data)) :
		result.append(sum(data[0:i+1]))
	
	return result