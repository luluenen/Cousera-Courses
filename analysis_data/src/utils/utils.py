
class Utils:

	@staticmethod
	def isStr(a):
		if type(a) is not str:
			raise TypeError('str is expected, but :'+type(a).__name__)

	@staticmethod
	def isList(a):
		if type(a) is not list:
			raise TypeError('list is expected, but :'+ type(a).__name__)	

	@staticmethod
	def isFloat(a):
		if type(a) is not float:
			raise TypeError('float is expected, but :'+ type(a).__name__)

	@staticmethod
	def isDict(a):
		if type(a) is not dict:
			raise TypeError('dict is expected, but :'+ type(a).__name__)
