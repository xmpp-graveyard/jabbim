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
		self.main.ui.roster.setStatus(jid,show)

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
		
		
	def loadRoster(self):
		# load roster widget
		layout=QtGui.QHBoxLayout(self.ui.rosterWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.ui.roster=widgets.rosterWidget.rosterWidget(self.ui.rosterWidget,self)
		layout.addWidget(self.ui.roster)

	def _connected(self):
		self.ui.rosterStackedWidget.setCurrentIndex(1)

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
		self.client = clientClass(jid+"/jabbim", password, jid.split("@")[1], 5222,self)
		self.client.connect()

translator=QtCore.QTranslator()
translator.load("locales/jabbim_"+str(QtCore.QLocale.system().name())[:2]+".qm")
app.installTranslator(translator)

MainWindow = mainWindow()
MainWindow.show()
reactor.run()

