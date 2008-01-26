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
from extra_ui import *

from twisted.python import log
import base64
class extraDialog(QtGui.QDialog):
	"""
	Jabbim Extra Dialog
	"""
	def __init__(self,typ,main,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		self.ui=Ui_Extra()
		self.ui.setupUi(self)
		self.main=main
		if typ=="emoticons":
			self.ui.label.setText("<h3>"+self.tr("Emoticons")+"</h3>")
			self.main.client.callRemote('rpc@jabbim.cz/service', 'getList', ('smileys/',)).addCallback(self._emoticonsListArrived)#.addErrback(self._emoticonsListError)
			QtCore.QObject.connect(self.ui.listWidget,QtCore.SIGNAL("currentItemChanged( QListWidgetItem *, QListWidgetItem *)"),self.selectionChanged)
		self.ui.preview.hide()
	def selectionChanged(self,item,old):
		if item:
			name=unicode(item.text())
			self.main.client.callRemote('rpc@jabbim.cz/service', 'getInfo', ('smileys/'+name,)).addCallback(self._emoticonArrived)
	
	def _emoticonArrived(self,data):
		data=data[0][0]
		self.ui.textBrowser.setPlainText(data[1])
		pixmap=QtGui.QPixmap()
		image=base64.decodestring(str(data[2]))
		pixmap.loadFromData(image)
		self.ui.preview.show()
		self.ui.preview.setPixmap(pixmap)
		#print unicode(data)
	
	def _emoticonsListArrived(self,data):
		#(({'white': 'Tohle je kratky popis, vlastne nic duleziteho .. \n', 'black': 'Tohle je kratky popis, vlastne nic duleziteho .. \n'},), None)
		emoticons=data[0][0]
		for name,desc in emoticons.iteritems():
			item=QtGui.QListWidgetItem(unicode(name),self.ui.listWidget)
			item.setToolTip(unicode(desc))

	def _emoticonsListError(self,data):
		print data


	def accept(self):
		self.done(1)

	def reject(self):
		self.close()
