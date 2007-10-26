import os
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from servicediscovery_ui import *
import dataforms
import legacyforms
from search import *

class serviceDiscoveryDialog(QtGui.QDialog):
	def __init__(self,main,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(False)
		self.ui=Ui_serviceDiscovery()
		self.ui.setupUi(self)
		self.main=main
		
		#for category in self.getCategories():
		self.ui.tree.header().hide()

		QtCore.QObject.connect(self.ui.tree, QtCore.SIGNAL("itemExpanded ( QTreeWidgetItem * )"),self.expanded)
		QtCore.QObject.connect(self.ui.tree, QtCore.SIGNAL("itemCollapsed ( QTreeWidgetItem * )"),self.collapsed)
		QtCore.QObject.connect(self.ui.tree, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.itemClicked)
		QtCore.QObject.connect(self.ui.tree, QtCore.SIGNAL("itemClicked ( QTreeWidgetItem *, int)"),self.itemSelected)
		QtCore.QObject.connect(self.ui.register, QtCore.SIGNAL("clicked()"),self.register)
		QtCore.QObject.connect(self.ui.search, QtCore.SIGNAL("clicked()"),self.search)
		self.group=QtGui.QButtonGroup(self)
		QtCore.QObject.connect(self.group,QtCore.SIGNAL("buttonClicked ( QAbstractButton * )"),self.buttonClicked)

#d=self.main.client.getRegisterForm(jid)
		self.load()


		#for key in self.main.client.disco.keys():
			#if self.main.client.disco[key][None].has_key("identities"):
				#item=QtGui.QTreeWidgetItem(self.ui.tree)
				#for identity,values in self.main.client.disco[key][None]["identities"].iteritems():
					#if 
				
			#elif self.main.client.disco[key][None].has_key("err"):
				#print key,"error"

	def buttonClicked(self,b):
		if b.typ=="register":
			d=self.main.client.getRegisterForm(unicode(b.jid))
			d.addCallback(self._onRegister)
		elif b.typ=="search":
			d=self.main.client.getSearchForm(b.jid)
			d.addCallback(self._gotSearchForm)

	def register(self):
		jid=unicode(self.ui.tree.currentItem().text(3))
		d=self.main.client.getRegisterForm(jid)
		d.addCallback(self._onRegister)

	def search(self):
		jid=unicode(self.ui.tree.currentItem().text(3))
		d=self.main.client.getSearchForm(jid)
		d.addCallback(self._gotSearchForm)

	def _gotSearchForm(self,data):
		if not data:
			return
		jid,legacy,form=data
		if form!=None:
			self.dialog=searchDialog(self.main,jid,form,self)
			self.dialog.show()

	def _onRegister(self,data):
		if not data:
			return
		jid,legacy,form=data
		if form!=None:
			self.dialog=dataforms.dataFormsDialog(self.main,form,jid,"register",self)
			self.dialog.show()
		else:
			self.dialog=legacyforms.legacyFormsDialog(self.main,legacy,jid,"disco",self)
			self.dialog.show()

	def expanded(self,item):
		self.ui.tree.resizeColumnToContents(0)
		#self.ui.tree.resizeColumnToContents(1)
		#self.ui.tree.resizeColumnToContents(2)

	def collapsed(self,item):
		self.ui.tree.resizeColumnToContents(0)
		#self.ui.tree.resizeColumnToContents(1)
		#self.ui.tree.resizeColumnToContents(2)

	def itemClicked(self,item,i):
		jid=unicode(item.text(3))
		if len(jid)==0:
			return
		self.main.client.getDiscoItems(jid, callback = self._discoItemsReceived, callback_par = (item))

	def hasFeature(self,item,feature):
		for data in item.data(32,0).toList():
			if unicode(data.toString())==feature:
				return True
		return False

	def itemSelected(self,item,i):
		self.ui.register.setEnabled(self.hasFeature(item,"jabber:iq:register"))
		self.ui.search.setEnabled(self.hasFeature(item,"jabber:iq:search"))

	def _discoItemsReceived(self,item):
		jid=unicode(item.text(3))
		for key,values in self.main.client.disco[jid][None]['items'].iteritems():
			it=QtGui.QTreeWidgetItem(item)
			it.setText(3,values['jid'])
			if values.has_key("name"):
				it.setText(0,values["name"])
			else:
				it.setText(0,key)
			it.setIcon(0,item.icon(0))
		self.ui.tree.sortItems(0,QtCore.Qt.AscendingOrder)
		item.setExpanded(True)
		
		self.ui.tree.resizeColumnToContents(0)

	def load(self):
		categories={}
		for key in self.main.client.disco.keys():
			
			if self.main.client.disco[key][None].has_key("identities"):
				for identity,values in self.main.client.disco[key][None]["identities"].iteritems():
					if values.has_key('category'):
						if not values['category'] in categories.keys():
							item=QtGui.QTreeWidgetItem(self.ui.tree)
							item.setText(0,values['category']) # todo => lepsi nazvy
							item.setIcon(0,QtGui.QIcon("images/48x48/apps/jabbim.png"))
							categories[values['category']]=item
						if values.has_key('name'):
							parentitem=QtGui.QTreeWidgetItem(categories[values['category']])
							parentitem.setText(0,values['name'])
							if values.has_key("type"):
								typ=values['type']
								if typ=="pep" or typ=="im":
									typ="jabber"
								elif typ=="file":
									typ="disk"
								parentitem.setIcon(0,self.main.getIcon(size="16x16",usertype=typ))
								parentitem.setText(3,key)
				if self.main.client.disco[key][None].has_key("features"):
					parentitem.setData(32,0,QtCore.QVariant(list(self.main.client.disco[key][None]['features'])))

					if "jabber:iq:register" in list(self.main.client.disco[key][None]['features']):
						register=QtGui.QPushButton(self.ui.tree)
						#register.setMaximumWidth(40)
						#register.setMinimumWidth(40)
						register.setIcon(QtGui.QIcon("images/16x16/actions/register.png"))
						#register.setEnabled(False)
						register.setFlat(True)
						register.jid=parentitem.text(3)
						register.typ="register"
						self.group.addButton(register)
						self.ui.tree.setItemWidget(parentitem,2,register)
					elif "jabber:iq:search" in list(self.main.client.disco[key][None]['features']):
					
						search=QtGui.QPushButton(self.ui.tree)
						#search.setMaximumWidth(16)
						#search.setMinimumWidth(16)
						search.setIcon(QtGui.QIcon("images/16x16/actions/search.png"))
						#search.setEnabled(False)
						search.setFlat(True)
						search.jid=parentitem.text(3)
						search.typ="search"
						self.group.addButton(search)
						self.ui.tree.setItemWidget(parentitem,1,search)

				if self.main.client.disco[key][None].has_key("items"):
					for item,values in self.main.client.disco[key][None]['items'].iteritems():
						it=QtGui.QTreeWidgetItem(parentitem)
						it.setText(0,item)
						it.setIcon(0,parentitem.icon(0))
						if values.has_key("jid"):
							it.setText(3,values['jid'])
				
				#item=self.main.ui.bookmarks.findItems(jid,QtCore.Qt.MatchExactly,1)[0]
			elif self.main.client.disco[key][None].has_key("err"):
				print key,"error"
			print self.main.client.disco[key]
		print categories.keys()
		self.ui.tree.sortItems(0,QtCore.Qt.AscendingOrder)
		self.ui.tree.resizeColumnToContents(0)
		self.ui.tree.setColumnWidth (1,20)
		self.ui.tree.setColumnWidth (2,20)
		return categories

	def accept(self):
		self.done(1)

