try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from chatwindow_ui import *
from chat import *
from groupchat import *

class chatWindow(QtGui.QMainWindow):
	def __init__(self,parent,main,jab):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		self.main=main
		self.jab=jab
		self.ui=Ui_chat()
		self.ui.setupUi(self)
		self.ui.tabCloseButton=QtGui.QPushButton(QtGui.QIcon("images/icons/close.png"),"",self.ui.chatTab)
		self.ui.chatTab.setCornerWidget(self.ui.tabCloseButton)
		QtCore.QObject.connect(self.ui.tabCloseButton, QtCore.SIGNAL("clicked ()"),self.removeTab)
		QtCore.QObject.connect(self.ui.chatTab, QtCore.SIGNAL("currentChanged ( int )"),self.changeTab)
		self.ui.chatTab.removeTab(0)
		self.ui.gridlayout.setMargin(1)
		self.ui.gridlayout.setSpacing(1)
	def changeTab(self,index):
		try:
			icon=self.main.ui.roster.getUsers(str(self.ui.chatTab.widget(index).jid))[0].icon(0)
			self.ui.chatTab.setTabIcon(index,icon)
		except:
			pass

	def addGroupChatTab(self,room,nickname):
		tab=QtGui.QWidget(self.ui.chatTab)
		tab.jid=room
		tab.name=unicode(nickname)
		tab.typ="groupchat"
		layout=QtGui.QHBoxLayout(tab)
		layout.setMargin(1)
		layout.setSpacing(1)
		tab.chat=groupChatWidget(self.main,room,self.jab,tab)
		layout.addWidget(tab.chat)
		self.ui.chatTab.addTab(tab,room)
		self.show()

	def addChatTab(self,jid,name,icon,message=None):
		print jid,name,icon,unicode(message)
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
		if message!=None:
			tab.chat.textEditWrite(message)

	def closeEvent(self,e):
		for index in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(0)
			if str(w.typ)=="groupchat":
				print str(w.jid)
				self.jab.getOffRoom(str(w.jid))
			self.ui.chatTab.removeTab(0)

	def removeTab(self):
		w=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())
		if str(w.typ)=="groupchat":
			print str(w.jid)
			self.jab.getOffRoom(str(w.jid))
		self.ui.chatTab.removeTab(self.ui.chatTab.currentIndex())
		if int(self.ui.chatTab.count())==0:
			self.close()