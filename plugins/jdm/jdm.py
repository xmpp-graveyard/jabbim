# -*- coding: utf8 -*-
import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from urllib import quote, unquote
from twisted.python import log
from include import utils


class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'jdm'
		self.description = 'Jabbim disk manager'
		self.author = u"Josef 'Pepeq' Halíček"
		self.name = 'JDM Plugin'
		self.version = '0.008'
		self.category = ['disk']
		self.url = 'http://dev.jabbim.cz/jabbim'
		if main:
			self.installTranslator()
			self.window = self.loadWindow("%s/plugins/%s/jdm.ui.py"%(self.homeDir, self.fname))
			self.window.setWindowIcon(self.main.windowIcon())
			self.log = False
			self.registerHandler('on_message', self.on_message, priority=4)
		else:
			self.loadConfig(homedir)
			
	def buildRosterMenu(self):
		menu=self.rosterMenu()
		menu.addAction("Jabbim disk manager",self.showSlot)
	
	def showSlot(self):
		self.window.show()
	
	def on_message(self, frm, typ, body, subject = None, xhtml = None,  chatstate = None,  delay = None):
		pass