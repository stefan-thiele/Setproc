import cPickle
from copy import deepcopy


class Measure(dict) :
    """
    This allows to parse a json file and generate a python object from it. The argument to be given is the filename of the json file. The function returns the data in a python object format.
    """
    def __init__(self, filename, mode) :
        dict.__init__(self)
        if mode == "Json" :
            temp = OpenJson(filename)
        elif mode == "Bin" :
            temp = OpenBin(filename)
        for x in temp :
            self[x] = deepcopy(temp[x])
        del(temp)


    def save(self, savename) :
        """
        Save all the keys field of a dictionnary in savename file. The "*.bin" extension should be used
        """
        done = True
        try :
            stream = open(savename,"w")
        except IOError :
            print "Problem while saving the file"
            done = False
        l = []
        temp = self.keys()
        l.append(temp) # this will be used when loading the file to set the keys of the dictionnary created
        for x in self:
            l.append(self[x])
        cPickle.dump(l, stream, 1)

        return done
