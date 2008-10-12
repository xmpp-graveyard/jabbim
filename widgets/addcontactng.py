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
			self.jid="test1.pyco.cz"
		else:
			# TODO - get user search jid from disco
			self.jid=""
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
		QtCore.QObject.connect(self.ui.search,QtCore.SIGNAL("clicked()"),self.search)
		QtCore.QObject.connect(self.ui.add,QtCore.SIGNAL("clicked()"),self.add)
		self.group=QtGui.QButtonGroup(self)
		QtCore.QObject.connect(self.group,QtCore.SIGNAL("buttonClicked ( QAbstractButton * )"),self.buttonClicked)
		QtCore.QObject.connect(self.ui.lineEdit,QtCore.SIGNAL("textEdited ( const QString & )"),self.textChanged)

		self.ui.treeWidget.setDragEnabled(True)
		self.ui.treeWidget.startDrag=self.startDrag
		self.ui.empty.hide()
		self.ui.add.hide()

#def getTransportForm(self, jid): 
#def getTransportJid(self, jid, prompt):

	def add(self):
		jid=unicode(self.ui.lineEdit.text())
   		dialog=addcontact.addContactDialog(self.main(),self,jid=jid,group="",name=jid.split('@')[0])
		if dialog.exec_()==1:
			self.done(1)

	def textChanged(self,text):
		t=unicode(text)
		if self.main().getJid(t) and t.find("@")!=-1:
			self.ui.add.show()
		else:
			self.ui.add.hide()

	def startDrag(self,actions):
		# start dragging selected contact
		item=self.ui.treeWidget.currentItem()
		jid=unicode(item.text(self.ui.treeWidget.jidIndex))
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
							if not self.ui.treeWidget.jidIndex:
								self.ui.treeWidget.jidIndex=fields[field['var']]['index']
		# set all columns' visibility before resizing any of them
		for f in fields.itervalues():
			self.ui.treeWidget.setColumnHidden(f['index'], f['empty'])
		for f in fields.itervalues():
			if not f['empty']:
				self.ui.treeWidget.resizeColumnToContents(f['index'])
		self.ui.treeWidget.setColumnWidth (0,18)
		self.ui.treeWidget.header().show()
		self.ui.treeWidget.show()


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
			jid=unicode(item.text(self.ui.treeWidget.jidIndex))
   			dialog=addcontact.addContactDialog(self.main(),self,jid=jid,group="",name=jid.split('@')[0])
			if dialog.exec_()==1:
				self.done(1)
