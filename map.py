"""
Here are gathered the class dedicated to coulomb maps. Now, with the new javascripts, 
"""

class JsonDataOld :
	"""
	This class is used to handle data stored in a json file. It takes a jsonfile as argument ang generate an object that makes data easier to manipulate
	"""
	def __init__(self,filename) :
		self._data = extracjson(filename)
		self._inputs = getinputs(self._data)
		self._outputs = getoutputs(self._data)
		self._sweep_number = size(self._data["measures"])
		self._inphase = getcolumns(self._data, getposcolumn(self._data,"real"), self._sweep_number)

	def map_phase(self):
		imshow(matrix(self._inphase).transpose().tolist(), origin="lower",extent = [-3,3,-1,1],aspect = 5)


class JsonData :
	"""
	This is the new class Json file that should generate in an esasier way, the correct plot with the correct axis.
	"""
	def __init__(self,filename):
		self._data = extracjson(filename)
		self._inputs = getinputs(self._data)
		self._outputs = getoutputs(self._data)
		self._sweep_number = size(self._data["measures"])
		self._inphase = getcolumns(self._data, getposcolumn(self._data,"real"),self._sweep_number)
		self._pylab = self._data["pylab"]

	def plot_prof(self):
		temp = plot_profile(self.im)
		return temp
		
	def plot_prof_h(self):
		temp = plot_profile_h(self.im)
		return temp
	
	def get_coup(self):
		temp =  get_coupling()
		self.cs = temp[0]
		self.cd = temp[1]
		self.alpha= temp[2]
		return temp
	
	def map_phase(self):
		self.fig = figure()
		self.ax  = self.fig.add_subplot(111)
		self.im = self.ax.imshow(matrix(self._inphase).transpose().tolist(), origin="lower" , extent = [self._pylab["x_min"], self._pylab["x_max"], self._pylab["y_min"]*1e3, self._pylab["y_max"]*1e3]  )
		self.col = self.fig.colorbar(self.im)
		self.ax = ax_format(self.ax,self._pylab["kind"])
		self.ax.set_aspect("auto")
		self.col.ax.title.set_text(r"$dI$/$dV$ $(\rm{S})$")
		
	def map_phase_mayavi(self):
		self.im_mayavi = emm.imshow(matrix(self._inphase).transpose().tolist(), origin="lower" , extent = [self._pylab["x_min"], self._pylab["x_max"], self._pylab["y_min"]*1e3, self._pylab["y_max"]*1e3]  )
