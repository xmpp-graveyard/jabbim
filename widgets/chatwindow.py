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
import gc
from chat import *
from chatwidget import *
from groupchat import *
from include import utils
#from gamechat import *
#from headlinewidget import *
#from palette import *
import os
from twisted.words.protocols.jabber import jid as jidT
from leaveroom_ui import *
import ctypes
from ctypes.util import find_library
import sys
#if sys.platform == 'win32' :
	#def _flash( window, yes ) :
		#ctypes.windll.user32.FlashWindow( int(window.winId()), yes )

	#def _isForegroundWindow( window ) :
		#return int(window.winId()) == ctypes.windll.user32.GetForegroundWindow()

	#def _startWindowFlashing( window, reactor, callback=None ) :
		#_flash( window, False )
		#_flash( window, True )
		#def onTimer() :
			#if _isForegroundWindow(window) :
				#doCancel()
				#op.notify()
				#return
			#_flash( window, True )
		#def doCancel() :
			#timerOp.cancel()
			#_flash( window, False )
		#timerOp = reactor.addTimer( 1, onTimer )
		#op = AsyncOp( callback, doCancel )
		#return op 

	#class FlashWindow( object ) :
		#def __init__( self, reactor ) :
			#self.__flashOp = None
			#self.__reactor = reactor

		#def flash( self ) :
			#if self.__flashOp : return
			#if _isForegroundWindow(self) : return
			#def onFlashComplete() :
				#self.__flashOp = None
			#self.__flashOp = _startWindowFlashing( self,
					#self.__reactor, onFlashComplete )

		#def cancelFlash( self ) :
			#if self.__flashOp is not None :
				#self.__flashOp.cancel()
	
#elif sys.platform.startswith('linux') :
#class _XClientMessage_data( ctypes.Union ) :
	#_fields_ = [('b', ctypes.c_char*20),
				#('s', ctypes.c_short*10),
				#('l', ctypes.c_long*5)
			#]

#class XClientMessageEvent( ctypes.Structure ) :
	#_fields_ = [('type', ctypes.c_int),
				#('serial', ctypes.c_ulong),
				#('send_event', ctypes.c_int),
				#('display', ctypes.c_void_p),
				#('window', ctypes.c_ulong),
				#('message_type', ctypes.c_ulong),
				#('format', ctypes.c_int),
				#('data', _XClientMessage_data)
			#]

#class XEvent( ctypes.Union ) :
	#_fields_ = [('xclient', XClientMessageEvent),
				#('padding', ctypes.c_char*96)
			#]

#ClientMessage = 33
#SubstructureRedirectmask = 1048576
#SubstructureNotifyMask = 524288

	#def _isForegroundWindow( window ) :
		#aWin = QtGui.QApplication.activeWindow()
		#if aWin is None :
			#return False
		#else :
			#return int(window.winId()) == aWin.winId()

	#def _flash( window, yes ) :
		#xdisplay = ctypes.c_void_p( int(QtGui.QX11Info.display()) )
		#rootwin = QtGui.QX11Info.appRootWindow()
		#winId = int(window.winId())
		#try:
			#X11 = ctypes.cdll.X11
		#except:
			#pass
		#else:
			#demandsAttention = X11.XInternAtom( xdisplay, "_NET_WM_STATE_DEMANDS_ATTENTION", 1 )
			#wmState = X11.XInternAtom( xdisplay, "_NET_WM_STATE", 1 )
			#e = XEvent()
			#e.xclient.type = ClientMessage
			#e.xclient.message_type = wmState
			#e.xclient.display = xdisplay
			#e.xclient.window = winId
			#e.xclient.format = 32
			#e.xclient.data.l[1] = demandsAttention
			#e.xclient.data.l[2] = 0
			#e.xclient.data.l[3] = 0
			#e.xclient.data.l[4] = 0
	
			#if yes :
				#e.xclient.data.l[0] = 1
			#else :
				#e.xclient.data.l[0] = 0
			#X11.XSendEvent( xdisplay, rootwin, 0, (SubstructureRedirectmask |
												#SubstructureNotifyMask),
							#ctypes.pointer(e) )

	#class FlashWindow( object ) :
		#def __init__( self, reactor ) :
			#self.__reactor = reactor
			#self.__flashing = False
			#self.__timer = None

		#def __stopFlash( self ) :
			#_flash( self, False )
			#self.__flashing = False
			#self.__timer.cancel()
			#self.__timer = None

		#def flash( self ) :
			#if self.__flashing :
				#return
			#_flash( self, True )
			#self.__flashing = True
			#def onTimer( ) :
				#if _isForegroundWindow( self ) :
					#self.__stopFlash()
			#self.__timer = self.__reactor.addTimer( 1, onTimer )

		#def cancelFlash( self ) :
			#if self.__flashing :
				#self.__stopFlash()

#else :
	#class FlashWindow( object ) :
		#def __init__( self, reactor ) :
			#pass

		#def flash( self ) :
			#pass

		#def cancelFlash( self ) :
			#pass


class leaveMucDialog(QtGui.QDialog):
	def __init__(self,main,jid,parent):
		QtGui.QDialog.__init__(self,parent)
		self.setModal(True)
		self.ui=Ui_leaveroom()
		self.ui.setupUi(self)
		self.main=main
		self.ui.leaveroom.setText(self.tr("You are trying to leave room ")+unicode(jid)+"<br/>"+self.tr("Do you realy want to leave this room?"))

	def accept(self):
		if self.ui.checkBox.isChecked():
			if self.main.config['askBeforeQuitMUC']!="False":
				self.main.config["askBeforeQuitMUC"]="False"
				self.main.config.write()
		self.done(1)

class leaveAllMucDialog(QtGui.QDialog):
	def __init__(self,main,parent):
		QtGui.QDialog.__init__(self,parent)
		self.setModal(True)
		self.ui=Ui_leaveroom()
		self.ui.setupUi(self)
		self.main=main
		self.ui.leaveroom.setText(self.tr("Do you really want to leave all rooms you are connected to?"))
		
	def accept(self):
		if self.ui.checkBox.isChecked():
			self.main.config["askBeforeQuitMUC"]="False"
		self.done(1)

class tabWidget(QtGui.QTabBar):
	def __init__(self,parent,main):
		QtGui.QTabBar.__init__(self,parent)
		self.main=main
	
	def mouseReleaseEvent(self,event):
		if self.main.main.QT43:
			if event.button()==QtCore.Qt.MidButton:
				pos=event.pos()
				index=self.tabAt(pos)
				if index!=-1:
					self.main.removeTab(index)
				event.ignore()
				return
		return QtGui.QTabBar.mouseReleaseEvent(self,event)

	def wheelEvent(self,event):
		if self.main.main.QT43:
			if event.delta() <= 0:
				self.main.next()
			else:
				self.main.previous()
			event.accept()
			return
		return QtGui.QTabBar.wheelEvent(self,event)

class chatWindow(QtGui.QMainWindow):
	"""
	@group Plugins: openNewChatTab, addChatTab
	"""
	def __init__(self,parent,main):
		apply(QtGui.QMainWindow.__init__,(self,None))
		self.main=main
		self.ui=Ui_chatWindow()
		self.ui.setupUi(self)
		self.tabBar=tabWidget(self,self)
		self.ui.chatTab.setTabBar(self.tabBar)
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
		nextTab=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.AltModifier + QtCore.Qt.Key_Right), self,self.next)
		previousTab=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.AltModifier + QtCore.Qt.Key_Left), self,self.previous)
		QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.ControlModifier + QtCore.Qt.Key_W), self,self.removeTab)

		QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.AltModifier + QtCore.Qt.Key_1), self,self.tabOne)
		QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.AltModifier + QtCore.Qt.Key_2), self,self.tabTwo)
		QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.AltModifier + QtCore.Qt.Key_3), self,self.tabThree)
		QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.AltModifier + QtCore.Qt.Key_4), self,self.tabFour)
		QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.AltModifier + QtCore.Qt.Key_5), self,self.tabFive)
		QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.AltModifier + QtCore.Qt.Key_6), self,self.tabSix)
		QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.AltModifier + QtCore.Qt.Key_7), self,self.tabSeven)
		QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.AltModifier + QtCore.Qt.Key_8), self,self.tabEight)
		QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.AltModifier + QtCore.Qt.Key_9), self,self.tabNine)

		QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.AltModifier + QtCore.Qt.ShiftModifier + QtCore.Qt.Key_Right), self,self.moveRight)
		QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.AltModifier + QtCore.Qt.ShiftModifier + QtCore.Qt.Key_Left), self,self.moveLeft)
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
		#self.show()
		#self._flash()
	#def _flash(self):
		#window=self
		#yes=True
		#X11 = ctypes.cdll.LoadLibrary(find_library("X11"))
		#xdisplay = X11.XOpenDisplay(os.environ['DISPLAY'])
		#rootwin = X11.XDefaultRootWindow(xdisplay)
		#winId = int(self.winId())
		
		##try:
			##X11 = ctypes.cdll.X11
		##except:
			##print "no ctypes.cdll.X11"
			##pass
		##else:
		#demandsAttention = X11.XInternAtom( xdisplay, "_NET_WM_STATE_DEMANDS_ATTENTION", 1 )
		#wmState = X11.XInternAtom( xdisplay, "_NET_WM_STATE", 1 )
		#e = XEvent()
		#e.xclient.type = ClientMessage
		#e.xclient.message_type = wmState
		#e.xclient.display = xdisplay
		#e.xclient.window = winId
		#e.xclient.format = 32
		#e.xclient.data.l[1] = demandsAttention
		#e.xclient.data.l[2] = 0
		#e.xclient.data.l[3] = 0
		#e.xclient.data.l[4] = 0
		#if yes :
			#e.xclient.data.l[0] = 1
		#else :
			#e.xclient.data.l[0] = 0
		#X11.XSendEvent( xdisplay, rootwin, 0, (SubstructureRedirectmask |
											#SubstructureNotifyMask),
						#ctypes.pointer(e) )
		#self.flash=False
		self.flashStatus=False
		


	def startFlash(self):
		print 'flash!'
		self.flashStatus=True
		if sys.platform == 'win32':
			print "starting flash timer"
			ctypes.windll.user32.FlashWindow(int(self.winId()),True)
			self.main.client.reactor.callLater(1,self.flash)

	def flash(self):
		print 'flash timer...'
		#ctypes.windll.user32.FlashWindow(int(self.winId()),False)
		ctypes.windll.user32.FlashWindow(int(self.winId()),True)
		if self.flashStatus:
			self.main.client.reactor.callLater(1,self.flash)
		#else:
			#ctypes.windll.user32.FlashWindow(int(self.winId()),False)



	def tabOne(self):
		self.ui.chatTab.setCurrentIndex(0)
	def tabTwo(self):
		self.ui.chatTab.setCurrentIndex(1)
	def tabThree(self):
		self.ui.chatTab.setCurrentIndex(2)
	def tabFour(self):
		self.ui.chatTab.setCurrentIndex(3)
	def tabFive(self):
		self.ui.chatTab.setCurrentIndex(4)
	def tabSix(self):
		self.ui.chatTab.setCurrentIndex(5)
	def tabSeven(self):
		self.ui.chatTab.setCurrentIndex(6)
	def tabEight(self):
		self.ui.chatTab.setCurrentIndex(7)
	def tabNine(self):
		self.ui.chatTab.setCurrentIndex(8)

	def moveRight(self):
		i=int(self.ui.chatTab.currentIndex())+1
		if i<self.ui.chatTab.count():
			widget=self.ui.chatTab.currentWidget()
			text=unicode(self.ui.chatTab.tabText(i-1))
			oldtext=unicode(self.ui.chatTab.tabText(i))
			oldicon=self.ui.chatTab.tabIcon(i)
			self.ui.chatTab.insertTab(i,widget,self.ui.chatTab.tabIcon(i-1),text)
			self.ui.chatTab.setTabText(i-1,oldtext)
			self.ui.chatTab.setTabIcon(i-1,oldicon)
			self.ui.chatTab.setTabText(i,text)
			QtCore.QObject.disconnect(self.ui.chatTab, QtCore.SIGNAL("currentChanged ( int )"),self.changeTab)
			self.ui.chatTab.setCurrentIndex(i)
			QtCore.QObject.connect(self.ui.chatTab, QtCore.SIGNAL("currentChanged ( int )"),self.changeTab)
			tab=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())
			tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)

	def moveLeft(self):
		i=int(self.ui.chatTab.currentIndex())-1
		if i>=0:
			widget=self.ui.chatTab.currentWidget()
			text=unicode(self.ui.chatTab.tabText(i+1))
			oldtext=unicode(self.ui.chatTab.tabText(i))
			oldicon=self.ui.chatTab.tabIcon(i)
			self.ui.chatTab.insertTab(i,widget,self.ui.chatTab.tabIcon(i+1),text)
			self.ui.chatTab.setTabText(i+1,oldtext)
			self.ui.chatTab.setTabIcon(i+1,oldicon)
			QtCore.QObject.disconnect(self.ui.chatTab, QtCore.SIGNAL("currentChanged ( int )"),self.changeTab)
			self.ui.chatTab.setCurrentIndex(i)
			QtCore.QObject.connect(self.ui.chatTab, QtCore.SIGNAL("currentChanged ( int )"),self.changeTab)
			tab=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())
			tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)

	def next(self):
		i=int(self.ui.chatTab.currentIndex())+1
		if i<=self.ui.chatTab.count():
			self.ui.chatTab.setCurrentIndex(i)

	def previous(self):
		i=int(self.ui.chatTab.currentIndex())-1
		if i>=0:
			self.ui.chatTab.setCurrentIndex(i)

	def inactive(self):
		if self.active==False:
			print "sending inactive chatstate to all tabs"
			for i in range(self.ui.chatTab.count()):
				w=self.ui.chatTab.widget(i)
				if w.typ=="chat":
					w.active=False
					self.main.client.sendMessage(unicode(w.jid),"",composing="inactive")
			self.active=None
		if self.active==None and self.main.active==False:
			print "publishing onInactivity event"
			self.main.client.dispatcher.publishEvent('onInactivity', 30)

	def event(self,ev):
		# WindowActivated
		#print int(ev.type())
		handler=QtGui.QMainWindow.event(self,ev)
		if int(ev.type())==24 or int(ev.type())==17:
			if self.isActiveWindow():
				widget=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())
				if widget:
					if self.active==None and widget.typ=="chat":
						#for i in range(self.ui.chatTab.count()):
							#w=self.ui.chatTab.widget(i)
							#if w.typ=="chat":
								#self.main.client.sendMessage(unicode(w.jid),"",composing="active")
						widget.active=True
						self.main.client.sendMessage(unicode(widget.jid),"",composing="active")
						self.main.client.dispatcher.publishEvent('onActivity')
						print "publishing onActivity event"
					if self.active==False:
						self.main.client.dispatcher.publishEvent('onActivity')
						print "publishing onActivity event"
					index=int(self.ui.chatTab.currentIndex())
					self.changeTab(index)
					widget=self.ui.chatTab.widget(index)
					widget.chat.unread=0
					self.setWindowTitle(unicode(self.ui.chatTab.tabText(index)).replace("&",""))
					self.active=True
					print "activated..........."
					
					ev2=list(self.main.events.events)
					r=False
					for event in ev2:
						if event['name']==widget.jid and (event['type']=="newMessage" or event['type']=="message"):
							event['widget'].closeClicked()
							r=True
					if r:
						print "some events were removed"
						self.flashStatus=False
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
		return handler

	def getUnreadMessages(self):
		count=0
		for i in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
			#try:
			count+=int(w.chat.unread)
			#except:
				#pass
		return count

	def findTab(self,jid=None,full=None):
		if full==True:
			for i in range(self.ui.chatTab.count()):
				w=self.ui.chatTab.widget(i)
				if self.main.getJid(w.jid).full()==self.main.getJid(jid).full():
					return w,i # tab, index
		elif full==False:
			userhost=self.main.getJid(jid).userhost()
			for i in range(self.ui.chatTab.count()):
				w=self.ui.chatTab.widget(i)
				if self.main.getJid(w.jid).userhost()==userhost:
					return w,i # tab, index
		else:
			for i in range(self.ui.chatTab.count()):
				w=self.ui.chatTab.widget(i)
				if self.main.getJid(w.jid).full()==self.main.getJid(jid).full():
					return w,i # tab, index

			for i in range(self.ui.chatTab.count()):
				w=self.ui.chatTab.widget(i)
				if self.main.getJid(w.jid).userhost()==self.main.getJid(jid).userhost():
					return w,i # tab, index
		return None,0 # tab, index

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
		
		
		

		widget=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())
		if not widget:
			return
		widget.chat.unread=0
		self.ui.chatTab.setTabText(index,widget.tabName)

		self.setWindowTitle(unicode(self.ui.chatTab.tabText(index)).replace("&",""))

		ev=list(self.main.events.events)
		for event in ev:
			if event['name']==widget.jid and (event['type']=="newMessage" or event['type']=="message"):
				event['widget'].closeClicked()
				#break
				self.main.events.refreshTray()
		if widget.typ=="chat":
			self.main.client.sendMessage(unicode(widget.jid),"",composing="active")
			widget.active=True
		
		for i in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
			if w:
				if w.typ=="chat":
					if w.active==True and w!=widget:
						self.main.client.sendMessage(unicode(w.jid),"",composing="inactive")
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
					
		tab=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())
		tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)

	def reconnect(self):
		for i in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
			if unicode(w.typ)=="groupchat":
				w.chat.ui.line.setEnabled(True)
				message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",self.tr("You are now online."))
				w.chat.textEditWrite(message)
				self.main.client.joinGC(w.jid, w.chat.nick)

	def onGCMessage(self,w,i,body,delay,subject,user,xhtml):
		oldbody=body
		if xhtml:
			body=xhtml
			body=body.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")
		countMessage=False
		
		if int(self.ui.chatTab.currentIndex())!=i:
			if self.ui.chatTab.tabBar().tabTextColor(i).name()!=QtGui.QColor(255,0,0).name():
				self.ui.chatTab.setTabIcon(i,QtGui.QIcon("images/16x16/actions/message.png"))
				self.ui.chatTab.tabBar().setTabTextColor(i,QtGui.QColor(0,128,0))
			self.main.chat.ui.chatTab.setTabText(i,"("+unicode(w.chat.unread+1)+") "+w.tabName)
			countMessage=True
		if not self.main.chat.isActiveWindow():
			self.main.chat.setWindowTitle("("+unicode(int(self.getUnreadMessages())+1)+") "+w.tabName.replace("&",""))
			countMessage=True
		# set room topic
		if subject!=None:
			w.chat.changeTopic(unicode(subject))
			#w.chat.ui.info.setCursorPosition(0)
		# set links, if we found them

		# avatar

		if self.main.client.groupchats[w.jid].users.has_key(user):
			truejid = self.main.client.groupchats[w.jid].users[user].truejid
			print truejid
			if truejid:
				truejid=unicode(jidT.JID(truejid).userhost())
				print truejid
		else:
			truejid = None

		file = None
		#print self.main.client.avatars
		if self.main.client.avatars.has_key(w.jid+'%'+user):
			file = self.main.homeDir+'/avatars/'+unicode(w.jid+'%'+user)
		elif truejid != None and self.main.client.avatars.has_key(truejid):
			file = self.main.homeDir+'/avatars/'+unicode(truejid)
		else:
			#self.getVCard(frm+'/'+user) #tohle asi neni potreba
			pass

		if not os.path.isfile(unicode(file)):
			print truejid, w.jid, user
			#sef@njs.netlab.cz/Doma jabber@conf.netlab.cz Sef 
			file="images/32x32/apps/jabbim.png"
		if unicode(user)==unicode(w.jid):
			file = "images/32x32/categories/conferences.png"
		if not w.chat.sizes.has_key(file):
			#pixmap=QtGui.QPixmap(file).scaledToHeight(32)
			pixmap=QtGui.QPixmap(file).scaled(32,32,QtCore.Qt.KeepAspectRatio)
			w.chat.sizes[file]=[unicode(pixmap.width()),unicode(pixmap.height())]

		# no delay message
		if delay==None or len(delay)==0:
			# it's our message
			if unicode(w.chat.nick)==unicode(user):
				if unicode(body).startswith("/me"):
					message=self.main.skin["my_me_message"].replace("[time]",self.main.now()).replace("[user]",user)#.replace("[message]",unicode(body)[3:])
					body=unicode(body)[3:]
					if w.chat.lastMessageFrom==unicode(user):
						if self.main.skin.has_key('my_me_message_continue'):
							message=self.main.skin["my_me_message_continue"].replace("[time]",self.main.now()).replace("[user]",user)
				else:
					message=self.main.skin["my_message"].replace("[time]",self.main.now()).replace("[user]",user)#.replace("[message]",unicode(body))
					if w.chat.lastMessageFrom==unicode(user):
						if self.main.skin.has_key('my_message_continue'):
							message=self.main.skin["my_message_continue"].replace("[time]",self.main.now()).replace("[user]",user)
			else:
				# it's message for us
				if utils.need_highlight(unicode(w.chat.nick), unicode(oldbody)) and not unicode(body).startswith("/me"):
					if int(self.ui.chatTab.currentIndex())!=i:
						if self.ui.chatTab.tabBar().tabTextColor(i).name()!=QtGui.QColor(255,0,0).name():
							self.ui.chatTab.setTabIcon(i,QtGui.QIcon("images/16x16/actions/message.png"))
							self.ui.chatTab.tabBar().setTabTextColor(i,QtGui.QColor(255,0,0))
					message=self.main.skin["message_for_me"].replace("[time]",self.main.now()).replace("[user]",user)#.replace("[message]",unicode(body))
					if w.chat.lastMessageFrom==unicode(user):
						if self.main.skin.has_key('message_for_me_continue'):
							message=self.main.skin["message_for_me_continue"].replace("[time]",self.main.now()).replace("[user]",user)
				else:
					if unicode(body).startswith("/me"):
						message=self.main.skin["me_message"].replace("[time]",self.main.now()).replace("[user]",user)#.replace("[message]",unicode(body)[3:])
						body=unicode(body)[3:]
						if w.chat.lastMessageFrom==unicode(user):
							if self.main.skin.has_key('me_message_continue'):
								message=self.main.skin["me_message_continue"].replace("[time]",self.main.now()).replace("[user]",user)
					else:
						message=self.main.skin["message"].replace("[time]",self.main.now()).replace("[user]",user)
						if w.chat.lastMessageFrom==unicode(user):
							if self.main.skin.has_key('message_continue'):
								message=self.main.skin["message_continue"].replace("[time]",self.main.now()).replace("[user]",user)
					colors=None
					if len(w.chat.getUserItems(user))!=0:
						item=w.chat.getUserItems(user)[0]
						if item in w.chat.colors:
							cIndex=w.chat.colors.index(item)
							colors=self.main.getSkinColors(cIndex)
					else:
						colors=self.main.getSkinColors(0)
					if colors!=None:
						message=message.replace("[foreground]",colors[0]).replace("[background]",colors[1])
						if len(colors)==3:
							message=message.replace("[additive]",colors[2])
		

			message=message.replace("[avatar]","<img src=\""+file+"\" height=\""+w.chat.sizes[file][1]+"\" width=\""+w.chat.sizes[file][0]+"\" />")
			message=message.replace('[message]',body)
			# write message
			if countMessage:
				w.chat.unread+=1
			print unicode(message)
			w.chat.textEditWrite(message)
			w.chat.lastMessageFrom=unicode(user)
			return
		else:
			# get delay from string
			delay=unicode(delay)
			delay="%s-%s-%s&nbsp;%s:%s:%s" % (delay[0:4],delay[4:6],delay[6:8],delay[9:11],delay[12:14],delay[15:17])
			# our delayed message
			if unicode(w.chat.nick)==unicode(user):
				message=self.main.skin["my_message_history"].replace("[time]",delay).replace("[user]",user).replace("[message]",unicode(body))
			else:
				# delayed message for us
				if utils.need_highlight(unicode(w.chat.nick), unicode(body)):
					message=self.main.skin["message_for_me_history"].replace("[time]",delay).replace("[user]",user).replace("[message]",unicode(body))
				else:
					message=self.main.skin["message_history"].replace("[time]",delay).replace("[user]",user).replace("[message]",unicode(body))
			message=message.replace("[avatar]","<img src=\""+file+"\" height=\""+unicode(int(w.chat.sizes[file][1])/2)+"\" width=\""+unicode(int(w.chat.sizes[file][0])/2)+"\" />")
			colors=None
			if len(w.chat.getUserItems(user))!=0:
				item=w.chat.getUserItems(user)[0]
				if item in w.chat.colors:
					cIndex=w.chat.colors.index(item)
					colors=self.main.getSkinColors(cIndex)
			else:
				colors=self.main.getSkinColors(0)
			if colors!=None:
				message=message.replace("[foreground]",colors[0]).replace("[background]",colors[1])
			w.chat.lastMessageFrom=unicode(user)

			w.chat.textEditWrite(message)

	def openNewChatTab(self,jid,name,icon=None,message=None):
		if not icon:
			icon=self.main.ui.roster.getIconByJID(jid)
		created=False
		if self.isHidden():
			created=True
			self.showMinimized()
		self.addChatTab(jid,unicode(user),icon,message)
		if created:
			self.setWindowState(self.windowState() & ~QtCore.Qt.WindowActive | QtCore.Qt.WindowMinimized )
			self.setWindowState(self.windowState() & QtCore.Qt.WindowActive)

		tab,tabIndex=self.findTab(jid)
		if tab:
			self.ui.chatTab.setTabIcon(tabIndex,QtGui.QIcon("images/16x16/actions/message.png"))
			self.ui.chatTab.tabBar().setTabTextColor(tabIndex,QtGui.QColor(255,0,0))
			self.ui.chatTab.setTabText(tabIndex,"("+str(tab.chat.unread+1)+") "+tab.tabName)
			if message:
				tab.chat.unread+=1

	def addChatTab(self,jid,name,icon,message=None):
		#for i in range(self.ui.chatTab.count()):
			#w=self.ui.chatTab.widget(i)
			#try:
				#tabjid=w.jid
			#except:
				#tabjid=""
			#if tabjid==jid:
		tab,index=self.findTab(jid,False)
		if tab:
			self.show()
			self.raise_()
			self.activateWindow()
			tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
			self.ui.chatTab.setCurrentIndex(index)
			return
		item=self.main.ui.roster.getUserItems(jidT.JID(jid).userhost())
		metaitem=self.main.ui.roster.getMetaItems(jidT.JID(jid).userhost())

		tab=QtGui.QWidget(self.ui.chatTab)
		tab.jid=jid
		tab.typ="chat"
		tab.ic=icon
		tab.active=True
		layout=QtGui.QHBoxLayout(tab)
		layout.setMargin(1)
		layout.setSpacing(1)
		tab.chat=chatWidget(self.main,jid,tab)
		it=[]
		if len(item)!=0:
			it=item
		elif len(metaitem)!=0:
			it=metaitem[0]

		if len(it)!=0:
			it=it[0]
			avatar=it.avatar
			if avatar:
				#avatar=avatar.pixmap(100,112)
				#print "avatar:",unicode(avatar.width())+"x"+unicode(avatar.height())
				#if avatar.width()<=58 and avatar.height()<=58:
					#size=64
				#else:
					#size=128
				#result=QtGui.QPixmap(size,size)
				#result.fill(QtCore.Qt.transparent)
				#frame=QtGui.QPixmap("images/"+unicode(size)+"x"+unicode(size)+"/frame.png")
				#painter=QtGui.QPainter(result)
				##painter.fillRect(0,0,size,size,QtGui.QBrush(self.palette().color(QtGui.QPalette.Window)))
				#painter.drawPixmap((size-avatar.width())/2,(size-avatar.height())/2,avatar)
				#painter.drawPixmap(0,0,frame)
				#painter.end()
				result=self.main.getAvatar(avatar,size="128x128",frame=True)
				if result:
					tab.chat.ui.avatar.setPixmap(result)
		else:
			result=self.main.getAvatar(unicode(jid).replace("/","%"),size="128x128",frame=True)
			if result:
			#if os.path.isfile(self.main.homeDir+'/avatars/'+unicode(jid).replace("/","%")):
				#f=open(self.main.homeDir+'/avatars/'+unicode(jid).replace("/","%"),"rb")
				#image = f.read()
				#f.close()
				#pixmap=QtGui.QPixmap()
				#pixmap.loadFromData(image)
				#avatar=QtGui.QIcon(pixmap)
				#avatar=avatar.pixmap(100,112)
				#if avatar.width()<=58 and avatar.height()<=58:
					#size=64
				#else:
					#size=128
				#result=QtGui.QPixmap(size,size)
				#result.fill(QtCore.Qt.transparent)
				#frame=QtGui.QPixmap("images/"+unicode(size)+"x"+unicode(size)+"/frame.png")
				#painter=QtGui.QPainter(result)
				##painter.fillRect(0,0,size,size,QtGui.QBrush(self.palette().color(QtGui.QPalette.Window)))
				
				#painter.drawPixmap((size-avatar.width())/2,(size-avatar.height())/2,avatar)
				#painter.drawPixmap(0,0,frame)
				#painter.end()
				tab.chat.ui.avatar.setPixmap(result)

				
		layout.addWidget(tab.chat)
		print "adding new tab...", icon
		tab.tabName=unicode("&"+unicode(name))
		self.ui.chatTab.addTab(tab,icon,"&"+unicode(name))
		if message:
			tab.unread=1
			self.setWindowTitle("(1) "+unicode(name))
			if not self.isActiveWindow() or self.windowState() & QtCore.Qt.WindowMinimized:
				self.startFlash()
		else:
			self.ui.chatTab.setCurrentIndex(self.ui.chatTab.indexOf(tab))
			self.setWindowTitle(unicode(name))
			tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)

		tab.chat.ui.label.setText("<font size=\"3\"><b>"+name+"</b></font>")
		if message!=None:
			message=message.replace("[avatar]","<img src=\""+tab.chat.file+"\" width=\"32\" height=\""+unicode(tab.chat.avatarHeight)+"\" />")
			tab.chat.textEditWrite(message)
		#self.show()
		#self.raise_()
		#self.activateWindow()
		#self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
		#self.activate()

	def addGroupChatTab(self,room,nickname,affiliation="",name=None):
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
		tab.chat=groupChatWidget(self.main,room,tab,nickname)
		#tab.chat.ui.admin.hide()
		layout.addWidget(tab.chat)
		jmeno = room
		if unicode(self.main.config["useMUCNames"])=="True":
			for nick, bookmark  in self.main.client.bookmarks['conference'].iteritems():
				if bookmark.jid.userhost() == room:
					jmeno = nick
		if name:
			jmeno=name
		tab.tabName=unicode(jmeno)
		self.ui.chatTab.addTab(tab,QtGui.QIcon("images/16x16/categories/muc.png"), jmeno)
		self.setWindowTitle(unicode(jmeno))
		self.ui.chatTab.setCurrentIndex(self.ui.chatTab.indexOf(tab))
		
		self.show()
		tab.chat.showConnecting()
		self.raise_()
		self.activateWindow()
		tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
		return True


	def closeEvent(self,e):
		ask=False
		for i in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
			if unicode(w.typ)=='groupchat':
				ask=True
				break
		
		if ask and self.main.config["askBeforeQuitMUC"]=="True" and self.main.app.shutdown==False:
			d=leaveAllMucDialog(self.main,self)
			if d.exec_()==1:
				for index in range(self.ui.chatTab.count()):
					self.removeTab(0,ask=False)
				e.accept()
			else:
				e.ignore()
		else:
			for index in range(self.ui.chatTab.count()):
				self.removeTab(0,ask=False)
			e.accept()

	def removeTab(self,index=None,ask=True):
		if index==None:
			index=self.ui.chatTab.currentIndex()
		w=self.ui.chatTab.widget(index)
		if w.typ=="chat":
			print w.chat.ui.splitter.sizes()
			self.main.config['chatSplitterSizes']=list(w.chat.ui.splitter.sizes())
			self.main.config['chatSplitter2Sizes']=list(w.chat.ui.splitter_2.sizes())
			self.main.client.sendMessage(unicode(w.jid),"",composing="gone")
		

		if w.typ=="groupchat":
			self.main.config['groupchatSplitSizes1']=list(w.chat.ui.splitter.sizes())
			self.main.config['groupchatSplitSizes2']=list(w.chat.ui.splitter_2.sizes())
			self.main.config['groupchatSplitSizes3']=list(w.chat.ui.splitter_3.sizes())
		removed=False
		if unicode(w.typ)=="groupchat" and self.main.client!=None:
			print self.main.config["askBeforeQuitMUC"]
			if ask and self.main.config["askBeforeQuitMUC"]=="True" and self.main.app.shutdown==False:
				d=leaveMucDialog(self.main,w.jid,self)
				if d.exec_()==1:
					if self.main.client.groupchats.has_key(w.jid):
						self.main.client.leaveGC(w.jid)
					self.ui.chatTab.removeTab(index)
					if int(self.ui.chatTab.count())==0:
						self.hide()
					removed=True
			else:
				if self.main.client.groupchats.has_key(w.jid):
					self.main.client.leaveGC(w.jid)
				self.ui.chatTab.removeTab(index)
				if int(self.ui.chatTab.count())==0:
					self.hide()
				removed=True
		else:
			self.ui.chatTab.removeTab(index)
			if int(self.ui.chatTab.count())==0:
				self.hide()
			removed=True
		#w.deleteLater()
		if removed:
			l=gc.get_referents(w)
			for x in range(len(l)):
				del l[0]
			l=gc.get_referrers(w)
			for x in range(len(l)):
				del l[0]
			print gc.get_referrers(w)
			w.setParent(None)
			del w
	
			print "GARBAGE:",gc.garbage
			del gc.garbage[:]
			print "GARBAGE:",gc.garbage
			print "UNREACHABLE OBJECTS:",gc.collect()

		#del
