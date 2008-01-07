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
import vcardeditor
from include import utils
import filetransfer 
class flowLayout(QtGui.QLayout):
	def __init__(self, parent=None, margin=1, spacing=1):
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
			#print x,y,item.sizeHint().width(),item.sizeHint().height()
			if not testOnly:
				item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

			x = nextX
			lineHeight = max(lineHeight, item.sizeHint().height())

		return y + lineHeight - rect.y()

class textView(QtGui.QTextEdit):
	def __init__(self,main,parent):
		QtGui.QTextEdit.__init__(self,parent)
		self.parent=main
		self.main=self.parent.main
		self.setMouseTracking(True)
		self.setReadOnly(True)
		self.data=[]
		self.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
		self.setAcceptDrops(True)
		self.setObjectName("chatView")

	def dragEnterEvent(self, event):
		#log.msg('DRAG ENTER')
		if event.mimeData().hasText():
			if self.main.getJid(unicode(event.mimeData().text())):
				event.acceptProposedAction()
			else:
				event.ignore()
		else:
			event.ignore()

	def dragMoveEvent(self, event):
		#log.msg('DRAG MOVE')
		event.acceptProposedAction()

	def dropEvent(self, event):
		if event.mimeData().hasText():
			jid=self.main.getJid(unicode(event.mimeData().text()))
			if not jid:
				event.ignore()
				return
			room=unicode(self.parent.jid)
			reason = self.tr("Hi! I'd love to see you in multichat at ") + room
			self.main.client.sendInvitation(jid.full(), room, reason,cont=True)
			event.acceptProposedAction()
		else:
			event.ignore()



	def mouseMoveEvent(self,event):
		anchor = self.anchorAt(event.pos())
		if len(anchor)!=0:
			self.viewport().setCursor(QtCore.Qt.PointingHandCursor)
		else:
			self.viewport().setCursor(QtCore.Qt.ArrowCursor)
		return QtGui.QTextEdit.mouseMoveEvent(self,event)

	def mousePressEvent(self,event):
		anchor = self.anchorAt(event.pos())
		if event.button()==QtCore.Qt.LeftButton:
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
		#print unicode(text)

		self.data.append(QtCore.QMimeData())
		self.data[-1].setText(unicode(text).replace("&gt;",">").replace("&lt;","<").replace("&amp;","&").replace("&quot;","\""))
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
		self.main.tabWord=None
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
	def __init__(self,main,jid,jab,nickname,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.jab=jab
		self.nick = nickname
		self.ui=Ui_groupchatwidget()
		self.ui.setupUi(self)
		self.ui.disco_info.hide()
		self.main=main
		self.affiliation=""
		self.role=""
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
		self.tabWord=None
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
		self.invitation=[]


		#self.flowLayout = flowLayout()
		self.flowLayout = QtGui.QHBoxLayout()
		self.flowLayout.setMargin(0)
		self.flowLayout.setSpacing(2)

		self.ui.sendButton.setMinimumHeight(self.ui.sendButton.height())
		self.ui.sendButton.setMaximumHeight(self.ui.sendButton.height())

		self.ui.smileys.setMinimumHeight(self.ui.sendButton.height())
		self.ui.smileys.setMaximumHeight(self.ui.sendButton.height())


		for key,value in self.main.plugins.iteritems():
			self.main.runPluginCommand(value.buildGroupchatWidget,[unicode(jidT.JID(self.jid).userhost()),self.flowLayout,self])
		
		self.ui.admin=QtGui.QToolButton()
		self.ui.admin.setIconSize(QtCore.QSize(16,16))
		self.ui.admin.setIcon(QtGui.QIcon("images/32x32/actions/register.png"))
		self.ui.admin.setToolTip(self.tr("Room administration"))
		self.ui.admin.setMinimumHeight(self.ui.sendButton.height())
		self.ui.admin.setMaximumHeight(self.ui.sendButton.height())
		self.flowLayout.addWidget(self.ui.admin)
		QtCore.QObject.connect(self.ui.admin, QtCore.SIGNAL("clicked ()"),self.roomConfigClicked)

		self.ui.clearChat=QtGui.QToolButton()
		self.ui.clearChat.setIconSize(QtCore.QSize(16,16))
		self.ui.clearChat.setIcon(QtGui.QIcon("images/32x32/actions/clear.png"))
		self.ui.clearChat.setToolTip(self.tr("Clear chat"))
		self.ui.clearChat.setMinimumHeight(self.ui.sendButton.height())
		self.ui.clearChat.setMaximumHeight(self.ui.sendButton.height())
		self.flowLayout.addWidget(self.ui.clearChat)
		QtCore.QObject.connect(self.ui.clearChat, QtCore.SIGNAL("clicked ()"),self.clearChat)
						
		self.ui.toggleInfo=QtGui.QToolButton()
		self.ui.toggleInfo.setIconSize(QtCore.QSize(16,16))
		self.ui.toggleInfo.setIcon(QtGui.QIcon("images/16x16/actions/info.png"))
		self.ui.toggleInfo.setCheckable(True)
		self.ui.toggleInfo.setToolTip(self.tr("Show room info"))
		self.ui.toggleInfo.setMinimumHeight(self.ui.sendButton.height())
		self.ui.toggleInfo.setMaximumHeight(self.ui.sendButton.height())
		self.flowLayout.addWidget(self.ui.toggleInfo)
		QtCore.QObject.connect(self.ui.toggleInfo, QtCore.SIGNAL("toggled(bool)"),self.toggleInfo)
						
		self.ui.admin.hide()
		self.ui.admin.hide()

		self.flowLayout.addStretch()

		self.ui.pluginWidget.setLayout(self.flowLayout)


		self.unread=0
		
		self.connecting=QtGui.QLabel(self.tr("Connecting to MUC. This can take a few seconds."),self.ui.textEdit)
		self.connecting.adjustSize()
	
		self.init=""
		if self.main.skin.has_key("on_init"):
			self.init=self.main.skin["on_init"]
		self.ui.textEdit.setHtml("<br/>"+self.init)

		self.disco_features = []
		log.msg("REQUESTING ROOM INFO")
		self._getInfo()
	def _getInfo(self):
		self.main.client.getDiscoInfo(self.jid, callback=self._infoReceived)
		#self.editing=False
		#self.topic=""
		#QtCore.QObject.connect(self.ui.info, QtCore.SIGNAL("cursorPositionChanged()"),self.topicChanged)
		#QtCore.QObject.connect(self.ui.saveTopic, QtCore.SIGNAL("clicked()"),self.topicSaved)
		#QtCore.QObject.connect(self.ui.revertTopic, QtCore.SIGNAL("clicked()"),self.topicReverted)
		#QtCore.QObject.connect(self.ui.editSubject, QtCore.SIGNAL("clicked()"),self.editSubject)

		#self.ui.saveTopic.hide()
		#self.ui.revertTopic.hide()
		#self.ui.editSubject.hide()
		#self.ui.info.setAcceptRichText(False)
		

	#def editSubject(self):
		#self.ui.info.setReadOnly(False)
		#position=int(self.ui.info.textCursor().position())
		#cursor=self.ui.info.textCursor()
		#cursor.setPosition(0)
		#self.ui.info.setTextCursor(cursor)
		#self.topic=unicode(self.ui.info.toPlainText())
		#self.ui.info.clear()
		#self.ui.info.setPlainText(self.topic)
		#cursor=self.ui.info.textCursor()
		#cursor.setPosition(position)
		#self.ui.info.setTextCursor(cursor)
		#self.ui.saveTopic.show()
		#self.ui.revertTopic.show()
		#self.ui.editSubject.hide()
		#self.ui.info.setFocus(QtCore.Qt.MouseFocusReason)


	#def topicReverted(self):
		#self.ui.saveTopic.hide()
		#self.ui.revertTopic.hide()
		#print self.topic
		#topic=utils.replace_url(self.topic)
		#self.ui.info.setHtml(unicode(topic))
		#self.editing=False
		#self.ui.info.setReadOnly(True)
		#self.ui.editSubject.show()

	#def topicSaved(self):
		#print 'save topic'
		#topic=unicode(self.ui.info.toPlainText())
		#self.main.client.sendMessage(self.jid, typ='groupchat',body='/me has set subject to: '+topic,subject=topic)
		#self.ui.saveTopic.hide()
		#self.ui.revertTopic.hide()
		#topic=utils.replace_url(topic)
		#self.ui.info.setHtml(unicode(topic))
		#self.editing=False
		#self.ui.info.setReadOnly(True)
		#self.ui.editSubject.show()
		

	#def topicChanged(self):
		#if self.editing==False and not self.ui.info.isReadOnly():
			#self.editing=True
			#position=int(self.ui.info.textCursor().position())
			#cursor=self.ui.info.textCursor()
			#cursor.setPosition(0)
			#self.ui.info.setTextCursor(cursor)
			#self.topic=unicode(self.ui.info.toPlainText())
			#self.ui.info.clear()
			#self.ui.info.setPlainText(self.topic)
			#cursor=self.ui.info.textCursor()
			#cursor.setPosition(position)
			#self.ui.info.setTextCursor(cursor)
			#self.ui.saveTopic.show()
			#self.ui.revertTopic.show()
		#elif self.editing==False and self.ui.info.isReadOnly() and self.role=='moderator':
			#self.ui.info.setReadOnly(False)

	def changeTopic(self,topic):
		subject=utils.replace_url(topic)
		#QtCore.QObject.disconnect(self.ui.info, QtCore.SIGNAL("cursorPositionChanged()"),self.topicChanged)
		self.ui.info.setHtml(unicode(subject))
		#QtCore.QObject.connect(self.ui.info, QtCore.SIGNAL("cursorPositionChanged()"),self.topicChanged)



	def _infoReceived(self, *a):
		self.disco_features = self.main.client.disco[self.jid][None]["features"]
		features = []
		possible_features = {
				# http://jabber.org/protocol/muc#register
				# http://jabber.org/protocol/muc#roomconfig
				# http://jabber.org/protocol/muc#roominfo
				"muc_hidden":self.tr("Hidden"),
				"muc_membersonly":self.tr("Members only"),
				"muc_moderated":self.tr("Moderated"),
				"muc_nonanonymous":self.tr("Non anonymous"),
				"muc_open":self.tr("Open"),
				"muc_passwordprotected":self.tr("Password protected"),
				"muc_persistent":self.tr("Persistent"),
				"muc_public":self.tr("Public"),
				# muc_rooms
				"muc_semianonymous":self.tr("Semi-anonymous"),
				"muc_temporary":self.tr("Temporary"),
				"muc_unmoderated":self.tr("Unmoderated"),
				"muc_unsecured":self.tr("Unsecured")
				}
		for f in self.disco_features:
			if f in possible_features.keys():
				if not unicode(possible_features[f]) in features:
					features.append(unicode(possible_features[f]))
			else:
				log.msg("Unknown room feature: %s" % f)
		
		self.ui.disco_info.setText(unicode(", ".join(features)))
		log.msg("ROOM INFO RECEIVED")
		log.msg(unicode(self.disco_features))
		
	
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
		if not item:
			return
		name=unicode(item.text(0)) # get contact name
		menu=QtGui.QMenu(self.ui.users) # make menu
		jid="%s/%s" % (self.jid, name)
		if item.parent()!=None:
			affiliation=""
			role=""
			if self.main.client.groupchats.has_key(self.jid):
				if self.main.client.groupchats[self.jid].users.has_key(name):
					affiliation=self.main.client.groupchats[self.jid].users[name].affiliation
					role=self.main.client.groupchats[self.jid].users[name].role
			
			affiliations={'none':0,'member':1,'admin':2,'owner':3}
			
			separator=False
			if (self.role=="moderator" or self.affiliation=="owner") and affiliations[self.affiliation]>affiliations[affiliation]:
				action=menu.addAction(self.tr("Kick"))
				action.setData(QtCore.QVariant(name))
				action.setObjectName("kick")
				separator=True
			if (self.affiliation=="admin" or self.affiliation=="owner") and affiliations[self.affiliation]>affiliations[affiliation]:
				action=menu.addAction(self.tr("Ban"))
				action.setData(QtCore.QVariant(name))
				action.setObjectName("ban")
				separator=True
			if separator:
				menu.addSeparator()
			
			separator=False

			if self.affiliation=="owner":
				if affiliation=='owner':
					action=menu.addAction(self.tr("Revoke ownership"))
					action.setData(QtCore.QVariant(name))
					action.setObjectName("revoke_owner")
					separator=True
				else:
					action=menu.addAction(self.tr("Grant ownership"))
					action.setData(QtCore.QVariant(name))
					action.setObjectName("grant_owner")
					separator=True

				if affiliation=='admin':
					action=menu.addAction(self.tr("Revoke admin"))
					action.setData(QtCore.QVariant(name))
					action.setObjectName("revoke_admin")
					separator=True
				else:
					action=menu.addAction(self.tr("Grant admin"))
					action.setData(QtCore.QVariant(name))
					action.setObjectName("grant_admin")
					separator=True
			if affiliations[self.affiliation]>affiliations[affiliation]:
				if self.affiliation=="admin" or self.affiliation=="owner":
					if (affiliation=='member' or affiliation=='none') and role=='moderator':
						action=menu.addAction(self.tr("Revoke moderator"))
						action.setData(QtCore.QVariant(name))
						action.setObjectName("revoke_moderator")
						separator=True
					elif role!='moderator':
						action=menu.addAction(self.tr("Grant moderator"))
						action.setData(QtCore.QVariant(name))
						action.setObjectName("grant_moderator")
						separator=True
					
					if affiliation=='member':
						action=menu.addAction(self.tr("Revoke membership"))
						action.setData(QtCore.QVariant(name))
						action.setObjectName("revoke_member")
						separator=True
					else:
						action=menu.addAction(self.tr("Grant membership"))
						action.setData(QtCore.QVariant(name))
						action.setObjectName("grant_member")
						separator=True
				if self.role=='moderator':
					if "muc_moderated" in self.disco_features:
						if affiliation=='participant':
							action=menu.addAction(self.tr("Revoke voice"))
							action.setData(QtCore.QVariant(name))
							action.setObjectName("revoke_voice")
							separator=True
						else:
							action=menu.addAction(self.tr("Grant voice"))
							action.setData(QtCore.QVariant(name))
							action.setObjectName("grant_voice")
							separator=True

			if separator:
				menu.addSeparator()

			
			action=menu.addAction(self.tr("vCard"))
			action.setData(QtCore.QVariant(jid))
			action.setIcon(QtGui.QIcon("images/16x16/categories/v-card.png"))
			action.setObjectName("vcard")
			
			action=menu.addAction(self.tr("Send file"))
			action.setData(QtCore.QVariant(jid))
			action.setIcon(QtGui.QIcon("images/32x32/actions/upload.png"))
			action.setObjectName("send_file")

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
		elif cmd=='ban':
			name=unicode(action.data().toString())
			if self.main.client.groupchats.has_key(self.jid):
				reason,b=QtGui.QInputDialog.getText(self,self.tr("Reason"),self.tr("Enter reason:"), QtGui.QLineEdit.Normal, "")
				reason=unicode(reason)
				# if user set new name of group
				if b==True:
					self.main.client.groupchats[self.jid].setAffiliation(name, 'outcast',  reason)
		elif cmd=='grant_moderator':
			name=unicode(action.data().toString())
			if self.main.client.groupchats.has_key(self.jid):
				self.main.client.groupchats[self.jid].setRole(name, 'moderator')
		elif cmd=='revoke_moderator':
			name=unicode(action.data().toString())
			if self.main.client.groupchats.has_key(self.jid):
				self.main.client.groupchats[self.jid].setRole(name, 'participant')
		elif cmd=='grant_voice':
			name=unicode(action.data().toString())
			if self.main.client.groupchats.has_key(self.jid):
				self.main.client.groupchats[self.jid].setRole(name, 'participant')
		elif cmd=='revoke_voice':
			name=unicode(action.data().toString())
			if self.main.client.groupchats.has_key(self.jid):
				self.main.client.groupchats[self.jid].setRole(name, 'visitor')
		elif cmd=='grant_member':
			name=unicode(action.data().toString())
			if self.main.client.groupchats.has_key(self.jid):
				self.main.client.groupchats[self.jid].setAffiliation(name, 'member')
		elif cmd=='revoke_member':
			name=unicode(action.data().toString())
			if self.main.client.groupchats.has_key(self.jid):
				self.main.client.groupchats[self.jid].setAffiliation(name, 'none')
		elif cmd=='grant_owner':
			name=unicode(action.data().toString())
			if self.main.client.groupchats.has_key(self.jid):
				self.main.client.groupchats[self.jid].setAffiliation(name, 'owner')
		elif cmd=='revoke_owner':
			name=unicode(action.data().toString())
			if self.main.client.groupchats.has_key(self.jid):
				self.main.client.groupchats[self.jid].setAffiliation(name, 'none')
		elif cmd=='grant_admin':
			name=unicode(action.data().toString())
			if self.main.client.groupchats.has_key(self.jid):
				self.main.client.groupchats[self.jid].setAffiliation(name, 'admin')
		elif cmd=='revoke_admin':
			name=unicode(action.data().toString())
			if self.main.client.groupchats.has_key(self.jid):
				self.main.client.groupchats[self.jid].setAffiliation(name, 'none')
		elif cmd == "vcard":
			jid=action.data()
			jid=unicode(jid.toString())
			self.ve=vcardeditor.vcardEditorDialog(self.main,jid,self,False)
			self.ve.show()
		elif cmd == "send_file":
			jid=unicode(action.data().toString())

			file=QtGui.QFileDialog.getOpenFileNames(self,"Choose file")
			file=list(file)
			if len(file)!=0:
				new=[]
				for f in file:
					new.append(unicode(f))
				file=new
				self.dialog=filetransfer.filetransferDialog(self.main,file,jid)
				self.dialog.show()
			

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

	def toggleInfo(self, b):
		log.msg("Info toggled:"+`b`)
		if b:
			self._getInfo()
			self.ui.disco_info.show()
			self.ui.toggleInfo.setToolTip(self.tr("Hide room info"))
		else:
			self.ui.disco_info.hide()
			self.ui.toggleInfo.setToolTip(self.tr("Show room info"))
	def roomConfigClicked(self):
		nick=self.main.client.groupchats[self.jid].nick
		if self.main.client.groupchats[self.jid].users[nick].affiliation=="owner":
			d=self.main.client.getMUCConfig(self.jid)
			d.addCallback(self._onRoomConfig)
		elif self.role=='moderator':
			self.dialog=groupchatAdminDialog(self.main,self.jid,None,self,subject=unicode(self.ui.info.toPlainText()))
			self.dialog.show()

	def _onRoomConfig(self,data):
		jid=data[0]
		form=data[1]
		if form!=None:
			self.dialog=groupchatAdminDialog(self.main,jid,form,self,subject=unicode(self.ui.info.toPlainText()))
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

	def getUserName(self,jid):
		#if self.main.client.groupchats[self.jid].users[nick].truejid:
		for nick,user in self.main.client.groupchats[self.jid].users.iteritems():
			if user.truejid==jid:
				return nick
		return jid

	def addRole(self,role,name):
		self.roles[role]=QtGui.QTreeWidgetItem(self.ui.users)
		self.roles[role].setBackground(0,QtGui.QBrush(self.ui.users.palette().color(QtGui.QPalette.AlternateBase)))
		self.roles[role].setIcon(0,QtGui.QIcon("images/32x32/categories/system-users.png"))
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

	def removeUser(self,nick,codes=[],reason="",actor=None):
		nick=unicode(nick)
		if self.main.client.groupchats[self.jid].nick==nick:
			if u'307' in codes:
				self.ui.line.setEnabled(False)
				self.ui.users.clear()
				self.addRoles()
				if actor and len(reason)!=0:
					name=self.getUserName(actor)
					message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",unicode(self.tr("You have been kicked from the room by %s. Reason: %s.")) % (unicode(name),unicode(reason)))
				elif actor:
					name=self.getUserName(actor)
					message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",unicode(self.tr("You have been kicked from the room by %s.")) % unicode(name))
				elif len(reason)!=0:
					message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",unicode(self.tr("You have been kicked from the room. Reason: %s.")) % unicode(reason))
				else:
					message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",unicode(self.tr("You have been kicked from the room.")))
				self.textEditWrite(message)
				return
			elif u'301' in codes:
				self.ui.line.setEnabled(False)
				self.ui.users.clear()
				self.addRoles()
				message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",unicode(self.tr("You have been banned for the room.")))
				self.textEditWrite(message)
				return
		if u'307' in codes:
			message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",nick+unicode(self.tr(" has been kicked from this room.")))
			self.textEditWrite(message)
		elif u'301' in codes:
			message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",nick+unicode(self.tr(" has been banned for this room.")))
			self.textEditWrite(message)

		item=self.getUserItems(nick)[0]
		parent=item.parent()
		parent.takeChild(int(parent.indexOfChild(item)))
		self.refreshStats()

	def editUser(self,nick,status,role=None,affiliation=None):
		if not self.connecting.isHidden():
			self.connecting.hide()
			for inv in self.invitation:
				reason = self.tr("Hi! I'd love to see you in multichat at ") + self.jid
				self.main.client.sendInvitation(inv, self.jid,reason, cont=True)
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


		if self.main.client.groupchats[self.jid].nick==nick:
			self.affiliation=affiliation
			self.role=role
			#print "affiliation:",affiliation,"role:",role
			if affiliation=="owner":
				self.ui.admin.show()
			if role=='moderator':
				#self.ui.info.setReadOnly(False)
				self.ui.admin.show()
				#self.ui.editSubject.show()
		

		#if self.ui.users.verticalScrollBar().isVisible():
			#self.ui.users.setColumnWidth(0,int(self.ui.users.width())-38-int(self.ui.users.verticalScrollBar().width()))
		#else:
			#self.ui.users.setColumnWidth(0,int(self.ui.users.width())-38)

		# Nastaveni stavu
		status = unicode(status)
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
			#avatar=avatar.pixmap(28,28)
			result=self.main.getAvatar(avatar,size="32x32",frame=False,status=self.main.icons[unicode(item.text(1))[0]])
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
			elif services.startswith("/nick "):
				if not self.main.client.groupchats[self.jid].users.has_key(services.replace("/nick ","")):
					self.main.client.sendPresence(to=self.jid+"/"+services.replace("/nick ",""))
					self.main.client.groupchats[self.jid].nick=services.replace("/nick ","")
				else:
					message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",unicode(self.tr("Nickname is used by somebody else.")))
					self.textEditWrite(message)
				self.ui.line.clear()
				self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
				return
			elif services.startswith("/join "):
				#self.main.client.sendPresence(to=self.jid+"/"+services.replace("/nick ",""))
				#self.main.client.groupchats[self.jid].nick=services.replace("/nick ","")
				if self.main.chat.addGroupChatTab(services.replace("/join ",""),self.main.client.groupchats[self.jid].nick):
					self.main.client.joinGC(services.replace("/join ",""), self.main.client.groupchats[self.jid].nick)
				self.ui.line.clear()
				#self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
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
				text=word
				break
			else:
				newt=word+" "
			i=i+1+len(word)
		if not self.tabWord:
			self.name_id=-1
			self.tabWord=text
		
		#text=unicode(cur.selectedText()).lower()
		#text=text[0]
		repeat=False
		users=self.main.client.groupchats[self.jid].users.keys()
		users.remove(self.nick)
		#print text
		for i in range(len(users)):
			if unicode(users[i]).lower()[:len(self.tabWord)]==unicode(self.tabWord).lower():
				if i>self.name_id:
					#cur=self.ui.line.textCursor()
					#cur.movePosition(QtGui.QTextCursor.End)
					#self.ui.line.setTextCursor(cur)
					#self.ui.line.setPlainText(users[i]+": ")
					cur=self.ui.line.textCursor()
					#cur.clearSelection()
					#cur.removeSelectedText()
					#cur.insertText(users[i]+": ")
					x=0 #first letter of word index in string
					newt=""
					pos=0
					ending = " " #ending of the sugested nick, set to space by default, example "Sef "
					for word in original.split(" "):
						if cur.position()>x and cur.position()<=x+1+len(word) and len(word)!=0:
							if x == 0: #if the nick is the first word in string, ending will be ": ", example - "Sef: "
								ending = ": "
							newt+=users[i]+ending
							pos=x+len(users[i]+ending)
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
				#if unicode(users[i]).lower()[:len(text)]==text:
					#repeat=True
				repeat=True
		self.name_id=-1
		if repeat==True:
		#if len(users)!=0:
			self.tabPressed()
			
