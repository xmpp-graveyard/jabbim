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
		self.version = '0.1132'
		self.category = ['disk']
		self.url = 'http://dev.jabbim.cz/jabbim'
		if main:
			self.installTranslator()
			self.window = self.loadWindow("%s/plugins/%s/jdm_ui.py"%(self.homeDir, self.fname))
			self.window.setWindowIcon(self.main.windowIcon())
			self.log = False
			self.registerHandler('on_message', self.on_message, priority=4)

			self.obsah=[]

		else:
			self.loadConfig(homedir)
		
	def updateView(self, vysledek, typ = 'public'):
		self.window.ui.list.clear()
		self.window.ui.log.clear()
		self.obsah=[]
		
		#[0][0] je seznam jednotlivych polozek, kazda polozka ma nazev a velikost
		for i in range (0,len(vysledek[0][0])):
			self.obsah.append([i,vysledek[0][0][i][0],vysledek[0][0][i][0].split(".")[-1],vysledek[0][0][i][1]])
			
			#self.window.ui.log.append(u"Název: %s \nVelikost: %s bytů\ntywe :)\n"%(self.obsah[i][0],self.obsah[i][1]))

		for i in range (0,len(self.obsah)):
			self.window.ui.log.append(unicode(self.obsah[i]))
			
			item=QtGui.QListWidgetItem(unicode(self.obsah[i][1]))
			item.setIcon(QtGui.QIcon(self.homeDir+"/plugins/jdm/text-x-generic-template.png"));  #preventivne pokud se netrefime
			
			if self.obsah[i][2] in ["exe","run","sh","bin"]: 
				item.setIcon(QtGui.QIcon(self.homeDir+"/plugins/jdm/application-x-executable.png"))
			if self.obsah[i][2] in ["svg","jpg","png","gif","tif","tiff","bmp","ico","xcf"]: 
				item.setIcon(QtGui.QIcon(self.homeDir+"/plugins/jdm/image-x-generic.png"))
			if self.obsah[i][2] in ["wav","mp3","ogg","mp4","flac"]:
				item.setIcon(QtGui.QIcon(self.homeDir+"/plugins/jdm/audio-x-generic.png"))
			if self.obsah[i][2] in ["rar","zip","gz","bz","tgz","deb","rpm","tar","pkg","7z","ace"]:
				item.setIcon(QtGui.QIcon(self.homeDir+"/plugins/jdm/package-x-generic.png"))
			if self.obsah[i][2] in ["htm","html","xml"]:
				item.setIcon(QtGui.QIcon(self.homeDir+"/plugins/jdm/text-html.png"))
			if self.obsah[i][2] in ["txt","c","py","log"]:
				item.setIcon(QtGui.QIcon(self.homeDir+"/plugins/jdm/text-x-generic.png"))
			if self.obsah[i][2] in ["mov","avi","mpg","swf","dv"]:
				item.setIcon(QtGui.QIcon(self.homeDir+"/plugins/jdm/text-x-generic.png"))
			if self.obsah[i][2] in ["odt","doc","pdf","docx"]:
				item.setIcon(QtGui.QIcon(self.homeDir+"/plugins/jdm/x-office-document.png"))
			if self.obsah[i][2] in ["ods","xls","cvs"]:
				item.setIcon(QtGui.QIcon(self.homeDir+"/plugins/jdm/x-office-spreadsheet.png"))
			if self.obsah[i][2] in ["pts","ppt","odp"]:
				item.setIcon(QtGui.QIcon(self.homeDir+"/plugins/jdm/x-office-presentation.png"))
			self.window.ui.list.addItem(item)
		
		#for i in range (0,len(vysledek[0][0])):
		#	self.window.ui.log.append(u"Název: %s \nVelikost: %s bytů\ntywe :)\n"%(self.obsah[i][0],self.obsah[i][1]))
	
	def buildRosterMenu(self):
		menu=self.rosterMenu()
		menu.addAction("Jabbim disk manager2",self.showSlot)
	
	def showSlot(self):
		self.window.show()
		self.main.client.callRemote('rpc@jabbim.cz/service', 'listPublic', (self.main.client.jid.userhost(),)).addCallback(self.updateView, 'public')
		
	
	def on_message(self, frm, typ, body, subject = None, xhtml = None,  chatstate = None,  delay = None):
		pass
	

	
