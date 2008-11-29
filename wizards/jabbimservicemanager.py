# -*- coding: utf-8 -*- 
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

import jsm_ui
import weakref
from widgets import servicediscovery, dataforms, legacyforms
from widgets.addcontactng import showDict, addDict, showWeather, addWeather

class jabbimServiceManager(QtGui.QDialog):
	def __init__(self,main,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.ui=jsm_ui.Ui_Dialog()
		self.ui.setupUi(self)
		self.main=weakref.ref(main)
		self.ui.treeWidget.hideColumn(2)
		self.ui.jids.hide()
		self.ui.add.hide()
		self.addFunc=None
		QtCore.QObject.connect(self.ui.treeWidget,QtCore.SIGNAL("currentItemChanged(QTreeWidgetItem *,QTreeWidgetItem *)"),self.itemChanged)
		QtCore.QObject.connect(self.ui.configure,QtCore.SIGNAL("clicked()"),self.configure)
		QtCore.QObject.connect(self.ui.add,QtCore.SIGNAL("clicked()"),self.add)
		QtCore.QObject.connect(self.ui.reg,QtCore.SIGNAL("clicked()"),self.register)
		self.loadServices()

	def _onRegister(self,data):
		if not data:
			return
		jid,legacy,form=data
		if form!=None:
			self.dialog=dataforms.dataFormsDialog(self.main(),form,jid,"register",self)
			self.dialog.show()
		else:
			self.dialog=legacyforms.legacyFormsDialog(self.main(),legacy,jid,"disco",self)
			self.dialog.show()

	def register(self):
		item = self.ui.treeWidget.currentItem()
		if not item:
			return
		d=self.main().client.getRegisterForm(unicode(item.data(0,32).toString()))
		d.addCallback(self._onRegister)

	def add(self):
		if self.addFunc:
			self.addFunc(self.main(),self.ui.jids)
		self.itemChanged(self.ui.treeWidget.currentItem(),None)

	def configure(self):
		item = self.ui.treeWidget.currentItem()
		if not item:
			return
		if unicode(item.data(0,32).toString())=="dict.jabbim.cz":
			showDict(self,self.main(),self.ui.jids)
			self.ui.reg.hide()
			self.ui.configure.hide()
			self.ui.add.show()
			self.ui.textBrowser.hide()
			self.ui.jids.show()
			self.addFunc=addDict
		elif unicode(item.data(0,32).toString())=="weather.netlab.cz":
			showWeather(self.main(),self.ui.jids)
			self.ui.reg.hide()
			self.ui.configure.hide()
			self.ui.add.show()
			self.ui.textBrowser.hide()
			self.ui.jids.show()
			self.addFunc=addWeather
	
	def itemChanged(self,item,old):
		if item:
			self.ui.add.hide()
			if unicode(item.text(2))[0]=="0":
				self.ui.reg.hide()
				self.ui.configure.show()
			else:
				self.ui.configure.hide()
				self.ui.reg.show()
			self.ui.jids.hide()
			self.ui.textBrowser.setHtml(item.data(1,32).toString())
			self.ui.textBrowser.show()
	
	def loadServices(self):
		trans=['icq.netlab.cz','icq.jabber.cz','icq.jabbim.cz']
		servs=['dict.jabbim.cz','weather.netlab.cz']
		transports={}
		services={}
		for transport in trans:
			transports[transport]=False
		for service in servs:
			services[service]=False
		
		for jd in self.main().client.roster['users'].keys():
			for transport in services:
				if jd.find(transport)!=-1:
					transports[transport]=True
					break
			for transport in transports:
				if jd==transport:
					transports[transport]=True
					break


		self.addService(self.tr("Dictionaries"),"dict.jabbim.cz",self.tr("<b>Dictionaries</b><br/>Dictionaries service allows you to translate words between languages from your Jabbim client."),transports["dict.jabbim.cz"])
		self.addService(self.tr("Weather"),"weather.jabbim.cz",self.tr("<b>Weather</b><br/>Weather service allows you to see actual weather in big cities.<br/>"),transports["weather.netlab.cz"])
		if transports["icq.netlab.cz"]:
			self.addService(self.tr("ICQ"),"icq.netlab.cz",self.tr("<b>ICQ</b><br/>ICQ transport allows you to chat with your friends who use ICQ."),transports["icq.netlab.cz"])
		elif transports["icq.jabbim.cz"]:
			self.addService(self.tr("ICQ"),"icq.jabbim.cz",self.tr("<b>ICQ</b><br/>ICQ transport allows you to chat with your friends who use ICQ."),transports["icq.jabbim.cz"])
		else:
			self.addService(self.tr("ICQ"),"icq.jabber.cz",self.tr("<b>ICQ</b><br/>ICQ transport allows you to chat with your friends who use ICQ."),transports["icq.jabber.cz"])
		#self.addService(self.tr("Weather"),"weather.jabbim.cz",self.tr("<b>Weather</b><br/>Weather service allows you to see actual weather in big cities.<br/>"),transports["weather.netlab.cz"])
		self.ui.treeWidget.resizeColumnToContents(0)
		self.ui.treeWidget.setMaximumWidth(150)
		self.ui.treeWidget.sortItems(2,QtCore.Qt.AscendingOrder)
	
	def addService(self,name,jid,description,registered=False):
		item=QtGui.QTreeWidgetItem(self.ui.treeWidget)
		item.setText(1,name)
		item.setIcon(0,self.main().getIcon("1@"+jid,status="online",size="16x16"))
		item.setData(0,32,QtCore.QVariant(unicode(jid)))
		item.setData(1,32,QtCore.QVariant(unicode(description)))
		if registered:
			item.setIcon(0,QtGui.QIcon("images/16x16/actions/ok.png"))
			item.setText(2,"0"+unicode(jid))
		else:
			item.setIcon(0,QtGui.QIcon())
			item.setText(2,"1"+unicode(jid))
		

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
				button=serviceButton(self,self.tr("ICQ Transport"),QtGui.QIcon("images/32x32/status/icq-online.png"),info,self.ui.regService)
				button.setPopupMode(QtGui.QToolButton.InstantPopup)
				self.registeredLayout.insertWidget(0,button)
				menu=QtGui.QMenu(button)
				menu.addAction(self.tr("Unregister"),self._unregisterICQ)
				button.setMenu(menu)
			else:
				info="""
				<h3>Jabber ICQ Transport Informations</h3>
				"""
				button=serviceButton(self,self.tr("ICQ Transport"),QtGui.QIcon("images/32x32/status/icq-online.png"),info,self.ui.regService)
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
