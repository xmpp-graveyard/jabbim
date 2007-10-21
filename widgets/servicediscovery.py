import os
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from servicediscovery_ui import *

class serviceDiscoveryDialog(QtGui.QDialog):
	def __init__(self,main,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		self.ui=Ui_serviceDiscovery()
		self.ui.setupUi(self)
		self.main=main
		
		#for category in self.getCategories():
		self.load()
		

		#for key in self.main.client.disco.keys():
			#if self.main.client.disco[key][None].has_key("identities"):
				#item=QtGui.QTreeWidgetItem(self.ui.tree)
				#for identity,values in self.main.client.disco[key][None]["identities"].iteritems():
					#if 
				
			#elif self.main.client.disco[key][None].has_key("err"):
				#print key,"error"

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
							item=QtGui.QTreeWidgetItem(categories[values['category']])
							item.setText(0,values['name'])
							if values.has_key("type"):
								typ=values['type']
								if typ=="pep" or typ=="im":
									typ="jabber"
								elif typ=="file":
									typ="disk"
								item.setIcon(0,self.main.getIcon(size="16x16",usertype=typ))
					print values
							
			elif self.main.client.disco[key][None].has_key("err"):
				print key,"error"
		print categories.keys()
		return categories

	def accept(self):
		self.done(1)
