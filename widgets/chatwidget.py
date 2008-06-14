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
from chatwidget_ui import *
from configobj import ConfigObj
#from palette import *
import urllib,re,os
from twisted.web.microdom import *
from twisted.web.domhelpers import gatherTextNodes
import filetransfer
from pyxl import jid as jidT
import time
from include import utils
from abstractchatwidget import abstractChatWidget,abstractTextView
import sys
class FTAskWidget(QtGui.QWidget):
	def __init__(self,file,event,chatwidget,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.setObjectName("FTAskWidget")
		self.chatwidget=chatwidget
		#self.main=main
		self.event=event
		self.gridlayout = QtGui.QGridLayout(self)
		self.gridlayout.setMargin(0)
		self.gridlayout.setSpacing(0)
		self.gridlayout.setObjectName("gridlayout")
		
		self.label=QtGui.QLabel(" <b>"+file+"</b> "+self.tr("Receive this file?"),self)
		self.label.setWordWrap(True)
		self.preview=QtGui.QLabel(self)
		self.preview.hide()
		self.yes=QtGui.QPushButton(self.tr('Yes'),self)
		self.no=QtGui.QPushButton(self.tr('No'),self)
		self.gridlayout.addWidget(self.label,0,0,1,2)
		self.gridlayout.addWidget(self.preview,1,0,1,2)
		self.gridlayout.addWidget(self.yes,2,0,1,1)
		self.gridlayout.addWidget(self.no,2,1,1,1)
		
		QtCore.QObject.connect(self.yes,QtCore.SIGNAL("clicked()"),self.accept)
		QtCore.QObject.connect(self.no,QtCore.SIGNAL("clicked()"),self.reject)

	def setPreview(self,pixmap):
		self.preview.show()
		self.preview.setPixmap(pixmap)

	def accept(self,b=None):
		self.event.submitClicked()
		self.chatwidget.ui.ftwidget.layout().removeWidget(self)
		self.setParent(None)
		self.deleteLater()

	def reject(self,b=None):
		self.event.closeClicked()
		self.chatwidget.ui.ftwidget.layout().removeWidget(self)
		self.setParent(None)
		self.deleteLater()


class FTWidget(QtGui.QWidget):
	def __init__(self,file,item,main,sid,parent=None,stats="",download=False):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.setObjectName("FTWidget")
		self.item=item
		self.main=main
		self.complete=False
		self.sid=sid
		self.gridlayout = QtGui.QGridLayout(self)
		self.gridlayout.setMargin(0)
		self.gridlayout.setSpacing(0)
		self.gridlayout.setObjectName("gridlayout")
	
		self.gridlayout1 = QtGui.QGridLayout()
		self.gridlayout1.setMargin(0)
		self.gridlayout1.setSpacing(6)
		self.gridlayout1.setObjectName("gridlayout1")

		self.label_2 = QtGui.QLabel(file,self)
		self.label_2.setObjectName("label_2")
		self.label_2.setTextFormat(QtCore.Qt.RichText)
		self.label_2.setWordWrap(True)


		spacerItem = QtGui.QSpacerItem(16,18,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
		#self.hboxlayout.addStretch()
		
		#self.closeButton = QtGui.QPushButton(self)
		#self.closeButton.setMaximumSize(16,16)
		#self.closeButton.setObjectName("closeButton")
		#self.closeButton.setFlat(True)
		#self.closeButton.setIcon(QtGui.QIcon("images/16x16/actions/process-stop.png"))
		#self.hboxlayout.addWidget(self.closeButton)

		#QtCore.QObject.connect(self.closeButton,QtCore.SIGNAL("clicked()"),self.closeClicked)

		#self.gridlayout1.addLayout(self.hboxlayout,0,0,1,1)
	
		self.stats = QtGui.QLabel(stats,self)

		self.progressBar = QtGui.QProgressBar(self)
	
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(1))
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
		self.progressBar.setSizePolicy(sizePolicy)
		self.progressBar.setProperty("value",QtCore.QVariant(0))
		self.progressBar.setOrientation(QtCore.Qt.Horizontal)
		self.progressBar.setObjectName("progressBar")
		self.gridlayout1.addWidget(self.stats,1,0,1,2)
		self.gridlayout1.addWidget(self.progressBar,2,0,1,2)
		if not download:
			self.gridlayout1.addWidget(self.label_2,3,0,1,2)
		self.gridlayout.addLayout(self.gridlayout1,0,0,1,1)
		self.gridlayout.setMargin(1)
		self.gridlayout.setSpacing(0)
		self.gridlayout1.setMargin(1)
		self.gridlayout1.setSpacing(0)
		self.setMinimumHeight(60)

	def reinit(self,file,item,main,sid,parent=None,stats=""):
		self.complete=False
		self.sid=sid
		self.stats.setText(stats)
		self.item=item
		self.progressBar.setProperty("value",QtCore.QVariant(0))
		self.label_2.setText(file)

		self.setMinimumHeight(60)

	def closeClicked(self):
		if self.item:
			if not self.complete:
				try:
					self.main.client.ft[self.sid].protocol.unregisterProducer()
					self.complete=None
				except:
					self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.item))
			elif self.complete==True:
				self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.item))

class flowLayout(QtGui.QLayout):
	"""
	Flow layout from Qt4 examples. Used for plugins buttons.
	"""
	def __init__(self, parent=None, margin=0, spacing=-1):
		QtGui.QLayout.__init__(self, parent)

		if parent is not None:
			self.setMargin(2)
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

class chatWidget(abstractChatWidget):
	def __init__(self,main,jid,parent=None,name=""):
		jidt=jidT.JID(jid)
		self.name=name
		self.main=main
		#try:
			#xhtml=main.client.roster['users'][jidt.userhost()].resources[jidt.resource].hasFeature('http://jabber.org/protocol/xhtml-im') #: True if user supports xhtml, otherwise False
		#except:
			#xhtml=False
		xhtml=main.client.hasFeature(jid,'http://jabber.org/protocol/xhtml-im')
		self.typ="chat"
		# get users avatar
		self.file=""
		if self.main.client.avatarDef.has_key(unicode(jidT.JID(jid).userhost())):
			self.file=self.main.realHomeDir+'/avatars/'+str(self.main.client.avatarDef[unicode(jidT.JID(jid).userhost())]) #: path to users avatar
		elif self.main.client.avatarDef.has_key(unicode(jidT.JID(jid).full())):
			self.file=self.main.realHomeDir+'/avatars/'+str(self.main.client.avatarDef[unicode(jidT.JID(jid).full())]) #: path to users avatar
		self.avatarHeight=32 #: avatars height
		if not os.path.isfile(self.file):
			# use default avatar if users avatar doesn't exist
			self.file=os.getcwd()+"/images/32x32/apps/jabbim.png"
		else:
			# change size of users avatar
			# TODO: size should be changed by skin...
			pixmap=QtGui.QPixmap(self.file).scaledToWidth(32)
			self.avatarHeight=int(pixmap.height())
		abstractChatWidget.__init__(self,Ui_chatwidget,abstractTextView,main,jid,xhtml,parent)

		self.metaJids=[]
		# set splitters sizes
		#self.ui.splitter.setSizes(list(self.main.config['chatSplitterSizes']))
		self.ui.splitter.setSizes([800,64])
		self.ui.splitter_2.setSizes(list(self.main.config['chatSplitter2Sizes']))
		widget=self.ui.splitter_2.widget(1)
		widget.setMaximumWidth(128)
		
		# Maximum width of avatar Widget
		self.ui.avatar.setMaximumWidth(128)
		self.ui.avatar.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		QtCore.QObject.connect(self.ui.avatar,QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.contactMenu)
		self.noColor=True
		self.lastMessageFrom=""
		

		# get self avatar
		self.selfHeight=32 #: height of self avatar
		f=""
		if self.main.client.avatarDef.has_key(self.main.client.jid.userhost()):
			f=self.main.realHomeDir+'/avatars/'+str(self.main.client.avatarDef[self.main.client.jid.userhost()])
		if not os.path.isfile(f):
			self.selfFile="images/32x32/apps/jabbim.png"
		else:
			pixmap=QtGui.QPixmap(f).scaledToWidth(32)
			self.selfFile=f
			self.selfHeight=int(pixmap.height())

		# plugins buttons
		self.flowLayout = flowLayout()
		for key,value in self.main.plugins.iteritems():
			if value['module']:
				self.main.runPluginCommand(value['module'].buildChatWidget,[unicode(self.jid),self.flowLayout,self])
		hasFeature=False
		self.ui.metaLabel.hide()
		self.ui.metaButton.hide()
		
		# sendFile buttons
		self.ui.sendFile=QtGui.QToolButton()
		self.ui.sendFile.setIconSize(QtCore.QSize(16,16))
		self.ui.sendFile.setIcon(QtGui.QIcon("images/32x32/actions/upload.png"))
		self.ui.sendFile.setToolTip(self.tr("Send file"))
		self.ui.sendFile.hide()
		self.registerFeatureForWidget('http://jabber.org/protocol/si/profile/file-transfer',self.ui.sendFile)		
		self.flowLayout.addWidget(self.ui.sendFile)
		QtCore.QObject.connect(self.ui.sendFile, QtCore.SIGNAL("clicked ()"),self.sendFiles)

		if self.main.client.groupchats.has_key(jidt.userhost()):
			#print "features:",self.main.client.groupchats[jidt.userhost()].users[jidt.resource].features
			hasFeature='http://jabber.org/protocol/si/profile/file-transfer' in self.main.client.groupchats[jidt.userhost()].users[jidt.resource].features
			self.ui.resourceButton.hide()
			self.ui.resourceLabel.hide()
			if hasFeature:
				self.ui.sendFile.show()
		else:
			if main.client.roster['users'].has_key(jidt.userhost()):
				self.buildResourceMenu()
				self.buildMetaMenu()

		self.ui.pluginWidget.setLayout(self.flowLayout)
		self.ui.ftwidget.setLayout(QtGui.QVBoxLayout())
		self.filetransfer={}
		
		result=self.main.getAvatar(self.main.client.jid.userhost(),size="64x64",frame=True)
		if result:
			print 'COUNT1',sys.getrefcount(result)
			self.blabla=result
			self.ui.selfAvatar.setPixmap(result)
			print 'COUNT2',sys.getrefcount(result)
			self.ui.selfAvatar.setMaximumWidth(64)
		else:
			self.ui.selfAvatar.hide()
			self.ui.lineWidget.setMinimumSize(100,64)
		self.refreshToolTip()

	def refreshLabel(self):
		print "ref"
		text="<font size=\"3\"><b>"+self.name+"</b></font>"
		contact=self.main.client.getContactByJid(self.jid)
		if not contact:
			self.ui.label.setText(text)
			return
		mood = contact.getPEP('http://jabber.org/protocol/mood')
		if mood != None:
			t = ''
			m = txt = ''
			for el in mood.elements():
				if el.name == 'text':
					txt = unicode(el)
				else:
					m = self.main.moods.get(el.name)
					if self.main.moodIcons.has_key(el.name):
						icon="<img src=\"%s\" />" % self.main.moodIcons[el.name].src
					else:
						icon=""
			if txt != '':
				t = m+ ' - %s'%txt
			else:
				t = m
			text+='<br />%s <font size="-1">&nbsp; %s</font>' % (icon,t)
			if self.main.config['showMoodChanges']=='True':
				user=unicode(self.main.ui.roster.getNameByJID(self.jid))
				message=icon+"&nbsp;"+user+" "+unicode(self.tr("is now"))+" "+ t
				self.textEditWrite(self.main.skin["status_message"].replace("[time]",self.main.now()).replace('[message]',unicode(message)))
		tune = contact.getPEP('http://jabber.org/protocol/tune')
		if type(tune) == list:
			for x in tune:
				print x
		elif tune!=None:
			artist = title = ''
			for el in tune.elements():
				if el.name == 'artist':
					artist = unicode(el)
				elif el.name == 'title':
					title = unicode(el)
			t = '%s: %s'%(artist, title)
			if len(t.strip())>1:
				text+='<br /><img src="images/22x22/icons/headphones.png" /><font size="-1">&nbsp; %s</font>' % (t) #ikonka se este muze menit ;)
				if self.main.config['showTuneChanges']=='True':
					user=unicode(self.main.ui.roster.getNameByJID(self.jid))
					message='<img src="images/22x22/icons/headphones.png" />&nbsp;'+user+" "+unicode(self.tr("is now listening:"))+" "+ t
					self.textEditWrite(self.main.skin["status_message"].replace("[time]",self.main.now()).replace('[message]',unicode(message)))

		self.ui.label.setText(text)

	def contactMenu(self,pos):
		items=self.main.ui.roster.getUserItems(self.main.getJid(self.jid).userhost())
		if len(items)==0:
			contactMenu=self.main.ui.roster.buildJidMenu(self.jid)
		else:
			item=items[0]
			group=item.group
			jid=item.jid
			contactMenu=self.main.ui.roster.buildContactMenu(unicode(jid),group)
		contactMenu.popup(self.ui.avatar.mapToGlobal(pos))

	def hasMetacontact(self,metacontact):
		return metacontact in self.metaJids

	def buildMetaMenu(self):
		jidt=self.main.getJid(self.jid)
		if self.main.client.roster['users'][jidt.userhost()].tag!=None:
			self.metaMenu=QtGui.QMenu(self.ui.metaButton)
			self.ui.metaLabel.show()
			self.ui.metaButton.show()
			meta=[]
			tag=self.main.client.roster['users'][jidt.userhost()].tag
			for jid,user in self.main.client.roster['users'].iteritems():
				if user.tag==tag:
					meta.append(jid)
			self.metaJids=meta
			for mJid in meta:
				
				name=self.main.ui.roster.getNameByJID(mJid)
				icon=self.main.ui.roster.getIconByJID(mJid)
				action=self.metaMenu.addAction(icon,name)
				action.setData(QtCore.QVariant(unicode(mJid)))
				if mJid==jidt.userhost():
					self.ui.metaButton.setText(action.text())
					self.ui.metaButton.setIcon(action.icon())
			self.metaMenu.connect(self.metaMenu, QtCore.SIGNAL("triggered ( QAction * )"),self.metaMenuTriggered)
			self.ui.metaButton.setMenu(self.metaMenu)


	def buildResourceMenu(self):
		jidt=self.main.getJid(self.jid)
		self.resourceMenu=QtGui.QMenu(self.ui.resourceButton)
		#action=self.resourceMenu.addAction(self.tr("Automatic"))
		#self.ui.resourceButton.setText(action.text())
		#try:
			#hasFeature=self.main.client.roster['users'][jidt.userhost()].resources[self.main.client.roster['users'][jidt.userhost()].getHighestResource()].hasFeature('http://jabber.org/protocol/si/profile/file-transfer')
		#except:
			#hasFeature=False
		count=0
		found=False
		for name,resource in self.main.client.roster['users'][jidt.userhost()].resources.iteritems():
			if name:
				count+=1
				action=self.resourceMenu.addAction(self.main.getIcon(unicode(jidt.userhost()),status=resource.show),name)
				if jidt.resource==name:
					self.ui.resourceButton.setText(action.text())
					self.ui.resourceButton.setIcon(action.icon())
					found=True
					#try:
						#hasFeature=self.main.client.roster['users'][jidt.userhost()].resources[name].hasFeature('http://jabber.org/protocol/si/profile/file-transfer')
					#except:
						#hasFeature=False
		if not found:
			self.ui.resourceButton.setText(self.tr("Automatic"))
			self.jid=self.main.getJid(self.jid).userhost()
			self.parent.jid=self.jid
		#if hasFeature:
			#self.ui.sendFile.show()
		#else:
			#self.ui.sendFile.hide()
		self.showFeaturedWidgets()
		if count<2:
			self.ui.resourceButton.hide()
			self.ui.resourceLabel.hide()
		else:
			self.ui.resourceButton.setEnabled(True)
			self.ui.resourceButton.show()
			self.ui.resourceLabel.show()
		self.resourceMenu.connect(self.resourceMenu, QtCore.SIGNAL("triggered ( QAction * )"),self.resourceMenuTriggered)
		self.ui.resourceButton.setMenu(self.resourceMenu)

	def metaMenuTriggered(self,action):
		self.ui.metaButton.setText(action.text())
		self.ui.metaButton.setIcon(action.icon())
		jidt=self.main.getJid(unicode(action.data().toString()))
		res = self.main.client.roster['users'][jidt.userhost()].getHighestResource()
		if res:
			jidt.resource=unicode(res)
		self.jid=unicode(jidt.full())
		self.parent.jid=self.jid
		self.buildResourceMenu()
		self.parent.tabName=unicode(action.text())
		self.parent.ic=action.icon()
		currentIndex=self.main.chat.ui.chatTab.currentIndex()
		self.main.chat.ui.chatTab.setTabIcon(currentIndex,self.parent.ic)
		self.main.chat.ui.chatTab.setTabText(currentIndex,self.parent.tabName)
		self.main.chat.setWindowTitle(unicode(self.main.chat.ui.chatTab.tabText(currentIndex)).replace("&",""))

	def resourceMenuTriggered(self,action):
		self.ui.resourceButton.setText(action.text())
		self.ui.resourceButton.setIcon(action.icon())
		jid=self.main.getJid(self.jid)
		if action.text()==self.tr("Automatic"):
			jid.resource=None
		else:
			jid.resource=unicode(action.text())
		self.jid=jid.full()
		self.parent.jid=self.jid
	
	def refreshToolTip(self):
		if self.main.client:
			text = self.main.getToolTip(self.jid)
			self.ui.avatar.setToolTip(text)

	def sendFiles(self):
		"""
		Shows filetransfer dialog and sends files to user who chats with us.
		"""
		self.main.sendFiles(self.jid)
		#file=QtGui.QFileDialog.getOpenFileNames(self,"Choose file")
		#file=list(file)
		#if len(file)!=0:
			#new=[]
			#for f in file:
				#new.append(unicode(f))
			#file=new
			## show filetransfer dialog and send files
			#self.dialog=filetransfer.filetransferDialog(self.main,file,self.jid)
			#self.dialog.show()
	
	def sendButtonClicked(self):
		"""
		Sends message writed in self.ui.line or call command if message starts with "/".
		"""
		if len(unicode(self.ui.line.toPlainText()))!=0:
			# execute commands if message starts with "/"
			services=unicode(self.ui.line.toPlainText())
			if services.startswith("/google"):
				anchor="http://www.google.com/search?q="+services.replace("/google ","")
				QtGui.QDesktopServices.openUrl(QtCore.QUrl(anchor))
				self.ui.line.clear()
				self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
				self.ui.line.composing=False
				return
				
			elif services.startswith("/"):
				try:
					cmd, args = services.split(" ", 1)
					args = args.split(" ")
				except ValueError:
					cmd = services
					args = []
				cmd = cmd[1:]
				# publish onCommnad event for events subscribers (mainly plugins)
				self.main.client.dispatcher.publishEvent("onCommand", cmd, args, self, "chat")
				self.ui.line.clear()
				self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
				self.ui.line.composing=False
				return
			
			# get plain text message
			text=unicode(self.ui.line.toPlainText())
			text=unescape(text)
			ret=[]
			if self.xhtml:
				xhtml=self.ui.line.toHtml()
				xhtml,same=self.qtHtmlToXhtml(xhtml,text)
			if self.xhtml and not same:
				# get message in Qt html format
				#xhtml=self.ui.line.toHtml()
				#xhtml,same=self.qtHtmlToXhtml(xhtml,text)
				# send message
				if same:
					for key,value in self.main.plugins.iteritems():
						if value['module']:
							ret.append(self.main.runPluginCommand(value['module'].on_messageSend,[unicode(self.jid),text,'',"active"]))
					if not False in ret:
						self.main.client.sendMessage(unicode(self.jid),text,composing="active")
				else:
					for key,value in self.main.plugins.iteritems():
						if value['module']:
							ret.append(self.main.runPluginCommand(value['module'].on_messageSend,[unicode(self.jid),text,xhtml,"active"]))
					if not False in ret:
						self.main.client.sendMessage(unicode(self.jid),text,xhtml=xhtml,composing="active")
				
				# prepare message for showing in GUI
				message=xhtml.replace("&quot;",'"')
				#file=self.main.homeDir+'/avatars/'+unicode(self.main.client.jid.userhost())
				#if not os.path.isfile(file):
					#file="images/32x32/apps/jabbim.png"
				#skin=self.main.skin["my_message"]
				#if self.lastMessageFrom==unicode(self.main.client.jid.user):
					#if self.main.skin.has_key('my_message_continue'):
						#skin=self.main.skin["my_message_continue"]
				#message=skin.replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",message).replace("[avatar]","<img src=\""+self.selfFile+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
				self.appendLastMessage(['out',self.main.client.jid.user,message,self.main.now(),self.selfFile])
				message=self.main.webkitThemeFactory.genOutgoingContent(self.main.client.jid.user,message,self.main.now(),self.selfFile)
				insert=False
			else:
				# send message
				#text=unescape(text)
				for key,value in self.main.plugins.iteritems():
					if value['module']:
						ret.append(self.main.runPluginCommand(value['module'].on_messageSend,[unicode(self.jid),text,'',"active"]))
				if not False in ret:
					self.main.client.sendMessage(unicode(self.jid),text,composing="active")
				
				# prepare message for showing in GUI
				text=unicode(text).replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")
				text=utils.replace_url(text)
				text=text.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")
				#file=self.main.homeDir+'/avatars/'+unicode(self.main.client.jid.userhost())
				#if not os.path.isfile(file):
					#file="images/32x32/apps/jabbim.png"
				#if unicode(text).startswith("/me"):
					#message=self.main.skin["my_me_message"]#.replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",text[3:]).replace("[avatar]","<img src=\""+file+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
					#if self.lastMessageFrom==unicode(self.main.client.jid.user):
						#if self.main.skin.has_key('my_me_message_continue'):
							#message=self.main.skin["my_me_message_continue"]
					#message=message.replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",text[3:]).replace("[avatar]","<img src=\""+self.selfFile+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
				#else:
					#message=self.main.skin["my_message"]
					#if self.lastMessageFrom==unicode(self.main.client.jid.user):
						#if self.main.skin.has_key('my_message_continue'):
							#message=self.main.skin["my_message_continue"]
					#message=message.replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",text).replace("[avatar]","<img src=\""+self.selfFile+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
				self.appendLastMessage(['out',self.main.client.jid.user,text,self.main.now(),self.selfFile])
				if self.lastMessageFrom==unicode(self.main.client.jid.user):
					message=self.main.webkitThemeFactory.genOutgoingNextContent(self.main.client.jid.user,text,self.main.now(),self.selfFile)
					insert=True
				else:
					message=self.main.webkitThemeFactory.genOutgoingContent(self.main.client.jid.user,text,self.main.now(),self.selfFile)
					insert=False

					
			self.lastMessageFrom=unicode(self.main.client.jid.user)
			# show message
			if not False in ret:
				self.textEditWrite(message,insert)
			# add message to 'sent messages history'
			self.sent.append(text)
			self.hindex = len(self.sent)
			
			#self.ui.line.clear()
			#self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
			self.clearLine()
			self.ui.line.composing=False
			# depracted
			if self.main.chat.active==False:
				self.main.client.dispatcher.publishEvent('onActivity')
				self.main.chat.active=True
