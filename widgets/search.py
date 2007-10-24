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
		layout=QtGui.QGridLayout(self)
		self.var,row=dataforms.makeDataForm(self,layout,self.form)
		
		self.ok=QtGui.QPushButton(self.tr("Search"),self)
		self.cancel=QtGui.QPushButton(self.tr("Cancel"),self)
		
		QtCore.QObject.connect(self.ok,QtCore.SIGNAL("clicked()"),self.search)
		QtCore.QObject.connect(self.cancel,QtCore.SIGNAL("clicked()"),self.reject)
		
		layout.addWidget(self.ok,row,0)
		layout.addWidget(self.cancel,row,1)

	def _gotResults(self,data):
		jid,legacy,form=data
		print unicode(form.toXml())

	def search(self):
		form=dataforms.sendDataForm(self.main,self.jid,self.form,self.var,"only get form")
		d=self.main.client.setSearchForm(self.jid,forms=form)
		d.addCallback(self._gotResults)
		

		#dataforms.sendDataForm(self.main,self.jid,self.form,self.var,"muc")
		#self.done(1)

	def reject(self):
		self.close()