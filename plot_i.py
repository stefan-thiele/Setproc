from enthought.traits.api import HasTraits, Int, Range, Array, Enum
from enthought.enable.api import ColorTrait
from enthought.traits.ui.api import View, Group, Item
from enthought.chaco.api import marker_trait, Plot, ArrayPlotData
from enthought.enable.component_editor import ComponentEditor



from numpy import linspace, sin

class Plot_i(HasTraits):

	plot = Instance(Plot)
	color = ColorTrait('blue')
	marker = marker_trait
	marker_size = Int(4)
	line_width = Int(4)
	traits_view = View(Group(
        Group(
            Item('plot_type',label = 'type'),
            Item('color', label="Color"),
            Item('marker', label="Marker"),
            orientation = 'vertical'),
        Group(
            Item('marker_size', label= "Size"),
            Item('line_width', label = 'Linewidth'),
            orientation = 'vertical'),
        orientation = 'horizontal'),
        Item('plot', editor=ComponentEditor(), show_label=False),
        width=800, height=600, resizable=True, title="Chaco Plot")

    def __init__(self,X,Y):
        super(Plot_i, self).__init__()
		self.load_data(X,Y)
		self.start()

	def load_data(self,X,Y) :
		self.X = X
		self.Y = Y
		plotdata = ArrayPlotData(x = X, y = Y)
        plot = Plot(plotdata)
		self.renderer_line = plot.plot(('x','y'),type = 'line', color = "blue")[0]
		self.renderer_scat = plot.plot(('x','y'),type = 'scatter', color = "blue")[0]
		self.plot = plot

	def start(self):
		self.configure_traits()

	def _color_changed(self):
        self.renderer_line.color = self.color
		self.renderer_scat.color = self.color

	def _marker_changed(self):
        self.renderer_scat.marker = self.marker

	def _marker_size_changed(self):
        self.renderer_scat.marker_size = self.marker_size

	def _line_width_changed(self):
		self.renderer_line.line_width = self.line_width

