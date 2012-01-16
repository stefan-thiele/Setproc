class shape(dict): 
"""
Description
"""	
	def __init__(self,x,y):
		dict.__init__(self)		
		self.x = x
		self.y = y
		self.tf()
	def tf(self):
		print("test")
	def area(self):
		return self.x*self.y
	def autorName(self,text):
		self.autor = text
	def test(self):
		self["bias"] = 3
	def set_keys(self):	
		self["a"] = 2
		self["b"] = 2
	def set_keys2(self):
		self = {"c":4,"d":5}



def get_json():
	import json
	res = json.load(open("/home/admins/repo1/test.json"))
	return res

