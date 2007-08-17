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
from os.path import basename
from twisted.python import log

class abstractWidget(QtGui.QWidget):
	def __init__(self,header,text,item,main,falseCall=None,falseDict=None,trueCall=None,trueDict=None,action=None,actionDict=None,parent=None,height=40):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.setObjectName("abstractWidget")
		self.item=item
		self.main=main
		self.trueCall=trueCall
		self.trueDict=trueDict
		self.falseCall=falseCall
		self.falseDict=falseDict
		self.action=action
		self.actionDict=actionDict
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
	
		self.label = QtGui.QLabel(header,self)
		self.label.setObjectName("label")
		self.hboxlayout.addWidget(self.label)
	
		self.label_2 = QtGui.QLabel(text,self)
		self.label_2.setTextFormat(QtCore.Qt.RichText)
		self.label_2.setObjectName("label_2")
		#self.hboxlayout.addWidget(self.label_2)

		#spacerItem = QtGui.QSpacerItem(16,18,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
		self.hboxlayout.addStretch()


		self.gridlayout1.addLayout(self.hboxlayout,0,0,1,1)

		self.gridlayout1.addWidget(self.label_2,1,0,1,2)
		self.gridlayout.addLayout(self.gridlayout1,0,0,1,1)
		self.gridlayout.setMargin(1)
		self.gridlayout.setSpacing(0)
		self.gridlayout1.setMargin(1)
		self.gridlayout1.setSpacing(0)
		self.setMinimumHeight(height)

	def closeClicked(self):
		if self.falseCall!=None:
			self.falseCall(*self.falseDict)
		self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.item))
		for event in self.main.events.events:
			if event['widget']==self:
				self.main.events.events.remove(event)
				break
		self.main.events.refreshTray()

	def submitClicked(self):
		if self.trueCall!=None:
			self.trueCall(*self.trueDict)
		self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.item))
		for event in self.main.events.events:
			if event['widget']==self:
				self.main.events.events.remove(event)
				break
		self.main.events.refreshTray()

class lineEditWidget(QtGui.QWidget):
	def __init__(self,header,text,maintext,item,main,icon=None,falseCall=None,falseDict=None,trueCall=None,trueDict=None,action=None,actionDict=None,parent=None,height=40):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.setObjectName("lineEditWidget")
		self.item=item
		self.main=main
		self.trueCall=trueCall
		self.trueDict=trueDict
		self.falseCall=falseCall
		self.falseDict=falseDict
		self.action=action
		self.actionDict=actionDict
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
	
		self.i=QtGui.QLabel(self)
		self.i.setPixmap(icon.pixmap(16,16))
		self.hboxlayout.addWidget(self.i)
	
		self.label = QtGui.QLabel(header,self)
		self.label.setObjectName("label")
		self.hboxlayout.addWidget(self.label)

		self.layout2 = QtGui.QHBoxLayout()
		self.layout2.setMargin(0)
		self.layout2.setSpacing(6)

		self.label_3 = QtGui.QTextEdit(maintext,self)
		self.label_3.setReadOnly(True)
		#self.label_3.setTextFormat(QtCore.Qt.RichText)
		#self.label_3.setWordWrap(True)
		self.label_3.setObjectName("label_3")

		self.label_2 = QtGui.QLabel(text,self)
		self.label_2.setTextFormat(QtCore.Qt.RichText)
		self.label_2.setObjectName("label_2")
		
		self.lineEdit=QtGui.QLineEdit(self)
		self.layout2.addWidget(self.label_2)
		self.layout2.addWidget(self.lineEdit)

		#spacerItem = QtGui.QSpacerItem(16,18,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
		self.hboxlayout.addStretch()


		self.gridlayout1.addLayout(self.hboxlayout,0,0,1,1)
		self.gridlayout1.addWidget(self.label_3,1,0,1,2)

		self.gridlayout1.addLayout(self.layout2,2,0,1,2)
		self.gridlayout.addLayout(self.gridlayout1,0,0,1,1)
		self.gridlayout.setMargin(1)
		self.gridlayout.setSpacing(0)
		self.gridlayout1.setMargin(1)
		self.gridlayout1.setSpacing(0)
		self.setMinimumHeight(height)


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

	def closeClicked(self):
		if self.falseCall!=None:
			self.falseCall(*self.falseDict)
		self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.item))
		for event in self.main.events.events:
			if event['widget']==self:
				self.main.events.events.remove(event)
				break
		self.main.events.refreshTray()

	def submitClicked(self):
		if self.trueCall!=None:
			self.trueCall(*self.trueDict+[unicode(self.lineEdit.text())])
		self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.item))
		for event in self.main.events.events:
			if event['widget']==self:
				self.main.events.events.remove(event)
				break
		self.main.events.refreshTray()

class InfoWidget(abstractWidget):
	def __init__(self,header,text,item,main,falseCall,falseDict,action,actionDict,parent=None):
		apply(abstractWidget.__init__,(self,header,text,item,main,falseCall,falseDict,None,None,action,actionDict,parent))
		self.closeButton = QtGui.QPushButton(self)
		self.closeButton.setMaximumSize(16,16)
		self.closeButton.setObjectName("closeButton")
		self.closeButton.setFlat(True)
		self.closeButton.setIcon(QtGui.QIcon("images/16x16/actions/ok.png"))
		self.hboxlayout.addWidget(self.closeButton)

		QtCore.QObject.connect(self.closeButton,QtCore.SIGNAL("clicked()"),self.closeClicked)
		#self.setMinimumHeight(40)

class BooleanWidget(abstractWidget):
	def __init__(self,header,text,item,main,trueCall,trueDict,falseCall,falseDict,parent=None,height=40):
		apply(abstractWidget.__init__,(self,header,text,item,main,falseCall,falseDict,trueCall,trueDict,parent,40))

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

class fileClass:
	def __init__(self,name,description):
		self.name=name
		self.description=description

class events:
	def __init__(self,main):
		self.main=main
		self.filetransferQueue={}
		self.filetransfer={}
		self.events=[]
		self.trayIcon=None
		self.jabbimIcon=True
		self.timer=QtCore.QTimer()
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.timeout)

	def timeout(self):
		if self.jabbimIcon:
			self.main.tray.setIcon(self.trayIcon)
		else:
			self.main.tray.setIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))
		self.jabbimIcon=not self.jabbimIcon

	def trayClicked(self):
		if len(self.events)!=0:
			widget=self.events[0]['widget']
			if widget.action!=None:
				widget.action(*widget.actionDict)
				return True
		return False

	def refreshTray(self):
		types=[]
		for event in self.events:
			if not event['type'] in types:
				types.append(event['type'])
		if len(types)==0:
			self.timer.stop()
			self.main.tray.setIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))
			self.jabbimIcon=True
		elif len(types)==1:
			self.trayIcon=self.events[0]['icon']
			self.timer.start(500)
		else:
			self.trayIcon=QtGui.QIcon("images/16x16/categories/event.png")
			self.timer.start(500)

	def addEvent(self,name,typ,icon,widget):
		if icon==None:
			icon=QtGui.QIcon("images/16x16/categories/event.png")
		else:
			icon=QtGui.QIcon(unicode(icon))
		self.events.append({'name':name,'type':typ,'icon':icon,'widget':widget})
		self.main.ui.tabWidget.setCurrentIndex(2)
		self.refreshTray()

	def addLineEditEvent(self,trueCall=None,trueDict=None,falseCall=None,falseDict=None,maintext="",header="",text="",name="",typ="",icon=None,action=None,actionDict=None,height=40):
		if icon==None:
			icon2=QtGui.QIcon("images/16x16/categories/event.png")
		else:
			icon2=QtGui.QIcon(unicode(icon))
		item=QtGui.QListWidgetItem(self.main.ui.eventsListWidget)
		item.setSizeHint(QtCore.QSize(100,height))
		item.widget=lineEditWidget(header,text,maintext,item,self.main,icon=icon2,falseCall=falseCall,falseDict=falseDict,trueCall=trueCall,trueDict=trueDict,action=action,actionDict=actionDict,parent=self.main.ui.eventsListWidget,height=height)
		self.main.ui.eventsListWidget.setItemWidget(item,item.widget)
		self.addEvent(unicode(name),unicode(typ),icon,item.widget)


	def addInfoEvent(self,trueCall=None,trueDict=None,header="",text="",name="",typ="",icon=None,action=None,actionDict=None):
		item=QtGui.QListWidgetItem(self.main.ui.eventsListWidget)
		item.setSizeHint(QtCore.QSize(100,40))
		item.widget=InfoWidget(header,text,item,self.main,trueCall,trueDict,action,actionDict,self.main.ui.eventsListWidget)
		self.main.ui.eventsListWidget.setItemWidget(item,item.widget)
		self.addEvent(unicode(name),unicode(typ),icon,item.widget)

	def addBooleanEvent(self,trueCall,trueDict,falseCall,falseDict,header="",text="",height=40,name="",typ="",icon=None):
		item=QtGui.QListWidgetItem(self.main.ui.eventsListWidget)
		item.setSizeHint(QtCore.QSize(100,height))
		item.widget=BooleanWidget(header,text,item,self.main,trueCall,trueDict,falseCall,falseDict,self.main.ui.eventsListWidget,height)
		self.main.ui.eventsListWidget.setItemWidget(item,item.widget)
		self.addEvent(unicode(name),unicode(typ),icon,item.widget)

	def addSubscribeEvent(self,jid,status):
		#	def sendPresence(self, to = None, show = None, status = None, priority = None, typ = None, caps = True):
		self.addBooleanEvent(self.main.client.sendPresence,[jid,None,status,None,'subscribed'],self.main.client.sendPresence,[jid,None,status,None,'unsubscribed'],header=self.main.tr('Subscribe request'),text=self.main.tr('From:')+" "+unicode(jid),name=jid,typ="subscribe")

	def addFTUploadEvent(self,jid,files,descriptions):
		# descriptions['soubor']='popis'
		filesQueue={}
		for name in files:
			filesQueue[name]=fileClass(name,descriptions[name])

		file=files
		fileCount=len(file)
		file=file[0]
		file=unicode(file)

		res = self.main.client.roster['users'][jid].getHighestResource()
		sid=self.main.client.sendFile(jid+'/'+res, basename(file), file,descriptions[file])

		self.filetransferQueue[sid]=filesQueue
		#self.main.filetransferDescriptions[sid]=descriptions
		item=QtGui.QListWidgetItem(self.main.ui.eventsListWidget)
		item.setSizeHint(QtCore.QSize(100,60))
		item.queueId=sid
		item.file=file
		item.jid=jid+'/'+res
		item.sent=1
		item.broken=[]
		item.all=fileCount
		item.widget=FTWidget(basename(file),item,self.main,sid,self.main.ui.eventsListWidget)
		self.main.ui.eventsListWidget.setItemWidget(item,item.widget)
		self.filetransfer[sid]=item
	
	def nextFTUploadEvent(self,sid,queueId):
		jid=self.filetransfer[sid].jid
		file=self.filetransferQueue[queueId][self.filetransferQueue[queueId].keys()[0]].name
		description=self.filetransferQueue[queueId][self.filetransferQueue[queueId].keys()[0]].description

		file=unicode(file)
		sid2=self.main.client.sendFile(jid, basename(file), file, description)
		item=QtGui.QListWidgetItem(self.main.ui.eventsListWidget)
		item.setSizeHint(QtCore.QSize(100,60))
		item.file=file
		item.jid=jid
		item.queueId=queueId
		item.sent=self.filetransfer[sid].sent+1
		#if self.ftError[sid]==None:
			#item.broken=self.filetransfer[sid].broken
		#else:
			#item.broken=self.filetransfer[sid].broken.append(self.filetransfer[sid].file)
		item.all=self.filetransfer[sid].all
		log.msg("SENDING "+str(item.sent)+"/"+str(item.all))
		item.widget=FTWidget(basename(file),item,self.main,sid2,self.main.ui.eventsListWidget,"("+str(item.sent)+"/"+str(item.all)+")")
		self.main.ui.eventsListWidget.setItemWidget(item,item.widget)
		self.filetransfer[sid2]=item
		#self.main.filetransferTimer.start(500)
		if self.main.ftError[sid]==None:
			self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.filetransfer[sid]))


