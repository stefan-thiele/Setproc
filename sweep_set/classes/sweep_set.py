from copy import deepcopy
from setproc.common.classes.open_json import OpenJson
from setproc.common.classes.open_bin import OpenBin
from setproc.sweep_set.classes.stat_point import Stat_point
from setproc.sweep_set.functions.extract_stat import extract_stat
from setproc.sweep_set.functions.merge_gb import merge_GB
from numpy import size, array, load
from pyplot import figure, draw, show, get_fignums
import numpy as np
import cPickle


exst = extract_stat




class sweep_set_open(dict) :
    """
    It generated an sweep_set_open object. Due to the huge data it can contains, the usual saving systeme can be replaced by npz format faster and more compact at a price of less versatility in what is saved (only "bias", "sweep_nbr" and "data")
    """
    def __init__(self, filename, mode) :
        dict.__init__(self)
        if mode == "npz" :
            temp = load(filename)
            for x in temp.files :
                self[x] = deepcopy(temp[x])
            del(temp)
        else :
            if mode == "Json" :
                temp = OpenJson(filename)
            elif mode == "Bin" :
                temp = OpenBin(filename)
            for x in temp :
                self[x] = deepcopy(temp[x])
            del(temp)


    def get_jump(self, nbr, i_start, w=4, power=1, sw=1, si = "None", mode ="classic", seuil1 = 0, seuil2 =0, span = 50) :
        up = Stat_point()
        down = Stat_point()
        if si == "None" :
            si = size(self["bias"])
        bsweep = self["bias"][i_start+(w-1)+sw/2:si-(w-1)-sw/2+1-sw%2]
        temp_array = array(self["data"][nbr][i_start:], dtype = np.float)
        jump = filter(temp_array, w, power, sw)
        if mode == "classic" :
            if( nbr == 0) :
                print("In classic mode")
            max_jump = jump.max()
            min_jump = jump.min()
            #construct up
            up.field = bsweep[jump.argmax()]
            up.value = max_jump
            up.up = True
            up.sweep_nbr = nbr
            #construct down
            down.field = bsweep[jump.argmin()]
            down.value = min_jump
            down.up = False
            down.sweep_nbr = nbr
        else :
            down.value, min_arg , up.value, max_arg = exst.extract_stat(jump, seuil1, seuil2, span)
            up.up = True
            up.sweep_nbr = nbr
            if max_arg < 0 :
                up.field = 0
            else :
                up.field = bsweep[max_arg]
                down.up = False
                up.sweep_nbr = nbr
            if min_arg < 0 :
                down.field = 0
            else :
                down.field = bsweep[min_arg]
        return down, up


    def sanity_check(self) :
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
            print "\tThe maximum difference is ", temp, " points with the sweep ", nbr

        return True


    def __add__(self, other) :
        return merge_GB([self, other])

    ##To plot and acess
    def plot_curve(self, nbr, i_start, w=4, pw = 1, sw = 1) :
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
        self.ax1.plot(X, Y)
        self.ax1.set_xlim(X[0], X[si-1])
        self.ax2 = self.fig.add_subplot(212)
        self.ax2.plot(X[(w-1)+sw/2:si-(w-1)-sw/2 +1 -sw%2], filter(np.array(Y), w, pw, sw))
        self.ax2.set_xlim(X[0], X[si-1])
        for i in get_fignums() :
            figure(i)
            draw()
        show()
        return True

    def get_sweep(self, nbr) :
        return [self["bias"], self["data"][nbr]]


    def save(self, savename) :
        """
        Save all the keys field of a dictionnary in savename file. The "*.bin" extension should be used
        """
        done = True
        try :
            stream = open(savename, "w")
        except IOError :
            print "Problem while saving the file"
            done = False
        l = []
        temp = self.keys()
        l.append(temp)
        for x in self:
            l.append(self[x])
        cPickle.dump(l, stream, 1)
        return done

    def savez(self, filename) :
        np.savez(filename, data = self["data"], bias= self["bias"], sweep_number = self["sweep_number"])

