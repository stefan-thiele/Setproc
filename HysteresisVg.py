class HystVg(Measure) :
	"""
	This class is used to handle data stored in a json file. It takes a jsonfile as argument ang generate an object that makes data easier to manipulate
	"""
	def __init__(self,filename,mode):
		Measure.__init__(self,filename,mode)

		"""
		self.pylab = None
		self.bias = None
		self.sweep_number = None
		self.data
		"""
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
		si = size(self["bias"])
		ymin = self["bias"][0]
		ymax= self["bias"][si-1]
		xmin = self["metadata"]["V_g"]["min"]	
		xmax = self["metadata"]["V_g"]["max"]
		self.im = imshow(self["data"])
		self.im.set_extent([xmin,xmax,ymin,ymax])


class FullHystVg(dict) :
	
	def __init__(self,trace,retrace,mode) :
		self.trace = HystVg(trace,mode)
		self.retrace = HystVg(retrace,mode)


	def _do_pic_map(self,width):
		sit = size(self.trace["bias"])	
		sir = size(self.retrace["bias"])
		if(sit != sir) :
			print "Size problem !! Are you sure that the data are compatible"
		else :
			self["data_pic"] = []
			for i in range(self.trace["sweep_number"]) :
				tempT = array(pic_detect(self.trace["data"][i],width))
				tempR = array(pic_detect(self.retrace["data"][i],width))
				self["data_pic"].append(((tempT + tempR)/(2*tempR)))
		return True

	def get_jump(self,i_start,seuil,w=9) :
		sit = size(self.trace["bias"])
		sir = size(self.retrace["bias"])
		self["data_pic"] = []
		vgmin = self.trace["metadata"]["V_g"]["min"]
		vgstep  = self.trace["metadata"]["V_g"]["step"]

		for i in range(self.trace["sweep_number"]) :
			bsweep = self.trace["bias"][i_start+(w-1):sit-(w-1)]
			jump = pic_detect(self.trace["data"][i][i_start:],w)
			max_jump = max(jump)
			if max_jump > seuil :
				self["data_pic"].append([ bsweep[jump.index(max_jump)], (vgmin + i*vgstep)])
		
		for i in range(self.retrace["sweep_number"]) :
			bsweep = self.retrace["bias"][i_start+(w-1):sir-(w-1)]
			jump = pic_detect(self.retrace["data"][i][i_start:],w)
			max_jump = max(jump)
			if max_jump > seuil :
				self["data_pic"].append([ bsweep[jump.index(max_jump)], (vgmin + i*vgstep)])
		return True
	

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
				self["data"].append((YT -array(YR))/YT)
				"""for j in range(sit) :
					self["data"][i][j] = self["data"][i][j]*sign(self.trace["bias"][j])
				"""
		return True

	def map_phase(self) :
		si = size(self.trace["bias"])
		ymin = self.trace["bias"][0]
		ymax= self.trace["bias"][si-1]
		xmin = self.trace["metadata"]["V_g"]["min"]	
		xmax = self.trace["metadata"]["V_g"]["max"]
		self.fig = figure()
		self.ax  = self.fig.add_subplot(111)
		self.im = self.ax.imshow(matrix(self["data"]).transpose().tolist())
		self.im.set_extent([xmin,xmax,ymin,ymax])
		self.ax.set_aspect("auto")

