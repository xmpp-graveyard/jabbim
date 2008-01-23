try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from configobj import ConfigObj
#from palette import *
import urllib,re,os
from twisted.web.microdom import *
from twisted.web.domhelpers import gatherTextNodes
import filetransfer
from twisted.words.protocols.jabber import jid as jidT
import time
from include import utils

class abstractTextView(QtGui.QTextEdit):
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
		self.main.tabWord=None
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
		QtCore.QObject.connect(self,QtCore.SIGNAL("currentCharFormatChanged ( const QTextCharFormat & )"),self.formatChanged)

	def focusInEvent(self,event):
		r=QtGui.QTextEdit.focusInEvent(self,event)
		self.reformat()
		return r

	def formatChanged(self,format):
		#print "format changed",len(unicode(self.toPlainText()))
		if len(unicode(self.toPlainText()))==0:
			self.reformat()

	def reformat(self):
		self.parent.underline(self.underline)
		self.parent.bold(self.bold)
		self.parent.italic(self.italic)
		if self.color:
			self.parent.color(unicode(self.color.name()))

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
		self.main.tabWord=None
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

class abstractChatWidget(QtGui.QWidget):
	def __init__(self,initClass,textEditClass,main,jid,xhtml=True,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.ui=initClass()
		self.ui.setupUi(self)
		self.main=main
		self.parent=parent
		self.xhtml=xhtml

		# chat view widget (self.ui.textEdit)
		l=QtGui.QHBoxLayout(self.ui.viewWidget)
		l.setMargin(0)
		l.setSpacing(0)
		self.ui.textEdit=textEditClass(self,self.ui.viewWidget)#textView(self,self.ui.viewWidget)
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
		self.sent = []
		self.hindex = 0

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
		self.unread=0 #: number of unread messages

		if not self.xhtml:
			self.ui.boldButton.hide()
			self.ui.italicButton.hide()
			self.ui.underlineButton.hide()
			self.ui.colorButton.hide()
		else:
			self.defaultFormat=self.ui.line.currentCharFormat()
			self.defaultColor=self.ui.line.textColor()
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
	
	def color(self,action):
		"""
		Sets foreground color according to action.data(). Data should be color like #FFFFFF or string "no" for default system color.
		"""
		if isinstance(action,unicode) or isinstance(action,str):
			color=action
			self.ui.line.color=QtGui.QColor(color)
		else:
			color=unicode(action.data().toString())
			self.ui.line.color=QtGui.QColor(color)
			self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)
		
		if color.startswith("#") and QtGui.QColor(color)!=self.defaultColor:
			c=QtGui.QColor(color)
			self.ui.line.setTextColor(c)
			colorIcon=QtGui.QPixmap(16,16)
			colorIcon.fill(c)
			self.ui.colorButton.setIcon(QtGui.QIcon(colorIcon))
			#self.noColor=False
		else:
			format=self.defaultFormat
			format.setFontItalic(self.ui.line.fontItalic())
			format.setFontUnderline(self.ui.line.fontUnderline())
			format.setFontWeight(self.ui.line.fontWeight())
			self.ui.line.setCurrentCharFormat(format)
			colorIcon=QtGui.QPixmap(16,16)
			colorIcon.fill(self.defaultFormat.foreground().color())
			self.ui.colorButton.setIcon(QtGui.QIcon(colorIcon))
			#self.noColor=True

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
		self.ui.line.italic=bool
		self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)
		self.ui.line.setFontItalic(bool)


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

	def underline(self,bool):
		"""
		Sets underline font according to bool.
		@type bool: boolean
		@param bool: True - underline font
		"""
		self.ui.line.underline=bool
		self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)
		self.ui.line.setFontUnderline(bool)


	def bold(self,bool):
		"""
		Sets bold font according to bool.
		@type bool: boolean
		@param bool: True - bold font
		"""
		self.ui.line.bold=bool
		self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)
		if bool==True:
			self.ui.line.setFontWeight(QtGui.QFont.Bold)
		else:
			self.ui.line.setFontWeight(QtGui.QFont.Normal)

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
		pass


