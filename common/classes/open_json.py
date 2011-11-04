class OpenJson(dict):
    """
    This allows to parse a json file and generate a python object from it. The argument to be given is the filename of the json file. The function returns the data in a python object format.
    """
    def __init__(self, filename) :
        dict.__init__(self)
        self.load_json(filename)

    def load_json(self, filename) :
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


    def load_cyc_stat(self, monjson) :
        """
        This function constructs the object given a Json file corresponding at many cycles. The corresponding kind of file is "cycle"
        """
        done = True
        try :
            K = monjson.keys()
            K.pop(K.index("vim_modeline")) #eliminate vim mode parameter
            # the function json_data(json_object,i,j) return the jth column of the ith measurement of a json_object
            self["sweep_number"] = size(monjson["measures"])
            self["bias"] = json_data(monjson, 0, 1)
            self["date"] = []
            self["data"] = []
            sweep_number = self["sweep_number"]
            for i in range(sweep_number):
                self["date"].append(monjson["measures"][i]["start"])
                self["data"].append(json_data(monjson, i, 2))
            K.pop(K.index("measures"))
            if (size(K) > 0) :
                self["metadata"] = dict([])
                for x in K :
                    self["metadata"][x]  = monjson[x]
        except KeyError :
            print "Problem while loading the file. If an object is howerver loaded, it can be incomplete"
            done = False

        return done
