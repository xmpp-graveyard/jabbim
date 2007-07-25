try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from filetransfer_ui import *
from os.path import basename

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

class delegate(QtGui.QItemDelegate):
	def __init__(self,parent=None):
		apply(QtGui.QItemDelegate.__init__,(self,parent))
	def createEditor(self,parent,option,index):
		if index.column() == 1:
			return QtGui.QItemDelegate(self).createEditor(parent, option, index)
		return False

class filetransferDialog(QtGui.QDialog):
	def __init__(self,main,files,jid,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.ui=Ui_fileTransfer()
		self.ui.setupUi(self)
		self.main=main
		self.files=files
		self.jid=jid
		self.d=delegate(self.ui.treeWidget)
		self.ui.treeWidget.setItemDelegate(self.d)
		self.ui.treeWidget.setIconSize(QtCore.QSize(64,64))
		for file in self.files:
			item=QtGui.QTreeWidgetItem(self.ui.treeWidget)
			item.setText(0,basename(unicode(file)))
			item.setData(32,0,QtCore.QVariant(unicode(file)))
			item.setFlags(QtCore.Qt.ItemIsEditable| QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
		#QtCore.QObject.connect(self.ui.treeWidget, QtCore.SIGNAL("itemClicked ( QTreeWidgetItem * , int)"),self.icon)

	#def icon(self,item,old):
		#print item
		#it=item.data(32,0)
		#file=unicode(it.toString())
		#if file.lower().endswith("png") or file.lower().endswith("jpg"):
			#if item.icon(0).isNull():
				#pixmap=QtGui.QPixmap(file)
				#pixmap=pixmap.scaled(QtCore.QSize(64,64))
				#icon=QtGui.QIcon(pixmap)
				#item.setIcon(0,icon)
		

	def accept(self):
		descriptions={}
		for i in range(int(self.ui.treeWidget.topLevelItemCount())):
			child=self.ui.treeWidget.topLevelItem(i)
			it=child.data(32,0)
			file=unicode(it.toString())
			descriptions[file]=unicode(child.text(1))
			
		jid=self.jid
		file=self.files
		files=self.files
		all=len(file)
		file=file[0]
		file=unicode(file)
		#self.jab.sendFile(jid,unicode(file))
		res = self.main.client.roster['users'][jid].getHighestResource()
		print "DESC:",descriptions[file]
		sid=self.main.client.sendFile(jid+'/'+res, basename(file), file,descriptions[file])
		self.main.filetransferQueue[sid]=files
		self.main.filetransferDescriptions[sid]=descriptions
		item=QtGui.QListWidgetItem(self.main.ui.eventsListWidget)
		item.setSizeHint(QtCore.QSize(100,60))
		item.queueId=sid
		item.file=file
		item.jid=jid+'/'+res
		item.sent=1
		item.broken=[]
		item.all=all
		item.widget=FTWidget(basename(file),item,self.main,sid,self.main.ui.eventsListWidget)
		self.main.ui.eventsListWidget.setItemWidget(item,item.widget)
		self.main.filetransfer[sid]=item
		self.done(1)