
class Polar :
	"""
	This class is used to handle data stored in a json file. It takes a jsonfile as argument ang generate an object that makes data easier to manipulate
	"""
	def __init__(self,filename,A=0,B=0) :
		self._data = extracjson(filename)
		self._sweep_number = size(self._data["measures"])
		self._theta = [self._data["measures"][0]["theta"] , self._data["measures"][self._sweep_number - 1]["theta"] ]
		self._rho = [-0.5,0.5]
		self._make_matrix(A,B) 

	def _make_matrix(self,A,B):
		self.real = []
		th = linspace(self._theta[0], self._theta[1], self._sweep_number)
		for i in range(len(self._data["measures"])):
			Si = size(colarray_pol(self._data["measures"][0]["data"],A,B,th[i]))
			if size(colarray_pol(self._data["measures"][i]["data"],A,B,th[i])) < Si :
				c = colarray_pol(self._data["measures"][i]["data"],A,B,th[i])
				c.append(colarray_pol(self._data["measures"][i]["data"],A,B,th[i])[Si-2])
				self.real.append(c)
			if size(colarray_pol(self._data["measures"][i]["data"],A,B,th[i])) > Si :
				c = colarray_pol(self._data["measures"][i]["data"],A,B,th[i])
				c.pop(Si)
				self.real.append(c)
			if size(colarray_pol(self._data["measures"][i]["data"],A,B,th[i])) == Si :
				self.real.append(colarray_pol(self._data["measures"][i]["data"],A,B,th[i]))

	def map_phase(self,delta,offset):
		Si = size(colarray(self._data["measures"][0]["data"],0,0))
		th = linspace(self._theta[0]+delta, self._theta[1]+delta, self._sweep_number)
		r = linspace(self._rho[0], self._rho[1], Si) 
		self.f= figure()
		self.ax = subplot(111, projection = 'polar')
		self.p= self.ax.pcolormesh(th,r, array(matrix(array(self.real)-offset).transpose()))
		self.p.set_cmap(cmap =french)
		self.ax.set_rmax(abs(max(self._rho)))
		self.cb = self.f.colorbar(self.p)
