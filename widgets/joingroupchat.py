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
import pyxl

from twisted.python import log

class joinGroupChatWindow(QtGui.QDialog):
	def __init__(self,main,room="",server="",parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		self.ui=Ui_joingroupchat()
		self.ui.setupUi(self)
		self.main=main
		self.ui.room.setText(room)
		self.ui.server.setText(server)
		self.ui.nickname.setText(main.client.jid.user)
		self.ui.roomList.setHeaderLabel(main.tr('Rooms'))
		self.ui.roomList.setSortingEnabled(False)
		self.server = server
		self.rooms = [] # [(roomname, roomjid, usercount), ]
		if self.server != '':
			self.main.client.getDiscoItems(server, callback = self._roomsReceived)
		
		QtCore.QObject.connect(self.ui.roomList,QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem *, int )"), self.roomSelected)
		QtCore.QObject.connect(self.ui.roomList,QtCore.SIGNAL("currentItemChanged ( QTreeWidgetItem * , QTreeWidgetItem * )"), self.roomChanged)
		QtCore.QObject.connect(self.ui.room,QtCore.SIGNAL("textChanged ( const QString & )"), self.textChanged)
	
	def textChanged(self, text):
		print 'pip'
		if unicode(text).strip() != '':
			self.ui.pushButton.setEnabled(True)
		else:
			self.ui.pushButton.setDisabled(True)
		
	def getNum(self, string):
		def reverse(s):
			s = list(s)
			s.reverse()
			return "".join(s)
		s = reverse(string)
		i1, i2 = s.find(")"), s.find("(")
		try:
			cislo = int(reverse(s[i1+1:i2]))
		except:
			cislo = 0
		return cislo

	def sortRooms(self, x, y):
		if x[2] > y[2]:
			return 1
		elif x[2] == y[2]:
			return 0
		elif x[2] < y[2]:
			return -1
	
	def _roomsReceived(self, res):
		log.msg( 'rooms received!')
		self.rooms = []
		self.ui.roomList.clear()
		for room in self.main.client.disco[self.server][None]['items'].itervalues():
			self.rooms.append((room['name'], room['jid'], self.getNum(room['name'])))

		self.rooms.sort(self.sortRooms)
		for room in self.rooms:
			item = QtGui.QTreeWidgetItem([room[0]], 0)
			item.setData(0, 32, QtCore.QVariant(room[1]))
			self.ui.roomList.insertTopLevelItem(0, item)

	def roomSelected(self, item, column):
		roomjid =  item.data(0, 32).toString()
		room = roomjid.split('@')[0]
		self.ui.room.setText(room)
		self.ui.name.setText(item.text(0))
	
	def roomChanged(self, item, lastitem):
		room = item.data(0, 32).toString()
		self.main.client.getDiscoItems(room, callback = self._participantsReceived, callback_par = (room, item))
	
	def _participantsReceived(self, par):
		item = par[1]
		for usr in self.main.client.disco[unicode(par[0])][None]['items'].itervalues():
			user=QtGui.QTreeWidgetItem(item)
			user.setText(0, usr['name'])
		self.ui.roomList.setItemExpanded(item,True)
		
	def accept(self):
		room=unicode(self.ui.room.text())
		server=unicode(self.ui.server.text())
		name=unicode(self.ui.name.text())
		nickname=unicode(self.ui.nickname.text())
		password=unicode(self.ui.password.text())
		if self.ui.bookmark.isChecked() and not self.main.client.bookmarks['conference'].has_key(name):
			self.main.client.bookmarks['conference'][name]=pyxl.client.Bookmark(name, 'conference', room+"@"+server, 'false', nickname, password)
			self.main.client.setBookmarks()
			self.main.buildBookmarks()

		#print "joining",room,nickname
		self.main.chat.addGroupChatTab(room+"@"+server,nickname)
		#self.main.groupchat[room+"@"+server]=[nickname,[]]
		self.main.client.joinGC(room+"@"+server, nickname)
		self.done(1)

	def reject(self):
		self.close()
