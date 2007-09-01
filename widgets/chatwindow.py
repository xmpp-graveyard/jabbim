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
		self.active=False
		self.timer=QtCore.QTimer()
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.inactive)
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

	def inactive(self):
		if self.active==False:
			for i in range(self.ui.chatTab.count()):
				w=self.ui.chatTab.widget(i)
				if w.typ=="chat":
					w.active=False
					self.main.client.sendMessage(str(w.jid),"",composing="inactive")
			self.active=None
		self.main.client.dispatcher.publishEvent('onInactivity', 30)

	def event(self,ev):
		# WindowActivated
		if int(ev.type())==24:
			widget=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())

			if self.active==None and widget.typ=="chat":
				#for i in range(self.ui.chatTab.count()):
					#w=self.ui.chatTab.widget(i)
					#if w.typ=="chat":
						#self.main.client.sendMessage(str(w.jid),"",composing="active")
				widget.active=True
				self.main.client.sendMessage(str(widget.jid),"",composing="active")
				self.main.client.dispatcher.publishEvent('onActivity')
			
			self.active=True

			
			#print self.main.events.events
			ev2=list(self.main.events.events)
			for event in ev2:
				if event['name']==widget.jid and (event['type']=="newMessage" or event['type']=="message"):
					event['widget'].closeClicked()
					#break
			self.main.events.refreshTray()
			color=self.ui.chatTab.tabBar().palette().color(QtGui.QPalette.Foreground)
			self.ui.chatTab.tabBar().setTabTextColor(self.ui.chatTab.currentIndex(),color)
			self.timer.stop()
		elif int(ev.type())==25:
			if self.active:
				print "INACTIVE"
				self.active=False
				self.timer.start(30000)
		return QtGui.QMainWindow.event(self,ev)

	def changeTab(self,index):
		try:
			self.ui.chatTab.widget(index).chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
		except: pass
		#try:
		jid=unicode(self.ui.chatTab.widget(index).jid)
		typ=unicode(self.ui.chatTab.widget(index).typ)
		if len(unicode(jid).rsplit("/"))!=1:
			resource=unicode(jid).rsplit("/")[1]
			jid=unicode(jid).rsplit("/")[0]
			#res=self.main.ui.roster.getResourceItems(jid)
			
			#show=self.main.icons[unicode(res[resource].text(1))[0]]
			#icon=self.main.getIcon(jid,show,size="16x16")
		#else:
		if typ=="chat":
			#icon=self.main.getIcon(jid,self.main.icons[unicode(self.main.ui.roster.getUserItems(jid)[0].status)],size="16x16")
			self.ui.chatTab.setTabIcon(index,self.ui.chatTab.widget(index).ic)
		elif typ == 'groupchat':
			self.ui.chatTab.setTabIcon(index,QtGui.QIcon("images/16x16/categories/muc.png"))
			
		color=self.ui.chatTab.tabBar().palette().color(QtGui.QPalette.Foreground)
		self.ui.chatTab.tabBar().setTabTextColor(index,color)
		
		self.setWindowTitle(self.ui.chatTab.tabText(index))

		widget=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())
		
		ev=list(self.main.events.events)
		for event in ev:
			if event['name']==widget.jid and (event['type']=="newMessage" or event['type']=="message"):
				event['widget'].closeClicked()
				#break
				self.main.events.refreshTray()
		if w.typ=="chat":
			self.main.client.sendMessage(str(widget.jid),"",composing="active")
			widget.active=True
		
		for i in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
			if w.typ=="chat":
				if w.active==True and w!=widget:
					self.main.client.sendMessage(str(w.jid),"",composing="inactive")
					w.active=False
		#except:
			#pass

	def activate(self,jid=None):
		print "activate"
		self.show()
		self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
		self.raise_()
		self.activateWindow()
		if jid:
			frm=jid
			tab=None
			tabIndex=0
			for i in range(self.main.chat.ui.chatTab.count()):
				w=self.main.chat.ui.chatTab.widget(i)
				if unicode(w.jid)==unicode(frm):
					tab=w
					tabIndex=i
					break
				if unicode(w.jid).rsplit("/")[0]==unicode(frm).rsplit("/")[0]:
					tab=w
					tabIndex=i
			# we found tab
			if tab!=None:
				self.ui.chatTab.setCurrentWidget(tab)
				#self.changeTab()
				return
					
		#tab=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())
		#tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)

	def reconnect(self):
		for i in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
			if str(w.typ)=="groupchat":
				w.chat.ui.line.setEnabled(True)
				message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",self.tr("You are now online."))
				w.chat.textEditWrite(message)
				self.main.client.joinGC(w.jid, w.name)

	def addChatTab(self,jid,name,icon,message=None):
		for i in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
			try:
				tabjid=w.jid
			except:
				tabjid=""
			if tabjid==jid:
				self.show()
				self.raise_()
				self.activateWindow()
				w.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
				self.ui.chatTab.setCurrentIndex(i)
				return
		tab=QtGui.QWidget(self.ui.chatTab)
		tab.jid=jid
		tab.typ="chat"
		tab.ic=icon
		tab.active=True
		layout=QtGui.QHBoxLayout(tab)
		layout.setMargin(1)
		layout.setSpacing(1)
		tab.chat=chatWidget(self.main,jid,tab)
		layout.addWidget(tab.chat)
		print "adding new tab...", icon
		self.ui.chatTab.addTab(tab,icon,unicode(name))
		self.ui.chatTab.setCurrentIndex(self.ui.chatTab.indexOf(tab))
		self.setWindowTitle(unicode(name))
		tab.chat.ui.label.setText("<h2>"+name+"<h2/>")
		if message!=None:
			tab.chat.textEditWrite(message)
		#self.show()
		#self.raise_()
		#self.activateWindow()
		#self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
		#self.activate()
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
		jmeno = room
		for nick, bookmark  in self.main.client.bookmarks['conference'].iteritems():
			if bookmark.jid.userhost() == room:
				jmeno = nick
		self.ui.chatTab.addTab(tab,QtGui.QIcon("images/16x16/categories/muc.png"), jmeno)
		self.setWindowTitle(unicode(jmeno))
		self.ui.chatTab.setCurrentIndex(self.ui.chatTab.indexOf(tab))
		self.show()
		self.raise_()
		self.activateWindow()
		tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
		return True


	def closeEvent(self,e):
		for index in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(0)
			if str(w.typ)=="groupchat" and self.main.client!=None:
				if self.main.client.groupchats.has_key(w.jid):
					self.main.client.leaveGC(w.jid)
			self.ui.chatTab.removeTab(0)
		self.hide()
		e.ignore()

	def removeTab(self):
		w=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())
		if str(w.typ)=="groupchat" and self.main.client!=None:
			if self.main.client.groupchats.has_key(w.jid):
				self.main.client.leaveGC(w.jid)
		self.ui.chatTab.removeTab(self.ui.chatTab.currentIndex())
		if int(self.ui.chatTab.count())==0:
			self.hide()
