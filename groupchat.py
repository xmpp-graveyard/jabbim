try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from groupchatwidget_ui import *
from groupchatadmin import *
from configobj import ConfigObj

class groupChatWidget(QtGui.QWidget):
	def __init__(self,main,jid,jab,affiliation,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.jab=jab
		self.ui=Ui_groupchatwidget()
		self.ui.setupUi(self)
		self.main=main
		self.affiliation=affiliation
		QtCore.QObject.connect(self.ui.sendButton, QtCore.SIGNAL("clicked ()"),self.sendButtonClicked)
		QtCore.QObject.connect(self.ui.roomConfig, QtCore.SIGNAL("clicked ()"),self.roomConfigClicked)
		QtCore.QObject.connect(self.ui.roomAdmin, QtCore.SIGNAL("clicked ()"),self.roomAdminClicked)
		QtCore.QObject.connect(self.ui.line, QtCore.SIGNAL("returnPressed ()"),self.sendButtonClicked)
		QtCore.QObject.connect(self.ui.smileys, QtCore.SIGNAL("clicked (bool)"),self.smileysClicked)
		short=QtGui.QShortcut("tab",self.ui.line)
		QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.tabPressed)
		self.ui.info_big.hide()
		self.loadSmileys()
		self.jid=jid
		self.name_id=-1 # for tabPressed
		self.roles={}
		self.addRole("participant","Participants")
		self.addRole("moderator","Moderators")
		self.addRole("visitor","Visitors")
		self.ui.users.header().hide()
		self.ui.users.hideColumn(1)

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

	def deleteUser(self,jid,nick):
		user=self.main.getGroupChatMember(jid,unicode(nick))
		parent=user.parent()
		parent.takeChild(int(parent.indexOfChild(user)))
		self.main.groupchat[jid][1].remove(user)
		self.refreshStats()

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

	def editUser(self,jid,nick,status,role,affiliation=None):
		if self.main.isGroupChatMember(jid,unicode(nick)):
			user=self.main.getGroupChatMember(jid,unicode(nick))
		# Pokud neni v mistnosti, vytvorime jej
		else:
			if self.roles.has_key(role):
				user=QtGui.QTreeWidgetItem(self.roles[role])
			else:
				user=QtGui.QTreeWidgetItem(self.ui.users)
			user.setText(0,unicode(nick))
			self.main.groupchat[jid][1].append(user)
		# Nastaveni stavu
		if status!="None":
			user.setIcon(0,self.main.getIcon(status=status,size="16x16"))
			#user.setText(1,self.nickSort[str(e[2].getShow())]+unicode(user.text(2)))
		else:
			user.setIcon(0,self.main.getIcon(status="online",size="16x16"))
		# Tooltip
		#user.setToolTip('<font color="blue"><b>'+unicode(user.text(2))+'</b></font><hr>'+unicode(e[2].getStatus())+'<br/><b>Jabber ID: </b>'+str(jid)+'')
		# serazeni
		self.ui.users.sortItems (0,QtCore.Qt.AscendingOrder)
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
			text=text.replace(" "+k,'<img src="images/16x16/emotes/'+v+'"/>')
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
		self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)

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
		for i in range(len(self.main.groupchat[self.jid][1])):
			if unicode(self.main.groupchat[self.jid][1][i].text(0)).lower()[:len(text)]==text and i>self.name_id:
				self.ui.line.setText(self.main.groupchat[self.jid][1][i].text(0)+": ")
				self.name_id=i
				return
			if unicode(self.main.groupchat[self.jid][1][i].text(0)).lower()[:len(text)]==text:
				repeat=True
		self.name_id=-1
		if repeat==True:
			self.tabPressed()
			