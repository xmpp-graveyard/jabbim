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
import pyxl

from twisted.python import log

class dataFormsDialog(QtGui.QDialog):
	def __init__(self,main,form,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		print unicode(form.toXml())
		#child = form.firstChildElement()
		#print "ELEMENTS",unicode(child.toXml())
		#print "ELEMENTS",child.elements()
		layout=QtGui.QGridLayout(self)
		
		self.instructions=QtGui.QTextEdit(self)
		self.instructions.setReadOnly(True)
		layout.addWidget(self.instructions,0,0,1,2)
		self.setMaximumWidth(400);
		self.var={}
		row=1
		for x in form.elements():
			if unicode(x.name)=="title":
				self.setWindowTitle(unicode(x))
			elif unicode(x.name)=="instructions":
				self.instructions.setText(unicode(x))
			elif unicode(x.name)=="field":
				if x['type']=="text-single":
					label=QtGui.QLabel(x['label'],self)
					layout.addWidget(label,row,0)
					widget=QtGui.QLineEdit(self)
					for child in x.elements():
						if child.name == 'value':
							widget.setText(unicode(child))
					layout.addWidget(widget,row,1)
					self.var[x['var']]={'widget':widget,'type':x['type']}
					row+=1
				elif x['type']=="fixed":
					label=QtGui.QLabel(self)
					label.setWordWrap(True)
					for child in x.elements():
						if child.name == 'value':
							label.setText(unicode(child))
					layout.addWidget(label,row,0,1,2)
					row+=1
				elif x['type']=="text-multi":
					label=QtGui.QLabel(x['label'],self)
					layout.addWidget(label,row,0)
					widget=QtGui.QTextEdit(self)
					for child in x.elements():
						if child.name == 'value':
							widget.setText(unicode(child))
					layout.addWidget(widget,row,1)
					self.var[x['var']]={'widget':widget,'type':x['type']}
					row+=1

	def accept(self):
		self.done(1)

	def reject(self):
		self.close()