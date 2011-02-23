import os as os



class Density_Open(ToSaveObject) :
	"""
	It generated an GB_Open object
	"""
	def __init__(self,trace,retrace,interval,mode = "Json"):
		ToSaveObject.__init__(self)
		self.filenames_trace = []
		self.filenames_retrace = []
		
		GB_array1 = []
		for i in interval :
			self.filenames_trace.append(str(i)+trace)
		for x in self.filenames_trace :
			print "Loading ",x," file. Please wait.."
			GB_array1.append(GB_Open(x,mode))
			GB_array1[-1].sanity_check()
		print "Merging...."
		self["trace"] = merge_GB(GB_array1)
		
		del(GB_array1)		
		GB_array2 = []
		for i in interval :
			self.filenames_retrace.append(str(i)+retrace)
		for x in self.filenames_retrace :
			print "Loading ",x," file. Please wait.."
			GB_array2.append(GB_Open(x,mode))
			GB_array2[-1].sanity_check()
		print "Merging...."
		self["retrace"] = merge_GB(GB_array2)
		del(GB_array2)
		print "Finale sanity check once merged"
		print "trace...."
		self["trace"].sanity_check()
		print "retrace..."
		self["retrace"].sanity_check()


	def get_stat(self,seuil,i_start,w) :
		self["UP"] = [[],[]]
		self["DOWN"] = [[],[]]
		self["sequence"] = [0]
		sweep_number = self["trace"]["sweep_number"]
		for i in range(sweep_number) :
			
			#TRACE STAT
			Down, Up = self["trace"].get_jump_2(i,i_start,seuil,w)
			#check the sequence and correct errors
			if(Down[2] and Up[2] ) :
				if(Down[0]<Up[0]) :
					if(self["sequence"][-1] == 0 ) :
						self["DOWN"][0].pop(-1)
						self["DOWN"][1].pop(-1)
						self["sequence"].pop(-1)
					self["sequence"].append(0)
					self["sequence"].append(1)
				else :
					if(self["sequence"][-1] == 1) :
						self["UP"][0].pop(-1)
						self["UP"][1].pop(-1)
						self["sequence"].pop(-1)
					self["sequence"].append(1)
					self["sequence"].append(0)
			elif(Down[2]):
				if(self["sequence"][-1] == 0 ) :
					self["DOWN"][0].pop(-1)
					self["DOWN"][1].pop(-1)
					self["sequence"].pop(-1)
				self["sequence"].append(0)
			elif(Up[2]) :
				if(self["sequence"][-1] == 1) :
					self["UP"][0].pop(-1)
					self["UP"][1].pop(-1)
					self["sequence"].pop(-1)
				self["sequence"].append(1)
			#once the sequence have been checked, add the stat
			if(Up[2]) :
				self["UP"][0].append(Up[0])
				self["UP"][1].append(Up[1])
			if(Down[2]) :
				self["DOWN"][0].append(Down[0])
				self["DOWN"][1].append(Down[1])

			#RETRACE STAT
			Down,Up = self["retrace"].get_jump_2(i,i_start,seuil,w)
			#check sequence
			if(Down[2] and Up[2] ) :
				if(Down[0]<Up[0]) :
					if(self["sequence"][-1] == 1) :
						self["UP"][0].pop(-1)
						self["UP"][1].pop(-1)
						self["sequence"].pop(-1)
					self["sequence"].append(1)
					self["sequence"].append(0)
				else :
					if(self["sequence"][-1] == 0 ) :
						self["DOWN"][0].pop(-1)
						self["DOWN"][1].pop(-1)
						self["sequence"].pop(-1)
					self["sequence"].append(0)
					self["sequence"].append(1)
			elif(Down[2]):
				if(self["sequence"][-1] == 0 ) :
					self["DOWN"][0].pop(-1)
					self["DOWN"][1].pop(-1)
					self["sequence"].pop(-1)
				self["sequence"].append(0)
			elif(Up[2]) :
				if(self["sequence"][-1] == 1) :
					self["UP"][0].pop(-1)
					self["UP"][1].pop(-1)
					self["sequence"].pop(-1)
				self["sequence"].append(1)
			#once the sequence has been checked, add stat
			if(Up[2]) :
				self["UP"][0].append(Up[0])
				self["UP"][1].append(Up[1])
			if(Down[2]) :
				self["DOWN"][0].append(Down[0])
				self["DOWN"][1].append(Down[1])
			

		return True

	def get_stat_2(self,seuil,i_start,w=4) :
		self["UP2"] = [[],[]]
		self["DOWN2"] = [[],[]]
		self["sequence2"] = []
		sweep_number = self["trace"]["sweep_number"]
		for i in range(sweep_number) :
			trace = self["trace"].get_jump(i,i_start,seuil,w)
			retrace = self["retrace"].get_jump(i,i_start,seuil,w)
			if(trace[2] ):
				if( size(self["sequence2"]) > 0 ) :
					if(self["sequence"][-1] == 0) :
						self["sequence"].pop(-1)
						self["DOWN2"][0].pop(-1)
						self["DOWN2"][1].pop(-1)
				self["DOWN2"][0].append(trace[0])
				self["DOWN2"][1].append(trace[1])
				self["sequence"].append(0)
			if(retrace[2] ):
				if( size(self["sequence2"]) > 0 ) :
					if(self["sequence"][-1] == 1) :
						self["sequence"].pop(-1)
						self["UP2"][0].pop(-1)
						self["UP2"][1].pop(-1)
				self["UP2"][0].append(retrace[0])
				self["UP2"][1].append(retrace[1])
				self["sequence"].append(1)
		return True
