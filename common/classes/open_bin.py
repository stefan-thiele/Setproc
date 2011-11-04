import cPickle

class OpenBin(dict):
    """
    This class create an OpenBin object given a binary file generated from a measurement
    """
    def __init__(self, filename) :
        dict.__init__(self)
        self.load_bin(filename)

    def load_bin(self, filename) :
        done = True
        try :
            stream = open(filename,"r")
        except IOError :
            print "Problem while loading the binary file. Check the file name and/or the folder"
            done = False

        temp = cPickle.load(stream)
        stream.close()
        X = temp[0]
        i = 1
        for x in X :
            self[x] = temp[i]
            i += 1
        return done
