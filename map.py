"""
Here are gathered the class dedicated to coulomb maps. Now, with the new javascripts,
"""

class Map(ToSaveObject) :
    """
    This class is used to handle data stored in a json file. It takes a jsonfile as argument ang generate an object that makes data easier to manipulate
    """
    def __init__(self,filename,xmin,xmax,ymin,ymax,mode = "Json") :
        ToSaveObject.__init__self(self)
        if mode == "Json" :
            data = get_json(filename)
            temp_data = getcolumns(data, getposcolumn(data,"real"), self._sweep_number)

            self["data"] = matrix(temp_data).transpose().tolist()
            self["extent"] = [xmin,xmax,ymin,ymax]
            self["inputs"] = getinputs(data)
            self["outputs"] = getoutputs(data)
            self["sweep_number"] = size(self["data"])
        elif mode == "Bin" :
            temp = OpenBin(filename)
            for x in temp :
                self[x] = temp[x]
            del(temp)


    def map_phase(self) :
        self.fig = figure()
        self.ax = self.fig.add_subplot(111)
        self.im = imshow(self["data"], origin="lower",extent = self["extent"])
        self.col = self.fig.colorbar(self.im)
        self.ax.set_aspect("auto")

    def plot_prof(self) :
        return plot_profile(self.im)

    def plot_prof_h(self) :
        return plot_profile_h(self.im)

    def get_coupling(self):
        return get_coupling()

