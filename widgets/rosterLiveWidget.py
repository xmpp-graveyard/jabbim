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
import sys,os

try: from PyQt4 import QtCore, QtGui
except: print "PyQt4 is not installed."
from os.path import basename
from twisted.python import log
import filetransfer

class activeWidget(QtGui.QWidget):
	def __init__(self,status,parent=None):
		QtGui.QWidget.__init__(self,parent)
		layout=QtGui.QVBoxLayout(self)
		layout.setMargin(2)
		self.stacked=QtGui.QStackedWidget(self)
		layout.addWidget(self.stacked)
		self.setAutoFillBackground(False)
		self.stacked.setAutoFillBackground(False)
		self.stacked.setCurrentIndex(0)
	
	def addStatusOnly(self,status):
		statusLabel=QtGui.QTextEdit(self)
		statusLabel.setReadOnly(True)
		statusLabel.viewport().setAutoFillBackground(False)
		statusLabel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		statusLabel.setHtml("<font size=\"-1\">"+unicode(status)+"</font>")
		statusLabel.setFrameShape(QtGui.QFrame.NoFrame)
		statusLabel.setFrameShadow(QtGui.QFrame.Plain)
		#statusLabel.setMaximumHeight(64)
		#layout.addWidget(statusLabel)

		self.stacked.addWidget(statusLabel)

	def addResource(self,resource):
		widget=QtGui.QWidget(self)
		widget.setAutoFillBackground(False)
		layout=QtGui.QVBoxLayout(widget)
		layout.setMargin(0)
		layout.setSpacing(0)
		label=QtGui.QLabel("Resource: "+resource.name)
		label.setTextFormat(QtCore.Qt.RichText)
		label.setMaximumHeight(32)
		layout.addWidget(label)
		if resource.status:
			statusLabel=QtGui.QTextEdit(self)
			statusLabel.setReadOnly(True)
			statusLabel.viewport().setAutoFillBackground(False)
			statusLabel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
			statusLabel.setHtml("<font size=\"-1\">"+unicode(resource.status)+"</font>")
			statusLabel.setFrameShape(QtGui.QFrame.NoFrame)
			statusLabel.setFrameShadow(QtGui.QFrame.Plain)
			#statusLabel.setMaximumHeight(32)
			layout.addWidget(statusLabel)
		layout.addStretch()
		self.stacked.addWidget(widget)


class activeButtons(QtGui.QWidget):
	def __init__(self,main,buttons,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.main=main
		self.layout=QtGui.QHBoxLayout(self)
		self.layout.setMargin(0)
		self.layout.setSpacing(0)
		self.setAutoFillBackground(False)
		self.buttons={}
		i=0
		group=QtGui.QButtonGroup(self)
		for b in buttons:
			if b=="separator":
				line = QtGui.QFrame(self)
				line.setFrameShape(QtGui.QFrame.VLine)
				line.setFrameShadow(QtGui.QFrame.Sunken)
				self.layout.addWidget(line)
			else:
				button = QtGui.QPushButton(self)
				#button.setGeometry(0,y+16,16,16)
				button.setMaximumSize(16,16)
				button.setFlat(True)
				button.setIcon(b)
				self.layout.addWidget(button)
				group.addButton(button)
				self.buttons[button]=i
				i+=1
		self.layout.addStretch()
		QtCore.QObject.connect(group,QtCore.SIGNAL("buttonClicked ( QAbstractButton * )"),self.clicked)
	
	def clicked(self,button):
		self.main.statusLabel.stacked.setCurrentIndex(self.buttons[button])

class groupItem:
	def __init__(self,name,icon,main):
		self.name=name
		self.icon=icon
		self.expanded=False
		self.typ='group'
		self.main=main
	
	def setExpanded(self,bool):
		self.expanded=bool
		if not self.expanded:
			self.icon=QtGui.QIcon("images/"+self.main.iconSize+"/icons/group-closed.png")
		else:
			self.icon=QtGui.QIcon("images/"+self.main.iconSize+"/icons/group-open.png")

class userItem:
	def __init__(self,name,group,main,icon=None):
		self.name=name
		self.backName=name
		self.icon=icon
		self.typ='user'
		self.group=group
		self.status=9
		self.statusMessage=None
		self.main=main
		self.avatar=None
		self.hidden=False
		self.test=None

	def clone(self):
		item=userItem(unicode(self.name),unicode(self.group),unicode(self.main),self.icon)
		item.statusMessage=unicode(self.statusMessage)
		item.avatar=self.avatar
		item.hidden=self.hidden
		item.jid=unicode(self.jid)
		return item

	def setIcon(self,icon):
		self.icon=icon
		self.main.repaint()
	
	def setAvatar(self,icon):
		self.avatar=icon
		self.main.repaint()
	
	def setHidden(self,hidden):
		self.hidden=hidden
		self.main.repaint()

class special:
	def __init__(self):
		self.typ="group"
		self.main="special"
		self.name="zzzzzzzzzzzzzzzzz"
		self.expanded=False

class rosterWidget(QtGui.QWidget):
	def __init__(self,parent=None,main=None):
		QtGui.QWidget.__init__(self,parent)
		self.main=main
		self.groups={}
		self.groups["zzzzzzzzzzzzzzzzz"]=special()
		self.users=[]
		self.iconSize="32x32"
		self.setMinimumWidth(150)
		self.setMinimumHeight(150)
		self.setAcceptDrops(True)
		self.groupGradient=QtGui.QLinearGradient(QtCore.QPointF(0, 0), QtCore.QPointF(0, 32))
		self.groupGradient.setColorAt(1, QtCore.Qt.darkRed)
		self.groupGradient.setColorAt(0, QtCore.Qt.white)

		self.selectedGroupGradient=QtGui.QLinearGradient(QtCore.QPointF(0, 0), QtCore.QPointF(0, 96))
		self.selectedGroupGradient.setColorAt(0.9, QtCore.Qt.white)
		self.selectedGroupGradient.setColorAt(0.5, QtGui.QColor(185,227,255))
		self.selectedGroupGradient.setColorAt(0.1, QtCore.Qt.white)
		self.selectedGroupGradient.setSpread(QtGui.QGradient.RepeatSpread)

		self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

		self.selected=None
		
		self.showOffline=False

		self.setMouseTracking(True)
		self.newitem=None
		self.item=None
		self.timer=QtCore.QTimer(self)
		self.timer.setSingleShot(True)
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.popup)
		self.sortedGroups=[]
		self.sorted={}
		
		self.statusLabel=None
		self.buttonWidget=None
		self.bigAvatar=False

		self.setFocusPolicy(QtCore.Qt.ClickFocus)
		self.data={}
		self.metaItems={}

		#QtCore.QObject.connect(self.main.scroll, QtCore.SIGNAL("sliderMoved(int)"),self.slider)

	#def slider(self,y):
		#pass

	def sortItems(self,column=None,typ=None):
		self.sortedGroups=self.groups.keys()
		self.sortedGroups.sort()
		for group in self.sortedGroups:
			temp=[]
			for user in self.getGroupUsers(group):
				temp.append([unicode(user.status)+user.name,user])
			temp.sort()
			self.sorted[group]=temp
		print self.sorted
		self.setSize()

	def mouseMoveEvent(self,event):
		item,x,y=self.itemAt(int(event.x()),int(event.y()),1)
		if item:
			if event.buttons()==QtCore.Qt.NoButton:
				if self.item==item[0]:
					if event.x()>self.width()-32 and int(event.y())<y+32 and int(event.y())>y:
						self.bigAvatar=True
						if self.statusLabel:
							self.statusLabel.resize(self.width()-96,64)
						self.repaint()
					else:
						self.bigAvatar=False
						if self.statusLabel:
							self.statusLabel.resize(self.width(),64)
						self.repaint()
			else:
				if item[0].typ=='user':
					mimeData = QtCore.QMimeData()
					mimeData.setText(item[0].jid)
					self.data[mimeData]=item[0]
					drag = QtGui.QDrag(self)
					drag.setMimeData(mimeData)
					drag.setHotSpot(event.pos())
					#- self.rect().topLeft())
					#dropAction = drag.start(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)
					dropAction = drag.start(QtCore.Qt.CopyAction)

	def popup(self):
		self.item=self.newitem
		self.selected=self.item
		self.repaint()

	def addGroup(self,name):
		item=groupItem(name,QtGui.QIcon("images/"+self.iconSize+"/icons/group-closed.png"),self)
		self.groups[name]=item
		self.repaint()
		return item

	def addUser(self,jid,name,group,offline=True,first=False):
		if len(name)==0:
			name=jid
		item=userItem(name,group,self)
		item.icon=self.main.getIcon(jid,size="32x32",status=self.main.icons["9"])
		item.jid=jid
		item.hidden=True
		#self.sortItems()
		self.users.append(item)

	def getGroupUsers(self,group):
		ret=[]
		for user in self.users:
			if self.showOffline==True:
				if user.group==group:
					ret.append(user)
			else:
				if user.group==group and not user.hidden:
					ret.append(user)
		return ret

	def getGroupSortedUsers(self,group):
		ret=[]
		for key in self.sorted[group]:
			user=key[1]
			if self.showOffline==True:
				if user.group==group:
					ret.append(user)
			else:
				if user.group==group and not user.hidden:
					ret.append(user)
		return ret

	def paintGroupItem(self,painter,item,x,y):
		doc=QtGui.QTextDocument()
		#if item==self.selected:
			#painter.save()
			#painter.translate(x,y)
			#painter.fillRect(0,0,self.width(),32,QtGui.QBrush(self.selectedGroupGradient))
			#painter.restore()
		#else:
			#painter.save()
			#painter.translate(x,y)
			#painter.fillRect(0,0,self.width(),32,QtGui.QBrush(self.groupGradient))
			#painter.restore()
		
		b=painter.brush()
		p=painter.pen()
		painter.setBrush(QtGui.QBrush(QtGui.QColor(30,144,255)))
		painter.setPen(QtGui.QPen(QtGui.QColor(30,144,230)))
		painter.save()
		painter.translate(x,y)

		if y>16:
			painter.drawLine(2,0,self.width()-2,0)

		if item.main=="special":
			painter.drawLine(2,0,self.width()-2,0)
			painter.restore()
			painter.setBrush(b)
			painter.setPen(p)
			return
		painter.drawEllipse(2,8,16,16)
		painter.drawEllipse(self.width()-18,8,16,16)
		#painter.drawEllipse(2,16,16,16)
		#painter.drawEllipse(self.width()-18,16,16,16)
		painter.drawRect(2,16,self.width()-4,32)
		painter.drawRect(11,8,self.width()-22,32)
		painter.restore()
		painter.setBrush(b)
		painter.setPen(p)
		
		if item.icon:
			painter.drawPixmap(x,y+4,item.icon.pixmap(32,32))
		
		doc.setHtml("<font color=\"white\">"+item.name+"</font>")
		
		painter.save()
		painter.translate(x+30,y+10)
		doc.drawContents(painter, QtCore.QRectF(0,0,self.width(),y+32))
		painter.restore()

	def resizeEvent(self,event):
		if self.statusLabel:
			self.statusLabel.resize(self.width(),64)
		return QtGui.QWidget.resizeEvent(self,event)

	def paintUserItem(self,painter,useritem,x,y):
		if useritem==self.item:
			#painter.save()
			#painter.translate(x,y)
			#painter.fillRect(0,0,self.width(),96,QtGui.QBrush(self.selectedGroupGradient))
			#painter.restore()
			#palette=QtGui.QPalette()
			#painter.save()
			#painter.translate(x,y)
			#painter.fillRect(0,0,self.width(),32,QtGui.QBrush(palette.color(QtGui.QPalette.Highlight)))
			#painter.restore()
			p=painter.pen()
			painter.setPen(QtGui.QPen(QtGui.QColor(30,144,230)))
			painter.save()
			painter.translate(x,y)
			painter.fillRect(3,0,self.width()-3,96,QtGui.QBrush(QtGui.QColor(220,229,255)))

			painter.drawLine(2,0,2,96)
			painter.drawLine(self.width()-2,0,self.width()-2,96)
			painter.restore()
			painter.setPen(p)


			if useritem.icon:
				painter.drawPixmap(x+3,y,useritem.icon.pixmap(32,32))

			doc=QtGui.QTextDocument()
			
			#if useritem.avatar:
				#pixmap=useritem.avatar.pixmap(32,32)
				##doc.setTextWidth(self.width()-30-pixmap.width())
				#doc.setPageSize(QtCore.QSizeF(self.width()-30-pixmap.width(),32))
			#else:
				#doc.setPageSize(QtCore.QSizeF(self.width(),64))
			#option=QtGui.QTextOption()
			#option.setWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)
			#doc.setDefaultTextOption(option)
			#if useritem.statusMessage:
				#doc.setHtml(useritem.name)
				#painter.save()
				#painter.translate(x+30,y)
				#doc.drawContents(painter, QtCore.QRectF(0,0,self.width(),y+32))
				#painter.restore()
					##self.statusLabel.setGeometry(0,y+32,self.width(),64)
					##self.statusLabel.show()
				##doc.setHtml("JID:<b>"+useritem.jid+"</b>")
				##painter.save()
				##painter.translate(4,y+32)
				##doc.drawContents(painter, QtCore.QRectF(0,0,self.width(),y+32))
				##painter.restore()
			#else:
			doc.setHtml(useritem.name)
			painter.save()
			painter.translate(x+35,y)
			doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-33,y+28))
			painter.restore()
			if not self.statusLabel:
				self.statusLabel=activeWidget(useritem.statusMessage,self)
				self.statusLabel.setGeometry(3,y+32,self.width()-3,64)
				self.statusLabel.show()
			if not self.buttonWidget and self.statusLabel:
				buttons=[]
				if self.metaItems.has_key(useritem.jid):
					for meta in self.metaItems[useritem.jid]:
						buttons.append(self.main.getIcon(meta.jid,size="16x16",status=self.main.icons[unicode(meta.status)]))
				#high=self.main.client.roster['users'][useritem.jid].getHighestResource()
				#if high:
					#high=self.main.client.roster['users'][useritem.jid].resources[high]
					#buttons.append(self.main.getIcon(useritem.jid,size="16x16",status=self.main.icons[self.main.shows[high.show]]))
					#print "YES",buttons
					#self.statusLabel.addResource(high)
					#for key,resource in self.main.client.roster['users'][useritem.jid].resources.iteritems():
						#if resource!=high:
							#buttons.append(self.main.getIcon(useritem.jid,size="16x16",status=self.main.icons[self.main.shows[resource.show]]))
							#self.statusLabel.addResource(resource)
					#print buttons
					self.buttonWidget=activeButtons(self,buttons,self)
					self.buttonWidget.setGeometry(35,y+16,self.width()-3,16)
					self.buttonWidget.show()
				else:
					## no resource
					if useritem.statusMessage:
						self.statusLabel.addStatusOnly(useritem.statusMessage)
						
			if useritem.avatar:
				#if self.bigAvatar:
					#pixmap=useritem.avatar.pixmap(96,96)
					#painter.drawPixmap(self.width()-pixmap.width()-3,y,pixmap)
				#else:
				pixmap=useritem.avatar.pixmap(32,32)
				painter.drawPixmap(self.width()-pixmap.width()-3,y,pixmap)

		else:
			#if event.region().contains(QtCore.QRect(0,y,self.width(),y+32)):
				#paint=True
			#if useritem==self.selected:
				#painter.save()
				#painter.translate(x,y)
				#painter.fillRect(0,0,self.width(),32,QtGui.QBrush(self.selectedGroupGradient))
				#painter.restore()
			#else:
			p=painter.pen()
			painter.setPen(QtGui.QPen(QtGui.QColor(30,144,230)))
			painter.save()
			painter.translate(x,y)
			painter.fillRect(0,0,self.width(),32,QtGui.QBrush(QtGui.QColor(255,255,255)))

			painter.drawLine(2,0,2,32)
			painter.drawLine(self.width()-2,0,self.width()-2,32)
			painter.restore()
			painter.setPen(p)



			if useritem.icon:
				painter.drawPixmap(x+3,y,useritem.icon.pixmap(32,32))

			doc=QtGui.QTextDocument()
			
			
			if useritem.statusMessage:
				doc.setHtml(useritem.name+"<br/><font size=\"-1\"><i>"+useritem.statusMessage+"</i></font>")
				painter.save()
				painter.translate(x+34,y)
				if useritem.avatar:
					doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-70,y+32))
				else:
					doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-38,y+32))
				painter.restore()
			else:
				doc.setHtml(useritem.name)
				painter.save()
				painter.translate(x+34,y+6)
				doc.drawContents(painter, QtCore.QRectF(0,0,self.width()-38,y+28))
				painter.restore()
			if useritem.avatar:
				painter.drawPixmap(self.width()-36,y,useritem.avatar.pixmap(32,32))

	def paintEvent(self,event):
		painter=QtGui.QPainter(self)
		painter.setClipping(True)
		painter.setRenderHint(painter.Antialiasing)
		painter.setClipRegion(event.region())
		for rect in event.region().rects():
			count=int(rect.height()/32)
			if float(rect.height())/32.0>float(count):
				count+=1
			items,x,y=self.itemAt(1,rect.y(),count+1)
			for item in items:
				if item.typ=="group":
					self.paintGroupItem(painter,item,0,y)
					y+=32
				else:
					self.paintUserItem(painter,item,0,y)
					if self.item==item:
						y+=64
					y+=32

	def itemAt(self,x1,y1,count=None):
		x=0
		y=0
		got=0
		gotx=0
		goty=0
		ret=[]
		for key in self.sortedGroups:
			item=self.groups[key]
			items=self.getGroupSortedUsers(item.name)
			if ((len(items)!=0 and not self.showOffline) or self.showOffline) or item.main=="special":
				if got!=0 and not item in ret:
					ret.append(item)
					got+=1
				if y1>=y and y1<=y+32:
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
						y+=32
						if got!=0 and not useritem in ret:
							ret.append(useritem)
							got+=1

						if useritem==self.item:
							if y1>=y and y1<=y+64+32:
								if count and not useritem in ret:
									ret.append(useritem)
									got+=1
									goty=y
								if not count:
									return useritem
						else:
							if y1>=y and y1<=y+32:
								if count and not useritem in ret:
									ret.append(useritem)
									got+=1
									goty=y
								if not count:
									return useritem
						if got==count:
							return ret,0,goty
						if useritem==self.item:
							y+=64

					#if useritem==self.item:
						#y-=32
				y+=32
		if got!=0:
			return ret,0,goty

		if count:
			return [],None,None

	def itemCoordinates(self,i):
		x=0
		y=0
		for key in self.sortedGroups:
			item=self.groups[key]
			items=self.getGroupSortedUsers(item.name)
			if ((len(items)!=0 and not self.showOffline) or self.showOffline) or item.main=="special":
				if item==i:
					return x,y
				if item.expanded and len(items)!=0:
					previous=None
					for useritem in items:
						y+=32
						if useritem==i:
							return x,y
						if useritem==self.item:
							y+=64

					#if useritem==self.item:
						#y-=32
				y+=32

		return None,None

	def setSize(self):
		x=0
		y=0
		for key in self.sortedGroups:
			item=self.groups[key]
			items=self.getGroupSortedUsers(item.name)
			if (len(items)!=0 and not self.showOffline) or self.showOffline:
				if item.expanded and len(items)!=0:
					for useritem in items:
						y+=32

				y+=32

		self.setMinimumHeight(y+64)

	def selectItem(self,item):
		if self.item!=item and item!=None and item.main!='special':
			self.item=item
			self.selected=item
			if self.statusLabel:
				self.statusLabel.setParent(None)
				self.statusLabel=None
			if self.buttonWidget:
				self.buttonWidget.setParent(None)
				self.buttonWidget=None
			self.repaint()

	def mousePressEvent(self,event):
		x=event.x()
		y=event.y()
		item=self.itemAt(x,y)
		self.selectItem(item)

		if item.typ=='group':
			if item.expanded:
				item.icon=QtGui.QIcon("images/"+self.iconSize+"/icons/group-closed.png")
				item.expanded=False
			else:
				item.icon=QtGui.QIcon("images/"+self.iconSize+"/icons/group-open.png")
				item.expanded=True
			self.setSize()
			self.repaint()

		QtGui.QWidget.mousePressEvent(self,event)

	def mouseDoubleClickEvent(self,event):
		x=event.x()
		y=event.y()
		item=self.itemAt(x,y)
		if item.typ=='group':
			if item.expanded:
				item.icon=QtGui.QIcon("images/"+self.iconSize+"/icons/group-closed.png")
				item.expanded=False
			else:
				item.icon=QtGui.QIcon("images/"+self.iconSize+"/icons/group-open.png")
				item.expanded=True
			self.setSize()
			self.repaint()
		else:
			self.main.chat.addChatTab(item.jid,item.name,self.main.getIcon(item.jid,self.main.icons[str(item.status)],size="16x16"))
			self.main.chat.activate()

	def keyPressEvent(self,event):
		key=event.key()
		if key==QtCore.Qt.Key_Down:
			x,y=self.itemCoordinates(self.item)
			if self.item.typ=="group":
				item=self.itemAt(x,y+33)
			else:
				item=self.itemAt(x,y+97)
			self.selectItem(item)
			event.accept()
		elif key==QtCore.Qt.Key_Up:
			x,y=self.itemCoordinates(self.item)
			#if self.item.typ=="group":
				#item=self.itemAt(x,y+33)
			#else:
			item=self.itemAt(x,y-3)
			self.selectItem(item)
			event.accept()
		event.ignore()
			

	def dragEnterEvent(self, event):
		if event.mimeData().hasText():
			event.acceptProposedAction()
		else:
			event.ignore()

	def dragMoveEvent(self, event):
		pos=event.pos()
		#print pos.x(),pos.y()
		item=self.itemAt(pos.x(),pos.y())
		if item:
			event.acceptProposedAction()
		else:
			event.ignore()

	def dropEvent(self, event):
		if event.mimeData().hasText():
			jid = unicode(event.mimeData().text())
			position = event.pos()
			item=self.itemAt(position.x(),position.y())
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
			items=QtCore.QStringList()
			if item.typ=="group":
				items.append(self.tr("Move"))
				items.append(self.tr("Copy"))
			else:
				items.append(self.tr("Move to group"))
				items.append(self.tr("Make metacontact"))
				items.append(self.tr("Copy to group"))
			q,b=QtGui.QInputDialog.getItem(self,self.tr("Contact action"),self.tr("Select action."), items,0,False)
			q=unicode(q)
			# if user set new name of group
			if b==True and len(q)!=0:
				if item.typ=='group':
					index=int(items.indexOf(QtCore.QRegExp(q)))
					if index==1:
						self.changeGroup(jid,"+",unicode(item.name))
					else:
						name=unicode(self.main.client.roster['users'][jid].name)
						contact=self.main.client.roster['users'][jid]
						g=contact.groups
						g.remove(unicode(self.groups[oldItem.group].name))
						self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription,g+[unicode(item.name)])
				else:
					index=int(items.indexOf(QtCore.QRegExp(q)))
					if index==2:
						self.changeGroup(jid,"+",unicode(item.group))
					elif index==0:
						name=unicode(self.main.client.roster['users'][jid].name)
						contact=self.main.client.roster['users'][jid]
						g=contact.groups
						g.remove(unicode(self.groups[oldItem.group].name))
						self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription,g+[unicode(item.group)])
					else:
						self.main.client.roster_meta[item.jid]={'tag':item.jid,'order':1}
						self.main.client.roster_meta[jid]={'tag':item.jid,'order':1}
						self.main.client.setMetacontacts()
			del self.data[event.mimeData()]

		else:
			event.ignore()

	
		

	def makeHiddenItem(self):
		pass

	def mimeTypes(self):
		# set mimetypes, which we accept
		return QtCore.QStringList("text/plain")

	def getGroupItem(self,name):
		return None

	def getHostItems(self,host):
		return []


	def getUserItems(self,jid,typ=False):
		ret=[]
		for user in self.users:
			if user.jid==jid:
				ret.append(user)
		return ret


	def hidden(self,bool):
		pass


	def refreshStats(self):
		pass

	def setStatus(self,jid,show,i=None,status=None,first=False):
		for user in self.getUserItems(jid):
			user.icon=self.main.getIcon(jid,size="32x32",status=self.main.icons[self.main.shows[unicode(show)]])
			if self.main.shows[unicode(show)]!="9":
				user.hidden=False
			else:
				user.hidden=True
			user.statusMessage=status
			user.status=self.main.shows[unicode(show)]
			if not first:
				if self.statusLabel:
					self.statusLabel.setParent(None)
					self.statusLabel=None
				if self.buttonWidget:
					self.buttonWidget.setParent(None)
					self.buttonWidget=None
				self.sortItems()
				
		self.repaint()

	def cloneContact(self,parent,item):
		pass

		
	def buildContactMenu(self,jid,group):
		# build contact menu
		contactMenu=QtGui.QMenu(self)
		# chat
		action=contactMenu.addAction(self.tr("Chat"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("chat")
		# separator
		contactMenu.addSeparator()
		# vcard
		action=contactMenu.addAction(self.tr("vCard"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("vcard")
		# vcard
		action=contactMenu.addAction(self.tr("Send file"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("send_file")
		# separator
		contactMenu.addSeparator()
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
		for k,v in self.main.client.roster['groups'].iteritems():
			if k!="Unknown":
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
				
		# signal
		contactMenu.connect(contactMenu, QtCore.SIGNAL("triggered ( QAction * )"),self.contactMenuTriggered)
		return contactMenu

	def buildGroupMenu(self,name):
		pass

	def groupMenuTriggered(self,action):
		pass

	def contactMenuTriggered(self,action):
		# contact menu action handler
		cmd=action.objectName()
		if cmd=="delete_action":
##			print "delete_action"
			## delete contact from roster
			## get contact jid
			print "delete contact CLICKED"
			jid=action.data()
			jid=str(jid.toString())
			self.main.client.delContact(jid)
			#print "roster_delete_action",jid
			## delete user from groups
			#for user in self.getUsers(jid):
				#self.delUser(jid,user)
			#QtGui.QApplication.postEvent(self.jab,customEvent(["roster_del_item",jid]))
			##self.jab.roster.delItem(jid) # send jabber command
			#self.refreshStats() # refresh group stats
		elif cmd=="rename":
			# add contact to the new group
			# get contact jid
			jid=action.data()
			jid=str(jid.toString())
			#name=unicode(self.main.client.roster['users'][jid].name)
##			print "roster_new_group_action",jid,name
			# get new group name with QDialog
			name,b=QtGui.QInputDialog.getText(self,self.tr("Rename"),self.tr("Enter new name:"), QtGui.QLineEdit.Normal, "")
			name=unicode(name)
			# if user set new name of group
			if b==True and len(name)!=0:
				# add new group
				contact=self.main.client.roster['users'][jid]
				self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription, self.main.client.roster['users'][jid].groups)
		elif cmd=="new_group":
			# add contact to the new group
			# get contact jid
			jid=action.data()
			jid=str(jid.toString())
			name=unicode(self.main.client.roster['users'][jid].name)
##			print "roster_new_group_action",jid,name
			# get new group name with QDialog
			group,b=QtGui.QInputDialog.getText(self,self.tr("New group"),self.tr("Add user to new group"), QtGui.QLineEdit.Normal, "")
			group=unicode(group)
			# if user set new name of group
			if b==True and len(group)!=0:
				# add new group
				contact=self.main.client.roster['users'][jid]
				self.main.client.sendRosterUpdate(contact.jid, contact.name, contact.subscription, self.main.client.roster['users'][jid].groups+[group])
		elif cmd=="check_group":
			items=action.data()
			items=items.toList()
			jid=str(items[0].toString())
			action=unicode(items[1].toString())[0]
			group=unicode(items[1].toString())[1:]

			#if self.main.groups.has_key(group):
				#if self.main.groups[group]['item']==self.main.groups['Unknown']['item']:
					#group="Unknown"
			#else:
				#group="Unknown"
			self.changeGroup(jid,action,group)
			
		elif cmd=="vcard":
			# get vcard of selected contact
			jid=action.data()
			jid=str(jid.toString())
			#QtGui.QApplication.postEvent(self.jab,customEvent(["get_vcard",jid]))
			self.main.client.getVCard(jid)
			#self.jab.getVCard(jid)
		elif cmd=="avatar":
			# get avatar of selected contact
			jid=action.data()
			jid=str(jid.toString())
			QtGui.QApplication.postEvent(self.jab,customEvent(["get_vcard",jid]))
			#self.jab.getVCard(jid,True)
		elif cmd=="get_avatars":
			# get avatars of users in selected group
			group=action.data()
			if not self.main.groups.has_key(group):
				group="Unknown"
			for jid,item in self.main.groups[group]["users"].iteritems():
				QtGui.QApplication.postEvent(self.jab,customEvent(["get_vcard",jid]))
				#self.jab.getVCard(jid,True)
		elif cmd=="chat":
			# chat with selected contact
			jid=action.data()
			jid=str(jid.toString())
			item=self.getUserItems(jid)[0]
			self.main.chat.addChatTab(item.jid,item.name,self.main.getIcon(item.jid,self.main.icons[str(item.status)],size="16x16"))
			self.main.chat.activate()

		elif cmd=="send_file":
			# chat with selected contact
			jid=action.data()
			jid=str(jid.toString())
			#jid=jid+"/"+self.getResources(jid)[0]
			file=QtGui.QFileDialog.getOpenFileNames(self,"Choose file")
			file=list(file)
			if len(file)!=0:
##				print file,"to",jid
				new=[]
				for f in file:
					new.append(unicode(f))
				file=new
				self.dialog=filetransfer.filetransferDialog(self.main,file,jid)
				self.dialog.show()
				#files=new
				#all=len(file)
				#file=file[0]
				#file=unicode(file)
				##self.jab.sendFile(jid,unicode(file))
				#res = self.main.client.roster['users'][jid].getHighestResource()
				#sid=self.main.client.sendFile(jid+'/'+res, basename(file), file)
				#self.main.filetransferQueue[sid]=files
				#item=QtGui.QListWidgetItem(self.main.ui.eventsListWidget)
				#item.setSizeHint(QtCore.QSize(100,60))
				#item.queueId=sid
				#item.file=file
				#item.jid=jid+'/'+res
				#item.sent=1
				#item.broken=[]
				#item.all=all
				#item.widget=FTWidget(basename(file),item,self.main,sid,self.main.ui.eventsListWidget)
				#self.main.ui.eventsListWidget.setItemWidget(item,item.widget)
				#self.main.filetransfer[sid]=item
				##self.main.filetransferTimer.start(500)
		log.msg("END CONTACT")
	def changeGroup(self,jid,action,group):
			name=unicode(self.main.client.roster['users'][jid].name)
			if action=="+":
				contact=self.main.client.roster['users'][jid]
##				print "adding",jid,"groups:",self.main.client.roster['users'][jid].groups+[group]
				self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription, self.main.client.roster['users'][jid].groups+[group])
			else:
				contact=self.main.client.roster['users'][jid]
				g=contact.groups
				g.remove(group)
##				print "deleting",jid,"groups:",g,'name:',name
				self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription,g)

	def contextMenuEvent (self,event):
		# show contact context menu
		item=self.itemAt(event.x(),event.y())
		group=item.group
		jid=item.jid
		#if self.main.client.roster['users'].has_key(jid):
		contactMenu=self.buildContactMenu(str(jid),group)
		contactMenu.move(event.globalX(),event.globalY())
		contactMenu.show()
		#else:
			#contactMenu=self.buildGroupMenu(unicode(item.text(2)))
			#contactMenu.move(event.globalX(),event.globalY())
			#contactMenu.show()



#app=QtGui.QApplication([])
#win=QtGui.QMainWindow()
#scroll=QtGui.QScrollArea(win)
#roster = rosterWidget(scroll)
#scroll.setWidget(roster)
##layout=QtGui.QHBoxLayout(scroll)
##layout.addWidget(roster)
##layout.setMargin(0)
#win.setCentralWidget(scroll)

#roster.addGroup("Jabber")
#roster.addUser('test',"HanzZ","ICQ")
#roster.addUser('lala',"Sef","ICQ")
#roster.addGroup("ICQ")
#roster.addUser('test',"HanzZ","Jabber")
#roster.addUser('lala',"Sef","Jabber")
#roster.addUser('test',"HanzZ","Jabber")
#roster.addUser('lala',"Sef","Jabber")
#roster.addGroup("AIM")
#roster.addUser('test',"HanzZ","AIM")
#roster.addUser('lala',"Sef","AIM")
#roster.addUser('test',"HanzZ","AIM")
#roster.addUser('lala',"Sef","AIM")
#win.show()
#app.exec_()


