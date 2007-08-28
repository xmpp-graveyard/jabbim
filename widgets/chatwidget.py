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
import urllib,re
from twisted.web.microdom import *
from twisted.web.domhelpers import gatherTextNodes

class textView(QtGui.QTextEdit):
	def __init__(self,parent):
		QtGui.QTextEdit.__init__(self,parent)
		self.setMouseTracking(True)
		self.setReadOnly(True)

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
			QtGui.QTextEdit.keyPressEvent(self,event)
		elif key==QtCore.Qt.Key_Return or key==QtCore.Qt.Key_Enter:
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

class normalLineEditWidget(QtGui.QTextEdit):
	def __init__(self,main,parent=None):
		apply(QtGui.QTextEdit.__init__,(self,parent))
		self.main=main
		self.parent=parent
		#self.setMaximumSize(QtCore.QSize(16777215,30))
		self.setObjectName("line")
		self.composing=False
	
	def keyPressEvent(self,event):
		if not self.composing:
			self.composing=True
			self.main.main.client.sendMessage(self.main.jid, "",composing="composing")
		key=event.key()
		if (key==QtCore.Qt.Key_Return or key==QtCore.Qt.Key_Enter) and (event.modifiers() & QtCore.Qt.ControlModifier or event.modifiers() & QtCore.Qt.ShiftModifier):
			QtGui.QTextEdit.keyPressEvent(self,event)
		elif key==QtCore.Qt.Key_Return or key==QtCore.Qt.Key_Enter:
			self.main.sendButtonClicked()
		else:
			QtGui.QTextEdit.keyPressEvent(self,event)

class chatWidget(QtGui.QWidget):
	def __init__(self,main,jid,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.ui=Ui_chatwidget()
		self.ui.setupUi(self)
		self.main=main

		l=QtGui.QHBoxLayout(self.ui.viewWidget)
		l.setMargin(0)
		l.setSpacing(0)
		self.ui.textEdit=textView(self.ui.viewWidget)
		l.addWidget(self.ui.textEdit)
		
		layout=QtGui.QHBoxLayout(self.ui.lineWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		if self.main.config['chatMode']=="normal":
			self.ui.line=normalLineEditWidget(self,self)
		else:
			self.ui.line=lineEditWidget(self,self)
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
		self.ui.textEdit.setAcceptRichText(True)
		self.ui.textEdit.setHtml("<br/>")
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
		self.ui.splitter.setSizes([500,70])

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

	def loadSmileys(self):
		# loads smileys.conf and makes buttons
		self.smileys=ConfigObj("smileys.conf",encoding='UTF8')
		self.s=QtGui.QFrame(self)
		self.s.hide()
		layout=QtGui.QGridLayout(self.s)
		layout.setMargin(0)
		layout.setSpacing(0)
		added=[]
		x=0
		y=0
		for k,v in self.smileys.iteritems():
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
		self.s.setGeometry ( self.ui.smileys.x()-60, self.ui.smileys.y()-200, 120, 200)
		self.s.setShown(bool)
	
	def textEditWrite(self,text):
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
			self.ui.line.append(data)
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
			self.main.client.sendMessage(str(self.jid),text)
			text=unicode(text).replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>")
			for word in text.split(' '):
				if word.find("http://")!=-1:
					text=text.replace(word,'<a href="'+unicode(urllib.unquote(word))+'">'+word+'</a>')
			message=self.main.skin["my_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",text)
			
			self.textEditWrite(message)
			self.ui.line.clear()
			self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
			self.ui.line.composing=False

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
