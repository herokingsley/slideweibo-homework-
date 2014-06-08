debug = True
#debug = False
class SlideBase:
	def __init__(self):
		self.status = 0 #not start yet
		pass
	
	def startExecute(self):
		self.stauts = 1 #starting

	def endExecute(self):
		self.status = 4 # finished
		pass
	

class SlideBaseArranger:
	def __init__(self):
		pass
	
	def run(self,url):
		
		pass

