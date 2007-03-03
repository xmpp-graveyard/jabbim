try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from grouped_events_ui import *
from addcontact import *

class groupedEventWindow(QtGui.QMainWindow):
	def __init__(self,parent,main,jab):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		self.main=main
		self.jab=jab
		self.ui=Ui_groupedevents()
		self.ui.setupUi(self)
		self.subscriptionsText=self.tr("Authorization requests")
		self.subscribedText=self.tr("Authorization informations")
		
		self.subscriptions=QtGui.QTreeWidgetItem(self.ui.events)
		self.subscriptions.setText(0,self.subscriptionsText + " (0)")
		self.subscribed=QtGui.QTreeWidgetItem(self.ui.events)
		self.subscribed.setText(0,self.subscribedText + " (0)")

		self.events={}
		QtCore.QObject.connect(self.ui.events, QtCore.SIGNAL("itemClicked ( QTreeWidgetItem * , int )"),self.eventClicked)
		QtCore.QObject.connect(self.ui.events, QtCore.SIGNAL("itemSelectionChanged ()"),self.eventSelected)
		QtCore.QObject.connect(self.ui.addContact, QtCore.SIGNAL("clicked()"),self.add)
		QtCore.QObject.connect(self.ui.ok, QtCore.SIGNAL("clicked()"),self.ok)
		self.text=self.tr("Use Jabber ID as name")
		self.ui.nickname.addItem(self.text)

	def ok(self):
		for item in self.ui.events.selectedItems():
			if item.parent()!=None:
				self.subscribed.takeChild(self.subscribed.indexOfChild(item))

	def add(self):
		toDel=[]
		for i in range(self.ui.selectedUsers.count()):
			item=self.ui.selectedUsers.item(i)
			jid=unicode(item.text())
			self.jab.roster.Authorize(jid)
			if not self.main.ui.roster.isUser(jid):
				if self.ui.nickname.currentText()==self.text:
					nickname=jid
				else:
					nickname=unicode(self.ui.nickname.currentText())
				group=unicode(self.ui.group.currentText())
				addContact(jid,nickname,group,self.main,self.jab)
				for x in range(self.subscriptions.childCount()):
					if unicode(self.subscriptions.child(x).text(0))==jid:
						toDel.append(x)
		toDel.sort(reverse=True)
		for i in toDel:
			self.subscriptions.takeChild(i)

	def eventSelected(self):
		self.ui.selectedUsers.clear()
		for item in self.ui.events.selectedItems():
			if item.parent()!=None:
				self.ui.selectedUsers.addItem(item.text(0))

	def eventClicked(self,item,i):
		if item.parent()==self.subscriptions:
			self.ui.stackedWidget.setCurrentIndex(0)
		elif item.parent()==self.subscribed:
			self.ui.stackedWidget.setCurrentIndex(1)
	
	def refresh(self):
		self.subscriptions.setText(0,self.subscriptionsText + " ("+str(self.subscriptions.childCount())+")")
		self.subscribed.setText(0,self.subscribedText + " ("+str(self.subscribed.childCount())+")")
	
	def addEvent(self,typ,data):
		self.ui.group.clear()
		for k,v in self.main.groups.iteritems():
			self.ui.group.addItem(unicode(k))
		if typ=="subscribe":
			self.events[data["jid"]]=QtGui.QTreeWidgetItem(self.subscriptions)
			self.events[data["jid"]].setText(0,data["jid"])
		elif typ=="subscribed":
			self.events[data["jid"]]=QtGui.QTreeWidgetItem(self.subscribed)
			self.events[data["jid"]].setText(0,data["jid"])
		self.refresh()
