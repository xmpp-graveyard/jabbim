try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from groupchatwidget_ui import *
#from groupchatadmin import *
from configobj import ConfigObj
import urllib,re
from twisted.web.microdom import *
from twisted.web.domhelpers import gatherTextNodes

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

class groupChatWidget(QtGui.QWidget):
	def __init__(self,main,jid,jab,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.jab=jab
		self.ui=Ui_groupchatwidget()
		self.ui.setupUi(self)
		self.main=main
		self.affiliation=""


		layout=QtGui.QHBoxLayout(self.ui.lineWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.ui.line=lineEditWidget(self,self)
		layout.addWidget(self.ui.line)

		QtCore.QObject.connect(self.ui.sendButton, QtCore.SIGNAL("clicked ()"),self.sendButtonClicked)
		QtCore.QObject.connect(self.ui.roomConfig, QtCore.SIGNAL("clicked ()"),self.roomConfigClicked)
		QtCore.QObject.connect(self.ui.roomAdmin, QtCore.SIGNAL("clicked ()"),self.roomAdminClicked)
		#QtCore.QObject.connect(self.ui.line, QtCore.SIGNAL("returnPressed ()"),self.sendButtonClicked)
		#QtCore.QObject.connect(self.ui.line, QtCore.SIGNAL("textChanged ()"),self.lines)
		#QtCore.QObject.connect(self.ui.smileys, QtCore.SIGNAL("clicked (bool)"),self.smileysClicked)
		QtCore.QObject.connect(self.ui.sendButton, QtCore.SIGNAL("clicked ()"),self.sendButtonClicked)
		QtCore.QObject.connect(self.ui.smileys, QtCore.SIGNAL("clicked (bool)"),self.smileysClicked)

		short=QtGui.QShortcut("tab",self.ui.line)
		QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.tabPressed)
		#self.ui.info_big.hide()
		self.loadSmileys()
		self.jid=jid
		self.name_id=-1 # for tabPressed
		self.roles={}
		self.addRole("participant","Participants")
		self.addRole("moderator","Moderators")
		self.addRole("visitor","Visitors")
		self.ui.users.header().hide()
		self.ui.users.hideColumn(1)
		#self.ui.line.setMaximumHeight(int(self.ui.line.currentFont().pointSize())+15)
		#self.ui.line.setMaximumHeight(int(self.ui.line.currentFont().pointSize())*8)
		#self.ui.lineWidget.setMaximumHeight(int(self.ui.line.currentFont().pointSize())*8)
		self.ui.splitter.setSizes([500,120])
		self.ui.splitter_2.setSizes([45,500,70])

	#def lines(self):
		#if self.ui.line.verticalScrollBar().isVisible():
			#self.ui.line.setMaximumHeight(int(self.ui.line.maximumHeight())+int(self.ui.line.currentFont().pointSize())+10)

	def changeAffiliation(self,affiliation):
		if affiliation=="owner":
			self.ui.admin.show()
		self.affiliation=affiliation

	def roomAdminClicked(self):
		if self.affiliation=="owner":
			self.chatadmin=groupchatAdminWindow(self,self.main,self.jab)
			self.jab.getGroupchatAdminList(self.jid,role="moderator")
			self.jab.getGroupchatAdminList(self.jid,affiliation="owner")
			self.jab.getGroupchatAdminList(self.jid,affiliation="member")
			self.jab.getGroupchatAdminList(self.jid,affiliation="outcast")
			self.jab.getGroupchatAdminList(self.jid,affiliation="admin")
			self.chatadmin.show()

	def roomConfigClicked(self):
		self.jab.getGroupchatConfig(self.jid)

	#def deleteUser(self,jid,nick):
		#user=self.main.getGroupChatMember(jid,unicode(nick))
		#parent=user.parent()
		#parent.takeChild(int(parent.indexOfChild(user)))
		#self.main.groupchat[jid][1].remove(user)
		#self.refreshStats()

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
		if nick in self.main.client.groupchats[self.jid].users.keys():
			if self.main.client.groupchats[self.jid].users[nick].item!=None:
				return self.main.client.groupchats[self.jid].users[nick].item
		return False

	def removeUser(self,nick):
		parent=self.main.client.groupchats[self.jid].users[nick].item.parent()
		parent.takeChild(int(parent.indexOfChild(self.main.client.groupchats[self.jid].users[nick].item)))
		self.refreshStats()

	def editUser(self,nick,status,role=None):
		if self.isUser(unicode(nick))==False:
			#user=self.isUser(unicode(nick))
		# Pokud neni v mistnosti, vytvorime jej
		#else:
			if self.roles.has_key(role):
				self.main.client.groupchats[self.jid].users[nick].item=QtGui.QTreeWidgetItem(self.roles[role])
			else:
				self.main.client.groupchats[self.jid].users[nick].item=QtGui.QTreeWidgetItem(self.ui.users)
			self.main.client.groupchats[self.jid].users[nick].item.setText(0,unicode(nick))
		# Nastaveni stavu
		if status!="None":
			self.main.client.groupchats[self.jid].users[nick].item.setIcon(0,self.main.getIcon(status=status,size="16x16"))
			self.main.client.groupchats[self.jid].users[nick].item.setText(1,self.main.shows[self.main.client.groupchats[self.jid].users[nick].show]+unicode(nick.lower()))
		else:
			self.main.client.groupchats[self.jid].users[nick].item.setIcon(0,self.main.getIcon(status="online",size="16x16"))
		# Tooltip
		#user.setToolTip('<font color="blue"><b>'+unicode(user.text(2))+'</b></font><hr>'+unicode(e[2].getStatus())+'<br/><b>Jabber ID: </b>'+str(jid)+'')
		# serazeni
		self.ui.users.sortItems (1,QtCore.Qt.AscendingOrder)
		self.refreshStats()

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

			self.main.client.sendMessage(self.jid, unicode(text, 'utf-8'), 'groupchat')
			self.ui.line.clear()
			self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
			#self.ui.line.setMaximumHeight(int(self.ui.line.currentFont().pointSize())+15)

	def tabPressed(self):
		# nick completion
		text=unicode(self.ui.line.toPlainText()).lower()
		if len(text)==0:
			return
		text=text[0]
		repeat=False
		users=self.main.client.groupchats[self.jid].users.keys()
		for i in range(len(users)):
			if unicode(users[i]).lower()[:len(text)]==text and i>self.name_id:
				cur=self.ui.line.textCursor()
				cur.movePosition(QtGui.QTextCursor.End)
				self.ui.line.setTextCursor(cur)
				self.ui.line.setPlainText(users[i]+": ")
				cur=self.ui.line.textCursor()
				cur.movePosition(QtGui.QTextCursor.End)
				self.ui.line.setTextCursor(cur)
				self.name_id=i
				return
			if unicode(users[i]).lower()[:len(text)]==text:
				repeat=True
		self.name_id=-1
		if repeat==True:
			self.tabPressed()
			
