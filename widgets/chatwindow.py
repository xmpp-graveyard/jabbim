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
# Recursively expand slist's objects
# into olist, using seen to track
# already processed objects.
def _getr(slist, olist, seen):
  for e in slist:
    if id(e) in seen:
      continue
    seen[id(e)] = None
    olist.append(e)
    tl = gc.get_referents(e)
    if tl:
      _getr(tl, olist, seen)

# The public function.
def get_all_objects():
  """Return a list of all live Python
  objects, not including the list itself."""
  gcl = gc.get_objects()
  olist = []
  seen = {}
  # Just in case:
  seen[id(gcl)] = None
  seen[id(olist)] = None
  seen[id(seen)] = None
  # _getr does the real work.
  _getr(gcl, olist, seen)
  return olist
import types

def get_refcounts():
    d = {}
    sys.modules
    # collect all classes
    for m in sys.modules.values():
        for sym in dir(m):
            o = getattr (m, sym)
            if type(o) is types.ClassType:
                d[o] = sys.getrefcount (o)
    # sort by refcount
    pairs = map (lambda x: (x[1],x[0]), d.items())
    pairs.sort()
    pairs.reverse()
    return pairs

def print_top_100():
    for n, c in get_refcounts()[:100]:
        print '%10d %s' % (n, c.__name__)


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
		self.ui.leaveroom.setText(self.tr("You are trying to leave room ")+unicode(jid)+". "+self.tr("Do you realy want to leave this room?"))
		policy=self.ui.leaveroom.sizePolicy()
		policy.setHeightForWidth(True)
		policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
		self.ui.leaveroom.setSizePolicy(policy)
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
		policy=self.ui.leaveroom.sizePolicy()
		policy.setHeightForWidth(True)
		policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
		self.ui.leaveroom.setSizePolicy(policy)

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
	MainWindow for conversations (chat)
	"""
	def __init__(self,parent,main):
		apply(QtGui.QMainWindow.__init__,(self,None))
		self.main=main #: Jabbim mainWindow
		self.ui=Ui_chatWindow()
		self.ui.setupUi(self)

		# make QTabWidget
		self.tabBar=tabWidget(self,self) #: QTabWidget for conversations
		self.ui.chatTab.setTabBar(self.tabBar)
		self.ui.chatTab.removeTab(0)
		self.ui.tabCloseButton=QtGui.QPushButton(QtGui.QIcon("images/icons/close.png"),"",self.ui.chatTab)
		self.ui.chatTab.setCornerWidget(self.ui.tabCloseButton)
		self.active=False #: depracted
		self.timer=QtCore.QTimer() #: depracted
		self.flashStatus=False #: True if window is flashing in windows bar

		QtCore.QObject.connect(self.ui.tabCloseButton, QtCore.SIGNAL("clicked ()"),self.removeTab)
		QtCore.QObject.connect(self.ui.chatTab, QtCore.SIGNAL("currentChanged ( int )"),self.changeTab)
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.inactive)

	#{ Private functions

	def startFlash(self):
		"""
		Starts windows flashing
		"""
		print 'flash!'
		self.flashStatus=True
		if sys.platform == 'win32':
			print "starting flash timer"
			ctypes.windll.user32.FlashWindow(int(self.winId()),True)
			self.main.client.reactor.callLater(1,self.flash)

	def flash(self):
		"""
		Called by flash timer, changes flash state
		"""
		print 'flash timer...'
		ctypes.windll.user32.FlashWindow(int(self.winId()),True)
		if self.flashStatus:
			self.main.client.reactor.callLater(1,self.flash)

	def inactive(self):
		"""
		Sends incative composing message when chat window is inactive
		"""
		if self.active==False:
			print "sending inactive chatstate to all tabs"
			for i in range(self.ui.chatTab.count()):
				w=self.ui.chatTab.widget(i)
				if w.typ=="chat":
					w.active=False
					self.main.client.sendMessage(unicode(w.jid),"",composing="inactive")
			self.active=None

	def event(self,ev):
		"""
		QWidgets event handler
		"""
		handler=QtGui.QMainWindow.event(self,ev)
		# activated
		if int(ev.type())==24 or int(ev.type())==17:
			if self.isActiveWindow():
				widget=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())
				if widget:
					# sends activity event to current tab, if we sent inactive before
					if self.active==None and widget.typ=="chat":
						widget.active=True
						self.main.client.sendMessage(unicode(widget.jid),"",composing="active")
					index=int(self.ui.chatTab.currentIndex())
					self.changeTab(index)
					self.active=True

				self.timer.stop()
		# inactive
		elif int(ev.type())==25:
			if self.active:
				self.active=False
				self.timer.start(30000)
		return handler

	#{ Shortcuts

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
		if i<self.ui.chatTab.count():
			self.ui.chatTab.setCurrentIndex(i)
		if i>=self.ui.chatTab.count() and self.main.config['tabCycling'] == 'True':
			self.ui.chatTab.setCurrentIndex(0)

	def previous(self):
		i=int(self.ui.chatTab.currentIndex())-1
		if i>=0:
			self.ui.chatTab.setCurrentIndex(i)
		if i < 0 and self.main.config['tabCycling'] == 'True':
			self.ui.chatTab.setCurrentIndex(self.ui.chatTab.count()-1)
	

	#{ Public Functions

	def getUnreadMessages(self):
		count=0
		for i in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
			#try:
			count+=int(w.chat.unread)
			#except:
				#pass
		return count

	def findTab(self,jid=None,full=None,typ=['chat','groupchat']):
		if full==True:
			for i in range(self.ui.chatTab.count()):
				w=self.ui.chatTab.widget(i)
				if self.main.getJid(w.jid).full()==self.main.getJid(jid).full() and w.typ in typ:
					return w,i # tab, index
		elif full==False:
			userhost=self.main.getJid(jid).userhost()
			for i in range(self.ui.chatTab.count()):
				w=self.ui.chatTab.widget(i)
				if self.main.getJid(w.jid).userhost()==userhost and not self.main.getJid(w.jid).resource and w.typ in typ:
					return w,i # tab, index
		else:
			for i in range(self.ui.chatTab.count()):
				w=self.ui.chatTab.widget(i)
				if self.main.getJid(w.jid).full()==self.main.getJid(jid).full() and w.typ in typ:
					return w,i # tab, index

			for i in range(self.ui.chatTab.count()):
				w=self.ui.chatTab.widget(i)
				if self.main.getJid(w.jid).userhost()==self.main.getJid(jid).userhost() and w.typ in typ:
					return w,i # tab, index
		return None,0 # tab, index

	def findTabByMeta(self,jid):
		userhost=self.main.getJid(jid).userhost()
		for i in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
			if w.typ=="chat":
				if w.chat.hasMetacontact(userhost):
					return w,i # tab, index
		return None,0


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
			jid=self.main.getJid(event['name'])
			if jid:
				if jid.userhost()==self.main.getJid(widget.jid).userhost() and (event['type']=="newMessage" or event['type']=="message"):
					event['widget'].closeClicked()
					#break
					self.flashStatus=False
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
		if self.main.client.avatarDef.has_key(w.jid+'/'+user):
			file = self.main.realHomeDir+'/avatars/'+str(self.main.client.avatarDef[w.jid+'/'+user])
		elif truejid != None and self.main.client.avatarDef.has_key(truejid):
			file = self.main.realHomeDir+'/avatars/'+str(self.main.client.avatarDef[truejid])
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
				self.main.client.dispatcher.publishEvent('groupchatMessageEvent', self.main.getJid(w.jid),user,oldbody,subject, xhtml)
				# it's message for us
				if utils.need_highlight(unicode(w.chat.nick), unicode(oldbody)) and not unicode(body).startswith("/me"):
					self.main.client.dispatcher.publishEvent('groupchatMessageForMeEvent', self.main.getJid(w.jid),user,oldbody,subject, xhtml)
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

	def addChatTab(self,jid,name,icon,message=None,full=False):
		#for i in range(self.ui.chatTab.count()):
			#w=self.ui.chatTab.widget(i)
			#try:
				#tabjid=w.jid
			#except:
				#tabjid=""
			#if tabjid==jid:
		if full:
			tab,index=self.findTab(jid,full)
		else:
			tab,index=self.findTab(jid,None)
		if tab:
			self.show()
			self.raise_()
			self.activateWindow()
			tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
			self.ui.chatTab.setCurrentIndex(index)
			return tab
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
		#if len(item)!=0:
			#it=item
		#elif len(metaitem)!=0:
			#it=metaitem[0]

		#if len(it)!=0:
			#it=it[0]
			#avatar=it.avatar
			#if avatar:
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
				#result=self.main.getAvatar(self.main.getJid(unicode(jid)).userhost(),size="128x128",frame=True)
				#if result:
					#tab.chat.ui.avatar.setPixmap(result)
		#else:
			#result=self.main.getAvatar(self.main.getJid(unicode(jid)).userhost(),size="128x128",frame=True)
			#if result:
			##if os.path.isfile(self.main.homeDir+'/avatars/'+unicode(jid).replace("/","%")):
				##f=open(self.main.homeDir+'/avatars/'+unicode(jid).replace("/","%"),"rb")
				##image = f.read()
				##f.close()
				##pixmap=QtGui.QPixmap()
				##pixmap.loadFromData(image)
				##avatar=QtGui.QIcon(pixmap)
				##avatar=avatar.pixmap(100,112)
				##if avatar.width()<=58 and avatar.height()<=58:
					##size=64
				##else:
					##size=128
				##result=QtGui.QPixmap(size,size)
				##result.fill(QtCore.Qt.transparent)
				##frame=QtGui.QPixmap("images/"+unicode(size)+"x"+unicode(size)+"/frame.png")
				##painter=QtGui.QPainter(result)
				###painter.fillRect(0,0,size,size,QtGui.QBrush(self.palette().color(QtGui.QPalette.Window)))
				
				##painter.drawPixmap((size-avatar.width())/2,(size-avatar.height())/2,avatar)
				##painter.drawPixmap(0,0,frame)
				##painter.end()
				#tab.chat.ui.avatar.setPixmap(result)
		result=self.main.getAvatar(self.main.getJid(unicode(jid)).userhost(),size="128x128",frame=True)
		if not result:
			result=self.main.getAvatar(QtGui.QPixmap("images/48x48/apps/jabbim.png"),size="64x64",frame=True)
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
		tab.chat.name=name
		tab.chat.refreshLabel()
		#tab.chat.ui.label.setText("<font size=\"3\"><b>"+name+"</b></font>")
		if message!=None:
			message=message.replace("[avatar]","<img src=\""+tab.chat.file+"\" width=\"32\" height=\""+unicode(tab.chat.avatarHeight)+"\" />")
			tab.chat.textEditWrite(message)
		return tab
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
		# splitter size
		tab.chat.ui.splitter.setSizes([800,64])
		tab.chat.ui.splitter_2.setSizes(list(self.main.config['groupchatSplitSizes2']))
		tab.chat.ui.splitter_3.setSizes(list(self.main.config['groupchatSplitSizes3']))
		#tab.chat.ui.admin.hide()
		layout.addWidget(tab.chat)
		jmeno = room
		if unicode(self.main.config["useMUCNames"])=="True":
			for nick, bookmark  in self.main.client.bookmarks['conference'].iteritems():
				if bookmark.jid.userhost() == room:
					jmeno = bookmark.name
		if name:
			jmeno=name
		if len(jmeno)>22:
			jmeno=jmeno[:22]+"..."
		tab.tabName=unicode(jmeno)
		self.ui.chatTab.addTab(tab,QtGui.QIcon("images/16x16/categories/muc.png"), jmeno)
		self.setWindowTitle(unicode(jmeno))
		self.ui.chatTab.setCurrentIndex(self.ui.chatTab.indexOf(tab))
		
		self.show()
		self.raise_()
		self.activateWindow()
		tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
		tab.chat.showConnecting()
		return True

	def addCustomTab(self,jid,nickname,name,widget,widgetList,typ="chat",full=False,icon=None):
		if full:
			tab,index=self.findTab(jid,full)
		else:
			tab,index=self.findTab(jid,None)
		if tab:
			self.show()
			self.raise_()
			self.activateWindow()
			#tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
			#self.ui.chatTab.setCurrentIndex(index)
			return tab
		if not icon:
			icon=QtGui.QIcon("images/16x16/categories/muc.png")
		tab=QtGui.QWidget(self.ui.chatTab)
		tab.jid=jid
		tab.typ=typ
		tab.ic=icon
		tab.active=True
		tab.name=nickname
		layout=QtGui.QHBoxLayout(tab)
		layout.setMargin(1)
		layout.setSpacing(1)
		tab.chat=widget(*widgetList)

		layout.addWidget(tab.chat)
		print "adding new custom tab", icon
		tab.tabName=unicode("&"+unicode(name))
		self.ui.chatTab.addTab(tab,icon,"&"+unicode(name))
		self.setWindowTitle(unicode(name))

		return tab

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
			try:
				self.main.config['groupchatSplitSizes3']=list(w.chat.ui.splitter_3.sizes())
				self.main.config['groupchatSplitSizes1']=list(w.chat.ui.splitter.sizes())
				self.main.config['groupchatSplitSizes2']=list(w.chat.ui.splitter_2.sizes())
			except:
				pass
		w.chat.on_remove()
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
		if removed:
			w.deleteLater()
			w.setParent(None)
			w.close()
			w.chat.parent=None
			w.chat.main=None
			del w.chat.parent
			del w.chat.ui
			del w.chat
			del w.jid
			del w.typ
			del w

			del gc.garbage[:]
			gc.collect()

			#from guppy import hpy; h=hpy()
			#print h.heap()
			#f=open(unicode(time.time()),'w')
			#for obj in get_all_objects():
				#f.write(str(type(obj))+" "+str(id(obj))+"\n")
			#f.close
			#print_top_100()
