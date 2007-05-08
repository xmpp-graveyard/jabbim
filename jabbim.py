"""
Jabbim.
Copyright (C) 2007 Jan Kaluza

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

import qt4reactor as reactor
app = QtGui.QApplication(sys.argv)
reactor.install(app)

from twisted.internet import reactor

import widgets
import pyxl

from configobj import ConfigObj
from include import utils

#def kill():
	#print "kill"
	#mainWindow.close()

#reactor.addSystemEventTrigger('after', 'shutdown', kill)

class clientClass(pyxl.client.Client):

	def on_init(self):
		self.roster['groups']['Unknown']=self.main.ui.roster.addGroup('Unknown')

	def on_authFailed(self,xmlstream):
		QtGui.QMessageBox.warning(self.main,self.main.tr("Error"),unicode(self.main.tr("Bad Jabber ID or password.")),0,1)
	
	def on_presence(self,jid,show):
		self.main.ui.roster.setStatus(jid.userhost(),show)

	def on_xml(self,xml):
		if self.main.xmlConsole.ui.enable.isChecked():
			text=unicode(xml)
			self.main.xmlConsole.ui.xml.append(text+"\n\n")
	
	def on_UpdateContact(self,jid):
		print "update",unicode(jid)

	def on_DeleteContact(self,jid):
		print "delete",unicode(jid)

class mainWindow(QtGui.QMainWindow):
	def __init__(self,parent=None):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		self.ui=widgets.mainWindow.Ui_MainWindow()
		self.ui.setupUi(self)
		self.homeDir=utils.getHomeDir() # get home dir
		utils.loadConfig(self) # load config files
		self.client=None
		# fill login form
		self.ui.login_password.setText(self.config['passwd'])
		self.ui.login_jid.setText(self.config['jid'])
		if self.config['savePasswd']=="True":
			self.ui.login_savePassword.setChecked(True)

		app.connect(self.ui.login_connect, QtCore.SIGNAL("clicked()"),self.connect)
		app.connect(app,QtCore.SIGNAL("lastWindowClosed() "),self.disconnect)
		app.connect(self.ui.showOffline, QtCore.SIGNAL("clicked(bool)"),self.hideOffline)
		app.connect(self.ui.actionShow_XML, QtCore.SIGNAL("triggered ( bool )"),self.showXml)


		self.ui.rosterStackedWidget.setCurrentIndex(0)
		self.loadRoster()
		
		self.statusPath="images/xxxxx/status/"
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
		self.statusMenu=QtGui.QMenu(self.tr("Status"),self.ui.statusButton)
		action=self.statusMenu.addAction(self.getIcon(status="online",size="16x16"),self.status["online"])
		action.setData(QtCore.QVariant("online"))
		action=self.statusMenu.addAction(self.getIcon(status="chat",size="16x16"),self.status["chat"])
		action.setData(QtCore.QVariant("chat"))
		action=self.statusMenu.addAction(self.getIcon(status="away",size="16x16"),self.status["away"])
		action.setData(QtCore.QVariant("away"))
		action=self.statusMenu.addAction(self.getIcon(status="xa",size="16x16"),self.status["xa"])
		action.setData(QtCore.QVariant("xa"))
		action=self.statusMenu.addAction(self.getIcon(status="dnd",size="16x16"),self.status["dnd"])
		action.setData(QtCore.QVariant("dnd"))
		action=self.statusMenu.addAction(self.getIcon(status="offline",size="16x16"),self.status["offline"])
		action.setData(QtCore.QVariant("offline"))
		self.ui.statusButton.setMenu(self.statusMenu)
		app.connect(self.statusMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.statusChanged)
		self.ui.statusButton.setText(unicode(self.status["offline"]))
		self.ui.statusButton.setIcon(self.getIcon("offline",size="16x16"))
		self.ui.statusButton.hide()
		self.offline=False
		self.xmlConsole=XMLConsole(self)

	def showXml(self,bool):
		self.xmlConsole.show()

	def hideOffline(self,bool):
		# hide or show offline users
		self.offline=not bool
		# rewrite online/all users stats in group QTreeWidgetItem
		for group,item in self.client.roster['groups'].iteritems():
			# return stats (online,offline,all users) for group
			for i in range(int(item.childCount())):
				child=item.child(i)
				if int(unicode(child.text(1))[0])==9:
					self.ui.roster.setItemHidden(child, not bool)
			self.ui.roster.hidden(not bool)

	def statusChanged(self,action):
		# status changed
		data=action.data()
		data=data.toString()
		self.ui.statusButton.setText(unicode(action.text()))
		self.ui.statusButton.setIcon(self.getIcon(status=data,size="16x16"))
		setstatus=statusWindow(data)
		setstatus.exec_()

	def loadRoster(self):
		# load roster widget
		layout=QtGui.QHBoxLayout(self.ui.rosterWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.ui.roster=widgets.rosterWidget.rosterWidget(self.ui.rosterWidget,self)
		layout.addWidget(self.ui.roster)

	def _connected(self):
		self.ui.rosterStackedWidget.setCurrentIndex(1)
		self.ui.statusButton.setText(unicode(self.status["online"]))
		self.ui.statusButton.setIcon(self.getIcon("online",size="16x16"))
		self.ui.statusButton.show()


	def disconnect(self):
		if self.client!=None:
			reactor.stop2()

	def getIcon(self,jid=None,typ=None,size="32x32",status=None):
		# return status icon
		path=self.statusPath.replace("xxxxx",size)
		#if jid!=None:
			#file=path+self.getUserType(jid)+"-"+self.iconSort[self.nickSort[typ]]+".png"
			#if os.path.exists(file):
				#icon=QtGui.QIcon(file)
			#else:
				##print "File not exist",file," <-",jid,typ
				##print "using",path+"jabber-"+self.iconSort[self.nickSort[typ]]+".png"
				#icon=QtGui.QIcon(path+"jabber-"+self.iconSort[self.nickSort[typ]]+".png")
		#else:
		if status==None:
			icon=QtGui.QIcon(path+"jabber-online.png")
		else:
			icon=QtGui.QIcon(path+"jabber-"+status+".png")
		return icon

	def connect(self):
		# Connect to the server
		jid=unicode(self.ui.login_jid.text())
		password=unicode(self.ui.login_password.text())
		if len(jid)!=0 and len(jid.split("@"))==2 and len(password)!=0:
			
			if jid!=self.config['jid'] or (password!=self.config['passwd'] and self.config['savePasswd']=="True") or self.config['savePasswd']!=str(self.ui.login_savePassword.isChecked()):
				ret=QtGui.QMessageBox.question(self,self.tr("Login information"), self.tr("Save current login information?"),3,4)
				if ret==3:
					self.config['savePasswd']=self.ui.login_savePassword.isChecked()
					if self.ui.login_savePassword.isChecked()==True:
						self.config['passwd']=password
					else:
						self.config['passwd']=""
					self.config['jid']=jid
					self.config.write()
		if self.client==None:
			self.client = clientClass(jid+"/jabbim", password, jid.split("@")[1], 5222,self)
		self.client.connect()

class XMLConsole(QtGui.QMainWindow):
	def __init__(self,data,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.ui=widgets.xmlConsole.Ui_xmlConsole()
		self.ui.setupUi(self)

class statusWindow(QtGui.QDialog):
	def __init__(self,data,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(False)
		self.ui=widgets.status.Ui_status()
		self.ui.setupUi(self)
		self.timer=QtCore.QTimer()
		app.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.timeout)
		app.connect(self.ui.status, QtCore.SIGNAL("cursorPositionChanged ()"),self.timerStop)
		app.connect(self.ui.status, QtCore.SIGNAL("textChanged ()"),self.timerStop)
		
		self.timer.start(1000)
		self.i=4
		self.data=data
		self.timeout()
	
	def timerStop(self):
		self.timer.stop()
		self.ui.time.setText("")
	
	def timeout(self):
		if self.i!=0:
			self.ui.time.setText(self.tr("Window will be closed in ")+unicode(self.i)+self.tr(" seconds."))
			self.i-=1
		else:
			self.accept()
	def accept(self):
		if self.data=="offline":
			MainWindow.client.sendPresence(show = "unavailable", status = unicode(self.ui.status.toPlainText ()))
			MainWindow.client.factory.stopTrying()
			MainWindow.ui.statusButton.setText(unicode(MainWindow.status["offline"]))
			MainWindow.ui.statusButton.setIcon(MainWindow.getIcon("offline",size="16x16"))
			MainWindow.ui.statusButton.hide()
			MainWindow.ui.rosterStackedWidget.setCurrentIndex(0)
			

			pass
		else:
			#app.postEvent(jab,customEvent(["set_status",self.groupchat,self.data,unicode(self.ui.status.toPlainText ())]))
			#jab.setStatus(MainWindow.groupchat,self.data,unicode(self.ui.status.toPlainText ()))
			MainWindow.client.sendPresence(show = unicode(self.data), status = unicode(self.ui.status.toPlainText ()))
		self.done(1)


translator=QtCore.QTranslator()
translator.load("locales/jabbim_"+str(QtCore.QLocale.system().name())[:2]+".qm")
app.installTranslator(translator)

MainWindow = mainWindow()
MainWindow.show()
reactor.run()

