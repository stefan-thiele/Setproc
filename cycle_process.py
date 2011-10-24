"""
This code is merging fo density_matrix.py and g_b.py. Its aim is to be able to process all the cycle data using one single object.
"""

class cycle_process(ToSaveObject) :
	"""
	Cycle_process can be used to post-process several traces and retraces files. It will merge the traces and retraces between themselves using the merge function. You can save the extracted data so you do not have anymore to open all the sweeps and therefore you gain time and memory.
	The syntax depends if you have weither or not already extracted data. If it is the case, the syntax is cycle_process("filename"). Otherwise it is cycle_process("trace_filename","retrace_filemane",list of the increment values,and mode (usually "Json")). A sanity_check is performed on each sweep as weel as on the merged ones.
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
			self.post_loading()

		else :
			#TRACE
			GB_array1 = []
            #Construct a filename array for loading files
			for i in interval :
				self.filenames_trace.append(str(i)+trace)
			
            #Load the files of the filename array
			for x in self.filenames_trace :
				print "Loading ",x," file. Please wait.."
				GB_array1.append(sweep_set_open(x,mode))
				GB_array1[-1].sanity_check()
			print "Merging...."
                        #merge all the GB object in a single one and delete the GB array
			self.trace = merge_GB(GB_array1)
			del(GB_array1)		
			
			#RETRACE
			GB_array2 = []
			for i in interval :
				self.filenames_retrace.append(str(i)+retrace)
			for x in self.filenames_retrace :
				print "Loading ",x," file. Please wait.."
				GB_array2.append(sweep_set_open(x,mode))
				GB_array2[-1].sanity_check()
			print "Merging...."
			self.retrace = merge_GB(GB_array2)
			del(GB_array2)
			
			#Final checking!!
			print "Finale sanity check once merged"
			print "trace...."
			self.trace.sanity_check()
			print "retrace..."
			self.retrace.sanity_check()
			self["metadata"] = self.trace["metadata"]
			del(self.filenames_trace)
			del(self.filenames_retrace)


	def get_stat(self,seuil,i_start,w,power=1,sw=1) :
		"""
		get_stat allows to detect the jumps going through all the sweeps. It uses directly the function get_jump_2 of the sweep_set_open object. This data are stored independtly from the trace and retrace file. The syntax is the following get_stat(seuil,i_start,w) where seuil is the threshold of detection, i_start is the number of points to skip from zero, and w is the filter widht (see the filter doc for more information).
		"""
		self["detection"] = []
		sweep_number = self.trace["sweep_number"]
		for i in range(sweep_number) :
			
			#TRACE STAT
			Down, Up = self.trace.get_jump(i,i_start,w,power,sw)
			Down.trace = True
			Up.trace = True
			
			#check what was detected first
			if( Down.field < Up.field) :
				self["detection"].append(Down)
                                self["detection"].append(Up)
			else :
				self["detection"].append(Up)
				self["detection"].append(Down)

			#RETRACE STAT
			Down, Up = self.retrace.get_jump(i,i_start,w,power,sw)
			Down.trace = False
			Up.trace = False
			#check what was detected first
			if( Down.field > Up.field) :
				self["detection"].append(Down)
                                self["detection"].append(Up)
			else :
				self["detection"].append(Up)
				self["detection"].append(Down)
		return True



		


	def get_hist(self,points,rge,shift_B,seuil,shift_trace=1):
		temp = []
		siup = size(self["detection"])
		for i in range(siup) :
			topush = self["detection"][i]
			if(abs(topush.value) > seuil) : 
				if (topush.trace == False) :
					temp.append(topush.field -shift_B)
				else :
					temp.append(topush.field)
		siup = size(temp)
 
		return histogram2d(temp[:siup-shift_trace],temp[shift_trace:siup],points,rge)



	def get_A_R(self,seuil) :
		"""
		This function parse the data and store all the sweep for which there was a jump both for the trace and retrace. They are store in ["AvsR"], the first element ["AvsR"][0] being the trace and the second the retrace.
		"""
		self["AvsR"] = [[],[]]
		size_detect = size(self["detection"])
		for i in range(size_detect-2) :
			first = self["detection"][i]
			#I want to start with a trace above the threshold
			if first.trace == False or abs(first.value) < seuil :
				continue
			
			if (size_detect -i) < 4 :
				stop = size_detect - i
			else :
				stop = 4

			#Now I check the retrace that are at most i+3 farer (cf get_stat)
			for j in range(i+1,i+stop) :
				second = self["detection"][j]
				#I first check if they belong to the same sweep and if the threshold is reached
				if(second.sweep_nbr == first.sweep_nbr and abs(second.value) > seuil) :	
					#I check if first is really the last jump of the trace
					if second.trace == True :
						break
					
					#I check if don't use twice  <--- TO BE ADDED!!!
					#if second.trace == False and second.sweep_nbr == first.sweep_nbr :
					self["AvsR"][0].append(first.field)
					self["AvsR"][1].append(second.field)
				#if they do not belong to the same sweep_nbr -> break
				else :
					continue	
		
	def sort_data(self,seuil,offset) :
		"""
		This function sort the jumps first according to trace and retrace and then according to the kind of transition, either up or done. For more information on the label up and down, please refer to the documentation of get_jump2.
		"""
		self["sort"] = dict()
		self["sort"]["trace"] = dict()
		self["sort"]["trace"]["up"] = []
		self["sort"]["trace"]["down"] = []
		self["sort"]["retrace"] = dict()
		self["sort"]["retrace"]["up"] = []
		self["sort"]["retrace"]["down"] = []
		for i in range(size(self["detection"])) :
                        topush = self["detection"][i]
			if topush.trace == True and abs(topush.value) > seuil :
				if topush.up == False :
					self["sort"]["trace"]["down"].append(topush.field)
				else :
					self["sort"]["trace"]["up"].append(topush.field)
			if topush.trace == False and abs(topush.value) > seuil :
				if topush.up == False :
					self["sort"]["retrace"]["down"].append(topush.field - offset)
				else :
					self["sort"]["retrace"]["up"].append(topush.field - offset)
		return True
	
	def get_double(self,seuil,offset):
		self["double"] = dict()
		self["double"]["trace"] = [[],[]]
		self["double"]["retrace"] = [[],[]]
		tot_size = size(self["detection"])
		itera = int(tot_size/4)
		for i in range(itera) :
			trace1 = self["detection"][4*i]
			trace2 = self["detection"][4*i+1]
			retrace1 = self["detection"][4*i+2]
			retrace2 = self["detection"][4*i+3]
			if(abs(trace1.value) > seuil and abs(trace2.value) > seuil) :
				self["double"]["trace"][0].append(trace1.field)
				self["double"]["trace"][1].append(trace2.field)
			if(abs(retrace1.value) > seuil and abs(retrace2.value) > seuil ):
				self["double"]["retrace"][0].append(retrace1.field)
				self["double"]["retrace"][1].append(retrace2.field)
			

	def get_value_stat(self) :
		self["value_stat"] =[]
		for i in range(size(self["detection"])) :
			self["value_stat"].append(self["detection"][i].value)
		figure()
		hist(log10(abs(array(self["value_stat"]))),200)
		return True


########################################################
###This part is dedicated to saving and loading the data
###

	def save_all(self,tracefile,retracefile,whole_experiment) :
		"""
		This function allows to save the data in binary format. This make them faster to load. The syntax is as follow : save_all(filename_for_trace,filename_for_retrace,filename_for_data_extracted)
		"""
		self.trace.savez(tracefile)
		self.retrace.savez(retracefile)
		self["filenames"] = [tracefile+".npz", retracefile+".npz"]
		self.ready_to_save()
		self.save(whole_experiment)
		self.post_loading()


	def load_bin(self,mode="npz") :
		"""
		to be documented latter
		"""
		self.trace = sweep_set_open(self["filenames"][0],mode)
		self.retrace = sweep_set_open(self["filenames"][1],mode)
		print ("Sanity checks")
		print ("* Trace")
		self.trace.sanity_check()
		print ("* Retrace")
		self.retrace.sanity_check()

	def ready_to_save(self) :  
		i = 0
		for x in self["detection"]  :
		    self["detection"][i ] = x.pass_array()
		    i = i+1

	def post_loading(self) :
		for i in range(len(self["detection"])) :
			self["detection"][i] = Stat_point(self["detection"][i])
