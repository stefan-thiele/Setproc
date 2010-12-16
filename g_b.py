import enthought.traits.api as eta
import enthought.traits.ui.api as etua



class GB_gui(eta.HasTraits) :
	a = None
	nbr_sweep = eta.Int
	width = eta.Int
	lunch = eta.Button
	f = None

	def __init__(self, A, nbr_sweep=0, width=9) :
		self.nbr_sweep = nbr_sweep
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

class GB_Json :
	"""
	This is the new class Json file that should generate in an esasier way, the correct plot with the correct axis.
	"""
	def __init__(self,filename):
		self._data = extracjson(filename)
		self._inputs = getinputs(self._data)
		self._outputs = getoutputs(self._data)
		self._sweep_number = size(self._data["measures"])
		self._pylab = self._data["pylab"]

	def plot_curve(self,nbr,w=9) :
		self.fig = figure()
		si = size(get_GB(self._data,1,nbr))
		self.ax = self.fig.add_subplot(211)
		plot(get_GB(self._data,1,nbr),get_GB(self._data, 0,nbr))
		self.ax.set_xlim(get_GB(self._data,1,nbr)[0],get_GB(self._data,1,nbr)[si-1])
		self.ax = self.fig.add_subplot(212)
		self.ax.set_xlim(get_GB(self._data,1,nbr)[0],get_GB(self._data,1,nbr)[si-1])
		plot(get_GB(self._data,1,nbr)[(w-1):si-(w-1)],pic_detect(get_GB(self._data,0,nbr),w))
		
	def get_jump(self,nbr,i_start,seuil,w=9) :
		state = False
		si = size(get_GB(self._data,1,nbr))
		bsweep = get_GB(self._data,1,nbr)[i_start+(w-1):si-(w-1)]
		jump = pic_detect(get_GB(self._data,0,nbr)[i_start:],w)
		max_jump = max(jump)
		if max_jump > seuil :
			state = True	
		return [ bsweep[jump.index(max_jump)], state]

	def get_sweep(self,nbr) :
		return [get_GB(self._data,1,nbr),get_GB(self._data, 0,nbr)]

	
	def get_stat(self,seuil,i_start,w=9):
		self.stat = []
		for i in range(self._sweep_number): 
			temp = self.get_jump(i,i_start,seuil,w)
			if(temp[1]):
				self.stat.append(temp[0]) 
		return True



class GB_pic_Json :
	"""
	This is the new class Json file that should generate in an esasier way, the correct plot with the correct axis.
	"""
	def __init__(self,filename):
		self._data = extracjson(filename)
		self._inputs = getinputs(self._data)
		self._outputs = getoutputs(self._data)
		self._sweep_number = size(self._data["measures"])
		self._pylab = self._data["pylab"]

	def plot_curve(self,nbr) :
		self.fig = figure()
		self.ax  = self.fig.add_subplot(111)
		plot(get_GB(self._data,1,nbr),get_GB(self._data, 0,nbr))

	def get_jump(self,nbr,i_start) :
		bsweep = get_GB(self._data,1,nbr)[i_start:]
		jump = get_GB(self._data,2,nbr)[i_start:]
		return bsweep[jump.index(max(jump))]

	def get_stat(self,seuil,i_start):
		self.stat = []
		for i in range(self._sweep_number):
			if(max(get_GB(self._data,2,i))>seuil):  #J'ai remplace 0 par 2... voir si ca marche
				self.stat.append(self.get_jump(i,i_start)) 
		return True

	def get_hist(self,nbr_pts,rge) :
		self.hist = hist(self.stat, nbr_pts,rge)





class new_GB :
		
	def __init__(self,A,R,picA,picR):
		self._A = GB_Json(A)
		self._R = GB_Json(R)
		self._picA = GB_pic_Json(picA)
		self._picR =  GB_pic_Json(picR)

	def get_stat(self,seuil) :
		self._picA.get_stat(seuil)
		self._picR.get_stat(seuil)

	def get_hist(self,nbr,rge) :
		self._picA.get_hist(nbr,rge)
		self._picR.get_hist(nbr,rge)

	def get_cycle(self,colr) :
		SA= sum_over(self._picA.hist[0])
		SR= sum_over(self._picR.hist[0])
		normA = max(SA)
		normR = max(SR)
		self.pA = plot(self._picA.hist[1][0:size(SA)],2 * (array(SA)/(1.* normA) - 0.5), linewidth = 3, color = colr )
		self.pR = plot(self._picR.hist[1][0:size(SA)],2 * (array(SR)/(1.* normR) - 0.5), linewidth = 3, color = colr )

