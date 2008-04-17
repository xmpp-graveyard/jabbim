import os
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from mucbrowser_ui import *
import pyxl

class delegate(QtGui.QItemDelegate):
	def __init__(self,parent=None):
		QtGui.QItemDelegate.__init__(self,parent)
	
	def paint(self,painter,option,index):
		# selected item
		if option.state & QtGui.QStyle.State_Selected and index.column()==2:
			#option.rect.setHeight(50)
			option.displayAlignment=QtCore.Qt.AlignTop
			text=unicode(index.data(32).toString())
			QtGui.QItemDelegate.paint(self,painter,option,index)
			#metrics=QtGui.QFontMetrics(option.font)
			painter.save()
			painter.setPen(option.palette.highlightedText().color())
			#print option.fontMetrics.height(),option.rect.y()
			#painter.drawText(option.rect.x()+QtGui.QApplication.style().pixelMetric(QtGui.QStyle.PM_FocusFrameHMargin) + 1,option.rect.y()+option.fontMetrics.height(),option.rect.width(),option.rect.height(),QtCore.Qt.TextWordWrap,users)
			doc=QtGui.QTextDocument()
			opt=doc.defaultTextOption()
			opt.setWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)
			doc.setDefaultTextOption(opt)
			doc.setDefaultFont(option.font)
			doc.setPageSize(QtCore.QSizeF(option.rect.width(),option.rect.height()-option.fontMetrics.height()))
			doc.setHtml("<font color=\"%s\">"%option.palette.highlightedText().color().name()+text+"</font>")
			print option.rect.y(),option.fontMetrics.height()
			painter.translate(option.rect.x()+1,option.rect.y()+option.fontMetrics.height())
			doc.drawContents(painter, QtCore.QRectF(0,0,option.rect.width(),option.rect.height()))
			painter.restore()
			return

		QtGui.QItemDelegate.paint(self,painter,option,index)
	
	def sizeHint(self,option,index):
		# selected item
		if option.state & QtGui.QStyle.State_Selected:
			return QtCore.QSize(100,50)
		return QtGui.QItemDelegate.sizeHint(self,option,index)

class MUCBrowserDialog(QtGui.QDialog):
	def __init__(self,main,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(False)
		self.ui=Ui_MUCBrowser()
		self.ui.setupUi(self)
		self.main=main
		self.ui.nickname.setText(main.client.jid.user)
		self.ui.groupchats.setItemDelegate(delegate(self.ui.groupchats))
		QtCore.QObject.connect(self.ui.groupchats, QtCore.SIGNAL("currentItemChanged ( QTreeWidgetItem * , QTreeWidgetItem * )"),self.selectionChanged)
		QtCore.QObject.connect(self.ui.groupchats, QtCore.SIGNAL("itemClicked ( QTreeWidgetItem *, int )"),self.CE)
		QtCore.QObject.connect(self.ui.showJid, QtCore.SIGNAL("stateChanged ( int )"),self.showJid)
		#QtCore.QObject.connect(self.ui.lineEdit, QtCore.SIGNAL("textChanged ( const QString & )"),self.filterChanged)
		QtCore.QObject.connect(self.ui.serverChangeButton, QtCore.SIGNAL("clicked()"),self.serverChanged)
		self.room=""
		self.ui.groupchats.hideColumn(1)
		self.ui.groupchats.setColumnWidth(0,42)
		self.ui.groupchats.setSortingEnabled(True)
		self.ui.groupchats.hideColumn(3)
		if not self.main.client.bookmarksEnabled:
			self.ui.groupBox_3.setEnabled(False)

		print self.main.client.disco[self.main.client.jid.host]
		mucjid = None
		for jid in self.main.client.disco[self.main.client.jid.host][None]['items'].iterkeys():
			print jid
			print self.main.client.disco[self.main.client.jid.host][None]['items'][jid]
			if self.main.client.hasIdentity(jid, 'conference', 'text') and jid.startswith('c'):
				mucjid = jid
				break
		self.server=mucjid
		if mucjid:
			self.ui.serverLabel.setText(self.tr("Server: ")+self.server)
			self.ui.lineEdit.setText(self.server)
			self.main.client.getDiscoItems(mucjid, callback = self._roomsReceived)
		self.ui.splitter.setSizes([500,150])

		#self.ui.lineEdit.hide()
		#self.ui.label_5.hide()

	def serverChanged(self):
		server=unicode(self.ui.lineEdit.text())
		self.server=server
		if self.server:
			self.ui.serverLabel.setText(self.tr("Server: ")+self.server)
			self.ui.groupchats.clear()
			self.main.client.getDiscoItems(self.server, callback = self._roomsReceived)

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
		if item and old:
			item.setSizeHint(0,old.sizeHint(0))

		if old:
			old.setData(0,QtCore.Qt.SizeHintRole,QtCore.QVariant())

		if item.parent()==None:
			room = item.data(0, 32).toString()
			self.main.client.getDiscoItems(room, callback = self._participantsReceived, callback_par = (room, item,old))
			r = room.split('@')[0]
			self.ui.roomLabel.setText(self.tr("Room: ")+r)
			self.room=r
			self.ui.name.setText(r)


	def _participantsReceived(self, par):
		item = par[1]
		for i in range(int(item.childCount())):
			item.takeChild(0)
		users="<b>Users:</b> "
		for usr in self.main.client.disco[unicode(par[0])][None]['items'].itervalues():
			users+=usr['name']+", "
			#user=QtGui.QTreeWidgetItem(item)
			#user.setText(1, usr['name'])
			#if self.ui.showJid.isChecked():
				#user.setText(1, usr['name'])
				#user.setIcon(1,self.main.getIcon(size="16x16"))
			#else:
				#user.setText(2, usr['name'])
				#user.setIcon(2,self.main.getIcon(size="16x16"))

			#user.setIcon(1,self.main.getIcon(size="16x16"))
		if item in self.ui.groupchats.selectedItems():
			item.setData(2,32,QtCore.QVariant(users))
			metrics=QtGui.QApplication.fontMetrics()
			print self.ui.groupchats.columnWidth(2),self.ui.groupchats.columnWidth(1)
			rect=metrics.boundingRect(0, 0,self.ui.groupchats.columnWidth(2), self.main.height(), QtCore.Qt.TextWordWrap, "Users: "+unicode(item.data(2,32).toString()))
			print 'aa',metrics.height(),rect.height()
			item.setSizeHint(0,QtCore.QSize(100,metrics.height()*2+rect.height()))
		#item.setToolTip(0,users)
		#self.ui.groupchats.setItemExpanded(item,True)
		#if self.ui.groupchats.sortColumn()==3:
			#self.ui.groupchats.sortByColumn(3,QtCore.Qt.DescendingOrder)
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
		room=unicode(self.room)#unicode(self.ui.room.text())
		server=unicode(self.server)#unicode(self.ui.server.text())
		name=unicode(self.ui.name.text())
		nickname=unicode(self.ui.nickname.text())
		password=unicode(self.ui.password.text())
		print room+'@'+server
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
