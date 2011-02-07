import enthought.traits.api as eta
import enthought.traits.ui.api as etua
import os as os


class GB_gui(eta.HasTraits) :
	
	nbr_sweep = eta.Range(0,500,1)
	width = eta.Int
	"""
	lunch = eta.Button
	f = None
	"""
	def __init__(self, A,width=9) :
		self.width = width
		self.a=A

	def _lunch_fired(self) :
		self.a.plot_curve(self.nbr_sweep, self.width)

	def _nbr_sweep_changed(self) :
		self.a.plot_curve(self.nbr_sweep, self.width)
	"""
	def _width_changed(self) :
		self.a.plot_curve(self.nbr_sweep, self.width)
	"""


class GB_Open(Measure) :
	"""
	This is the new class Json file that should generate in an esasier way, the correct plot with the correct axis.
	"""
	def __init__(self,filename,mode):
		Measure.__init__(self,filename,mode)
		
	def plot_curve(self,nbr,w=9) :
		try :
			self.fig.clear()
			self.ax.clear()
		except :
			self.fig = figure()
		X = self["bias"]
		Y = self["data"][nbr]
		si = size(self["bias"])
		self.ax = self.fig.add_subplot(211)
		plot(X,Y)
		self.ax.set_xlim(X[0],X[si-1])
		self.ax = self.fig.add_subplot(212)
		self.ax.set_xlim(X[0],X[si-1])
		plot(X[(w-1):si-(w-1)],pic_detect(Y,w))
		return True
		
	def get_jump(self,nbr,i_start,seuil,w=9) :
		state = False
		si = size(self["bias"])
		bsweep = self["bias"][i_start+(w-1):si-(w-1)]
		jump = pic_detect(self["data"][nbr][i_start:],w)
		max_jump = max(jump)
		if max_jump > seuil :
			state = True	
		return [ bsweep[jump.index(max_jump)], state]

	def get_sweep(self,nbr) :
		return [self["bias"],self["data"][nbr]]

	
	def get_stat(self,seuil,i_start,w=9):
		self["stat"] = []
		for i in range(self["sweep_number"]): 
			temp = self.get_jump(i,i_start,seuil,w)
			if(temp[1]):
				self["stat"].append(temp[0]) 
		return True
	
	def get_hist(self,nbr_pts,rge,stat_name) :
		temp = hist(self[stat_name], nbr_pts,rge)
		self["hist"] = [temp[0],temp[1]]
		return True



class Pic_Open(Measure) :
	"""
	This is the new class Json file that should generate in an esasier way, the correct plot with the correct axis.
	"""
	def __init__(self,filename,mode):
		Measure.__init__(self,filename,mode)
	
	def _inter_stat(self,trace) :
		temp = []
		data = []
		XA = trace["bias"] #attention le bias du pic a moins de point !!
		XP = self["bias"]
		SA = size(trace["bias"])
		SP = size(self["bias"])
		fig = figure()
		fig.set_size_inches(16.7  ,  10.575)
 		for i in range(3) : #self["sweep_number"]) :
			fig.clf()
			YA = trace["data"][i]
			YP = self["data"][i]
			#plot de la trace ( YA=f(XA) )
			ax = fig.add_subplot(211)
			plot(XA,YA)
			ax.set_xlim(XA[0],XA[SA-1])
			#plot du pic
			ax = fig.add_subplot(212)
			ax.set_xlim(XA[0],XA[SA-1])
			plot(XP,YP)
			temp = ginput()
			if size(temp) > 0 :
				tosave = temp[0][0] #seulement le champ	
				######This should be improved in order to get the real max
				#print tosave
				#pos = XP.index(tosave)
				#toput = max(YP[(pos-window/2),(pos+window/2)])
				##################
				data.append(tosave) 
		close(fig)
		return data

	def plot_curve(self,nbr) :
		self.fig = figure()
		self.ax  = self.fig.add_subplot(111)
		x = self["bias"]
		y = self["data"][nbr]
		plot(x,y)

	def get_jump(self,nbr,i_start) :
		bsweep = self["bias"][i_start:]
		jump = self["data"][nbr][i_start:]
		return bsweep[jump.index(max(jump))]

	def get_stat(self,seuil,i_start):
		self["init_stat"] = []
		for i in range(self["sweep_number"]) :	
			try :
				if(max(self["data"][i])>seuil) :
					self["init_stat"].append(self.get_jump(i,i_start))
			except :
				print "No data in the sweep"
		return True

	def get_hist(self,nbr_pts,rge,stat_name) :
		temp = hist(self[stat_name], nbr_pts,rge)
		self["hist"] = [temp[0],temp[1]]
		return True

	def new_stat(self,stat_name,trace) :
		self[stat_name] = self._inter_stat(trace)
		return True 



class probar_pic(Measure) :
	
	def __init__(self,filename,mode):
		OpenMeasures.__init__(self,filename,mode)
		self["cycle_number"] = size(self["data"])
		"""
		self.pylab = None
		self.bias = None
		self.sweep_number = None
		self.data
		"""

	def get_stat(self):
		self["stat"] = []
		for i in range(self["cycle_number"]):
			self["stat"].append(self["data"][i]["info"]["try_nbr"])
		
		return True	
		
	def get_histogram(self,nbr,rge) :
		self["histogram"] = histogram(self["stat"],nbr,rge)

	def get_hist(self,nbr,rge) :
		self["histogram"] = hist(self["stat"],nbr,rge)

	def plot_jump(self,nbr):
		tmp_si = len(self["data"][nbr]["data"])
		X = self["data"][nbr]["bias"][tmp_si-2]
		Y = self["data"][nbr]["data"][tmp_si-2]
		f=gcf()
		f.clf()
		plot(X,Y)
	def get_sweep_jump(self,nbr) :
		tmp_si = len(self["data"][nbr]["data"])
		X = self["data"][nbr]["bias"][tmp_si-2]
		Y = self["data"][nbr]["data"][tmp_si-2]
		return [X,Y]

	def get_stat_jumps(self,w,seuil):
		self["jump_stat"] = []
		stat_temp = []
		for i in range(self["cycle_number"]) :
			X,Y = self.get_sweep_jump(i)
			tpsi = size(X)
			Yp = pic_detect(Y,w)
			temp = who_above(X[w-1:tpsi-w+1],Yp,seuil)
			stat_temp.append(temp)
		for i in range(len(stat_temp)) :
			for j in range(size(stat_temp[i])) :
				self["jump_stat"].append(stat_temp[i][j])


		return True




class new_GB(Measure) :
		
	def __init__(self,files="here",mode="Bin"):
		
		if( size(files) == 1 ) :
			Measure.__init__(self,files[0],"Bin")
			try :
				print self["with_pic"]
			except KeyError :
				self["with_pic"] = True	
	
		if( size(files) > 3 ) :
			folder = os.getcwd()+"/"
			self["filenames"] = dict([])
			self["filenames"]["A"] = folder+files[0]
			self["filenames"]["R"] = folder+files[1]
			self["filenames"]["PicA"] = folder+files[2]
			self["filenames"]["PicR"] = folder+files[3]
			self["filenames"]["mode"] = mode
			self["comments"] = ""
			self["with_pic"] = True
			
		if( size(files) > 1 and size(files) < 3 ) :
			folder = os.getcwd()+"/"
			self["filenames"] = dict([])
			self["filenames"]["A"] = folder+files[0]
			self["filenames"]["R"] = folder+files[1]
			self["filenames"]["mode"] = mode
			self["comments"] = "Data registred without the original Pic files"
			self["with_pic"] = False
		

	def load_files(self) :
		self._A = GB_Open(self["filenames"]["A"],self["filenames"]["mode"])
		self._R = GB_Open(self["filenames"]["R"],self["filenames"]["mode"])
		if (self["with_pic"]) :
			self._picA = Pic_Open(self["filenames"]["PicA"],self["filenames"]["mode"])
			self._picR =  Pic_Open(self["filenames"]["PicR"],self["filenames"]["mode"])


	def get_stat(self,seuil,i_start) :
		self._picA.get_stat(seuil,i_start)
		self._picR.get_stat(seuil,i_start)

	def get_hist(self,nbr,rge,stat_name) :
		self._picA.get_hist(nbr,rge,stat_name)
		self._picR.get_hist(nbr,rge,stat_name)

	def get_cycle(self,colr,offset) :
		HA = self._picA["hist"]
		HR = self._picR["hist"]
		SA= sum_over(HA[0])
		SR= sum_over(HR[0])
		norm = self._A["sweep_number"]
		self.pA = plot(array(HA[1][0:size(SA)])-offset,2 * (array(SA)/(1.* norm) - 0.5), linewidth = 3, color = colr )
		self.pR = plot(array(HR[1][0:size(SA)]) + offset,2 * (array(SR)/(1.* norm) - 0.5), linewidth = 3, color = colr )

	def get_cycle_trace(self,colr,offset) :
		HA = self._A["hist"]
		HR = self._R["hist"]
		SA= sum_over(HA[0])
		SR= sum_over(HR[0])
		norm = self._A["sweep_number"]
		self.pA = plot(array(HA[1][0:size(SA)])-offset,2 * (array(SA)/(1.* norm) - 0.5), linewidth = 3, color = colr )
		self.pR = plot(array(HR[1][0:size(SA)]) + offset,2 * (array(SR)/(1.* norm) - 0.5), linewidth = 3, color = colr )

	def newstat_A(self,statname) :
		self._picA.new_stat(statname,self._A)
		return True


	def newstat_R(self,statname) :
		self._picR.new_stat(statname,self._R)
		return True

	def save_all(self,A=None,R=None,picA=None,picR=None):
	
		#makes sure that if the dict filenames does not exist, it is created
		try :
			self["filenames"]
		except KeyError:
			self["filenames"] = dict([])

		#verifies if the whole experiment has been at least saved once
		try :
			print self["filenames"]["own"]
		except KeyError :
			print "Save the full experiment as\n"
			self["filenames"]["own"] = input("Filename (must be a string) : ")
		
	
		if(A == None and self["filenames"]["mode"] != "Bin"):
			print "You must specify filenames the first time you save in Bin mode \n"
		else :
			self._A.save(A)
			self._R.save(R)
			if (self["with_pic"]) :
				self._picA.save(picA)
				self._picR.save(picR)

		if(A != None) :
			folder = os.getcwd()+"/"
			self["filenames"]["A"] = folder+A
			self["filenames"]["R"] = folder+R
			if (self["with_pic"]) :
				self["filenames"]["PicA"] = folder+picA
				self["filenames"]["PicR"] = folder+picR
			self["filenames"]["mode"] = "Bin"
		filename = self["filenames"]["own"]
		self.save(filename)	
		return True
