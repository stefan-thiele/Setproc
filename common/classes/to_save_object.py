import cPickle #for saving

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
