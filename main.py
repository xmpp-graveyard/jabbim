"""
Piskvorky is jabber based game.
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
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from jabber import *
import sys,os,time,random
from configobj import ConfigObj

from mainwindow import *
from login import *
from preferences import *
from roster import *
from status import *
from chatwindow import *
from joingroupchat import *
from addcontact import *

#import games

class mainWindow(QtGui.QMainWindow):
	def __init__(self,parent=None):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		self.ui=Ui_mainWindow()
		self.ui.setupUi(self)
		self.loadRoster()
		# Signals
		app.connect(self.ui.showOffline, QtCore.SIGNAL("clicked(bool)"),self.hideOffline)
		app.connect(self.ui.addContact, QtCore.SIGNAL("clicked(bool)"),self.addContact)
		app.connect(self.ui.actionPreferences, QtCore.SIGNAL("triggered ( bool )"),self.preferencesClicked)
		self.timer=QtCore.QTimer()
		app.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.tick)
		self.timer.start(50)
		self.homeDir=self.getHomeDir()
		self.loadConfig()
		self.loadSkin()
		self.loadStatus()
		self.loadBookmarks()
		self.loadGroupchat()
		self.groupchat={}
		#self.users={}
		self.groups={}
		self.groups["Unknown"]={"item":self.ui.roster.addGroup(self.tr("Unknown")),"users":{}}
		self.chat=chatWindow(self,self,jab)
		self.ui.gridlayout.setMargin(1)
		self.ui.gridlayout.setSpacing(1)
		self.ready=False
		self.log=QtGui.QTextEdit(None)
		#self.log.show()
		
		self.tray=QtGui.QSystemTrayIcon(QtGui.QIcon("images/status/online.png"))
		menu=QtGui.QMenu(self)
		menu.addMenu(self.statusMenu)
		menu.addSeparator()
		menu.addAction(self.tr("Close"),self.trayQuit)
		
		app.connect(self.tray,QtCore.SIGNAL("activated (QSystemTrayIcon::ActivationReason)"),self.trayActivated)
		self.tray.setContextMenu(menu)
		self.tray.show()

	def trayQuit(self):
		self.close()
		self.tray.hide()

	def trayActivated(self,reason):
		if reason==QtGui.QSystemTrayIcon.Trigger:
			if self.isHidden():
				self.show()
			else:
				self.hide()

	def preferencesClicked(self,bool):
		# shows preferences
		w=preferencesWindow(self,self)
		w.show()

	def loadSkin(self):
		# loads config and repairs config file
		self.skin=ConfigObj("skins/"+self.config["chat_skin"],encoding='UTF8')

	def addContact(self,bool):
		contact=addContactWindow(self,jab)
		contact.exec_()

	def buildGroupchatMenu(self):
		self.groupchatMenu.clear()
		action=self.groupchatMenu.addAction(self.tr("Join new groupchat"))
		action.setData(QtCore.QVariant("new"))
		
		self.groupchatMenu.addSeparator()
		
		for k,v in self.bookmarks.iteritems():
			action=self.groupchatMenu.addAction(unicode(k))
			action.setData(QtCore.QVariant(v))
		self.groupchatMenu.addSeparator()
		action=self.groupchatMenu.addAction(self.tr("Manage bookmarks"))
		action.setData(QtCore.QVariant("manage"))

	def loadGroupchat(self):
		self.groupchatMenu=QtGui.QMenu(self.ui.groupchat)
		self.buildGroupchatMenu()
		self.ui.groupchat.setMenu(self.groupchatMenu)
		app.connect(self.groupchatMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.groupchatChanged)

	def loadRoster(self):
		layout=QtGui.QHBoxLayout(self.ui.rosterWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.ui.roster=rosterWidget(self.ui.rosterWidget,self,jab)
		layout.addWidget(self.ui.roster)

	def loadStatus(self):
		self.statuses={"online":QtGui.QIcon("images/status/online.png"),
						"available":QtGui.QIcon("images/status/online.png"),
						"offline":QtGui.QIcon("images/status/offline.png"),
						"chat":QtGui.QIcon("images/status/chat.png"),
						"away":QtGui.QIcon("images/status/away.png"),
						"xa":QtGui.QIcon("images/status/xa.png"),
						"dnd":QtGui.QIcon("images/status/dnd.png"),
						"None":QtGui.QIcon("images/status/offline.png")
						}
		self.nickSort={"online":"1",
						"available":"1",
						"chat":"2",
						"away":"3",
						"xa":"4",
						"dnd":"5",
						"None":"9",
						"offline":"9"
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
		action=self.statusMenu.addAction(self.statuses['online'],self.status["online"])
		action.setData(QtCore.QVariant("online"))
		action=self.statusMenu.addAction(self.statuses['chat'],self.status["chat"])
		action.setData(QtCore.QVariant("chat"))
		action=self.statusMenu.addAction(self.statuses['away'],self.status["away"])
		action.setData(QtCore.QVariant("away"))
		action=self.statusMenu.addAction(self.statuses['xa'],self.status["xa"])
		action.setData(QtCore.QVariant("xa"))
		action=self.statusMenu.addAction(self.statuses['dnd'],self.status["dnd"])
		action.setData(QtCore.QVariant("dnd"))
		self.ui.statusButton.setMenu(self.statusMenu)
		app.connect(self.statusMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.statusChanged)
		self.offline=True


	def groupchatChanged(self,action):
		data=action.data()
		data=data.toString()
		if data=="new":
			newchat=joinGroupChatWindow(self,jab)
			ret=newchat.exec_()
			if ret==1:
				self.chat.show()
		elif data=="manage":
			win=preferencesWindow(self,self,1)
			win.show()
		else:
			room=unicode(action.text())
			nickname=unicode(data)
			jab.getIntoRoom(room,nickname)
			self.groupchat[room]=[]
			self.chat.addGroupChatTab(room,nickname)

	def statusChanged(self,action):
		data=action.data()
		data=data.toString()
		self.ui.statusButton.setText(unicode(action.text()))
		self.ui.statusButton.setIcon(self.statuses[str(data)])
		setstatus=statusWindow(data)
		setstatus.exec_()


	def loadBookmarks(self):
		# loads config and repairs config file
		self.bookmarks=ConfigObj(self.homeDir+'/.jabbim/bookmarks',encoding='UTF8')
		if len(self.bookmarks)==0:
			if not os.path.isdir(self.homeDir+'/.jabbim'):
				os.mkdir(self.homeDir+'/.jabbim')
			self.bookmarks=ConfigObj(self.homeDir+'/.jabbim/bookmarks',encoding='UTF8')
			self.bookmarks.write()

	def loadConfig(self):
		# loads config and repairs config file
		configs={"jid":"",
				"passwd":"",
				"savePasswd":"",
				"chat_skin":"default.conf",
				"tray_message_view_connect":"logged_in",
				"tray_message_view_disconnect":"all",
				"proxy_type":"none",
				"proxy_server":"",
				"proxy_port":"",
				"proxy_user":"",
				"proxy_passwd":"",
				"resource":"Jabbim"
				}
		self.config=ConfigObj(self.homeDir+'/.jabbim/config',encoding='UTF8')
		if len(self.config)==0:
			if not os.path.isdir(self.homeDir+'/.jabbim'):
				os.mkdir(self.homeDir+'/.jabbim')
			self.config=ConfigObj(self.homeDir+'/.jabbim/config',encoding='UTF8')
			for k,v in configs.iteritems():
				self.config[k]=v
			self.config.write()
		rewrite=False
		for k,v in configs.iteritems():
			try:
				self.config[k]
			except:
				self.config[k]=v
				rewrite=True
		if rewrite==True:
			self.config.write()

	def getHomeDir(self):
		# gets homedir on win32 or linux
		if sys.platform != 'win32' :
			return os.path.expanduser( '~' )
		def valid(path):
			if path and os.path.isdir(path):
				return True
			return False
		def env(name):
			return os.environ.get( name, '' )
		homeDir = env( 'USERPROFILE' )
		if not valid(homeDir):
			homeDir = env( 'HOME' )
			if not valid(homeDir):
				homeDir = '%s%s' % (env('HOMEDRIVE'),env('HOMEPATH'))
				if not valid(homeDir):
					homeDir = env( 'SYSTEMDRIVE' )
					if homeDir and (not homeDir.endswith('\\')):
						homeDir += '\\'
					if not valid(homeDir):
						homeDir = 'C:\\'
		return homeDir

	def hideOffline(self,bool):
		self.offline=not bool
		for group,v in self.groups.iteritems():
			for k,user in self.groups[group]["users"].iteritems():
				if int(user["item"].text(1)[0])==9:
					self.ui.roster.setItemHidden(user["item"], not bool)
			self.ui.roster.hidden(not bool)

	def now(self):
		h,m,s=time.localtime()[3:6]
		return "%02d:%02d:%02d" % (h,m,s)

	def isGroupChat(self,jid):
		for k,v in self.groupchat.iteritems():
			if k==jid:
				return True
		return False

	def isGroupChatMember(self,chat,name):
		for user in self.groupchat[chat]:
			if unicode(user.text())==unicode(name):
				return True
		return False

	def getGroupChatMember(self,chat,name):
		for user in self.groupchat[chat]:
			if unicode(user.text())==unicode(name):
				return user
		return None

	def setLog(self,text,color):
		return
		cur=self.log.textCursor()
		cur.movePosition(QtGui.QTextCursor.End)
		self.log.setTextCursor(cur)
		self.log.insertHtml('<font color="'+color+'">'+text+'</font><br/><br/>')
		cur=self.log.textCursor()
		cur.movePosition(QtGui.QTextCursor.End)
		self.log.setTextCursor(cur)

	def jabberCommandHandler(self,e):
		if e[0] == "con_ready":
			MainWindow.show()
			login.done(1)
			jab.setStatus()

		elif e[0] == "groupchat_server_message":
			jid=str(e[1])
			text=unicode(e[2])
			for i in range(self.chat.ui.chatTab.count()):
				w=self.chat.ui.chatTab.widget(i)
				if str(w.jid)==jid:
					message=self.skin["status_message"].replace("[time]",self.now()).replace("[message]",unicode(text))
					w.chat.textEditWrite(message)
					return

		elif e[0] == "groupchat_message":
			jid=str(e[1])
			user=unicode(e[2])
			for i in range(self.chat.ui.chatTab.count()):
				w=self.chat.ui.chatTab.widget(i)
				if str(w.jid)==jid:
					if unicode(w.name)==unicode(user):
						message=self.skin["my_message"].replace("[time]",self.now()).replace("[user]",user).replace("[message]",unicode(e[3]))
					else:
						message=self.skin["message"].replace("[time]",self.now()).replace("[user]",user).replace("[message]",unicode(e[3]))
					w.chat.textEditWrite(message)
					return

		elif e[0] == "chat_message":
			jid=str(e[1])
			if len(self.ui.roster.getUsers(jid))!=0:
				user=self.ui.roster.getUsers(jid)[0]
				icon=user.icon(0)
				user=user.text(2)
			else:
				icon=self.status["offline"]
				user=jid
				
			message=self.skin["message"].replace("[time]",self.now()).replace("[user]",user).replace("[message]",unicode(e[3]))
			tab=None
			tabIndex=0
			for i in range(self.chat.ui.chatTab.count()):
				w=self.chat.ui.chatTab.widget(i)
				if str(w.jid)==jid+"/"+str(e[4]):
					tab=w
					tabIndex=i
					break
				if str(w.jid).rsplit("/")[0]==jid:
					tab=w
					tabIndex=i
			if tab!=None:
				if int(self.chat.ui.chatTab.currentIndex())!=tabIndex:
					self.chat.ui.chatTab.setTabIcon(tabIndex,QtGui.QIcon("images/status/message.png"))
				tab.chat.textEditWrite(message)
				return
			self.chat.show()
			self.chat.addChatTab(jid,unicode(user),icon,message)
		
		elif e[0] == "subscribe":
			jab.roster.Authorize(str(e[1]))
		
		elif e[0] == "nick_update":
			self.setLog("Presence - start","red")
			# Prisla presence
			jid=str(e[1])
			self.setLog("jid: "+jid,"blue")
			# Pokud je jid v rosteru:
			if self.ui.roster.isUser(jid):
				# Prochazeni vsech uzivatelu v rosteru, kteri maji shodne jid
				for user,group in self.ui.roster.getUsers(jid,True).iteritems():
					# Pokud se nejedna o odhlaseni uzivatele
					if str(e[2].getType())!="unavailable":
						# Pridani resource k uzivateli, pokud uz tam neni
						if not e[3] in self.groups[group]["users"][jid]["resources"]:
							self.groups[group]["users"][jid]["resources"].append(e[3])
							resources=self.groups[group]["users"][jid]["resources"]
							self.setLog("resources: "+unicode(resources),"black")
							try:
								resources.remove('')
							except:
								pass
							# Pokud je resourcu vic, pridavaji se polozky do rosteru
							if len(resources)>1:
								# Zjisteni jid+"/"+resource v rosteru
								res=[]
								for i in range(user.childCount()):
									j=user.child(i)
									j=j.data(32,0)
									j=str(j.toString())
									res.append(j)
								for resource in resources:
									# Pokud uz neni resource v rosteru, pridame ho
									if not jid+'/'+resource in res and len(resource)!=0:
										item=self.ui.roster.addResource(jid+'/'+resource,unicode(user.text(2))+" - "+resource,user)
						# Zmena stavu
						if self.config["tray_message_view_connect"]=="all":
							self.tray.showMessage(self.tr("User status"), self.tr("User ")+unicode(user.text(2))+self.tr(" is now ")+self.status[str(e[2].getShow())]+"\n"+unicode(e[2].getStatus()), QtGui.QSystemTrayIcon.Information, 5000)
						elif self.config["tray_message_view_connect"]=="online" and str(e[2].getShow())=="None":
							self.tray.showMessage(self.tr("User status"), self.tr("User ")+unicode(user.text(2))+self.tr(" is now ")+self.status[str(e[2].getShow())]+"\n"+unicode(e[2].getStatus()), QtGui.QSystemTrayIcon.Information, 5000)
						elif self.config["tray_message_view_connect"]=="logged_in" and int(unicode(user.text(1)[0]))==9:
							self.tray.showMessage(self.tr("User status"), self.tr("User ")+unicode(user.text(2))+self.tr(" is now ")+self.status[str(e[2].getShow())]+"\n"+unicode(e[2].getStatus()), QtGui.QSystemTrayIcon.Information, 5000)
						if str(e[2].getShow())!="None":
							user.setIcon(0,self.statuses[str(e[2].getShow())])
							user.setText(1,self.nickSort[str(e[2].getShow())]+unicode(user.text(2)))
						else:
							user.setIcon(0,self.statuses["online"])
							user.setText(1,self.nickSort["online"]+unicode(user.text(2)))
						for i in range(self.chat.ui.chatTab.count()):
							w=self.chat.ui.chatTab.widget(i)
							if str(w.jid)==jid or str(w.jid).rsplit("/")[0]==jid:
								self.chat.ui.chatTab.setTabIcon(i,user.icon(0))
						# Nastaveni tooltip
						user.setToolTip(0,'<font color="blue"><b>'+unicode(user.text(2))+'</b></font><hr>'+unicode(e[2].getStatus())+'<br/><b>'+self.tr("Jabber ID:")+' </b>'+str(jid)+'')
						# Nastaveni stavove zpravy pod nick v rosteru. Pokud neni zprava nastavena, vytvori se jen nick bez zpravy.
						user.setText(0,unicode(user.text(2)))
						#if unicode(e[2].getStatus())=="None" or len(e[2].getStatus())==0:
							#user.label.setText(unicode(user.text(2)))
						#else:
							#text=[word for word in unicode(e[2].getStatus()).split('\n') if word != ''][0]
							#user.label.setText(unicode(self.ui.roster.getUsers(jid)[0].text(2))+'<br/><font size="-1"><i>'+text+"</i></font>")
						# Zobrazeni polozky v rosteru
						self.ui.roster.setItemHidden(user,False)
					# Jedna se o odhlaseni
					elif str(e[2].getType())=="unavailable":
						# Pokud byl user predtim prihlaseny
						print unicode(user.text(1))
						if int(unicode(user.text(1))[0])!=9:
							# Odebrani resource z databaze
							try:
								self.groups[group]["users"][jid]["resources"].remove(e[3])
							except:
								print self.groups[group]["users"][jid]["resources"]
							# pokud by po smazani zbyla jen jedina resource, smaze se z rosteru
							if int(user.childCount())==2:
								for i in range(user.childCount()):
									user.takeChild(0)
							else:
								# pokud po smazani nezbude ani jedna resource, je kontakt offline
								if int(user.childCount())<=1:
									user.setIcon(0,self.statuses["offline"])
									user.setText(1,self.nickSort["offline"]+unicode(user.text(2)))
									self.ui.roster.setItemHidden(user,self.offline)
								# smazani resource
								for i in range(user.childCount()):
									item=user.child(i)
									j=item.data(32,0)
									j=str(j.toString())
									if str(j)==jid+"/"+e[3]:
										user.takeChild(i)
										break
							for i in range(self.chat.ui.chatTab.count()):
								w=self.chat.ui.chatTab.widget(i)
								if str(w.jid)==jid or str(w.jid).rsplit("/")[0]==jid:
									self.chat.ui.chatTab.setTabIcon(i,user.icon(0))
				# aktualizace cisel skupin
				self.ui.roster.refreshStats()
				# serazeni polozek v rosteru
				self.ui.roster.sortItems (1,QtCore.Qt.AscendingOrder)
			# Pokud je jid groupchat
			elif self.isGroupChat(jid):
				if str(e[2].getType())!="unavailable":
					nick=unicode(e[3])
					# Nalezeni spravneho groupchatu
					for i in range(self.chat.ui.chatTab.count()):
						w=self.chat.ui.chatTab.widget(i)
						if str(w.jid)==jid:
							# Pokud je uzivatel jiz v mistnosti, nacteme jej od tam
							print jid,e[2].getAffiliation()
							if self.isGroupChatMember(jid,unicode(nick)):
								user=self.getGroupChatMember(jid,unicode(nick))
							# Pokud neni v mistnosti, vytvorime jej
							else:
								user=QtGui.QListWidgetItem(unicode(nick))
								self.groupchat[jid].append(user)
							# Nastaveni stavu
							if str(e[2].getShow())!="None":
								user.setIcon(self.statuses[str(e[2].getShow())])
								#user.setText(1,self.nickSort[str(e[2].getShow())]+unicode(user.text(2)))
							else:
								user.setIcon(self.statuses["online"])
							# Tooltip
							#user.setToolTip('<font color="blue"><b>'+unicode(user.text(2))+'</b></font><hr>'+unicode(e[2].getStatus())+'<br/><b>Jabber ID: </b>'+str(jid)+'')
							# Pridani do seznamu uzivatelu v mistnosti
							w.chat.ui.listWidget.addItem(user)
							# serazeni
							w.chat.ui.listWidget.sortItems()
							return
				elif str(e[2].getType())=="unavailable":
					nick=unicode(e[3])
					for i in range(self.chat.ui.chatTab.count()):
						w=self.chat.ui.chatTab.widget(i)
						if str(w.jid)==jid:
							user=self.getGroupChatMember(jid,unicode(nick))
							w.chat.ui.listWidget.takeItem(int(w.chat.ui.listWidget.row(user)))
			else:
				self.setLog("jid in not in roster or groupchat: "+jid,"red")
			self.setLog("Presence END","red")
		elif e[0] == "roster_update":
			print " roster update"
			self.setLog("start - roster update","red")
			items=e[1].getItems()
			self.setLog(unicode(items),"blue")
			#self.groups={}
			for jid in items:
				try:
					jid=str(jid).lower()
					groups=e[1].getGroups(jid)
					self.setLog("jid: "+jid+", grous:"+unicode(groups),"black")
					if groups==None or groups==[]:
						groups=["Unknown"]
						#name=e[1].getName(jid)
						#self.groups["Unknown"]["users"][str(jid)]=self.ui.roster.addUser(jid,name,None,self.offline,self.statuses["offline"])
					for group in groups:
						if self.groups.has_key(group)==False:
							self.groups[group]={"item":self.ui.roster.addGroup(group),"users":{}}
						name=e[1].getName(jid)
						self.groups[group]["users"][str(jid)]={"item":self.ui.roster.addUser(jid,name,self.groups[group]["item"],self.offline,self.statuses["offline"]),"resources":[]}
				except:
					self.setLog("ERROR in parsing: "+jid,"red")
			self.ui.roster.sortItems (1,QtCore.Qt.AscendingOrder)
			self.setLog(unicode(self.groups),"green")
			self.setLog("end - roster update","red")
			jab.outc.put(True)
				

	def tick(self):
		# new chat lines handler
		lines = None#jab.newChatLines(self.actualRoom)
		if lines!=None and len(lines)!=0:
			for line in lines:
				self.widget.textEditWrite(line)

		# we must use try as forced reading of empty queue raises an error
		try:
			e = jab.inc.get(timeout = 0)
		except:
			e=None
		if e!=None:
			self.jabberCommandHandler(e)
		try:
			e = jab.err.get(timeout = 0)
			self.jabberErrorHandler(e)
		except:
			pass

	def jabberErrorHandler(self,error):
		if error == "con":
			self.jabberError(self.tr("Totaly unable to connect to server."))
			login.ui.connect.setEnabled(True)
		elif error == "auth":
			self.jabberError(self.tr("Bad username or password."))
			login.ui.connect.setEnabled(True)

	def jabberError(self,error):
		QtGui.QMessageBox.warning(self,self.tr("Error"),unicode(error),0,1)

class statusWindow(QtGui.QDialog):
	def __init__(self,data,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(False)
		self.ui=Ui_status()
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
		jab.setStatus(self.data,unicode(self.ui.status.toPlainText ()))
		self.done(1)


app = QtGui.QApplication(sys.argv)

jab = Jabber()
translator=QtCore.QTranslator()
translator.load("locales/jabbim_"+str(QtCore.QLocale.system().name())[:2]+".qm")
app.installTranslator(translator)

MainWindow = mainWindow()

login=loginWindow(MainWindow,jab,MainWindow)
ref=login.show()
sys.exit(app.exec_())
