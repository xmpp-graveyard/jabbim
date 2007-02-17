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
		self.ui.chatTab.removeTab(0)

	def addGroupChatTab(self,room,nickname):
		tab=QtGui.QWidget(self.ui.chatTab)
		tab.jid=room
		tab.name=unicode(nickname)
		tab.typ="groupchat"
		layout=QtGui.QHBoxLayout(tab)
		tab.chat=groupChatWidget(self.main,room,self.jab,tab)
		layout.addWidget(tab.chat)
		self.ui.chatTab.addTab(tab,room)
		self.show()

	def addChatTab(self,jid,name,message=None):
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
		tab.chat=chatWidget(self.main,jid,self.jab,tab)
		layout.addWidget(tab.chat)
		self.ui.chatTab.addTab(tab,unicode(name))
		if message!=None:
			tab.chat.textEditWrite(message)

	def closeEvent(self,e):
		for index in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
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