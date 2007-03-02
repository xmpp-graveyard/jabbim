try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from groupchatwidget_ui import *
from configobj import ConfigObj

class groupChatWidget(QtGui.QWidget):
	def __init__(self,main,jid,jab,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.jab=jab
		self.ui=Ui_groupchatwidget()
		self.ui.setupUi(self)
		self.main=main
		QtCore.QObject.connect(self.ui.sendButton, QtCore.SIGNAL("clicked ()"),self.sendButtonClicked)
		QtCore.QObject.connect(self.ui.line, QtCore.SIGNAL("returnPressed ()"),self.sendButtonClicked)
		QtCore.QObject.connect(self.ui.smileys, QtCore.SIGNAL("clicked (bool)"),self.smileysClicked)
		short=QtGui.QShortcut("tab",self.ui.line)
		QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.tabPressed)
		self.ui.info_big.hide()
		self.loadSmileys()
		self.jid=jid
		self.name_id=-1 # for tabPressed

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
				action=QtGui.QAction(QtGui.QIcon("images/22x22/emotes/"+v),"",self.s)
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
			text=text.replace(k,'<img src="images/smileys/'+v+'"/>')
		self.ui.textEdit.insertHtml(text)
		cur=self.ui.textEdit.textCursor()
		cur.movePosition(QtGui.QTextCursor.End)
		self.ui.textEdit.setTextCursor(cur)
	
	def addEmoticon(self,action):
		# add emoticon to the self.ui.line
		data=action.data()
		data=data.toString()
		self.ui.line.insert(data)
		self.ui.smileys.setChecked(False)
		self.s.hide()
	
	def sendButtonClicked(self):
		# sends message
		if len(unicode(self.ui.line.text()))!=0:
			self.jab.groupchatSend(str(self.jid),unicode(self.ui.line.text()))
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