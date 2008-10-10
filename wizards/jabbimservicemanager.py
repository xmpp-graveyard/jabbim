# -*- coding: utf-8 -*- 
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

import jabbimservicemanager_ui
import weakref
from widgets import servicediscovery
#445223432
#class JabberDiskService:
#	def __init__(self):
		#self.info="""
			#<h3>Jabber Disk informations</h3>
#			"""
		#self.title="Jabber Disk"
#		self.icon=QtGui.QIcon("images/32x32/status/disk-online.png")

class serviceButton(QtGui.QToolButton):
	def __init__(self,manager,title,icon,info,parent):
		QtGui.QToolButton.__init__(self,parent)
		self.manager=weakref.proxy(manager)
		self.title=title
		self.info=info
		self.setText(title)
		self.setIcon(icon)
		self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
		self.setIconSize(QtCore.QSize(32,32))
		self.setMouseTracking(True)
	
	def mouseMoveEvent(self,event):
		if self.manager.currentInfo!=self.title:
			self.manager.currentInfo=self.title
			self.manager.ui.info.setHtml(self.info)
		return QtGui.QToolButton.mouseMoveEvent(self,event)

class jabbimServiceManager(QtGui.QDialog):
	def __init__(self,main,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.ui=jabbimservicemanager_ui.Ui_jabbimServiceManager()
		self.ui.setupUi(self)
		self.main=weakref.ref(main)
		self.registerLayout=QtGui.QHBoxLayout(self.ui.registerService)
		self.registeredLayout=QtGui.QHBoxLayout(self.ui.registeredServices)
		self.currentInfo=""
		self.loadServices()
		QtCore.QObject.connect(self.ui.registerJabberDisk,QtCore.SIGNAL("clicked()"),self._registerJabberDisk)
		QtCore.QObject.connect(self.ui.registerIcq,QtCore.SIGNAL("clicked()"),self._registerICQ)
		QtCore.QObject.connect(self.ui.registerDictionaries,QtCore.SIGNAL("clicked()"),self._registerDict)
		QtCore.QObject.connect(self.ui.back,QtCore.SIGNAL("clicked()"),self.home)
		QtCore.QObject.connect(self.ui.advanced,QtCore.SIGNAL("clicked()"),self.advanced)
		self.home()
	
	def advanced(self):
		self.discovery=servicediscovery.serviceDiscoveryDialog(self.main,self)
		self.discovery.show()
		self.hide()
	
	def home(self):
		self.ui.stackedWidget.setCurrentIndex(0)
		self.ui.back.hide()
	
	def loadServices(self):
		for i in range(self.registerLayout.count()):
			item=self.registerLayout.itemAt(0)
			if item.widget():
				item.widget().setParent(None)
			else:
				self.registerLayout.removeItem(item)
		for i in range(self.registeredLayout.count()):
			item=self.registeredLayout.itemAt(0)
			if item.widget():
				item.widget().setParent(None)
			else:
				self.registeredLayout.removeItem(item)

		dict=False
		weather=False
		for jd in self.main().client.roster['users'].keys():
			if jd.find("dict.jabbim.cz")!=-1:
				dict=True
			if jd.find("weather.netlab.cz"):
				weather=True

		# Jabber disk
		info="""
		<h3>Jabber Disk informations</h3>
		"""
		if (not self.main().client.roster['users'].has_key("public@disk.jabbim.cz") or not self.main().client.roster['users'].has_key("private@disk.jabbim.cz")) or not self.main().client.roster['users'].has_key("album@disk.jabbim.cz"):

			button=serviceButton(self,self.tr("Jabber Disk"),QtGui.QIcon("images/32x32/status/disk-online.png"),info,self.ui.registerService)
			self.registerLayout.addWidget(button)
			QtCore.QObject.connect(button,QtCore.SIGNAL("clicked()"),self.registerJabberDisk)
		else:
			button=serviceButton(self,self.tr("Jabber Disk"),QtGui.QIcon("images/32x32/status/disk-online.png"),info,self.ui.registeredServices)
			button.setPopupMode(QtGui.QToolButton.InstantPopup)
			self.registeredLayout.addWidget(button)
			menu=QtGui.QMenu(button)
			menu.addAction(self.tr("Unregister"),self._unregisterJabberDisk)
			button.setMenu(menu)

		# Weather
		info="""
		<h3>Jabber Weather Informations</h3>
		"""
		if weather:
			button=serviceButton(self,self.tr("Weather"),QtGui.QIcon("images/32x32/status/weather-online.png"),info,self.ui.registerService)
			self.registerLayout.addWidget(button)
			QtCore.QObject.connect(button,QtCore.SIGNAL("clicked()"),self.registerWeather)
		else:
			button=serviceButton(self,self.tr("Weather"),QtGui.QIcon("images/32x32/status/weather-online.png"),info,self.ui.registeredServices)
			button.setPopupMode(QtGui.QToolButton.InstantPopup)
			self.registeredLayout.addWidget(button)
			menu=QtGui.QMenu(button)
			menu.addAction(self.tr("Unregister"),self._unregisterWeather)
			button.setMenu(menu)
			
		#ICQ JIT
		self.loadICQService()
		#DICT
		if dict:
			info="""
			<h3>Jabber Dictionaries Informations</h3>
			"""
			button=serviceButton(self,self.tr("Dictionaries"),QtGui.QIcon("images/32x32/apps/jabbim.png"),info,self.ui.registeredServices)
			button.setPopupMode(QtGui.QToolButton.InstantPopup)
			self.registeredLayout.addWidget(button)
			menu=QtGui.QMenu(button)
			menu.addAction(self.tr("Change registered dictionaries"),self.registerDict)
			menu.addAction(self.tr("Unregister"),self._unregisterDict)
			button.setMenu(menu)
		else:
			info="""
			<h3>Jabber Dictionaries Informations</h3>
			"""
			button=serviceButton(self,self.tr("Dictionaries"),QtGui.QIcon("images/32x32/apps/jabbim.png"),info,self.ui.registerService)
			self.registerLayout.addWidget(button)
			QtCore.QObject.connect(button,QtCore.SIGNAL("clicked()"),self.registerDict)
		
		self.registerLayout.addStretch()
		self.registeredLayout.addStretch()

	def registerWeather(self):
		pass
		
	def unregisterWeather(self):
		pass
		
	def _unregisterDict(self):
		jid="dict.jabbim.cz"
		j = self.main().getJid(jid)
		for jd in self.main().client.roster['users'].iterkeys():
			if jd.find(j.host) != -1:
				self.main().client.delContact(jd)
		self.home()
		self.main().client.reactor.callLater(1,self.loadServices)
		
	def registerDict(self):
		self.ui.stackedWidget.setCurrentIndex(3)
		self.ui.back.show()
		d={}
		d['cze2eng@dict.jabbim.cz']= self.tr("Czech to English")
		d['cze2fre@dict.jabbim.cz']= self.tr("Czech to French")
		d['cze2ger@dict.jabbim.cz']= self.tr("Czech to German")
		d['cze2ita@dict.jabbim.cz']= self.tr("Czech to Italian")
		d['cze2lat@dict.jabbim.cz']= self.tr("Czech to Latin")
		d['cze2rus@dict.jabbim.cz']= self.tr("Czech to Russian")
		d['cze2spa@dict.jabbim.cz']= self.tr("Czech to Spanish")
		d['eng2cze@dict.jabbim.cz']= self.tr("English to Czech")
		d['eng2epo@dict.jabbim.cz']= self.tr("English to Esperanto")
		d['eng2fre@dict.jabbim.cz']= self.tr("English to French")
		d['eng2ger@dict.jabbim.cz']= self.tr("English to German")
		d['eng2ita@dict.jabbim.cz']= self.tr("English to Italian")
		d['eng2lat@dict.jabbim.cz']= self.tr("English to Latin")
		d['eng2por@dict.jabbim.cz']= self.tr("English to Portugese")
		d['eng2spa@dict.jabbim.cz']= self.tr("English to Spanish")
		d['epo2eng@dict.jabbim.cz']= self.tr("Esperanto to English")
		d['fre2cze@dict.jabbim.cz']= self.tr("French to Czech")
		d['fre2eng@dict.jabbim.cz']= self.tr("French to English")
		d['fre2ger@dict.jabbim.cz']= self.tr("French to German")
		d['fre2ita@dict.jabbim.cz']= self.tr("French to Italian")
		d['fre2spa@dict.jabbim.cz']= self.tr("French to Spanish")
		d['ger2cze@dict.jabbim.cz']= self.tr("German to Czech")
		d['ger2eng@dict.jabbim.cz']= self.tr("German to English")
		d['ger2fre@dict.jabbim.cz']= self.tr("German to French")
		d['ger2spa@dict.jabbim.cz']= self.tr("German to Spanish")
		d['ita2cze@dict.jabbim.cz']= self.tr("Italian to Czech")
		d['ita2eng@dict.jabbim.cz']= self.tr("Italian to English")
		d['ita2fre@dict.jabbim.cz']= self.tr("Italian to French")
		d['lat2cze@dict.jabbim.cz']= self.tr("Latin to Czech")
		d['lat2eng@dict.jabbim.cz']= self.tr("Latin to English")
		d['por2eng@dict.jabbim.cz']= self.tr("Portugese to English")
		d['por2spa@dict.jabbim.cz']= self.tr("Portugese to Spanish")
		d['rus2cze@dict.jabbim.cz']= self.tr("Russian to Czech")
		d['spa2cze@dict.jabbim.cz']= self.tr("Spanish to Czech")
		d['spa2eng@dict.jabbim.cz']= self.tr("Spanish to English")
		d['spa2fre@dict.jabbim.cz']= self.tr("Spanish to French")
		d['spa2ger@dict.jabbim.cz']= self.tr("Spanish to German")
		d['spa2por@dict.jabbim.cz']= self.tr("Spanish to Portugese")
		d['ciz2cze@dict.jabbim.cz']= self.tr("Foreign words to Czech")

		self.ui.dictionaries.clear()
		for jid,name in d.iteritems():
			item=QtGui.QTreeWidgetItem(self.ui.dictionaries)
			if not name:
				item.setText(0,jid)
			else:
				item.setText(0,name)
			item.jid=jid
			registered=self.main().client.roster['users'].has_key(jid)
			if registered:
				item.registered=QtCore.Qt.Checked
				item.setCheckState(0,QtCore.Qt.Checked)
			else:
				item.setCheckState(0,QtCore.Qt.Unchecked)
				item.registered=QtCore.Qt.Unchecked
		self.ui.dictionaries.sortItems(0,QtCore.Qt.AscendingOrder)
	
	def _registerDict(self):
		for i in range(0,int(self.ui.dictionaries.topLevelItemCount())):
			item=self.ui.dictionaries.topLevelItem(i)
			if item.checkState(0)!=item.registered:
				if item.checkState(0)==QtCore.Qt.Checked:
					self.main().autoAdd[unicode(item.jid)]={}
					self.main().client.addContact(unicode(item.jid),"",unicode(item.text(0)),[unicode(self.tr("Dictionaries"))])
				else:
					self.main().client.delContact(unicode(item.jid))
		self.home()
		self.main().client.reactor.callLater(1,self.loadServices)

	def registerICQ(self):
		self.ui.stackedWidget.setCurrentIndex(2)
		self.ui.back.show()
	
	def loadICQService(self,data=None):
		print "icq",data
		if not data:
			d=self.main().client.getRegisterForm("icq.jabber.cz")
			d.addCallback(self.loadICQService)
		else:
			jid,legacy,form=data
			if legacy.has_key("registered"):
				info="""
				<h3>Jabber ICQ Transport Informations</h3>
				"""
				button=serviceButton(self,self.tr("ICQ Transport"),QtGui.QIcon("images/32x32/status/icq-online.png"),info,self.ui.registerService)
				button.setPopupMode(QtGui.QToolButton.InstantPopup)
				self.registeredLayout.insertWidget(0,button)
				menu=QtGui.QMenu(button)
				menu.addAction(self.tr("Unregister"),self._unregisterICQ)
				button.setMenu(menu)
			else:
				info="""
				<h3>Jabber ICQ Transport Informations</h3>
				"""
				button=serviceButton(self,self.tr("ICQ Transport"),QtGui.QIcon("images/32x32/status/icq-online.png"),info,self.ui.registerService)
				self.registerLayout.insertWidget(0,button)
				QtCore.QObject.connect(button,QtCore.SIGNAL("clicked()"),self.registerICQ)
	
	def _unregisterICQ(self,data=None):
		if not data:
			d=self.main().client.setRegisterForm("icq.jabber.cz",remove=True)
			d.addCallback(self._unregisterICQ)
		else:
			jid="icq.jabber.cz"
			self.main().client.delContact(jid)
			j = self.main().getJid(jid)
			for jd in self.main().client.roster['users'].iterkeys():
				if jd.find(j.host) != -1:
					self.main().client.delContact(jd)

	def _registerICQ(self,data=None):
		if not data:
			d=self.main().client.getRegisterForm("icq.jabber.cz")
			d.addCallback(self._registerICQ)
		else:
			jid,legacy,form=data
			ret={}
			ret['password']=unicode(self.ui.icqPassword.text())
			if legacy.has_key('key'):
				ret['key']=unicode(legacy['key'])
			ret['username']=unicode(self.ui.icqNumber.text())
			self.main().autoAdd["icq.jabber.cz"]={"group":"ICQ"}
			self.main().client.setRegisterForm("icq.jabber.cz",legacy=ret)
			self.home()
			self.main().client.reactor.callLater(1,self.loadServices)

	def registerJabberDisk(self):
		self.ui.stackedWidget.setCurrentIndex(1)
		self.ui.back.show()

	def _unregisterJabberDisk(self):
		if self.main().client.roster['users'].has_key("public@disk.jabbim.cz"):
			self.main().client.delContact("public@disk.jabbim.cz")
		if self.main().client.roster['users'].has_key("private@disk.jabbim.cz"):
			self.main().client.delContact("private@disk.jabbim.cz")
		if self.main().client.roster['users'].has_key("album@disk.jabbim.cz"):
			self.main().client.delContact("album@disk.jabbim.cz")
		self.main().client.reactor.callLater(1,self.loadServices)
	
	def _registerJabberDisk(self,data=None):
		if not data:
			d=self.main().client.getRegisterForm("disk.jabbim.cz")
			d.addCallback(self._registerJabberDisk)
		else:
			self.main().autoAdd['public@disk.jabbim.cz']={"name":self.tr("Public"),"group":"Disk"}
			self.main().autoAdd['private@disk.jabbim.cz']={"name":self.tr("Private"),"group":"Disk"}
			self.main().autoAdd['album@disk.jabbim.cz']={"name":self.tr("Album"),"group":"Disk"}
			self.main().client.setRegisterForm("disk.jabbim.cz",legacy={})
			self.home()
			self.main().client.reactor.callLater(2,self.loadServices)
