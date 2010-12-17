
class TracePolar(OpenMeasures) :
	"""
	This class is used to handle data stored in a json file. It takes a jsonfile as argument ang generate an object that makes data easier to manipulate
	"""
	def __init__(self,filename,mode):
		OpenMeasures.__init__(self,filename,mode)

		"""
		self.pylab = None
		self.bias = None
		self.sweep_number = None
		self.data
		"""
		try :
			self["theta"] = [self["metadata"]["theta_min"],self["metadata"]["theta_max"]]
		except :
			print "This file does not contain any information about the angle range\n Please, enter these informations"
			self["theta"] = []
			self["theta"].append(input("theta_min : "))
			self["theta"].append(input("theta_max : "))

		self._check_data_size()


	def _check_data_size(self):
		"""
		This method makes sure that all the sweep have the same number of points than the bias
		"""
		sib = size(self["bias"])
		dsi = []
		for i in range(self["sweep_number"]) :
			sit = size(self["data"][i])
			dsi.append(abs(sit-sib))
			if (sit < sib ) :
				for j in range(sib - sit) :
					#recopie la derniere valeur pour completer
					self["data"][i].append(self["data"][i][sit-1])
			if (sit < sib ) :
				#recopie la derniere valeur pour completer
				self["data"][i] = self["data"][i][0:sib]

		print "Maximum points modified ----->  " , max(dsi)
			

	def map_phase(self,delta,offset):
		Si = size(self["bias"])
		th = linspace(self["theta"][0]+delta, self["theta"][1]+delta, self["sweep_number"])
		r = array(self["bias"])
		self.f= figure()
		self.ax = subplot(111, projection = 'polar')
		self.p= self.ax.pcolormesh(th,r, array(matrix(array(self["data"])-offset).transpose()))
		self.p.set_cmap(cmap =french)
		self.ax.set_rmax(abs(max(self["bias"])))
		self.cb = self.f.colorbar(self.p)



class FullPolar(dict) :
	
	def __init__(self,trace,retrace,mode) :
		self.trace = TracePolar(trace,mode)
		self.retrace = TracePolar(retrace,mode)

	def _do_difference(self) :
		sit = size(self.trace["bias"])	
		sir = size(self.retrace["bias"])
		if(sit != sir) :
			print "Size problem !! Are you sure that the data are compatible"
		else :
			self["data"] = []
			temp = self.retrace["data"]
			for i in range(self.trace["sweep_number"]) :
				YT = array(self.trace["data"][i])
				YR = self.retrace["data"][i]
				YR.reverse()
				self["data"].append(YT -array(YR))
				for j in range(sit) :
					self["data"][i][j] = self["data"][i][j]*sign(self.trace["bias"][j])
		return True


	def map_phase(self,delta,offset):
		Si = size(self.trace["bias"])
		th = linspace(self.trace["theta"][0]+delta, self.trace["theta"][1]+delta, self.trace["sweep_number"])
		r = array(self.trace["bias"])
		self.f= figure()
		self.ax = subplot(111, projection = 'polar')
		self.p= self.ax.pcolormesh(th,r, array(matrix(array(self["data"])-offset).transpose()))
		self.p.set_cmap(cmap =french)
		self.ax.set_rmax(abs(max(self.trace["bias"])))
		self.ax.yaxis.set_major_locator(MaxNLocator(3))
		self.cb = self.f.colorbar(self.p)
