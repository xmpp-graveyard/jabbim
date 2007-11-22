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
from groupchatwidget_ui import *
from groupchatadmin import *
from configobj import ConfigObj
import urllib,re,os
from twisted.web.microdom import *
from twisted.web.domhelpers import gatherTextNodes
import dataforms
from twisted.words.protocols.jabber import jid as jidT

class flowLayout(QtGui.QLayout):
	def __init__(self, parent=None, margin=0, spacing=-1):
		QtGui.QLayout.__init__(self, parent)

		if parent is not None:
			self.setMargin(margin)
		self.setSpacing(spacing)

		self.itemList = []

	def addItem(self, item):
		self.itemList.append(item)

	def count(self):
		return len(self.itemList)

	def itemAt(self, index):
		if index >= 0 and index < len(self.itemList):
			return self.itemList[index]

	def takeAt(self, index):
		if index >= 0 and index < len(self.itemList):
			return self.itemList.pop(index)

	def expandingDirections(self):
		return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

	def hasHeightForWidth(self):
		return True

	def heightForWidth(self, width):
		height = self.doLayout(QtCore.QRect(0, 0, width, 0), True)
		return height

	def setGeometry(self, rect):
		QtGui.QLayout.setGeometry(self, rect)
		self.doLayout(rect, False)

	def sizeHint(self):
		return self.minimumSize()

	def minimumSize(self):
		size = QtCore.QSize()

		for item in self.itemList:
			size = size.expandedTo(item.minimumSize())

		size += QtCore.QSize(2 * self.margin(), 2 * self.margin())
		return size

	def doLayout(self, rect, testOnly):
		x = rect.x()
		y = rect.y()
		lineHeight = 0

		for item in self.itemList:
			nextX = x + item.sizeHint().width() + self.spacing()
			if nextX - self.spacing() > rect.right() and lineHeight > 0:
				x = rect.x()
				y = y + lineHeight + self.spacing()
				nextX = x + item.sizeHint().width() + self.spacing()
				lineHeight = 0

			if not testOnly:
				item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

			x = nextX
			lineHeight = max(lineHeight, item.sizeHint().height())

		return y + lineHeight - rect.y()

class textView(QtGui.QTextEdit):
	def __init__(self,main,parent):
		QtGui.QTextEdit.__init__(self,parent)
		self.parent=main
		self.setMouseTracking(True)
		self.setReadOnly(True)
		self.data=[]
	def mouseMoveEvent(self,event):
		anchor = self.anchorAt(event.pos())
		if len(anchor)!=0:
			self.viewport().setCursor(QtCore.Qt.PointingHandCursor)
		else:
			self.viewport().setCursor(QtCore.Qt.ArrowCursor)
		return QtGui.QTextEdit.mouseMoveEvent(self,event)
		
	def mousePressEvent(self,event):
		anchor = self.anchorAt(event.pos())
		if len(anchor)!=0:
			QtGui.QDesktopServices.openUrl(QtCore.QUrl(anchor))
		return QtGui.QTextEdit.mousePressEvent(self,event)

	def createMimeDataFromSelection (self):
		text=unicode(self.textCursor().selection().toHtml())
		#print text
		a=parseString(text)
		for el in a.getElementsByTagName('img'):
			path=el.attributes['src'].split('/')[-1]
			for k,v in self.parent.smileys.iteritems():
				if v==path:
					path=k
					newnode = parseString("<div> "+path+"</div>").documentElement
					el.parentNode.replaceChild(newnode,el)
					break
		b=a.getElementsByTagName('body')
		try:
			c=parseString(unicode(b[0].toxml(),'utf-8').replace("<!--EndFragment-->","").replace("<!--StartFragment-->",""))
		except:
			c=parseString(unicode(b[0].toxml()).replace("<!--EndFragment-->","").replace("<!--StartFragment-->",""))
		for el in c.getElementsByTagName('br'):
			#if self.parent.main.skin['spaces_between_lines']=='1':
				#newnode = parseString("<div> "+unichr(2028)+unichr(2028)+"</div>").documentElement
			#else:
			newnode = parseString("<div> "+unichr(2028)+"</div>").documentElement
			el.parentNode.replaceChild(newnode,el)
		for el in c.getElementsByTagName('table'):
			newnode = parseString(unicode(el.toxml(),'utf-8')+"<div>"+unichr(2028)+unichr(2028)+"NN</div>").documentElement
			#print unicode(el.toxml())
			el.parentNode.replaceChild(newnode,el)
			
		text=gatherTextNodes(c)
		u=False
		try:
			text=unicode(text, 'utf-8')
			u=True
		except:
			text=unicode(text)
		#if u:
		text=text.replace(unichr(2028),"\n")
		print unicode(text)

		self.data.append(QtCore.QMimeData())
		self.data[-1].setText(unicode(text))
		return self.data[-1]

class lineEditWidget(QtGui.QTextEdit):
	def __init__(self,main,parent=None):
		apply(QtGui.QTextEdit.__init__,(self,parent))
		self.main=main
		self.parent=parent
		#self.setMaximumSize(QtCore.QSize(16777215,30))
		self.setObjectName("line")
	
	def keyPressEvent(self,event):
		key=event.key()
		if key==QtCore.Qt.Key_Return or key==QtCore.Qt.Key_Enter:
			self.main.sendButtonClicked()
		else:
			QtGui.QTextEdit.keyPressEvent(self,event)
			text=unicode(self.toPlainText())
			for k,v in self.parent.smileys.iteritems():
				if text.find(" "+k)!=-1:
					html=self.toHtml()
					html.replace(k,'<img src="images/16x16/emotes/'+v+'"/> ')
					cur=self.textCursor()
					self.setHtml(html)
					self.setTextCursor(cur)

class frame(QtGui.QFrame):
	def __init__(self,main,parent=None):
		QtGui.QFrame.__init__(self,parent)
		self.main=main

	def hideEvent(self,event):
		self.main.ui.smileys.setChecked(False)

class normalLineEditWidget(QtGui.QTextEdit):
	def __init__(self,main,parent=None):
		apply(QtGui.QTextEdit.__init__,(self,parent))
		self.main=main
		self.parent=parent
		#self.setMaximumSize(QtCore.QSize(16777215,30))
		self.setObjectName("line")
	
	def keyPressEvent(self,event):
		key=event.key()
		if (key==QtCore.Qt.Key_Return or key==QtCore.Qt.Key_Enter) and (event.modifiers() & QtCore.Qt.ControlModifier):
			if self.main.main.config['sendByCtrl']=="True":
				self.main.sendButtonClicked()
				event.accept()
			else:
				return QtGui.QTextEdit.keyPressEvent(self,event)
		elif key==QtCore.Qt.Key_Return or key==QtCore.Qt.Key_Enter:
			print self.main.main.config['sendByCtrl']
			if self.main.main.config['sendByCtrl']=="False":
				self.main.sendButtonClicked()
				event.accept()
			else:
				return QtGui.QTextEdit.keyPressEvent(self,event)
		elif key == QtCore.Qt.Key_Up and  self.main.hindex > 0 and (event.modifiers() & QtCore.Qt.ControlModifier): 

			self.main.hindex = self.main.hindex-1
			self.main.ui.line.setText(self.main.sent[self.main.hindex])
		elif key == QtCore.Qt.Key_Down and  self.main.hindex < len(self.main.sent) and (event.modifiers() & QtCore.Qt.ControlModifier): 

			self.main.hindex = self.main.hindex+1
			self.main.ui.line.setText(self.main.sent[self.main.hindex])
		else:
			return QtGui.QTextEdit.keyPressEvent(self,event)

class groupChatWidget(QtGui.QWidget):
	def __init__(self,main,jid,jab,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.jab=jab
		self.ui=Ui_groupchatwidget()
		self.ui.setupUi(self)
		self.main=main
		self.affiliation=""
		self.cache={}
		self.lines=0
		self.maxLines=300

		l=QtGui.QHBoxLayout(self.ui.viewWidget)
		l.setMargin(0)
		l.setSpacing(0)
		self.ui.textEdit=textView(self,self.ui.viewWidget)
		#self.ui.textEdit=textView()
		#self.ui.textEdit.setReadOnly(False)
		l.addWidget(self.ui.textEdit)

		layout=QtGui.QHBoxLayout(self.ui.lineWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		if self.main.config['chatMode']=="normal":
			self.ui.line=normalLineEditWidget(self,self)
		else:
			self.ui.line=lineEditWidget(self,self)
		self.ui.line.setAcceptRichText(False)
		layout.addWidget(self.ui.line)

		#self.buttonGroup=QtGui.QButtonGroup(self.ui.logs)
		##self.buttonGroup.setExclusive(True)
		#self.ui.logsLayout=QtGui.QHBoxLayout(self.ui.logs)
		
		#self.actual=QtGui.QPushButton(self.tr("Actual"),self.ui.logs)
		#self.actual.setCheckable(True)
		#self.actual.setChecked(True)
		#self.ui.logsLayout.addWidget(self.actual)
		#self.buttonGroup.addButton(self.actual)

		QtCore.QObject.connect(self.ui.sendButton, QtCore.SIGNAL("clicked ()"),self.sendButtonClicked)
		
		
		#QtCore.QObject.connect(self.buttonGroup, QtCore.SIGNAL("buttonClicked ( QAbstractButton * )  "),self.logButton)
		#QtCore.QObject.connect(self.ui.line, QtCore.SIGNAL("returnPressed ()"),self.sendButtonClicked)
		#QtCore.QObject.connect(self.ui.line, QtCore.SIGNAL("textChanged ()"),self.lines)
		#QtCore.QObject.connect(self.ui.smileys, QtCore.SIGNAL("clicked (bool)"),self.smileysClicked)
		QtCore.QObject.connect(self.ui.sendButton, QtCore.SIGNAL("clicked ()"),self.sendButtonClicked)
		QtCore.QObject.connect(self.ui.smileys, QtCore.SIGNAL("clicked (bool)"),self.smileysClicked)
		QtCore.QObject.connect(self.ui.users, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.userClicked)
		QtCore.QObject.connect(self.ui.users, QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.usersContextMenu)
		self.ui.users.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		short=QtGui.QShortcut("tab",self.ui.line)
		QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.tabPressed)
		#self.ui.info_big.hide()
		self.loadSmileys()
		self.jid=jid
		self.name_id=-1 # for tabPressed
		self.roles={}
		self.addRole("participant",self.tr("Participants"))
		self.addRole("moderator",self.tr("Moderators"))
		self.addRole("visitor",self.tr("Visitors"))
		self.ui.users.header().hide()
		self.ui.users.hideColumn(1)
		#self.ui.line.setMaximumHeight(int(self.ui.line.currentFont().pointSize())+15)
		#self.ui.line.setMaximumHeight(int(self.ui.line.currentFont().pointSize())*8)
		#self.ui.lineWidget.setMaximumHeight(int(self.ui.line.currentFont().pointSize())*8)
		self.ui.splitter.setSizes(list(self.main.config['groupchatSplitSizes1']))
		self.ui.splitter_2.setSizes(list(self.main.config['groupchatSplitSizes2']))
		self.ui.splitter_3.setSizes(list(self.main.config['groupchatSplitSizes3']))
		#if self.main.client.groupchats[self.jid].users[nick].affiliation=="owner":
		
		self.sent = []
		self.hindex = 0
		self.sizes={}
		self.colors=[]



		self.flowLayout = flowLayout()
		
		for key,value in self.main.plugins.iteritems():
			value.buildChatWidget(unicode(jidT.JID(self.jid).userhost()),self.flowLayout)
		
		self.ui.admin=QtGui.QToolButton()
		self.ui.admin.setIconSize(QtCore.QSize(16,16))
		self.ui.admin.setIcon(QtGui.QIcon("images/32x32/actions/register.png"))
		self.ui.admin.setToolTip(self.tr("Room administration"))
		self.flowLayout.addWidget(self.ui.admin)
		QtCore.QObject.connect(self.ui.admin, QtCore.SIGNAL("clicked ()"),self.roomConfigClicked)

		self.ui.clearChat=QtGui.QToolButton()
		self.ui.clearChat.setIconSize(QtCore.QSize(16,16))
		self.ui.clearChat.setIcon(QtGui.QIcon("images/32x32/actions/clear.png"))
		self.ui.clearChat.setToolTip(self.tr("Clear chat"))
		self.flowLayout.addWidget(self.ui.clearChat)
		QtCore.QObject.connect(self.ui.clearChat, QtCore.SIGNAL("clicked ()"),self.clearChat)
		self.ui.admin.hide()

		self.ui.pluginWidget.setLayout(self.flowLayout)


		self.unread=0
		
		self.connecting=QtGui.QLabel(self.tr("Connecting to MUC. This can take a few seconds."),self.ui.textEdit)
		self.connecting.adjustSize()
	
		self.init=""
		if self.main.skin.has_key("on_init"):
			self.init=self.main.skin["on_init"]
		self.ui.textEdit.setHtml("<br/>"+self.init)

	
	def showConnecting(self):
		pos=self.ui.textEdit.mapToGlobal(QtCore.QPoint(0,0))
		x=pos.x()
		y=pos.y()
		self.connecting.setGeometry((x+self.ui.textEdit.width())/2-self.connecting.width()/2,(y+self.ui.textEdit.height())/2-self.connecting.height()/2, self.connecting.width(), self.connecting.height())
		self.connecting.show()
		
	def addRoles(self):
		self.addRole("participant",self.tr("Participants"))
		self.addRole("moderator",self.tr("Moderators"))
		self.addRole("visitor",self.tr("Visitors"))
	#def lines(self):
		#if self.ui.line.verticalScrollBar().isVisible():
			#self.ui.line.setMaximumHeight(int(self.ui.line.maximumHeight())+int(self.ui.line.currentFont().pointSize())+10)

	#def changeAffiliation(self,affiliation):
		#if affiliation=="owner":
			#self.ui.admin.show()
		#self.affiliation=affiliation

	def usersContextMenu(self,pos):
		item=self.ui.users.itemFromIndex(self.ui.users.indexAt(pos)) # get selected item
		name=unicode(item.text(0)) # get contact name
		menu=QtGui.QMenu(self.ui.users) # make menu
		if item.parent()!=None:
			action=menu.addAction(self.tr("Kick"))
			action.setData(QtCore.QVariant(name))
			action.setObjectName("kick")

		menu.connect(menu, QtCore.SIGNAL("triggered ( QAction * )"),self.usersContextMenuTriggered)
		# set menu position and show
		menu.popup(self.ui.users.mapToGlobal(pos))
	
	def usersContextMenuTriggered(self,action):
		cmd=action.objectName()
		if cmd=="kick":
			name=unicode(action.data().toString())
			if self.main.client.groupchats.has_key(self.jid):
				reason,b=QtGui.QInputDialog.getText(self,self.tr("Reason"),self.tr("Enter reason:"), QtGui.QLineEdit.Normal, "")
				reason=unicode(reason)
				# if user set new name of group
				if b==True:
					self.main.client.groupchats[self.jid].setRole(name, 'none',  reason)

	def userClicked(self,item,i):
		if item.parent()==None:
			return
		icon=self.main.getIcon(status=self.main.icons[unicode(item.text(1))[0]],size="16x16")
		self.main.chat.addChatTab(self.jid+"/"+unicode(item.text(0)),item.text(0),icon)
		self.main.chat.activate()
		
	def clearChat(self):
		self.init=""
		if self.main.skin.has_key("on_init"):
			self.init=self.main.skin["on_init"]
		self.ui.textEdit.setHtml("<br/>"+self.init)
	
	def roomConfigClicked(self):
		nick=self.main.client.groupchats[self.jid].nick
		if self.main.client.groupchats[self.jid].users[nick].affiliation=="owner":
			d=self.main.client.getMUCConfig(self.jid)
			d.addCallback(self._onRoomConfig)

	def _onRoomConfig(self,data):
		jid=data[0]
		form=data[1]
		if form!=None:
			self.dialog=groupchatAdminDialog(self.main,jid,form,self)
			self.dialog.show()

	def roomAdminClicked(self):
		pass
		#self.jab.getGroupchatConfig(self.jid)

	#def deleteUser(self,jid,nick):
		#user=self.main.getGroupChatMember(jid,unicode(nick))
		#parent=user.parent()
		#parent.takeChild(int(parent.indexOfChild(user)))
		#self.main.groupchat[jid][1].remove(user)
		#self.refreshStats()

	def getUserItems(self,name):
		items=self.ui.users.findItems(unicode(name), QtCore.Qt.MatchFixedString| QtCore.Qt.MatchCaseSensitive|QtCore.Qt.MatchRecursive,0)
		if len(items)!=0:
			return items
		return []

	def addRole(self,role,name):
		self.roles[role]=QtGui.QTreeWidgetItem(self.ui.users)
		self.roles[role].setText(0,unicode(name))
		self.roles[role].setText(1,unicode(name))
		self.ui.users.setItemExpanded(self.roles[role],True)
		self.ui.users.setItemHidden(self.roles[role],True)

	def refreshStats(self):
		for k,v in self.roles.iteritems():
			v.setText(0,unicode(v.text(1))+" ("+str(v.childCount())+")")
			if int(v.childCount())>0:
				self.ui.users.setItemHidden(v,False)

	def isUser(self,nick):
		if len(self.getUserItems(nick))==0:
			return False
		return True

	def removeUser(self,nick):
		item=self.getUserItems(nick)[0]
		parent=item.parent()
		parent.takeChild(int(parent.indexOfChild(item)))
		self.refreshStats()

	def editUser(self,nick,status,role=None,affiliation=None):
		if not self.connecting.isHidden():
			self.connecting.hide()
		new=False
		if self.isUser(unicode(nick))==False:
			new=True
			if self.roles.has_key(role):
				item=QtGui.QTreeWidgetItem(self.roles[role])
			else:
				item=QtGui.QTreeWidgetItem(self.ui.users)
			item.setText(0,unicode(nick))
			self.colors.append(item)
		else:
			item=self.getUserItems(nick)[0]
			if item.parent()!=self.roles[role]:
				self.removeUser(nick)
				new=True
				if self.roles.has_key(role):
					item=QtGui.QTreeWidgetItem(self.roles[role])
				else:
					item=QtGui.QTreeWidgetItem(self.ui.users)
				item.setText(0,unicode(nick))
				self.colors.append(item)


		
		if affiliation=="owner" and self.main.client.groupchats[self.jid].nick==nick:
			self.ui.admin.show()

		#if self.ui.users.verticalScrollBar().isVisible():
			#self.ui.users.setColumnWidth(0,int(self.ui.users.width())-38-int(self.ui.users.verticalScrollBar().width()))
		#else:
			#self.ui.users.setColumnWidth(0,int(self.ui.users.width())-38)

		# Nastaveni stavu
		if status!="None":
			item.setIcon(0,self.main.getIcon(status=status,size="32x32"))
			item.setText(1,self.main.shows[status]+unicode(nick.lower()))
		else:
			item.setIcon(0,self.main.getIcon(status="online",size="32x32"))
			item.setText(1,self.main.shows['online']+unicode(nick.lower()))
			status="online"

		if new:
			item.setIcon(1,QtGui.QIcon("images/32x32/apps/jabbim.png"))
			self.main.client.on_avatarUpdate(self.jid+"/"+unicode(item.text(0)))

		jid=self.jid+"/"+nick
		text='<table><tr>'
		if os.path.isfile(self.main.homeDir+'/avatars/'+unicode(jid).replace("/","%")):
			f=open(self.main.homeDir+'/avatars/'+unicode(jid).replace("/","%"),"rb")
			image = f.read()
			f.close()
			pixmap=QtGui.QPixmap()
			pixmap.loadFromData(image)
			pixmap=QtGui.QIcon(pixmap)
			pixmap=pixmap.pixmap(64,64)
			text+='<td><img src="'+self.main.homeDir+'/avatars/'+unicode(jid).replace("/","%")+'" width="'+str(pixmap.width())+'" height="'+str(pixmap.height())+'"/></td>'
		text+='<td><b>'+self.tr("Name:")+'</b> '+nick+'<br/>'
		if self.main.client.groupchats[self.jid].users[nick].truejid:
			text+='<b>'+self.tr("JID:")+'</b> '+self.main.client.groupchats[self.jid].users[nick].truejid+'<br/>'
		else:
			text+='<b>'+self.tr("JID:")+'</b> '+unicode(self.jid)+'/'+nick+'<br/>'
		text+='<img src="images/16x16/status/jabber-%s.png">' % status # hodilo by se rozlisit k jakymu poatri transportu
		text+='<font size="-1">%s</font><br>' % unicode(self.main.client.groupchats[self.jid].users[nick].status).replace("None","")
		text+="</td></tr></table>"
		item.setToolTip(0,text)

		avatar=item.icon(1)
		if not avatar.isNull():
			avatar=avatar.pixmap(28,28)
			#item.setIcon(1,QtGui.QIcon(avatar))
	
			result=QtGui.QPixmap(32,32)
			result.fill(QtCore.Qt.transparent)
			frame=QtGui.QPixmap("images/32x32/frame.png")
			painter=QtGui.QPainter(result)
			painter.fillRect(0,0,32,32,QtGui.QColor(0,0,0,0))
			painter.drawPixmap((32-avatar.width())/2,(32-avatar.height())/2,avatar)
			icon=self.main.getIcon(status=self.main.icons[unicode(item.text(1))[0]],size="16x16")
			#painter.drawPixmap(0,0,frame)
			
			if icon:
				painter.drawPixmap(16,16,icon.pixmap(16,16))
			painter.end()
			#self.frameAvatar=QtGui.QIcon(result)
		else:
			result=QtGui.QPixmap(32,32)
			result.fill(QtCore.Qt.transparent)
			#frame=QtGui.QPixmap("images/32x32/frame.png")
			painter=QtGui.QPainter(result)
			painter.fillRect(0,0,32,32,QtGui.QColor(0,0,0,0))
			#painter.drawPixmap((32-avatar.width())/2,(32-avatar.height())/2,avatar)
			icon=self.main.getIcon(status=self.main.icons[unicode(item.text(1))[0]],size="16x16")
			#painter.drawPixmap(0,0,frame)
			
			if icon:
				painter.drawPixmap(16,16,icon.pixmap(16,16))
			painter.end()

		item.setIcon(0,QtGui.QIcon(result))


		# Tooltip
		#user.setToolTip('<font color="blue"><b>'+unicode(user.text(2))+'</b></font><hr>'+unicode(e[2].getStatus())+'<br/><b>Jabber ID: </b>'+str(jid)+'')
		# serazeni
		self.ui.users.sortItems (1,QtCore.Qt.AscendingOrder)
		self.refreshStats()

	def setTooltip(self,item,jid):
		#jid=self.jid+"/"+nick
		nick=unicode(jidT.JID(jid).resource)
		status=self.main.client.groupchats[self.jid].users[nick].show
		item=self.getUserItems(nick)[0]
		text='<table><tr>'
		if os.path.isfile(self.main.homeDir+'/avatars/'+unicode(jid).replace("/","%")):
			f=open(self.main.homeDir+'/avatars/'+unicode(jid).replace("/","%"),"rb")
			image = f.read()
			f.close()
			pixmap=QtGui.QPixmap()
			pixmap.loadFromData(image)
			pixmap=QtGui.QIcon(pixmap)
			pixmap=pixmap.pixmap(64,64)
			text+='<td><img src="'+self.main.homeDir+'/avatars/'+unicode(jid).replace("/","%")+'" width="'+str(pixmap.width())+'" height="'+str(pixmap.height())+'"/></td>'
		text+='<td><b>'+self.tr("Name:")+'</b> '+nick+'<br/>'
		if self.main.client.groupchats[self.jid].users[nick].truejid:
			text+='<b>'+self.tr("JID:")+'</b> '+self.main.client.groupchats[self.jid].users[nick].truejid+'<br/>'
		else:
			text+='<b>'+self.tr("JID:")+'</b> '+unicode(self.jid)+'/'+nick+'<br/>'
		text+='<img src="images/16x16/status/jabber-%s.png">' % status # hodilo by se rozlisit k jakymu poatri transportu
		text+='<font size="-1">%s</font><br>' % unicode(self.main.client.groupchats[self.jid].users[nick].status).replace("None","")
		text+="</td></tr></table>"
		item.setToolTip(0,text)

	def loadSmileys(self):
		# loads smileys.conf and makes buttons
		smileys=ConfigObj("smileys.conf",encoding='UTF8')
		self.smileys={}
		for k,v in smileys.iteritems():
			self.smileys[k.replace("<","&lt;").replace(">","&gt;")]=v
		self.s=frame(self,self)
		self.s.setWindowFlags(QtCore.Qt.Popup)
		self.s.hide()
		layout=QtGui.QGridLayout(self.s)
		layout.setMargin(0)
		layout.setSpacing(0)
		added=[]
		x=0
		y=0
		for k,v in smileys.iteritems():
			if added.count(v)==0:
				added.append(v)
				button=QtGui.QToolButton(self)
				action=QtGui.QAction(QtGui.QIcon("images/16x16/emotes/"+v),"",self.s)
				action.setData(QtCore.QVariant(k))
				button.setDefaultAction(action)
				button.setToolTip(str(k))
				QtCore.QObject.connect(button, QtCore.SIGNAL("triggered ( QAction *)"),self.addEmoticon)
				layout.addWidget(button,x,y)
				y+=1
				if y==5:
					y=0
					x+=1
	
	def smileysClicked(self,bool):
		pos=self.ui.smileys.mapToGlobal(QtCore.QPoint(0,0))
		x=pos.x()
		y=pos.y()
		self.s.setGeometry(x-60,y-220, 120, 200)
		if self.s.isVisible():
			self.s.setVisible(False)
		else:
			self.s.setVisible(True)

	def logButton(self,button):
		if button==self.actual:
			self.ui.textEdit.setHtml(self.cache['actual'])
		else:
			time=unicode(button.text())
			self.cache['actual']=self.ui.textEdit.toHtml()
			self.ui.textEdit.setHtml(self.cache[time])

	def textEditWrite(self,text):
		#if self.actual.isChecked():
			cursor=QtGui.QTextCursor(self.ui.textEdit.document())
			cursor.beginEditBlock()
			cursor.movePosition(QtGui.QTextCursor.End)
			
			toEnd=False
			if self.ui.textEdit.verticalScrollBar().value()==self.ui.textEdit.verticalScrollBar().maximum():
				toEnd=True
			for k,v in self.smileys.iteritems():
				text=text.replace(" "+k,' <img src="images/16x16/emotes/'+v+'"/>')
			#cursor.insertHtml(text)
			cursor.insertFragment(QtGui.QTextDocumentFragment.fromHtml(text))
			cursor.endEditBlock()
			if toEnd:
				self.ui.textEdit.verticalScrollBar().setValue(self.ui.textEdit.verticalScrollBar().maximum())
			#f=open("test.html","w")
			#self.main.xmlConsole.ui.xml.append(f.write(unicode(self.ui.textEdit.toHtml()))+"\n\n")
			
			#f.close()
		#else:
			#self.cache['actual']+=text

		#self.lines+=1
		#if self.lines>self.maxLines:
			#self.lines=0
			#self.cache[self.main.now()]=self.ui.textEdit.toHtml()
			#self.ui.textEdit.setHtml("")
			#button=QtGui.QPushButton(self.main.now(),self.ui.logs)
			#button.setCheckable(True)
			#self.ui.logsLayout.addWidget(button)
			#self.buttonGroup.addButton(button)

	def addEmoticon(self,action):
		# add emoticon to the self.ui.line
		data=action.data()
		data=data.toString()
		if self.main.config['chatMode']=="normal":
			cur=self.ui.line.textCursor()
			cur.insertText(" "+data)
			self.ui.line.setTextCursor(cur)
		else:
			for k,v in self.smileys.iteritems():
				data=data.replace(k,' <img src="images/16x16/emotes/'+v+'" />')
			self.ui.line.insertHtml(data)
		self.ui.smileys.setChecked(False)
		self.s.hide()
		self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)

	def sendButtonClicked(self):
		# sends message
		# sends message
		if len(unicode(self.ui.line.toPlainText()))!=0:
			services=unicode(self.ui.line.toPlainText())
			if services.startswith("/google"):
				anchor="http://www.google.com/search?q="+services.replace("/google ","")
				QtGui.QDesktopServices.openUrl(QtCore.QUrl(anchor))
				self.ui.line.clear()
				self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
				return
			if self.main.config['chatMode']=="normal":
				text=unicode(self.ui.line.toPlainText())
				#text=unicode(text, 'utf-8')
				text=unescape(text)
			else:
				text=unicode(self.ui.line.toHtml())
				a=parseString(text)
				for el in a.getElementsByTagName('img'):
					path=el.attributes['src'].split('/')[-1]
					for k,v in self.smileys.iteritems():
						if v==path:
							path=k
					newnode = parseString("<div> "+path+"</div>").documentElement
					el.parentNode.replaceChild(newnode,el)
				for el in a.getElementsByTagName('br'):
					newnode = parseString("<div> "+unichr(2028)+"</div>").documentElement
					el.parentNode.replaceChild(newnode,el)
				b=a.getElementsByTagName('body')
				c=parseString(b[0].toxml())
				text=gatherTextNodes(c)
				text=unicode(text, 'utf-8')
				text=text.replace(unichr(2028),"\n")
				text=unescape(text)
			self.main.client.sendMessage(self.jid, text, 'groupchat')
			self.sent.append(text)
			self.hindex = len(self.sent)
			self.ui.line.clear()
			self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
			if self.main.chat.active==False:
				self.main.client.dispatcher.publishEvent('onActivity')
				self.main.chat.active=True
				self.main.chat.timer.stop()

			#self.ui.line.setMaximumHeight(int(self.ui.line.currentFont().pointSize())+15)

	def tabPressed(self):
		# nick completion
		original=unicode(self.ui.line.toPlainText())
		t=unicode(self.ui.line.toPlainText()).lower()
		text=t
		if len(text)==0:
			return
		cur=self.ui.line.textCursor()
		#cur.select(QtGui.QTextCursor.WordUnderCursor)
		#cur.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.KeepAnchor)
		#self.ui.line.setTextCursor(cur)

		i=0
		newt=""
		for word in text.split(" "):
			if cur.position()>i and cur.position()<=i+1+len(word) and len(word)!=0:
				text=word[0]
				break
			else:
				newt=word+" "
			i=i+1+len(word)
		#text=unicode(cur.selectedText()).lower()
		#text=text[0]
		repeat=False
		users=self.main.client.groupchats[self.jid].users.keys()
		print text
		for i in range(len(users)):
			if unicode(users[i]).lower()[0]==unicode(text).lower() and i>self.name_id:
				#cur=self.ui.line.textCursor()
				#cur.movePosition(QtGui.QTextCursor.End)
				#self.ui.line.setTextCursor(cur)
				#self.ui.line.setPlainText(users[i]+": ")
				cur=self.ui.line.textCursor()
				#cur.clearSelection()
				#cur.removeSelectedText()
				#cur.insertText(users[i]+": ")
				x=0
				newt=""
				pos=0
				for word in original.split(" "):
					if cur.position()>x and cur.position()<=x+1+len(word) and len(word)!=0:
						newt+=users[i]+": "
						pos=x+len(users[i]+": ")
					else:
						newt+=word+" "
					x=x+1+len(word)
				if len(word)==0:
					newt=newt[:-1]
				#cur.movePosition(QtGui.QTextCursor.NextWord, QtGui.QTextCursor.KeepAnchor)

				self.ui.line.setPlainText(newt)
				cur.setPosition(pos)
				self.ui.line.setTextCursor(cur)
				self.name_id=i
				return
			if unicode(users[i]).lower()[:len(text)]==text:
				repeat=True
		self.name_id=-1
		if repeat==True:
			self.tabPressed()
			
