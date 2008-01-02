"""
Copyright (C) 2007 	Jan 'Hanzz' Kaluza (hanzz at njs.netlab.cz)
Copyright (C) 2007	Jiri 'Sef' Gabrys	(sef at njs.netlab.cz)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""
from configobj import ConfigObj
from twisted.python import log
from imp import load_source
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
import utils

class PluginBase:
	def __init__(self, main, homedir):
		self.main = main
		self.config = None
		self.configDialog = None
		self.description = 'basic plugin class'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'Basic plugin'
		self.fname = ''
		self.version = '0.1'
		self.category = ['test', 'misc']
		self.url = 'dev.jabbim.cz/jabbim'
		self.handlers = []
		self.homeDir = homedir
		self.translator=None
		self.developMode=False
		self.loadedWindows=[]

	def connected(self):
		pass

	def rosterMenu(self):
		menu=self.main.ui.menuPlugins.addMenu(unicode(self.name))
		return menu

	def buildRosterMenu(self):
		pass

	def buildChatWidget(self,jid,layout,widget):
		pass

	def buildGroupchatWidget(self,jid,layout,widget):
		pass

	def loadUi(self,file,parent,wid):
		#print locals()
		ui = None
		f=open(utils.path(file))
		ui=load_source(self.fname, utils.path(file), f)
		f.close()
		wid.ui=None
		#print dir(ui)
		for func in dir(ui):
			if func.startswith("Ui_"):
				wid.ui=getattr(ui, func)()
				wid.ui.setupUi(wid)
		if wid.ui==None:
			return None
		self.loadedWindows.append(wid)
		return wid

	def loadWidget(self,file,parent=None):
		wid=QtGui.QWidget(parent)
		return self.loadUi(file,parent,wid)

	def loadWindow(self,file,parent=None):
		wid=QtGui.QMainWindow(parent)
		return self.loadUi(file,parent,wid)

	def loadDialog(self,file,parent=None):
		wid=QtGui.QDialog(parent)
		return self.loadUi(file,parent,wid)

	def on_configChanged(self):
		pass

	def installTranslator(self):
		self.translator=QtCore.QTranslator()
		directory=u"%s/plugins/%s/"%(self.homeDir, self.fname)
		self.translator.load(utils.path(directory+unicode(QtCore.QLocale.system().name()[:2])+u".qm"))
		log.msg("trying to load localization file "+ directory+unicode(QtCore.QLocale.system().name())[:2]+".qm")

	def tr(self,text,cl=None):
		if not self.translator:
			return text
		if cl:
			trans=self.translator.translate(cl,text)
		else:
			trans=self.translator.translate("Plugin",text)
			if len(trans)==0:
				trans=self.translator.translate("self.main",text)
				if len(trans)==0:
					return text
		return trans
	
	def getConfig(self,config):
		return ConfigObj(config,encoding='UTF8')

	def on_saveConfig(self):
		pass

	def on_showPreferences(self,dialog):
		pass

	def on_endPreferences(self):
		pass

	def loadConfig(self,homedir=None):
		if homedir==None:
			homedir=self.main.homeDir
			
# 		try:
# 			self.confObj = ConfigObj(main.homeDir+'/.jabbim/plugins/'+self.fname+'/config.ini',encoding='UTF8')
# 			
# 		except:
# 			log.msg('No config for: '+self.name)
# # 			return False
		self.config = ConfigObj(utils.path(homedir+'/'+self.fname+'-config.ini'),encoding='UTF8')
		if self.configDialog:
			for k,v in self.configDialog.config.iteritems():
				#try:
					#self.config[k]['value'] = self.confObj[k]
				#except:
				if not self.config.has_key(k) and not k.startswith("__"):
					self.config[k] = v['value']
					#self.confObj[k] = self.config[k]['default']
					self.config.write()
	
	def writeConfig(self):
		#for k in self.config.iterkeys():
			#self.confObj[k] = self.config[k]['value']
		#self.confObj.write()
		if self.config:
			self.config.write()
	
	def registerHandler(self, name, method, priority = 5):
		self.main.client.dispatcher.registerHandler(name, method, self.name, priority = priority)
		self.handlers.append(name)
	
	def on_remove(self):
		pass
	
	def remove(self):
		self.on_remove()
		for window in self.loadedWindows:
			window.close()
		for i in range(int(len(self.loadedWindows))):
			del self.loadedWindows[0]
		self.writeConfig()
		for handler in self.handlers:
			self.main.client.dispatcher.unregisterHandler(handler, unicode(self.name))
		self.main = None
		self.config = None
		self.configDialog = None
		self.description = 'basic plugin class'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'Basic plugin'
		self.fname = ''
		self.version = '0.1'
		self.category = ['test', 'misc']
		self.url = 'dev.jabbim.cz/jabbim'
		self.handlers = []
		self.homeDir = None
		self.translator=None
		self.developMode=False
		self.loadedWindows=[]
		
