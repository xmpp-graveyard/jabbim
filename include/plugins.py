from configobj import ConfigObj
from twisted.python import log

class PluginBase:
	def __init__(self, main):
		self.main = main
		self.config = {} #{'hodnota':{default:'', description:'', value: ''}}
		self.description = 'basic plugin class'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'Basic plugin'
		self.fname = ''
		self.version = '0.1'
		self.category = ['test', 'misc']
		self.url = 'dev.jabbim.cz/jabbim'
	
	def loadConfig(self):
# 		try:
# 			self.confObj = ConfigObj(main.homeDir+'/.jabbim/plugins/'+self.fname+'/config.ini',encoding='UTF8')
# 			
# 		except:
# 			log.msg('No config for: '+self.name)
# # 			return False
		self.confObj = ConfigObj(self.main.homeDir+'/.jabbim/plugins/'+self.fname+'/config.ini',encoding='UTF8')
		for k in self.config.iterkeys():
			try:
				self.config[k]['value'] = self.confObj[k]
			except:
				self.config[k]['value'] = self.config[k]['default']
				self.confObj[k] = self.config[k]['default']
				self.confObj.write()
	
	def writeConfig(self):
		for k in self.config.iterkeys():
			self.confObj[k] = self.config[k]['value']
		self.confObj.write()
