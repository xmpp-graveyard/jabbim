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
import time

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
		self.temp_hosts=[]
		
	def on_discoInfoReceived(self, jid, node):
		if not self.main.hosts.has_key(jid):
			try:
				name=self.disco[jid][node]['identities'].keys()[0]
				typ=self.disco[jid][node]['identities'][name]['type']
			except:
				typ=None
			if typ!=None:
				if typ=="pep" or typ=="im":
					typ="jabber"
				elif typ=="file":
					typ="disk"
				self.main.hosts[jid]=typ
				#for key,v in self.roster['users'].iteritems():
					#if len(key.split("@"))>1:
						#if key.split("@")[1]==jid:
							#for i in range(len(v.rosterItems)):
								#status=self.main.icons[unicode(v.rosterItems[i].text(1))[0]]
								##users.append(self.main.groups[k]["users"][key]["item"])
								##groups[self.main.groups[k]["users"][key]["item"]]=k
								#self.roster['users'][key].rosterItems[i].setIcon(0,self.main.getIcon(jid=jid,size=str(self.main.config['rosterIconSize']),status=status,usertype=typ))

	def on_rosterAddUser(self, contact):
		groups=contact.groups
		name=contact.name
		jid=contact.jid
		
		if jid!=contact.tag:
			if len(unicode(jid).rsplit("@"))!=1:
				host=unicode(jid).rsplit("@")[1]
				if not self.disco.has_key(host) and not host in self.temp_hosts:
					#self.main.getUserType(host)
					self.temp_hosts.append(host)
					self.getDiscoInfo(host)
			if len(groups)==0:
				# add user item to Unknown group
				self.roster['users'][jid].rosterItems.append(self.main.ui.roster.addUser(jid,name,self.roster['groups']['Unknown']))
			for group in groups:
				# add user item to the group
				self.roster['users'][jid].rosterItems.append(self.main.ui.roster.addUser(jid,name,self.roster['groups'][group]))


	def on_rosterArrived(self):
		#del self.temp_hosts
		for jid,user in self.roster['users'].iteritems():
			if user.tag!=None and jid!=user.tag:
				for item in self.roster['users'][jid].rosterItems:
					self.roster['users'][user.tag].rosterItems.append(self.main.ui.roster.addMetaContact(user.tag,user.tag,item))

	def on_authFailed(self,xmlstream):
		QtGui.QMessageBox.warning(self.main,self.main.tr("Error"),unicode(self.main.tr("Bad Jabber ID or password.")),0,1)
	
	def on_presence(self,jid,show):
		
	
		if show=="offline":

			jid=jid.full()
			# Pridani resource
			if len(unicode(jid).rsplit("/"))!=1:
				resource=unicode(jid).rsplit("/")[1]
				jid=unicode(jid).rsplit("/")[0]
				if self.roster['users'][jid].resourcesItems.has_key(resource):
					for user in self.roster['users'][jid].rosterItems:
						#self.roster['users'][unicode(jid).rsplit("/")[0]].resourcesItems[resource]=self.main.ui.roster.addResource(jid,unicode(user.text(2))+" - "+k,user)
						user.takeChild(user.indexOfChild(self.roster['users'][jid].resourcesItems[resource]))
					del self.roster['users'][jid].resourcesItems[resource]
				if len(self.roster['users'][jid].resources)!=0:
					highest=self.roster['users'][jid].resources[self.roster['users'][jid].getHighestResource()]
					self.main.ui.roster.setStatus(jid,highest.show)
				else:
					self.main.ui.roster.setStatus(jid,show)
			else:
				self.main.ui.roster.setStatus(jid,show)
				
			#if len(unicode(jid).rsplit("/"))!=1:
				#resource=unicode(jid).rsplit("/")[1]
				#if self.roster['users'][unicode(jid).rsplit("/")[0]].resourcesItems.has_key(resource):
					#for user in self.roster['users'][unicode(jid).rsplit("/")[0]].rosterItems:
						##self.roster['users'][unicode(jid).rsplit("/")[0]].resourcesItems[resource]=self.main.ui.roster.addResource(jid,unicode(user.text(2))+" - "+k,user)
						#user.takeChild(user.indexOfChild(self.roster['users'][unicode(jid).rsplit("/")[0]].resourcesItems[resource]))
		else:

			jid=jid.full()
			# Pridani resource
			if len(unicode(jid).rsplit("/"))!=1:
				resource=unicode(jid).rsplit("/")[1]
				jid=unicode(jid).rsplit("/")[0]
				if len(self.roster['users'][jid].resources)>1:
					for i,v in self.roster['users'][jid].resources.iteritems():
						if not self.roster['users'][jid].resourcesItems.has_key(i):
							if self.roster['users'][jid].resourcesItems.has_key(0):
								add=False
							else:
								if self.roster['users'][jid].tag==None or self.roster['users'][jid].tag==jid:
									add=False
								else:
									add=True
							for user in self.roster['users'][jid].rosterItems:
								if add:
									self.roster['users'][jid].resourcesItems[0]=self.main.ui.roster.addSubGroup(self.main.tr("Resources:"),user,first="911")
								try:
									self.roster['users'][jid].resourcesItems[i]=self.main.ui.roster.addResource(jid + "/" + i,i,user)
								except:
									print "ERROR:",unicode(jid),unicode(show),unicode(resource),user
								self.main.ui.roster.setResourceStatus(jid,i,v.show)
				highest=self.roster['users'][jid].resources[self.roster['users'][jid].getHighestResource()]
				self.main.ui.roster.setStatus(jid,highest.show)
				self.main.ui.roster.setResourceStatus(jid,resource,show)
			else:
				self.main.ui.roster.setStatus(jid,show)
				
	def on_xml(self,xml):
		if self.main.xmlConsole.ui.enable.isChecked():
			text=unicode(xml)
			self.main.xmlConsole.ui.xml.append(text+"\n\n")
	
	def on_UpdateContact(self,jid):
		#print "update",unicode(jid),"groups:",self.roster['users'][jid].groups
		contact=self.roster['users'][jid]
		items=contact.getUserItems()
		toDel=[]
		for name,item in self.roster['groups'].iteritems():
			if name in contact.groups:
				add=True
				for i in items:
					parent=i.parent()
					if item==parent:
						add=False
						name=contact.name
						if name==None or len(name)==0:
							name=jid
						i.setText(0,unicode(name))
						i.setText(1,unicode(i.text(1))[0]+unicode(name).lower())
						i.setText(2,unicode(name))
						item.setData(32,0,QtCore.QVariant([unicode(jid),unicode("contact")]))
						self.main.ui.roster.setStatus(jid,self.main.icons[unicode(i.text(1))[0]],i)
						self.main.ui.roster.sortItems(1,QtCore.Qt.AscendingOrder)
						
				if add:
					if len(contact.getUserItems())!=0:
						i=contact.getUserItems()[0].clone() # clone contact item
						contact.rosterItems.append(i)
						for x in range(int(i.childCount())):
							child=i.child(x)
							
							it=child.data(32,0)
							it=it.toList()
							data=str(it[0].toString())
							typ=unicode(it[1].toString())
							
							if typ=="meta":

								print "len",len(self.roster['users'][data].rosterItems)
								print data,jid
								self.roster['users'][data].rosterItems.append(child)
								print "len",len(contact.rosterItems)
						self.roster['groups'][name].addChild(i) # add item to the new group
						self.main.ui.roster.setStatus(contact.jid,None,i)
					else:
						contact.rosterItems.append(self.main.ui.roster.addUser(contact.jid,contact.name,self.roster['groups'][name]))
						self.main.ui.roster.sortItems(1,QtCore.Qt.AscendingOrder)
						self.main.ui.roster.setStatus(contact.jid,None)
						self.main.ui.roster.refreshStats()
			else:
				for i in items:
					parent=i.parent()
					if item==parent:
						self.roster['users'][unicode(jid)].rosterItems.remove(i)
						parent.takeChild(parent.indexOfChild(i))
						if int(parent.childCount())==0:
							toDel.append(unicode(parent.text(2)))
							self.main.ui.roster.takeTopLevelItem(self.main.ui.roster.indexOfTopLevelItem(parent))
						break
		for name in toDel:
			del self.roster['groups'][name]

	def on_DeleteContact(self,jid):
		#print "delete",unicode(jid)
		contact=self.roster['users'][jid]
		items=contact.getUserItems()
		for name,item in self.roster['groups'].iteritems():
			for i in items:
				parent=i.parent()
				if item==parent:
					parent.takeChild(parent.indexOfChild(i))
					break

	def on_subscribe(self, msg,t):
		#self.ui.infoDockWidget.show()
		pass

	def on_message(self, frm, typ, body, subject = None, xhtml = None,chatstate = None,  delay = None):
		#print "message",frm
		if self.roster['users'].has_key(str(frm).rsplit("/")[0]):
			user=self.roster['users'][str(frm).rsplit("/")[0]].rosterItems[0]
			icon=user.icon(0)
			user=user.text(2)
		else:
			icon=self.main.getIcon(status="offline",size="16x16")
			user=frm
		
		message=unicode(body).replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>")
		message=self.main.skin["message"].replace("[time]",self.main.now()).replace("[user]",unicode(user)).replace("[message]",message)
		tab=None
		tabIndex=0
		for i in range(self.main.chat.ui.chatTab.count()):
			w=self.main.chat.ui.chatTab.widget(i)
			if str(w.jid)==str(frm):
				tab=w
				tabIndex=i
				break
			if str(w.jid).rsplit("/")[0]==str(frm).rsplit("/")[0]:
				tab=w
				tabIndex=i
		if tab!=None:
			if int(self.main.chat.ui.chatTab.currentIndex())!=tabIndex:
				self.main.chat.ui.chatTab.setTabIcon(tabIndex,QtGui.QIcon("images/16x16/actions/message.png"))
			tab.chat.textEditWrite(message)
		else:
			self.main.chat.addChatTab(frm,unicode(user),icon,message)

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
		self.hosts={}

		self.chat=widgets.chatwindow.chatWindow(self,self)

		app.connect(self.ui.login_connect, QtCore.SIGNAL("clicked()"),self.connect)
		app.connect(app,QtCore.SIGNAL("lastWindowClosed() "),self.disconnect)
		app.connect(self.ui.showOffline, QtCore.SIGNAL("clicked(bool)"),self.hideOffline)
		app.connect(self.ui.actionShow_XML, QtCore.SIGNAL("triggered ( bool )"),self.showXml)
		app.connect(self.ui.actionPreferences, QtCore.SIGNAL("triggered ( bool )"),self.preferencesClicked)

		self.ui.rosterStackedWidget.setCurrentIndex(0)
		self.loadRoster()
		self.loadSkin() # load chat skin
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
		self.ui.showOffline.hide()
		
		#self.addInfoSubscribe()
		#self.addInfoSubscribe()
		#self.addInfoSubscribe()

	#def addInfoSubscribe(self):
		#widget=subscribeWidget(self.ui.infoDockWidget)
		#self.ui.infoLayout.addWidget(widget)

	def getUserType(self,jid):
		# get type of jid (rss,disk,jabber, etc.)
		print self.client.disco[jid]
		#if len(jid.split("@"))!=1:
			#if self.discoInfo.has_key(jid.split("@")[1]):
				#typ=self.discoInfo[jid.split("@")[1]]
				#if typ=="pep" or typ=="im":
					#typ="jabber"
				#elif typ=="file":
					#typ="disk"
				#return typ
		#else:
			#print jid
		return "jabber"

	def preferencesClicked(self,bool):
		# shows preferences
		w=widgets.preferences.preferencesWindow(self,self)
		w.show()

	def loadSkin(self):
		# loads config and repairs config file
		self.skin=ConfigObj("skins/"+self.config["chat_skin"],encoding='UTF8')

	def now(self):
		# get time
		h,m,s=time.localtime()[3:6]
		return "%02d:%02d:%02d" % (h,m,s)

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
		self.ui.showOffline.show()


	def disconnect(self):
		if self.client!=None:
			reactor.stop2()

	def getIcon(self,jid=None,typ=None,size="32x32",status=None,usertype="jabber"):
		# return status icon
		path=self.statusPath.replace("xxxxx",size)
		typ=unicode(typ)
		if jid!=None:
			#file=path+self.getUserType(jid)+"-"+self.icons[self.show[typ]]+".png"
			if len(jid.split("@"))>1:
				host=jid.split("@")[1]
			else:
				host=None
			if self.hosts.has_key(host):
				usertype=self.hosts[host]
			if status==None:
				status=self.icons[self.shows[typ]]
			file=path+usertype+"-"+status+".png"
			if os.path.exists(file):
				icon=QtGui.QIcon(file)
			else:
				#print "File not exist",file," <-",jid,typ
				#print "using",path+"jabber-"+self.iconSort[self.nickSort[typ]]+".png"
				icon=QtGui.QIcon(path+"jabber-"+self.icons[self.shows[typ]]+".png")
		else:
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
			MainWindow.ui.showOffline.hide()

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

