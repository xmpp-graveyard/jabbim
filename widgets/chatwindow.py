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
from include import utils
#from gamechat import *
#from headlinewidget import *
#from palette import *
import os
from twisted.words.protocols.jabber import jid as jidT

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

		#QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.AltModifier + QtCore.Qt.ShiftModifier + QtCore.Qt.Key_Right), self,self.moveRight)
		#QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.AltModifier + QtCore.Qt.ShiftModifier + QtCore.Qt.Key_Left), self,self.moveLeft)
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
		#if i<=self.ui.chatTab.count():
			#widget=self.ui.chatTab.currentWidget()
			#text=unicode(self.ui.chatTab.tabText(i-1))
			#oldtext=unicode(self.ui.chatTab.tabText(i))
			#oldicon=self.ui.chatTab.tabIcon(i)
			#self.ui.chatTab.insertTab(i,widget,self.ui.chatTab.tabIcon(i-1),text)
			#self.ui.chatTab.setTabText(i-1,oldtext)
			#self.ui.chatTab.setTabIcon(i-1,oldicon)
			#QtCore.QObject.disconnect(self.ui.chatTab, QtCore.SIGNAL("currentChanged ( int )"),self.changeTab)
			#self.ui.chatTab.setCurrentIndex(i)
			#QtCore.QObject.connect(self.ui.chatTab, QtCore.SIGNAL("currentChanged ( int )"),self.changeTab)
			#tab=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())
			#tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)

	def moveLeft(self):
		i=int(self.ui.chatTab.currentIndex())-1
		#if i>=0:
			#widget=self.ui.chatTab.currentWidget()
			#text=unicode(self.ui.chatTab.tabText(i+1))
			#oldtext=unicode(self.ui.chatTab.tabText(i))
			#oldicon=self.ui.chatTab.tabIcon(i)
			#self.ui.chatTab.insertTab(i,widget,self.ui.chatTab.tabIcon(i+1),text)
			#self.ui.chatTab.setTabText(i+1,oldtext)
			#self.ui.chatTab.setTabIcon(i+1,oldicon)
			#QtCore.QObject.disconnect(self.ui.chatTab, QtCore.SIGNAL("currentChanged ( int )"),self.changeTab)
			#self.ui.chatTab.setCurrentIndex(i)
			#QtCore.QObject.connect(self.ui.chatTab, QtCore.SIGNAL("currentChanged ( int )"),self.changeTab)
			#tab=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())
			#tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)

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
				print "publishing onActivity event"
			if self.active==False:
				self.main.client.dispatcher.publishEvent('onActivity')
				print "publishing onActivity event"
			index=int(self.ui.chatTab.currentIndex())
			widget=self.ui.chatTab.widget(index)
			widget.chat.unread=0
			self.setWindowTitle(unicode(self.ui.chatTab.tabText(index)).replace("&",""))
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

	def getUnreadMessages(self):
		count=0
		for i in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
			#try:
			count+=int(w.chat.unread)
			#except:
				#pass
		return count

	def findTab(self,jid=None):
		for i in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
			if unicode(w.jid)==jid:
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
					
		tab=self.ui.chatTab.widget(self.ui.chatTab.currentIndex())
		tab.chat.ui.line.setFocus(QtCore.Qt.MouseFocusReason)

	def reconnect(self):
		for i in range(self.ui.chatTab.count()):
			w=self.ui.chatTab.widget(i)
			if str(w.typ)=="groupchat":
				w.chat.ui.line.setEnabled(True)
				message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",self.tr("You are now online."))
				w.chat.textEditWrite(message)
				self.main.client.joinGC(w.jid, w.name)

	def onGCMessage(self,w,i,body,delay,subject,user):
		countMessage=False
		if int(self.ui.chatTab.currentIndex())!=i:
			if self.ui.chatTab.tabBar().tabTextColor(i).name()!=QtGui.QColor(255,0,0).name():
				self.ui.chatTab.setTabIcon(i,QtGui.QIcon("images/16x16/actions/message.png"))
				self.ui.chatTab.tabBar().setTabTextColor(i,QtGui.QColor(0,128,0))
			self.main.chat.ui.chatTab.setTabText(i,w.tabName+" ("+str(w.chat.unread+1)+")")
			countMessage=True
		if not self.main.chat.isActiveWindow():
			self.main.chat.setWindowTitle(w.tabName.replace("&","")+" ("+str(int(self.getUnreadMessages())+1)+")")
			countMessage=True
		# set room topic
		if subject!=None:
			subject=utils.replace_url(subject)
			w.chat.ui.info.setHtml(unicode(subject))
			#w.chat.ui.info.setCursorPosition(0)
		# set links, if we found them
					
		# no delay message
		if delay==None or len(delay)==0:
			# it's our message
			if unicode(w.name)==unicode(user):
				if unicode(body).startswith("/me"):
					message=self.main.skin["my_me_message"].replace("[time]",self.main.now()).replace("[user]",user)#.replace("[message]",unicode(body)[3:])
					body=unicode(body)[3:]
				else:
					message=self.main.skin["my_message"].replace("[time]",self.main.now()).replace("[user]",user)#.replace("[message]",unicode(body))
			else:
				# it's message for us
				if utils.need_highlight(unicode(w.name), unicode(body)) and not unicode(body).startswith("/me"):
					if int(self.ui.chatTab.currentIndex())!=i:
						if self.ui.chatTab.tabBar().tabTextColor(i).name()!=QtGui.QColor(255,0,0).name():
							self.ui.chatTab.setTabIcon(i,QtGui.QIcon("images/16x16/actions/message.png"))
							self.ui.chatTab.tabBar().setTabTextColor(i,QtGui.QColor(255,0,0))
					message=self.main.skin["message_for_me"].replace("[time]",self.main.now()).replace("[user]",user)#.replace("[message]",unicode(body))
				else:
					if unicode(body).startswith("/me"):
						message=self.main.skin["me_message"].replace("[time]",self.main.now()).replace("[user]",user)#.replace("[message]",unicode(body)[3:])
						body=unicode(body)[3:]
					else:
						message=self.main.skin["message"].replace("[time]",self.main.now()).replace("[user]",user)#.replace("[message]",unicode(body))
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
					
			
			if self.main.client.groupchats[w.jid].users.has_key(user):
				truejid = self.main.client.groupchats[w.jid].users[user].truejid
				print truejid
				if truejid:
					truejid=unicode(jidT.JID(truejid).userhost())
					print truejid
			else:
				truejid = None
			file = None
			print self.main.client.avatars
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
				pixmap=QtGui.QPixmap(file).scaledToHeight(32)
				
				w.chat.sizes[file]=str(pixmap.width())
				
			message=message.replace("[avatar]","<img src=\""+file+"\" height=\"32\" width=\""+w.chat.sizes[file]+"\" />")
			message=message.replace('[message]',body)
			# write message
			if countMessage:
				w.chat.unread+=1
			w.chat.textEditWrite(message)
			return
		else:
			# get delay from string
			delay=unicode(delay)
			delay="%s-%s-%s %s:%s:%s" % (delay[0:4],delay[4:6],delay[6:8],delay[9:11],delay[12:14],delay[15:17])
			# our delayed message
			if unicode(w.name)==unicode(user):
				message=self.main.skin["my_message_history"].replace("[time]",delay).replace("[user]",user).replace("[message]",unicode(body))
			else:
				# delayed message for us
				if utils.need_highlight(unicode(w.name), unicode(body)):
					message=self.main.skin["message_for_me_history"].replace("[time]",delay).replace("[user]",user).replace("[message]",unicode(body))
				else:
					message=self.main.skin["message_history"].replace("[time]",delay).replace("[user]",user).replace("[message]",unicode(body))

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


			w.chat.textEditWrite(message)

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
				#print "avatar:",str(avatar.width())+"x"+str(avatar.height())
				#if avatar.width()<=58 and avatar.height()<=58:
					#size=64
				#else:
					#size=128
				#result=QtGui.QPixmap(size,size)
				#result.fill(QtCore.Qt.transparent)
				#frame=QtGui.QPixmap("images/"+str(size)+"x"+str(size)+"/frame.png")
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
				#frame=QtGui.QPixmap("images/"+str(size)+"x"+str(size)+"/frame.png")
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
		self.ui.chatTab.setCurrentIndex(self.ui.chatTab.indexOf(tab))
		self.setWindowTitle(unicode(name))
		if jidT.JID(jid).resource:
			tab.chat.ui.label.setText("<font size=\"3\"><b>"+name+"</b><br/>"+self.tr("Resource:")+" "+jidT.JID(jid).resource+"</font>")
		else:
			tab.chat.ui.label.setText("<font size=\"3\"><b>"+name+"</b></font>")
		if message!=None:
			message=message.replace("[avatar]","<img src=\""+tab.chat.file+"\" width=\"32\" height=\""+str(tab.chat.avatarHeight)+"\" />")
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
		#tab.chat.ui.admin.hide()
		layout.addWidget(tab.chat)
		jmeno = room
		if str(self.main.config["useMUCNames"])=="True":
			for nick, bookmark  in self.main.client.bookmarks['conference'].iteritems():
				if bookmark.jid.userhost() == room:
					jmeno = nick
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

		if w.typ=="chat":
			print w.chat.ui.splitter.sizes()
			self.main.config['chatSplitterSizes']=list(w.chat.ui.splitter.sizes())
			self.main.config['chatSplitter2Sizes']=list(w.chat.ui.splitter_2.sizes())

		if w.typ=="groupchat":
			self.main.config['groupchatSplitSizes1']=list(w.chat.ui.splitter.sizes())
			self.main.config['groupchatSplitSizes2']=list(w.chat.ui.splitter_2.sizes())
			self.main.config['groupchatSplitSizes3']=list(w.chat.ui.splitter_3.sizes())

		self.ui.chatTab.removeTab(self.ui.chatTab.currentIndex())
		if int(self.ui.chatTab.count())==0:
			self.hide()
