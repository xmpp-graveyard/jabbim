import os
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from tooltip_ui import *
#from eventsFTWidget_ui import *
from os.path import basename
from twisted.python import log


class doc(QtGui.QTextDocument):
	def __init__(self,parent=None):
		apply(QtGui.QTextDocument.__init__,(self,parent))

class SubscribeWidget(QtGui.QWidget):
	def __init__(self,frm,item,main,parent=None,stats=""):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.setObjectName("SubscribeWidget")
		self.item=item
		self.main=main
		self.frm=frm
		self.status=stats
		self.gridlayout = QtGui.QGridLayout(self)
		self.gridlayout.setMargin(0)
		self.gridlayout.setSpacing(0)
		self.gridlayout.setObjectName("gridlayout")
	
		self.gridlayout1 = QtGui.QGridLayout()
		self.gridlayout1.setMargin(0)
		self.gridlayout1.setSpacing(6)
		self.gridlayout1.setObjectName("gridlayout1")
	
		self.hboxlayout = QtGui.QHBoxLayout()
		self.hboxlayout.setMargin(0)
		self.hboxlayout.setSpacing(6)
		self.hboxlayout.setObjectName("hboxlayout")
	
		self.label = QtGui.QLabel(self.tr("Subscribe request"),self)
		self.label.setObjectName("label")
		self.hboxlayout.addWidget(self.label)
	
		self.label_2 = QtGui.QLabel(self.tr("Od:")+" "+frm,self)
		self.label_2.setObjectName("label_2")
		#self.hboxlayout.addWidget(self.label_2)

		spacerItem = QtGui.QSpacerItem(16,18,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
		self.hboxlayout.addStretch()
		
		self.submitButton = QtGui.QPushButton(self)
		self.submitButton.setMaximumSize(16,16)
		self.submitButton.setFlat(True)
		self.submitButton.setIcon(QtGui.QIcon("images/16x16/actions/ok.png"))
		self.hboxlayout.addWidget(self.submitButton)

		
		self.closeButton = QtGui.QPushButton(self)
		self.closeButton.setMaximumSize(16,16)
		self.closeButton.setObjectName("closeButton")
		self.closeButton.setFlat(True)
		self.closeButton.setIcon(QtGui.QIcon("images/16x16/actions/process-stop.png"))
		self.hboxlayout.addWidget(self.closeButton)

		QtCore.QObject.connect(self.closeButton,QtCore.SIGNAL("clicked()"),self.closeClicked)
		QtCore.QObject.connect(self.submitButton,QtCore.SIGNAL("clicked()"),self.submitClicked)


		self.gridlayout1.addLayout(self.hboxlayout,0,0,1,1)
	
		self.stats = QtGui.QLabel(stats,self)


	
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(1))
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)

		self.gridlayout1.addWidget(self.stats,2,0,1,2)
		self.gridlayout1.addWidget(self.label_2,1,0,1,2)
		self.gridlayout.addLayout(self.gridlayout1,0,0,1,1)
		self.gridlayout.setMargin(1)
		self.gridlayout.setSpacing(0)
		self.gridlayout1.setMargin(1)
		self.gridlayout1.setSpacing(0)
		self.setMinimumHeight(60)

	def closeClicked(self):
		self.main.client.sendPresence(to = self.frm, status = self.status, typ = 'unsubscribed')
		self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.item))
	def submitClicked(self):
		self.main.client.sendPresence(to = self.frm, status = self.status, typ = 'subscribed')
		self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.item))



class FTWidget(QtGui.QWidget):
	def __init__(self,file,item,main,sid,parent=None,stats=""):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.setObjectName("FTWidget")
		self.item=item
		self.main=main
		self.complete=False
		self.sid=sid
		self.gridlayout = QtGui.QGridLayout(self)
		self.gridlayout.setMargin(0)
		self.gridlayout.setSpacing(0)
		self.gridlayout.setObjectName("gridlayout")
	
		self.gridlayout1 = QtGui.QGridLayout()
		self.gridlayout1.setMargin(0)
		self.gridlayout1.setSpacing(6)
		self.gridlayout1.setObjectName("gridlayout1")
	
		self.hboxlayout = QtGui.QHBoxLayout()
		self.hboxlayout.setMargin(0)
		self.hboxlayout.setSpacing(6)
		self.hboxlayout.setObjectName("hboxlayout")
	
		self.label = QtGui.QLabel(self.tr("File transfer:"),self)
		self.label.setObjectName("label")
		self.hboxlayout.addWidget(self.label)
	
		self.label_2 = QtGui.QLabel(file,self)
		self.label_2.setObjectName("label_2")
		self.hboxlayout.addWidget(self.label_2)

		spacerItem = QtGui.QSpacerItem(16,18,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
		self.hboxlayout.addStretch()
		
		self.closeButton = QtGui.QPushButton(self)
		self.closeButton.setMaximumSize(16,16)
		self.closeButton.setObjectName("closeButton")
		self.closeButton.setFlat(True)
		self.closeButton.setIcon(QtGui.QIcon("images/16x16/actions/process-stop.png"))
		self.hboxlayout.addWidget(self.closeButton)

		QtCore.QObject.connect(self.closeButton,QtCore.SIGNAL("clicked()"),self.closeClicked)

		self.gridlayout1.addLayout(self.hboxlayout,0,0,1,1)
	
		self.stats = QtGui.QLabel(stats,self)


		self.progressBar = QtGui.QProgressBar(self)
	
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(1))
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
		self.progressBar.setSizePolicy(sizePolicy)
		self.progressBar.setProperty("value",QtCore.QVariant(0))
		self.progressBar.setOrientation(QtCore.Qt.Horizontal)
		self.progressBar.setObjectName("progressBar")
		self.gridlayout1.addWidget(self.stats,1,0,1,2)
		self.gridlayout1.addWidget(self.progressBar,2,0,1,2)
		self.gridlayout.addLayout(self.gridlayout1,0,0,1,1)
		self.gridlayout.setMargin(1)
		self.gridlayout.setSpacing(0)
		self.gridlayout1.setMargin(1)
		self.gridlayout1.setSpacing(0)
		self.setMinimumHeight(60)

	def reinit(self,file,item,main,sid,parent=None,stats=""):
		self.complete=False
		self.sid=sid
		self.stats.setText(stats)
		self.progressBar.setProperty("value",QtCore.QVariant(24))
		self.setMinimumHeight(60)

	def closeClicked(self):
		if not self.complete:
			self.main.client.ft[self.sid].protocol.unregisterProducer()
			self.complete=None
		elif self.complete==True:
			self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.item))

#documentLayout()->anchorAt(position);
class delegate(QtGui.QItemDelegate):
	def __init__(self,parent=None):
		apply(QtGui.QItemDelegate.__init__,(self,parent))
		
	def paint(self,painter,option, index):
		r=QtCore.QRect(QtCore.QPoint(0, 0), option.rect.size())
		if not index.data(QtCore.Qt.BackgroundRole).isNull():
			painter.save()
			painter.translate(option.rect.topLeft())
			painter.fillRect(r,QtGui.QBrush(QtGui.QColor(index.data(QtCore.Qt.BackgroundRole))))

			painter.restore()


		if option.state & QtGui.QStyle.State_Selected:
			painter.save()
			painter.translate(option.rect.topLeft())
			painter.fillRect(r,option.palette.highlight())

			painter.restore()

		doc=QtGui.QTextDocument()
		doc.setHtml(index.data().toString())

		size=doc.size()
		rectSize=option.rect.size()
		posun=(float(rectSize.height())-float(size.height()))/2


		if not index.data(QtCore.Qt.DecorationRole).isNull():
			icon=QtGui.QIcon(index.data(QtCore.Qt.DecorationRole))
			painter.save()
			painter.translate(option.rect.topLeft())
			if index.column()==3:
				icon.paint(painter,0,0,32,32)
			else:
				icon.paint(painter,0,5,22,22)
			painter.restore()
			rect=option.rect.topLeft()
			rect.setX(rect.x()+24)
			rect.setY(rect.y()+int(posun))
		else:
			rect=option.rect.topLeft()
			rect.setY(rect.y()+int(posun))
		
		painter.save()
		painter.translate(rect)
		doc.drawContents(painter, QtCore.QRectF(QtCore.QRect(QtCore.QPoint(0, 0), rectSize)))

		painter.restore()


	
	def sizeHint(self,option,index):

		doc=QtGui.QTextDocument()
		#doc.setHtml(index.data().toString())
		doc.setHtml("test<br/><font size=\"-1\">test</font>")
		return doc.size().toSize()

		
		#QWidget *Delegate::createEditor(QWidget *parent, const QStyleOptionViewItem &/*option*/, const QModelIndex &/*index*/) const
		#{
		#return new QTextEdit(parent);
		#}
		
		#void Delegate::setEditorData(QWidget *editor, const QModelIndex &index) const
		#{
		#String value=index.data(Qt::DisplayRole).toString();
		#QTextEdit *te=static_cast<QTextEdit*>(editor);
		#te.setHtml(value);
		#}
		
		#def setModelData(editor,model,index):

			#QTextEdit *te=static_cast<QTextEdit*>(editor);
			#model.setData(index, te.toHtml());  
		
		
	def updateEditorGeometry(self,editor,option,index):

		editor.setGeometry(option.rect)



class tooltipWidget(QtGui.QWidget):
	def __init__(self,main,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.setMouseTracking (True)
		self.main=main
		self.ui=Ui_tooltipwidget()
		self.ui.setupUi(self)
		self.ui.gridlayout.setMargin(0)
		self.ui.gridlayout.setSpacing(0)
		self.setWindowFlags(QtCore.Qt.Popup)
		self.setPalette(QtGui.QToolTip.palette())
	def enterEvent(self,event):
		self.hide()

class rosterWidget(QtGui.QTreeWidget):
	def __init__(self,parent,main):
		apply(QtGui.QTreeWidget.__init__,(self,parent))
		self.setObjectName("rosterView")
		self.delegate=delegate()
##		print self.itemDelegate()
##		print self.delegate
		self.setMouseTracking (True)
		self.main=main # mainwindow pointer
		#self.setIndentation(2)
		if self.main.config['rosterMode']=="normal":
			self.setItemDelegate(self.delegate)
			self.setIconSize(QtCore.QSize(32,32))
			self.main.config['rosterIconSize']="32x32"
		elif self.main.config['rosterMode']=="compact":
			size=unicode(self.main.config['rosterIconSize']).rsplit("x")
			self.setIconSize(QtCore.QSize(int(size[0]),int(size[1])))

		#print self.itemDelegate()
		# main variables
		#self.jab=jab # jab instance pointer
		self.edit=0 # temp variable for tabPressed()
		# roster config and design informations
		self.setAlternatingRowColors(True)
		self.setRootIsDecorated(False)
		self.setDragEnabled(True)
		self.setAcceptDrops(True)
		self.setAllColumnsShowFocus(True)
		#self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
		self.header().hide()
		# add and hide columns
		self.headerItem().setText(0,QtGui.QApplication.translate("roster", "Roster", None, QtGui.QApplication.UnicodeUTF8))
		self.headerItem().setText(1,QtGui.QApplication.translate("roster", "id", None, QtGui.QApplication.UnicodeUTF8))
		self.headerItem().setText(2,QtGui.QApplication.translate("roster", "name", None, QtGui.QApplication.UnicodeUTF8))
		self.headerItem().setText(3,QtGui.QApplication.translate("roster", "", None, QtGui.QApplication.UnicodeUTF8))
		self.headerItem().setText(4,QtGui.QApplication.translate("roster", "test", None, QtGui.QApplication.UnicodeUTF8))
		self.hideColumn(1)
		self.hideColumn(2)
		self.hideColumn(4)

		#self.tooltip=tooltipWidget(self.main)
		self.tooltip=None
		self.timer=QtCore.QTimer()
		#QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.tooltip.hide)

		QtCore.QObject.connect(self, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.contactClicked)
		QtCore.QObject.connect(self, QtCore.SIGNAL("itemExpanded ( QTreeWidgetItem * )"),self.expanded)
		QtCore.QObject.connect(self, QtCore.SIGNAL("itemCollapsed ( QTreeWidgetItem * )"),self.collapsed)

		self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

		self.dnd={}
		self.makeHiddenItem()

	def makeHiddenItem(self):
		self.item=QtGui.QTreeWidgetItem(self)
		self.item.setText(1,"999")
		self.setItemHidden(self.item, True)

	def expanded(self,item):
		# change icon if group item expanded
		if item.parent()==None:
			item.setIcon(0,QtGui.QIcon("images/"+self.main.config['rosterIconSize']+"/icons/group-open.png"))

	def collapsed(self,item):
		# change icon if group item collapsed
		if item.parent()==None:
			item.setIcon(0,QtGui.QIcon("images/"+self.main.config['rosterIconSize']+"/icons/group-closed.png"))


	def contactClicked(self,item,column):
		# open chat window for clicked contact
		if self.main.client.roster['groups'].has_key(unicode(item.text(2))):
			return
		it=item.data(32,0)
		it=it.toList()
		data=str(it[0].toString())
		self.main.chat.addChatTab(data,unicode(item.text(2)),self.main.getIcon(data,self.main.icons[unicode(item.text(1))[0]],size="16x16"))


	def addMetaParent(self,tag,parent,offline=False):
		item=QtGui.QTreeWidgetItem(parent)
		item.setText(1,"9")
		# add new resource called 'name', JID 'jid' with QTreeWidgetItem 'user'
		item.setData(32,0,QtCore.QVariant([unicode(tag),unicode("metaparent")]))
		item.setData(32,1,QtCore.QVariant(unicode(tag)))
		if offline!=False:
			self.setItemHidden(item, True)
		self.sortItems(1,QtCore.Qt.AscendingOrder)
		return item

	def addMetaContact(self,jid,name,user,offline=False):
		#item=self.ui.roster.addResource(jid+'/'+resource,unicode(user.text(2))+" - "+resource,user)

		# add new resource called 'name', JID 'jid' with QTreeWidgetItem 'user'
		item=QtGui.QTreeWidgetItem(user)
		if name==None or len(name)==0:
			name=jid
		if self.main.config['rosterMode']=='normal':
			item.setText(0,'<font color="'+unicode(self.main.ui.userStyleWidget.palette().color(QtGui.QPalette.WindowText).name())+'">'+name+"</font>")
		elif self.main.config['rosterMode']=='compact':
			item.setText(0,name)
		item.setText(1,"9"+unicode(name).lower())
		item.setText(2,unicode(name))
		item.setText(4,unicode(jid))
		item.setData(32,0,QtCore.QVariant([unicode(jid),unicode("meta")]))
		if offline!=False:
			self.setItemHidden(item, True)
		self.sortItems(1,QtCore.Qt.AscendingOrder)
		return item


	def addResource(self,jid,name,user):
		#item=self.ui.roster.addResource(jid+'/'+resource,unicode(user.text(2))+" - "+resource,user)

		# add new resource called 'name', JID 'jid' with QTreeWidgetItem 'user'
		item=QtGui.QTreeWidgetItem(user)
		if name==None or len(name)==0:
			name=jid
		item.setText(0,unicode(name))
		item.setText(1,"9"+unicode(name).lower())
		item.setText(2,unicode(name))
		item.setData(32,0,QtCore.QVariant([unicode(jid),unicode("resource")]))
		self.sortItems(1,QtCore.Qt.AscendingOrder)
		return item

	def startDrag(self,actions):
		# start dragging selected contact
		item=self.currentItem()
		it=item.data(32,0)
		it=it.toList()
		data=str(it[0].toString())
		self.drag=QtGui.QDrag(self)
		mimeData=QtCore.QMimeData()
		mimeData.setText(data)
		self.dnd[data]=item
		self.drag.setMimeData(mimeData)
		self.action=self.drag.start(QtCore.Qt.CopyAction)

	def dropMimeData(self,parent, index, data, action ):
		# drop data => change group for dropped contact
		jid=str(data.text())
		oldParent=self.dnd[jid].parent()
		item=self.dnd[jid]
		it=item.data(32,0)
		it=it.toList()
		typ=unicode(it[1].toString())

		it=parent.data(32,0)
		it=it.toList()
		newParent=parent
		newParentJid=unicode(it[0].toString())
		newParentTyp=unicode(it[1].toString())

		if item==newParent:
			return False

		# Pridani kontaktu do klasicke skupiny
		if newParentTyp=="group" and typ=="contact":
			if unicode(oldParent.text(2))=="Unknown":
				self.changeGroup(jid,"+",unicode(newParent.text(2)))
			else:
				items=QtCore.QStringList()
				items.append(self.tr("Copy"))
				items.append(self.tr("Move"))
				q,b=QtGui.QInputDialog.getItem(self,self.tr("Copy/Move contact"),self.tr("Copy or move?"), items,0,False)
				q=unicode(q)
				# if user set new name of group
				if b==True and len(q)!=0:
					index=int(items.indexOf(QtCore.QRegExp(q)))
					if index==0:
						self.changeGroup(jid,"+",unicode(newParent.text(2)))
					else:
						name=unicode(self.main.client.roster['users'][jid].name)
						contact=self.main.client.roster['users'][jid]
						g=contact.groups
						g.remove(unicode(oldParent.text(2)))
						self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription,g+[unicode(newParent.text(2))])
			self.main.ui.roster.sortItems (1,QtCore.Qt.AscendingOrder)
			self.main.ui.roster.refreshStats()
			return True

		# Pridani kontaktu k metakontaktu
		elif newParentTyp=="metaparent" and typ=="contact":
			if item.parent() in self.main.client.metaParents.values():
##				print "not contact"
				return False
			i=self.getUserItems(jid)[0].clone() # clone contact item
			i.setData(32,0,QtCore.QVariant([unicode(jid),unicode("meta")]))
			for contact in self.getUserItems(jid):
				it=contact.data(32,0)
				it=it.toList()
				if unicode(it[1].toString())=="contact":
					par=contact.parent()
					par.takeChild(par.indexOfChild(contact))
			tag=unicode(parent.data(32,1).toString())
			self.main.client.metaParents[tag].addChild(i)
			self.main.client.roster_meta[jid]={'tag':tag,'order':1}
			self.main.client.setMetacontacts()
			self.main.ui.roster.sortItems (1,QtCore.Qt.AscendingOrder)
			self.main.ui.roster.refreshStats()
			return True

		# Vytvoreni noveho metakontaktu sloucenim dvou kontaktu
		elif newParentTyp=="contact" and typ=="contact":
			i=self.getUserItems(jid)[0].clone() # clone contact item
			i.setData(32,0,QtCore.QVariant([unicode(jid),unicode("meta")]))
			i2=self.getUserItems(newParentJid)[0].clone() # clone contact item
			i2.setData(32,0,QtCore.QVariant([unicode(newParentJid),unicode("meta")]))

			self.main.client.metaParents[newParentJid]=self.addMetaParent(newParentJid,newParent.parent())
			self.main.client.metaParents[newParentJid].addChild(i)
			self.main.client.metaParents[newParentJid].addChild(i2)
			self.cloneContact(self.main.client.metaParents[newParentJid],i2)


			for contact in self.getUserItems(jid):
				it=contact.data(32,0)
				it=it.toList()
				if unicode(it[1].toString())=="contact":
					par=contact.parent()
					par.takeChild(par.indexOfChild(contact))

			for contact in self.getUserItems(newParentJid):
				it=contact.data(32,0)
				it=it.toList()
				if unicode(it[1].toString())=="contact":
					par=contact.parent()
					par.takeChild(par.indexOfChild(contact))

			self.main.client.roster_meta[newParentJid]={'tag':newParentJid,'order':1}
			self.main.client.roster_meta[jid]={'tag':newParentJid,'order':1}
			self.main.client.setMetacontacts()
			self.main.ui.roster.sortItems (1,QtCore.Qt.AscendingOrder)
			self.main.ui.roster.refreshStats()
			return True

		# Odebrani kontaktu z metakontaktu a jeho pridani do klasicke skupiny
		elif newParentTyp=="group" and typ=="meta":
			if item.parent() not in self.main.client.metaParents.values():
##				print "not contact"
				return False
			i=self.getUserItems(jid,"meta")[0].clone() # clone contact item
			i.setData(32,0,QtCore.QVariant([unicode(jid),unicode("contact")]))
			
			oldParent.takeChild(oldParent.indexOfChild(item))
	
			newParent.addChild(i)
			contact=self.main.client.roster['users'][jid]
			self.main.client.sendRosterUpdate(contact.jid, contact.name, contact.subscription, [unicode(newParent.text(2))])
			
			del self.main.client.roster_meta[jid]
			tag=self.main.client.roster['users'][jid].tag
			count=0
			toDel=""
			for jid,value in self.main.client.roster_meta.iteritems():
				if value['tag']==tag:
					toDel=jid
					count+=1
			if count==1:
				del self.main.client.roster_meta[toDel]
				jid=toDel
				groups=contact.groups
				# user is not in any group
				if len(groups)==0:
					# add user item to Unknown group
					i=self.getUserItems(jid)[0].clone() # clone contact item
					i.setData(32,0,QtCore.QVariant([unicode(jid),unicode("contact")]))
					self.main.client.roster['groups']['Unknown'].addChild(i)
				else:
					for group in groups:
						# add user item to the group
						i=self.getUserItems(jid)[0].clone() # clone contact item
						i.setData(32,0,QtCore.QVariant([unicode(jid),unicode("contact")]))
						self.main.client.roster['groups'][group].addChild(i)
				oldParent.takeChild(0)
			if int(oldParent.childCount())<=1:
				oldParent.parent().takeChild(oldParent.parent().indexOfChild(oldParent))

##			print self.main.client.roster_meta
			self.main.client.setMetacontacts()
			return True

		
		else:
			return False

	def mimeTypes(self):
		# set mimetypes, which we accept
		return QtCore.QStringList("text/plain")

	def getGroupItem(self,name):
		items=self.findItems(name, QtCore.Qt.MatchFixedString,2)
		if len(items)==1:
			return items[0]
		return None

	def getHostItems(self,host):
		items=self.findItems(unicode(host), QtCore.Qt.MatchContains|QtCore.Qt.MatchRecursive,4)
		if len(items)!=0:
				return items
		return []


	def getUserItems(self,jid,typ=False):
		items=self.findItems(unicode(jid), QtCore.Qt.MatchFixedString|QtCore.Qt.MatchRecursive,4)
		if len(items)!=0:
			if typ:
				new=[]
				for item in items:
					it=item.data(32,0)
					it=it.toList()
					if unicode(it[1].toString())==typ:
						new.append(item)
				return new
			else:
				return items
		return []
		#if not self.main.client.roster['users'].has_key(jid):
			#return []
		#return self.main.client.roster['users'][jid].getUserItems()

	def getResourceItems(self,jid):
		if not self.main.client.roster['users'].has_key(jid):
			return {}
		return self.main.client.roster['users'][jid].resourcesItems

	def getMetaItems(self,jid):
		if not self.main.client.roster['users'].has_key(jid):
			return {}
		return self.main.client.roster['users'][jid].metaItems


	def hidden(self,bool):
		# little hack (qt doesn't repaint reshown items, when we have not one top level item at the end)
		self.setItemHidden(self.item, False)
		self.setItemHidden(self.item, True)
		#self.setItemHidden(self.item, False)
		#self.item.setText(0,"---")


	def refreshStats(self):
		# rewrite online/all users stats in group QTreeWidgetItem
		for group,item in self.main.client.roster['groups'].iteritems():
			# return stats (online,offline,all users) for group
			offline=0
			online=0
			for i in range(int(item.childCount())):
				if int(unicode(item.child(i).text(1))[0])==9:
					offline+=1
				else:
					online+=1
			if online==0:
				if self.main.offline==True:
					self.setItemHidden(self.main.client.roster['groups'][group],False)
				else:
					self.setItemHidden(self.main.client.roster['groups'][group],True)
			else:
				self.setItemHidden(self.main.client.roster['groups'][group],False)
			if self.main.config['rosterMode']=='normal':
				self.main.client.roster['groups'][group].setText(0,"<font color=\""+unicode(self.main.ui.groupStyleWidget.palette().color(QtGui.QPalette.WindowText).name())+"\">"+unicode(self.main.client.roster['groups'][group].text(2))+" ("+str(online)+"/"+str(online+offline)+")</font>")
			elif self.main.config['rosterMode']=='compact':
				self.main.client.roster['groups'][group].setText(0,unicode(self.main.client.roster['groups'][group].text(2))+" ("+str(online)+"/"+str(online+offline)+")")

	def setStatus(self,jid,show,i=None,status=None,first=False):
		if not self.main.shows.has_key(show):
			if len(self.main.client.roster['users'][jid].status)!=0:
				if len(self.main.client.roster['users'][jid].status)>1:
					show=self.main.client.roster['users'][jid].status[0]
				else:
					show=self.main.client.roster['users'][jid].status
			else:
				show="online"
		#print i
		if i!=None:
			item=i
			name=unicode(item.text(0))
			item.setText(1,self.main.shows[unicode(show)]+unicode(name).lower())
			item.setIcon(0,self.main.getIcon(jid,size=self.main.config['rosterIconSize'],status=self.main.icons[self.main.shows[unicode(show)]]))
			if self.main.shows[unicode(show)]!="9":
				self.setItemHidden(item, False)
		else:
			if len(self.main.client.roster['users'][jid].resources)>1:
				resources=" ("+str(len(self.main.client.roster['users'][jid].resources))+") "
			else:
				resources=""
			for item in self.getUserItems(jid):
				name=unicode(item.text(0))
				it=item.data(32,0)
				it=it.toList()
				jid=str(it[0].toString())
				typ=str(it[1].toString())
				set=False
				if typ=='meta':
					if int(self.main.shows[unicode(show)])<int(item.parent().child(0).text(1)[0]):
						set=True
				if status!=None:
							#item.setText(0,+name+"</font>")
					if self.main.config['rosterMode']=='normal':
						item.setText(0,'<font color="'+unicode(self.main.ui.userStyleWidget.palette().color(QtGui.QPalette.WindowText).name())+'">'+unicode(item.text(2))+resources+"<br/><font size=\"-1\"><i>&nbsp;&nbsp;"+status+"</i></font></font>")
					elif self.main.config['rosterMode']=='compact':
						item.setText(0,unicode(item.text(2))+resources)
					item.setData(32,4,QtCore.QVariant(unicode(status)))
				else:
					if self.main.config['rosterMode']=='normal':
						item.setText(0,'<font color="'+unicode(self.main.ui.userStyleWidget.palette().color(QtGui.QPalette.WindowText).name())+'">'+unicode(item.text(2))+resources+"</font>")
					elif self.main.config['rosterMode']=='compact':
						item.setText(0,unicode(item.text(2))+resources)
				item.setText(1,self.main.shows[unicode(show)]+unicode(name).lower())
				item.setIcon(0,self.main.getIcon(jid,size=self.main.config['rosterIconSize'],status=self.main.icons[self.main.shows[unicode(show)]]))
				if set:
					parent=item.parent()
					self.cloneContact(parent,item)
				if self.main.shows[unicode(show)]!="9":
					self.setItemHidden(item, False)
					if typ=='meta':
						self.setItemHidden(item.parent(), False)
				else:
					self.setItemHidden(item, True)

		if not first:
			self.sortItems (1,QtCore.Qt.AscendingOrder)
			self.refreshStats()
		self.hidden(True)

	def cloneContact(self,parent,item):
		it=item.data(32,0)
		it=it.toList()
		jid=str(it[0].toString())
		typ=str(it[1].toString())
		parent.setText(0,item.text(0))
		parent.setText(1,item.text(1))
		parent.setText(2,item.text(2))
		parent.setText(4,item.text(4))
		parent.setIcon(0,item.icon(0))
		parent.setData(32,0,QtCore.QVariant([unicode(jid),unicode("metaparent")]))
		#parent.setData(32,0,item.data(32,0))
		parent.setData(32,4,item.data(32,4))

	def setResourceStatus(self,jid,resource,show):
		if not self.main.shows.has_key(show):
			show="online"
		#for item in self.getResourceItems(jid):
		if self.main.client.roster['users'].has_key(jid):
			if self.main.client.roster['users'][jid].resourcesItems.has_key(resource):
				item=self.main.client.roster['users'][jid].resourcesItems[resource]
				name=unicode(item.text(0))
				item.setText(1,"9"+self.main.shows[unicode(show)]+unicode(name).lower())
				item.setIcon(0,self.main.getIcon(size=str(self.main.config['rosterIconSize']),status=self.main.icons[self.main.shows[unicode(show)]]))
			#if self.main.shows[unicode(show)]!="9":
				#self.setItemHidden(item, False)
		self.sortItems (1,QtCore.Qt.AscendingOrder)
		self.refreshStats()


	def addSubGroup(self,name,sub,first="1"):
		# add new group to the roster and return group QTreeWidgetItem
		item=QtGui.QTreeWidgetItem(sub)
		item.setText(0,"<b>"+name+"</b>")
		item.setText(1,first+unicode(name).lower())
		item.setText(2,name)
		#item.setIcon(0,QtGui.QIcon("images/"+self.main.config['rosterIconSize']+"/icons/group-closed.png"))
		#item.setBackgroundColor(0,QtGui.QColor("#000000"))
		#item.setBackgroundColor(3,QtGui.QColor("#000000"))
		#item.setTextColor(0,QtGui.QColor("#FFFFFF"))
		#item.setTextColor(3,QtGui.QColor("#FFFFFF"))
		return item


	def addGroup(self,name):
		# add new group to the roster and return group QTreeWidgetItem
		item=QtGui.QTreeWidgetItem(self)
		if self.main.config['rosterMode']=='normal':
			item.setText(0,'<font color="'+unicode(self.main.ui.groupStyleWidget.palette().color(QtGui.QPalette.WindowText).name())+'">'+name+"</font>")
		elif self.main.config['rosterMode']=='compact':
			item.setText(0,name)
		item.setText(1,"1"+unicode(name).lower())
		item.setText(2,name)
		item.setData(32,0,QtCore.QVariant([unicode(""),unicode("group")]))
		item.setIcon(0,QtGui.QIcon("images/"+self.main.config['rosterIconSize']+"/icons/group-closed.png"))
		color=self.main.ui.groupStyleWidget.palette().color(QtGui.QPalette.Window)
		item.setBackgroundColor(0,color)
		item.setBackgroundColor(3,color)
		#item.setTextColor(0,QtGui.QColor("#FFFFFF"))
		#item.setTextColor(3,QtGui.QColor("#FFFFFF"))
		return item
	
	def addUser(self,jid,name,group,offline=True,first=False):
		# add new user to the roster and resturn QTreeWidgetItem

		if group==None:
			item=QtGui.QTreeWidgetItem(self)
		else:
			item=QtGui.QTreeWidgetItem(group)
		# if we get no name, we can use jid as name
		if name==None or len(name)==0:
			name=jid
		# item data
		if self.main.config['rosterMode']=='normal':
			item.setText(0,'<font color="'+unicode(self.main.ui.userStyleWidget.palette().color(QtGui.QPalette.WindowText).name())+'">'+name+"</font>")
		elif self.main.config['rosterMode']=='compact':
			item.setText(0,name)
		item.setText(1,"9"+unicode(name).lower())
		item.setText(2,unicode(name))
		item.setText(4,unicode(jid))
		item.setData(32,0,QtCore.QVariant([unicode(jid),unicode("contact")]))
		item.setIcon(0,self.main.getIcon(size=str(self.main.config['rosterIconSize']),status=self.main.icons["9"]))
		item.setFlags(item.flags()|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled)
		color=self.main.ui.userStyleWidget.palette().color(QtGui.QPalette.Window)
		item.setBackgroundColor(0,color)
		item.setBackgroundColor(3,color)
		# item design
		if len(self.main.client.roster['users'][jid].status)!=0:
			if len(self.main.client.roster['users'][jid].status)>1:
				show=self.main.client.roster['users'][jid].status[0]
			else:
				show=self.main.client.roster['users'][jid].status
		else:
			show="offline"
		if unicode(item.text(1))[0]=='9':
			self.setItemHidden(item, offline)
		if not first:
			self.setStatus(jid,show)

			self.sortItems (1,QtCore.Qt.AscendingOrder)
			self.refreshStats()
		return item
		
	def resizeEvent(self,event):
		# when we resize roster, we need to resize columns too, because of avatar.
		QtGui.QTreeWidget.resizeEvent(self,event)
		if self.verticalScrollBar().isVisible():
			self.setColumnWidth(0,int(self.width())-50)
		else:
			self.setColumnWidth(0,int(self.width())-38)
		#self.tooltip.setMaximumWidth(self.width())
		#self.tooltip.setMinimumWidth(self.width())
		
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
		# delete from group
		if group!=None and len(self.main.client.roster['users'][jid].groups)>1:
			action=contactMenu.addAction(self.tr("Delete from group"))
			action.setData(QtCore.QVariant([unicode(jid),u"-"+group.text(2)]))
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
				else:
					action.setData(QtCore.QVariant([unicode(jid),u"+"+unicode(k)]))
		# signal
		contactMenu.connect(contactMenu, QtCore.SIGNAL("triggered ( QAction * )"),self.contactMenuTriggered)
		return contactMenu

	def buildGroupMenu(self,name):
		# build contact menu
		groupMenu=QtGui.QMenu(self)
		# chat
		action=groupMenu.addAction(self.tr("Rename"))
		action.setData(QtCore.QVariant(name))
		action.setObjectName("rename")
		groupMenu.connect(groupMenu, QtCore.SIGNAL("triggered ( QAction * )"),self.groupMenuTriggered)
		return groupMenu

	def groupMenuTriggered(self,action):
		# contact menu action handler
		cmd=action.objectName()
		if cmd=="rename":
			name=action.data()
			name=unicode(name.toString())
			item=self.getGroupItem(name)
			group,b=QtGui.QInputDialog.getText(self,self.tr("Rename group"),self.tr("Enter new group name"), QtGui.QLineEdit.Normal, "")
			group=unicode(group)
			# if user set new name of group
			if b==True and len(group)!=0:
				for i in range(int(item.childCount())):
					child=item.child(i)
					it=child.data(32,0)
					it=it.toList()
					jid=str(it[0].toString())
					#print "move "+jid+" to "+group
					# add new group
					contact=self.main.client.roster['users'][jid]
					for count in range(self.main.client.roster['users'][jid].groups.count(name)):
						self.main.client.roster['users'][jid].groups.remove(name)
					self.main.client.roster['users'][jid].groups.append(group)
					self.main.client.sendRosterUpdate(contact.jid, contact.name, contact.subscription,self.main.client.roster['users'][jid].groups)


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
			user=self.getUserItems(jid)[0]
			self.contactClicked(user,0)
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
				self.main.filetransferQueue.append(file)
				all=len(file)
				file=file[0]
				file=unicode(file)
				#self.jab.sendFile(jid,unicode(file))
				res = self.main.client.roster['users'][jid].getHighestResource()
				sid=self.main.client.sendFile(jid+'/'+res, basename(file), file)
				item=QtGui.QListWidgetItem(self.main.ui.eventsListWidget)
				item.setSizeHint(QtCore.QSize(100,60))
				item.file=file
				item.jid=jid
				item.sent=1
				item.broken=[]
				item.all=all
				item.widget=FTWidget(basename(file),item,self.main,sid,self.main.ui.eventsListWidget)
				self.main.ui.eventsListWidget.setItemWidget(item,item.widget)
				self.main.filetransfer[sid]=item
				self.main.filetransferTimer.start(500)
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
		item=self.itemFromIndex(self.indexAt(QtCore.QPoint(event.x(),event.y())))
		group=item.parent()
		it=item.data(32,0)
		it=it.toList()
		jid=str(it[0].toString())
		if self.main.client.roster['users'].has_key(jid):
			contactMenu=self.buildContactMenu(str(jid),group)
			contactMenu.move(event.globalX(),event.globalY())
			contactMenu.show()
		else:
			contactMenu=self.buildGroupMenu(unicode(item.text(2)))
			contactMenu.move(event.globalX(),event.globalY())
			contactMenu.show()

	#def mouseMoveEvent(self,event):
		#item=self.itemAt(int(event.x()),int(event.y()))
		#if self.tooltip!=item and item!=None and item.parent()!=None:
			
			#if self.tooltip!=None:
				#status=unicode(self.tooltip.data(32,4).toString())
				#if status!="None" and len(status)!=0 and status!=None:
					#status=status.replace("\n"," ").replace("<","&lt;").replace(">","&gt;")
					#self.tooltip.setText(0,unicode(self.tooltip.text(2))+"<br/><font size=\"-1\"><i>&nbsp;&nbsp;"+status+"</i></font>")
				#else:
					#self.tooltip.setText(0,unicode(self.tooltip.text(2)))
			#self.tooltip=item
			#it=item.data(32,0)
			#it=it.toList()
			#jid=str(it[0].toString())
			#contact=self.main.client.roster['users'][jid]
			#text=""
			#if contact.resources.keys()[0]!=None:
				#text+="<br/><b>Resources:</b><br/>"
			#if text!="":
				#for resource in contact.resources.keys():
					#if resource!=None:
						#text+="&nbsp;&nbsp;<a href=\""+resource+"\">"+resource+"</a><br/>"
				#item.setText(0,unicode(item.text(2))+text)
		
		#return QtGui.QTreeWidget.mouseMoveEvent(self,event)


	def viewportEvent(self,event):
		#print event.type()
		#if event.type()==QtCore.QEvent.ToolTip:# and self.tooltip.isHidden():
			#item=self.itemAt(int(event.x()),int(event.y()))
			#if item!=None:
				#if item.parent()!=None:
					#it=item.data(32,0)
					#it=it.toList()
					#jid=str(it[0].toString())
					#typ=str(it[1].toString())
					#if typ=="contact":
						#message=self.main.client.roster['users'][jid].status[1]
						##if os.path.isfile(self.main.homeDir+'/.jabbim/avatars/'+jid):
							##pixmap=QtGui.QPixmap()
							##f=open(self.main.homeDir+'/.jabbim/avatars/'+jid,"rb")
							##image=f.read()
							##f.close()
							##pixmap.loadFromData(image)
							##if pixmap.isNull():
								##self.tooltip.ui.icon.hide()
							##else:
								##self.tooltip.ui.icon.show()
								##self.tooltip.ui.icon.setPixmap(pixmap.scaled(64,64,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
						##else:
						#self.tooltip.ui.icon.hide()
						#self.tooltip.ui.jid.setText(jid)
						#self.tooltip.ui.status.setText(self.main.status[self.main.icons[unicode(item.text(1))[0]]])
						#if message!=None:
							#if len(message)==0:
								#self.tooltip.ui.message.hide()
							#else:
								#self.tooltip.ui.message.show()
								#self.tooltip.ui.message.setText(message.replace("\n","<br/>"))
						#else:
							#self.tooltip.ui.message.hide()
						#self.tooltip.adjustSize()
						#if int(event.y())+20+int(self.tooltip.height())>int(self.height()):
							#self.tooltip.move(self.mapToGlobal(QtCore.QPoint(0,event.y()-10-int(self.tooltip.height()))))
						#else:
							#self.tooltip.move(self.mapToGlobal(QtCore.QPoint(0,event.y()+20)))
						
						#self.tooltip.show()
						#self.timer.start(3000)
		return QtGui.QTreeWidget.viewportEvent(self,event)
