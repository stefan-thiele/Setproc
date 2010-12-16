"""
@uthor : Romain Vincent
Created 10/12/2010

This file contains the class that handle the opening and saving of the measures.All functions specific to this method should be defined in this file
"""


class OpenMeasures(dict): 
	"""
	This allows to parse a json file and generate a python object from it. The argument to be given is the filename of the json file. The function returns the data in a python object format.
	"""
	def __init__(self,filename,mode) :
		dict.__init__(self)
		self["bias"] = None
		self["sweep_number"] = None
		self["data"] = None
		self.load_data(filename,mode)
	"""
	### The following method handle the choice of the functions and the functions corresponding to each kind of measure
	"""	
	def load_data(self,filename,mode) :
		"""
		This function load the data providing the kind of data given as input ("Json" for Json files ans "Bin" for binary files
		"""
		if mode == "Json" :
			self.load_json(filename)
		else :
			load_bin(filename)

		#Then the monjson object is deleted
		try : 
			del monjson	
		except :
			print "Could not delete the json object"
		
		return True

	def load_json(self,filename) :
		"""
		This function choose the good parser by reading the "kind" field contained in the metadata. If not it asks you the information if not given
		"""
		try :
			monjson = json.load(open(filename,'r'))
		except :
			print "Problem loading the file"
		#insure that the file contains the information kind. If not, the user has to provide it
		try :
			kind = monjson["kind"]
		except :
			kind = input("There is no information concerning the kind of file. Could you provide it ?")
		#choose the function corresponding to the kind of file
		if kind == "cyc" :
			self.load_cyc_stat(monjson)
		
		elif kind == "cyc_loc" :
			self.load_cyc_loc(monjson)

		else :
			print "The kind ",kind, " is not recognized \n"

	#First function for Json file (kind "cyc" of file)
	def load_cyc_stat(self,monjson) :
		"""
		This function constructs the object given a Json file corresponding at many cycles. The corresponding kind of file is "cycle"
		"""
		try :
			K = monjson.keys()
			K.pop(K.index("vim_modeline")) #vim mode
		except :
			print "Problem while generating the key values. Other problems may follow"
		#Number of sweep
		try :
			self["sweep_number"] = size(monjson["measures"])
		except :
			print "No sweep number Does the file contain data?"
		#Bias
		try : 
			self["bias"] = data_json(monjson,0,1)
		except :
			print "No bias loaded. Does the file contain data?"

		#all the data(without bias information)
		try : 
			self["data"] = []
			for i in range(self["sweep_number"]):
				self["data"].append(json_data(monjson,i,2))
			K.pop(K.index("measures"))
		except :
			print "Problem loading data... Check the file"
		#and then the metadata
		try :
			K.pop(K.index("filetype"))
		except :
			print "This file seems not to have been generated by nanoQt"
		try :
			if (size(K) > 0) :
				self["metadata"] = dict([])
				for x in K :
					self["metadata"][x]  = monjson[x]
		except :
			print "Problem while generating the metadata"


		return True

	def load_cyc_loc(self,monjson) :
		"""
		This function constructs the object given a Json file corresponding at many cycles. The corresponding kind of file is "cycle_local"
		"""
		try :
			K = monjson.keys()
			K.pop(K.index("vim_modeline")) #vim mode
		except :
			print "Problem while generating the key values. Other problems may follow"
		#Number of sweep
		try :
			self["sweep_number"] = size(monjson["measures"])
		except :
			print "No sweep number Does the file contain data?"
		##########################################################################################################
		#Construct the sweep. This kind of the sweep contains the bias, the data and the number of "detect" sweep.
		##########################################################################################################
		self["data"] = []
		nbr = 0
		nbr_detect = 0

		for i in range(self["sweep_number"]) :
			test = monjson["measures"][i]["type"]

			#first part of the sweep
			if test == "approach" :
				self["data"].append(dict([])) #Each element of the array data is a dictionnary
				self["data"][nbr]["bias"] = []  # The element "bias" is an array
				self["data"][nbr]["data"] = []  # The element "bias" is an array
				self["data"][nbr]["bias"].append(json_data(monjson,i,1))
				self["data"][nbr]["data"].append(json_data(monjson,i,2))
			#second part of the sweep
			elif test == "detect" : 
				nbr_detect = nbr_detect + 1
				self["data"][nbr]["bias"].append(json_data(monjson,i,1))
				self["data"][nbr]["data"].append(json_data(monjson,i,2))

			else :
				self["data"][nbr]["bias"].append(json_data(monjson,i,1))
				self["data"][nbr]["data"].append(json_data(monjson,i,2))
				self["data"][nbr]["info"] = dict([])
				self["data"][nbr]["info"]["try_nbr"] = nbr_detect
				nbr = nbr + 1	
				nbr_detect = 0

		return True



	def load_bin(self,filename) :

		stream = open(filename,"r")
		temp = cPickle.load(stream)
		#temp = pickle.load(pickle.Unpickler(stream))
		stream.close()
		X = temp[0]
		i=1
		for x in X :
			self[x] = temp[i]
			i+=1
		return True
	
	
	def save(self,savename) :
		stream = open(savename,"w")
		l =[]
		temp = self.keys()
		l.append(temp)
		for x in self:
			l.append(self[x])
		cPickle.dump(l,stream,1)
		return True
			


