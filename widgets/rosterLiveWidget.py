"""
Copyright (C) 2007 	Jan 'Hanzz' Kaluza (hanzz at njs.netlab.cz)
Copyright (C) 2007	Jiri 'Sef' Gabrys	(sef at njs.netlab.cz)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See theF
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""
import sys,os

try: from PyQt4 import QtCore, QtGui
except: print "PyQt4 is not installed."
from os.path import basename
from twisted.python import log
from twisted.words.protocols.jabber import jid as jidT
import time
import filetransfer
import albumfiletransfer
import addcontact
import vcardeditor
import commands
from include import rot13

class activeWidget(QtGui.QWidget):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.setObjectName("selectedContact")
		self.parent=parent
		
		# main layout
		l=QtGui.QGridLayout(self)
		l.setMargin(2)
		l.setSpacing(0)
		self.setAutoFillBackground(False)
		
		# layout for JID, jidLabel is virtual widget for resizing layout row to 22px
		l4=QtGui.QHBoxLayout()
		self.jidLabel=QtGui.QWidget(self)
		self.jidLabel.setMinimumHeight(30)
		self.jidLabel.setMaximumHeight(30)
		self.jidLabel.setMinimumWidth(1)
		self.jidLabel.setMaximumWidth(1)

		# adding jidLabel to the main layout
		l4.addStretch()
		l4.addWidget(self.jidLabel)
		l.addLayout(l4,0,0)

		# QTextEdit for status message
		self.statusLabel=QtGui.QTextEdit(self)
		self.statusLabel.setObjectName("selectedContactStatus")
		self.statusLabel.hide()
		self.statusLabel.setFrameShape(QtGui.QFrame.NoFrame)
		self.statusLabel.setFrameShadow(QtGui.QFrame.Plain)
		self.statusLabel.setMaximumHeight(30)
		self.statusLabel.setReadOnly(True)
		self.statusLabel.viewport().setAutoFillBackground(False)
		self.statusLabel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		l.addWidget(self.statusLabel,1,0)

		# layout and buttonGroup for buttons if contact is metacontact
		self.layout2=QtGui.QHBoxLayout()
		self.layout2.setMargin(0)
		self.layout2.setSpacing(0)
		self.buttons={}
		self.group=QtGui.QButtonGroup(self)
		
		self.layout2.addStretch()
		QtCore.QObject.connect(self.group,QtCore.SIGNAL("buttonClicked ( QAbstractButton * )"),self.clicked)
		l.addLayout(self.layout2,3,0,QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

		# menu button, maybe we can delete this part in future
		self.menu=QtGui.QPushButton(self)
		self.menu.setIcon(QtGui.QIcon("images/22x22/apps/jabbim.png"))
		self.menu.setMinimumHeight(26)
		self.menu.setMaximumHeight(26)
		self.menu.setFocusPolicy(QtCore.Qt.NoFocus)
		self.menu.setFlat(True)
		l.addWidget(self.menu,2,0,QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
		self.menu.setObjectName("rosterMenu")

		# label for avatar
		self.label=QtGui.QLabel(self)
		l.addWidget(self.label,0,1,5,1,QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)

		l.setRowStretch(4,10)


	def setData(self,item,buttons):
		# sets new data for activeWidget
		self.item=item
		# sets new menu (in future delete this part?)
		menu=self.parent.buildContactMenu(item.jid,item.group)
		self.menu.setMenu(menu)
		self.menu.hide()
		
		# sets status message
		status=self.item.statusMessage
		if status:
			self.statusLabel.show()
			if self.parent.theme:
				self.statusLabel.setHtml("<font size=\"-1\">"+unicode(status)+"</font>")
			else:
				self.statusLabel.setHtml("<font size=\"-1\" color=\""+self.parent.palet.color(QtGui.QPalette.HighlightedText).name()+"\">"+unicode(status)+"</font>")
		else:
			self.statusLabel.hide()
		#print "privacy2"
		# delete old metacontact buttons
		for button,meta in self.buttons.iteritems():
			self.layout2.removeWidget(button)
			self.group.removeButton(button)
			button.setParent(None)
		for i in range(len(self.buttons.values())):
			del self.buttons.values()[0]
		self.buttons={}
		#print "privacy3"
		# add new metacontact buttons
		for b in buttons:
			meta=b[0]
			icon=b[1]
			#if b=="separator":
				#line = QtGui.QFrame(self)
				#line.setFrameShape(QtGui.QFrame.VLine)
				#line.setFrameShadow(QtGui.QFrame.Sunken)
				#layout2.addWidget(line)
			#else:
			button = QtGui.QPushButton(self)
			#button.setGeometry(0,y+16,16,16)
			button.setFocusPolicy(QtCore.Qt.NoFocus)
			button.setMaximumSize(16,16)
			button.setFlat(True)
			button.setIcon(icon)
			self.layout2.insertWidget(0,button)
			self.group.addButton(button)
			self.buttons[button]=meta
		#print "privacy4"
		# sets avatar
		size=64
		#if len(buttons)==0 and not status:
			#size=32
		self.label.setMaximumSize(size,size)
		if self.item.avatar:
			pixmap=self.item.selectedFrameAvatar.pixmap(size,size)
			self.label.setPixmap(pixmap)
			self.label.setMinimumHeight(pixmap.height())
			self.label.show()
		else:
			self.label.hide()
		#print "privacy5"
		# resize activeWidget according to userItem size
		self.resize(self.parent.width()-46,self.parent.selectedHeight+32)

	def refreshData(self):
		# sets changed data (changed by clicked() slot)
		# sets status message
		status=self.item.statusMessage
		if status:
			self.statusLabel.show()
			self.statusLabel.setHtml("<font size=\"-1\">"+unicode(status)+"</font>")
		else:
			self.statusLabel.hide()

		# sets avatar
		size=64
		self.label.setMaximumSize(size,size)
		if self.item.avatar:
			pixmap=self.item.selectedFrameAvatar.pixmap(size,size)
			self.label.setPixmap(pixmap)

		# resize activeWidget according to userItem size
		self.resize(self.parent.width()-46,self.parent.selectedHeight-32)

	def clicked(self,button):
		# sets item properties according to metaItem, which is represented by button
		meta=self.buttons[button]
		self.item.name=meta.name
		self.item.escapedName=meta.escapedName
		self.item.frameAvatar=meta.frameAvatar
		self.item.selectedFrameAvatar=meta.selectedFrameAvatar
		self.item.icon=meta.icon
		self.item.avatar=meta.avatar
		self.item.status=meta.status
		self.item.statusMessage=meta.statusMessage
		self.item.jid=meta.jid
		self.parent.repaint()
		self.refreshData()

class groupItem:
	def __init__(self,name,icon,main):
		self.name=name
		self.icon=icon
		self.expanded=False
		self.typ='group'
		self.main=main
		self.online=0
		self.all=0
		self.escapedName=name.replace("<","&lt;").replace(">","&gt;")

	def setExpanded(self,bool):
		self.expanded=bool
		if not self.expanded:
			self.icon=QtGui.QIcon("images/"+self.main.iconSize+"/icons/group-closed.png")
		else:
			self.icon=QtGui.QIcon("images/"+self.main.iconSize+"/icons/group-open.png")

class userItem:
	"""
	Class for users roster items
	"""
	def __init__(self,name,group,jid,main,icon=None):
		self.name=name #: contact name
		self.icon=icon #: contact icon
		self.typ='user' #: typ of item, constant for user items
		self.group=group #: group of contact
		self.status=9
		self.statusMessage=None #: statusMessage
		self.main=main #: rosterWidget
		self.avatar=None
		self.hidden=False
		#self.test=None
		self.metajid="" #: contains parent jid of this item, if this contact is member of metacontacts
		self.blink=None # if True, icon blinks
		self.jid = jid
		self.privacy = {"block":False, "allow":False, "hide":False}
		self.hiddenBySearch=False
		self.transport=False
		self.escapedName=name.replace("<","&lt;").replace(">","&gt;")

	def clone(self):
		"""
		Makes new instance of userItem which is copy of current userItem
		"""
		item=userItem(unicode(self.name),unicode(self.group),self.jid,self.main,self.icon)
		item.statusMessage=self.statusMessage
		item.avatar=self.avatar
		item.hidden=self.hidden
		item.jid=unicode(self.jid)
		item.metajid=unicode(self.metajid)
		item.status=int(self.status)
		item.frameAvatar=self.frameAvatar
		item.privacy['block']=self.privacy['block']
		item.privacy['allow']=self.privacy['allow']
		item.privacy['hide']=self.privacy['hide']
		item.selectedFrameAvatar=self.selectedFrameAvatar
		return item

	def setIcon(self,icon):
		"""
		Sets userItem icon
		@type icon: QtGui.QIcon
		"""
		self.icon=icon
		self.main.repaint()
	
	def setAvatar(self,icon):
		"""
		Sets userItem's avatar. Frame is painted automaticaly by this function.
		@type icon: QtGui.QIcon
		"""
		self.avatar=icon
		self.frameAvatar=QtGui.QIcon(self.main.main.getAvatar(self.avatar.pixmap(30,30),size="32x32",frame=True))
		self.selectedFrameAvatar=QtGui.QIcon(self.main.main.getAvatar(self.avatar.pixmap(60,58),size="64x64",frame=True))
	
	def setHidden(self,hidden):
		"""
		Hide or show userItem
		@type hidden: boolean
		"""
		self.hidden=hidden
		self.main.repaint()

class special:
	"""
	special item for contact which aren't in any group
	"""
	def __init__(self):
		self.typ="group"
		self.main="special"
		#self.name=".#$%^&*()_.@#$%^&*(((((((((("
		self.name="zzzzzzzzzzzzzzzzzzzzzz%%%$@#@^&"
		self.expanded=True

class rosterWidget(QtGui.QWidget):
	"""
	RosterLiveWidget class.
	"""
	def __init__(self,parent=None,main=None):
		QtGui.QWidget.__init__(self,parent)
		self.main=main
		self.groups={}
		self.specialName="zzzzzzzzzzzzzzzzzzzzzz%%%$@#@^&"
		#self.specialName=".#$%^&*()_.@#$%^&*(((((((((("
		self.groups[self.specialName]=special()
		self.users=[]
		self.iconSize="32x32"
		self.setObjectName("mainRosterWidget")
		self.setMinimumWidth(150)
		self.setMinimumHeight(150)
		self.setAcceptDrops(True)
		self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
		self.setMouseTracking(True)
		self.setFocusPolicy(QtCore.Qt.ClickFocus)

		self.selected=None
		self.selectedHeight=0
		self.showOffline=False
		self.newitem=None
		self.item=None
		self.sortedGroups=[]
		self.sorted={}
		self.statusLabel=activeWidget(self)
		self.buttonWidget=None
		self.bigAvatar=False
		self.data={}
		self.metaItems={}
		self.events=[]
		self.bl=True
		self.changePos=False
		self.searchMode=False
		self.reshow=False
		self.userHeight=32
		self.groupHeight=32
		self.theme=True
		self.timestamp=0
		self.scrollUp = None
		self.compact=False

		self.timer=QtCore.QTimer(self) # timer for drag and drop
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.popup)
		self.timerBlink=QtCore.QTimer(self) # timer for blinking
		QtCore.QObject.connect(self.timerBlink, QtCore.SIGNAL("timeout ()"),self.blink)

		self.colors=QtGui.QTreeWidget(self.main)
		self.colors.hide()
		self.colors.setObjectName("rosterView")

		self.reskin()
		self.blinkJids=[]
		self.main.ui.rosterSearch.hide()
		self.main.ui.rosterSearchLabel.hide()

	def disconnect(self):
		"""
		Resets roster. Called by mainWindow on disconnect
		"""
		self.groups={}
		#self.specialName=".#$%^&*()_.@#$%^&*(((((((((("
		self.specialName="zzzzzzzzzzzzzzzzzzzzzz%%%$@#@^&"
		self.groups[self.specialName]=special()

	def refreshEvents(self):
		"""
		Blinks with userItem icon if there is some event for userItem with event's JID.
		"""
		events=[]
		for event in self.main.events.events:
			if event['type']=="message":
				JID=jidT.JID(event['name']).userhost()
				if not JID in self.blinkJids:
					self.blinkJids.append(JID)
				events.append(JID)
				for item in self.getUserItems(JID):
					item.blink=QtGui.QIcon(event['iconName'].replace("xxxxx","32x32"))
					self.events.append(item)
		for jid in self.blinkJids:
			if not jid in events:
				for item in self.getUserItems(jid):
					if item in self.events:
						self.events.remove(item)
		self.timerBlink.start(500)

	def blink(self):
		self.bl=not self.bl
		if len(self.main.events.events)>0:
			#log.msg("blink")
			self.repaint()
		else:
			self.timerBlink.stop()
			self.bl=True
			self.repaint()

	def reskin(self,style=None):
		"""
		Reload roster skin
		"""


		if self.theme==True:
			self.colors.setObjectName("rosterView")
		else:
			self.colors.setObjectName("rosterView2")

		self.palet=self.colors.palette()
		
		self.palette().setColor(QtGui.QPalette.Window,self.palet.color(QtGui.QPalette.Base))
		self.repaint()

	def sortItems(self,column=None,typ=None):
		"""
		Sort groups and users in groups and count online/offline users
		"""
		self.sortedGroups=self.groups.keys()
		self.sortedGroups.sort()
		for group in self.sortedGroups:
			temp=[]
			for user in self.getGroupUsers(group):
				temp.append([unicode(user.status)+user.name,user])
			temp.sort()
			self.sorted[group]=temp

			all=0
			online=0
			for user in self.users:
				if user.group==group:
					all+=1
					if unicode(user.status)!="9":
						online+=1
			self.groups[group].online=online
			self.groups[group].all=all

		self.setSize()

	def event(self,event):
		# tooltip request:
		if int(event.type())==110:
			item=self.itemAt(int(event.x()),int(event.y()),1)[0] # get item in coordinates
			self.setToolTip("")
			if len(item)!=0:
				item=item[0]
				if item!=None and item.typ=="user": # tooltips are only for contacts (not for groups)
					text='<table><tr>'
					if item.avatar!=None and os.path.isfile(self.main.homeDir+'/avatars/'+unicode(item.jid)):
						pixmap=item.avatar.pixmap(64,64)
						text+='<td><img src="'+self.main.homeDir+'/avatars/'+unicode(item.jid)+'" width="'+str(pixmap.width())+'" height="'+str(pixmap.height())+'"/></td>'
					text+='<td><b>'+self.tr("Name:")+'</b> '+item.escapedName+'<br/>'
					text+='<b>'+self.tr("JID:")+'</b> '+item.jid+'<br/>'
					contact = self.main.client.roster["users"][item.jid]
					if unicode(contact.subscription) == 'from':
						text+='<b>'+self.tr("Subscription:")+'</b> '+self.tr(" from")+'<br/>'
					elif unicode(contact.subscription) == 'to':
						text+='<b>'+self.tr("Subscription:")+'</b> '+self.tr(" to")+'<br/>'
					elif unicode(contact.subscription) == 'none':
						text+='<b>'+self.tr("Subscription:")+'</b> '+self.tr(" none")+'<br/>'	
						
					for res in contact.resources.keys():
						status = contact.resources[res].status
						if not status:
							status = ""
						priority = contact.resources[res].priority
						#if priority == None:
						#	priority = self.tr("Unknown")
						if priority != None:
							priority = "(%s: %s)" % (self.tr("Priority"),priority)
						else:
							priority = ""
						text+='<img src="images/16x16/status/jabber-%s.png">' % contact.resources[res].show # hodilo by se rozlisit k jakymu poatri transportu
						if res != None:
							text+='<b>%s</b> %s<br>' % (res, priority)
						text+='<font size="-1">%s</font>' % (status)
					text+="</td></tr></table>"
					self.setToolTip(text)
		return QtGui.QWidget.event(self,event)

	def mouseMoveEvent(self,event):
		"""
		starts drag and drop if mouse button is pressed
		"""
		item,x,y=self.itemAt(int(event.x()),int(event.y()),1)
		if item:
			if event.buttons()!=QtCore.Qt.NoButton:
				if item[0].typ=='user' and len(self.data)==0:
					mimeData = QtCore.QMimeData()
					mimeData.setText(item[0].jid) # mimedata is users jid
					self.data[mimeData]=item[0] # we have to find the item if user drop it
					self.drag = QtGui.QDrag(self)
					self.drag.setMimeData(mimeData)
					
					f=QtGui.QApplication.font()
					f.setPixelSize(11)
					f.setBold(True)

					metrics=QtGui.QFontMetrics(f)
					width=int(metrics.width(item[0].name))
					
					avatar=item[0].avatar.pixmap(64,64)
					
					result=QtGui.QPixmap(avatar.width()+width+6,avatar.height()+4)
					result.fill(QtGui.QColor(0,0,0))
					painter=QtGui.QPainter(result)
					painter.fillRect(1,1,result.width()-2,result.height()-2,QtGui.QBrush(self.palet.color(QtGui.QPalette.Base)))
					painter.drawPixmap(2,2,avatar)
					painter.setFont(f)
					painter.drawText(QtCore.QRectF(avatar.width()+3,0,width,avatar.height()),QtCore.Qt.AlignCenter,item[0].name)
					painter.end()

					self.drag.setPixmap(result)
					QtCore.QObject.connect(self.drag,QtCore.SIGNAL("targetChanged ( QWidget * )"),self.dtc)
					dropAction = self.drag.start(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)
			elif len(self.data)!=0:
				self.data={}
				
		return QtGui.QWidget.mouseMoveEvent(self,event)

	def dtc(self,widget):
		if widget!=self and self.selected:
			self.selected=None
			self.repaint()
			
		
	#def dndmessage(self,text):
		#if self.main.client.roster['users'].has_key(text):
			#return "presunout kontakt/vytvorit metakontakt"

	def popup(self):
		"""
		called by timer if user wants to use autoscroll when DNDs the item
		"""
		if self.scrollUp==None:
			self.timer.stop()
		if not self.scrollUp:
			if self.main.scroll.verticalScrollBar().value()+10>self.main.scroll.verticalScrollBar().maximum():
				self.main.scroll.verticalScrollBar().setValue(self.main.scroll.verticalScrollBar().maximum())
				self.timer.stop()
			else:
				self.main.scroll.verticalScrollBar().setValue(self.main.scroll.verticalScrollBar().value()+10)
		else:
			if self.main.scroll.verticalScrollBar().value()-10<0:
				self.main.scroll.verticalScrollBar().setValue(0)
				self.timer.stop()
			else:
				self.main.scroll.verticalScrollBar().setValue(self.main.scroll.verticalScrollBar().value()-10)

	def addGroup(self,name):
		"""
		add new group
		@type name: unicode
		@rtype: groupItem
		@return: created groupItem
		"""
		item=groupItem(name,QtGui.QIcon("images/"+self.iconSize+"/icons/group-closed.png"),self)
		self.groups[name]=item
		self.repaint()
		return item

	def addUser(self,jid,name,group):
		"""
		add new user
		@type jid: unicode
		@type name: unicode
		@type group: unicode
		@rtype: userItem
		@return: created userItem
		"""
		if len(name)==0:
			name=jid
		if not group:
			group=self.specialName
		item=userItem(name,group,jid,self)
		item.icon=self.main.getIcon(jid,size="32x32",status=self.main.icons["9"])
		item.hidden=True
		item.setAvatar(QtGui.QIcon("images/48x48/apps/jabbim.png"))
		self.users.append(item)

	def getGroupUsers(self,group):
		"""
		get user items according to show online from `group`
		@type group: unicode
		@rtype: list
		@return: list of userItem
		"""
		ret=[]
		for user in self.users:
			if self.showOffline==True:
				if user.group==group:
					ret.append(user)
			else:
				if user.group==group and not user.hidden:
					ret.append(user)
		return ret

	def getAllGroupUsers(self,group):
		ret=[]
		for user in self.users:
			if user.group==group:
				ret.append(user)
		return ret

	def getGroupSortedUsers(self,group):
		"""
		get all users from group. Returned list is sorted and depends on self.showOffline variable.
		@type group: unicode
		@rtype: list
		@return: sorted list of userItem
		"""
		ret=[]
		transport=self.main.config['showTransports']
		for key in self.sorted[group]:
			user=key[1]
			if self.showOffline==True and not user.hiddenBySearch:
				if user.group==group:
					if (transport=="False" and user.transport==False) or transport=="True":
						ret.append(user)
			else:
				if user.group==group and not user.hidden and not user.hiddenBySearch:
					if (transport=="False" and user.transport==False) or transport=="True":
						ret.append(user)
		return ret

	def paintCompactGroupItem(self,painter,item,x,y):
		"""
		paints group item in compact roster
		"""
		if item.main=="special":
			# we don't want to paint `special` item
			return

		# set the font size for text
		doc=QtGui.QTextDocument()
		#font=doc.defaultFont()
		font=QtGui.QApplication.fontMetrics()
		fontHeight=int(font.height())
		#font.setPixelSize(12)
		#doc.setDefaultFont(font)

		# paint background of item
		painter.save()
		painter.translate(x,y)
		painter.fillRect(0,0,self.width(),22,QtGui.QBrush(self.main.ui.groupStyleWidget.palette().window()))
		painter.restore()

		
		p=painter.pen()
		painter.setPen(self.main.ui.groupStyleWidget.palette().color(QtGui.QPalette.Text))

		#painter.save()
		#painter.translate(x,y+5)
		#painter.drawText(self.width()-52,12,unicode(item.online))
		#painter.drawPixmap(self.width()-45,0,self.main.getIcon(status="online",size="16x16").pixmap(16,16))
		#painter.drawText(self.width()-28,12,unicode(item.all))
		#painter.drawPixmap(self.width()-21,0,self.main.getIcon(status="offline",size="16x16").pixmap(16,16))
		#painter.restore()

		painter.setPen(p)
		
		if item.icon:
			painter.drawPixmap(x,y,item.icon.pixmap(22,22))

		#doc.setHtml("<font color=\""+self.main.ui.groupStyleWidget.palette().color(QtGui.QPalette.Text).name()+"\">"+item.escapedName+" ("+str(item.online)+"/"+str(item.all)+")</font>")

		#painter.save()
		#painter.translate(x+30,y+(22-fontHeight)/2)
		#doc.drawContents(painter, QtCore.QRectF(0,0,self.width(),y+20))
		#painter.restore()

		# write the name of the group
		doc.setHtml("<font color=\""+self.main.ui.groupStyleWidget.palette().color(QtGui.QPalette.Text).name()+"\">"+item.escapedName+"</font>")
		painter.save()
		painter.translate(x+30,y+(22-fontHeight)/2)
		doc.drawContents(painter, QtCore.QRectF(0,0,self.width(),y+22))
		painter.restore()
		width=int(font.width("("+str(item.online)+"/"+str(item.all)+")"))
		doc.setHtml("<font color=\""+self.main.ui.groupStyleWidget.palette().color(QtGui.QPalette.Text).name()+"\">("+str(item.online)+"/"+str(item.all)+")</font>")
		painter.save()
		painter.translate((int(self.width())-width-6),y+(22-fontHeight)/2)
		doc.drawContents(painter, QtCore.QRectF(0,0,width+15,y+20))
		painter.restore()

	def paintGroupItem(self,painter,item,x,y):
		"""
		paints group item in normal roster
		"""
		if item.main=="special":
			return
		
		# set font
		doc=QtGui.QTextDocument()
		font=QtGui.QApplication.fontMetrics()
		fontHeight=int(font.height())
		#font.setPixelSize(12)
		#doc.setDefaultFont(font)

		# paint background
		painter.save()
		painter.translate(x,y)

		if item==self.selected:
			if self.theme:
				painter.fillRect(0,0,self.width(),30,QtGui.QBrush(self.main.ui.selectedItemStyle.palette().window()))
			else:
				painter.fillRect(0,0,self.width(),30,QtGui.QBrush(self.main.ui.selectedItemStyle.palette().color(QtGui.QPalette.Highlight)))
		else:
			if self.theme:
				painter.fillRect(0,0,self.width(),30,QtGui.QBrush(self.main.ui.groupStyleWidget.palette().window()))
			else:
				painter.fillRect(0,0,self.width(),30,QtGui.QBrush(self.main.ui.groupStyleWidget.palette().color(QtGui.QPalette.AlternateBase)))
		
		painter.restore()
		
		# draw status icon of item
		if item.icon:
			painter.drawPixmap(x,y,item.icon.pixmap(32,32))

		if item==self.selected:
			if self.theme:
				fontcolor=self.main.ui.groupStyleWidget.palette().color(QtGui.QPalette.Text).name()
			else:
				fontcolor=self.palet.color(QtGui.QPalette.HighlightedText).name()
		else:
			fontcolor=self.main.ui.groupStyleWidget.palette().color(QtGui.QPalette.Text).name()


		# write the name of the group
		doc.setHtml("<font color=\""+fontcolor+"\">"+item.escapedName+"</font>")
		painter.save()
		painter.translate(x+30,y+(32-fontHeight)/2)
		doc.drawContents(painter, QtCore.QRectF(0,0,self.width(),y+32))
		painter.restore()
		width=int(font.width("("+str(item.online)+"/"+str(item.all)+")"))
		doc.setHtml("<font color=\""+fontcolor+"\">("+str(item.online)+"/"+str(item.all)+")</font>")
		painter.save()
		painter.translate((int(self.width())-width-6),y+(32-fontHeight)/2)
		doc.drawContents(painter, QtCore.QRectF(0,0,width+15,y+32))
		painter.restore()

	def resizeEvent(self,event):
		"""
		resizes activeWidget if roster is resized
		"""
		if self.statusLabel:
			self.statusLabel.resize(self.width()-46,self.selectedHeight-32)
		return QtGui.QWidget.resizeEvent(self,event)

	def paintCompactUserItem(self,painter,useritem,x,y):
		if useritem==self.item:
			if self.metaItems.has_key(useritem.metajid) or self.main.config['bigOnClick']=="True":

				height=79
				#if not useritem.statusMessage:
					#height-=32
				#if not self.metaItems.has_key(useritem.metajid):
					#height-=16
				self.selectedHeight=height+20
	
	
				# paint roster background
				#painter.save()
				#painter.translate(x,y)
				#painter.fillRect(0,0,self.width(),32,QtGui.QBrush(self.palet.color(QtGui.QPalette.Base)))
				#painter.restore()
	
				# set pen and brush for item background
				b=painter.brush()
				p=painter.pen()
				if self.theme:
					painter.setBrush(self.main.ui.selectedItemStyle.palette().window())
					pen=QtGui.QPen(self.main.ui.selectedItemStyle.palette().color(QtGui.QPalette.Text))
				else:
					painter.setBrush(self.main.ui.selectedItemStyle.palette().color(QtGui.QPalette.Highlight))
					color=self.main.ui.selectedItemStyle.palette().color(QtGui.QPalette.Highlight)
					# Qt4.2 uses .light() but Qt4.3 uses lighter(), so we have to try both of them because of compatibility
					try:
						pen=QtGui.QPen(color.lighter())
					except:
						pen=QtGui.QPen(color.light())
				pen.setWidth(0)
				painter.setPen(pen)
	
				# paint item background and border
				painter.save()
				painter.translate(x,y)
				painter.drawRect(5,5,self.width()-10,height+3)
				painter.restore()
				painter.setBrush(b)
				painter.setPen(p)
				
				# paint user status icon
				if useritem in self.events:
					if self.bl:
						painter.drawPixmap(x+7,y+11,useritem.icon.pixmap(32,32))
					else:
						painter.drawPixmap(x+7,y+11,useritem.blink.pixmap(32,32))
				else:
					if useritem.privacy['block'] or useritem.privacy['hide']:
						painter.drawPixmap(x+7,y+11,self.main.getIcon(status="error",size="32x32").pixmap(32,32))
					else:
						painter.drawPixmap(x+7,y+11,useritem.icon.pixmap(32,32))
	
				# set font
				doc=QtGui.QTextDocument()
				font=QtGui.QApplication.fontMetrics()
				fontHeight=int(font.height())
				#font=doc.defaultFont()
				#font.setPixelSize(12)
				#doc.setDefaultFont(font)
	
				# paint user name 
				res=""
				if len(self.main.client.roster['users'][useritem.jid].resources)>1:
					res=" ("+str(len(self.main.client.roster['users'][useritem.jid].resources))+")"
				if self.theme:
					doc.setHtml("<font color=\""+self.main.ui.userStyleWidget.palette().color(QtGui.QPalette.Text).name()+"\">"+useritem.escapedName+res+"</font>")
				else:
					doc.setHtml("<font color=\""+self.palet.color(QtGui.QPalette.HighlightedText).name()+"\">"+useritem.escapedName+res+"</font>")
				painter.save()
				painter.translate(x+41,y+8+(32-fontHeight)/2)
				if useritem.avatar:
					doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-33-32,y+28))
				else:
					doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-33,y+28))
				painter.restore()
	
				# show activeWidget
				if self.statusLabel:
					if self.reshow:
						buttons=[]
						# get metacontact items
						if self.metaItems.has_key(useritem.metajid) and not self.searchMode:
							for meta in self.metaItems[useritem.metajid]:
								buttons.append([meta,self.main.getIcon(meta.jid,size="16x16",status=self.main.icons[unicode(meta.status)])])
						# change activeWidget data and geometry
						self.statusLabel.setData(useritem,buttons)
						self.statusLabel.setGeometry(41,y+7,self.width()-46,height)
						self.statusLabel.show()
						self.reshow=False
					elif self.changePos:
						self.statusLabel.setGeometry(41,y+7,self.width()-46,height)
						self.changePos=False
			elif self.main.config['bigOnClick']=="False":
				height=28
				self.selectedHeight=28
				#painter.save()
				#painter.translate(x,y)
				#painter.fillRect(0,0,self.width(),32,QtGui.QBrush(self.palet.color(QtGui.QPalette.Base)))
				#painter.restore()


				# set pen and brush for item background
				b=painter.brush()
				p=painter.pen()
				if self.theme:
					painter.setBrush(self.main.ui.selectedItemStyle.palette().window())
					pen=QtGui.QPen(self.main.ui.selectedItemStyle.palette().color(QtGui.QPalette.Text))
				else:
					painter.setBrush(self.main.ui.selectedItemStyle.palette().color(QtGui.QPalette.Highlight))
					color=self.main.ui.selectedItemStyle.palette().color(QtGui.QPalette.Highlight)
					# Qt4.2 uses .light() but Qt4.3 uses lighter(), so we have to try both of them because of compatibility
					try:
						pen=QtGui.QPen(color.lighter())
					except:
						pen=QtGui.QPen(color.light())
				pen.setWidth(0)
				painter.setPen(pen)
	
				# paint item background and border
				painter.save()
				painter.translate(x,y-2)
				painter.drawRect(1,0,self.width()-2,height+2)
				painter.restore()
				painter.setBrush(b)
				painter.setPen(p)


				if useritem in self.events:
					if self.bl:
						painter.drawPixmap(x+7,y,useritem.icon.pixmap(22,22))
					else:
						painter.drawPixmap(x+7,y,useritem.blink.pixmap(22,22))
				else:
					if useritem.privacy['block'] or useritem.privacy['hide']:
						painter.drawPixmap(x+7,y,self.main.getIcon(status="error",size="22x22").pixmap(22,22))
					else:
						painter.drawPixmap(x+7,y,useritem.icon.pixmap(22,22))
				doc=QtGui.QTextDocument()
				font=QtGui.QApplication.fontMetrics()
				fontHeight=int(font.height())
				#font=doc.defaultFont()
				#font.setPixelSize(12)
				#font.setWeight(18)
				#doc.setDefaultFont(font)
				
				if useritem.avatar:
					pixmap=useritem.avatar.pixmap(22,22)
				res=""
				if len(self.main.client.roster['users'][useritem.jid].resources)>1:
					res=" ("+str(len(self.main.client.roster['users'][useritem.jid].resources))+")"

				if self.theme:
					doc.setHtml("<font color=\""+self.main.ui.userStyleWidget.palette().color(QtGui.QPalette.Text).name()+"\">"+useritem.escapedName+res+"</font>")
				else:
					doc.setHtml("<font color=\""+self.palet.color(QtGui.QPalette.HighlightedText).name()+"\">"+useritem.escapedName+res+"</font>")

				painter.save()
				painter.translate(x+41,y+(22-fontHeight)/2)
				if useritem.avatar:
					doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-38-22,y+14))
				else:
					doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-38,y+14))
				painter.restore()
				if useritem.avatar:
					painter.drawPixmap(self.width()-4-32+(int((32-pixmap.width())/2)),y,pixmap)

		else:

			painter.save()
			painter.translate(x,y)
			if self.theme:
				brush=QtGui.QBrush(self.main.ui.userStyleWidget.palette().window())
				if brush.color().alpha()!=0:
					painter.fillRect(0,0,self.width(),22,brush)
			else:
				painter.fillRect(0,0,self.width(),22,QtGui.QBrush(self.palet.color(QtGui.QPalette.Base)))
			painter.restore()



			if useritem in self.events:
				if self.bl:
					painter.drawPixmap(x+7,y,useritem.icon.pixmap(22,22))
				else:
					painter.drawPixmap(x+7,y,useritem.blink.pixmap(22,22))
			else:
				if useritem.privacy['block'] or useritem.privacy['hide']:
					painter.drawPixmap(x+7,y,self.main.getIcon(status="error",size="22x22").pixmap(22,22))
				else:
					painter.drawPixmap(x+7,y,useritem.icon.pixmap(22,22))
			doc=QtGui.QTextDocument()
			font=QtGui.QApplication.fontMetrics()
			fontHeight=int(font.height())
			#font=doc.defaultFont()
			#font.setPixelSize(12)
			#font.setWeight(18)
			#doc.setDefaultFont(font)
			
			if useritem.avatar:
				pixmap=useritem.avatar.pixmap(22,22)
			res=""
			if len(self.main.client.roster['users'][useritem.jid].resources)>1:
				res=" ("+str(len(self.main.client.roster['users'][useritem.jid].resources))+")"

			doc.setHtml("<font color=\""+self.main.ui.userStyleWidget.palette().color(QtGui.QPalette.Text).name()+"\">"+useritem.escapedName+res+"</font>")
			painter.save()
			painter.translate(x+41,y+(22-fontHeight)/2)
			if useritem.avatar:
				doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-38-22,y+14))
			else:
				doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-38,y+14))
			painter.restore()
			if useritem.avatar:
				painter.drawPixmap(self.width()-4-32+(int((32-pixmap.width())/2)),y,pixmap)

	def paintUserItem(self,painter,useritem,x,y):
		"""
		paints user item in normal roster
		"""
		if useritem==self.item:
			if self.metaItems.has_key(useritem.metajid) or self.main.config['bigOnClick']=="True":
				#print useritem.privacy
				# Item is selected
				height=79
				self.selectedHeight=height+10
	
				# paint roster background
				#painter.save()
				#painter.translate(x,y)
				#painter.fillRect(0,0,self.width(),32,QtGui.QBrush(self.palet.color(QtGui.QPalette.Base)))
				#painter.restore()
	
				# set pen and brush for item background
				b=painter.brush()
				p=painter.pen()
				if self.theme:
					painter.setBrush(self.main.ui.selectedItemStyle.palette().window())
					pen=QtGui.QPen(self.main.ui.selectedItemStyle.palette().color(QtGui.QPalette.Text))
				else:
					painter.setBrush(self.main.ui.selectedItemStyle.palette().color(QtGui.QPalette.Highlight))
					color=self.main.ui.selectedItemStyle.palette().color(QtGui.QPalette.Highlight)
					# Qt4.2 uses .light() but Qt4.3 uses lighter(), so we have to try both of them because of compatibility
					try:
						pen=QtGui.QPen(color.lighter())
					except:
						pen=QtGui.QPen(color.light())
				pen.setWidth(0)
				painter.setPen(pen)
	
				# paint item background and border
				painter.save()
				painter.translate(x,y)
				painter.drawRect(5,5,self.width()-10,height+3)
				painter.restore()
				painter.setBrush(b)
				painter.setPen(p)
				
				# paint user status icon
				if useritem in self.events:
					if self.bl:
						painter.drawPixmap(x+7,y+11,useritem.icon.pixmap(32,32))
					else:
						painter.drawPixmap(x+7,y+11,useritem.blink.pixmap(32,32))
				else:
					if useritem.privacy['block'] or useritem.privacy['hide']:
						painter.drawPixmap(x+7,y+11,self.main.getIcon(status="error",size="32x32").pixmap(32,32))
					else:
						painter.drawPixmap(x+7,y+11,useritem.icon.pixmap(32,32))
	
				# set font
				doc=QtGui.QTextDocument()
				font=QtGui.QApplication.fontMetrics()
				fontHeight=int(font.height())
	
				# paint user name 
				res=""
				if len(self.main.client.roster['users'][useritem.jid].resources)>1:
					res=" ("+str(len(self.main.client.roster['users'][useritem.jid].resources))+")"
				if self.theme:
					doc.setHtml("<font color=\""+self.main.ui.userStyleWidget.palette().color(QtGui.QPalette.Text).name()+"\">"+useritem.escapedName+res+"</font>")
				else:
					doc.setHtml("<font color=\""+self.palet.color(QtGui.QPalette.HighlightedText).name()+"\">"+useritem.escapedName+res+"</font>")
				painter.save()
				painter.translate(x+41,y+8+(32-fontHeight)/2)
				if useritem.avatar:
					doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-33-32,y+28))
				else:
					doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-33,y+28))
				painter.restore()
				# show activeWidget
				if self.statusLabel:
					if self.reshow:
						buttons=[]
						# get metacontact items
						if self.metaItems.has_key(useritem.metajid) and not self.searchMode:
							for meta in self.metaItems[useritem.metajid]:
								buttons.append([meta,self.main.getIcon(meta.jid,size="16x16",status=self.main.icons[unicode(meta.status)])])
						# change activeWidget data and geometry
						self.statusLabel.setData(useritem,buttons)
						print "height:",height
						self.statusLabel.setGeometry(41,y+7,self.width()-46,height)
						self.statusLabel.show()
						#self.statusLabel.setGeometry(41,y+7,self.width()-46,height)
						self.reshow=False
					elif self.changePos:
						self.statusLabel.setGeometry(41,y+7,self.width()-46,height)
						self.changePos=False
			elif self.main.config['bigOnClick']=="False":
				height=32
				self.selectedHeight=30
				#painter.save()
				#painter.translate(x,y)
				#painter.fillRect(0,0,self.width(),32,QtGui.QBrush(self.palet.color(QtGui.QPalette.Base)))
				#painter.restore()


				# set pen and brush for item background
				b=painter.brush()
				p=painter.pen()
				if self.theme:
					painter.setBrush(self.main.ui.selectedItemStyle.palette().window())
					pen=QtGui.QPen(self.main.ui.selectedItemStyle.palette().color(QtGui.QPalette.Text))
				else:
					painter.setBrush(self.main.ui.selectedItemStyle.palette().color(QtGui.QPalette.Highlight))
					color=self.main.ui.selectedItemStyle.palette().color(QtGui.QPalette.Highlight)
					# Qt4.2 uses .light() but Qt4.3 uses lighter(), so we have to try both of them because of compatibility
					try:
						pen=QtGui.QPen(color.lighter())
					except:
						pen=QtGui.QPen(color.light())
				pen.setWidth(0)
				painter.setPen(pen)
	
				# paint item background and border
				painter.save()
				painter.translate(x,y-2)
				painter.drawRect(1,0,self.width()-2,height+2)
				painter.restore()
				painter.setBrush(b)
				painter.setPen(p)


				if useritem in self.events:
					if self.bl:
						painter.drawPixmap(x+7,y,useritem.icon.pixmap(32,32))
					else:
						painter.drawPixmap(x+7,y,useritem.blink.pixmap(32,32))
				else:
					if useritem.privacy['block'] or useritem.privacy['hide']:
						painter.drawPixmap(x+7,y,self.main.getIcon(status="error",size="32x32").pixmap(32,32))
					else:
						painter.drawPixmap(x+7,y,useritem.icon.pixmap(32,32))
	
				doc=QtGui.QTextDocument()
				font=QtGui.QApplication.fontMetrics()
				fontHeight=int(font.height())
				#font=doc.defaultFont()
				#font.setPixelSize(12)
				#font.setWeight(18)
				#doc.setDefaultFont(font)
	
				res=""
				if len(self.main.client.roster['users'][useritem.jid].resources)>1:
					res=" ("+str(len(self.main.client.roster['users'][useritem.jid].resources))+")"

				if useritem.avatar:
					pixmap=useritem.frameAvatar.pixmap(32,32)
				if useritem.statusMessage:
					if self.theme:
						doc.setHtml("<font color=\""+self.main.ui.userStyleWidget.palette().color(QtGui.QPalette.Text).name()+"\">"+useritem.escapedName+res+"</font>")
					else:
						doc.setHtml("<font color=\""+self.palet.color(QtGui.QPalette.HighlightedText).name()+"\">"+useritem.escapedName+res+"</font>")
					painter.save()
					painter.translate(x+41,y+2)
					if useritem.avatar:
						doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-43-32,y+32))
					else:
						doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-41,y+32))
					painter.restore()
					if self.theme:
						#doc.setHtml("<font color=\""+self.main.ui.userStyleWidget.palette().color(QtGui.QPalette.Text).name()+"\">"+useritem.escapedName+res+"</font>")
						doc.setHtml("<font size=\"-1\" color=\""+self.main.ui.userStyleWidget.palette().color(QtGui.QPalette.Text).name()+"\"><i>"+useritem.statusMessage+"</i></font>")
					else:
						doc.setHtml("<font size=\"-1\" color=\""+self.palet.color(QtGui.QPalette.HighlightedText).name()+"\"><i>"+useritem.statusMessage+"</i></font>")
					painter.save()
					painter.translate(x+41,y+16)
					if useritem.avatar:
						doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-43-32,y+32))
					else:
						doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-41,y+32))
					painter.restore()
				else:
					if self.theme:
						doc.setHtml("<font color=\""+self.main.ui.userStyleWidget.palette().color(QtGui.QPalette.Text).name()+"\">"+useritem.escapedName+res+"</font>")
					else:
						doc.setHtml("<font color=\""+self.palet.color(QtGui.QPalette.HighlightedText).name()+"\">"+useritem.escapedName+res+"</font>")
					painter.save()
					painter.translate(x+41,y+(32-fontHeight)/2)
					if useritem.avatar:
						doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-38-32,y+28))
					else:
						doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-38,y+28))
					painter.restore()
				if useritem.avatar:
					painter.drawPixmap(self.width()-4-32+(int((32-pixmap.width())/2)),y,pixmap)


		else:

			painter.save()
			painter.translate(x,y)
			if useritem==self.selected:
				if self.theme:
					painter.fillRect(0,0,self.width(),32,QtGui.QBrush(self.main.ui.selectedItemStyle.palette().window()))
				else:
					painter.fillRect(0,0,self.width(),32,QtGui.QBrush(self.main.ui.selectedItemStyle.palette().color(QtGui.QPalette.Highlight)))
			else:
				if self.theme:
					brush=QtGui.QBrush(self.main.ui.userStyleWidget.palette().window())
					if brush.color().alpha()!=0:
						painter.fillRect(0,0,self.width(),32,brush)
					#painter.fillRect(0,0,self.width(),32,QtGui.QBrush(self.main.ui.userStyleWidget.palette().window()))
				else:
					painter.fillRect(0,0,self.width(),32,QtGui.QBrush(self.palet.color(QtGui.QPalette.Base)))
			painter.restore()
			
			if useritem in self.events:
				if self.bl:
					painter.drawPixmap(x+7,y,useritem.icon.pixmap(32,32))
				else:
					painter.drawPixmap(x+7,y,useritem.blink.pixmap(32,32))
			else:
				if useritem.privacy['block'] or useritem.privacy['hide']:
					painter.drawPixmap(x+7,y,self.main.getIcon(status="error",size="32x32").pixmap(32,32))
				else:
					painter.drawPixmap(x+7,y,useritem.icon.pixmap(32,32))

			doc=QtGui.QTextDocument()
			font=QtGui.QApplication.fontMetrics()
			fontHeight=int(font.height())
			#font=doc.defaultFont()
			#font.setPixelSize(12)
			#font.setWeight(18)
			#doc.setDefaultFont(font)

			res=""
			if len(self.main.client.roster['users'][useritem.jid].resources)>1:
				res=" ("+str(len(self.main.client.roster['users'][useritem.jid].resources))+")"

			if useritem.avatar:
				pixmap=useritem.frameAvatar.pixmap(32,32)
			if useritem==self.selected:
				if self.theme:
					fontcolor=self.main.ui.userStyleWidget.palette().color(QtGui.QPalette.Text).name()
				else:
					fontcolor=self.palet.color(QtGui.QPalette.HighlightedText).name()
			else:
				fontcolor=self.main.ui.userStyleWidget.palette().color(QtGui.QPalette.Text).name()
			if useritem.statusMessage:
				doc.setHtml("<font color=\""+fontcolor+"\">"+useritem.escapedName+res+"</font>")
				painter.save()
				painter.translate(x+41,y+2)
				if useritem.avatar:
					doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-43-32,y+32))
				else:
					doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-41,y+32))
				painter.restore()
				doc.setHtml("<font size=\"-1\" color=\""+fontcolor+"\"><i>"+useritem.statusMessage+"</i></font>")
				painter.save()
				painter.translate(x+41,y+16)
				if useritem.avatar:
					doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-43-32,y+32))
				else:
					doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-41,y+32))
				painter.restore()
			else:
				doc.setHtml("<font color=\""+fontcolor+"\">"+useritem.escapedName+res+"</font>")
				painter.save()
				painter.translate(x+41,y+(32-fontHeight)/2)
				if useritem.avatar:
					doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-38-32,y+28))
				else:
					doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-38,y+28))
				painter.restore()
			if useritem.avatar:
				painter.drawPixmap(self.width()-4-32+(int((32-pixmap.width())/2)),y,pixmap)

	def paintEvent(self,event):
		QtGui.QWidget.paintEvent(self,event)
		painter=QtGui.QPainter(self)
		painter.setClipping(True)
		#painter.setRenderHint(painter.Antialiasing)
		painter.setClipRegion(event.region())
		for rect in event.region().rects():
			count=int(rect.height()/self.userHeight)
			if float(rect.height())/float(self.userHeight)>float(count):
				count+=1
			#if self.searchMode:
				#items,x,y=self.searchtemAt(1,rect.y(),count+1)
			#else:
			items,x,y=self.itemAt(1,rect.y(),count+1)
			if len(items)==0 and not self.searchMode:
				#doc=QtGui.QTextDocument()
				#option=doc.defaultTextOption()
				#option.setWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)
				#doc.setDefaultTextOption(option)
				#doc.setHtml(self.tr("You haven't any contacts in your contact list. You can add them with Add contact from menu Actions."))
				if len(self.users)==0:
					painter.drawText(QtCore.QRectF(10,10,self.width()-20,100),QtCore.Qt.AlignLeft | QtCore.Qt.TextWordWrap,self.tr("You haven't any contacts in your contact list. You can add them with Add contact from menu Actions."))
				else:
					painter.drawText(QtCore.QRectF(10,10,self.width()-20,100),QtCore.Qt.AlignLeft | QtCore.Qt.TextWordWrap,self.tr("You haven't any online contact in your contact list. To see offline contacts, you have to click Show Offline button, which is above this message."))
				#doc.drawContents(painter,)
			for item in items:
				if item.typ=="group":
					if self.compact:
						self.paintCompactGroupItem(painter,item,0,y)
					else:
						self.paintGroupItem(painter,item,0,y)
					y+=self.groupHeight
				else:
					if self.compact:
						self.paintCompactUserItem(painter,item,0,y)
					else:
						self.paintUserItem(painter,item,0,y)
					if self.item==item:
						y+=self.selectedHeight-28
					y+=self.userHeight
		if self.reshow:
			self.statusLabel.hide()

	def itemAt(self,x1,y1,count=None):
		"""
		Get items at position x1,y1.
		@type x1: number
		@type x2: number
		@type count: number
		@param count: count of returned items. First item has position [x1,y1].
		@rtype: list
		@return: [list of userItem, groupItem, specialItem,X of last item, Y of last item]
		"""
		x=0
		y=0
		got=0
		gotx=0
		goty=0
		ret=[]
		if self.searchMode==False:
			for key in self.sortedGroups:
				item=self.groups[key]
				items=self.getGroupSortedUsers(item.name)
				if ((len(items)!=0 and not self.showOffline) or self.showOffline) and item.all!=0:
					if got!=0 and not item in ret:
						ret.append(item)
						got+=1
					if y1>=y and y1<=y+self.groupHeight:
						if count and not item in ret:
							ret.append(item)
							got+=1
							goty=y
						if not count:
							return item
					if got==count:
						return ret,0,goty
					if item.expanded and len(items)!=0:
						previous=None
						for useritem in items:
							y+=self.userHeight
							if got!=0 and not useritem in ret:
								ret.append(useritem)
								got+=1
	
							if useritem==self.item:
								if y1>=y and y1<=y+self.selectedHeight-28+self.userHeight:
									if count and not useritem in ret:
										ret.append(useritem)
										got+=1
										goty=y
									if not count:
										return useritem
							else:
								if y1>=y and y1<=y+self.userHeight:
									if count and not useritem in ret:
										ret.append(useritem)
										got+=1
										goty=y
									if not count:
										return useritem
							if got==count:
								return ret,0,goty
							if useritem==self.item:
								y+=self.selectedHeight-28
					y+=self.groupHeight
		else:
			users=[]
			for item in self.users:
				if not self.metaItems.has_key(item.jid):
					users.append([item.name.lower(),item])
			for v in self.metaItems.itervalues():
				for user in v:
					users.append([user.name.lower(),user])
			users.sort()
			for item in users:
				item=item[1]
				if item.hiddenBySearch==False:
					useritem=item
					if got!=0 and not useritem in ret:
						ret.append(useritem)
						got+=1

					if useritem==self.item:
						if y1>=y and y1<=y+self.selectedHeight-28+self.userHeight:
							if count and not useritem in ret:
								ret.append(useritem)
								got+=1
								goty=y
							if not count:
								return useritem
					else:
						if y1>=y and y1<=y+self.userHeight:
							if count and not useritem in ret:
								ret.append(useritem)
								got+=1
								goty=y
							if not count:
								return useritem
					if got==count:
						return ret,0,goty
					if useritem==self.item:
						y+=self.selectedHeight-28
					y+=self.userHeight

		if got!=0:
			return ret,0,goty

		if count:
			return [],None,None

	def itemCoordinates(self,i):
		"""
		Return coordinates of userItem i
		@type i: userItem
		@rtype: list
		@return: [X,Y]
		"""
		x=0
		y=0
		if self.searchMode==False:
			for key in self.sortedGroups:
				item=self.groups[key]
				items=self.getGroupSortedUsers(item.name)
				if ((len(items)!=0 and not self.showOffline) or self.showOffline) and item.all!=0:
					if item==i:
						return x,y
					if item.expanded and len(items)!=0:
						previous=None
						for useritem in items:
							y+=self.userHeight
							if useritem==i:
								return x,y
							if useritem==self.item:
								y+=self.selectedHeight-28
	
						#if useritem==self.item:
							#y-=32
					y+=self.groupHeight
		else:
			#for item in self.users:
				#if item.hiddenBySearch==False:
					#useritem=item
					#if useritem==i:
						#return x,y
					#if useritem==self.item:
						#y+=self.selectedHeight-28
					#y+=self.userHeight

			users=[]
			for item in self.users:
				if not self.metaItems.has_key(item.jid):
					users.append([item.name.lower(),item])
			for v in self.metaItems.itervalues():
				for user in v:
					users.append([user.name.lower(),user])
			users.sort()
			for item in users:
				item=item[1]
				if item.hiddenBySearch==False:
					useritem=item
					if useritem==i:
						return x,y
					if useritem==self.item:
						y+=self.selectedHeight-28
					y+=self.userHeight

		return None,None

	def setSize(self):
		"""
		Set height of rosterLiveWidget
		"""
		x=0
		y=0
		if self.searchMode==False:
			for key in self.sortedGroups:
				item=self.groups[key]
				items=self.getGroupSortedUsers(item.name)
				if (len(items)!=0 and not self.showOffline) or self.showOffline:
					if item.expanded and len(items)!=0:
						for useritem in items:
							y+=self.userHeight
					y+=self.groupHeight
		else:
			for item in self.users:
				if item.hiddenBySearch==False:
					useritem=item
					if useritem==self.item:
						y+=self.selectedHeight-28
					y+=self.userHeight
		size=y+self.selectedHeight-28
		if size<self.parent().height()-20:
			if self.parent().height()-20>0:
				self.setMinimumHeight(self.parent().height()-20)
		else:
			if y+self.selectedHeight-28>0 and self.selectedHeight!=0 and not self.statusLabel.isHidden():
				self.setMinimumHeight(size)
			else:
				self.setMinimumHeight(size)
		#self.setMinimumHeight(1500)


	#def sel(self):
		#self.item=self.selected
		#self.reshow=True
		#self.repaint()
		#self.setSize()

	#def sel2(self):
		#self.item = None
		#self.selected = None
		#self.statusLabel.hide()
		#self.reshow=True
		#self.repaint()
		#self.setSize()

	def selectItem(self,item):
		"""
		Select item
		@type item: userItem
		"""
		if self.item!=item and item!=None and item.main!='special':
			#self.selected=item
			self.item=item
			self.reshow=True
			self.repaint()
			self.setSize()
			#self.main.client.reactor.callLater(0.2,self.sel)

		elif self.item == item and self.item != None and item.main!='special':
			self.item = None
			#self.selected = None
			self.statusLabel.hide()
			self.reshow=True
			self.repaint()
			self.setSize()
		if item!=None:
			if item.typ=='group' and item.main!='special':
				self.statusLabel.hide()

	def mouseReleaseEvent(self,event):
		x=event.x()
		y=event.y()
		item=self.itemAt(x,y)
		if item==None:
			return QtGui.QWidget.mouseReleaseEvent(self,event)
		t=QtGui.QApplication.doubleClickInterval()/1000.0
		timestamp=float(time.time())
		if timestamp-self.timestamp<=t:
			self.mouseDoubleClickEvent(event)
		else:
			if event.button() == QtCore.Qt.LeftButton:
				self.oldItem=self.item
				if item.typ=='group':
					self.selectItem(item)
				else:
					self.selectItem(item)
	
				if item.typ=='group' and item.main!='special':
					if item.expanded:
						item.icon=QtGui.QIcon("images/"+self.iconSize+"/icons/group-closed.png")
						item.expanded=False
					else:
						item.icon=QtGui.QIcon("images/"+self.iconSize+"/icons/group-open.png")
						item.expanded=True
					self.setSize()
					self.statusLabel.hide()
					self.repaint()
		self.timestamp=float(timestamp)
		QtGui.QWidget.mouseReleaseEvent(self,event)

	def mouseDoubleClickEvent(self,event):
		x=event.x()
		y=event.y()
		item=self.itemAt(x,y)
		if self.item!=item:
			item=self.oldItem
		if item==None:
			return QtGui.QWidget.mouseReleaseEvent(self,event)
		if item.typ=='group' and item.main!='special':
			if item.expanded:
				item.icon=QtGui.QIcon("images/"+self.iconSize+"/icons/group-closed.png")
				item.expanded=False
			else:
				item.icon=QtGui.QIcon("images/"+self.iconSize+"/icons/group-open.png")
				item.expanded=True
			self.setSize()
			self.repaint()
		else:
			jidt = jidT.JID(item.jid)
			if jidt.resource:
				res=jidt.resource
			else:
				res = self.main.client.roster['users'][item.jid].getHighestResource()
			if res==None:
				self.main.chat.addChatTab(item.jid,item.name,self.main.getIcon(item.jid,self.main.icons[str(item.status)],size="16x16"))
			else:
				self.main.chat.addChatTab(item.jid+"/"+res,item.name,self.main.getIcon(item.jid,self.main.icons[str(item.status)],size="16x16"))
			self.main.chat.activate()

	def keyPressEvent(self,event):
		key=event.key()
		if key==QtCore.Qt.Key_Down:
			if self.item:
				x,y=self.itemCoordinates(self.item)
				if self.item.typ=="group" or self.item.typ=="special":
					item=self.itemAt(x,y+self.userHeight+5)
				else:
					if not self.compact:
						item=self.itemAt(x,y+self.selectedHeight+33)
					else:
						item=self.itemAt(x,y+self.selectedHeight+1)
					print item.typ
					if item.main=="special":
						x,y=self.itemCoordinates(item)
						item=self.itemAt(x,y+1+self.groupHeight)
	
				self.selectItem(item)
			#self.timer.start(40)
			event.accept()
		elif key==QtCore.Qt.Key_Up:
			if self.item:
				x,y=self.itemCoordinates(self.item)
	
				item=self.itemAt(x,y-3)
				if item.main=="special":
					x,y=self.itemCoordinates(item)
					item=self.itemAt(x,y-3)
				self.selectItem(item)
			#self.timer.start(40)
			event.accept()
		elif (key==QtCore.Qt.Key_Return or key==QtCore.Qt.Key_Enter) and self.item != None:
			jid = jidT.JID(self.item.jid)
			jid_r = jid.userhost()
			item=self.item
			if jid.resource:
				res=jid.resource
			else:
				res = self.main.client.roster['users'][jid_r].getHighestResource()
			if res==None:
				self.main.chat.addChatTab(item.jid,item.name,self.main.getIcon(item.jid,self.main.icons[str(item.status)],size="16x16"))
			else:
				self.main.chat.addChatTab(item.jid+"/"+res,item.name,self.main.getIcon(item.jid,self.main.icons[str(item.status)],size="16x16"))

			#self.main.chat.addChatTab(item.jid,item.name,self.main.getIcon(item.jid,self.main.icons[str(item.status)],size="16x16"))
			self.main.chat.activate()
		elif key==QtCore.Qt.Key_Escape:
			self.item = None
			#self.selected = None
			if self.searchMode==True:
				self.searchMode=False
				for user in self.users:
					user.hiddenBySearch=False
				self.main.ui.rosterSearch.setText("")
				self.main.ui.rosterSearch.hide()
				self.main.ui.rosterSearchLabel.hide()

			self.statusLabel.hide()
			self.reshow=True
			self.setSize()
			self.repaint()

		elif key==QtCore.Qt.Key_Delete: #tohle by mozna chtelo nejake potvrzeni 'Opravdu to chcete udelat?'
			self.main.client.delContact(self.item.jid)
		elif key==QtCore.Qt.Key_F2:
			jid=self.item.jid
			try:
				name=unicode(self.main.client.roster['users'][jid].name)
			except:
				name = ''
##			print "roster_new_group_action",jid,name
			# get new group name with QDialog
			name,b=QtGui.QInputDialog.getText(self,self.tr("Rename"),self.tr("Enter new name:"), QtGui.QLineEdit.Normal, name)
			name=unicode(name)
			# if user set new name of group
			if b==True and len(name)!=0:
				# add new group
				contact=self.main.client.roster['users'][jid]
				self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription, self.main.client.roster['users'][jid].groups)
			pass
		elif key==QtCore.Qt.Key_F and event.modifiers() & QtCore.Qt.ControlModifier:
			QtGui.QMessageBox.warning(self,':)',unicode(rot13.scramble("Frs fnzbmerwzr ifrpuab ivqv n wra gnx gb ararpun :C")),0,1)
		elif key==QtCore.Qt.Key_O and event.modifiers() & QtCore.Qt.ControlModifier:
			check=not self.main.ui.showOffline.isChecked()
			self.main.ui.showOffline.setChecked(check)
			self.main.hideOffline(check)
		elif key==QtCore.Qt.Key_E and event.modifiers() & QtCore.Qt.ControlModifier:
			self.main.client.evil = not self.main.client.evil
			print self.main.client.evil
		else:
			#self.main.ui.rosterSearch.setFocus(QtCore.Qt.MouseFocusReason)
			self.main.ui.rosterSearch.event(event)
		event.ignore()
			

	def dragEnterEvent(self, event):
		#log.msg('DRAG ENTER')
		if event.mimeData().hasText() or event.mimeData().hasFormat("text/uri-list"):
			event.acceptProposedAction()
		else:
			event.ignore()

	def dragMoveEvent(self, event):
		#log.msg('DRAG MOVE')
		pos=event.pos()
		#print pos.x(),pos.y()
		item=self.itemAt(pos.x(),pos.y())
		self.scrollUp=None
		if pos.y()-self.main.scroll.verticalScrollBar().value()>self.main.scroll.height()-16:
			self.timer.start(50)
			self.scrollUp=False
		if pos.y()-self.main.scroll.verticalScrollBar().value()<32:
			self.scrollUp=True
			self.timer.start(50)
		
		#if not pos.y()>self.main.scroll.height()-16 and not pos.y()-self.main.scroll.verticalScrollBar().value():
			#self.timer.stop()
		
		if item:
			event.acceptProposedAction()
			if self.selected!=item:
				self.selected=item
				self.repaint()
		else:
			if self.selected:
				self.selected=None
				self.repaint()
			event.ignore()

	def dropEvent(self, event):
		self.scrollUp=None
		if self.selected:
			self.selected=None
			self.repaint()

		if (event.mimeData().hasUrls()):
			urlList=event.mimeData().urls()
			if len(urlList)>0:
				new=[]
				for url in urlList:
					f=unicode(url.toLocalFile())
					if len(f)!=0:
						new.append(f)
				file=new
				print file
				position = event.pos()
				item=self.itemAt(position.x(),position.y())
				if item.typ=="user":
					self.main.showFiletransferDialog(file,jid)
					#if item.jid=="album@disk.jabbim.cz":
						#self.dialog=albumfiletransfer.albumFiletransferDialog(self.main,file,item.jid)
					#else:
						#self.dialog=filetransfer.filetransferDialog(self.main,file,item.jid)
					#self.dialog.show()
			event.acceptProposedAction()
		elif event.mimeData().hasText():
			jid = unicode(event.mimeData().text())
			position = event.pos()
			item=self.itemAt(position.x(),position.y())
			if not self.data.has_key(event.mimeData()):
				gr=""
				if item.typ=="group":
					gr=item.name
				elif item.typ=="user":
					gr=item.group
				try:
					jidT.JID(jid)
					validJid=True
				except:
					validJid=False
				if validJid:
					dialog=addcontact.addContactDialog(self.main,self,jid=jid,group=gr,name=jid.split('@')[0])
					dialog.exec_()
				#else:
					
				event.ignore()
				return
			
			oldItem=self.data[event.mimeData()]
			if item==oldItem:
				event.ignore()
				del self.data[event.mimeData()]
				return

			#print jid,item.name
			#for piece in pieces:
				#newLabel = DragLabel(piece, self)
				#newLabel.move(position)
				#newLabel.show()
	
				#position += QtCore.QPoint(newLabel.width(), 0)
	
			#if event.source() in self.children():
				#event.setDropAction(QtCore.Qt.MoveAction)
				#event.accept()
			#else:
			event.acceptProposedAction()
			
			# normal user > group
			if oldItem.typ=="user" and item.typ=="group":
				#items=QtCore.QStringList()
				#items.append(self.tr("Move"))
				#items.append(self.tr("Copy"))
				#q,b=QtGui.QInputDialog.getItem(self,self.tr("Action"),self.tr("Select action."), items,0,False)
				#q=unicode(q)
				
				contactMenu=QtGui.QMenu(self)
				if item.name!=self.specialName:
					action=contactMenu.addAction(self.tr("Move to group"))
					action.jid=jid
					action.oldItem=oldItem
					action.item=item
					action.setObjectName("move_to_group_ng")
					
					action=contactMenu.addAction(self.tr("Copy to group"))
					action.jid=jid
					action.item=item
					action.setObjectName("copy_to_group_ng")
				# signal
				contactMenu.connect(contactMenu, QtCore.SIGNAL("triggered ( QAction * )"),self.dropMenuTriggered)
				contactMenu.popup(self.mapToGlobal(position))

				#if b==True and len(q)!=0:
					#index=int(items.indexOf(QtCore.QRegExp(q)))
					#if index==0:
						#name=unicode(self.main.client.roster['users'][jid].name)
						#contact=self.main.client.roster['users'][jid]
						#g=contact.groups
						#if len(g)!=0:
							#g.remove(unicode(self.groups[oldItem.group].name))
						#else:
							#for yy in self.getUserItems(contact.jid):
								#self.users.remove(yy)
						#self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription,g+[unicode(item.name)])
					#else:
						#self.changeGroup(jid,"+",unicode(item.name))

			# metacontact > normal user
			elif oldItem.typ=="user" and oldItem.metajid!="" and item.typ=="user":
				del self.data[event.mimeData()]
				event.ignore()
				return
				items=QtCore.QStringList()
				items.append(self.tr("Move to group"))
				q,b=QtGui.QInputDialog.getItem(self.main,self.tr("Contact action"),self.tr("Select action."), items,0,False)
				q=unicode(q)
				if b==True and len(q)!=0:
					index=int(items.indexOf(QtCore.QRegExp(q)))

					if index==0:
						for it in self.metaItems[oldItem.metajid]:
							if it.jid==oldItem.jid:
								self.setHighest(oldItem.metajid)
								self.metaItems[oldItem.metajid].remove(it)
								del self.main.client.roster_meta[oldItem.jid]
								break
						print self.metaItems[oldItem.metajid]
						if len(self.metaItems[oldItem.metajid])==1:
							highest=self.metaItems[oldItem.metajid][0]
							#oldItem.name=highest.name+"LOL"
							#oldItem.icon=highest.icon
							#oldItem.avatar=highest.avatar
							#oldItem.status=highest.status
							#oldItem.statusMessage=highest.statusMessage
							#oldItem.jid=highest.jid
							#if str(oldItem.status)!="9":
								#oldItem.hidden=False
							#else:
								#oldItem.hidden=True
							#oldItem.metajid=""
							#oldItem.tag=""
							self.setHighest(oldItem.metajid)
							del self.main.client.roster_meta[self.metaItems[oldItem.metajid][0].jid]
							del self.metaItems[oldItem.metajid]
							name=unicode(self.main.client.roster['users'][highest.jid].name)
							contact=self.main.client.roster['users'][highest.jid]
							gr=unicode(oldItem.group)
							for it in self.getUserItems(oldItem.metajid):
								self.users.remove(it)
							for it in self.getUserItems(contact.jid):
								it.metajid=""
							self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription,[gr])
						
						self.main.client.setMetacontacts()
						name=unicode(self.main.client.roster['users'][jid].name)
						contact=self.main.client.roster['users'][jid]
						for it in self.getUserItems(contact.jid):
							it.metajid=""
						self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription,[unicode(item.group)])
						self.statusLabel.hide()
						self.sortItems()
						self.repaint()
						

			# normal user > normal/meta user
			elif oldItem.typ=="user" and item.typ=="user":
				#items=QtCore.QStringList()
				#items.append(self.tr("Move to group"))
				#items.append(self.tr("Make metacontact"))
				#items.append(self.tr("Copy to group"))
				#q,b=QtGui.QInputDialog.getItem(self,self.tr("Contact action"),self.tr("Select action."), items,0,False)
				#q=unicode(q)
				# build contact menu
				contactMenu=QtGui.QMenu(self)
				if self.specialName!=item.group:
					action=contactMenu.addAction(self.tr("Move to group"))
					action.jid=jid
					action.oldItem=oldItem
					action.item=item
					action.setObjectName("move_to_group_nn")
				
				action=contactMenu.addAction(self.tr("Make metacontact"))
				action.item=item
				action.oldItem=oldItem
				action.setObjectName("make_metacontact_nn")
				if self.specialName!=item.group:
					action=contactMenu.addAction(self.tr("Copy to group"))
					action.jid=jid
					action.item=item
					action.setObjectName("copy_to_group_nn")
				# signal
				contactMenu.connect(contactMenu, QtCore.SIGNAL("triggered ( QAction * )"),self.dropMenuTriggered)
				contactMenu.popup(self.mapToGlobal(position))

				#if b==True and len(q)!=0:
					#index=int(items.indexOf(QtCore.QRegExp(q)))

					#if index==0:
						#name=unicode(self.main.client.roster['users'][jid].name)
						#contact=self.main.client.roster['users'][jid]
						#g=contact.groups
						#if len(g)!=0:
							#g.remove(unicode(self.groups[oldItem.group].name))
						#else:
							#for yy in self.getUserItems(contact.jid):
								#self.users.remove(yy)
						#self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription,g+[unicode(item.group)])
					#elif index==1:
						#if not self.metaItems.has_key(item.metajid):
							#item.metajid=item.jid
							#item.tag=item.jid
							#self.metaItems[item.metajid]=[]
							#self.main.client.roster_meta[item.jid]={'tag':item.tag,'order':10}
							#it=item.clone()
							#it.tag=item.tag

							#self.metaItems[item.metajid].append(it)
						#it=oldItem.clone()
						#it.tag=item.tag

						#self.metaItems[item.metajid].append(it)
						#for i in self.getUserItems(oldItem.jid):
							#self.users.remove(i)
						#self.setHighest(item.metajid)
						#self.main.client.roster_meta[oldItem.jid]={'tag':item.tag,'order':1}
						#self.main.client.setMetacontacts()
						
						#self.sortItems()
						#if self.item!=item:
							#self.selectItem(item)
						#self.reshow=True
						#self.repaint()

					#elif index==2:
						#self.changeGroup(jid,"+",unicode(item.group))
			event.acceptProposedAction()
			del self.data[event.mimeData()]
		else:
			event.ignore()

	def dropMenuTriggered(self,action):
		cmd=action.objectName()
		if cmd=="move_to_group_nn":
			jid=action.jid
			oldItem=action.oldItem
			item=action.item

			name=unicode(self.main.client.roster['users'][jid].name)
			contact=self.main.client.roster['users'][jid]
			g=contact.groups
			if len(g)!=0:
				g.remove(unicode(self.groups[oldItem.group].name))
			else:
				for yy in self.getUserItems(contact.jid):
					self.users.remove(yy)
			self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription,g+[unicode(item.group)])
		elif cmd=="make_metacontact_nn":
			item=action.item
			oldItem=action.oldItem
			if not self.metaItems.has_key(item.metajid):
				item.metajid=item.jid
				item.tag=item.jid
				self.metaItems[item.metajid]=[]
				self.main.client.roster_meta[item.jid]={'tag':item.tag,'order':10}
				it=item.clone()
				it.tag=item.tag

				self.metaItems[item.metajid].append(it)
			it=oldItem.clone()
			it.tag=item.tag

			self.metaItems[item.metajid].append(it)
			for i in self.getUserItems(oldItem.jid):
				self.users.remove(i)
			self.setHighest(item.metajid)
			self.main.client.roster_meta[oldItem.jid]={'tag':item.tag,'order':1}
			self.main.client.setMetacontacts()
			
			self.sortItems()
			if self.item!=item:
				self.selectItem(item)
			self.reshow=True
			self.repaint()

		elif cmd=="copy_to_group_nn":
			item=action.item
			jid=action.jid
			self.changeGroup(jid,"+",unicode(item.group))

		elif cmd=="move_to_group_ng":
			jid=action.jid
			oldItem=action.oldItem
			item=action.item
			name=unicode(self.main.client.roster['users'][jid].name)
			contact=self.main.client.roster['users'][jid]
			g=contact.groups
			if len(g)!=0:
				g.remove(unicode(self.groups[oldItem.group].name))
			else:
				for yy in self.getUserItems(contact.jid):
					self.users.remove(yy)
			self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription,g+[unicode(item.name)])
		elif cmd=="copy_to_group_ng":
			item=action.item
			jid=action.jid
			self.changeGroup(jid,"+",unicode(item.name))

	def makeHiddenItem(self):
		pass

	def mimeTypes(self):
		# set mimetypes, which we accept
		return QtCore.QStringList("text/plain")

	def getGroupItem(self,name):
		return None

	def getHostItems(self,host):
		"""
		Get all userItem with selected host
		@type host: unicode
		@rtype: list
		@return: list of userItem
		"""
		ret=[]
		for user in self.users:
			j=self.main.getJid(user.jid)
			if j:
				if j.host==host:
					ret.append(user)
		for mainjid,users in self.metaItems.iteritems():
			for user in users:
				j=self.main.getJid(user.jid)
				if j:
					if j.host==host:
						ret.append(user)
		#print "HOSTITEMS:",ret
		return ret

	def search(self,text=""):
		text=unicode(text).lower()
		first=None
		if len(text)!=0:
			self.main.ui.rosterSearch.show()
			self.main.ui.rosterSearchLabel.show()
			self.searchMode=True
			for user in self.users:
				if user.name.lower().find(text)!=-1:
					user.hiddenBySearch=False
					if not first:
						first=user
				else:
					user.hiddenBySearch=True
			for v in self.metaItems.itervalues():
				for user in v:
					if user.name.lower().find(text)!=-1:
						user.hiddenBySearch=False
						if not first:
							first=user
					else:
						user.hiddenBySearch=True
			
		else:
			self.main.ui.rosterSearch.hide()
			self.main.ui.rosterSearchLabel.hide()
			self.searchMode=False
			self.statusLabel.hide()
			for user in self.users:
				user.hiddenBySearch=False
				if not first:
					first=user
			for v in self.metaItems.itervalues():
				for user in v:
					user.hiddenBySearch=False
					if not first:
						first=user
		if self.item:
			if self.item.typ=="user":
				if self.item.hiddenBySearch==True:
					self.statusLabel.hide()
					self.selectItem(first)
				else:
					self.reshow=True
			else:
				self.statusLabel.hide()
				self.selectItem(first)
		else:
			self.selectItem(first)
		self.setSize()
		self.repaint()
		

	def getUserItems(self,jid):
		"""
		Get all userItems with JID jid
		@type jid: unicode
		@rtype: list
		@return: list of userItem
		"""
		ret=[]
		for user in self.users:
			if user.jid==jid:
				ret.append(user)
		return ret

	def getMetaParents(self,jid):
		ret=[]
		for user in self.users:
			if user.metajid==jid:
				ret.append(user)
		return ret

	def getMetaItems(self,jid):
		"""
		Get all metaItems with JID jid
		@type jid: unicode
		@rtype: list
		@return: list of userItem
		"""
		ret=[]
		for mainjid,users in self.metaItems.iteritems():
			for user in users:
				if user.jid==jid:
					ret.append([user,mainjid])
		return ret

	def hidden(self,bool):
		pass


	def refreshStats(self):
		pass

	def setStatus(self,jid,show,i=None,status=None,first=False):

		res = self.main.client.roster['users'][jid].getHighestResource()
		if res!=None:
			res=self.main.client.roster['users'][jid].resources[res]
			show=res.show
			status=res.status

		for user in self.getUserItems(jid):
			
			user.icon=self.main.getIcon(jid,size="32x32",status=self.main.icons[self.main.shows[unicode(show)]])
			if self.main.shows[unicode(show)]!="9":
				user.hidden=False
			elif len(self.main.client.roster['users'][jid].resources)==0:
				user.hidden=True
				if self.item==user:
					self.statusLabel.hide()
			user.statusMessage=status
			user.status=self.main.shows[unicode(show)]

		for couple in self.getMetaItems(jid):
			user=couple[0]
			mainjid=couple[1]
			user.icon=self.main.getIcon(jid,size="32x32",status=self.main.icons[self.main.shows[unicode(show)]])
			if self.main.shows[unicode(show)]!="9":
				user.hidden=False
			else:
				user.hidden=True
			user.statusMessage=status
			user.status=self.main.shows[unicode(show)]
			highest=None
			print "-------"
			for item in self.metaItems[mainjid]:
				print jid,item.jid,item.status
				if highest:
					husertype=""
					usertype=""
					if self.main.hosts.has_key(jidT.JID(highest.jid).host):
						husertype=self.main.hosts[jidT.JID(highest.jid).host]
					if self.main.hosts.has_key(jidT.JID(item.jid).host):
						usertype=self.main.hosts[jidT.JID(item.jid).host]
					#if (int(item.status)<int(highest.status) and husertype!="jabber" and highest.status=="9") or (husertype!="jabber" and highest.status=="9"):
					#print item.jid,highest.jid,item.status,highest.status,usertype=="jabber" and item.status!="9",highest.status=="9" and item.status!="9"
					if (usertype=="jabber" and str(item.status)!="9") or (str(highest.status)=="9" and str(item.status!="9")):
						highest=item
				else:
					highest=item
			print highest.jid
			print "-------"
			if highest:
				item=self.getMetaParents(mainjid)
				if len(item)!=0:
					item=item[0]
					print item.jid,highest.jid
					if item.jid!=highest.jid:
						item.name=highest.name
						item.escapedName=highest.escapedName
						item.frameAvatar=highest.frameAvatar
						item.selectedFrameAvatar=highest.selectedFrameAvatar
						item.icon=highest.icon
						item.avatar=highest.avatar
						item.status=highest.status
						item.statusMessage=highest.statusMessage
						item.jid=highest.jid
						if str(item.status)!="9":
							item.hidden=False
						else:
							item.hidden=True
		if not first:
			#self.statusLabel.hide()
			self.changePos=True
			self.sortItems()
		#for user in self.getUserItems(jid):
			#log.msg("hidden:"+unicode(user.hidden))
		self.repaint()

	def setHighest(self,mainjid):
		highest=None
		print "-------"
		for item in self.metaItems[mainjid]:
			if highest:
				husertype=""
				usertype=""
				if self.main.hosts.has_key(jidT.JID(highest.jid).host):
					husertype=self.main.hosts[jidT.JID(highest.jid).host]
				if self.main.hosts.has_key(jidT.JID(item.jid).host):
					usertype=self.main.hosts[jidT.JID(item.jid).host]
				#if (int(item.status)<int(highest.status) and husertype!="jabber" and highest.status=="9") or (husertype!="jabber" and highest.status=="9"):
				#print item.jid,highest.jid,item.status,highest.status,usertype=="jabber" and item.status!="9",highest.status=="9" and item.status!="9"
				if ((usertype=="jabber" and str(item.status)!="9") or (str(highest.status)=="9" and str(item.status!="9"))) and item.jid!=mainjid:
					highest=item
			else:
				if item.jid!=mainjid:
					highest=item
		print "-------"
		if highest:
			item=self.getUserItems(mainjid)
			if len(item)!=0:
				item=item[0]
				if item.jid!=highest.jid:
					item.name=highest.name
					item.icon=highest.icon
					item.avatar=highest.avatar
					item.status=highest.status
					item.statusMessage=highest.statusMessage
					item.jid=highest.jid
					if str(item.status)!="9":
						item.hidden=False
					else:
						item.hidden=True

	def cloneContact(self,parent,item):
		pass

		
	def buildContactMenu(self,jid,group):
		# build contact menu
		contactMenu=QtGui.QMenu(self)
		contact = self.main.client.roster['users'][jid]
		oneres = len(contact.resources.keys()) < 2
		# chat
		if oneres:
			action=contactMenu.addAction(self.tr("Chat"))
			if action != None:
				action.setData(QtCore.QVariant(unicode(jid)))
				action.setObjectName("chat")
		else:
			submenu = contactMenu.addMenu(self.tr("Chat"))
			for res in contact.resources.keys():
				if res != None:
					action=submenu.addAction(unicode(res))
					action.setData(QtCore.QVariant("%s/%s" % (jid, res)))
					action.setObjectName("chat")
		if self.main.client.groupchats != {}:	# Mozna zobrazit i kdyz v mucu nejsme aby to bylo vic videt :)
			submenu = contactMenu.addMenu(QtGui.QIcon("images/16x16/categories/muc.png"),self.tr("Invite to conference"))
			if oneres:
				for gc in self.main.client.groupchats.keys():
					action = submenu.addAction(gc)
					action.setData(QtCore.QVariant([jid, gc]))
					action.setObjectName("invite_gc")
			else:
				for gc in self.main.client.groupchats.keys():
					submenu2 = submenu.addMenu(gc)
					for res in contact.resources.keys():
						if res != None:
							action = submenu2.addAction(res)
							action.setData(QtCore.QVariant(["%s/%s" % (jid, res), gc]))
							action.setObjectName("invite_gc")
		# custom status
		if oneres:
			submenu=contactMenu.addMenu(self.tr("Custom status"))

			for status in ["online", "chat", "away", "xa", "dnd", "offline"]:
				action=submenu.addAction(self.main.getIcon(status=status,size="32x32"),self.main.status[status])
				action.setObjectName("custom_status")
				action.setData(QtCore.QVariant([unicode(status), unicode(jid)]))
		else:
			submenu = contactMenu.addMenu(self.tr("Custom status"))
			resmenu = submenu.addMenu(self.tr("All resources"))
			submenu.addSeparator()
			resources=contact.resources.keys()
			resmenus=[]
			for resource in resources:
				if resource!=None:
					resmenus.append((submenu.addMenu(res),resource))
			resmenus.append((resmenu, ""))
			for resm in resmenus:
				resmenu, res = resm
				for status in ["online", "chat", "away", "xa", "dnd", "offline"]:
			                action=resmenu.addAction(self.main.getIcon(status=status,size="32x32"),self.main.status[status])
					print "LOG 9"
					action.setObjectName("custom_status")
					if res:
						jr = "%s/%s" % (jid, res)
					else:
						jr = jid
					action.setData(QtCore.QVariant([unicode(status), unicode(jr)]))

		# separator
		contactMenu.addSeparator()
		# vcard
		if oneres:
			action=contactMenu.addAction(QtGui.QIcon("images/16x16/categories/v-card.png"),self.tr("vCard"))
			resource=contact.resources.keys()
			if len(resource)!=0:
				action.setData(QtCore.QVariant("%s/%s" % (jid, resource[0])))
			else:
				action.setData(QtCore.QVariant("%s" % (jid)))
			action.setObjectName("vcard")
		else:		# Potrebujeme resource pro Software Version, vCard je na nem nezavisla
			submenu=contactMenu.addMenu(QtGui.QIcon("images/16x16/categories/v-card.png"),self.tr("vCard"))
			for res in contact.resources.keys():
				if res != None:
					action=submenu.addAction(res)
					action.setData(QtCore.QVariant("%s/%s" %(jid,res)))
					action.setObjectName("vcard")
		#action=contactMenu.addAction(self.tr("vCard"))
		#action.setData(QtCore.QVariant(jid))
		#action.setObjectName("vcard")
		# filetransfer
		if oneres:
			resource=contact.resources.keys()
			if len(resource)!=0:
				print contact.resources.keys()
				print self.main.client.roster['users'][jid].resources[resource[0]].features
				if self.main.client.roster['users'][jid].resources[resource[0]].hasFeature('http://jabber.org/protocol/si/profile/file-transfer'):
					action=contactMenu.addAction(self.tr("Send file"))
					action.setData(QtCore.QVariant(jid))
					action.setObjectName("send_file")
					action.setIcon(QtGui.QIcon("images/32x32/actions/upload.png"))
		else:
			submenu = contactMenu.addMenu(self.tr("Send file"))
			for resource in contact.resources.keys():
				if resource != None:
					if len(resource)!=0:
						if self.main.client.roster['users'][jid].resources[resource].hasFeature('http://jabber.org/protocol/si/profile/file-transfer'):
							action = submenu.addAction(resource)
							action.setIcon(QtGui.QIcon("images/32x32/actions/upload.png"))
							action.setData(QtCore.QVariant("%s/%s" % (jid, resource)))
							action.setObjectName("send_file")

		for key,value in self.main.plugins.iteritems():
			if value['module']:
				self.main.runPluginCommand(value['module'].buildContactMenu,[contactMenu,contact])
		# separator
		contactMenu.addSeparator()
		
		# break up metacontact
		if self.main.client.roster_meta.has_key(jid):
			action=contactMenu.addAction(self.tr("Break up metacontact"))
			action.setData(QtCore.QVariant(jid))
			action.setObjectName("break_up_meta")
		# rename
		action=contactMenu.addAction(self.tr("Rename"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("rename")
		# delete from group
		if group!=None and len(self.main.client.roster['users'][jid].groups)>1:
			action=contactMenu.addAction(self.tr("Delete from group"))
			action.setData(QtCore.QVariant([unicode(jid),u"-"+group]))
			action.setObjectName("check_group")
		# delete from roster
		action=contactMenu.addAction(self.tr("Delete from roster"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("delete_action")
		# separator
		contactMenu.addSeparator()
		# groups . submenu
		group=contactMenu.addMenu (self.tr("Groups"))
		# groups . new group
		action=group.addAction(self.tr("New Group"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("new_group")
		# groups . separator
		group.addSeparator()
		# groups . groups list
		#g=self.getGroups(str(jid))
		for k,v in self.groups.iteritems():
			if k!="Unknown" and k!=self.specialName:
				action=group.addAction(unicode(k))
				action.setObjectName("check_group")
				action.setCheckable(True)
			#if len(self.main.client.roster['users'][jid].groups)==0:
				#if k=="Unknown":
					#action.setChecked(True)
					#action.setData(QtCore.QVariant([unicode(jid),u"-"+unicode(k)]))
				#else:
					#action.setData(QtCore.QVariant([unicode(jid),u"+"+unicode(k)]))
			#else:
				if k in self.main.client.roster['users'][jid].groups:
					action.setChecked(True)
					action.setData(QtCore.QVariant([unicode(jid),u"-"+unicode(k)]))
					if len(self.main.client.roster['users'][jid].groups)<=1:
						action.setEnabled(False)
				else:
					action.setData(QtCore.QVariant([unicode(jid),u"+"+unicode(k)]))
				
		subscription = contactMenu.addMenu(self.tr("Authorization"))
		value = contact.subscription
		if value in ["none", "to"]:
			action = subscription.addAction(self.tr("Send authorization to contact"))
			action.setData(QtCore.QVariant(jid))
			action.setObjectName("a_authorize")
		if value in ["from", "both"]:
			action = subscription.addAction(self.tr("Remove authorization from contact"))	
			action.setData(QtCore.QVariant(jid))
			action.setObjectName("a_unauthorize")
		if value in ["none", "from"]:
			action = subscription.addAction(self.tr("Request authorization from contact"))	
			action.setData(QtCore.QVariant(jid))
			action.setObjectName("a_ask")
		
		if self.main.client.privacy:
			if self.main.client.privacy.active:
				submenu = contactMenu.addMenu(self.tr("Privacy"))
				if not self.main.client.privacy.active.isBlockedJID(jid):
					action = submenu.addAction(self.tr("Block contact"))
					action.setData(QtCore.QVariant(jid))
					action.setObjectName("privacy_block")
				else:
					action = submenu.addAction(self.tr("Unblock contact"))
					action.setData(QtCore.QVariant(jid))
					action.setObjectName("privacy_unblock")
				
				# Sekci nemazat
				#if not self.main.client.privacy.active.isAllowedJID(jid):
				#	action = submenu.addAction(self.tr("Allow contact to see my status when I am invisible"))
				#	action.setData(QtCore.QVariant(jid))
				#	action.setObjectName("privacy_allow")
				#else:
				#	action = submenu.addAction(self.tr("Disallow contact to see my status when I am invisible"))
				#	action.setData(QtCore.QVariant(jid))
				#	action.setObjectName("privacy_disallow")
				
				if not self.main.client.privacy.active.isHiddenJID(jid):
					action = submenu.addAction(self.tr("Always hide my status to contact"))
					action.setData(QtCore.QVariant(jid))
					action.setObjectName("privacy_hide")
				else:
					action = submenu.addAction(self.tr("Don't hide my status to contact"))
					action.setData(QtCore.QVariant(jid))
					action.setObjectName("privacy_unhide")
		if len(contact.resources)!=0:
			if oneres:
				action=contactMenu.addAction(QtGui.QIcon("images/16x16/actions/exec.png"),self.tr("Extra actions"))
				action.setData(QtCore.QVariant("%s/%s" % (jid, contact.resources.keys()[0])))
				action.setObjectName("ad_hoc")
			else:
				submenu=contactMenu.addMenu(QtGui.QIcon("images/16x16/actions/exec.png"),self.tr("Extra actions"))
				for res in contact.resources.keys():
					if res != None:
						action=submenu.addAction(res)
						action.setData(QtCore.QVariant("%s/%s" %(jid,res)))
						action.setObjectName("ad_hoc")
		
		# signal
		contactMenu.connect(contactMenu, QtCore.SIGNAL("triggered ( QAction * )"),self.contactMenuTriggered)
		return contactMenu

	def buildGroupMenu(self,name):
		# build contact menu
		contactMenu=QtGui.QMenu(self)
		action=contactMenu.addAction(self.tr("Rename"))
		action.setData(QtCore.QVariant(name))
		action.setObjectName("rename")
		
		action=contactMenu.addAction(self.tr("Remove group"))
		action.setData(QtCore.QVariant(name))
		action.setObjectName("remove_group")
		# signal
		contactMenu.connect(contactMenu, QtCore.SIGNAL("triggered ( QAction * )"),self.groupMenuTriggered)
		return contactMenu
	
	def groupMenuTriggered(self,action):
		cmd=action.objectName()
		if cmd=="rename":
			name=action.data()
			name=unicode(name.toString())
			group,b=QtGui.QInputDialog.getText(self.main,self.tr("Rename group"),self.tr("Enter new group name"), QtGui.QLineEdit.Normal, "")
			group=unicode(group)
			# if user set new name of group
			if b==True and len(group)!=0:
				for item in self.getAllGroupUsers(name):
					jid=item.jid
					contact=self.main.client.roster['users'][jid]
					for count in range(self.main.client.roster['users'][jid].groups.count(name)):
						self.main.client.roster['users'][jid].groups.remove(name)
					self.main.client.roster['users'][jid].groups.append(group)
					self.main.client.sendRosterUpdate(contact.jid, contact.name, contact.subscription,self.main.client.roster['users'][jid].groups)
		elif cmd=="remove_group":
			name=action.data()
			name=unicode(name.toString())
			ret=QtGui.QMessageBox.question(self,self.tr("Remove group?"), self.tr("Do you want to remove group ")+unicode(name)+self.tr(" from your roster?"),QtGui.QMessageBox.Yes|QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
			if ret==QtGui.QMessageBox.Yes:
				for item in self.getAllGroupUsers(name):
					jid=item.jid
					contact=self.main.client.roster['users'][jid]
					g=contact.groups
					g.remove(name)
					self.main.client.sendRosterUpdate(contact.jid, contact.name, contact.subscription,g)

	def breakMetaContacts(self,jid):
		item=self.getUserItems(jid)[0]
		metajid=item.metajid
		for it in self.getUserItems(jid):
			self.users.remove(it)
		for it in self.metaItems[metajid]:
			del self.main.client.roster_meta[it.jid]
			self.main.client.on_UpdateContact(it.jid)
		del self.metaItems[metajid]
		self.main.client.setMetacontacts()

	def contactMenuTriggered(self,action):
		# contact menu action handler
		cmd=action.objectName()
		if cmd=="delete_action":
			# delete contact from roster
			print "delete contact CLICKED"
			jid=action.data()
			jid=unicode(jid.toString())
			ret=QtGui.QMessageBox.question(self,self.tr("Delete contact?"), self.tr("Do you want to delete this contact from your roster?"),QtGui.QMessageBox.Yes|QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
			if ret==QtGui.QMessageBox.Yes:
				self.main.client.delContact(jid)
		elif cmd=="break_up_meta":
			# break up metacontact
			jid=action.data()
			jid=unicode(jid.toString())
			self.breakMetaContacts(jid)
		elif cmd=="rename":
			# rename contact
			jid=action.data()
			jid=unicode(jid.toString())
			try:
				name=unicode(self.main.client.roster['users'][jid].name)
			except:
				name = ''
			if len(name) == 0:
				name = jid.split('@')[0]
			name,b=QtGui.QInputDialog.getText(self.main,self.tr("Rename"),self.tr("Enter new name:"), QtGui.QLineEdit.Normal, name)
			name=unicode(name)
			# if user set new name
			if b==True and len(name)!=0:
				# change name
				contact=self.main.client.roster['users'][jid]
				self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription, self.main.client.roster['users'][jid].groups)
		elif cmd=="new_group":
			# add contact to the new group
			# get contact jid
			jid=action.data()
			jid=unicode(jid.toString())
			name=unicode(self.main.client.roster['users'][jid].name)
			group,b=QtGui.QInputDialog.getText(self.main,self.tr("New group"),self.tr("Add user to new group"), QtGui.QLineEdit.Normal, "")
			group=unicode(group)
			# if user set new name of group
			if b==True and len(group)!=0:
				# add new group
				contact=self.main.client.roster['users'][jid]
				self.main.client.sendRosterUpdate(contact.jid, contact.name, contact.subscription, self.main.client.roster['users'][jid].groups+[group])
		elif cmd=="check_group":
			# change users group
			items=action.data()
			items=items.toList()
			jid=unicode(items[0].toString())
			action=unicode(items[1].toString())[0]
			group=unicode(items[1].toString())[1:]
			self.changeGroup(jid,action,group)
		elif cmd=="vcard":
			# get vcard of selected contact
			jid=action.data()
			jid=unicode(jid.toString())
			#self.main.client.getVCard(jid)
			self.ve=vcardeditor.vcardEditorDialog(self.main,jid,self.main,False)
			self.ve.show()
			#d=self.main.client.getVCard(jid)
			#d.addCallback(self.vcardArrived)
		elif cmd=="chat":
			# chat with selected contact
			jid=action.data()
			jid=unicode(jid.toString())
			#if jid.find("/") == -1:
				#item=self.getUserItems(jid)[0]
				#self.main.chat.addChatTab(item.jid,item.name,self.main.getIcon(item.jid,self.main.icons[str(item.status)],size="16x16"))
			#else:
				#jid_r, res = jid.split("/", 1)
				#item=self.getUserItems(jid_r)[0]
				#self.main.chat.addChatTab(jid,"%s/%s" % (item.name, res),self.main.getIcon(item.jid,self.main.icons[str(item.status)],size="16x16"))
			
			jid=jidT.JID(jid)
			if not jid.resource:
				item=self.getUserItems(jid.userhost())[0]
				res = self.main.client.roster['users'][jid.userhost()].getHighestResource()
				if res==None:
					self.main.chat.addChatTab(item.jid,item.name,self.main.getIcon(item.jid,self.main.icons[str(item.status)],size="16x16"))
				else:
					self.main.chat.addChatTab(item.jid+"/"+res,item.name,self.main.getIcon(item.jid,self.main.icons[str(item.status)],size="16x16"))
			else:
				item=self.getUserItems(jid.userhost())[0]
				self.main.chat.addChatTab(jid.full(),item.name,self.main.getIcon(item.jid,self.main.icons[str(item.status)],size="16x16"))
			self.main.chat.activate()
		elif cmd == "invite_gc":
			user_jid, room_jid = [unicode(val.toString()) for val in action.data().toList()]
			reason = self.tr("Hi! I'd love to see you in multichat at ") + room_jid
			self.main.client.sendInvitation(user_jid, room_jid, reason)

		elif cmd=="custom_status":
			show, jid = [unicode(val.toString()) for val in action.data().toList()]
			self.main.sendCustomStatus(jid, show)

		elif cmd=="send_file":
			# sends files to contact
			jid=action.data()
			jid=unicode(jid.toString())
			self.main.sendFiles(jid)
			#file=QtGui.QFileDialog.getOpenFileNames(self.main,"Choose file")
			#file=list(file)
			#if len(file)!=0:
				#new=[]
				#for f in file:
					#new.append(unicode(f))
				#file=new
				#self.dialog=filetransfer.filetransferDialog(self.main,file,jid)
				#self.dialog.show()
		elif cmd == "a_authorize":
			jid=action.data()
			jid=unicode(jid.toString())
			self.main.client.sendPresence(jid, typ="subscribed")
			value = self.main.client.roster['users'][jid].subscription
			if value == "none":
				self.main.client.roster['users'][jid].subscription = "from"
			elif value == "to":
				self.main.client.roster['users'][jid].subscription = "both"
			log.msg("%s authorized" % jid)
		elif cmd == "a_unauthorize":
			jid=action.data()
			jid=unicode(jid.toString())
			self.main.client.sendPresence(jid, typ="unsubscribed")
			value = self.main.client.roster['users'][jid].subscription
			if value == "from":
				self.main.client.roster['users'][jid].subscription = "none"
			elif value == "both":
				self.main.client.roster['users'][jid].subscription = "to"
			log.msg("removed autorization from %s" % jid)
		elif cmd == "a_ask":
			jid=action.data()
			jid=unicode(jid.toString())
			self.main.client.sendPresence(jid, typ="subscribe")
			log.msg("sent subscription request to %s" % jid)

		elif cmd == "privacy_block":
			jid=unicode(action.data().toString())
			self.main.client.privacy.active.blockJID(jid)
			log.msg("Blocking jid %s." % jid)
			self.main.client.sendPresence(jid, typ="unavailable")
		elif cmd == "privacy_unblock":
			jid=unicode(action.data().toString())
			self.main.client.privacy.active.unBlockJID(jid)
			log.msg("Unblocking jid %s." % jid)


		elif cmd == "privacy_allow":
			jid=unicode(action.data().toString())
			self.main.client.privacy.active.allowJID(jid)
			log.msg("Allowing jid %s." % jid)
		elif cmd == "privacy_disallow":
			jid=unicode(action.data().toString())
			self.main.client.privacy.active.disAllowJID(jid)
			log.msg("Disallowing jid %s." % jid)

		elif cmd == "privacy_hide":
			jid=unicode(action.data().toString())
			self.main.client.privacy.active.hideJID(jid)
			log.msg("Hiding jid %s." % jid)
			self.main.client.sendPresence(jid, typ="unavailable")
		elif cmd == "privacy_unhide":
			jid=unicode(action.data().toString())
			self.main.client.privacy.active.unHideJID(jid)
			log.msg("Unhiding jid %s." % jid)
		elif cmd == "ad_hoc":
			jid=unicode(action.data().toString())
			self.cmds = commands.Commands(self.main, jid)
			self.cmds.dialog.show()
		log.msg("END CONTACT")

	#def vcardArrived(self,data):
		#self.dialog=vcardview.vcardViewDialog(self.main,data,self)
		#self.dialog.show()
		#self.ve=vcardeditor.vcardEditorDialog(self.main,data,self,False)
		#self.ve.show()
		

	def changeGroup(self,jid,action,group):
		# change group of users
		name=unicode(self.main.client.roster['users'][jid].name)
		if action=="+":
			contact=self.main.client.roster['users'][jid]
			self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription, self.main.client.roster['users'][jid].groups+[group])
		else:
			contact=self.main.client.roster['users'][jid]
			g=contact.groups
			g.remove(group)
			self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription,g)

	def contextMenuEvent (self,event):
		# show contact context menu
		item=self.itemAt(event.x(),event.y())
		if item.typ=="user":
			if self.item!=item:
				self.selectItem(item)
			group=item.group
			jid=item.jid
			#if self.main.client.roster['users'].has_key(jid):
			contactMenu=self.buildContactMenu(unicode(jid),group)
			#contactMenu.move(event.globalX(),event.globalY())
			contactMenu.popup(QtCore.QPoint(event.globalX(),event.globalY()))
		elif item.typ=="group":
			contactMenu=self.buildGroupMenu(item.name)
			contactMenu.move(event.globalX(),event.globalY())
			contactMenu.popup(QtCore.QPoint(event.globalX(),event.globalY()))
