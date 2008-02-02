"""
Copyright (C) 2007 	Jan 'Hanzz' Kaluza (hanzz at njs.netlab.cz)
Copyright (C) 2007	Jiri 'Sef' Gabrys	(sef at njs.netlab.cz)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from groupchatadmin_ui import *
#import pyxl

from twisted.python import log
import dataforms
class searchDialog(QtGui.QDialog):
	def __init__(self,main,jid,form,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(False)
		self.main=main
		self.jid=jid
		self.form=form
		l=QtGui.QHBoxLayout(self)
		self.splitter = QtGui.QSplitter(self)
		self.splitter.setOrientation(QtCore.Qt.Horizontal)
		l.addWidget(self.splitter)
		widget=QtGui.QWidget(self.splitter)

		layout=QtGui.QGridLayout(widget)
		self.var,row=dataforms.makeDataForm(widget,layout,self.form)
		
		self.ok=QtGui.QPushButton(self.tr("Search"),widget)
		self.cancel=QtGui.QPushButton(self.tr("Cancel"),widget)
		
		QtCore.QObject.connect(self.ok,QtCore.SIGNAL("clicked()"),self.search)
		QtCore.QObject.connect(self.cancel,QtCore.SIGNAL("clicked()"),self.reject)

		self.table=QtGui.QTreeWidget(self.splitter)
		#layout.addWidget(self.table,1,2,row-1,1)
		self.table.header().hide()

		
		layout.addWidget(self.ok,row,0)
		layout.addWidget(self.cancel,row,1)

		self.splitter.setSizes([150,500])

	def _gotResults(self,data):
		self.table.clear()
		jid,legacy,form=data
		for i in range(int(self.table.columnCount())):
			self.table.headerItem().setText(i,"")
		#self.tree.headerItem().setText(3,QtGui.QApplication.translate("serviceDiscovery", "jid", None, QtGui.QApplication.UnicodeUTF8))
		#<x xmlns='jabber:x:data' type='result'><title>Search Results for users.netlab.cz</title><reported><field var='jid' label='Jabber ID'/><field var='fn' label='Full Name'/><field var='given' label='Name'/><field var='middle' label='Middle Name'/><field var='family' label='Family Name'/><field var='nickname' label='Nickname'/><field var='bday' label='Birthday'/><field var='ctry' label='Country'/><field var='locality' label='City'/><field var='email' label='Email'/><field var='orgname' label='Organization Name'/><field var='orgunit' label='Organization Unit'/></reported>
		#<item><field var='jid'><value>hanzz@jabbim.pl</value></field><field var='fn'><value/></field><field var='family'><value/></field><field var='given'><value/></field><field var='middle'><value/></field><field var='nickname'><value/></field><field var='bday'><value/></field><field var='ctry'><value/></field><field var='locality'><value/></field><field var='email'><value/></field><field var='orgname'><value/></field><field var='orgunit'><value/></field></item></x>
		fields=[]
		i=0
		for x in form.elements():
			if x.name=="reported":
				for field in x.elements():
					if field.name=="field":
						fields.append(field['var'])
						self.table.headerItem().setText(i,field['label'])
						i+=1
			elif x.name=="item":
				item=QtGui.QTreeWidgetItem(self.table)
				for field in x.elements():
					if field.name=="field":
						text=""
						for y in field.elements():
							if y.name=="value":
								text=unicode(y)
						item.setText(fields.index(field['var']),unicode(text))
		self.table.header().show()
		for i in range(int(self.table.columnCount())):
			self.table.resizeColumnToContents(i)

	def search(self):
		form=dataforms.sendDataForm(self.main,self.jid,self.form,self.var,"only get form")
		d=self.main.client.setSearchForm(self.jid,forms=form)
		d.addCallback(self._gotResults)
		

		#dataforms.sendDataForm(self.main,self.jid,self.form,self.var,"muc")
		#self.done(1)

	def reject(self):
		self.close()
