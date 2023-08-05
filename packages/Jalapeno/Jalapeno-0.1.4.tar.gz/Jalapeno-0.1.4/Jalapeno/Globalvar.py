from Jalapeno.lib.eventEngine import *
import webbrowser
engine = eventEngine()
events = {}

#def browser_start(website):
#	def starter():
#		webbrowser.open(website)
#	return starter
#Using class instead of closure for pickling
class browser_starter():
	def __init__(self,website):
		self.website = website
	def __call__(self,listener):
		webbrowser.open(self.website)





#events['Browse']=Event('Browse','Proc',browser_starter('http://127.0.0.1:5588/redirect'))
events['Browse']=Event('Browse','SubProc',"Jalapeno/GUI/Gutils/Chrome.py")
