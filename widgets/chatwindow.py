try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from chat import *
from chatwidget import *
from groupchat import *
#from gamechat import *
#from headlinewidget import *
#from palette import *
import os

class chatWindow(QtGui.QMainWindow):
	def __init__(self,parent,main):
		apply(QtGui.QMainWindow.__init__,(self,None))
		self.main=main
		self.ui=Ui_chatWindow()
		self.ui.setupUi(self)
		self.ui.chatTab.removeTab(0)
		## tab
		#self.ui.chatTab = mainTab(main,self.ui.centralwidget)
		#self.ui.chatTab.setObjectName("chatTab")
		#self.ui.gridlayout.addWidget(self.ui.chatTab,0,0,1,1)

		self.ui.tabCloseButton=QtGui.QPushButton(QtGui.QIcon("images/icons/close.png"),"",self.ui.chatTab)
		self.ui.chatTab.setCornerWidget(self.ui.tabCloseButton)
		QtCore.QObject.connect(self.ui.tabCloseButton, QtCore.SIGNAL("clicked ()"),self.removeTab)
		QtCore.QObject.connect(self.ui.chatTab, QtCore.SIGNAL("currentChanged ( int )"),self.changeTab)
		#self.ui.chatTab.removeTab(0)
		#self.ui.gridlayout.setMargin(1)
		#self.ui.gridlayout.setSpacing(1)
		#palette=self.palette()
		#palette,images=loadPalette(palette,self.main.palette["chatwindow"])
		#self.setPalette(palette)
		#self.pixmap=images['bgImage']

	#def paintEvent(self,event):
		## paintEvent handler
		#if self.pixmap!=None:
			#viewport=self
			#painter=QtGui.QPainter(viewport)
			#for x in range(int(int(viewport.width())//self.pixmap.width())+1):
				#for y in range(int(int(viewport.height())/self.pixmap.height())+1):
					#painter.drawPixmap(x*int(self.pixmap.width()),y*self.pixmap.height(),self.pixmap)
		#QtGui.QMainWindow.paintEvent(self,event)


	def changeTab(self,index):
		try:
			self.ui.chatTab.widget(index).chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
		except: pass
		#try:
		jid=unicode(self.ui.chatTab.widget(index).jid)
		if len(unicode(jid).rsplit("/"))!=1:
			resource=unicode(jid).rsplit("/")[1]
			jid=unicode(jid).rsplit("/")[0]
			#res=self.main.ui.roster.getResourceItems(jid)
			
			#show=self.main.icons[unicode(res[resource].text(1))[0]]
			#icon=self.main.getIcon(jid,show,size="16x16")
		#else:
		print "jid:"+unicode(jid)
		icon=self.main.getIcon(jid,self.main.icons[unicode(self.main.ui.roster.getUserItems(jid)[0].text(1))[0]],size="16x16")
		color=self.ui.chatTab.tabBar().palette().color(QtGui.QPalette.Foreground)
		self.ui.chatTab.tabBar().setTabTextColor(index,color)
		self.ui.chatTab.setTabIcon(index,icon)
		self.setWindowTitle(self.ui.chatTab.tabText(index))

		#except:
			#pass

	def addChatTab(self,jid,name,icon,message=None):
		for i in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
			try:
				tabjid=w.jid
			except:
				tabjid=""
			if w.jid==jid:
				self.show()
				self.raise_()
				self.activateWindow()
				w.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
				self.ui.chatTab.setCurrentIndex(i)
				return
		tab=QtGui.QWidget(self.ui.chatTab)
		tab.jid=jid
		tab.typ="chat"
		layout=QtGui.QHBoxLayout(tab)
		layout.setMargin(1)
		layout.setSpacing(1)
		tab.chat=chatWidget(self.main,jid,tab)
		layout.addWidget(tab.chat)
		print "adding new tab...", icon
		self.ui.chatTab.addTab(tab,icon,unicode(name))
		self.ui.chatTab.setCurrentIndex(self.ui.chatTab.indexOf(tab))
		tab.chat.ui.label.setText("<h2>"+name+"<h2/>")
		if message!=None:
			tab.chat.textEditWrite(message)
		self.show()
		self.raise_()
		self.activateWindow()
		self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
		tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)

	def addGroupChatTab(self,room,nickname,affiliation=""):
		for i in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
			try:
				tabjid=w.jid
			except:
				tabjid=""
			if w.jid==room:
				self.show()
				self.raise_()
				self.activateWindow()
				w.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
				self.ui.chatTab.setCurrentIndex(i)
				return False
		tab=QtGui.QWidget(self.ui.chatTab)
		tab.jid=room
		tab.name=unicode(nickname)
		tab.typ="groupchat"
		layout=QtGui.QHBoxLayout(tab)
		layout.setMargin(1)
		layout.setSpacing(1)
		tab.chat=groupChatWidget(self.main,room,tab)
		tab.chat.ui.admin.hide()
		layout.addWidget(tab.chat)
		self.ui.chatTab.addTab(tab,QtGui.QIcon("images/16x16/categories/muc.png"),room)
		self.ui.chatTab.setCurrentIndex(self.ui.chatTab.indexOf(tab))
		self.show()
		self.raise_()
		self.activateWindow()
		tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
		return True


	def closeEvent(self,e):
		for index in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(0)
			if str(w.typ)=="groupchat":
				#print str(w.jid)
				self.main.client.leaveGC(w.jid)
				#self.jab.getOffRoom(str(w.jid),self.main.groupchat[str(w.jid)][0])
			self.ui.chatTab.removeTab(0)

	def removeTab(self):
		w=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())
		if str(w.typ)=="groupchat":
			#print str(w.jid)
			self.main.client.leaveGC(w.jid)
		self.ui.chatTab.removeTab(self.ui.chatTab.currentIndex())
		if int(self.ui.chatTab.count())==0:
			self.close()