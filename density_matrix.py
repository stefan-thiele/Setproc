import os as os



class Density_Open(ToSaveObject) :
	"""
	It generated an GB_Open object
	"""
	def __init__(self,trace,retrace,interval,mode = "Json"):
		ToSaveObject.__init__(self)
		self.filenames_trace = []
		self.filenames_retrace = []
		
		GB_array = []
		for i in interval :
			self.filenames_trace.append(str(i)+trace)
		for x in self.filenames_trace :
			GB_array.append(GB_Open(x,mode))
		self["trace"] = merge_GB(GB_array)
		del(GB_array)
		
		GB_array = []
		for i in interval :
			self.filenames_retrace.append(str(i)+retrace)
		for x in self.filenames_retrace :
			GB_array.append(GB_Open(x,mode))
		self["retrace"] = merge_GB(GB_array)
		del(GB_array)


	def get_stat(self,seuil,i_start,w) :
		self["UP"] = [[],[]]
		self["DOWN"] = [[],[]]
		self["sequence"] = []
		sweep_number = self["trace"]["sweep_number"]
		for i in range(sweep_number) :
			
			Down, Up = self["trace"].get_jump_2(i,i_start,seuil,w)
			if(Up[2]) :
				self["UP"][0].append(Up[0])
				self["UP"][1].append(Up[1])
			if(Down[2]) :
				self["DOWN"][0].append(Down[0])
				self["DOWN"][1].append(Down[1])

			if(Down[2] and Up[2] ) :
				if(Down[0]<Up[0]) :
					self["sequence"].append(0)
					self["sequence"].append(1)
				else :
					self["sequence"].append(1)
					self["sequence"].append(0)
			elif(Down[2]):
				self["sequence"].append(0)
			elif(Up[2]) :
				self["sequence"].append(1)

			Down,Up = self["retrace"].get_jump_2(i,i_start,seuil,w)
			if(Up[2]) :
				self["UP"][0].append(Up[0])
				self["UP"][1].append(Up[1])
			if(Down[2]) :
				self["DOWN"][0].append(Down[0])
				self["DOWN"][1].append(Down[1])
			
			if(Down[2] and Up[2] ) :
				if(Down[0]<Up[0]) :
					self["sequence"].append(1)
					self["sequence"].append(0)
				else :
					self["sequence"].append(0)
					self["sequence"].append(1)
			elif(Down[2]):
				self["sequence"].append(0)
			elif(Up[2]) :
				self["sequence"].append(1)

		return True

	def correlation_stat(self) :
		X1 = copy(self["trace"]["stat"][0])
		sX1 = size(X1)
		Y1 = copy(self["retrace"]["stat"][0])
		sY1 = size(Y1)
		X1 = X1.tolist()
		Y1 = Y1.tolist()
		X2= copy(X1)
		X2 = X2.tolist()
		X2.pop(0)
		sX2 = size(X2)
		Y2 = copy(Y1)
		Y2 = Y2.tolist()
		if( sX1 > sY1 ):
			X1 = X1[:sY1]
		else :
			Y1 = Y1[:sX1]
		
		if( sX2 > sY1) :
			X2 = X2[:sY1]
		else :
			Y2 = Y2[:sX2]
		self["stat"] = dict()
		self["stat"]["X"] = X1
		self["stat"]["Y"] = Y1
		for i in range(size(X2)) :
			self["stat"]["X"].append(X2[i])
		for i in range(size(Y2)) :
			self["stat"]["Y"].append(Y2[i])

		return True

	def correlation_trace(self) :
		X1 = copy(self["trace"]["stat"][0])
		sX1 =size(X1)
		X1 = X1.tolist()
		Y1 = copy(self["retrace"]["stat"][0])
		sY1 = size(Y1)
		Y1 = Y1.tolist()
		if( sX1 > sY1 ):
			X1 = X1[:sY1]
		else :
			Y1 = Y1[:sX1]
		return X1,Y1
	
	def correlation_retrace(self) :
		X1 = copy(self["trace"]["stat"][0])
		X1 = X1.tolist()
		X1.pop(0)
		sX1 =size(X1)
		Y1 = copy(self["retrace"]["stat"][0])
		sY1 = size(Y1)
		Y1 = Y1.tolist()
		if( sX1 > sY1 ):
			X1 = X1[:sY1]
		else :
			Y1 = Y1[:sX1]
		return X1,Y1
