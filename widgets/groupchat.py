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
#from groupchatadmin import *
from configobj import ConfigObj
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

class normalLineEditWidget(QtGui.QTextEdit):
	def __init__(self,main,parent=None):
		apply(QtGui.QTextEdit.__init__,(self,parent))
		self.main=main
		self.parent=parent
		#self.setMaximumSize(QtCore.QSize(16777215,30))
		self.setObjectName("line")
	
	def keyPressEvent(self,event):
		key=event.key()
		if (key==QtCore.Qt.Key_Return or key==QtCore.Qt.Key_Enter) and (event.modifiers() & QtCore.Qt.ControlModifier or event.modifiers() & QtCore.Qt.ShiftModifier):
			QtGui.QTextEdit.keyPressEvent(self,event)
		elif key==QtCore.Qt.Key_Return or key==QtCore.Qt.Key_Enter:
			self.main.sendButtonClicked()
		else:
			QtGui.QTextEdit.keyPressEvent(self,event)

class groupChatWidget(QtGui.QWidget):
	def __init__(self,main,jid,jab,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.jab=jab
		self.ui=Ui_groupchatwidget()
		self.ui.setupUi(self)
		self.main=main
		self.affiliation=""
		self.cache={}
		self.lines=0
		self.maxLines=300

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
		layout.addWidget(self.ui.line)

		#self.buttonGroup=QtGui.QButtonGroup(self.ui.logs)
		##self.buttonGroup.setExclusive(True)
		#self.ui.logsLayout=QtGui.QHBoxLayout(self.ui.logs)
		
		#self.actual=QtGui.QPushButton(self.tr("Actual"),self.ui.logs)
		#self.actual.setCheckable(True)
		#self.actual.setChecked(True)
		#self.ui.logsLayout.addWidget(self.actual)
		#self.buttonGroup.addButton(self.actual)

		QtCore.QObject.connect(self.ui.sendButton, QtCore.SIGNAL("clicked ()"),self.sendButtonClicked)
		QtCore.QObject.connect(self.ui.roomConfig, QtCore.SIGNAL("clicked ()"),self.roomConfigClicked)
		QtCore.QObject.connect(self.ui.roomAdmin, QtCore.SIGNAL("clicked ()"),self.roomAdminClicked)
		#QtCore.QObject.connect(self.buttonGroup, QtCore.SIGNAL("buttonClicked ( QAbstractButton * )  "),self.logButton)
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
		self.addRole("participant",self.tr("Participants"))
		self.addRole("moderator",self.tr("Moderators"))
		self.addRole("visitor",self.tr("Visitors"))
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

	def getUserItems(self,name):
		items=self.ui.users.findItems(unicode(name), QtCore.Qt.MatchFixedString|QtCore.Qt.MatchRecursive,0)
		if len(items)!=0:
			return items
		return []

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
		if len(self.getUserItems(nick))==0:
			return False
		return True

	def removeUser(self,nick):
		item=self.getUserItems(nick)[0]
		parent=item.parent()
		parent.takeChild(int(parent.indexOfChild(item)))
		self.refreshStats()

	def editUser(self,nick,status,role=None):
		if self.isUser(unicode(nick))==False:
			if self.roles.has_key(role):
				item=QtGui.QTreeWidgetItem(self.roles[role])
			else:
				item=QtGui.QTreeWidgetItem(self.ui.users)
			item.setText(0,unicode(nick))
		else:
			item=self.getUserItems(nick)[0]
		# Nastaveni stavu
		if status!="None":
			item.setIcon(0,self.main.getIcon(status=status,size="16x16"))
			item.setText(1,self.main.shows[status]+unicode(nick.lower()))
		else:
			item.setIcon(0,self.main.getIcon(status="online",size="16x16"))
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

	def logButton(self,button):
		if button==self.actual:
			self.ui.textEdit.setHtml(self.cache['actual'])
		else:
			time=unicode(button.text())
			self.cache['actual']=self.ui.textEdit.toHtml()
			self.ui.textEdit.setHtml(self.cache[time])

	def textEditWrite(self,text):
		#if self.actual.isChecked():
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
			cursor.endEditBlock()
			if toEnd:
				self.ui.textEdit.verticalScrollBar().setValue(self.ui.textEdit.verticalScrollBar().maximum())
		#else:
			#self.cache['actual']+=text

		#self.lines+=1
		#if self.lines>self.maxLines:
			#self.lines=0
			#self.cache[self.main.now()]=self.ui.textEdit.toHtml()
			#self.ui.textEdit.setHtml("")
			#button=QtGui.QPushButton(self.main.now(),self.ui.logs)
			#button.setCheckable(True)
			#self.ui.logsLayout.addWidget(button)
			#self.buttonGroup.addButton(button)

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
		# sends message
		if len(unicode(self.ui.line.toPlainText()))!=0:
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
			self.main.client.sendMessage(self.jid, text, 'groupchat')
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
			
