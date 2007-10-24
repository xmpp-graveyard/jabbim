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
class groupchatAdminDialog(QtGui.QDialog):
	def __init__(self,main,jid,form,affiliation,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(False)
		self.ui=Ui_groupchatAdmin()
		self.ui.setupUi(self)
		self.main=main
		self.jid=jid
		self.form=form
		self.affiliation=affiliation
		layout=QtGui.QGridLayout(self.ui.config)
		self.var,row=dataforms.makeDataForm(self.ui.config,layout,self.form)
		
		layout2=QtGui.QGridLayout(self.ui.affiliation)
		self.scroll=QtGui.QScrollArea(self.ui.affiliation)
		layout2.addWidget(self.scroll,0,0)
		
		widget=QtGui.QWidget()
		layout3=QtGui.QGridLayout(widget)
		
		self.members=QtGui.QListWidget(widget)
		layout3.addWidget(self.members,1,0,1,1)
		
		self.scroll.setWidget(widget)
		
		
	def accept(self):
		dataforms.sendDataForm(self.main,self.jid,self.form,self.var,"muc")
		self.done(1)

	def reject(self):
		self.close()