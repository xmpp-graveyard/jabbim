# -*- coding: utf8 -*-
import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from urllib import quote, unquote
from twisted.python import log
from include import utils

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'jdm'
		self.description = 'Jabbim disk manager'
		self.author = u"Josef 'Pepeq' Halíček"
		self.name = 'JDM Plugin'
		self.version = '0.1147'
		self.category = ['disk']
		self.url = 'http://dev.jabbim.cz/jabbim'
		if main:
			self.installTranslator()
			self.window = self.loadWindow("%s/jdm_ui.py" % self.pluginDir)
			self.window.setWindowIcon(self.main.windowIcon())
			QtCore.QObject.connect(self.window.ui.reload,QtCore.SIGNAL("clicked()"),self.call)
			QtCore.QObject.connect(self.window.ui.list, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem * , QListWidgetItem * )"),self.clicked)
			self.window.ui.list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
			self.window.ui.list.startDrag=self.startDrag
			QtCore.QObject.connect(self.window.ui.list,QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.fileMenu)
			self.log = False
			self.registerHandler('on_message', self.on_message, priority=4)
			self.obsah=[]
			self.dnd={}
		else:
			self.loadConfig(homedir)

	def startDrag(self,actions):
		# start dragging selected contact
		item=self.window.ui.list.currentItem()

		self.drag=QtGui.QDrag(self.window.ui.list)
		mimeData=QtCore.QMimeData()
		mimeData.setText("http://disk.jabbim.cz/"+self.main.client.jid.userhost()+"/"+item.text())
		mimeData.setUrls([QtCore.QUrl("http://disk.jabbim.cz/"+self.main.client.jid.userhost()+"/"+item.text())])
		self.dnd=item
		self.drag.setMimeData(mimeData)
		self.action=self.drag.start(QtCore.Qt.CopyAction)

	def fileMenu(self,pos):
		print "menu"
		item=self.window.ui.list.currentItem()
		if not item:
			return
		self.menu=QtGui.QMenu()
		self.menu.addAction(self.tr("Remove file"),self.removeCurrentFile)
		self.menu.popup(self.window.ui.list.mapToGlobal(pos))
	
	def removeCurrentFile(self):
		item=self.window.ui.list.currentItem()
		if not item:
			return
		self.main.client.sendMessage("public@disk.jabbim.cz", u"rm "+unicode(item.text()))
		item=self.window.ui.list.takeItem(self.window.ui.list.currentRow())
		del item

	def toNormalSize(self,size):
		original=int(size)
		new=int(size/1000) # kB
		if new==0:
			return str(round(original,2.0))+" B" # B
		size=new
		new=int(size/1000) # MB
		if new==0:
			return str(round(original/1000.0,2))+" kB" # kB
		return str(round(original/1000000.0,2))+" MB" # MB

	def updateView(self, data, typ = 'public'):
		self.window.ui.list.clear()
		#self.window.ui.log.clear()
		data=data[0][0]
		print data #2 - white.zip [37.5KiB] - 38438
		for file in data:
			name=file[0]
			size=file[1]
			ext=name.split('.')[-1]
			item=QtGui.QListWidgetItem(unicode(name))
			item.setData(32,QtCore.QVariant([unicode(size)]))
			if ext in ["exe","run","sh","bin"]: 
				item.setIcon(QtGui.QIcon(self.pluginDir+"/application-x-executable.png"))
			elif ext in ["svg","jpg","png","gif","tif","tiff","bmp","ico","xcf"]: 
				item.setIcon(QtGui.QIcon(self.pluginDir+"/image-x-generic.png"))
			elif ext in ["wav","mp3","ogg","mp4","flac"]:
				item.setIcon(QtGui.QIcon(self.pluginDir+"/audio-x-generic.png"))
			elif ext in ["rar","zip","gz","bz","tgz","deb","rpm","tar","pkg","7z","ace"]:
				item.setIcon(QtGui.QIcon(self.pluginDir+"/package-x-generic.png"))
			elif ext in ["htm","html","xml"]:
				item.setIcon(QtGui.QIcon(self.pluginDir+"/text-html.png"))
			elif ext in ["txt","c","py","log"]:
				item.setIcon(QtGui.QIcon(self.pluginDir+"/text-x-generic.png"))
			elif ext in ["mov","avi","mpg","swf","dv"]:
				item.setIcon(QtGui.QIcon(self.pluginDir+"/text-x-generic.png"))
			elif ext in ["odt","doc","pdf","docx"]:
				item.setIcon(QtGui.QIcon(self.pluginDir+"/x-office-document.png"))
			elif ext in ["ods","xls","cvs"]:
				item.setIcon(QtGui.QIcon(self.pluginDir+"/x-office-spreadsheet.png"))
			elif ext in ["pts","ppt","odp"]:
				item.setIcon(QtGui.QIcon(self.pluginDir+"/x-office-presentation.png"))
			else:
				item.setIcon(QtGui.QIcon(self.pluginDir+"/text-x-generic-template.png"));  #preventivne pokud se netrefime
			self.window.ui.list.addItem(item)

	def buildMainWindowMenu(self):
		menu=self.mainWindowMenu()
		menu.addAction("Jabbim disk manager",self.showSlot)
	
	def call(self,jid="",type="public"):
		if jid=="":
			self.jid=self.main.client.jid.userhost()
		else:
			self.jid=jid
		self.type=type
		if self.type=="public":
			self.main.client.callRemote('rpc@jabbim.cz/service', 'listPublic', (self.jid,)).addCallback(self.updateView, 'public')
	
	
	def showSlot(self):
		self.window.show()
		self.call()
	
	def on_message(self, frm, typ, body, subject = None, xhtml = None,  chatstate = None,  delay = None,error=None):
		if unicode(frm).find("public@disk.jabbim.cz")!=-1:
			if not self.window.isHidden():
				return False
		return True
		
	def clicked(self,item,old):
		print 'click',item
		self.window.ui.label_name.setText(item.text())
		data=item.data(32).toList()
		size=int(data[0].toString())
		self.window.ui.label_size.setText(self.toNormalSize(size))
		#self.window.ui.log.append(unicode(self.obsah[self.obsah.index(item.text())][2]))
		#self.window.ui.log.append(unicode(item.text()))
		

	
