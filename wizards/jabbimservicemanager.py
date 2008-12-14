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
		self.ui=jsm_ui.Ui_JabbimServiceManager()
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
		QtCore.QObject.connect(self.ui.advanced,QtCore.SIGNAL("clicked()"),self.advanced)
		self.loadServices()

	def advanced(self):
		self.discovery=servicediscovery.serviceDiscoveryDialog(self.main,self)
		self.discovery.show()
		self.hide()

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
		registered=unicode(item.text(2))[0]=="0"
		jid=unicode(item.data(0,32).toString())
		print jid,registered
		if not registered:
			if jid=="disk.jabbim.cz":
				self.registerJabberDisk()
				self.setItemRegistered(item,True)
			elif jid in ["weather.netlab.cz","dict.jabbim.cz"]:
				self.configure()
			else:
				d=self.main().client.getRegisterForm(jid)
				d.addCallback(self._onRegister)
		else:
			if jid=="disk.jabbim.cz":
				self.unregisterJabberDisk()
				self.setItemRegistered(item,False)
			elif jid=="dict.jabbim.cz":
				self.removeServiceContacts("dict.jabbim.cz")
				self.setItemRegistered(item,False)
			elif jid=="weather.netlab.cz":
				self.removeServiceContacts("weather.netlab.cz")
				self.setItemRegistered(item,False)

	def setItemRegistered(self,item,registered):
		if registered:
			item.setText(2,"0"+unicode(item.data(0,32).toString()))
			item.setIcon(0,QtGui.QIcon("images/16x16/actions/ok.png"))
		else:
			item.setText(2,"1"+unicode(item.data(0,32).toString()))
			item.setIcon(0,QtGui.QIcon())
		self.ui.treeWidget.resizeColumnToContents(0)
		self.ui.treeWidget.sortItems(2,QtCore.Qt.AscendingOrder)
		self.itemChanged(item,None)

	def add(self):
		if self.addFunc:
			self.addFunc(self.main(),self.ui.jids)
		if (self.ui.treeWidget.currentItem().text(2))[0]=="1":
			self.setItemRegistered(self.ui.treeWidget.currentItem(),True)
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
		else:
			d=self.main().client.getRegisterForm(unicode(item.data(0,32).toString()))
			d.addCallback(self._onRegister)

	def itemChanged(self,item,old):
		if item:
			self.ui.add.hide()
			if unicode(item.text(2))[0]=="0":
				self.ui.reg.setText(self.tr("Unregister"))
				if not unicode(item.data(0,32).toString()) in ["disk.jabbim.cz"]:
					self.ui.configure.show()
			else:
				self.ui.configure.hide()
				self.ui.reg.setText(self.tr("Register"))
			self.ui.reg.show()
			self.ui.jids.hide()
			self.ui.textBrowser.setHtml(item.data(1,32).toString())
			self.ui.textBrowser.show()
	
	def loadServices(self):
		self.ui.treeWidget.clear()
		trans=['icq.netlab.cz','icq.jabber.cz','icq.jabbim.cz','sms.netlab.cz','sms.jabbim.cz']
		servs=['dict.jabbim.cz','weather.netlab.cz','disk.jabbim.cz']
		transports={}
		services={}
		for transport in trans:
			transports[transport]=False
		for service in servs:
			services[service]=False
		
		for jd in self.main().client.roster['users'].keys():
			for transport in services:
				if jd.find(transport)!=-1:
					services[transport]=True
					break
			for transport in transports:
				if self.main().getJid(jd).userhost()==transport:
					transports[transport]=True
					break


		self.addService(self.tr("Dictionaries"),"dict.jabbim.cz",self.tr("<b>Dictionaries</b><br/>Dictionaries service allows you to translate words between languages from your Jabbim client."),services["dict.jabbim.cz"])
		self.addService(self.tr("Weather"),"weather.netlab.cz",self.tr("<b>Weather</b><br/>Weather service allows you to see actual weather in big cities."),services["weather.netlab.cz"])
		self.addService(self.tr("Jabber Disk"),"disk.jabbim.cz",self.tr("<b>Jabber Disk</b><br/>Jabber Disk allows you to upload files to Jabbim server where they can be downloaded by your friends."),services["disk.jabbim.cz"])
		self.addService(self.tr("SMS Vodafone/O2"),"sms.netlab.cz",self.tr("<b>SMS Vodafone/O2</b><br/>SMS Vodafone/O2 allows you to send SMS messages straight from your Jabbim Client."),transports["sms.netlab.cz"])
		if transports["icq.netlab.cz"]:
			self.addService(self.tr("ICQ"),"icq.netlab.cz",self.tr("<b>ICQ</b><br/>ICQ transport allows you to chat with your friends who use ICQ."),transports["icq.netlab.cz"])
		elif transports["icq.jabbim.cz"]:
			self.addService(self.tr("ICQ"),"icq.jabbim.cz",self.tr("<b>ICQ</b><br/>ICQ transport allows you to chat with your friends who use ICQ."),transports["icq.jabbim.cz"])
		else:
			self.addService(self.tr("ICQ"),"icq.jabber.cz",self.tr("<b>ICQ</b><br/>ICQ transport allows you to chat with your friends who use ICQ."),transports["icq.jabber.cz"])
		#self.addService(self.tr("Weather"),"weather.jabbim.cz",self.tr("<b>Weather</b><br/>Weather service allows you to see actual weather in big cities.<br/>"),transports["weather.netlab.cz"])
		self.ui.treeWidget.resizeColumnToContents(0)
		self.ui.treeWidget.setMaximumWidth(180)
		self.ui.treeWidget.setMinimumWidth(180)
		self.ui.treeWidget.sortItems(2,QtCore.Qt.AscendingOrder)
	
	def addService(self,name,jid,description,registered=False):
		item=QtGui.QTreeWidgetItem(self.ui.treeWidget)
		item.setText(1,name)
		item.setIcon(1,self.main().getIcon("1@"+jid,status="online",size="16x16"))
		item.setData(0,32,QtCore.QVariant(unicode(jid)))
		item.setData(1,32,QtCore.QVariant(unicode(description)))
		if registered:
			item.setIcon(0,QtGui.QIcon("images/16x16/actions/ok.png"))
			item.setText(2,"0"+unicode(jid))
		else:
			item.setIcon(0,QtGui.QIcon())
			item.setText(2,"1"+unicode(jid))
		
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

	def removeServiceContacts(self,jid):
		self.main().client.delContact(jid)
		j = self.main().getJid(jid)
		for jd in self.main().client.roster['users'].iterkeys():
			if jd.find(j.host) != -1:
				self.main().client.delContact(jd)

	def unregisterJabberDisk(self):
		if self.main().client.roster['users'].has_key("public@disk.jabbim.cz"):
			self.main().client.delContact("public@disk.jabbim.cz")
		if self.main().client.roster['users'].has_key("private@disk.jabbim.cz"):
			self.main().client.delContact("private@disk.jabbim.cz")
		if self.main().client.roster['users'].has_key("album@disk.jabbim.cz"):
			self.main().client.delContact("album@disk.jabbim.cz")
		#self.main().client.reactor.callLater(1,self.loadServices)
	
	def registerJabberDisk(self,data=None):
		if not data:
			d=self.main().client.getRegisterForm("disk.jabbim.cz")
			d.addCallback(self.registerJabberDisk)
		else:
			self.main().autoAdd['public@disk.jabbim.cz']={"name":self.tr("Public"),"group":"Disk"}
			self.main().autoAdd['private@disk.jabbim.cz']={"name":self.tr("Private"),"group":"Disk"}
			self.main().autoAdd['album@disk.jabbim.cz']={"name":self.tr("Album"),"group":"Disk"}
			self.main().client.setRegisterForm("disk.jabbim.cz",legacy={})
			#self.main().client.reactor.callLater(2,self.loadServices)
