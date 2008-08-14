# -*- coding: utf8 -*-
import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from urllib import quote, unquote
from twisted.python import log
from include import utils
import base64
from widgets import dataforms,legacyforms
try:
	from hashlib import md5
except:
	log.msg('Please upgrade to python2.5')
	from md5 import new as md5

class config:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['iconMode']={'type':'boolean','label':self.main.tr("Show files as icons"),'value':'True'}

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'jdm'
		self.installTranslator()
		self.description = self.tr('Jabbim disk manager')
		self.author = u"Josef 'Pepeq' Halíček"
		self.name = self.tr('JDM Plugin')
		self.version = '0.1148'
		self.category = ['utils']
		self.url = 'http://dev.jabbim.cz/jabbim'
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
			self.esPath=""
			self.window.ui.buttonDownload.setIcon(QtGui.QIcon("%s/document-save.png" % self.pluginDir))
			self.window.ui.buttonUpload.setIcon(QtGui.QIcon("%s/upload.png" % self.pluginDir))
			self.window.ui.buttonDelete.setIcon(QtGui.QIcon("%s/edit-delete.png" % self.pluginDir))
			self.window.ui.buttonHome.setIcon(QtGui.QIcon("%s/home.png" % self.pluginDir))
			self.window.ui.publicButton.setIcon(QtGui.QIcon("%s/jdisk-public-24.png" % self.pluginDir))
			self.window.ui.privateButton.setIcon(QtGui.QIcon("%s/jdisk-private-24.png" % self.pluginDir))
			self.window.ui.albumButton.setIcon(QtGui.QIcon("%s/jalbum-32.png" % self.pluginDir))
			self.window.ui.easyshareButton.setIcon(QtGui.QIcon("%s/easy_share32.png" % self.pluginDir))
			self.window.ui.showMiniRoster.setIcon(self.main.ui.tabWidget.tabIcon(0))
			self.group=QtGui.QButtonGroup(self.window)
			self.update=False

			QtCore.QObject.connect(self.group,QtCore.SIGNAL("buttonClicked ( QAbstractButton * )"),self.buttonClicked)
			QtCore.QObject.connect(self.window.ui.reload,QtCore.SIGNAL("clicked()"),self.call)
			QtCore.QObject.connect(self.window.ui.esUp,QtCore.SIGNAL("clicked()"),self.esUp)
			QtCore.QObject.connect(self.window.ui.esPath,QtCore.SIGNAL("returnPressed()"),self.esPathFinished)
			QtCore.QObject.connect(self.window.ui.list, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem * , QListWidgetItem * )"),self.clicked)
			QtCore.QObject.connect(self.window.ui.list,QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.fileMenu)
			QtCore.QObject.connect(self.window.ui.buttonDownload,QtCore.SIGNAL("clicked()"),self.downloadCurrentFile)
			QtCore.QObject.connect(self.window.ui.buttonDelete,QtCore.SIGNAL("clicked()"),self.removeCurrentFile)
			QtCore.QObject.connect(self.window.ui.buttonUpload,QtCore.SIGNAL("clicked()"),self.sendFile)
			QtCore.QObject.connect(self.window.ui.buttonHome,QtCore.SIGNAL("clicked()"),self.home)
			QtCore.QObject.connect(self.window.ui.publicButton,QtCore.SIGNAL("clicked()"),self.public)
			QtCore.QObject.connect(self.window.ui.privateButton,QtCore.SIGNAL("clicked()"),self.private)
			QtCore.QObject.connect(self.window.ui.albumButton,QtCore.SIGNAL("clicked()"),self.album)
			QtCore.QObject.connect(self.window.ui.easyshareButton,QtCore.SIGNAL("clicked()"),self.easyshare)
			QtCore.QObject.connect(self.window.ui.showMiniRoster,QtCore.SIGNAL("clicked()"),self.showMiniRoster)
			QtCore.QObject.connect(self.window.ui.list,QtCore.SIGNAL("itemDoubleClicked ( QListWidgetItem * )"),self.doubleClicked)

			self.log = False
			self.registerHandler('on_message', self.on_message, priority=4)
			self.registerHandler('on_ftEnd', self.on_ftEnd, priority = 4)
			self.obsah=[]
			self.dnd={}
			if not os.path.exists(self.main.realHomeDir+"/jdmcache"):
				os.mkdir(self.main.realHomeDir+"/jdmcache")
			self.cache=self.main.realHomeDir+"/jdmcache"
			self.cacheList=self.getConfig(self.cache+"/list.cfg")
			self.filesToOpen=[]
			self.window.ui.progress=QtGui.QProgressBar(self.window.ui.statusbar)
			self.window.ui.statusbar.addWidget(self.window.ui.progress,1)
			self.window.ui.progress.hide()
			self.stopDownload=False
		else:
			self.loadConfig(homedir)
	
	def esPathFinished(self):
		self.esPath=unicode(self.window.ui.esPath.text())
		if not self.esPath.endswith("/") and self.esPath!="":
			self.espath+="/"
		if self.esPath=="":
			self.easyshare()
		else:
			contact = self.main.client.getContactByJid(self.jid)
			jid=self.jid+"/"+contact.getHighestResource()
			#self.window.ui.esPath.setText(self.esPath)
			self.main.client.callRemote(jid, 'listShare',(unicode(self.esPath),)).addCallback(self.updateView)	

	def esUp(self):
		d=self.esPath.split("/")
		if len(d)>2:
			self.esPath='/'.join(d[:-2])+"/"
			contact = self.main.client.getContactByJid(self.jid)
			jid=self.jid+"/"+contact.getHighestResource()
			self.window.ui.esPath.setText(self.esPath)
			self.main.client.callRemote(jid, 'listShare',(unicode(self.esPath),)).addCallback(self.updateView)
		elif len(self.esPath)!=0:
			self.easyshare()
	
	def easyshare(self):
		contact = self.main.client.getContactByJid(self.jid)
		if contact:
			jid=self.jid+"/"+contact.getHighestResource()
			self.main.client.callRemote(jid, 'getShares',()).addCallback(self.esGotShares)
			self.typ='easyshare'
			self.esPath=""
			#self.window.ui.esPath.setText(self.esPath)
			self.window.ui.esWidget.show()
	
	def esGotShares(self,data):
		data=data[0][0]
		self.window.ui.esPath.setText(self.esPath)
		self.window.ui.list.clear()
		icon=QtGui.QIcon(self.pluginDir+"/folder.png")
		for d in data:
			item=QtGui.QListWidgetItem(self.window.ui.list)
			item.setData(32,QtCore.QVariant(QtCore.QStringList([u"-1"])))
			item.setText(unicode(d))
			item.setIcon(icon)
	
	def buildContactMenu(self,menu,contact):
		"""
		Adds QAction to the menu above contact 
		"""
		self.action=menu.addAction(self.tr("Jabber Disk"))
		self.action.setData(QtCore.QVariant(unicode(contact.jid)))
		self.action.setObjectName("jdm_show_jdisk")
		self.action.setIcon(QtGui.QIcon("%s/jdisk-public-24.png" % self.pluginDir))
		QtCore.QObject.connect(self.action,QtCore.SIGNAL("triggered ( bool )"),self.contactMenuToggled)

	def contactMenuToggled(self,b):
		"""
		User choose our QAction from contactMenu (menu above contact)
		"""
		jid=unicode(self.action.data().toString())
		self.showSlot(jid)
		self.action.deleteLater()

	def showMiniRoster(self):
		self.main.ui.roster.showMiniRoster(self.miniRosterAccepted)
	
	def miniRosterAccepted(self,jid):
		self.call(jid,'public')
		

	def setIconMode(self,bool):
		if bool:
			if self.typ=="album":
				self.window.ui.list.setGridSize(QtCore.QSize(160,160))
			else:
				self.window.ui.list.setGridSize(QtCore.QSize(128,96))
			self.window.ui.list.setViewMode(QtGui.QListView.IconMode)
			self.config["iconMode"]='True'
		else:
			self.window.ui.list.setGridSize(QtCore.QSize())
			self.window.ui.list.setViewMode(QtGui.QListView.ListMode)
			self.config["iconMode"]='False'
		self.config.write()

	def public(self):
		self.window.ui.esWidget.hide()
		self.call(typ='public')

	def private(self):
		self.window.ui.esWidget.hide()
		self.call(typ='private')

	def album(self):
		self.window.ui.esWidget.hide()
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
		elif cmd=="show_my_album_jdm":
			self.showSlot(self.main.client.jid.userhost(),typ='album')
		elif cmd=="show_users_disk_jdm":
			self.showSlot(unicode(action.parent().parent().jid))
		elif cmd=="show_users_album_jdm":
			self.showSlot(unicode(action.parent().parent().jid),typ="album")
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
		# my
		action=menu.addAction(self.tr("Show my Jdisk in JDM"))
		action.setObjectName("show_my_disk_jdm")
		action=menu.addAction(self.tr("Show my Album in JDM"))
		action.setObjectName("show_my_album_jdm")
		action=menu.addAction(self.tr("Show my Jdisk in browser"))
		action.setObjectName("show_my_disk")
		action=menu.addAction(self.tr("Show my Album in browser"))
		action.setObjectName("show_my_album")
		menu.addSeparator()
		# users
		action=menu.addAction(self.tr("Show users Jdisk in JDM"))
		action.setObjectName("show_users_disk_jdm")
		action=menu.addAction(self.tr("Show users Album in JDM"))
		action.setObjectName("show_users_album_jdm")
		action=menu.addAction(self.tr("Show users Jdisk in browser"))
		action.setObjectName("show_users_disk")
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
		elif event.mimeData().hasText():
			# test if it is JID
			jid2=self.main.getJid(unicode(event.mimeData().text()))
			if not jid2:
				event.ignore()
				return
			else:
				self.window.ui.line_jid.setText(unicode(jid2.userhost()))
				event.acceptProposedAction()

	def dragMoveEvent(self, event):
		event.acceptProposedAction()
	def dragEnterEvent(self, event):
		if event.mimeData().hasText() or event.mimeData().hasFormat("text/uri-list"):
			event.acceptProposedAction()
		elif event.mimeData().hasText():
			if self.main.getJid(unicode(event.mimeData().text())):
				event.acceptProposedAction()
			else:
				event.ignore()
		else:
			event.ignore()	
			
	def fileMenu(self,pos):
		items=self.window.ui.list.selectedItems()
		self.menu=QtGui.QMenu()
		#action=self.menu.addAction(self.tr("Show files as icons"))
		#action.setCheckable(True)
		#if self.config['iconMode']=="True":
			#action.setChecked(True)
		#else:
			#action.setChecked(False)
		#QtCore.QObject.connect(action,QtCore.SIGNAL("triggered ( bool)"),self.setIconMode)
		if len(items)!=0:
			if len(items)>1:
				self.menu.addAction(self.tr("Download files"),self.downloadCurrentFile)
				if self.jid==self.main.client.jid.userhost():
					self.menu.addAction(self.tr("Remove files"),self.removeCurrentFile)
				if self.typ!="private":
					self.menu.addAction(self.tr("Copy links to clipboard"),self.copyToClipboard)
			else:
				self.menu.addAction(self.tr("Download file"),self.downloadCurrentFile)
				if self.jid==self.main.client.jid.userhost():
					self.menu.addAction(self.tr("Remove file"),self.removeCurrentFile)
				if self.typ!="private":
					self.menu.addAction(self.tr("Copy link to clipboard"),self.copyToClipboard)
			self.menu.popup(self.window.ui.list.mapToGlobal(pos))

	def copyToClipboard(self):
		items=self.window.ui.list.selectedItems()
		if len(items)==0:
			return
		text=""
		for item in items:
			if self.typ=="public":
				text+="http://disk.jabbim.cz/"+self.jid+"/"+unicode(item.text().replace(" ", "%20"))+"\n"
			elif self.typ=="album":
				text+="http://album.jabbim.cz/"+self.jid+"/"+unicode(item.text().replace(" ", "%20"))+"\n"
		QtGui.QApplication.clipboard().setText(text[:-1])

	def downloadCurrentFile(self):
		items=self.window.ui.list.selectedItems()
		if len(items)==0:
			return
		if self.typ=="easyshare":
			contact = self.main.client.getContactByJid(self.jid)
			if contact:
				jid=self.jid+"/"+contact.getHighestResource()
				data=[]
				for item in items:
					data.append(self.esPath+unicode(item.text()))
				self.main.client.callRemote(jid, 'getFiles',(data,))
		else:
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
		if not self.update:
			self.window.ui.list.clear()
		self.window.ui.esPath.setText(self.esPath)
		data=data[0][0]
		self.thumbs={}
		for file in data:
			if self.update:
				items=self.window.ui.list.findItems(file[0],QtCore.Qt.MatchExactly)
				if len(items)!=0:
					continue
			name=file[0]
			size=file[1]
			item=QtGui.QListWidgetItem(unicode(name))
			item.setData(32,QtCore.QVariant(QtCore.QStringList([unicode(size)])))
			if int(size)==-1:
				item.setIcon(QtGui.QIcon(self.pluginDir+"/folder.png"))
			else:
				ext=name.split('.')[-1]
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
			if self.typ=="album":
				self.thumbs[name]=item
		data=self.thumbs.keys()
		if self.typ=="album" and len(data)!=0:
			self.stopDownload=False
			self.window.ui.progress.setValue(0)
			self.window.ui.progress.setMaximum(len(data))
			self.window.ui.progress.show()
			self.main.client.callRemote('rpc@jabbim.cz/service', 'getThumb', (self.jid,data[0])).addCallback(self.thumbArrived,data)
		if self.update==True:
			self.update=False

	def thumbArrived(self,thumb,data,check=True):
		cacheFile="%s/%s.jpg" % (self.cache,self.jid+data[0])
		if thumb:
			print "saving",data[0],check
			image=base64.decodestring(str(thumb[0]))
			pixmap=QtGui.QPixmap()
			pixmap.loadFromData(image)
			self.thumbs[data[0]].setIcon(QtGui.QIcon(pixmap))
			f=open(cacheFile,"wb")
			f.write(image)
			f.close()
			self.cacheList[cacheFile] = md5(image).hexdigest()
			self.cacheList.write()
		else:
			self.thumbs[data[0]].setIcon(QtGui.QIcon(cacheFile))
		self.window.ui.progress.setValue(self.window.ui.progress.value()+1)
		del data[0]
		if len(data)==0:
			self.thumbs={}
			self.window.ui.progress.hide()

			#if check:
				#data=self.thumbs.keys()
				#self.main.client.callRemote('rpc@jabbim.cz/service', 'getHash', (self.jid,data[0])).addCallback(self.hashArrived,data)
		else:
			if not self.stopDownload:
				cacheFile="%s/%s.jpg" % (self.cache,self.jid+data[0])
				if os.path.isfile(cacheFile):
					self.main.client.reactor.callLater(0,self.thumbArrived,None,data)
				else:
					self.main.client.callRemote('rpc@jabbim.cz/service', 'getThumb', (self.jid,data[0])).addCallback(self.thumbArrived,data)
			else:
				self.stopDownload=False
				self.thumbs={}
				self.window.ui.progress.hide()

	def hashArrived(self,hs,data):
		hs=hs[0][0]
		cacheFile="%s/%s.jpg" % (self.cache,self.jid+data[0])
		download=True
		if self.cacheList.has_key(cacheFile):
			print data[0],hs,self.cacheList[cacheFile]
			if self.cacheList[cacheFile]==hs:
				download=False
		if download:
			self.main.client.callRemote('rpc@jabbim.cz/service', 'getThumb', (self.jid,data[0])).addCallback(self.thumbArrived,[data[0]],False)
		del data[0]
		if len(data)!=0:
			cacheFile="%s/%s.jpg" % (self.cache,self.jid+data[0])
			self.main.client.callRemote('rpc@jabbim.cz/service', 'getHash', (self.jid,data[0])).addCallback(self.hashArrived,data)
		

	def buildMainWindowMenu(self):
		menu=self.mainWindowMenu()
		menu.addAction("Jabbim disk manager",self.showSlot)
	
	def call(self,jid=None,typ=None):
		self.stopDownload=True
		self.window.ui.label_size.setText("")
		self.window.ui.label_name.setText("")
		if typ:
			self.typ=typ
		if jid:
			self.jid=jid
			self.window.ui.line_jid.setText(self.jid)
		else:
			self.jid=unicode(self.window.ui.line_jid.text())
		print "call",self.jid,self.typ
		if self.typ=="public":
			self.main.client.callRemote('rpc@jabbim.cz/service', 'listPublic', (self.jid,)).addCallback(self.updateView)
			self.window.ui.list.setIconSize(QtCore.QSize(32,32))
			self.window.ui.list.setGridSize(QtCore.QSize(128,96))
			self.window.ui.esWidget.hide()
		elif self.typ=="private":
			self.main.client.callRemote('rpc@jabbim.cz/service', 'listPrivate', (self.jid,)).addCallback(self.updateView)
			self.window.ui.list.setIconSize(QtCore.QSize(32,32))
			self.window.ui.list.setGridSize(QtCore.QSize(128,96))
			self.window.ui.esWidget.hide()
		elif self.typ=="album":
			self.main.client.callRemote('rpc@jabbim.cz/service', 'listAlbum', (self.jid,)).addCallback(self.updateView)
			#if self.config['iconMode']=="True":
			self.window.ui.list.setIconSize(QtCore.QSize(128,128))
			self.window.ui.list.setGridSize(QtCore.QSize(160,160))
			self.window.ui.esWidget.hide()

		if self.jid != self.main.client.jid.userhost():
			self.window.ui.buttonDelete.setEnabled(False)
			self.window.ui.buttonUpload.setEnabled(False)
			self.window.ui.privateButton.setEnabled(False)
		else:
			self.window.ui.buttonDelete.setEnabled(True)
			self.window.ui.buttonUpload.setEnabled(True)
			self.window.ui.privateButton.setEnabled(True)
	
	
	def showSlot(self,jid=None,typ='public'):
		self.window.show()
		if self.main.client.isVip:
			self.window.ui.vipInfo.hide()
		else:
			self.window.ui.vipInfo.show()
		if (not self.main.client.roster['users'].has_key("public@disk.jabbim.cz") or not self.main.client.roster['users'].has_key("private@disk.jabbim.cz")) or not self.main.client.roster['users'].has_key("album@disk.jabbim.cz"):
			d=self.main.client.getRegisterForm("disk.jabbim.cz")
			d.addCallback(self._onRegister)
		self.call(jid,typ)
		self.window.ui.buttonDownload.setEnabled(False)

	def _onRegister(self,data):
		if not data:
			return
		jid,legacy,form=data
		if form!=None:
			self.dialog=dataforms.dataFormsDialog(self.main,form,jid,"register",self)
			self.dialog.show()
		else:
			self.dialog=legacyforms.legacyFormsDialog(self.main,legacy,jid,"disco",self.window)
			self.dialog.show()
	
	def on_message(self,msg):
		frm, typ, body, subject ,  xhtml,chatstate ,  delay, error = msg.legacyUnpack()
		if self.typ=="public":
			text="public@disk.jabbim.cz"
		elif self.typ=="private":
			text="private@disk.jabbim.cz"
		elif self.typ=="album":
			text="album@disk.jabbim.cz"
		else:
			return True
		if unicode(frm).find(text)!=-1:
			if not self.window.isHidden():
				return False
		return True

	def on_ftEnd(self, sid, error = None): #pokud je error None je vse v poradku, jinak strucny popis chyby.
		if not self.window.isHidden():
			if self.typ=="public":
				text="public@disk.jabbim.cz"
			elif self.typ=="private":
				text="private@disk.jabbim.cz"
			elif self.typ=="album":
				text="album@disk.jabbim.cz"
			filename=unicode(self.main.client.ft[sid].file)
			if error == None and self.main.client.ft[sid].tojid.find(text)!=-1 and not filename in self.filesToOpen:
				self.update=True
				self.call(typ=self.typ)
			if filename in self.filesToOpen:
				self.filesToOpen.remove(filename)
				if self.main.allowedJids.has_key(text+"/"+self.main.client.ft[sid].fileprops['name']):
					del self.main.allowedJids[text+"/"+self.main.client.ft[sid].fileprops['name']]
				if error==None:
					if sys.platform == 'win32':
						filename=filename.replace("/","\\")
						print "open win32",[filename]
						os.startfile(filename)
					else:
						print "open linux",[filename]
						os.system(u"xdg-open \"%s\"" % filename.encode('utf8'))
			

	def clicked(self,item,old):
		if item:
			self.window.ui.label_name.setText(item.text())
			data=item.data(32).toList()
			size=int(data[0].toString())
			if size==-1:
				self.window.ui.label_size.setText(self.tr("Folder"))
				self.window.ui.buttonDelete.setEnabled(self.jid==self.main.client.jid.userhost())
				self.window.ui.buttonDownload.setEnabled(True)
			else:
				self.window.ui.label_size.setText(self.toNormalSize(size))
				self.window.ui.buttonDelete.setEnabled(False)
				self.window.ui.buttonDownload.setEnabled(False)
		else:
			self.window.ui.buttonDelete.setEnabled(False)
			self.window.ui.buttonDownload.setEnabled(False)
			self.window.ui.label_size.setText("")
			self.window.ui.label_name.setText("")

	def doubleClicked(self,item):
		if self.typ=="public":
			self.main.allowedJids["public@disk.jabbim.cz/"+unicode(item.text())]=self.cache
			self.main.client.sendMessage("public@disk.jabbim.cz", u"get "+self.jid+" "+unicode(item.text()))
			self.filesToOpen.append(self.cache+"/"+unicode(item.text()))
		elif self.typ=="private":
			self.main.allowedJids["private@disk.jabbim.cz/"+unicode(item.text())]=self.cache
			self.main.client.sendMessage("private@disk.jabbim.cz", u"get "+self.jid+" "+unicode(item.text()))
			self.filesToOpen.append(self.cache+"/"+unicode(item.text()))
		elif self.typ=="album":
			self.main.allowedJids["album@disk.jabbim.cz/"+unicode(item.text())]=self.cache
			self.main.client.sendMessage("album@disk.jabbim.cz", u"get "+self.jid+" "+unicode(item.text()))
			self.filesToOpen.append(self.cache+"/"+unicode(item.text()))
		elif self.typ=="easyshare":
			contact = self.main.client.getContactByJid(self.jid)
			if contact:
				jid=self.jid+"/"+contact.getHighestResource()
				self.esPath+=unicode(item.text())+"/"
				self.main.client.callRemote(jid, 'listShare',(unicode(self.esPath),)).addCallback(self.updateView)

		
