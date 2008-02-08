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
#import filetransfer
from abstractchatwidget import abstractChatWidget,abstractTextView
import addcontact

class textView(abstractTextView):
	"""
	QTextEdit for conversation.
	"""
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

class groupChatWidget(abstractChatWidget):
	def __init__(self,main,jid,jab,nickname,parent=None):
		abstractChatWidget.__init__(self,Ui_groupchatwidget,textView,main,jid,True,parent)
		self.nick = nickname #: MUC Jabber ID
		self.affiliation="" #: user affiliation
		self.role="" #: user role
		# these days depracted, but maybe will be used in future
		self.cache={}
		self.lines=0
		self.maxLines=300
		self.tabWord=None #: when user press Tab, contains word where was Tab pressed
		self.name_id=-1 # for tabPressed
		self.ui.disco_info.hide()
		self.lastMessageFrom=""

		# signals
		QtCore.QObject.connect(self.ui.users, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.userClicked)
		QtCore.QObject.connect(self.ui.users, QtCore.SIGNAL("itemClicked ( QTreeWidgetItem * , int )"),self.userSingleClicked)
		QtCore.QObject.connect(self.ui.users, QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.usersContextMenu)

		# shortcuts
		short=QtGui.QShortcut("tab",self.ui.line)
		QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.tabPressed)
		
		# make roles in users list
		self.roles={} #: list of possible roles [possible role:QtreeWidgetItem]
		self.addRole("participant",self.tr("Participants"))
		self.addRole("moderator",self.tr("Moderators"))
		self.addRole("visitor",self.tr("Visitors"))
		self.ui.users.header().hide()
		self.ui.users.hideColumn(1)
		self.ui.users.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

		# splitter size
		self.ui.splitter.setSizes(list(self.main.config['groupchatSplitSizes1']))
		self.ui.splitter_2.setSizes(list(self.main.config['groupchatSplitSizes2']))
		self.ui.splitter_3.setSizes(list(self.main.config['groupchatSplitSizes3']))

		self.sizes={} #: sizes of avatars of other occupants
		self.colors=[] #: colors of other occupants
		self.invitation=[] #: contains JIDs where is send invitation when first presence from MUC arrived (important for converting chat to groupchat)

		# layout for plugins
		self.flowLayout = QtGui.QHBoxLayout()
		self.flowLayout.setMargin(0)
		self.flowLayout.setSpacing(2)

		# use the same height for all buttons
		self.ui.sendButton.setMinimumHeight(self.ui.sendButton.height())
		self.ui.sendButton.setMaximumHeight(self.ui.sendButton.height())
		self.ui.smileys.setMinimumHeight(self.ui.sendButton.height())
		self.ui.smileys.setMaximumHeight(self.ui.sendButton.height())

		# load plugins buttons
		for key,value in self.main.plugins.iteritems():
			if value['module']:
				self.main.runPluginCommand(value['module'].buildGroupchatWidget,[unicode(self.jid),self.flowLayout,self])

		# make global buttons
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
						
		self.ui.changeNick=QtGui.QToolButton()
		self.ui.changeNick.setIconSize(QtCore.QSize(16,16))
		self.ui.changeNick.setIcon(QtGui.QIcon("images/16x16/actions/edit.png"))
		self.ui.changeNick.setToolTip(self.tr("Change nickname"))
		self.ui.changeNick.setMinimumHeight(self.ui.sendButton.height())
		self.ui.changeNick.setMaximumHeight(self.ui.sendButton.height())
		self.flowLayout.addWidget(self.ui.changeNick)
		QtCore.QObject.connect(self.ui.changeNick, QtCore.SIGNAL("clicked ()"),self.changeNick)
						
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
		self.flowLayout.addStretch()
		self.ui.pluginWidget.setLayout(self.flowLayout)


		self.unread=0 #: number of unread message

		# label showed until first presence arrive
		self.connecting=QtGui.QLabel(self.tr("Connecting to MUC. This can take a few seconds."),self.ui.textEdit)
		self.connecting.adjustSize()

		if self.main.selfAvatar:
			result=self.main.getAvatar(self.main.selfAvatar,size="64x64",frame=True)
			self.ui.selfAvatar.setPixmap(result)
			self.ui.selfAvatar.setMaximumWidth(64)
		else:
			self.ui.selfAvatar.hide()

		self.disco_features = [] #: list of room features
		log.msg("REQUESTING ROOM INFO")
		self._getInfo()

	def _getInfo(self):
		"""
		Gets room disco#info.
		"""
		self.main.client.getDiscoInfo(self.jid, callback=self._infoReceived)

	def changeTopic(self,topic):
		"""
		Called when rooms topic is changed.
		@type topic: unicode
		@param topic: new topic
		"""
		subject=utils.replace_url(topic)
		self.ui.info.setHtml(unicode(subject))

	def _infoReceived(self, *a):
		"""
		Called By pyxl when disco#info is received
		"""
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
		"""
		Shows 'connecting...' QLabel in conversations QTextEdit.
		"""
		pos=self.ui.textEdit.mapToGlobal(QtCore.QPoint(0,0))
		x=pos.x()
		y=pos.y()
		self.connecting.setGeometry((x+self.ui.textEdit.width())/2-self.connecting.width()/2,(y+self.ui.textEdit.height())/2-self.connecting.height()/2, self.connecting.width(), self.connecting.height())
		self.connecting.show()
		
	def addRoles(self):
		"""
		Adds all roles QTreeWidgetItems to users list (self.ui.users).
		"""
		self.addRole("participant",self.tr("Participants"))
		self.addRole("moderator",self.tr("Moderators"))
		self.addRole("visitor",self.tr("Visitors"))

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
			user = None
			if self.main.client.groupchats.has_key(self.jid):
				if self.main.client.groupchats[self.jid].users.has_key(name):
					user = self.main.client.groupchats[self.jid].users[name]
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

			if user != None:
				if user.truejid != None:
					jid = jidT.JID(user.truejid).userhost()
					action=menu.addAction(self.tr("Add to roster"))
					action.setData(QtCore.QVariant([jid, name]))
					action.setIcon(QtGui.QIcon("images/16x16/actions/add-user.png"))
					action.setObjectName("add-user")
			
			action=menu.addAction(self.tr("vCard"))
			action.setData(QtCore.QVariant(jid))
			action.setIcon(QtGui.QIcon("images/16x16/categories/v-card.png"))
			action.setObjectName("vcard")
			
			action=menu.addAction(self.tr("Send file"))
			action.setData(QtCore.QVariant(jid))
			action.setIcon(QtGui.QIcon("images/32x32/actions/upload.png"))
			action.setObjectName("send_file")

			for key,value in self.main.plugins.iteritems():
				if value['module']:
					self.main.runPluginCommand(value['module'].buildGroupchatContactMenu,[menu,jid,user])

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
			self.main.sendFiles(jid)
		elif cmd == 'add-user':
			jid, nick = [unicode(val.toString()) for val in action.data().toList()]
			addcontact.addContactDialog(self.main,self.main, jid = jid, name = nick).show()
			

	def userClicked(self,item,i):
		if item.parent()==None:
			return
		icon=self.main.getIcon(status=self.main.icons[unicode(item.text(1))[0]],size="16x16")
		self.main.chat.addChatTab(self.jid+"/"+unicode(item.text(0)),item.text(0),icon)
		self.main.chat.activate()
	
	def userSingleClicked(self,item,i):
		if item.parent()==None:
			return
		text = unicode(self.ui.line.text)
		if len(text) == 0:
			self.ui.line.setText(unicode(item.text(0))+': ')
			self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
			cur=self.ui.line.textCursor()
			cur.movePosition(QtGui.QTextCursor.End)
			self.ui.line.setTextCursor(cur)
		
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

	def changeNick(self):
		nick, b = QtGui.QInputDialog.getText(self,self.tr("Change nick"),self.tr("Enter new nickname:"), QtGui.QLineEdit.Normal, "")
		if nick and b:
			if nick not in self.main.client.groupchats[self.jid].users.keys():
				self.main.client.sendPresence(to=self.jid+"/"+nick)
				self.main.client.groupchats[self.jid].nick=nick
				self.nick=nick
			else:
				message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",unicode(self.tr("Nickname is used by somebody else.")))
				self.textEditWrite(message)

		self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)

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

	def removeUser(self,nick,codes=[],reason="",actor=None,n=None):
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
		elif u'303' in codes:
			message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",nick+unicode(self.tr(" has been renamed to "))+unicode(n)+".")
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

	def logButton(self,button):
		if button==self.actual:
			self.ui.textEdit.setHtml(self.cache['actual'])
		else:
			time=unicode(button.text())
			self.cache['actual']=self.ui.textEdit.toHtml()
			self.ui.textEdit.setHtml(self.cache[time])
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
					self.nick=services.replace("/nick ","")
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
			elif services.startswith("/leave"):
				tab,tabIndex=self.main.chat.findTab(unicode(self.jid))
				self.main.chat.removeTab(tabIndex, False)
				self.ui.line.clear()
				return
			elif services.startswith("/say"):
				self.ui.line.setPlainText(services.replace("/say ",""))

			elif services.startswith("/") and not services.startswith("/me"):
				try:
					cmd, args = services.split(" ", 1)
					args = args.split(" ")
				except ValueError:
					cmd = services
					args = []
				cmd = cmd[1:]
				self.main.client.dispatcher.publishEvent("onCommand", cmd, args, self, "groupchat")
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

			# get message in Qt html format
			xhtml=self.ui.line.toHtml()
			xhtml,same=self.qtHtmlToXhtml(xhtml,text)
			ret=[]
			if same:
				for key,value in self.main.plugins.iteritems():
					if value['module']:
						ret.append(self.main.runPluginCommand(value['module'].on_groupchatMessageSend,[unicode(self.jid),text,'',"active"]))
				if not False in ret:
					self.main.client.sendMessage(unicode(self.jid),text,'groupchat',composing="active")
			else:
				for key,value in self.main.plugins.iteritems():
					if value['module']:
						ret.append(self.main.runPluginCommand(value['module'].on_groupchatMessageSend,[unicode(self.jid),text,xhtml,"active"]))
				if not False in ret:
					self.main.client.sendMessage(unicode(self.jid),text,'groupchat',xhtml=xhtml,composing="active")

			#self.main.client.sendMessage(self.jid, text, 'groupchat')
			self.sent.append(text)
			self.hindex = len(self.sent)
			#self.ui.line.clear()
			#self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
			self.clearLine()
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
			
