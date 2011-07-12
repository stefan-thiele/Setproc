"""
This code originates from g_b.py and has been modified. From now on, it is located into the lib folder.
"""


class sweep_set_open(Measure) :
	"""
	sweep_set_open depends on the object Measures. Its aim is to provide all the functions needed in order to process the data of a set of several sweeps. It takes as argument a filename and its format (either "Json" or "Bin").The avaible functions are the following : plot_curve , get_jump, get_jump2, get_jump3, get_sweep, get_stat_old, get_stat, get_hist, sanity_check. For further information on each one of these functions, please refer to the specific doc.
	"""
	def __init__(self,filename,mode):
		"""
		The constructeur uses the one of the Measure object. The argument are the filename and its format (either "Json" or "Bin")
		"""
		Measure.__init__(self,filename,mode)
		
	def plot_curve(self,nbr,i_start,w=4) :
		"""
		This function allows to plot a curve corresponding to a specific sweep as well as the filtred result. The syntax is the follwing : plot_curve(nbr,i_stat,w) where nbr is the sweep number (it starts from zero), i_stat is the number of points to skip from the beginning and w is the width of the filter ( the one used is pic_detect2, see the filter doc for more informations)
		"""
		try :
			self.fig.clear()
			self.ax1.clear()
			self.ax2.clear()
		except :
			self.fig = figure()
		X = self["bias"][i_start:]
		Y = self["data"][nbr][i_start:]
		si = size(self["bias"][i_start:])
		self.ax1 = self.fig.add_subplot(211)
		self.ax1.plot(X,Y)
		self.ax1.set_xlim(X[0],X[si-1])
		self.ax2 = self.fig.add_subplot(212)
		self.ax2.plot(X[(w-1):si-(w-1)],pic_detect_2(Y,w))
		self.ax2.set_xlim(X[0],X[si-1])
		#this function redraws all the figure of the environment
		for i in get_fignums() :
			figure(i)
			draw()
			show()
		return True


	def get_jump(self,nbr,i_start,seuil,w=4) :
		"""
		This function filter a given sweep using pic_detect() and spot the position of a jump in the sweep. The syntax is as follow : get_jump(nbr,i_start,seuil,w) where nbr is the sweep number (starting from zero), i_start is the number of points to skip from zero, seuil is the threshold of the detection and w is the width of the filter (see the filter doc for more information). The returned value is a list [b_jump,v_jum,state] where b_jump is the X value for which the jump occured and v_jump is its value in a.u. of the filter. state is True if v_jump>seuil and False otherwise
		"""
		state = False
		si = size(self["bias"])
		bsweep = self["bias"][i_start+(w-1):si-(w-1)]
		jump = pic_detect(self["data"][nbr][i_start:],w)
		max_jump = max(jump)
		if max_jump > seuil :
			state = True	
		return [ bsweep[jump.index(max_jump)],max_jump, state]

	def get_jump_2(self,nbr,i_start,seuil,w=4) :
		"""
		This function filter a given sweep using pic_detect2() and spot the position of a jump in the sweep. The syntax is as follow : get_jump2(nbr,i_start,seuil,w) where nbr is the sweep number (starting from zero), i_start is the number of points to skip from zero, seuil is the threshold of the detection and w is the width of the filter (see the filter doc for more information)
		"""
		state = [False,False]
		si = size(self["bias"])
		bsweep = self["bias"][i_start+(w-1):si-(w-1)]
		temp_array = array(self["data"][nbr][i_start:], dtype = np.float)
		jump = pic_detect_2(temp_array,w)
		max_jump = max(jump)
		min_jump = min(jump)
		if min_jump < -1*seuil :
			state[0] = True
		if max_jump > seuil :
			state[1] = True
		return [ [ bsweep[jump.index(min_jump)], min_jump , state[0],nbr ], [ bsweep[jump.index(max_jump)] , max_jump, state[1],nbr]]


	def get_sweep(self,nbr) :
		"""
		This function return a list containing the [X,Y] of a given sweep. The syntax is get_sweep(nbr) with nbr the sweep number starting from zero.
		"""
		return [self["bias"],self["data"][nbr]]
	
	def get_stat_old(self,seuil,i_start,w=4) :
		"""
		This function goes through all the sweeps of the object to perform a get_jump and store the result into ["old_stat"], the first column corresponds to the X value of a jump and the seconde one to the filtered value. Only the jump with state equal to True are stored.
		"""
		self["old_stat"] = [[],[]]
		for i in range(self["sweep_number"]): 
			temp = self.get_jump(i,i_start,seuil,w)
			if(True):
				self["old_stat"][0].append(temp[0]) 
				self["old_stat"][1].append(temp[1])
		return True
	
	def get_stat(self,seuil,i_start,w=4):
		"""
		This function goes through all the sweeps of the object to perform a get_jump2 and store the result into ["stat"], the first column corresponds to the X value of a jump and the seconde one to the filtered value. Only the jump with state equal to True are stored.
		"""
		self["stat"] = [[],[]]
		for i in range(self["sweep_number"]): 
			temp = self.get_jump_2(i,i_start,seuil,w)
			if(True):
				self["stat"][0].append(temp[0]) 
				self["stat"][1].append(temp[1])
		return True
	
	def get_hist(self,nbr_pts,rge,stat_name,seuil="all") :
		"""
		This function return the histogram datat of the set of sweeps. It should be used only with a set of jumps obtained with get_stat_old. The syntax is the following get_hist(nbr_pts,range,stat_name,seuil) where nbr_pts is the bin number, range is the range to be used of the histogram on the X axis, stat_name is the name of the set of jumps obtained by get_stat_old (usually "old_stat").
		"""
		stat_temp = copy(self[stat_name]).tolist()
		size_stat_temp = size(stat_temp)/size(stat_temp[0])
		final_r = []
		if(seuil != "all"):
			for i in range(size_stat_temp_min) :
				if(seuil > stat_temp[size_stat_temp - (i+1)][1]) :
					stat_temp.pop(size_stat_temp - (i+1))
		
		for i in range((size(stat_temp)/size(stat_temp[0]))):
			final_r.append(stat_temp[i][0])
		
		temp_r = histogram(final_r, nbr_pts,rge)
		self["hist"] = [temp_r]
		return True


	def get_hist2(self,nbr_pts,rge,stat_name,seuil="all") :
		"""
		This function return the histogram data of the set of sweeps. It should be used only with a set of jumps obtained with get_stat. The syntax is the following get_hist(nbr_pts,range,stat_name,seuil) where nbr_pts is the bin number, range is the range to be used of the histogram on the X axis, stat_name is the name of the set of jumps obtained by get_stat (usually "stat").
		"""
		stat_temp_min = copy(self[stat_name][0]).tolist()
		stat_temp_max = copy(self[stat_name][1]).tolist()
		size_stat_temp_min = size(stat_temp_min)/size(stat_temp_min[0])
		size_stat_temp_max = size(stat_temp_max)/size(stat_temp_max[0])
		final_min = []
		final_max = []
		if(seuil != "all"):
			for i in range(size_stat_temp_min) :
				if(seuil < stat_temp_min[size_stat_temp_min - (i+1)][1]) :
					stat_temp_min.pop(size_stat_temp_min - (i+1))
			for i in range(size_stat_temp_max) :
				if(seuil > stat_temp_max[size_stat_temp_max - (i+1)][1]) :
					stat_temp_max.pop(size_stat_temp_max - (i+1))
		
		for i in range((size(stat_temp_min)/size(stat_temp_min[0]))):
			final_min.append(stat_temp_min[i][0])
		
		for i in range((size(stat_temp_max)/size(stat_temp_max[0]))):
			final_max.append(stat_temp_max[i][0])
		
		temp_min = histogram(final_min, nbr_pts,rge)
		temp_max = histogram(final_max, nbr_pts,rge)
		self["hist2"] = [temp_min,temp_max]
		return True

	def sanity_check(self) :
		"""
		This function insures that all the sweep have the same number of points, if not its uses the prvious point to complete the sweep and reports how many point at max add to be changed. If there is no error during acquition, this number should remains around unity due to round-up issues.
		"""
		size_bias = size(self["bias"])
		nbr = None
		temp = 0
		for i in range(self["sweep_number"]) :
			size_data = size(self["data"][i])

			if (size_data < size_bias ) :
				nbr = i
				for j in range(size_bias - size_data) :
					#recopie la derniere valeur pour completer
					self["data"][i].append(self["data"][i][size_data-j-1])
			if (size_data > size_bias ) :

				#recopie la derniere valeur pour completer
				self["data"][i] = self["data"][i][0:size_bias]
				nbr = i
			if (abs(size_data - size_bias) > temp ) :

				temp = abs(size_data - size_bias)
		if(nbr == None) :
			print "\tPerfect matching"
		else :
			print "\tThe maximum difference is ",temp," points with the sweep ",nbr
		
		return True
				

	def __add__(self,other) :
		"""
		This function allows to merge two set of sweeps using the syntax sweep1 + sweep2. The merging of the two is handled by the merg_GB functions. See merge_GB doc for more informations.
		"""
		return merge_GB([self,other])

