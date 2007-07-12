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

class lineEditWidget(QtGui.QTextEdit):
	def __init__(self,main,parent=None):
		apply(QtGui.QTextEdit.__init__,(self,parent))
		self.main=main
		self.parent=parent
		self.setMaximumSize(QtCore.QSize(16777215,30))
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

class chatWidget(QtGui.QWidget):
	def __init__(self,main,jid,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.ui=Ui_chatwidget()
		self.ui.setupUi(self)

		layout=QtGui.QHBoxLayout(self.ui.lineWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.ui.line=lineEditWidget(self,self)
		layout.addWidget(self.ui.line)
		
		#self.ui.gridlayout.addWidget(self.ui.line,2,0,1,1)
		self.main=main
		QtCore.QObject.connect(self.ui.sendButton, QtCore.SIGNAL("clicked ()"),self.sendButtonClicked)
		#QtCore.QObject.connect(self.ui.line, QtCore.SIGNAL("returnPressed ()"),self.sendButtonClicked)
		#QtCore.QObject.connect(self.ui.line, QtCore.SIGNAL("textChanged ()"),self.lines)
		QtCore.QObject.connect(self.ui.smileys, QtCore.SIGNAL("clicked (bool)"),self.smileysClicked)

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
		self.ui.line.setMaximumHeight(int(self.ui.line.currentFont().pointSize())*8)
		self.ui.lineWidget.setMaximumHeight(int(self.ui.line.currentFont().pointSize())*8)


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
		cur=self.ui.textEdit.textCursor()
		cur.movePosition(QtGui.QTextCursor.End)
		self.ui.textEdit.setTextCursor(cur)
		# emoticons
		for k,v in self.smileys.iteritems():
			text=text.replace(" "+k,' <img src="images/16x16/emotes/'+v+'"/>')
		self.ui.textEdit.insertHtml(text)
		cur=self.ui.textEdit.textCursor()
		cur.movePosition(QtGui.QTextCursor.End)
		self.ui.textEdit.setTextCursor(cur)
	
	def addEmoticon(self,action):
		# add emoticon to the self.ui.line
		data=action.data()
		data=data.toString()
		self.ui.line.append(data)
		self.ui.smileys.setChecked(False)
		self.s.hide()
		self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
	
	def sendButtonClicked(self):
		# sends message
		if len(unicode(self.ui.line.toPlainText()))!=0:
			text=unicode(self.ui.line.toHtml())
			a=parseString(text)
			for el in a.getElementsByTagName('img'):
				path=el.attributes['src'].split('/')[-1]
				for k,v in self.smileys.iteritems():
					if v==path:
						path=k
				newnode = parseString("<div> "+path+"</div>").documentElement
				el.parentNode.replaceChild(newnode,el)
			b=a.getElementsByTagName('body')
			c=parseString(b[0].toxml())
			text=gatherTextNodes(c)

			self.main.client.sendMessage(str(self.jid),text)
			for word in text.split(' '):
				if word.find("http://")!=-1:
					print word,'<a href="'+word+'">'+word+'</a>'
					text=text.replace(word,'<a href="'+unicode(urllib.unquote(word))+'">'+word+'</a>')
			message=self.main.skin["my_message"].replace("[time]",self.main.now()).replace("[user]",self.main.client.jid.user).replace("[message]",text)
			self.textEditWrite(message)
			self.ui.line.clear()


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
