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
		#self._name_default()

	def _lunch_fired(self) :
		self.a.plot_curve(self.nbr_sweep, self.width)

	def _nbr_sweep_changed(self) :
		self.a.plot_curve(self.nbr_sweep, self.width)
"""
	def _width_changed(self) :
		self.a.plot_curve(self.nbr_sweep, self.width)
"""

class GB_Open(OpenMeasures) :
	"""
	This is the new class Json file that should generate in an esasier way, the correct plot with the correct axis.
	"""
	def __init__(self,filename,mode):
		OpenMeasures.__init__(self,filename,mode)
		"""
		self.pylab = None
		self.bias = None
		self.sweep_number = None
		self.data
		"""

	def plot_curve(self,nbr,w=9) :
		try :
			self.fig.clear()
			self.ax.clear()
		except :
			self.fig = figure()
		#self.fig.clf()
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



class Pic_Open(OpenMeasures) :
	"""
	This is the new class Json file that should generate in an esasier way, the correct plot with the correct axis.
	"""
	def __init__(self,filename,mode):
		OpenMeasures.__init__(self,filename,mode)
		"""
		self.pylab = None
		self.bias = None
		self.sweep_number = None
		self.data
		"""
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





class new_GB(dict) :
		
	def __init__(self,A=None,R=None,picA=None,picR=None,mode="Bin",comment = None):
		dict.__init__(self)
		if(A != None) :
			folder = os.getcwd()+"/"
			self["filenames"] = dict([])
			self["filenames"]["A"] = folder+A
			self["filenames"]["R"] = fodler+R
			self["filenames"]["picA"] = foldr+picA
			self["filenames"]["picR"] = folder+picB
			self["filenames"]["mode"] = mode
			self["comments"] =  comment
			
	return True

	def load_data(self) :
		self._A = GB_Open(self["filenames"]["A"],self["filenames"]["mode"])
		self._R = GB_Open(self["filenames"]["R"],self["filenames"]["mode"])
		self._picA = Pic_Open(pself["filenames"]["PicA"],self["filenames"]["mode"])
		self._picR =  Pic_Open(pself["filenames"]["PicR"],self["filenames"]["mode"])


	def get_stat(self,seuil,i_start) :
		self._picA.get_stat(seuil,i_start)
		self._picR.get_stat(seuil,i_start)

	def get_hist(self,nbr,rge,stat_name) :
		self._picA.get_hist(nbr,rge,stat_name)
		self._picR.get_hist(nbr,rge,stat_name)

	def get_cycle(self,colr) :
		HA = self._picA["hist"]
		HR = self._picR["hist"]
		SA= sum_over(HA[0])
		SR= sum_over(HR[0])
		normA = max(SA)
		normR = max(SR)
		self.pA = plot(HA[1][0:size(SA)],2 * (array(SA)/(1.* normA) - 0.5), linewidth = 3, color = colr )
		self.pR = plot(HR[1][0:size(SA)],2 * (array(SR)/(1.* normR) - 0.5), linewidth = 3, color = colr )

	def newstat_A(self,statname) :
		self._picA.new_stat(statname,self._A)
		return True


	def newstat_R(self,statname) :
		self._picR.new_stat(statname,self._R)
		return True

	def save(self,A,R,picA,picR):
		
		if(A == None and self["filenames"]["mode"] != "Bin"):
			print "You must specify filenames the first time you save in Bin mode \n"
		else :
			self._A.save(A)
			self._R.save(R)
			self._picA.save(picA)
			self._picA.save(picR)

		if(A != None) :
			folder = os.getcwd()+"/"
			self["filenames"] = dict([])
			self["filenames"]["A"] = folder+A
			self["filenames"]["R"] = fodler+R
			self["filenames"]["picA"] = foldr+picA
			self["filenames"]["picR"] = folder+picB
			self["filenames"]["mode"] = "Bin"
		
		return True
