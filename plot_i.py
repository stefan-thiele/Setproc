"""
This  Object allow a better manipulation of the 2D plot
"""
import pylab as plt

class plot_i():
	""""
	In the end, should be used instead of the classic commend plot of pyplot
	"""
	def __init__(self, X, Y, **args):
		self.fig = plt.figure()
		self.ax = self.fig.add_subplot(111)
		self.ax.plot(X, Y, **args)
    
	def set_xlabel(self, Xlabel):
		self.ax.set_xlabel(Xlabel)

	def set_xlabel_size(self,size):
		label = self.ax.get_xlabel()
		self.ax.Set_xlabel(lable, size = size)
		
    
	def set_ylabel(self, Ylabel):
		self.ax.set_ylabel

	def set_ya

	
