import os as os



class Density_Open(ToSaveObject) :
	"""
	It generated an GB_Open object
	"""
	def __init__(self,trace,retrace = None ,interval = None, mode = "Json"):
		ToSaveObject.__init__(self)
		self.filenames_trace = []
		self.filenames_retrace = []
		if(interval == None and retrace ==None) :
			temp = OpenBin(trace)
			for x in temp :
				self[x] = temp[x]
			del(temp)


		else :
			GB_array1 = []
			for i in interval :
				self.filenames_trace.append(str(i)+trace)
			for x in self.filenames_trace :
				print "Loading ",x," file. Please wait.."
				GB_array1.append(GB_Open(x,mode))
				GB_array1[-1].sanity_check()
			print "Merging...."
			self.trace = merge_GB(GB_array1)
			
			del(GB_array1)		
			GB_array2 = []
			for i in interval :
				self.filenames_retrace.append(str(i)+retrace)
			for x in self.filenames_retrace :
				print "Loading ",x," file. Please wait.."
				GB_array2.append(GB_Open(x,mode))
				GB_array2[-1].sanity_check()
			print "Merging...."
			self.retrace = merge_GB(GB_array2)
			del(GB_array2)
			print "Finale sanity check once merged"
			print "trace...."
			self.trace.sanity_check()
			print "retrace..."
			self.retrace.sanity_check()
			self["metadata"] = self.trace["metadata"]
			del(self.filenames_trace)
			del(self.filenames_retrace)


	def get_stat(self,seuil,i_start,w) :
		self["UP"] = [[],[],[],[]]
		self["DOWN"] = [[],[],[],[]]
		self["sequence"] = []
		sweep_number = self.trace["sweep_number"]
		for i in range(sweep_number) :
			
			#TRACE STAT
			Down, Up = self.trace.get_jump_2(i,i_start,seuil,w)
			#check the sequence and correct errors
			if(Down[2] and Up[2] ) :
				if(Down[0]<Up[0]) :
					if(size(self["sequence"])>0) :
						if(self["sequence"][-1] == 0 ) :
							self["DOWN"][0].pop(-1)
							self["DOWN"][1].pop(-1)
							self["DOWN"][2].pop(-1)
							self["DOWN"][3].pop(-1)
							self["sequence"].pop(-1)
					self["sequence"].append(0)
					self["sequence"].append(1)
				else :
					if(size(self["sequence"])>0) :
						if(self["sequence"][-1] == 1 ) :
							self["UP"][0].pop(-1)
							self["UP"][1].pop(-1)
							self["UP"][2].pop(-1)
							self["UP"][3].pop(-1)
							self["sequence"].pop(-1)
					self["sequence"].append(1)
					self["sequence"].append(0)
			elif(Down[2]):
				if(size(self["sequence"])>0) :
					if(self["sequence"][-1] == 0 ) :
						self["DOWN"][0].pop(-1)
						self["DOWN"][1].pop(-1)
						self["DOWN"][2].pop(-1)
						self["DOWN"][3].pop(-1)
						self["sequence"].pop(-1)
				self["sequence"].append(0)
			elif(Up[2]) :
				if(size(self["sequence"])>0) :
					if(self["sequence"][-1] == 1 ) :
						self["UP"][0].pop(-1)
						self["UP"][1].pop(-1)
						self["UP"][2].pop(-1)
						self["UP"][3].pop(-1)
						self["sequence"].pop(-1)
				self["sequence"].append(1)
			#once the sequence have been checked, add the stat
			if(Up[2]) :
				self["UP"][0].append(Up[0])
				self["UP"][1].append(Up[1])
				self["UP"][2].append("trace")
				self["UP"][3].append(Up[3])
			if(Down[2]) :
				self["DOWN"][0].append(Down[0])
				self["DOWN"][1].append(Down[1])
				self["DOWN"][2].append("trace")
				self["DOWN"][3].append(Down[3])

			#RETRACE STAT
			Down,Up = self.retrace.get_jump_2(i,i_start,seuil,w)
			#check sequence
			if(Down[2] and Up[2] ) :
				if(Down[0]<Up[0]) :
					if(size(self["sequence"])>0) :
						if(self["sequence"][-1] == 1 ) :
							self["UP"][0].pop(-1)
							self["UP"][1].pop(-1)
							self["UP"][2].pop(-1)
							self["UP"][3].pop(-1)
							self["sequence"].pop(-1)
					self["sequence"].append(1)
					self["sequence"].append(0)
				else :
					if(size(self["sequence"])>0) :
						if(self["sequence"][-1] == 0 ) :
							self["DOWN"][0].pop(-1)
							self["DOWN"][1].pop(-1)
							self["DOWN"][2].pop(-1)
							self["DOWN"][3].pop(-1)
							self["sequence"].pop(-1)
					self["sequence"].append(0)
					self["sequence"].append(1)
			elif(Down[2]):
				if(size(self["sequence"])>0) :
					if(self["sequence"][-1] == 0 ) :
						self["DOWN"][0].pop(-1)
						self["DOWN"][1].pop(-1)
						self["DOWN"][2].pop(-1)
						self["DOWN"][3].pop(-1)
						self["sequence"].pop(-1)
				self["sequence"].append(0)
			elif(Up[2]) :
				if(size(self["sequence"])>0) :
					if(self["sequence"][-1] == 1 ) :
						self["UP"][0].pop(-1)
						self["UP"][1].pop(-1)
						self["UP"][2].pop(-1)
						self["UP"][3].pop(-1)
						self["sequence"].pop(-1)
				self["sequence"].append(1)
			#once the sequence has been checked, add stat
			if(Up[2]) :
				self["UP"][0].append(Up[0])
				self["UP"][1].append(Up[1])
				self["UP"][2].append("retrace")
				self["UP"][3].append(Up[3])
			if(Down[2]) :
				self["DOWN"][0].append(Down[0])
				self["DOWN"][1].append(Down[1])
				self["DOWN"][2].append("retrace")
				self["DOWN"][3].append(Down[3])
			

		return True

	def get_stat_2(self,seuil,i_start,w=4) :
		self["UP2"] = [[],[]]
		self["DOWN2"] = [[],[]]
		self["sequence2"] = []
		sweep_number = self.trace["sweep_number"]
		for i in range(sweep_number) :
			trace = self.trace.get_jump(i,i_start,seuil,w)
			retrace = self.retrace.get_jump(i,i_start,seuil,w)
			if(trace[2] ):
				if( size(self["sequence2"]) > 0 and size(self["DOWN"][0]) > 0 ) :
					if(self["sequence2"][-1] == 0) :
						self["sequence2"].pop(-1)
						self["DOWN2"][0].pop(-1)
						self["DOWN2"][1].pop(-1)
				self["DOWN2"][0].append(trace[0])
				self["DOWN2"][1].append(trace[1])
				self["sequence2"].append(0)
			if(retrace[2] ):
				if( size(self["sequence2"]) > 0 and size(self["UP"][0]) > 0 ) :
					if(self["sequence2"][-1] == 1) :
						self["sequence2"].pop(-1)
						self["UP2"][0].pop(-1)
						self["UP2"][1].pop(-1)
				self["UP2"][0].append(retrace[0])
				self["UP2"][1].append(retrace[1])
				self["sequence2"].append(1)
		return True

	def get_hist_vs_retrace(self,points,rge,shift_B,shift_trace) :
		tempUp = deep_copy(self["UP"])
		tempDown = deep_copy(self["DOWN"])
		siup = size(tempUp[0])
		sidown = size(tempDown[0])
		for i in range(siup) :
			if (tempUp[2][i] == "retrace") :
				tempUp[0][i] = tempUp[0][i] - shift_B
		for i in range(sidown) :
			if (tempDown[2][i] == "retrace") :
				tempDown[0][i] = tempDown[0][i] - shift_B
		min_si = min(siup,sidown)
		return histogram2d(tempDown[0][:min_si-shift_trace],tempUp[0][shift_trace:min_si],points,rge)

	def get_hist_vs_trace(self,points,rge,shift_B,shift_trace=1):
		tempUp = deep_copy(self["UP"])
		siup = size(tempUp[0])
		for i in range(siup) :
			if (tempUp[2][i] == "retrace") :
				tempUp[0][i] = tempUp[0][i] -shift_B
		return histogram2d(tempUp[0][:siup-shift_trace],tempUp[0][shift_trace:siup],points,rge)

	def get_animation(self,nbr_of_frame,points,rge,shift_B) :
		self["animation"] = []
		for i in range(nbr_of_frame) :
			self["animation"].append(self.get_hist_vs_retrace(points,rge,shift_B,i))
			self["animation"].append(self.get_hist_vs_trace(points,rge,shift_B,i+1))
		return True

	def save_all(self,tracefile,retracefile,whole_experiment) :
		self.trace.save(tracefile)
		self.retrace.save(retracefile)
		self["filenames"] = [tracefile, retracefile]
		self.save(whole_experiment)

	def load_bin(self):
		self.trace = GB_Open(self["filenames"][0],"Bin")
		self.retrace = GB_Open(self["filenames"][1],"Bin")
		print "Sanity checks"
		print "* Trace"
		self.trace.sanity_check()
		print "* Retrace"
		self.retrace.sanity_check()

