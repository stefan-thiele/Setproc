"""
Here are gathered the class dedicated to coulomb maps. Now, with the new javascripts,
"""

class Map(ToSaveObject) :
    """
    This class is used to handle data stored in a json file. It takes a jsonfile as argument ang generate an object that makes data easier to manipulate
    """
    def __init__(self,filename,Xchannel,Ychannel,mode = "Json") :
        ToSaveObject.__init__(self)

        if mode == "Json" :
            temp = OpenJson(filename)
        elif mode == "Bin" :
            temp = OpenBin(filename)

        for x in temp :
            self[x] = temp[x]
        del(temp)

        if mode == "Json" :
            self["data"] = matrix(self["data"]).transpose().tolist()

        X = self["metadata"][Xchannel]
        Y = self["metadata"][Ychannel]
        self["extent"] = [X["min"],X["max"],Y["min"],Y["max"]]

    def map_phase(self) :
        self.fig = figure()
        self.ax = self.fig.add_subplot(111)
        self.im = imshow(self["data"], interpolation = "nearest", origin="lower",extent = self["extent"])
        self.col = self.fig.colorbar(self.im)
        self.ax.set_aspect("auto")

    def plot_prof(self) :
        return plot_profile(self.im)

    def plot_prof_h(self) :
        return plot_profile_h(self.im)

    def get_coupling(self):
        return get_coupling()

    def check_merge(self,other):
        return check_merge_map(self,other)

    def merge(self,other):
        return map_merge(self,other)

