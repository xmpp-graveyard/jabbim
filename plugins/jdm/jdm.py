# -*- coding: utf8 -*-
import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from urllib import quote, unquote
from twisted.python import log
from include import utils

class config:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['iconMode']={'type':'boolean','label':self.main.tr("Show files as icons"),'value':'True'}

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'jdm'
		self.description = 'Jabbim disk manager'
		self.author = u"Josef 'Pepeq' Halíček"
		self.name = 'JDM Plugin'
		self.version = '0.1147'
		self.category = ['utils']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.installTranslator()
		self.configDialog=config(self)
		if main:
			self.loadConfig()
			self.window = self.loadWindow("%s/jdm_ui.py" % self.pluginDir,self.main)
			self.window.setWindowIcon(self.main.windowIcon())
			self.window.ui.list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
			self.window.ui.list.startDrag=self.startDrag
			self.window.ui.list.setAcceptDrops(True)
			self.window.ui.list.dropEvent = self.dropEvent
			self.window.ui.list.dragMoveEvent = self.dragMoveEvent
			self.window.ui.list.dragEnterEvent = self.dragEnterEvent
			self.window.ui.line_jid.setText(self.main.client.jid.userhost())
			self.jid = self.main.client.jid.userhost()
			self.typ = "public"
			self.window.ui.buttonDownload.setIcon(QtGui.QIcon("%s/document-save.png" % self.pluginDir))
			self.window.ui.buttonUpload.setIcon(QtGui.QIcon("%s/upload.png" % self.pluginDir))
			self.window.ui.buttonDelete.setIcon(QtGui.QIcon("%s/edit-delete.png" % self.pluginDir))
			self.window.ui.buttonHome.setIcon(QtGui.QIcon("%s/home.png" % self.pluginDir))
			self.window.ui.publicButton.setIcon(QtGui.QIcon("%s/jdisk-public-24.png" % self.pluginDir))
			self.window.ui.privateButton.setIcon(QtGui.QIcon("%s/jdisk-private-24.png" % self.pluginDir))
			self.window.ui.albumButton.setIcon(QtGui.QIcon("%s/jalbum-32.png" % self.pluginDir))
			self.group=QtGui.QButtonGroup(self.window)

			QtCore.QObject.connect(self.group,QtCore.SIGNAL("buttonClicked ( QAbstractButton * )"),self.buttonClicked)
			QtCore.QObject.connect(self.window.ui.reload,QtCore.SIGNAL("clicked()"),self.call)
			QtCore.QObject.connect(self.window.ui.list, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem * , QListWidgetItem * )"),self.clicked)
			QtCore.QObject.connect(self.window.ui.list,QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.fileMenu)
			QtCore.QObject.connect(self.window.ui.buttonDownload,QtCore.SIGNAL("clicked()"),self.downloadCurrentFile)
			QtCore.QObject.connect(self.window.ui.buttonDelete,QtCore.SIGNAL("clicked()"),self.removeCurrentFile)
			QtCore.QObject.connect(self.window.ui.buttonUpload,QtCore.SIGNAL("clicked()"),self.sendFile)
			QtCore.QObject.connect(self.window.ui.buttonHome,QtCore.SIGNAL("clicked()"),self.home)
			QtCore.QObject.connect(self.window.ui.publicButton,QtCore.SIGNAL("clicked()"),self.public)
			QtCore.QObject.connect(self.window.ui.privateButton,QtCore.SIGNAL("clicked()"),self.private)
			QtCore.QObject.connect(self.window.ui.albumButton,QtCore.SIGNAL("clicked()"),self.album)
			self.log = False
			self.registerHandler('on_message', self.on_message, priority=4)
			self.registerHandler('on_ftEnd', self.on_ftEnd, priority = 4)
			self.obsah=[]
			self.dnd={}
		else:
			self.loadConfig(homedir)

	def setIconMode(self,bool):
		if bool:
			self.window.ui.list.setGridSize(QtCore.QSize(128,96))
			self.window.ui.list.setViewMode(QtGui.QListView.IconMode)
			self.config["iconMode"]='True'
		else:
			self.window.ui.list.setGridSize(QtCore.QSize())
			self.window.ui.list.setViewMode(QtGui.QListView.ListMode)
			self.config["iconMode"]='False'
		self.config.write()

	def public(self):
		self.call(typ='public')

	def private(self):
		self.call(typ='private')

	def album(self):
		self.call(typ='album')

	def home(self):
		self.call(self.main.client.jid.userhost())

	def buttonClicked(self,button):
		pass

	def chatMenuItemTriggered(self,action):
		cmd=unicode(action.objectName())
		if cmd=="show_my_disk":
			anchor="http://disk.jabbim.cz/%s/"%(unicode(self.main.client.jid.userhost()))
			QtGui.QDesktopServices.openUrl(QtCore.QUrl(anchor))
		elif cmd=="show_users_disk":
			anchor="http://disk.jabbim.cz/%s/"%(unicode(action.parent().parent().jid))
			QtGui.QDesktopServices.openUrl(QtCore.QUrl(anchor))
		elif cmd=="show_my_disk_jdm":
			self.showSlot(self.main.client.jid.userhost())
		elif cmd=="show_users_disk_jdm":
			self.showSlot(unicode(action.parent().parent().jid))
		elif cmd=="show_my_album":
			anchor="http://album.jabbim.cz/%s/"%(unicode(self.main.client.jid.userhost()))
			QtGui.QDesktopServices.openUrl(QtCore.QUrl(anchor))
		elif cmd=="show_users_album":
			anchor="http://album.jabbim.cz/%s/"%(unicode(action.parent().parent().jid))
			QtGui.QDesktopServices.openUrl(QtCore.QUrl(anchor))

	def buildChatWidget(self,jid,layout,widget):
		jid=self.main.getJid(jid)
		# create Archive button
		button=QtGui.QToolButton()
		button.setPopupMode(QtGui.QToolButton.InstantPopup)
		button.setArrowType(QtCore.Qt.NoArrow)
		button.setIconSize(QtCore.QSize(16,16))
		button.setIcon(QtGui.QIcon("%s/jdisk-public.png" % self.pluginDir))
		button.jid=unicode(jid.userhost())
		button.setToolTip("Jabbim Album")
		# add button to buttonGroup
		menu=QtGui.QMenu(button)
		action=menu.addAction(self.tr("Show my Jdisk in JDM"))
		action.setObjectName("show_my_disk_jdm")
		action=menu.addAction(self.tr("Show users Jdisk in JDM"))
		action.setObjectName("show_users_disk_jdm")
		menu.addSeparator()
		action=menu.addAction(self.tr("Show my Jdisk in browser"))
		action.setObjectName("show_my_disk")
		action=menu.addAction(self.tr("Show users Jdisk in browser"))
		action.setObjectName("show_users_disk")
		menu.addSeparator()
		action=menu.addAction(self.tr("Show my Album in browser"))
		action.setObjectName("show_my_album")
		action=menu.addAction(self.tr("Show users Album in browser"))
		action.setObjectName("show_users_album")
		QtCore.QObject.connect(menu, QtCore.SIGNAL("triggered ( QAction *)"),self.chatMenuItemTriggered)
		button.setMenu(menu)
		layout.addWidget(button)



	def sendFile(self):
		if self.typ=="public":
			self.main.sendFiles('public@disk.jabbim.cz')
		elif self.typ=="private":
			self.main.sendFiles('private@disk.jabbim.cz')
		elif self.typ=="album":
			self.main.sendFiles('album@disk.jabbim.cz')

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
	
	def dropEvent(self, event):
		if (event.mimeData().hasUrls()):
			urlList=event.mimeData().urls()
			if len(urlList)>0:
				new=[]
				for url in urlList:
					f=unicode(url.toLocalFile())
					if len(f)!=0:
						new.append(f)
				file=new
				if self.typ=="public":
					self.main.showFiletransferDialog(file, 'public@disk.jabbim.cz')
				elif self.typ=="private":
					self.main.showFiletransferDialog(file, 'private@disk.jabbim.cz')
				elif self.typ=="album":
					self.main.showFiletransferDialog(file, 'album@disk.jabbim.cz')
			event.acceptProposedAction()

	def dragMoveEvent(self, event):
		event.acceptProposedAction()
	def dragEnterEvent(self, event):
		if event.mimeData().hasText() or event.mimeData().hasFormat("text/uri-list"):
			event.acceptProposedAction()
		else:
			event.ignore()	
			
	def fileMenu(self,pos):
		items=self.window.ui.list.selectedItems()
		self.menu=QtGui.QMenu()
		action=self.menu.addAction(self.tr("Show files as icons"))
		action.setCheckable(True)
		if self.config['iconMode']=="True":
			action.setChecked(True)
		else:
			action.setChecked(False)
		QtCore.QObject.connect(action,QtCore.SIGNAL("triggered ( bool)"),self.setIconMode)
		if len(items)!=0:
			if len(items)>1:
				self.menu.addAction(self.tr("Download files"),self.downloadCurrentFile)
				if self.jid==self.main.client.jid.userhost():
					self.menu.addAction(self.tr("Remove files"),self.removeCurrentFile)
			else:
				self.menu.addAction(self.tr("Download file"),self.downloadCurrentFile)
				if self.jid==self.main.client.jid.userhost():
					self.menu.addAction(self.tr("Remove file"),self.removeCurrentFile)
		self.menu.popup(self.window.ui.list.mapToGlobal(pos))

	def downloadCurrentFile(self):
		items=self.window.ui.list.selectedItems()
		if len(items)==0:
			return
		for item in items:
			if self.typ=="public":
				self.main.client.sendMessage("public@disk.jabbim.cz", u"get "+self.jid+" "+unicode(item.text()))
			elif self.typ=="private":
				self.main.client.sendMessage("private@disk.jabbim.cz", u"get "+self.jid+" "+unicode(item.text()))
			elif self.typ=="album":
				self.main.client.sendMessage("album@disk.jabbim.cz", u"get "+self.jid+" "+unicode(item.text()))

	def removeCurrentFile(self):
		items=self.window.ui.list.selectedItems()
		if len(items)==0:
			return
		for item in items:
			if self.typ=="public":
				self.main.client.sendMessage("public@disk.jabbim.cz", u"rm "+unicode(item.text()))
			elif self.typ=="private":
				self.main.client.sendMessage("private@disk.jabbim.cz", u"rm "+unicode(item.text()))
			elif self.typ=="album":
				self.main.client.sendMessage("album@disk.jabbim.cz", u"rm "+unicode(item.text()))
		for i in range(len(items)):
			self.window.ui.list.takeItem(self.window.ui.list.row(items[0]))
			del items[0]

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

	def updateView(self, data):
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
	
	def call(self,jid=None,typ="public"):
		self.typ=typ
		if jid:
			self.jid=jid
			self.window.ui.line_jid.setText(self.jid)
		else:
			self.jid=unicode(self.window.ui.line_jid.text())
		print "call",self.jid,self.typ
		if self.typ=="public":
			self.main.client.callRemote('rpc@jabbim.cz/service', 'listPublic', (self.jid,)).addCallback(self.updateView)
		elif self.typ=="private":
			self.main.client.callRemote('rpc@jabbim.cz/service', 'listPrivate', (self.jid,)).addCallback(self.updateView)
		elif self.typ=="album":
			self.main.client.callRemote('rpc@jabbim.cz/service', 'listAlbum', (self.jid,)).addCallback(self.updateView)
		if self.jid != self.main.client.jid.userhost():
			self.window.ui.buttonDelete.setEnabled(False)
			self.window.ui.buttonUpload.setEnabled(False)
			self.window.ui.privateButton.setEnabled(False)
		else:
			self.window.ui.buttonDelete.setEnabled(True)
			self.window.ui.buttonUpload.setEnabled(True)
			self.window.ui.privateButton.setEnabled(True)
	
	
	def showSlot(self,jid=None):
		self.window.show()
		self.call(jid)
		self.window.ui.buttonDownload.setEnabled(False)
	
	def on_message(self, frm, typ, body, subject = None, xhtml = None,  chatstate = None,  delay = None,error=None):
		if self.typ=="public":
			text="public@disk.jabbim.cz"
		elif self.typ=="private":
			text="private@disk.jabbim.cz"
		elif self.typ=="album":
			text="album@disk.jabbim.cz"
		if unicode(frm).find(text)!=-1:
			if not self.window.isHidden():
				return False
		return True
		
	
	def on_ftEnd(self, sid, error = None): #pokud je error None je vse v poradku, jinak strucny popis chyby.
		if self.typ=="public":
			text="public@disk.jabbim.cz"
		elif self.typ=="private":
			text="private@disk.jabbim.cz"
		elif self.typ=="album":
			text="album@disk.jabbim.cz"
		if error == None and self.main.client.ft[sid].tojid.find(text)!=-1:
			self.call(typ=self.typ)
		
		print sid, error
			
	
	def clicked(self,item,old):
		self.window.ui.label_name.setText(item.text())
		data=item.data(32).toList()
		size=int(data[0].toString())
		self.window.ui.label_size.setText(self.toNormalSize(size))
		self.window.ui.buttonDelete.setEnabled(self.jid==self.main.client.jid.userhost())
		self.window.ui.buttonDownload.setEnabled(True)
