import sys,os
try: from PyQt4 import QtCore, QtGui
except: print "PyQt4 is not installed."
import widgets
from configobj import ConfigObj
from include import utils

class mainWindow(QtGui.QMainWindow):
	def __init__(self,parent=None):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		self.ui=widgets.mainWindow.Ui_MainWindow()
		self.ui.setupUi(self)
		self.homeDir=utils.getHomeDir() # get home dir
		utils.loadConfig(self) # load config files
		self.loadRoster() # load roster widget

		self.shows={u"online":u"1",
					u"available":u"1",
					u"chat":u"2",
					u"away":u"3",
					u"xa":u"4",
					u"dnd":u"5",
					u"None":u"1",
					u"offline":u"9",
					u"unavailable":u"9"
					}
		self.icons={u"1":u"online",
					u"2":u"chat",
					u"3":u"away",
					u"4":u"xa",
					u"5":u"dnd",
					u"9":u"offline"
					}
		self.status={"online":self.tr("Online"),
					"available":self.tr("Online"),
					"chat":self.tr("Chatty"),
					"away":self.tr("Away"),
					"xa":self.tr("Extended away"),
					"dnd":self.tr("DND"),
					"None":self.tr("Online"),
					"offline":self.tr("Offline")
					}

		self.roster={"groups":{},"users":{}}
		self.roster['groups']['Unknown']=self._addGroup('Unknown')
		self.addUser('test@jabbim.cz',"test",self.roster['groups']['Unknown'],first=True)

		items=self.ui.roster.getUserItems("test@jabbim.cz")
		lenght=int(len(items))
		for i in range(lenght):
			item=self.ui.roster.getUserItems("test@jabbim.cz")[0]
			print "DELETE ITEM:"+unicode(item.text(1))
			parent=item.parent()
			if parent:
				index=parent.indexOfChild(item)
				if index>-1:
					it=parent.takeChild(index)
					#it.view=0
					#del it
					#it=0

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
		item.setText(0,unicode(name))
		item.setText(1,"9"+unicode(name).lower())
		item.setText(2,unicode(name))
		item.setText(4,unicode(jid))
		item.setData(32,0,QtCore.QVariant([unicode(jid),unicode("contact")]))
		item.setIcon(0,self.getIcon(size=str(self.config['rosterIconSize']),status=self.icons["9"]))
		item.setFlags(item.flags()|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled)
		# item design
		#if len(self.main.client.roster['users'][jid].status)!=0:
			#if len(self.main.client.roster['users'][jid].status)>1:
				#show=self.main.client.roster['users'][jid].status[0]
			#else:
				#show=self.main.client.roster['users'][jid].status
		#else:
			#show="offline"
		#if unicode(item.text(1))[0]=='9':
			#self.ui.roster.setItemHidden(item, offline)
		return item

	def getIcon(self,jid=None,typ=None,size="32x32",status=None):
		icon=QtGui.QIcon()
		return icon

	def _addGroup(self, group):
		item=self.ui.roster.addGroup(unicode(group))
		index=self.ui.roster.indexFromItem(item,0)
		self.ui.roster.expand(index)
		return item
	
	def _addUser(self, itemjid, name, grp):
		return self.ui.roster.addUser(itemjid,name,grp)
	
	def loadRoster(self):
		# load roster widget
		layout=QtGui.QHBoxLayout(self.ui.rosterWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.ui.roster=widgets.rosterWidget.rosterWidget(self.ui.rosterWidget,self)
		layout.addWidget(self.ui.roster)


app = QtGui.QApplication(sys.argv)

MainWindow = mainWindow()
MainWindow.show()
app.exec_()
