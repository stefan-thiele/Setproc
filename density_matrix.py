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

	def get_stat_2(self,seuil,span,i_start,w=4) :
		self["UP2"] = [[],[]]
		self["DOWN2"] = [[],[]]
		sweep_number = self["trace"]["sweep_number"]

		for i in range(sweep_number) :
			
			temp_stat = self["trace"].get_jump_3(i,i_start,seuil,span,w)

		return True
