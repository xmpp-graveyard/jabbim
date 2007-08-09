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

class BooleanWidget(QtGui.QWidget):
	def __init__(self,header,text,item,main,trueCall,trueDict,falseCall,falseDict,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.setObjectName("BooleanWidget")
		self.item=item
		self.main=main
		self.trueCall=trueCall
		self.trueDict=trueDict
		self.falseCall=falseCall
		self.falseDict=falseDict
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
	

	
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(1))
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)

		self.gridlayout1.addWidget(self.label_2,1,0,1,2)
		self.gridlayout.addLayout(self.gridlayout1,0,0,1,1)
		self.gridlayout.setMargin(1)
		self.gridlayout.setSpacing(0)
		self.gridlayout1.setMargin(1)
		self.gridlayout1.setSpacing(0)
		self.setMinimumHeight(60)

	def closeClicked(self):
		self.falseCall(*self.falseDict)
		#self.main.client.sendPresence(to = self.frm, status = self.status, typ = 'unsubscribed')
		self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.item))
	def submitClicked(self):
		self.trueCall(*self.trueDict)
		#self.main.client.sendPresence(to = self.frm, status = self.status, typ = 'subscribed')
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

class fileClass:
	def __init__(self,name,description):
		self.name=name
		self.description=description

class events:
	def __init__(self,main):
		self.main=main
		self.filetransferQueue={}
		self.filetransfer={}

	def addBooleanEvent(self,trueCall,trueDict,falseCall,falseDict,header="",text=""):

		item=QtGui.QListWidgetItem(self.main.ui.eventsListWidget)
		item.setSizeHint(QtCore.QSize(100,40))
		item.widget=BooleanWidget(header,text,item,self.main,trueCall,trueDict,falseCall,falseDict,self.main.ui.eventsListWidget)
		self.main.ui.eventsListWidget.setItemWidget(item,item.widget)

	def addSubscribeEvent(self,jid,status):
		#	def sendPresence(self, to = None, show = None, status = None, priority = None, typ = None, caps = True):
		self.addBooleanEvent(self.main.client.sendPresence,[jid,None,status,None,'subscribed'],self.main.client.sendPresence,[jid,None,status,None,'unsubscribed'],header=self.main.tr('Subscribe request'),text=self.main.tr('From:')+" "+unicode(jid))

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


