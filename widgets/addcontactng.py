# -*- coding: utf-8 -*- 

import os
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from addcontactng_ui import *
from search import *
import pyxl
import weakref
import vcardeditor
import addcontact
import dataforms,legacyforms
import wizards

class tabBar(QtGui.QTabBar):
	def __init__(self,parent=None):
		QtGui.QTabBar.__init__(self,parent)

class addContactDialog(QtGui.QDialog):
	def __init__(self,main,parent=None,jid=""):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(False)
		self.ui=Ui_addContact()
		self.ui.setupUi(self)
		self.main=weakref.ref(main)
		if self.main().client.jid.host in ['jabbim.cz','jabber.cz','njs.netlab.cz','jabbim.com','jabbim.pl']:
			self.jabbimUser=True
			self.jid="test1.pyco.cz"
		else:
			self.jabbimUser=False
			# TODO - get user search jid from disco
			self.jid=""
		self.addFunction=None
		self.ui.description.hide()
		self.ui.service.insertSeparator(0)
		srv = unicode(self.main().client.jid.host)
		if srv in self.main().client.disco.keys():
			print self.main().client.disco[srv]
			if self.main().client.disco[srv][None].has_key("identities"):
				if self.main().client.disco[srv][None].has_key("items"):
					for item,d in self.main().client.disco[srv][None]['items'].iteritems():
						key=d['jid']
						if key in self.main().client.disco.keys():
							if self.main().client.disco[key][None].has_key("identities"):
								for identity,values in self.main().client.disco[key][None]["identities"].iteritems():
									if values.has_key('category'):
										if values.has_key('name'):
											#[u'conference', u'service', u'headline', u'component', u'server', u'services', u'proxy', u'directory', u'gateway', u'store', u'pubsub']
											if values['category'] in ['service','headline','services','store','directory','component','gateway']:
												if values.has_key("type"):
													typ=values['type']
													if typ=="pep" or typ=="im":
														typ="jabber"
													elif typ=="file":
														typ="disk"
													registered=False
													for jd in self.main().client.roster['users'].keys():
														if jd.find(key)!=-1:
															registered=True
															break
													if registered:
														self.ui.service.insertItem(0,self.main().getIcon(size="16x16",usertype=typ),values['name'],QtCore.QVariant(unicode(key)))
													else:
														self.ui.service.addItem(self.main().getIcon(size="16x16",usertype=typ),values['name'],QtCore.QVariant(unicode(key)))
			elif self.main().client.disco[key][None].has_key("err"):
				print key,"error"
		self.ui.service.insertItem(0,self.main().getIcon(size="16x16",usertype="jabber"),"Jabber",QtCore.QVariant(unicode(self.main().client.jid.host)))
		self.ui.service.setCurrentIndex(0)


##		self.tabBar=tabBar(self.ui._tabBar)
##		self.tabBar.addTab(self.tr("Jabber ID"))
##		self.tabBar.addTab(self.tr("Name"))
##		l=QtGui.QHBoxLayout(self.ui._tabBar)
##		l.addWidget(self.tabBar)
		self.ui._tabBar.hide()
		self.form=None
		d=self.main().client.getSearchForm(self.jid)
		d.addCallback(self._gotSearchForm)
		self.ui.treeWidget.hide()
		self.ui.addToRoster.hide()
		QtCore.QObject.connect(self.ui.search,QtCore.SIGNAL("clicked()"),self.search)
		QtCore.QObject.connect(self.ui.add,QtCore.SIGNAL("clicked()"),self.add)
		self.group=QtGui.QButtonGroup(self)
		QtCore.QObject.connect(self.group,QtCore.SIGNAL("buttonClicked ( QAbstractButton * )"),self.buttonClicked)
		QtCore.QObject.connect(self.ui.lineEdit,QtCore.SIGNAL("textEdited ( const QString & )"),self.textChanged)

		QtCore.QObject.connect(self.ui.service,QtCore.SIGNAL("currentIndexChanged ( int )"),self.serviceChanged)

		self.ui.treeWidget.setDragEnabled(True)
		self.ui.treeWidget.startDrag=self.startDrag
		self.ui.empty.hide()
		self.ui.add.hide()
		self.gateway=False
		self.ui.picture.setPixmap(QtGui.QPixmap("images/lupa-smile.png"))
		self.ui.picture.setAlignment(QtCore.Qt.AlignCenter)
		self.ui.picture.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)

#def getTransportForm(self, jid): 
#def getTransportJid(self, jid, prompt):
	
	def isServiceRegistered(self,key):
		for jd in self.main().client.roster['users'].keys():
			if jd.find(key)!=-1:
				return True
		return False

	def serviceChanged(self,index):
		if index==0:
			self.gateway=False
			self.addFunction=None
			self.ui.add.hide()
			self.ui.search.show()
			self.ui.searchLabel.setText(self.tr("User:"))
			self.ui.description.setText(self.tr("Enter informations about contact or whole Jabber ID."))
			self.ui.description.show()
			self.ui.treeWidget.hide()
			self.ui.picture.show()
			self.ui.lineEdit.show()
			return
		jid=unicode(self.ui.service.itemData(index).toString())
		print jid
		print list(self.main().client.disco[jid][None]['features'])
		self.ui.lineEdit.show()
		self.ui.search.show()
		if not self.isServiceRegistered(jid):
			if jid=="icq.jabber.cz":
				self.addFunction=None
				self.discovery2=wizards.jabbimservicemanager.jabbimServiceManager(self.main(),self.main())
				self.discovery2.registerICQ()
				self.discovery2.show()
			elif jid=="weather.netlab.cz":
				self.ui.picture.hide()
				self.ui.search.hide()
				self.ui.add.hide()
				self.ui.description.hide()
				self.ui.lineEdit.hide()
				self.ui.searchLabel.hide()
				self.showWeather()
				self.addFunction=self._addWeather
			elif jid=="dict.jabbim.cz":
				self.ui.picture.hide()
				self.ui.search.hide()
				self.ui.add.hide()
				self.ui.description.hide()
				self.ui.lineEdit.hide()
				self.ui.searchLabel.hide()
				self.showDict()
				self.addFunction=self._addDict
			else:
				self.ui.picture.show()
				self.addFunction=None
				self._nowAskingFor=jid
				d=self.main().client.getRegisterForm(jid)
				d.addCallback(self._onRegister)
				self.ui.treeWidget.hide()
		else:
			#if "jabber:iq:gateway" in list(self.main().client.disco[jid][None]['features']):
			if jid=="weather.netlab.cz":
				self.ui.picture.hide()
				self.ui.search.hide()
				self.ui.add.hide()
				self.ui.description.hide()
				self.ui.lineEdit.hide()
				self.ui.searchLabel.hide()
				self.showWeather()
				self.addFunction=self._addWeather
			elif jid=="dict.jabbim.cz":
				self.ui.picture.hide()
				self.ui.search.hide()
				self.ui.add.hide()
				self.ui.description.hide()
				self.ui.lineEdit.hide()
				self.ui.searchLabel.hide()
				self.showDict()
				self.addFunction=self._addDict
			else:
				self.addFunction=None
				self.ui.picture.show()
				d=self.main().client.getTransportForm(jid)
				self._nowAskingFor=jid
				d.addCallback(self._transportForm,jid)
				d.addErrback(self._transportFormError,jid)
				self.ui.treeWidget.hide()

	def showDict(self):
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

		self.ui.treeWidget.clear()
		for jid,name in d.iteritems():
			item=QtGui.QTreeWidgetItem(self.ui.treeWidget)
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

		for i in range(self.ui.treeWidget.columnCount())[1:]:
			self.ui.treeWidget.setColumnHidden(i,True)

		self.ui.treeWidget.sortItems(0,QtCore.Qt.AscendingOrder)
		self.ui.treeWidget.resizeColumnToContents(0)
		self.ui.treeWidget.show()
		self.ui.addToRoster.show()

	def _addDict(self):
		for i in range(0,int(self.ui.treeWidget.topLevelItemCount())):
			item=self.ui.treeWidget.topLevelItem(i)
			if item.checkState(0)!=item.registered:
				item.registered=not item.registered
				if item.checkState(0)==QtCore.Qt.Checked:
					self.main().autoAdd[unicode(item.jid)]={}
					self.main().client.addContact(unicode(item.jid),"",unicode(item.text(0)),[unicode(self.tr("Dictionaries"))])
				else:
					self.main().client.delContact(unicode(item.jid))

	def _addWeather(self):
		for i in range(0,int(self.ui.treeWidget.topLevelItemCount())):
			item=self.ui.treeWidget.topLevelItem(i)
			if item.checkState(0)!=item.registered:
				item.registered=not item.registered
				if item.checkState(0)==QtCore.Qt.Checked:
					self.main().autoAdd[unicode(item.jid)]={}
					self.main().client.addContact(unicode(item.jid),"",unicode(item.text(0)),[unicode(self.tr("Weather"))])
				else:
					self.main().client.delContact(unicode(item.jid))

	def _transportForm(self,data,jid):
		self.ui.description.setText(unicode(data['desc']))
		self.ui.searchLabel.setText(unicode(data['prompt']))
		self.ui.search.hide()
		self.ui.add.show()
		self.ui.description.show()
		self.gateway=True
	
	def _transportFormError(self,data,jid):
		if _nowAskingFor==jid:
			self.ui.searchLabel.setText(self.tr("User:"))
			self.ui.search.show()
			self.gateway=False
			self.ui.description.hide()

	def showWeather(self):
		l=unicode(QtCore.QLocale.system().name())[:2]
		if l=="cs":
			jids={'beroun@weather.netlab.cz':"Opava",
			'brno@weather.netlab.cz':u'Brno',
			'cesky_tesin@weather.netlab.cz':u'Český Těšín',
			'frydek@weather.netlab.cz':u'Frýdek Místek',
			'karvina@weather.netlab.cz':u'Karviná',
			'kladno@weather.netlab.cz':u'Kladno',
			'kolin@weather.netlab.cz':u'Kolín',
			'opava@weather.netlab.cz':u'Opava',
			'ostrava@weather.netlab.cz':u'Ostrava',
			'pilsen@weather.netlab.cz':u'Plzeň',
			'pisek@weather.netlab.cz':u'Písek',
			'prague@weather.netlab.cz':u'Praha',
			'rosice@weather.netlab.cz':u'Rošice',
			'slavkov_u_brna@weather.netlab.cz':u'Slavkov u Brna',
			'tabor@weather.netlab.cz':u'Tábor',
			'usti_nad_labem@weather.netlab.cz':u'Ústí nad Labem',
			'cheb@weather.netlab.cz':u'Cheb',
			'primda@weather.netlab.cz':u'Přimda',
			'churanov@weather.netlab.cz':u'Churáňov',
			'milesovka@weather.netlab.cz':u'Milešovka',
			'kocelovice@weather.netlab.cz':u'Kocelovice',
			'praha@weather.netlab.cz':u'Praha',
			'liberec@weather.netlab.cz':u'Liberec',
			'kostelni_myslova@weather.netlab.cz':u'Kostelní Myslová',
			'pribyslav@weather.netlab.cz':u'Přibyslav',
			'usti_nad_orlici@weather.netlab.cz':u'Ústí nad Labem',
			'cervena@weather.netlab.cz':u'Červená',
			'holesov@weather.netlab.cz':u'Holešov',
			'lysa_hora@weather.netlab.cz':u'Lysá Hora',
			'ceskebudejovice@weather.netlab.cz':u'České Budějovice'}
			self.ui.treeWidget.clear()
			self.ui.treeWidget.headerItem().setText(0,self.tr("Locality"))
			for jid,name in jids.iteritems():
				item=QtGui.QTreeWidgetItem(self.ui.treeWidget)
				item.setText(0,unicode(name))
				item.jid=unicode(jid)
				registered=self.main().client.roster['users'].has_key(jid)
				if registered:
					item.registered=QtCore.Qt.Checked
					item.setCheckState(0,QtCore.Qt.Checked)
				else:
					item.setCheckState(0,QtCore.Qt.Unchecked)
					item.registered=QtCore.Qt.Unchecked
			for i in range(self.ui.treeWidget.columnCount())[1:]:
				self.ui.treeWidget.setColumnHidden(i,True)
			self.ui.treeWidget.sortItems(0,QtCore.Qt.AscendingOrder)
			self.ui.treeWidget.resizeColumnToContents(0)
			self.ui.treeWidget.show()
			self.ui.addToRoster.show()

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

	def add(self,data=None):
		if self.gateway:
			if data:
				jid=unicode(data)
			else:
				d=self.main().client.getTransportJid(unicode(self.ui.service.itemData(self.ui.service.currentIndex()).toString()),unicode(self.ui.lineEdit.text()))
				d.addCallback(self._add)
				return
		else:
			jid=unicode(self.ui.lineEdit.text())
		if not self.addFunction:
			dialog=addcontact.addContactDialog(self.main(),self,jid=jid,group="",name=jid.split('@')[0])
			if dialog.exec_()==1:
				self.done(1)
		else:
			self.addFunction()

	def _add(self,data=None):
		self.main().reactor.callLater(0,self.add,data)

	def textChanged(self,text):
		if self.ui.service.currentIndex()==0:
			t=unicode(text)
			if self.main().getJid(t) and t.find("@")!=-1:
				self.ui.add.show()
			else:
				self.ui.add.hide()

	def startDrag(self,actions):
		# start dragging selected contact
		item=self.ui.treeWidget.currentItem()
		jid=unicode(item.jid)
		self.ui.treeWidget.drag=QtGui.QDrag(self.ui.treeWidget)
		mimeData=QtCore.QMimeData()
		mimeData.setText(jid)
		self.ui.treeWidget.drag.setMimeData(mimeData)
		self.ui.treeWidget.action=self.ui.treeWidget.drag.start(QtCore.Qt.CopyAction)

	def buttonClicked(self,b):
		if b.jid:
			self.ve=vcardeditor.vcardEditorDialog(self.main(),b.jid,self,False)
			self.ve.show()


	def search(self):
		self.ui.treeWidget.jidIndex=None
		print "search"
		form=self.form
		for x in form.elements():
			if unicode(x.name)=="field":
				if x.hasAttribute("var"):
					if x['var']=="fulltext":
						for child in x.elements():
							if child.name == 'value':
								make=False
								child.children = []
								child.children.append(unicode(self.ui.lineEdit.text()))
						if make:
							x.addElement('value', content = unicode(self.ui.lineEdit.text()))
					elif x['var']=="engine":
						make=True
						selected=["jabbim"]
						#for item in widget.selectedItems():
						#	selected.append(unicode(item.data(32).toString()))

						for child in x.elements():
							if child.name == 'value':
								make=False
								child.children = []
								if len(selected)!=0:
									child.children.append(selected[0])
									selected.remove(selected[0])
						for text in selected:
							x.addElement('value', content = unicode(text))
		print "send"
		d=self.main().client.setSearchForm(self.jid,forms=form)
		d.addCallback(self._gotResults)

	def _gotResults(self,data):
		self.ui.picture.hide()
		self.ui.treeWidget.clear()
		fields={}
		jid,legacy,form=data
		if not form:
			self.ui.empty.show()
			return
		self.ui.empty.hide()
		self.ui.treeWidget.headerItem().setText(0,"")
		i=1
		for x in form.elements():
			if x.name=="reported":
				for field in x.elements():
					if field.name=="field":
						fields[field['var']] = { 'index': i, 'empty': True }
						self.ui.treeWidget.headerItem().setText(i,field['label'])
						i+=1
			elif x.name=="item":
				item=QtGui.QTreeWidgetItem(self.ui.treeWidget)

				register=QtGui.QPushButton(self.ui.treeWidget)
				register.setIcon(QtGui.QIcon("images/16x16/categories/v-card.png"))
				register.setIconSize(QtCore.QSize(16,16))
				register.setFlat(True)
				register.jid=None
				self.group.addButton(register)
				self.ui.treeWidget.setItemWidget(item,0,register)
				for field in x.elements():
					if field.name=="field":
						text=u""
						for y in field.elements():
							if y.name=="value":
								text=unicode(y).strip()
						item.setText(fields[field['var']]['index'], text)
						if len(text) > 0:
							fields[field['var']]['empty'] = False;
						if field['var']=='jid':
							register.jid=unicode(text)
							item.jid=unicode(text)
							#if not self.ui.treeWidget.jidIndex:
							#	self.ui.treeWidget.jidIndex=fields[field['var']]['index']
		# set all columns' visibility before resizing any of them
		for f in fields.itervalues():
			self.ui.treeWidget.setColumnHidden(f['index'], f['empty'])
		for f in fields.itervalues():
			if not f['empty']:
				self.ui.treeWidget.resizeColumnToContents(f['index'])
		self.ui.treeWidget.setColumnWidth (0,18)
		self.ui.treeWidget.header().show()
		self.ui.treeWidget.show()
		self.ui.addToRoster.show()


	def _gotSearchForm(self,data):
 		print "got search form"
		if not data:
			return
		jid,legacy,form=data
		if form!=None:
			self.form=form

	def accept(self):
		item=self.ui.treeWidget.currentItem()
		if item:
			jid=item.jid
		if not self.addFunction:
			dialog=addcontact.addContactDialog(self.main(),self,jid=jid,group="",name=jid.split('@')[0])
			if dialog.exec_()==1:
				self.done(1)
		else:
			self.addFunction()
