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
from joingroupchat_ui import *

class joinGroupChatWindow(QtGui.QDialog):
	def __init__(self,main,room="",server="",parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		self.ui=Ui_joingroupchat()
		self.ui.setupUi(self)
		self.main=main
		self.ui.room.setText(room)
		self.ui.server.setText(server)

	def accept(self):
		room=unicode(self.ui.room.text())
		server=unicode(self.ui.server.text())
		name=unicode(self.ui.name.text())
		nickname=unicode(self.ui.nickname.text())
		password=unicode(self.ui.password.text())
		#if self.ui.bookmark.isChecked() and not self.main.bookmarks.has_key(room):
			#print "setting bookmark for",room+"@"+server
			#self.main.bookmarks[room+"@"+server]={"name":name,"nick":nickname,"autojoin":"0","password":password}
			#self.jab.setBookmarks(self.main.bookmarks)
			#self.main.buildGroupchatMenu()
		#print "joining",room,nickname
		self.main.chat.addGroupChatTab(room+"@"+server,nickname)
		#self.main.groupchat[room+"@"+server]=[nickname,[]]
		self.main.client.joinGC(room+"@"+server, nickname)
		self.done(1)

	def reject(self):
		self.close()
