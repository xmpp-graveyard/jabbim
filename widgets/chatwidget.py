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
from twisted.words.protocols.jabber import jid as jidT
import time
from include import utils
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

class textView(QtGui.QTextEdit):
	"""
	Text view for chat conversation.
	"""
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
		self.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)

	def dragEnterEvent(self, event):
		if event.mimeData().hasText():
			if self.main.getJid(unicode(event.mimeData().text())):
				event.acceptProposedAction()
			else:
				event.ignore()
		else:
			event.ignore()

	def dragMoveEvent(self, event):
		event.acceptProposedAction()

	def dropEvent(self, event):
		"""
		Called when something is dropped to this widget.
		If there is JID dropped, new MUC is created and the jid is invited to the room.
		"""
		if event.mimeData().hasText():
			# test if it is JID
			jid2=self.main.getJid(unicode(event.mimeData().text()))
			if not jid2:
				event.ignore()
				return

			room=str(int(time.time())) # define room name
			# find server when we can host the room
			mucjid = None
			for jid, node in self.main.client.disco.iteritems():
				if not node[None].has_key('identities'):
					continue
				for id in node[None]['identities'].itervalues():
					#print jid, id
					if id.get('category') == 'conference' and id.get('type') == 'text' and jid.startswith('c'):
						mucjid = jid
						break
				if mucjid:
					break
			room+="@"+mucjid # room jabber id
			
			name=self.parent.parent.tabName # get name of tab where is this widget showed
			rmIndex=int(self.main.chat.ui.chatTab.currentIndex()) # get index of this tab
			# join to the room and send invitation
			if self.main.chat.addGroupChatTab(room,self.main.client.jid.user,name=name):
				tab,index=self.main.chat.findTab(room)
				tab.chat.invitation=[unicode(jid2.full()),unicode(self.parent.jid)]
				self.main.client.joinGC(room, self.main.client.jid.user)
			# remove old user2user conversation tab
			self.main.chat.removeTab(rmIndex)
			event.acceptProposedAction()
		else:
			event.ignore()
		
	def mouseMoveEvent(self,event):
		"""
		Changes mouse pointer if it is above link.
		"""
		anchor = self.anchorAt(event.pos())
		if len(anchor)!=0:
			self.viewport().setCursor(QtCore.Qt.PointingHandCursor)
		else:
			self.viewport().setCursor(QtCore.Qt.ArrowCursor)
		return QtGui.QTextEdit.mouseMoveEvent(self,event)

	def mousePressEvent(self,event):
		"""
		Opens link under mouse pointer.
		"""
		anchor = self.anchorAt(event.pos())
		if event.button()==QtCore.Qt.LeftButton:
			if len(anchor)!=0:
				QtGui.QDesktopServices.openUrl(QtCore.QUrl(anchor))
		return QtGui.QTextEdit.mousePressEvent(self,event)
	
	def createMimeDataFromSelection(self):
		"""
		Creates data for clipboard from selected text.
		"""
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
			if self.main.main.config['sendByCtrl']=="False":
				self.main.sendButtonClicked()
				event.accept()
			else:
				return QtGui.QTextEdit.keyPressEvent(self,event)
		
		else:
			return QtGui.QTextEdit.keyPressEvent(self,event)
			text=unicode(self.toPlainText())
			for k,v in self.parent.smileys.iteritems():
				if text.find(" "+k)!=-1:
					html=self.toHtml()
					html.replace(k,'<img src="'+v+'"/> ')
					cur=self.textCursor()
					self.setHtml(html)
					self.setTextCursor(cur)

class normalLineEditWidget(QtGui.QTextEdit):
	"""
	QTextEdit widget for user input.
	"""
	def __init__(self,main,parent=None):
		apply(QtGui.QTextEdit.__init__,(self,parent))
		self.main=main #: MainWindow pointer
		self.parent=parent #: parent
		self.setObjectName("line")
		self.composing=False #: True if user is typing
		self.timer=QtCore.QTimer() # timer to determine if user paused typing
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"),self.paused)
		self.text=""
		self.t=False
		self.bold=False
		self.italic=False
		self.underline=False
		self.color=None

	def paused(self):
		"""
		Detects if user stops typing and sends 'paused' message if user stops.
		"""
		try:
			self.timer.stop()
		except:pass
		if self.text==unicode(self.toPlainText()):
			# text from previous loop is the same as currently typed text => user stops typing
			self.main.main.client.sendMessage(self.main.jid, "",composing="paused")
			self.composing=False
		else:
			# text from previous loop is diffrent from currently typed text => user is typing
			self.timer.start(2000)
			self.text=unicode(self.toPlainText())

		self.t=False
	
	def keyPressEvent(self,event):
		if not self.composing:
			# user starts typing
			self.main.main.client.sendMessage(self.main.jid, "",composing="composing")
		key=event.key()
		if (key==QtCore.Qt.Key_Return or key==QtCore.Qt.Key_Enter) and (event.modifiers() & QtCore.Qt.ControlModifier):
			if self.main.main.config['sendByCtrl']=="True":
				self.main.sendButtonClicked()
				event.accept()
			else:
				return QtGui.QTextEdit.keyPressEvent(self,event)
		elif key==QtCore.Qt.Key_Return or key==QtCore.Qt.Key_Enter:
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
			# detect format of current character
			b=self.fontWeight()==QtGui.QFont.Bold
			if self.bold!=b:
				self.bold=b
				self.parent.ui.boldButton.setChecked(b)
			b=self.fontItalic()
			if self.italic!=b:
				self.italic=b
				self.parent.ui.italicButton.setChecked(b)
			b=self.fontUnderline()
			if self.underline!=b:
				self.underline=b
				self.parent.ui.underlineButton.setChecked(b)
			b=self.textColor()
			if self.color!=b:
				self.color=b
				colorIcon=QtGui.QPixmap(16,16)
				colorIcon.fill(b)
				self.parent.ui.colorButton.setIcon(QtGui.QIcon(colorIcon))

			QtGui.QTextEdit.keyPressEvent(self,event)

		# user starts composing so we have to start checking if he doesn't stop
		# we have to start timer only once, so there is some type of locker self.t
		if not self.t and not self.composing:
			self.text=unicode(self.toPlainText())
			self.t=True
			self.timer.start(2000)
		if not self.composing:
			self.composing=True

class frame(QtGui.QFrame):
	"""
	QFrame for emoticons.
	"""
	def __init__(self,main,parent=None):
		QtGui.QFrame.__init__(self,parent)
		self.main=main

	def hideEvent(self,event):
		"""
		Uncheck Emoticons button in ChatWidget
		"""
		self.main.ui.smileys.setChecked(False)

class chatWidget(QtGui.QWidget):
	def __init__(self,main,jid,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.ui=Ui_chatwidget()
		self.ui.setupUi(self)
		self.main=main
		self.parent=parent

		# chat view widget (self.ui.textEdit)
		l=QtGui.QHBoxLayout(self.ui.viewWidget)
		l.setMargin(0)
		l.setSpacing(0)
		self.ui.textEdit=textView(self,self.ui.viewWidget)
		l.addWidget(self.ui.textEdit)

		# chat editor widget (self.ui.line)
		layout=QtGui.QHBoxLayout(self.ui.lineWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.ui.line=normalLineEditWidget(self,self)
		self.ui.line.setAcceptRichText(False)
		layout.addWidget(self.ui.line)

		self.first=None #: True if first message arrived; False if arrived more than one message. Otherwise None.
		self.jid=jid #: users JID

		# signals
		QtCore.QObject.connect(self.ui.sendButton, QtCore.SIGNAL("clicked ()"),self.sendButtonClicked)
		QtCore.QObject.connect(self.ui.line, QtCore.SIGNAL("returnPressed ()"),self.sendButtonClicked)
		QtCore.QObject.connect(self.ui.smileys, QtCore.SIGNAL("clicked (bool)"),self.smileysClicked)
		QtCore.QObject.connect(self.ui.boldButton, QtCore.SIGNAL("toggled (bool)"),self.bold)
		QtCore.QObject.connect(self.ui.italicButton, QtCore.SIGNAL("toggled (bool)"),self.italic)
		QtCore.QObject.connect(self.ui.underlineButton, QtCore.SIGNAL("toggled (bool)"),self.underline)
		
		self.ui.textEdit.setAcceptRichText(False)
		# save init part from self.main.skin to the textEdit
		self.init=""
		if self.main.skin.has_key("on_init"):
			self.init=self.main.skin["on_init"]
		self.ui.textEdit.setHtml("<br/>"+self.init)
		
		self.loadSmileys() # load emoticons
		
		# set splitters sizes
		self.ui.splitter.setSizes(list(self.main.config['chatSplitterSizes']))
		self.ui.splitter_2.setSizes(list(self.main.config['chatSplitter2Sizes']))
		widget=self.ui.splitter_2.widget(1)
		widget.setMaximumWidth(128)
		
		# Maximum width of avatar Widget
		self.ui.avatar.setMaximumWidth(128)
		
		self.sent = []
		self.hindex = 0
		self.unread=0 #: number of unread messages
		
		# get users avatar
		self.file=self.main.homeDir+'/avatars/'+unicode(jidT.JID(jid).userhost()) #: path to users avatar
		self.avatarHeight=32 #: avatars height
		if not os.path.isfile(self.file):
			# use default avatar if users avatar doesn't exist
			self.file="images/32x32/apps/jabbim.png"
		else:
			# change size of users avatar
			# TODO: size should be changed by skin...
			pixmap=QtGui.QPixmap(self.file).scaledToWidth(32)
			self.avatarHeight=int(pixmap.height())

		# get self avatar
		self.selfHeight=32 #: height of self avatar
		f=self.main.homeDir+'/avatars/'+self.main.client.jid.userhost()
		if not os.path.isfile(f):
			self.file="images/32x32/apps/jabbim.png"
		else:
			pixmap=QtGui.QPixmap(f).scaledToWidth(32)
			self.selfHeight=int(pixmap.height())
		
		# allow xhmtl if user supports it
		jidt=jidT.JID(self.jid)
		try:
			self.xhtml=self.main.client.roster['users'][jidt.userhost()].resources[jidt.resource].hasFeature('http://jabber.org/protocol/xhtml-im') #: True if user supports xhtml, otherwise False
		except:
			self.xhtml=False
		if not self.xhtml:
			self.ui.boldButton.hide()
			self.ui.italicButton.hide()
			self.ui.underlineButton.hide()
			self.ui.colorButton.hide()
		else:
			self.defaultFormat=self.ui.line.currentCharFormat()
			colorMenu=QtGui.QMenu(self.ui.colorButton)
			colorIcon=QtGui.QPixmap(16,16)
			
			colorIcon.fill(QtCore.Qt.white)
			action=colorMenu.addAction(QtGui.QIcon(colorIcon),self.tr('White'))
			action.setData(QtCore.QVariant("#ffffff"))

			colorIcon.fill(QtCore.Qt.black)
			action=colorMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Black'))
			action.setData(QtCore.QVariant("#000000"))
			
			colorIcon.fill(QtCore.Qt.red)
			action=colorMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Red'))
			action.setData(QtCore.QVariant("#ff0000"))
			
			colorIcon.fill(QtCore.Qt.green)
			action=colorMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Green'))
			action.setData(QtCore.QVariant("#00ff00"))
			
			colorIcon.fill(QtCore.Qt.blue)
			action=colorMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Blue'))
			action.setData(QtCore.QVariant("#0000ff"))

			colorIcon.fill(QtCore.Qt.magenta)
			action=colorMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Pink'))
			action.setData(QtCore.QVariant("#ff00ff"))

			colorIcon.fill(QtCore.Qt.yellow)
			action=colorMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Yellow'))
			action.setData(QtCore.QVariant("#ffff00"))

			colorMenu.addSeparator()

			action=colorMenu.addAction(self.tr('No color'))
			action.setData(QtCore.QVariant("no"))

			QtCore.QObject.connect(colorMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.color)
			self.ui.colorButton.setMenu(colorMenu)
			colorIcon.fill(self.defaultFormat.foreground().color())
			self.ui.colorButton.setIcon(QtGui.QIcon(colorIcon))

		# plugins buttons
		self.flowLayout = flowLayout()
		for key,value in self.main.plugins.iteritems():
			if value['module']:
				self.main.runPluginCommand(value['module'].buildChatWidget,[unicode(jidT.JID(self.jid).userhost()),self.flowLayout,self])
		
		# sendFile buttons
		self.ui.sendFile=QtGui.QToolButton()
		self.ui.sendFile.setIconSize(QtCore.QSize(16,16))
		self.ui.sendFile.setIcon(QtGui.QIcon("images/32x32/actions/upload.png"))
		self.ui.sendFile.setToolTip(self.tr("Send file"))
		self.flowLayout.addWidget(self.ui.sendFile)
		QtCore.QObject.connect(self.ui.sendFile, QtCore.SIGNAL("clicked ()"),self.sendFiles)

		self.ui.pluginWidget.setLayout(self.flowLayout)

		if self.main.selfAvatar:
			result=self.main.getAvatar(self.main.selfAvatar,size="64x64",frame=True)
			self.ui.selfAvatar.setPixmap(result)
			self.ui.selfAvatar.setMaximumWidth(64)
		else:
			self.ui.selfAvatar.hide()

	def color(self,action):
		"""
		Sets foreground color according to action.data(). Data should be color like #FFFFFF or string "no" for default system color.
		"""
		color=unicode(action.data().toString())
		self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)
		if color.startswith("#"):
			c=QtGui.QColor(color)
			self.ui.line.setTextColor(c)
			colorIcon=QtGui.QPixmap(16,16)
			colorIcon.fill(c)
			self.ui.colorButton.setIcon(QtGui.QIcon(colorIcon))
		else:
			format=self.defaultFormat
			format.setFontItalic(self.ui.line.fontItalic())
			format.setFontUnderline(self.ui.line.fontUnderline())
			format.setFontWeight(self.ui.line.fontWeight())
			self.ui.line.setCurrentCharFormat(format)
			colorIcon=QtGui.QPixmap(16,16)
			colorIcon.fill(self.defaultFormat.foreground().color())
			self.ui.colorButton.setIcon(QtGui.QIcon(colorIcon))

	def clearLine(self):
		format=self.ui.line.currentCharFormat()
		self.ui.line.clear()
		self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)
		self.ui.line.setCurrentCharFormat(format)
		

	def italic(self,bool):
		"""
		Sets italic font according to bool.
		@type bool: boolean
		@param bool: True - italic font
		"""
		self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)
		self.ui.line.setFontItalic(bool)

	def underline(self,bool):
		"""
		Sets underline font according to bool.
		@type bool: boolean
		@param bool: True - underline font
		"""
		self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)
		self.ui.line.setFontUnderline(bool)

	def bold(self,bool):
		"""
		Sets bold font according to bool.
		@type bool: boolean
		@param bool: True - bold font
		"""
		self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)
		if bool==True:
			self.ui.line.setFontWeight(QtGui.QFont.Bold)
		else:
			self.ui.line.setFontWeight(QtGui.QFont.Normal)

	def sendFiles(self):
		"""
		Shows filetransfer dialog and sends files to user who chats with us.
		"""
		file=QtGui.QFileDialog.getOpenFileNames(self,"Choose file")
		file=list(file)
		if len(file)!=0:
			new=[]
			for f in file:
				new.append(unicode(f))
			file=new
			# show filetransfer dialog and send files
			self.dialog=filetransfer.filetransferDialog(self.main,file,self.jid)
			self.dialog.show()

	def loadSmileys(self):
		"""
		Loads emoticons pack according to self.main.config['emoticons'] and makes
		widget for choosing emoticons
		"""
		# load emoticons pack
		smileys=ConfigObj("emoticons/"+self.main.config['emoticons'],encoding='UTF8')
		src='emoticons/'
		if len(smileys)==0:
			smileys=ConfigObj(self.main.realHomeDir+"/emoticons/"+self.main.config['emoticons'],encoding='UTF8')
			src=self.main.realHomeDir+'/emoticons/'
		if len(smileys)==0:
			# emotions pack doesn't exist
			return

		# load images
		self.smileys={} #: images for emoticons. for example {":-)":"emoticons/default/smile.png"}
		for k,v in smileys['emoticons'].iteritems():
			self.smileys[k.replace("<","&lt;").replace(">","&gt;")]=src+os.path.dirname(self.main.config['emoticons'])+"/"+v
		
		# make QFrame for images preview
		self.s=frame(self,self)
		self.s.setWindowFlags(QtCore.Qt.Popup)
		self.s.hide()
		layout=QtGui.QGridLayout(self.s)
		layout.setMargin(0)
		layout.setSpacing(0)
		added=[]
		x=0
		y=0
		# make QToolButton for every image, add it to layout of self.s, and connnect to self.addEmotion
		for k,v in smileys['emoticons'].iteritems():
			if added.count(v)==0:
				added.append(v)
				button=QtGui.QToolButton(self)
				action=QtGui.QAction(QtGui.QIcon(src+os.path.dirname(self.main.config['emoticons'])+"/"+v),"",self.s)
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
		"""
		Shows self.s (QFrame with emoticons).
		"""
		pos=self.ui.smileys.mapToGlobal(QtCore.QPoint(0,0))
		x=pos.x()
		y=pos.y()
		self.s.setGeometry(x-60,y-200, 120, 200)
		if self.s.isVisible():
			self.s.setVisible(False)
		else:
			self.s.setVisible(True)
	
	def textEditWrite(self,text,history=False):
		"""
		Appends formated message to the chat view (self.ui.textEdit).
		@type text: unicode
		@param text: formated message
		@type history: boolean
		@param history: True if text is history message (has delay). In this case self.first will not be updated.
		"""
		# update information about first message of this chat
		if not history:
			if self.first==True:
				self.first=False
			elif self.first==None:
				self.first=True
		self.ui.textEdit.setUpdatesEnabled(False) # disable updates because of performance
		# move text cursor to the end of document
		cursor=QtGui.QTextCursor(self.ui.textEdit.document())
		cursor.beginEditBlock()
		cursor.movePosition(QtGui.QTextCursor.End)
		
		# if scrollbar is in the end, we have to scroll it to the end as well when we finish
		toEnd=False
		if self.ui.textEdit.verticalScrollBar().value()==self.ui.textEdit.verticalScrollBar().maximum():
			toEnd=True
		# replace emoticons by images
		for k,v in self.smileys.iteritems():
			text=text.replace(" "+k,'&nbsp;<img src="'+v+'"/>')
			text=text.replace("&nbsp;"+k,'&nbsp;<img src="'+v+'"/>')
			text=text.replace(">"+k,'><img src="'+v+'"/>')
		# insert text to the self.ui.textEdit
		cursor.insertFragment(QtGui.QTextDocumentFragment.fromHtml(text))
		cursor.endEditBlock()
		if toEnd:
			# scroll to the end
			self.ui.textEdit.verticalScrollBar().setValue(self.ui.textEdit.verticalScrollBar().maximum())
		self.ui.textEdit.setUpdatesEnabled(True)
		

	
	def addEmoticon(self,action):
		"""
		Insert emoticon according to action.objectName() to the self.ui.line. Called when user choose one of emoticons.
		@type action: QAction
		@param action: emotion QAction
		"""
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
			if self.xhtml:
				# get message in Qt html format
				xhtml=self.ui.line.toHtml()
				
				# remove things which are not allowed by XEP or are unnecessarily
				a=parseString(unicode(xhtml))
				for el in a.getElementsByTagName('p'):
					if el.hasAttribute("style"):
						el.removeAttribute("style")
				for el in a.getElementsByTagName('body'):
					if el.hasAttribute("style"):
						el.removeAttribute("style")
				b=a.getElementsByTagName('body')
				b=b[0]
				xhtml=b.toxml()
				# TODO: we must replace only first <body> and <p>... not tags in whole message
				xhtml=unicode(xhtml,'utf-8').replace("<body>","").replace("</body>","").replace("<p>","<span>").replace("</p>","</span>")
				
				# send message
				self.main.client.sendMessage(unicode(self.jid),text,xhtml=xhtml,composing="active")
				
				# prepare message for showing in GUI
				message=xhtml.replace("&quot;",'"')
				file=self.main.homeDir+'/avatars/'+unicode(self.main.client.jid.userhost())
				if not os.path.isfile(file):
					file="images/32x32/apps/jabbim.png"
				message=self.main.skin["my_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",message).replace("[avatar]","<img src=\""+file+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
			else:
				# send message
				self.main.client.sendMessage(unicode(self.jid),text,composing="active")
				
				# prepare message for showing in GUI
				text=unicode(text).replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")
				text=utils.replace_url(text)
				text=text.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")
				file=self.main.homeDir+'/avatars/'+unicode(self.main.client.jid.userhost())
				if not os.path.isfile(file):
					file="images/32x32/apps/jabbim.png"
				if unicode(text).startswith("/me"):
					message=self.main.skin["my_me_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",text[3:]).replace("[avatar]","<img src=\""+file+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
				else:
					message=self.main.skin["my_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",text).replace("[avatar]","<img src=\""+file+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
			# show message
			self.textEditWrite(message)
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