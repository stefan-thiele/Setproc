"""
@uthor : Romain Vincent
Created 10/12/2010

This file contains the classes that handle the opening and saving of the measures.All functions specific to this method should be defined in this file
"""


"""
This first class is a generique one and it makes sure that all the opening method handle the common operations (such as saving) in the same manners
"""
class Measure(dict) :
	"""
	This allows to parse a json file and generate a python object from it. The argument to be given is the filename of the json file. The function returns the data in a python object format.
	"""
	################################
	def __init__(self,filename,mode) :
		dict.__init__(self)
		if mode == "Json" :
			temp = OpenJson(filename)
		elif mode == "Bin" :
			temp = OpenBin(filename)
		for x in temp :
			self[x] = temp[x]
		

	def save(self,savename) :
		"""
		Save all the keys field of a dictionnary in savename file. The "*.bin" extension should be used
		"""
		state = True
		try :
			stream = open(savename,"w")
		except IOError :
			print "Problem while saving the file"
			state = False
		l =[]
		temp = self.keys()
		l.append(temp)
		for x in self:
			l.append(self[x])
		cPickle.dump(l,stream,1)

		return state


"""
This class is derived from the OpenMeasure class. It is specific to the json file data.
"""

class OpenJson(dict): 
	"""
	This allows to parse a json file and generate a python object from it. The argument to be given is the filename of the json file. The function returns the data in a python object format.
	"""
	################################
	def __init__(self,filename) :
		dict.__init__(self)
		state = self.load_json(filename)
	"""
	### The following method handle the choice of the functions 
	and the functions corresponding to each kind of measure
	"""	
	
	############################
	def load_json(self,filename,kind = "cyc") :
		"""
		This function choose the good parser by reading the "kind" field contained in the metadata. If not it asks you the information if not given
		"""
		state = True
		try :
			monjson = get_json(filename)
			if(kind == None):
				kind = monjson["kind"]

		#handling exceptions
		except IOError : #in case the file could not be loaded
			print "Problem loading the file"
			state = False
		except KeyError: #in case the "kind" element of the json object does not exist
			kind = input("There is no information concerning the kind of file. Could you provide it ?")
		if(state) :
			#instructions
			if kind == "cyc" : #this function will be soon deprecated
				state = self.load_cyc_stat(monjson)
			elif kind == "cyc_loc" : #this function will be soon deprecated
				state = self.load_cyc_loc(monjson)
			elif kind == "new": #this is the one that should always been used
				state = self.load_new(monjson)
			else :
				print "The kind ",kind, " is not recognized"
				while True :
					print "I enter the while loop"
					choice = input("would you try again ? ")
					if choice in('y','yes') :
						kind = input("Enter the kind of sweep :")
						state = self.load_json(filename,kind)
						break
					if choice in ('no','n'):
						print "Its your choice"
						state = False
						break
					
		return state

	###############################
	#First function for Json file (kind "cyc" of file)
	def load_cyc_stat(self,monjson) :
		"""
		This function constructs the object given a Json file corresponding at many cycles. The corresponding kind of file is "cycle"
		"""
		state = True
		try :
			K = monjson.keys()
			K.pop(K.index("vim_modeline")) #eliminate vim mode parameter
			self["sweep_number"] = size(monjson["measures"])
			self["bias"] = json_data(monjson,0,1)
			self["data"] = []
			for i in range(self["sweep_number"]):
				self["data"].append(json_data(monjson,i,2)) #this function return the columns 2 of the sweep i
			K.pop(K.index("measures"))
			if (size(K) > 0) :
				self["metadata"] = dict([])
				for x in K :
					self["metadata"][x]  = monjson[x]
		except KeyError :
			print "Problem while generating the metadata"
			state = False

		return state


	def load_new(self,monjson) :
		"""
		This function constructs the object given a Json file corresponding at many cycles. The corresponding kind of file is "cycle_local"
		"""
		state = True
		try :
			K = monjson.keys()
			K.pop(K.index("vim_modeline")) #vim mode
			self["sweep_number"] = size(monjson["measures"])
		except KeyError :
			print "Problem while loading the data in --load_cyc_loc--."
		##########################################################################################################
		#Construct the sweep. This kind of the sweep contains the bias, the data and the number of "detect" sweep.
		##########################################################################################################
		self["data"] = []
		nbr = -1
		sweep_keys = None
		try :
			for i in range(self["sweep_number"]) :

				#check if it is the first element of a sweep
				#if( monjson["measures"][i].__contains__("start") == True) :
				if( monjson["measures"][i]["type"] == "approach") :
					sweep_keys = [] #Create the dict for the current sweep
					nbr = nbr +1
					self["data"].append(dict([]))

				#Check the kind of sweep
				typesweep = monjson["measures"][i]["type"]
				if( sweep_keys.__contains__(typesweep) == False) : #add unknown kind
					sweep_keys.append(typesweep)
					self["data"][nbr][typesweep] = dict([])
					self["data"][nbr][typesweep]["info"] = dict([])
					self["data"][nbr][typesweep]["info"]["try_nbr"] = 1 
				
				#Push all the needed data!!
				self["data"][nbr][typesweep]["bias"] = []  # The element "bias" is an array
				self["data"][nbr][typesweep]["data"] = []  # The element "bias" is an array
				self["data"][nbr][typesweep]["bias"].append(json_data(monjson,i,1))
				self["data"][nbr][typesweep]["data"].append(json_data(monjson,i,2))
				self["data"][nbr][typesweep]["info"]["try_nbr"] += 1
		
			self["total_sweep"] = nbr 

		except KeyError : 
			print "Key problem while loading data"
			state = False
		
		return state


class OpenBin(dict): 
	"""
	This allows to parse a json file and generate a python object from it. The argument to be given is the filename of the json file. The function returns the data in a python object format.
	"""
	################################
	def __init__(self,filename) :
		dict.__init__(self)
		self.load_bin(filename)
	"""
	### The following method handle the choice of the functions 
	and the functions corresponding to each kind of measure
	"""	

	def load_bin(self,filename) :
		state = True
		try :
			stream = open(filename,"r")
		except IOError :
			print "Problem while loading the binary file"
			state = False

		temp = cPickle.load(stream)
		stream.close()
		X = temp[0]
		i=1
		for x in X :
			self[x] = temp[i]
			i+=1
		return state
