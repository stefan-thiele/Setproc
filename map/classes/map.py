from setproc.map.functions.map_functions import plot_profile_h, plot_profile, get_coupling, map_merge, check_merge_map
from setproc.common.classes.to_save_object import ToSaveObject
from setproc.common.classes.open_json import OpenJson
from setproc.common.classes.open_bin import OpenBin
from numpy import matrix, log10
from matplotlib.pyplot import figure, imshow

class Map(ToSaveObject) :
    """
    This class is used to handle data stored in a json file. It takes a jsonfile as argument ang generate an object that makes data easier to manipulate
    """
    def __init__(self, filename, Xchannel, Ychannel, mode = "Json") :
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
        self["extent"] = [X["min"], X["max"], Y["min"], Y["max"]]
        self.check(X["min"], X["max"])

    def map_phase(self) :
        self.fig = figure()
        self.ax = self.fig.add_subplot(111)
        self.im = imshow(self["data"], interpolation = "nearest", origin="lower", extent = self["extent"])
        self.col = self.fig.colorbar(self.im)
        self.ax.set_aspect("auto")

    def plot_prof(self) :
        return plot_profile(self.im)

    def plot_prof_h(self) :
        return plot_profile_h(self.im)

    def get_coupling(self):
        return get_coupling()

    def check_merge(self, other):
        return check_merge_map(self, other)

    def merge(self, other):
        return map_merge(self, other)

    def check(self, xmin, xmax) :
        if xmin > xmax :
            self.reverse_data()
        return True

    def log_scale(self):
        self["datalog"] = log10(self["data"])

    def map_log(self):
        self.log_scale()
        self.fig_log = figure()
        self.ax_log = self.fig_log.add_subplot(111)
        self.im_log = imshow(self["datalog"], interpolation = "nearest", origin="lower", extent = self["extent"])
        self.col_log = self.fig_log.colorbar(self.im_log)
        self.ax_log.set_aspect("auto")

    def reverse_data(self):
        #swapt the extent elements
        temp = self["extent"][0]
        self["extent"][0] = self["extent"][1]
        self["extent"][1] = temp
        data_tp = self["data"]
        data_tp = matrix(data_tp).transpose().tolist()
        data_tp.reverse()
        self["data"] = matrix(data_tp).transpose().tolist()
        return True

    def __add__(self,other):
        self.merge(other)


    def __mod__(self,other):
        self.check_merge(other)



