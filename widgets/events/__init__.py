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
from os.path import basename
from widgets import vcardeditor
from widgets import chatwidget
from twisted.internet import threads
import base64
import ftwidget
import weakref
from booleanwidget import booleanWidget
from ftwidget import FTDownloadWidget,FTUploadWidget
from adduserwidget import addUserWidget

class abstractEvent:
	def __init__(self,parent):
		self.parent=weakref.proxy(parent)
		self.alive=True
		self.widgets=[]
		self.typ="dummy"
		self.category=None
		self.ID=None

	def setType(self,typ):
		self.typ=unicode(typ)

	def setCategory(self,category):
		self.category=unicode(category)
		if self.ID:
			self.parent.refreshTray()

	def addWidget(self,widget):
		self.widgets.append(weakref.ref(widget))

	def getWidgets(self):
		ret=[]
		for widget in self.widgets:
		    ret.append(widget())
		return ret

	def accept(self):
		if not self.alive:
			return False
		for widget in self.widgets:
			widget().eventAccepted()
		self.alive=False

		return True

	def reject(self):
		if not self.alive:
			return False
		for widget in self.widgets:
			widget().eventRejected()
		self.alive=False
		return True

class booleanEvent(abstractEvent):
	def __init__(self,parent):
		abstractEvent.__init__(self,parent)
		self.acceptHandler=None
		self.acceptDict=[]
		self.rejectHandler=None
		self.rejectDict=[]

	def setAcceptHandler(self,acceptHandler,acceptDict=[]):
		self.acceptHandler=acceptHandler
		self.acceptDict=acceptDict

	def setRejectHandler(self,rejectHandler,rejectDict=[]):
		self.rejectHandler=rejectHandler
		self.rejectDict=rejectDict

	def accept(self):
		if abstractEvent.accept(self):
			if self.acceptHandler:
				self.acceptHandler(*self.acceptDict)
        	self.parent.main.reactor.callLater(0,self.parent.removeEvent,int(self.ID))

	def reject(self):
		if abstractEvent.reject(self):
			if self.rejectHandler:
				self.rejectHandler(*self.rejectDict)
			self.parent.main.reactor.callLater(0,self.parent.removeEvent,int(self.ID))

class FTDownloadEvent(abstractEvent):
	def __init__(self,parent):
		abstractEvent.__init__(self,parent)
		self.SID=None

	def setFileTransfered(self,transfered):
		for widget in self.widgets:
			widget().setFileTransfered(transfered)

	def transferFinished(self):
		for widget in self.widgets:
			widget().transferFinished()

	def setFileSize(self,size):
		for widget in self.widgets:
			widget().setFileSize(size)

	def setCurrentFile(self,file):
		for widget in self.widgets:
			widget().setCurrentFile(file)

	def accept(self):
		if abstractEvent.accept(self):
		 	self.parent.main.reactor.callLater(0,self.parent.removeEvent,int(self.ID))

	def reject(self):
		if abstractEvent.reject(self):
			self.parent.main.reactor.callLater(0,self.parent.removeEvent,int(self.ID))

class FTUploadEvent(abstractEvent):
	def __init__(self,parent):
		abstractEvent.__init__(self,parent)
		self.queue={}
		self.SID=None

	def setQueue(self,queue):
		self.queue=queue
		for widget in self.widgets:
			widget().setQueue(queue)

	def setCurrentFile(self,file):
		for widget in self.widgets:
			widget().setCurrentFile(file)

	def setFileSize(self,size):
		for widget in self.widgets:
			widget().setFileSize(size)

	def setFileTransfered(self,transfered):
		for widget in self.widgets:
			widget().setFileTransfered(transfered)

	def transferFinished(self):
		for widget in self.widgets:
			widget().transferFinished()

	def accept(self):
		if abstractEvent.accept(self):
		 	self.parent.main.reactor.callLater(0,self.parent.removeEvent,int(self.ID))

	def reject(self):
		if abstractEvent.reject(self):
			self.parent.main.reactor.callLater(0,self.parent.removeEvent,int(self.ID))


class abstractWidget(QtGui.QWidget):
	def __init__(self,header,text,item,main,falseCall=None,falseDict=None,trueCall=None,trueDict=None,action=None,actionDict=None,parent=None,height=40):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.setObjectName("abstractWidget")
		self.eventClass=event(self,trueCall,trueDict,falseCall,falseDict)
		self.item=item
		self.main=main
		#self.trueCall=trueCall
		#self.trueDict=trueDict
		#self.falseCall=falseCall
		#self.falseDict=falseDict
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

		self.hwidget=QtGui.QWidget(self)
		self.hwidget.palette().setColor(QtGui.QPalette.Base,parent.palette().color(QtGui.QPalette.AlternateBase))
		self.hwidget.setAutoFillBackground(True)

		self.hboxlayout = QtGui.QHBoxLayout(self.hwidget)
		self.hboxlayout.setMargin(0)
		self.hboxlayout.setSpacing(6)
		self.hboxlayout.setObjectName("hboxlayout")

		self.label = QtGui.QLabel(header,self)
		self.label.setObjectName("label")
		#self.label.setAutoFillBackground(False)
		self.label.setAutoFillBackground(False)
		self.hboxlayout.addWidget(self.label)

		self.label_2 = QtGui.QLabel(text,self)
		self.label_2.setTextFormat(QtCore.Qt.RichText)
		self.label_2.setWordWrap(True)
		self.label_2.setObjectName("label_2")
		self.label_2.setAutoFillBackground(False)
		#self.hboxlayout.addWidget(self.label_2)

		#spacerItem = QtGui.QSpacerItem(16,18,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
		self.hboxlayout.addStretch()


		self.gridlayout1.addWidget(self.hwidget,0,0,1,1)

		self.gridlayout1.addWidget(self.label_2,1,0,1,2)
		self.gridlayout.addLayout(self.gridlayout1,0,0,1,1)
		self.gridlayout.setMargin(1)
		self.gridlayout.setSpacing(0)
		self.gridlayout1.setMargin(1)
		self.gridlayout1.setSpacing(0)
		self.setMinimumHeight(height)

	def closeClicked(self):
		for item in self.main.ui.eventsListWidget.selectedItems():
			if hasattr(item.widget,"eventClass"):
				item.widget.eventClass.reject()
				self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(item))

		self.eventClass.reject()
		self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.item))
		for event in self.main.events.events:
			if event['widget']==self:
				for eventClass in event['childs']:
					eventClass.reject()
				self.main.events.events.remove(event)
				break
		self.main.events.refreshTray()

	def submitClicked(self):
		for item in self.main.ui.eventsListWidget.selectedItems():
			if hasattr(item.widget,"eventClass"):
				item.widget.eventClass.accept()
				self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(item))
		self.eventClass.accept()
		#if self.trueCall!=None:
			#self.trueCall(*self.trueDict)
			#self.trueCall=None
		self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.item))
		for event in self.main.events.events:
			if event['widget']==self:
				for eventClass in event['childs']:
					eventClass.accept()
				self.main.events.events.remove(event)
				break
		self.main.events.refreshTray()

class lineEditWidget(QtGui.QWidget):
	def __init__(self,header,text,maintext,item,main,icon=None,falseCall=None,falseDict=None,trueCall=None,trueDict=None,action=None,actionDict=None,parent=None,height=40,value=u"",falseText=None,trueText=None):
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

		self.hwidget=QtGui.QWidget(self)

		self.hwidget.palette().setColor(QtGui.QPalette.Base,parent.palette().color(QtGui.QPalette.AlternateBase))
		self.hwidget.setAutoFillBackground(True)

		self.hboxlayout = QtGui.QHBoxLayout(self.hwidget)
		self.hboxlayout.setMargin(0)
		self.hboxlayout.setSpacing(6)
		self.hboxlayout.setObjectName("hboxlayout")

		self.i=QtGui.QLabel(self)
		self.i.setPixmap(icon.pixmap(16,16))
		#self.i.palette().setColor(QtGui.QPalette.Base,QtGui.QColor(128,128,128))
		#self.i.setAutoFillBackground(True)
		self.hboxlayout.addWidget(self.i)

		self.label = QtGui.QLabel(header,self)
		self.label.setObjectName("label")
		#self.label.palette().setColor(QtGui.QPalette.Base,QtGui.QColor(128,128,128))
		#self.label.setAutoFillBackground(True)
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
		self.lineEdit.setText(value)
		QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL("returnPressed()"), self.submitClicked)
	#	self.lineEdit.setFocus(QtCore.Qt.MouseFocusReason)

		self.layout2.addWidget(self.label_2)
		self.layout2.addWidget(self.lineEdit)

		#spacerItem = QtGui.QSpacerItem(16,18,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
		self.hboxlayout.addStretch()

		connect=QtGui.QPushButton(unicode(trueText))
		decline=QtGui.QPushButton(unicode(falseText))

		self.gridlayout1.addWidget(self.hwidget,0,0,1,2)
		self.gridlayout1.addWidget(self.label_3,2,0,1,2)

		self.gridlayout1.addWidget(connect,3,0,1,1)
		self.gridlayout1.addWidget(decline,3,1,1,1)

		self.gridlayout1.addLayout(self.layout2,1,0,1,2)
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
		#self.submitButton.palette().setColor(QtGui.QPalette.Button,QtGui.QColor(128,128,128))
		#self.submitButton.setAutoFillBackground(True)
		self.hboxlayout.addWidget(self.submitButton)

		self.closeButton = QtGui.QPushButton(self)
		self.closeButton.setMaximumSize(16,16)
		self.closeButton.setObjectName("closeButton")
		self.closeButton.setFlat(True)
		self.closeButton.setIcon(QtGui.QIcon("images/16x16/actions/process-stop.png"))
		#self.closeButton.palette().setColor(QtGui.QPalette.Button,QtGui.QColor(128,128,128))
		#self.closeButton.setAutoFillBackground(True)

		self.hboxlayout.addWidget(self.closeButton)

		QtCore.QObject.connect(self.closeButton,QtCore.SIGNAL("clicked()"),self.closeClicked)
		QtCore.QObject.connect(self.submitButton,QtCore.SIGNAL("clicked()"),self.submitClicked)

		QtCore.QObject.connect(decline,QtCore.SIGNAL("clicked()"),self.closeClicked)
		QtCore.QObject.connect(connect,QtCore.SIGNAL("clicked()"),self.submitClicked)

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
		apply(abstractWidget.__init__,(self,header,text,item,main,falseCall,falseDict,action,actionDict,action,actionDict,parent))
		self.closeButton = QtGui.QPushButton(self)
		self.closeButton.setMaximumSize(16,16)
		self.closeButton.setObjectName("closeButton")
		self.closeButton.setFlat(True)
		self.closeButton.setIcon(QtGui.QIcon("images/16x16/actions/process-stop.png"))
		self.hboxlayout.addWidget(self.closeButton)
		QtCore.QObject.connect(self.closeButton,QtCore.SIGNAL("clicked()"),self.closeClicked)
		#self.setMinimumHeight(40)

##class BooleanWidget(abstractWidget):
##	def __init__(self,header,text,item,main,trueCall,trueDict,falseCall,falseDict,parent=None,height=40,pixmap=None):
##		apply(abstractWidget.__init__,(self,header,text,item,main,falseCall,falseDict,trueCall,trueDict,None,None,parent,40))
##
##		self.submitButton = QtGui.QPushButton(self)
##		self.submitButton.setMaximumSize(16,16)
##		self.submitButton.setFlat(True)
##		self.submitButton.setIcon(QtGui.QIcon("images/16x16/actions/ok.png"))
##		self.hboxlayout.addWidget(self.submitButton)
##
##		self.closeButton = QtGui.QPushButton(self)
##		self.closeButton.setMaximumSize(16,16)
##		self.closeButton.setObjectName("closeButton")
##		self.closeButton.setFlat(True)
##		self.closeButton.setIcon(QtGui.QIcon("images/16x16/actions/process-stop.png"))
##		self.hboxlayout.addWidget(self.closeButton)
##
##		QtCore.QObject.connect(self.closeButton,QtCore.SIGNAL("clicked()"),self.closeClicked)
##		QtCore.QObject.connect(self.submitButton,QtCore.SIGNAL("clicked()"),self.submitClicked)
##
##		if pixmap:
##			label=QtGui.QLabel()
##			label.setPixmap(pixmap)
##			label.setAlignment(QtCore.Qt.AlignCenter)
##			self.gridlayout.addWidget(label,1,0,1,1)

##class AddUserWidget(abstractWidget):
##	def __init__(self,header,text,item,main,trueCall,trueDict,falseCall,falseDict,parent=None,height=40):
##		apply(abstractWidget.__init__,(self,header,text,item,main,falseCall,falseDict,trueCall,trueDict,None,None,parent,40))
##
##		self.submitButton = QtGui.QPushButton(self)
##		self.submitButton.setMaximumSize(16,16)
##		self.submitButton.setFlat(True)
##		self.submitButton.setIcon(QtGui.QIcon("images/16x16/actions/ok.png"))
##		self.hboxlayout.addWidget(self.submitButton)
##		#self.label_2.setWordWrap(False)
##		self.closeButton = QtGui.QPushButton(self)
##		self.closeButton.setMaximumSize(16,16)
##		self.closeButton.setObjectName("closeButton")
##		self.closeButton.setFlat(True)
##		self.closeButton.setIcon(QtGui.QIcon("images/16x16/actions/process-stop.png"))
##		self.hboxlayout.addWidget(self.closeButton)
##
##		self.vcard=QtGui.QPushButton(self.tr("Vcard"))
##		self.chat=QtGui.QPushButton(self.tr("Chat"))
##
##		QtCore.QObject.connect(self.closeButton,QtCore.SIGNAL("clicked()"),self.closeClicked)
##		QtCore.QObject.connect(self.submitButton,QtCore.SIGNAL("clicked()"),self.submitClicked)
##		QtCore.QObject.connect(self.vcard,QtCore.SIGNAL("clicked()"),self.vcardClicked)
##		QtCore.QObject.connect(self.chat,QtCore.SIGNAL("clicked()"),self.chatClicked)
##
##		l=QtGui.QHBoxLayout()
##		l.addWidget(self.vcard)
##		l.addWidget(self.chat)
##		self.gridlayout1.addLayout(l,2,0)
##
##	def vcardClicked(self,b=False):
##		self.ve=vcardeditor.vcardEditorDialog(self.main,self.jid,self.main,False)
##		self.ve.show()
##
##	def chatClicked(self,b=False):
##		self.main.chat.addChatTab(self.jid,self.jid,self.main.getIcon(self.jid,'online',size="16x16"))
##		self.main.chat.activate()


class FTWidget(QtGui.QWidget):
	def __init__(self,file,item,main,sid,parent=None,stats="",download=False):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.setObjectName("FTWidget")
		self.item=item
		self.main=main
		self.complete=False
		self.queueId=sid
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
		self.label_2.setTextFormat(QtCore.Qt.RichText)
		self.label_2.setWordWrap(True)
		if download:
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
		if not download:
			self.gridlayout1.addWidget(self.label_2,3,0,1,2)
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
		self.item=item
		self.progressBar.setProperty("value",QtCore.QVariant(0))
		self.label_2.setText(file)

		self.setMinimumHeight(60)

	def closeClicked(self):
		if self.item:
			tab,index=self.main.chat.findTab(self.main.events.filetransferWidget[self.queueId].jid,typ=['chat'])
			print 'trying to close FTWidget',self.complete
			if self.complete==False:
				if self.main.events.filetransferQueue.has_key(self.queueId):
					self.main.events.filetransferQueue[self.queueId]=[]
				if self.main.client.ft.has_key(self.sid):
					print 'stopping filetransfer sid =',self.sid
					if self.main.client.ft[self.sid]:
						self.main.client.ft[self.sid].delete()
					self.complete=None
					return
			else:
				self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.item))
			#else:
				#self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.item))
			if tab:
				if tab.chat.filetransfer.has_key(self.queueId):
					tab.chat.ui.ftwidget.layout().removeWidget(tab.chat.filetransfer[self.queueId])
					tab.chat.filetransfer[self.queueId].setParent(None)
					del tab.chat.filetransfer[self.queueId]

class fileClass:
	def __init__(self,name,description):
		self.name=name
		self.description=description

class events:
	def __init__(self,main):
		self.main=main
		self.filetransferQueue={}
		self.filetransferWidget={}
		self.filetransfer={}
		#self.events=[]
		self.events={}
		self.trayIcon=None
		self.jabbimIcon=None
		self.timer=QtCore.QTimer()
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.timeout)
		#QtCore.QObject.connect(self.main.ui.eventsListWidget, QtCore.SIGNAL("itemDoubleClicked ( QListWidgetItem * )"),self.itemClicked)
		#self.main.ui.eventsListWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		self.ID=0
		self.blankIcon=QtGui.QPixmap(16,16)
		self.blankIcon.fill(QtCore.Qt.transparent)

		self.messagesLayout=QtGui.QVBoxLayout(self.main.ui.messages)
		self.messagesLayout.setContentsMargins(2,2,2,2)
		self.filetransfersLayout=QtGui.QVBoxLayout(self.main.ui.fileTransfers)
		self.filetransfersLayout.setContentsMargins(2,2,2,2)
		self.authorizationsLayout=QtGui.QVBoxLayout(self.main.ui.authorizations)
		self.authorizationsLayout.setContentsMargins(2,2,2,2)

		self.main.ui.authorizations.hide()
		self.main.ui.fileTransfers.hide()
		self.main.ui.messages.hide()

		colors=QtGui.QTreeWidget()
		self.main.ui.scrollAreaWidgetContents.palette().setColor(QtGui.QPalette.Window,QtGui.QColor(colors.palette().color(QtGui.QPalette.Base)))
		colors.deleteLater()
		del colors
		self.ftEvents={}



	def itemClicked(self,item):
		widget=item.widget
		if widget.action!=None:
			widget.action(*widget.actionDict)
		widget.submitClicked()

	def timeout(self):
		if self.jabbimIcon:
			self.main.tray.setIcon(self.trayIcon)
			self.main.ui.tabWidget.setTabIcon(2,self.trayIcon)
		else:
			self.main.tray.setIcon(self.main.getCurrentTrayIcon())
			self.main.ui.tabWidget.setTabIcon(2,QtGui.QIcon(self.blankIcon))
		self.jabbimIcon=not self.jabbimIcon

	def trayClicked(self):
		if len(self.events)!=0:
			for event in self.events.values():
				if event.category!="messages":
					return False
			self.events[self.events.keys()[0]].accept()
		return False

	def refreshTray(self):
		types=[]
		mainWindow=self.main
		if len(self.events)==0:
			if self.main.selfStatus!="":
				data=self.main.selfStatus
				mainWindow.tray.setToolTip(unicode(mainWindow.tr('Your status:'))+" "+unicode(self.main.status[data]))
			else:
				mainWindow.tray.setToolTip('')
		categories=[]
		for event in self.events.values():
			if not event.category in categories:
				categories.append(event.category)
		if len(categories)==0:
			self.timer.stop()
			if self.jabbimIcon!=None:
				mainWindow.tray.setIcon(self.main.getCurrentTrayIcon())
				self.main.ui.tabWidget.setTabIcon(2,QtGui.QIcon("images/16x16/categories/event.png"))
				if self.main.ui.tabWidget.currentIndex()==2:
					self.main.ui.tabWidget.setCurrentIndex(0)
				self.jabbimIcon=None
		elif categories==["messages"]:
			self.trayIcon=QtGui.QIcon("images/16x16/actions/message.png")
			self.timer.start(1000)
		else:
			self.trayIcon=QtGui.QIcon("images/16x16/categories/event.png")
			self.timer.start(1000)
#		if not 'message' in types and not 'newMessage' in types:
	#		self.main.chat.flashStatus=False
		#self.main.ui.roster.refreshEvents()

	def getEvents(self,name,typ):
		ret=[]
		for event in self.events:
			if event['type']==typ and event['name']==name:
				ret.append(event)
		return ret

	def getEventByID(self,ID):
		for event in self.events:
			if event['ID']==ID:
				return event
		return None

	def addChildEvent(self,parentID,eventClass):
		print 'addChildEvent',parentID
		parent=self.getEventByID(parentID)
		if parent:
			eventClass.parent=parent['widget']
			parent['childs'].append(eventClass)
			print 'added',parentID

	def addEvent(self,event=None):
		if not event:
			self.events[self.ID]=abstractEvent(self)
		else:
			self.events[self.ID]=event
		self.events[self.ID].ID=self.ID
		self.ID+=1
		if self.events[self.ID-1].category:
			self.refreshTray()
		return self.events[self.ID-1]

	def removeEvent(self,ID):
		if not self.events.has_key(ID):
			return
		widget=self.events[ID].widgets[0]()
		category=self.events[ID].category
		if category=="messages":
			self.messagesLayout.removeWidget(widget)
			widget.setParent(None)
			widget.deleteLater()
			del widget
			if self.messagesLayout.count()==0:
				self.main.ui.messages.hide()
		elif category=="filetransfers":
			self.filetransfersLayout.removeWidget(widget)
			widget.setParent(None)
			widget.deleteLater()
			del widget
			if self.filetransfersLayout.count()==0:
				self.main.ui.fileTransfers.hide()
		elif category=="authorizations":
			self.authorizationsLayout.removeWidget(widget)
			widget.setParent(None)
			widget.deleteLater()
			del widget
			if self.authorizationsLayout.count()==0:
				self.main.ui.authorizations.hide()
		if hasattr(self.events[ID],"SID"):
			if self.ftEvents.has_key(self.events[ID].SID):
				del self.ftEvents[self.events[ID].SID]
		del self.events[ID].widgets
		del self.events[ID]
		self.refreshTray()

	def removeAll(self):
		for i in range(len(self.events.keys())):
			self.removeEvent(self.events.keys()[0])

	def addWidget(self,widget,group="messages"):
		if group=="messages":
			widget.setParent(self.main.ui.messages)
			self.messagesLayout.addWidget(widget)
			self.main.ui.messages.show()
			return widget
		elif group=='filetransfers':
			widget.setParent(self.main.ui.fileTransfers)
			self.filetransfersLayout.addWidget(widget)
			self.main.ui.fileTransfers.show()
			return widget
		elif group=="authorizations":
			widget.setParent(self.main.ui.authorizations)
			self.authorizationsLayout.addWidget(widget)
			self.main.ui.authorizations.show()
			return widget

##		if icon==None:
##			iconName=""
##			icon=QtGui.QIcon("images/16x16/categories/event.png")
##		else:
##			iconName=unicode(icon)
##			icon=QtGui.QIcon(unicode(icon).replace("xxxxx","16x16"))
##		self.events.append({'ID':self.ID,'name':name,'type':typ,'icon':icon,'iconName':iconName,'widget':widget,'tooltip':tooltip,'childs':[]})
##		if typ!="message":
##			self.main.ui.tabWidget.setCurrentIndex(2)
##		#self.main.ui.roster.refreshEvents()
##		self.refreshTray()
##		self.ID+=1
##		return self.ID-1

	def addLineEditEvent(self,trueCall=None,trueDict=None,falseCall=None,falseDict=None,maintext="",header="",text="",name="",typ="",icon=None,action=None,actionDict=None,height=40,value=u"",trueText=None,falseText=None):
		if icon==None:
			icon2=QtGui.QIcon("images/16x16/categories/event.png")
		else:
			icon2=QtGui.QIcon(unicode(icon).replace("xxxxx","16x16"))
		item=QtGui.QListWidgetItem(self.main.ui.eventsListWidget)
		item.setSizeHint(QtCore.QSize(100,height))
		item.widget=lineEditWidget(header,text,maintext,item,self.main,icon=icon2,falseCall=falseCall,falseDict=falseDict,trueCall=trueCall,trueDict=trueDict,action=action,actionDict=actionDict,parent=self.main.ui.eventsListWidget,height=height,value=value,trueText=trueText,falseText=falseText)
		self.main.ui.eventsListWidget.setItemWidget(item,item.widget)
		self.addEvent(unicode(name),unicode(typ),icon,item.widget)


	def addBooleanEvent(self,typ="message",category="messages"):
		event=booleanEvent(self)
		event.setType(typ)
		event.setCategory(category)
		widget=booleanWidget(event)
		widget=self.addWidget(widget,category)
		event.addWidget(widget)
		return self.addEvent(event)
		#return event

	def addFTReceivedEvent(self,sid,id,jid,pixmap):
		text=unicode(" %s is sending you file."%unicode(jid))
		metrics=QtGui.QApplication.fontMetrics()
		rect=metrics.boundingRect(0, 0,self.main.width(), self.main.height(), QtCore.Qt.TextWordWrap, text)
		if pixmap:
			height=metrics.height()+rect.height()+metrics.height()+pixmap.height()
		else:
			height=metrics.height()+rect.height()+metrics.height()
		return self.addBooleanEvent(self.main.client.ftStarted,[sid,id],self.main.client._declineFT,[sid,  id],self.main.tr("File transfer"),text=text,height=height,name=unicode(jid),typ="ftTransfer",icon=None,pixmap=pixmap)

	def addAddUserEvent(self,jid,status):
		"""
		Adds 'Add User' Event.
		@type jid: unicode
		@param jid: Jabber ID of sender
		@type status: unicode
		@param status: senders status message
		"""
		event=booleanEvent(self)
		event.setType("addUser")
		event.setCategory("authorizations")
		widget=addUserWidget(event)
		widget.setData(jid,status)
		widget=self.addWidget(widget,"authorizations")
		event.addWidget(widget)
		event.setAcceptHandler(self.main.client._onSubscribe,[jid,'online',False])
		event.setRejectHandler(self.main.client.sendPresence,[jid,None,'online',None,'unsubscribed'])
		return self.addEvent(event)

	def addSubscribeEvent(self,jid,status):
		#	def sendPresence(self, to = None, show = None, status = None, priority = None, typ = None, caps = True):
		mainWindow=self.main
		self.addBooleanEvent(self.main.client.sendPresence,[jid,None,status,None,'subscribed'],self.main.client.sendPresence,[jid,None,status,None,'unsubscribed'],header=unicode(mainWindow.tr('Subscribe request')),text=unicode(mainWindow.tr('From:'))+" "+unicode(jid),name=jid,typ="subscribe")

	def isImage(self,file):
		if unicode(file).lower().endswith('.jpg'):
			return 'image/jpeg'
		if unicode(file).lower().endswith('.png'):
			return 'image/png'
		if unicode(file).lower().endswith('.gif'):
			return 'image/gif'
		if unicode(file).lower().endswith('.jpeg'):
			return 'image/jpeg'
		if unicode(file).lower().endswith('.bmp'):
			return 'image/bmp'
		if unicode(file).lower().endswith('.tiff'):
			return 'image/tiff'
		return False

	def makeFTPreview(self,file):
		img=QtGui.QImage(file)
		image=img.scaled(128,128,QtCore.Qt.KeepAspectRatio)#,QtCore.Qt.SmoothTransformation)
		return image

	def addFTUploadEvent(self,jid,files,descriptions):
		print "addFTUploadEvent"
		typ=self.isImage(files[0])
		j=self.main.getJid(jid)
		feature=False
		if self.main.client.roster['users'].has_key(j.userhost()):
			#print self.main.client.roster['users'][j.userhost()].resources,j.resource
			if self.main.client.roster['users'][j.userhost()].resources.has_key(j.resource):
				#print 'blabla',self.main.client.roster['users'][j.userhost()].resources[j.resource].features
				feature=self.main.client.roster['users'][j.userhost()].resources[j.resource].hasFeature('http://kopete.kde.org/protocol/file-preview')
		print 'feature',feature
		if typ!=False and feature:
			print 'generating file preview'
			d=threads.deferToThread(self.makeFTPreview,files[0])
			d.addCallback(self._addFTUploadEvent,jid,files,descriptions,'image/png')
		else:
			print "starting ft upload"
			self._addFTUploadEvent(None,jid,files,descriptions,None)

	def _addFTUploadEvent(self,preview,jid,files,descriptions,previewType=None):
		#print jid,previewType,preview
		print "_addFTUploadEvent"
		if preview:
			bytes=QtCore.QByteArray()
			buf=QtCore.QBuffer(bytes)
			buf.open(QtCore.QIODevice.WriteOnly)
			preview.save(buf, "PNG")
			preview=base64.encodestring(str(bytes))
		filesQueue={}
		text=""
		for name in files:
			if files.index(name)!=0:
				filesQueue[name]=fileClass(name,descriptions[name])
			#	text+="<b>"+basename(name)+'</b><br/>'
			#else:
			#	text+="<font size=\"-1\">"+basename(name)+"</font><br/>"
		# get event height (based on font size)
		#metrics=QtGui.QApplication.fontMetrics()
		#rect=metrics.boundingRect(0, 0,self.main.width(), self.main.height(), QtCore.Qt.TextWordWrap, text)
		#height=metrics.height()+rect.height()+metrics.height()+10

		if jid.find("/") == -1:
			res = self.main.client.roster['users'][jid].getHighestResource()
		else:
			jid, res = jid.split("/", 1)

		event=FTUploadEvent(self)
		event.setType("ftUpload")
		event.setCategory("filetransfers")
		event.setQueue(filesQueue)
		event.jid=jid+"/"+res
		widget=FTUploadWidget(event)
		widget=self.addWidget(widget,"filetransfers")
		event.addWidget(widget)


		file=files
		fileCount=len(file)
		file=file[0]
		file=unicode(file)

		event.setCurrentFile(file)

		if res==None:
			sid=self.main.client.sendFile(jid, basename(file), file,descriptions[file],preview=preview,previewType='image/png')
			tab,index=self.main.chat.findTab(jid,typ=['chat'])
		else:
			sid=self.main.client.sendFile(jid+'/'+res, basename(file), file,descriptions[file],preview=preview,previewType='image/png')
			tab,index=self.main.chat.findTab(jid+'/'+res,typ=['chat'])
		event.SID=sid
		event.setFileSize(int(self.main.client.ft[sid].size))
		self.ftEvents[sid]=event
		self.addEvent(event)
		mainWindow=self.main
		mainWindow.tray.showMessage(unicode(mainWindow.tr("Sending file "))+basename(file)+mainWindow.tr(" to ")+unicode(jid), mainWindow.tr("You can see progress of sending in Events tab in main window."), QtGui.QSystemTrayIcon.Information, 4000)

		if tab:
			#tab.chat.filetransfer[sid]=chatwidget.FTWidget(text,None,self.main,sid,tab.chat.ui.ftwidget)
			#tab.chat.ui.ftwidget.layout().addWidget(tab.chat.filetransfer[sid])
			tab.chat.textEditWrite(self.main.webkitThemeFactory.genChatStatus(unicode(mainWindow.tr("Sending file"))+" "+basename(file),self.main.now()))
			tab.chat.lastMessageFrom=""
##		self.filetransferQueue[sid]=filesQueue
##		#self.main.filetransferDescriptions[sid]=descriptions
##		self.filetransferWidget[sid]=QtGui.QListWidgetItem(self.main.ui.eventsListWidget)
##		self.filetransferWidget[sid].setSizeHint(QtCore.QSize(100,height))
##		self.filetransferWidget[sid].queueId=sid
##		self.filetransferWidget[sid].file=file
##		self.filetransferWidget[sid].jid=jid+'/'+res
##		self.filetransferWidget[sid].sent=1
##		self.filetransferWidget[sid].broken=[]
##		self.filetransferWidget[sid].errors=[]
##		self.filetransferWidget[sid].all=fileCount
##		self.filetransferWidget[sid].download=False
##		self.filetransferWidget[sid].typ='normal'
##		self.filetransferWidget[sid].widget=FTWidget(text,self.filetransferWidget[sid],self.main,sid,self.main.ui.eventsListWidget)
##		self.filetransferWidget[sid].widget.setMinimumHeight(height)
##		if tab:
##			QtCore.QObject.connect(self.filetransferWidget[sid].widget.progressBar,QtCore.SIGNAL("valueChanged(int)"),tab.chat.filetransfer[sid].progressBar.setValue)
##		self.main.ui.eventsListWidget.setItemWidget(self.filetransferWidget[sid],self.filetransferWidget[sid].widget)
		#self.filetransfer[sid]=self.filetransferWidget[sid]
##		self.filetransfer[sid]={'queueId':sid}

	def addFTDownloadEvent(self,jid,file,description,sid,size):
		# descriptions['soubor']='popis'
		file=unicode(file)
		#text="<b>"+basename(unicode(file))+'</b>'

		event=FTDownloadEvent(self)
		event.setType("ftDonwload")
		event.setCategory("filetransfers")
		widget=FTDownloadWidget(event)
		widget=self.addWidget(widget,"filetransfers")
		event.addWidget(widget)
		event.setCurrentFile(file)
		event.setFileSize(int(size))
		event.SID=sid
		# get event height (based on font size)
##		metrics=QtGui.QApplication.fontMetrics()
##		rect=metrics.boundingRect(0, 0,self.main.width(), self.main.height(), QtCore.Qt.TextWordWrap, text)
##		height=metrics.height()+rect.height()+metrics.height()+10
		tab,index=self.main.chat.findTab(unicode(jid),typ=['chat'])
		mainWindow=self.main
		if tab:
##			tab.chat.filetransfer[sid]=chatwidget.FTWidget(text,None,self.main,sid,tab.chat.ui.ftwidget)
##			tab.chat.ui.ftwidget.layout().addWidget(tab.chat.filetransfer[sid])
			tab.chat.textEditWrite(self.main.webkitThemeFactory.genChatStatus(unicode(mainWindow.tr("Receiving file"))+" "+unicode(basename(file)),self.main.now()))
			tab.chat.lastMessageFrom=""

		self.ftEvents[sid]=event
		self.addEvent(event)
##		self.filetransferWidget[sid]=QtGui.QListWidgetItem(self.main.ui.eventsListWidget)
##		self.filetransferWidget[sid].download=True
##		self.filetransferWidget[sid].setSizeHint(QtCore.QSize(100,height))
##		self.filetransferWidget[sid].queueId=sid
##		self.filetransferWidget[sid].file=file
##		self.filetransferWidget[sid].jid=jid
##		self.filetransferWidget[sid].sent=1
##		self.filetransferWidget[sid].broken=[]
##		self.filetransferWidget[sid].all=1
##		self.filetransferWidget[sid].errors=[]
##		self.filetransferWidget[sid].typ='normal'
##		self.filetransferWidget[sid].widget=FTWidget(text,self.filetransferWidget[sid],self.main,sid,self.main.ui.eventsListWidget,download=True)
##		self.filetransferWidget[sid].widget.setMinimumHeight(height)
##		if tab:
##			QtCore.QObject.connect(self.filetransferWidget[sid].widget.progressBar,QtCore.SIGNAL("valueChanged(int)"),tab.chat.filetransfer[sid].progressBar.setValue)
##		self.main.ui.eventsListWidget.setItemWidget(self.filetransferWidget[sid],self.filetransferWidget[sid].widget)
##		self.filetransfer[sid]={'queueId':sid}

	def nextFTUploadEvent(self,sid):
		event=self.ftEvents[sid]
		jid=event.jid
		file=event.queue[event.queue.keys()[0]].name
		typ=self.isImage(file)
		j=self.main.getJid(jid)
		feature=False
		if self.main.client.roster.has_key(j.userhost()):
			if self.main.client.roster[j.userhost()].resources.has_key(j.resource):
				feature=self.main.client.roster[j.userhost()].resources[j.resource].hasFeature('http://kopete.kde.org/protocol/file-preview')
		if typ!=False and feature:
			print 'generating file preview'
			d=threads.deferToThread(self.makeFTPreview,files[0])
			d.addCallback(self._nextFTUploadEvent,sid,'image/png')
		else:
			self._nextFTUploadEvent(None,sid,None)

	def _nextFTUploadEvent(self,preview,sid,previewType=False):
		event=self.ftEvents[sid]
		jid=event.jid
		file=event.queue[event.queue.keys()[0]].name
		description=event.queue[event.queue.keys()[0]].description
		del event.queue[event.queue.keys()[0]]


		if preview:
			bytes=QtCore.QByteArray()
			buf=QtCore.QBuffer(bytes)
			buf.open(QtCore.QIODevice.WriteOnly)
			preview.save(buf, "PNG")
			preview=base64.encodestring(str(bytes))

		#text="<b>"+basename(unicode(file))+'</b>'
##		for f in self.filetransferQueue[queueId].keys():
##			if f!=file:
##				text+="<font size=\"-1\">"+basename(f)+"</font><br/>"
		# get event height (based on font size)
##		metrics=QtGui.QApplication.fontMetrics()
##		rect=metrics.boundingRect(0, 0,self.main.width(), self.main.height(), QtCore.Qt.TextWordWrap, text)
##		height=metrics.height()+rect.height()+metrics.height()+10

		widget=event.getWidgets()[0]
		#widget.setText(text)
		event.setCurrentFile(file)
		event.setQueue(event.queue)
		mainWindow=self.main
		file=unicode(file)
		sid2=self.main.client.sendFile(jid, basename(file), file, description,preview=preview,previewType=previewType)
		event.setFileSize(int(self.main.client.ft[sid2].size))
		event.SID=sid2
		self.ftEvents[sid2]=event
		del self.ftEvents[sid]
		#mainWindow.tray.showMessage(mainWindow.tr("Sending file ")+basename(file)+mainWindow.tr(" to ")+unicode(jid), mainWindow.tr("You can see progress of sending in Events tab in main window."), QtGui.QSystemTrayIcon.Information, 4000)


		tab,index=self.main.chat.findTab(jid,typ=['chat'])
		if tab:
##			if tab.chat.filetransfer.has_key(queueId):
##				tab.chat.filetransfer[queueId].reinit(text,None,self.main,sid2,self.main.ui.eventsListWidget,"("+str(self.filetransferWidget[queueId].sent)+"/"+str(self.filetransferWidget[queueId].all)+")")#=FTWidget(text,item,self.main,sid2,self.main.ui.eventsListWidget,"("+str(item.sent)+"/"+str(item.all)+")")
##				tab.chat.filetransfer[queueId].setMinimumHeight(height)
			tab.chat.textEditWrite(self.main.webkitThemeFactory.genChatStatus(unicode(mainWindow.tr("Sending file"))+" "+unicode(basename(file)),self.main.now()))
			tab.chat.lastMessageFrom=""
##		self.filetransferWidget[queueId].setSizeHint(QtCore.QSize(100,height))
##		self.filetransferWidget[queueId].file=file
##		self.filetransferWidget[queueId].jid=jid
##		self.filetransferWidget[queueId].queueId=queueId
##		self.filetransferWidget[queueId].download=False
##		self.filetransferWidget[queueId].sent=self.filetransferWidget[queueId].sent+1
##		#if self.ftError[sid]==None:
##			#item.broken=self.filetransfer[sid].broken
##		#else:
##			#item.broken=self.filetransfer[sid].broken.append(self.filetransfer[sid].file)
##		self.filetransferWidget[queueId].all=self.filetransferWidget[queueId].all
##		self.filetransferWidget[queueId].typ='normal'
##		#log.msg("SENDING "+str(item.sent)+"/"+str(item.all))
##		self.filetransferWidget[queueId].widget.reinit(text,self.filetransferWidget[queueId],self.main,sid2,self.main.ui.eventsListWidget,"("+str(self.filetransferWidget[queueId].sent)+"/"+str(self.filetransferWidget[queueId].all)+")")#=FTWidget(text,item,self.main,sid2,self.main.ui.eventsListWidget,"("+str(item.sent)+"/"+str(item.all)+")")
##		self.filetransferWidget[queueId].widget.setMinimumHeight(height)
##		self.filetransferWidget[queueId].widget.setMaximumHeight(height)
##		#item.widget.reinit(text,item,self.main,sid2,self.main.ui.eventsListWidget,"("+str(item.sent)+"/"+str(item.all)+")")#=FTWidget(text,item,self.main,sid2,self.main.ui.eventsListWidget,"("+str(item.sent)+"/"+str(item.all)+")")
##		#item.widget.setMinimumHeight(height)
##		#self.main.ui.eventsListWidget.setItemWidget(self.filetransferWidget[queueId],self.filetransferWidget[queueId].widget)
##		self.filetransfer[sid2]={'queueId':queueId}
##		#self.main.filetransferTimer.start(500)
		#if self.main.ftError[sid]==None:
			#self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(self.filetransfer[sid]))

