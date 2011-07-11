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
		self["detection"] = [[],[],[],[],[]]
		sweep_number = self.trace["sweep_number"]
		for i in range(sweep_number) :
			
			#TRACE STAT
			Down, Up = self.trace.get_jump_2(i,i_start,seuil,w)
			if(Down[2] and Up[2] ) :
				if(Down[0]<Up[0]) :
					self["detection"][0].append(Down[0])
					self["detection"][1].append(Down[1])
					self["detection"][2].append("trace")
					self["detection"][3].append(Down[3])
					self["detection"][4].append('down')
					self["detection"][0].append(Up[0])
					self["detection"][1].append(Up[1])
					self["detection"][2].append("trace")
					self["detection"][3].append(Up[3])
					self["detection"][4].append("up")
				else :
					self["detection"][0].append(Up[0])
					self["detection"][1].append(Up[1])
					self["detection"][2].append("trace")
					self["detection"][3].append(Up[3])
					self["detection"][4].append('up')
					self["detection"][0].append(Down[0])
					self["detection"][1].append(Down[1])
					self["detection"][2].append("trace")
					self["detection"][3].append(Down[3])
					self["detection"][4].append("down")
			elif(Up[2]) :
				self["detection"][0].append(Up[0])
				self["detection"][1].append(Up[1])
				self["detection"][2].append("trace")
				self["detection"][3].append(Up[3])
				self["detection"][4].append("up")
			elif(Down[2]) :
				self["detection"][0].append(Down[0])
				self["detection"][1].append(Down[1])
				self["detection"][2].append("trace")
				self["detection"][3].append(Down[3])
				self["detection"][4].append("down")

			#RETRACE STAT
			Down,Up = self.retrace.get_jump_2(i,i_start,seuil,w)
			if(Down[2] and Up[2] ) :
				if(Down[0] > Up[0]) :
					self["detection"][0].append(Down[0])
					self["detection"][1].append(Down[1])
					self["detection"][2].append("retrace")
					self["detection"][3].append(Down[3])
					self["detection"][4].append("down")
					self["detection"][0].append(Up[0])
					self["detection"][1].append(Up[1])
					self["detection"][2].append("retrace")
					self["detection"][3].append(Up[3])
					self["detection"][4].append("up")
				else :
					self["detection"][0].append(Up[0])
					self["detection"][1].append(Up[1])
					self["detection"][2].append("retrace")
					self["detection"][3].append(Up[3])
					self["detection"][4].append("up")
					self["detection"][0].append(Down[0])
					self["detection"][1].append(Down[1])
					self["detection"][2].append("retrace")
					self["detection"][3].append(Down[3])
					self["detection"][4].append("down")
			elif(Up[2]) :
				self["detection"][0].append(Up[0])
				self["detection"][1].append(Up[1])
				self["detection"][2].append("retrace")
				self["detection"][3].append(Up[3])
				self["detection"][4].append("up")
			elif(Down[2]) :
				self["detection"][0].append(Down[0])
				self["detection"][1].append(Down[1])
				self["detection"][2].append("retrace")
				self["detection"][3].append(Down[3])
				self["detection"][4].append("down")
			

		return True
	def evol_state(self,shift) :
		self["evol"]=[[],[],[],[]]
		for i in range(size(self["detection"][0])) :
			if self["detection"][2][i] == "retrace" :
				self["evol"][0].append(self["detection"][0][i] - shift)
			else :
				self["evol"][0].append(self["detection"][0][i])
			self["evol"][1].append(self["detection"][3][i])
			self["evol"][2].append(self["detection"][2][i])
			self["evol"][3].append(self["detection"][4][i])

		return True

	def plot_evol(self,span) :
		self.fig = figure()
		self.ax = self.fig.add_subplot(111)
		color = "blue"
		conf = 1
		for i in range(size(self["detection"][0])-span) :
			if self["evol"][2][i] == "trace" :
				if self["evol"][3][i] == "down" :
					self.ax.plot(self["evol"][1][i],self["evol"][0][i],'bo')
				else :
					self.ax.plot(self["evol"][1][i],self["evol"][0][i],'ro')

			if self["evol"][2][i] == "retrace" :
				if self["evol"][3][i] == "down" :
					self.ax.plot(self["evol"][1][i],self["evol"][0][i],'ro')
				else :
					self.ax.plot(self["evol"][1][i],self["evol"][0][i],'bo')

			self.ax.set_xlim(i,i-span)
			#sleep(0.01)
			#draw()
		


	def plot_Map_H(self,kind,trans,Hmin,stepH):
		temp = [[],[]]
		for i in range(size(self["detection"][0])):
			if self["detection"][2][i] == kind and self["detection"][4][i] == trans :
				temp[0].append(Hmin + self["detection"][3][i] * stepH)
				temp[1].append(self["detection"][0][i])
		return temp

	def get_hist(self,points,rge,shift_B,shift_trace=1):
		temp = deep_copy(self["detection"])
		siup = size(temp[0])
		for i in range(siup) :
			if (temp[2][i] == "retrace") :
				temp[0][i] = temp[0][i] -shift_B
		return histogram2d(temp[0][:siup-shift_trace],temp[0][shift_trace:siup],points,rge)

	def get_direct_trans(self,Tr) :
		self["direct_trans"] = [[],[]]
		for i in range(size(self["detection"][0])-2) :
			if abs(self["detection"][0][i+1]) > Tr :
				self["direct_trans"][0].append(self["detection"][0][i])
				self["direct_trans"][1].append(self["detection"][0][i+2])


	def get_A_R(self) :
		self["AvsR"] = [[],[]]
		for i in range(size(self["detection"][0])) :
			print i
			for j in range(size(self["detection"][0])-(i+1)) :
				check = self["detection"][3][j+i+1]-1
				if self["detection"][3][i] == check :
					if self["detection"][2][i] == "retrace" and self["detection"][2][j+i+1] == "trace" :
						self["AvsR"][0].append(self["detection"][0][i])
						self["AvsR"][1].append(self["detection"][0][j+i+1])
						break
	
	def sort_data(self,offset) :
		self["sort"] = dict()
		self["sort"]["trace"] = dict()
		self["sort"]["trace"]["up"] = []
		self["sort"]["trace"]["down"] = []
		self["sort"]["retrace"] = dict()
		self["sort"]["retrace"]["up"] = []
		self["sort"]["retrace"]["down"] = []
		for i in range(size(self["detection"][0])) :
			if self["detection"][2][i] == "trace" :
				if self["detection"][4][i] == "down" :
					self["sort"]["trace"]["down"].append(self["detection"][0][i])
				if self["detection"][4][i] == "up" :
					self["sort"]["trace"]["up"].append(self["detection"][0][i])
			if self["detection"][2][i] == "retrace" :
				if self["detection"][4][i] == "down" :
					self["sort"]["retrace"]["down"].append(self["detection"][0][i] - offset)
				if self["detection"][4][i] == "up" :
					self["sort"]["retrace"]["up"].append(self["detection"][0][i] - offset)
		return True

	def get_double(self,offset = 0) :
		self["double"]= dict()
		self["double"]["trace"]=[[],[],[]]
		self["double"]["retrace"] = [[],[],[]]

		for i in range(size(self["detection"])) :
			type_sweep = self["detection"][2][i]
			nbr_sweep = self["detection"][3][i]
			for j in range(size(self["detection"][0])-(i+1)) :
				if type_sweep == self["detection"][2][j+i+1] and nbr_sweep == self["detection"][3][j+i+1] :
					if type_sweep == "trace" :
						self["double"]["trace"][0].append(self["detection"][0][i])
						self["double"]["trace"][1].append(self["detection"][0][j+i+1])
						self["double"]["trace"][2].append(nbr_sweep)
					if type_sweep == "retrace" :
						self["double"]["retrace"][0].append(self["detection"][0][i] - offset)
						self["double"]["retrace"][1].append(self["detection"][0][j+i+1] - offset)
						self["double"]["retrace"][2].append(nbr_sweep)

	def get_animation(self,nbr_of_frame,points,rge,shift_B) :
		self["animation"] = []
		for i in range(nbr_of_frame) :
			#self["animation"].append(self.get_hist(points,rge,shift_B,i))
			self["animation"].append(self.get_hist(points,rge,shift_B,i+1))
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

