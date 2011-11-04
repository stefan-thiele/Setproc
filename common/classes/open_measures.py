"""
@uthor : Romain Vincent
Created 10/12/2010

This file contains the classes that handle the opening and saving of the measures.All functions specific to this method should be defined in this file
"""


class ToSaveObject(dict) :

    def __init__(self) :
        dict.__init__(self)


    def save(self,savename) :
        """
        Save all the keys field of a dictionnary in savename file. The "*.bin" extension should be used
        """
        done = True
        try :
            stream = open(savename,"w")
        except IOError :
            print "Problem while saving the file"
            done = False
        l =[]
        temp = self.keys()
        l.append(temp) # this will be used when loading the file to set the keys of the dictionnary created
        for x in self:
            l.append(self[x])
        cPickle.dump(l,stream,1)

        return done





class Measure(dict) :
    """
    This allows to parse a json file and generate a python object from it. The argument to be given is the filename of the json file. The function returns the data in a python object format.
    """
    def __init__(self,filename,mode) :
        dict.__init__(self)
        if mode == "Json" :
            temp = OpenJson(filename)
        elif mode == "Bin" :
            temp = OpenBin(filename)
        for x in temp :
            self[x] = deepcopy(temp[x])
        del(temp)


    def save(self,savename) :
        """
        Save all the keys field of a dictionnary in savename file. The "*.bin" extension should be used
        """
        done = True
        try :
            stream = open(savename,"w")
        except IOError :
            print "Problem while saving the file"
            done = False
        l =[]
        temp = self.keys()
        l.append(temp) # this will be used when loading the file to set the keys of the dictionnary created
        for x in self:
            l.append(self[x])
        cPickle.dump(l,stream,1)

        return done



class OpenJson(dict):
    """
    This allows to parse a json file and generate a python object from it. The argument to be given is the filename of the json file. The function returns the data in a python object format.
    """
    def __init__(self,filename) :
        dict.__init__(self)
        state = self.load_json(filename)

    def load_json(self,filename) :
        """
        This function choose the good parser by reading the "kind" field contained in the metadata. If not it asks you the information if not given
        """
        done = True
        try :
            monjson = get_json(filename)
        except IOError :
            print "Problem loading the file"
            done = False

        if(done) :
            done = self.load_cyc_stat(monjson)

        return done


    def load_cyc_stat(self,monjson) :
        """
        This function constructs the object given a Json file corresponding at many cycles. The corresponding kind of file is "cycle"
        """
        done = True
        try :
            K = monjson.keys()
            K.pop(K.index("vim_modeline")) #eliminate vim mode parameter
            # the function json_data(json_object,i,j) return the jth column of the ith measurement of a json_object
            self["sweep_number"] = size(monjson["measures"])
            self["bias"] = json_data(monjson,0,1)
            self["date"] = []
            self["data"] = []
            sweep_number = self["sweep_number"]
            for i in range(sweep_number):
                self["date"].append(monjson["measures"][i]["start"])
                self["data"].append(json_data(monjson,i,2))
            K.pop(K.index("measures"))
            if (size(K) > 0) :
                self["metadata"] = dict([])
                for x in K :
                    self["metadata"][x]  = monjson[x]
        except KeyError :
            print "Problem while loading the file. If an object is howerver loaded, it can be incomplete"
            done = False

        return done


class OpenBin(dict):
    """
    This class create an OpenBin object given a binary file generated from a measurement
    """
    def __init__(self,filename) :
        dict.__init__(self)
        self.load_bin(filename)

    def load_bin(self,filename) :
        done = True
        try :
            stream = open(filename,"r")
        except IOError :
            print "Problem while loading the binary file. Check the file name and/or the folder"
            done = False

        temp = cPickle.load(stream)
        stream.close()
        X = temp[0]
        i=1
        for x in X :
            self[x] = temp[i]
            i+=1
        return done


