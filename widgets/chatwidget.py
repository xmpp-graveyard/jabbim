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

class flowLayout(QtGui.QLayout):
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
	def __init__(self,main,parent):
		QtGui.QTextEdit.__init__(self,parent)
		self.parent=main
		self.setMouseTracking(True)
		self.setReadOnly(True)
		self.data=[]
		self.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
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

class TextIconHandler(QtCore.QObject):
	def intrinsicSize(self,doc,posInDocument,format):
		charFormat = format.toCharFormat()
		return QSizeF(22,22)
	
	def drawObject(self,painter, rect, doc, posInDocument, format):
		charFormat = format.toCharFormat()
		pixmap = QtGui.QPixmap("images/16x16/emotes/biggrin.png")
		painter.drawPixmap(rect, pixmap, pixmap.rect())

class lineEditWidget(QtGui.QTextEdit):
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
					html.replace(k,'<img src="images/16x16/emotes/'+v+'"/> ')
					cur=self.textCursor()
					self.setHtml(html)
					self.setTextCursor(cur)

class normalLineEditWidget(QtGui.QTextEdit):
	def __init__(self,main,parent=None):
		apply(QtGui.QTextEdit.__init__,(self,parent))
		self.main=main
		self.parent=parent
		#self.setMaximumSize(QtCore.QSize(16777215,30))
		self.setObjectName("line")
		self.composing=False
		self.timer=QtCore.QTimer()
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"),self.paused)
		self.text=""
		self.t=False
	def paused(self):
		try:
			self.timer.stop()
		except:pass
		if self.text==unicode(self.toPlainText()):
			self.main.main.client.sendMessage(self.main.jid, "",composing="paused")
			self.composing=False
		else:
			self.timer.start(2000)
			self.text=unicode(self.toPlainText())


		self.t=False
	
	def keyPressEvent(self,event):
		if not self.composing:
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
			QtGui.QTextEdit.keyPressEvent(self,event)
		if not self.t and not self.composing:
			self.text=unicode(self.toPlainText())
			self.t=True
			self.timer.start(2000)
		if not self.composing:
			self.composing=True

class frame(QtGui.QFrame):
	def __init__(self,main,parent=None):
		QtGui.QFrame.__init__(self,parent)
		self.main=main

	def hideEvent(self,event):
		self.main.ui.smileys.setChecked(False)

class chatWidget(QtGui.QWidget):
	def __init__(self,main,jid,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.ui=Ui_chatwidget()
		self.ui.setupUi(self)
		self.main=main

		l=QtGui.QHBoxLayout(self.ui.viewWidget)
		l.setMargin(0)
		l.setSpacing(0)
		self.ui.textEdit=textView(self,self.ui.viewWidget)
		l.addWidget(self.ui.textEdit)
		
		layout=QtGui.QHBoxLayout(self.ui.lineWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		if self.main.config['chatMode']=="normal":
			self.ui.line=normalLineEditWidget(self,self)
		else:
			self.ui.line=lineEditWidget(self,self)
		self.ui.line.setAcceptRichText(False)
		#handler=TextIconHandler()
		#print dir(self.ui.textEdit.document().documentLayout())
		#self.ui.textEdit.document().documentLayout().registerHandler(0x1000, handler)
		layout.addWidget(self.ui.line)
		self.first=None
		#self.ui.gridlayout.addWidget(self.ui.line,2,0,1,1)
		QtCore.QObject.connect(self.ui.sendButton, QtCore.SIGNAL("clicked ()"),self.sendButtonClicked)
		if self.main.config['chatMode']=="normal":
			QtCore.QObject.connect(self.ui.line, QtCore.SIGNAL("returnPressed ()"),self.sendButtonClicked)
		#QtCore.QObject.connect(self.ui.line, QtCore.SIGNAL("textChanged ()"),self.lines)
		QtCore.QObject.connect(self.ui.smileys, QtCore.SIGNAL("clicked (bool)"),self.smileysClicked)
		QtCore.QObject.connect(self.ui.boldButton, QtCore.SIGNAL("clicked (bool)"),self.bold)
		self.ui.textEdit.setAcceptRichText(True)
		self.init=""
		if self.main.skin.has_key("on_init"):
			self.init=self.main.skin["on_init"]
		self.ui.textEdit.setHtml("<br/>"+self.init)
		#short=QtGui.QShortcut(QtCore.Qt.Key_Return,self.ui.line)
		#QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.sendButtonClicked)
		self.loadSmileys()
		self.jid=jid
		self.name_id=-1 # for tabPressed
		#palette=self.palette()
		#palette,images=loadPalette(palette,self.main.palette["chatwidget"])
		#self.setPalette(palette)
		#self.pixmap=images['bgImage']
		#print self.ui.line.currentFont().pointSize()
		#self.ui.line.setMaximumHeight(int(self.ui.line.currentFont().pointSize())*8)
		#self.ui.lineWidget.setMaximumHeight(int(self.ui.line.currentFont().pointSize())*8)
		self.ui.splitter.setSizes(list(self.main.config['chatSplitterSizes']))
		self.ui.avatar.setMaximumWidth(128)
		self.ui.splitter_2.setSizes(list(self.main.config['chatSplitter2Sizes']))
		widget=self.ui.splitter_2.widget(1)
		widget.setMaximumWidth(128)
		self.sent = []
		self.hindex = 0
		self.unread=0
		self.file=self.main.homeDir+'/avatars/'+unicode(jidT.JID(jid).userhost())
		#<img src="[avatar]" width="32" height="32"/>
		self.avatarHeight=32
		if not os.path.isfile(self.file):
			self.file="images/32x32/apps/jabbim.png"
		else:
			pixmap=QtGui.QPixmap(self.file).scaledToWidth(32)
			self.avatarHeight=int(pixmap.height())
		self.selfHeight=32
		f=self.main.homeDir+'/avatars/'+self.main.client.jid.userhost()
		if not os.path.isfile(f):
			self.file="images/32x32/apps/jabbim.png"
		else:
			pixmap=QtGui.QPixmap(f).scaledToWidth(32)
			self.selfHeight=int(pixmap.height())
		self.xhtml=False
		if not self.xhtml:
			self.ui.boldButton.hide()


		self.flowLayout = flowLayout()
		
		for key,value in self.main.plugins.iteritems():
			self.main.runPluginCommand(value.buildChatWidget,[unicode(jidT.JID(self.jid).userhost()),self.flowLayout,self])
		
		self.ui.sendFile=QtGui.QToolButton()
		self.ui.sendFile.setIconSize(QtCore.QSize(16,16))
		self.ui.sendFile.setIcon(QtGui.QIcon("images/32x32/actions/upload.png"))
		self.ui.sendFile.setToolTip(self.tr("Send file"))
		self.flowLayout.addWidget(self.ui.sendFile)
		
		self.ui.pluginWidget.setLayout(self.flowLayout)
		QtCore.QObject.connect(self.ui.sendFile, QtCore.SIGNAL("clicked ()"),self.sendFiles)

		if self.main.selfAvatar:
			result=self.main.getAvatar(self.main.selfAvatar,size="64x64",frame=True)
			self.ui.selfAvatar.setPixmap(result)
			self.ui.selfAvatar.setMaximumWidth(64)
		else:
			self.ui.selfAvatar.hide()


	def bold(self,bool):
		print bool
		if bool==True:
			self.ui.line.setFontWeight(QtGui.QFont.Bold)
		else:
			self.ui.line.setFontWeight(QtGui.QFont.Normal)

	#def lines(self):
		#if self.ui.line.verticalScrollBar().isVisible():
			#self.ui.line.setMaximumHeight(int(self.ui.line.maximumHeight())+int(self.ui.line.currentFont().pointSize())+10)

	#def paintEvent(self,event):
		## paintEvent handler
		#if self.pixmap!=None:
			#viewport=self
			#painter=QtGui.QPainter(viewport)
			#for x in range(int(int(viewport.width())//self.pixmap.width())+1):
				#for y in range(int(int(viewport.height())/self.pixmap.height())+1):
					#painter.drawPixmap(x*int(self.pixmap.width()),y*self.pixmap.height(),self.pixmap)
		#QtGui.QWidget.paintEvent(self,event)

	def sendFiles(self):
		#jid=action.data()
		#jid=str(jid.toString())
		file=QtGui.QFileDialog.getOpenFileNames(self,"Choose file")
		file=list(file)
		if len(file)!=0:
			new=[]
			for f in file:
				new.append(unicode(f))
			file=new
			self.dialog=filetransfer.filetransferDialog(self.main,file,self.jid)
			self.dialog.show()

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
		self.s.setGeometry(x-60,y-200, 120, 200)
		if self.s.isVisible():
			self.s.setVisible(False)
		else:
			self.s.setVisible(True)

	
	def textEditWrite(self,text,history=False):
		if not history:
			if self.first==True:
				self.first=False
			elif self.first==None:
				self.first=True
		self.ui.textEdit.setUpdatesEnabled(False)
		cursor=QtGui.QTextCursor(self.ui.textEdit.document())
		cursor.beginEditBlock()
		cursor.movePosition(QtGui.QTextCursor.End)
		
		toEnd=False
		if self.ui.textEdit.verticalScrollBar().value()==self.ui.textEdit.verticalScrollBar().maximum():
			toEnd=True
		for k,v in self.smileys.iteritems():
			text=text.replace(" "+k,' <img src="images/16x16/emotes/'+v+'"/>')
			#if text[:len(v)]==k:
				#text='<img src="images/16x16/emotes/'+v+'"/>'+text[len(v):]
		#cursor.insertHtml(text)
		cursor.insertFragment(QtGui.QTextDocumentFragment.fromHtml(text))
		#format = cursor.charFormat()
		#icon=TextIconFormat('s','s')
		#cursor.insertText(QtCore.QString(QtCore.QChar.ObjectReplacementCharacter), icon)
		#cursor.setCharFormat(format)
		cursor.endEditBlock()
		if toEnd:
			self.ui.textEdit.verticalScrollBar().setValue(self.ui.textEdit.verticalScrollBar().maximum())
		self.ui.textEdit.setUpdatesEnabled(True)
		

	
	def addEmoticon(self,action):
		# add emoticon to the self.ui.line
		data=action.data()
		data=data.toString()
		if self.main.config['chatMode']=="normal":
			#self.ui.line.append(data)
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
		if len(unicode(self.ui.line.toPlainText()))!=0:
			services=unicode(self.ui.line.toPlainText())
			if services.startswith("/google"):
				anchor="http://www.google.com/search?q="+services.replace("/google ","")
				QtGui.QDesktopServices.openUrl(QtCore.QUrl(anchor))
				self.ui.line.clear()
				self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
				self.ui.line.composing=False
				return
			if self.main.config['chatMode']=="normal":
				text=unicode(self.ui.line.toPlainText())
				#text=unicode(text, 'utf-8')
				text=unescape(text)
			else:
				text=self.ui.line.toHtml()
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
			if self.xhtml:
				text=self.ui.line.toHtml()
				#text=text.replace(unichr(0),"")
				#print text
				a=parseString(unicode(text))
				for el in a.getElementsByTagName('p'):
					if el.hasAttribute("style"):
						el.removeAttribute("style")
				for el in a.getElementsByTagName('body'):
					if el.hasAttribute("style"):
						el.removeAttribute("style")
				#for el in a.getElementsByTagName('span'):
					#if el.hasAttribute("style"):
						#el.removeAttribute("style")



				b=a.getElementsByTagName('body')
				b=b[0]

				text=b.toxml()
				text=unicode(text,'utf-8')
				self.main.client.sendMessage(unicode(self.jid),xhtml=text,composing="active")
			else:
				self.main.client.sendMessage(unicode(self.jid),text,composing="active")
			text=unicode(text).replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")
			for word in text.split(' '):
				if word.find("http://")!=-1:
					text=text.replace(word,'<a href="'+unicode(urllib.unquote(word))+'">'+word+'</a>')
			file=self.main.homeDir+'/avatars/'+unicode(self.main.client.jid.userhost())
			if not os.path.isfile(file):
				file="images/32x32/apps/jabbim.png"
			if unicode(text).startswith("/me"):
				message=self.main.skin["my_me_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",text[3:]).replace("[avatar]","<img src=\""+file+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
			else:
				message=self.main.skin["my_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",text).replace("[avatar]","<img src=\""+file+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
			
			self.textEditWrite(message)
			self.sent.append(text)
			self.hindex = len(self.sent)
			self.ui.line.clear()
			self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
			self.ui.line.composing=False
			if self.main.chat.active==False:
				self.main.client.dispatcher.publishEvent('onActivity')
				self.main.chat.active=True

	def tabPressed(self):
		# nick completion
		text=unicode(self.ui.line.text()).lower()
		if len(text)==0:
			return
		text=text[0]
		repeat=False
		for i in range(self.ui.listWidget.count()):
			if unicode(self.ui.listWidget.item(i).text()).lower()[:len(text)]==text and i>self.name_id:
				self.ui.line.setText(self.ui.listWidget.item(i).text()+": ")
				self.name_id=i
				return
			if unicode(self.ui.listWidget.item(i).text()).lower()[:len(text)]==text:
				repeat=True
		self.name_id=-1
		if repeat==True:
			self.tabPressed()
