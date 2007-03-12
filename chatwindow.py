try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from chatwindow_ui import *
from chat import *
from groupchat import *
from gamechat import *
from headlinewidget import *
from palette import *
import os

class mainTabBar(QtGui.QTabBar):
	def __init__(self,main,parent=None):
		apply(QtGui.QTabBar.__init__,(self,parent))
		palette=self.palette()
		palette,images=loadPalette(palette,main.palette["chatwindowTab"])
		self.setPalette(palette)
		self.pixmap=images['bgImage']
	def paintEvent(self,event):
		# paintEvent handler
		if self.pixmap!=None:
			viewport=self
			painter=QtGui.QPainter(viewport)
			for x in range(int(int(viewport.width())//self.pixmap.width())+1):
				for y in range(int(int(viewport.height())/self.pixmap.height())+1):
					painter.drawPixmap(x*int(self.pixmap.width()),y*self.pixmap.height(),self.pixmap)
		QtGui.QTabBar.paintEvent(self,event)

class mainTab(QtGui.QTabWidget):
	def __init__(self,main,parent=None):
		apply(QtGui.QTabWidget.__init__,(self,parent))
		palette=self.palette()
		self.setTabBar(mainTabBar(main,self))
		#palette,images=loadPalette(palette,main.palette["chatwindowTab"])
		#self.setPalette(palette)
		#self.pixmap=images['bgImage']
		#print self.pixmap


class chatWindow(QtGui.QMainWindow):
	def __init__(self,parent,main,jab):
		apply(QtGui.QMainWindow.__init__,(self,None))
		self.main=main
		self.jab=jab
		self.ui=Ui_chat()
		self.ui.setupUi(self)
		# tab
		self.ui.chatTab = mainTab(main,self.ui.centralwidget)
		self.ui.chatTab.setObjectName("chatTab")
		self.ui.gridlayout.addWidget(self.ui.chatTab,0,0,1,1)

		self.ui.tabCloseButton=QtGui.QPushButton(QtGui.QIcon("images/icons/close.png"),"",self.ui.chatTab)
		self.ui.chatTab.setCornerWidget(self.ui.tabCloseButton)
		QtCore.QObject.connect(self.ui.tabCloseButton, QtCore.SIGNAL("clicked ()"),self.removeTab)
		QtCore.QObject.connect(self.ui.chatTab, QtCore.SIGNAL("currentChanged ( int )"),self.changeTab)
		self.ui.chatTab.removeTab(0)
		self.ui.gridlayout.setMargin(1)
		self.ui.gridlayout.setSpacing(1)
		palette=self.palette()
		palette,images=loadPalette(palette,self.main.palette["chatwindow"])
		self.setPalette(palette)
		self.pixmap=images['bgImage']

	def paintEvent(self,event):
		# paintEvent handler
		if self.pixmap!=None:
			viewport=self
			painter=QtGui.QPainter(viewport)
			for x in range(int(int(viewport.width())//self.pixmap.width())+1):
				for y in range(int(int(viewport.height())/self.pixmap.height())+1):
					painter.drawPixmap(x*int(self.pixmap.width()),y*self.pixmap.height(),self.pixmap)
		QtGui.QMainWindow.paintEvent(self,event)


	def changeTab(self,index):
		try:
			self.ui.chatTab.widget(index).chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
		except: pass
		try:
			icon=self.main.getIcon(str(self.ui.chatTab.widget(index).jid),self.main.iconSort[unicode(self.main.ui.roster.getUsers(str(self.ui.chatTab.widget(index).jid))[0].text(1))[0]],size="16x16")
			self.ui.chatTab.setTabIcon(index,icon)
		except:
			pass

	def addHeadlineTab(self):
		tab=QtGui.QWidget(self.ui.chatTab)
		tab.jid=""
		tab.name=self.tr("Headlines")
		tab.typ="headline"
		layout=QtGui.QHBoxLayout(tab)
		layout.setMargin(1)
		layout.setSpacing(1)
		tab.chat=headlineWidget(self.main,self.jab,tab)
		layout.addWidget(tab.chat)
		self.ui.chatTab.addTab(tab,self.tr("Headlines"))
		self.ui.chatTab.setCurrentIndex(self.ui.chatTab.indexOf(tab))
		self.show()
		return tab.chat

	def addGameChatTab(self,room,nickname):
		tab=QtGui.QWidget(self.ui.chatTab)
		tab.jid=room
		tab.name=unicode(nickname)
		tab.typ="groupchat"
		layout=QtGui.QHBoxLayout(tab)
		layout.setMargin(1)
		layout.setSpacing(1)
		tab.chat=gameChatWidget(self.main,room,self.jab,tab)
		layout.addWidget(tab.chat)
		self.ui.chatTab.addTab(tab,room)
		self.ui.chatTab.setCurrentIndex(self.ui.chatTab.indexOf(tab))
		self.show()

	def addGroupChatTab(self,room,nickname,affiliation=""):
		tab=QtGui.QWidget(self.ui.chatTab)
		tab.jid=room
		tab.name=unicode(nickname)
		tab.typ="groupchat"
		layout=QtGui.QHBoxLayout(tab)
		layout.setMargin(1)
		layout.setSpacing(1)
		tab.chat=groupChatWidget(self.main,room,self.jab,affiliation,tab)
		tab.chat.ui.admin.hide()
		layout.addWidget(tab.chat)
		self.ui.chatTab.addTab(tab,QtGui.QIcon("images/16x16/categories/muc.png"),room)
		self.ui.chatTab.setCurrentIndex(self.ui.chatTab.indexOf(tab))
		self.show()

	def addChatTab(self,jid,name,icon,message=None):
		for i in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
			try:
				if w.jid==jid:
					self.show()
					return
			except:
				pass
		self.show()
		tab=QtGui.QWidget(self.ui.chatTab)
		tab.jid=jid
		tab.typ="chat"
		layout=QtGui.QHBoxLayout(tab)
		layout.setMargin(1)
		layout.setSpacing(1)
		tab.chat=chatWidget(self.main,jid,self.jab,tab)
		layout.addWidget(tab.chat)
		self.ui.chatTab.addTab(tab,icon,unicode(name))
		self.ui.chatTab.setCurrentIndex(self.ui.chatTab.indexOf(tab))
		if os.path.isfile(self.main.homeDir+'/.jabbim/avatars/'+jid):
			pixmap=QtGui.QPixmap()
			f=open(self.main.homeDir+'/.jabbim/avatars/'+jid,"r")
			image=f.read()
			f.close()
			pixmap.loadFromData(image)
			tab.chat.ui.avatar.setPixmap(pixmap.scaled(32,32,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
		tab.chat.ui.label.setText("<h2>"+name+"<h2/>")
		if message!=None:
			tab.chat.textEditWrite(message)
		self.show()

	def closeEvent(self,e):
		for index in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(0)
			if str(w.typ)=="groupchat":
				print str(w.jid)
				self.jab.getOffRoom(str(w.jid),self.main.groupchat[str(w.jid)][0])
			self.ui.chatTab.removeTab(0)

	def removeTab(self):
		w=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())
		if str(w.typ)=="groupchat":
			print str(w.jid)
			self.jab.getOffRoom(str(w.jid),self.main.groupchat[str(w.jid)][0])
		self.ui.chatTab.removeTab(self.ui.chatTab.currentIndex())
		if int(self.ui.chatTab.count())==0:
			self.close()