import os
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from mucbrowser_ui import *
import pyxl

class MUCBrowserDialog(QtGui.QDialog):
	def __init__(self,main,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(False)
		self.ui=Ui_MUCBrowser()
		self.ui.setupUi(self)
		self.main=main
		self.ui.nickname.setText(main.client.jid.user)
		QtCore.QObject.connect(self.ui.groupchats, QtCore.SIGNAL("currentItemChanged ( QTreeWidgetItem * , QTreeWidgetItem * )"),self.selectionChanged)
		QtCore.QObject.connect(self.ui.groupchats, QtCore.SIGNAL("itemClicked ( QTreeWidgetItem *, int )"),self.CE)
		QtCore.QObject.connect(self.ui.showJid, QtCore.SIGNAL("stateChanged ( int )"),self.showJid)
		QtCore.QObject.connect(self.ui.lineEdit, QtCore.SIGNAL("textChanged ( const QString & )"),self.filterChanged)

		self.ui.groupchats.hideColumn(1)
		self.ui.groupchats.setColumnWidth(0,42)
		self.ui.groupchats.setSortingEnabled(True)
		self.ui.groupchats.hideColumn(3)
		if not self.main.client.bookmarksEnabled:
			self.ui.groupBox_3.setEnabled(False)

		mucjid = None
		for jid, node in self.main.client.disco.iteritems():
			if not node[None].has_key('identities'):
				continue
			for id in node[None]['identities'].itervalues():
				print jid, id
				if id.get('category') == 'conference' and id.get('type') == 'text' and jid.startswith('c'):
					mucjid = jid
					break
		self.server=mucjid
		if mucjid:
			self.ui.server.setText(self.server)
			self.main.client.getDiscoItems(mucjid, callback = self._roomsReceived)
		self.ui.splitter.setSizes([500,150])

		self.ui.lineEdit.hide()
		self.ui.label_5.hide()

	def filterChanged(self,text):
		if len(text)<4 and len(text)!=0:
			return
		for i in range(self.ui.groupchats.topLevelItemCount()):
			item=self.ui.groupchats.topLevelItem(i)
			if len(text)==0:
				self.ui.groupchats.setItemHidden(item, False)
			else:
				if unicode(item.text(1)).find(unicode(text).lower())==-1:
					self.ui.groupchats.setItemHidden(item, True)
				#else:
					#self.ui.groupchats.setItemHidden(item, False)
				
	def showJid(self,b):
		if self.ui.showJid.isChecked():
			for i in range(self.ui.groupchats.topLevelItemCount()):
				item=self.ui.groupchats.topLevelItem(i)
				for x in range(item.childCount()):
					child=item.child(x)
					child.setText(1,unicode(child.text(2)))
					child.setIcon(1,child.icon(2))
					child.setText(2,"")
					child.setIcon(2,QtGui.QIcon())
			self.ui.groupchats.showColumn(1)
			self.ui.groupchats.resizeColumnToContents(1)
		else:
			self.ui.groupchats.hideColumn(1)
			for i in range(self.ui.groupchats.topLevelItemCount()):
				item=self.ui.groupchats.topLevelItem(i)
				for x in range(item.childCount()):
					child=item.child(x)
					child.setText(2,unicode(child.text(1)))
					child.setIcon(2,child.icon(1))
					child.setText(1,"")
					child.setIcon(1,QtGui.QIcon())
		self.ui.groupchats.setColumnWidth(0,42)
	
		#self.ui.groupchats.setColumnWidth(0,36)

	def CE(self,item,i):
		if item.isExpanded():
			self.ui.groupchats.collapseItem(item)
		else:
			self.ui.groupchats.expandItem(item)

	def selectionChanged(self,item,old):
		if item.parent()==None:
			room = item.data(0, 32).toString()
			self.main.client.getDiscoItems(room, callback = self._participantsReceived, callback_par = (room, item))
			r = room.split('@')[0]
			self.ui.room.setText(r)
			self.ui.name.setText(r)
	
	def _participantsReceived(self, par):
		item = par[1]
		for i in range(int(item.childCount())):
			item.takeChild(0)
		users="<b>Users:</b> "
		for usr in self.main.client.disco[unicode(par[0])][None]['items'].itervalues():
			users+=usr['name']+", "
			user=QtGui.QTreeWidgetItem(item)
			#user.setText(1, usr['name'])
			if self.ui.showJid.isChecked():
				user.setText(1, usr['name'])
				user.setIcon(1,self.main.getIcon(size="16x16"))
			else:
				user.setText(2, usr['name'])
				user.setIcon(2,self.main.getIcon(size="16x16"))

			#user.setIcon(1,self.main.getIcon(size="16x16"))

		item.setToolTip(0,users)
		#self.ui.groupchats.setItemExpanded(item,True)
		if self.ui.groupchats.sortColumn()==3:
			self.ui.groupchats.sortByColumn(3,QtCore.Qt.DescendingOrder)
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
		self.rooms = []
		self.ui.groupchats.clear()
		for room in self.main.client.disco[self.server][None]['items'].itervalues():
			self.rooms.append((room['name'], room['jid'], self.getNum(room['name'])))

		self.rooms.sort(self.sortRooms)
		for room in self.rooms:
			item = QtGui.QTreeWidgetItem(0)
			item.setText(1,room[1])
			item.setText(2,room[0])
			item.setText(3,(int(room[2])+1)*'a')
			item.setData(0, 32, QtCore.QVariant(room[1]))
			item.setIcon(0,QtGui.QIcon("images/16x16/categories/muc.png"))
			#item.setIcon(1,QtGui.QIcon("images/16x16/categories/muc.png"))
			self.ui.groupchats.insertTopLevelItem(0, item)
		self.ui.groupchats.sortByColumn(3,QtCore.Qt.DescendingOrder)
	def accept(self):
		room=unicode(self.ui.room.text())
		server=unicode(self.ui.server.text())
		name=unicode(self.ui.name.text())
		nickname=unicode(self.ui.nickname.text())
		password=unicode(self.ui.password.text())

		if not name:
			name = room
			if self.main.client.bookmarksEnabled:
				for bkey in self.main.client.bookmarks['conference'].keys():
					if self.main.client.bookmarks['conference'][bkey].jid.userhost() == "%s@%s" % (room, server):
						name = self.main.client.bookmarks['conference'][bkey].name
		if self.main.client.bookmarksEnabled:
			if self.ui.bookmark.isChecked() and not self.main.client.bookmarks['conference'].has_key(name):
				self.main.client.bookmarks['conference'][name]=pyxl.client.Bookmark(name, 'conference', room+"@"+server, 'false', nickname, password)
				self.main.client.setBookmarks()
				self.main.buildBookmarks()

		#print "joining",room,nickname
		if self.main.chat.addGroupChatTab(room+"@"+server,nickname):
			self.main.client.joinGC(room+"@"+server, nickname)
		self.done(1)
