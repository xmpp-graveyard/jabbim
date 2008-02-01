# -*- coding: utf-8 -*- 
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
import gc
#gc.set_debug(gc.DEBUG_LEAK|gc.DEBUG_UNCOLLECTABLE)
#self.callRemote('rpc@jabbim.cz/service', 'getInfo', ('smileys/white',)).addCallback(pis)
import sys,os
sys.path.append('.')
try: from PyQt4 import QtCore, QtGui
except: print "PyQt4 is not installed."

try:
	QtGui.QWizard
	USE_WIZARDS=True
except:
	USE_WIZARDS=False
import qt4reactor

class jabbimApplication(QtGui.QApplication):
	def __init__(self,args=[]):
		QtGui.QApplication.__init__(self,args)
		self.shutdown=False
	
	def commitData(self,manager):
		print "data commited"
		self.shutdown=True
		manager.release()

app = jabbimApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
qt4reactor.install(app)
from twisted.internet import reactor, threads
from twisted.internet.defer import DeferredList
from twisted.python import log
import time,base64, re
try:
	from hashlib import sha1
except:
	log.msg('Please upgrade to python2.5')
	from sha import new as sha1

import widgets
if USE_WIZARDS:
	import wizards
import pyxl
from pyxl import storage
import traceback
from configobj import ConfigObj
from include import utils
from include import rot13
import urllib, random, xmlrpclib
from imp import load_source
from urllib import quote, unquote
from include import plugins
from os.path import basename,dirname
from twisted.words.protocols.jabber.xmlstream import IQ
from twisted.words.xish.domish import Element
from twisted.words.protocols.jabber import jid as jidT
import ctypes

class clientClass(pyxl.client.Client):

	def on_init(self):
		self.temp_hosts=[]
		self.client_os = utils.get_os_info()
		self.version = '0.4SVN'
		self.bookmarksEnabled=True
		self.xmlCount=[]

#	def on_GCpresenceError(self, fromjid, code, typ, name):
#		log.msg("ERROR")
#		QtGui.QMessageBox.warning(self.main,self.main.tr("Error"),unicode(fromjid+" "+code+" "+typ+" "+name),0,1)

	def on_bookmarksFail(self):
		self.main.ui.tabWidget.setTabEnabled(1,False)
		self.bookmarksEnabled=False
		mainWindow=self.main
		self.main.tray.showMessage(MainWindow.tr("Error"),mainWindow.tr("Your server doesn't support Private XML Storage. Some functions will be disabled."))
		
	def on_privacyFail(self):
		self.main.ui.actionPrivacy_list_editor.setEnabled(False)

	def on_GCpresenceError(self, fromjid, code, typ, name, text, resource = ""):
		mainWindow=self.main
		log.msg("error")
		#log.msg("RESOURCE: "+resource)
		# find tab
		tab=None
		tabIndex=0
		for i in range(self.main.chat.ui.chatTab.count()):
			w=self.main.chat.ui.chatTab.widget(i)
			if unicode(w.jid)==unicode(fromjid):
				tab=w
				tabIndex=i
				break
		# we found tab
		if tab!=None:
			self.main.chat.ui.chatTab.removeTab(tabIndex)
			if int(self.main.chat.ui.chatTab.count())==0:
				self.main.chat.hide()
		if int(code)==409:
			self.main.events.addLineEditEvent(maintext=unicode(fromjid)+"<br/>"+text,trueCall=self.main.joinGC,trueDict=[fromjid],falseCall=None,falseDict=None,header="Groupchat Error",text="New name:",name=unicode(fromjid),typ="groupchatError",icon=None,action=None,actionDict=None,height=100, value=resource)
		else:
			self.main.events.addInfoEvent(header=mainWindow.tr("Groupchat error"),text=text,name=unicode(fromjid),typ='groupchatError')
		#QtGui.QMessageBox.warning(self.main,self.main.tr("Error"),unicode(fromjid+" "+unicode(code)+" "+unicode(name)+" "+unicode(text)),0,1)

	def on_roleErr(self,  muc,  err,  nick):
		log.msg("error")
		#QtGui.QMessageBox.warning(self.main,self.main.tr("Error"),unicode(muc+" "+err+" "+nick),0,1)
	
	def on_affiliationErr(self,  muc,  err,  nick):
		log.msg("error")
		#QtGui.QMessageBox.warning(self.main,self.main.tr("Error"),unicode(muc+" "+err+" "+nick),0,1)

	def on_ftTransfered(self, sid, bytes): # pocet prenesenych bajtu pro prenos se SID
		toDel=[] # finished transfers
		widget=self.main.events.filetransfer[sid] # event widget
		mainWindow=self.main
		if widget.typ=='normal':
			if self.ft.has_key(sid):
				# Filetransfer is alive
				size=float(self.ft[sid].size)
				sent=float(self.ft[sid].transfered)
				widget.widget.progressBar.setValue(int((sent/size)*100))
			else:
				# Filetransfer finished
				log.msg("ft.finished")
				widget.widget.progressBar.setValue(100)
				if widget.widget.complete==None:
					# User wants to close transfer
					toDel.append(sid)
					widget.widget.complete=True
					widget.widget.closeClicked()
				else:
					# transport finished
					toDel.append(sid)
					if self.main.ftError[sid]==None:
						widget.widget.stats.setText(mainWindow.tr("Complete"))
						self.main.tray.showMessage(mainWindow.tr('File transfer'),mainWindow.tr("File ")+unicode(widget.file)+mainWindow.tr(" has been sent/downloaded "), QtGui.QSystemTrayIcon.Information, 4000)
					else:
						widget.widget.stats.setText(mainWindow.tr("Error")+" "+unicode(self.main.ftError[sid]))
						self.main.tray.showMessage(mainWindow.tr('File transfer'),mainWindow.tr("File ")+unicode(widget.file)+mainWindow.tr(" can't be sent/downloadeded "), QtGui.QSystemTrayIcon.Critical, 4000)
					widget.widget.complete=True
	
	
			for sid in toDel:
				if self.main.events.filetransfer[sid].download==False:
					queueId=self.main.events.filetransfer[sid].queueId # filetransfer queue ID
					if queueId!=None:
						# delete sent file from queue and start uploading next file in queue
						del self.main.events.filetransferQueue[queueId][self.main.events.filetransfer[sid].file]
						if len(self.main.events.filetransferQueue[queueId])!=0:
							self.main.events.nextFTUploadEvent(sid,queueId)
					else:
						log.msg(unicode(self.main.events.filetransferQueue))
						log.msg(unicode(self.main.events.filetransfer[sid].file))
				# delete this filetransfer
				del self.main.events.filetransfer[sid]
		else:
			if self.ft.has_key(sid):
				# Filetransfer is alive
				size=float(self.ft[sid].size)
				sent=float(self.ft[sid].transfered)
				widget.setValue(int((sent/size)*100))
			else:
				# Filetransfer finished
				log.msg("ft.finished")
				widget.setValue(100)
				# User wants to close transfer
				del self.main.events.filetransfer[sid]

	def on_ftEnd(self, sid, error = None): #pokud je error None je vse v poradku, jinak strucny popis chyby.
		self.main.ftError[sid]=error
		print sid,self.main.allowedSids
		if sid in self.main.allowedSids:
			# continuing with jabbim extra
			print "Part of jabbim extra has been downloaded"
			file=self.ft[sid].file
			root=utils.extractZip(file,dirname(file))
			self.main.allowedSids.remove(sid)
			self.main.preferencesWindow.reloadView(file,root)
		del self.ft[sid]
		self.on_ftTransfered(sid, 0) # we have to delete filetransfer and etc

	def on_discoInfoReceived(self, jid, node):
		# save type of host, it not exist
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
				#if self.main.transports.has_key(jid):
					#self.main.transports[jid]=typ
					#self.menus=[]
					#for jid,typ in self.main.transports.iteritems():
						#jid=unicode(jid)
						#menu=QtGui.QMenu(unicode(jid),self.main.statusMenu)
						#menu.setIcon(self.main.getIcon("jid@"+unicode(jid),status="offline",size="16x16"))
						#action=menu.addAction(self.main.getIcon("jid@"+unicode(jid),status="online",size="16x16"),self.main.status["online"])
						#action.setData(QtCore.QVariant([jid,"online"]))
						#action=menu.addAction(self.main.getIcon("jid@"+unicode(jid),status="chat",size="16x16"),self.main.status["chat"])
						#action.setData(QtCore.QVariant([jid,"chat"]))
						#action=menu.addAction(self.main.getIcon("jid@"+unicode(jid),status="away",size="16x16"),self.main.status["away"])
						#action.setData(QtCore.QVariant([jid,"away"]))
						#action=menu.addAction(self.main.getIcon("jid@"+unicode(jid),status="xa",size="16x16"),self.main.status["xa"])
						#action.setData(QtCore.QVariant([jid,"xa"]))
						#action=menu.addAction(self.main.getIcon("jid@"+unicode(jid),status="dnd",size="16x16"),self.main.status["dnd"])
						#action.setData(QtCore.QVariant([jid,"dnd"]))
						#action=menu.addAction(self.main.getIcon("jid@"+unicode(jid),status="offline",size="16x16"),self.main.status["offline"])
						#action.setData(QtCore.QVariant([jid,"offline"]))
						##app.connect(menu, QtCore.SIGNAL("triggered ( QAction *)"),self.main.statusChanged)
						#self.menus.append(menu)
					#self.main.buildStatusMenu(self.menus)
					#self.main.buildStatusWidgetMenu()
				for host in self.main.hosts:
					for i in self.main.ui.roster.getUserItems(host):
						i.transport=True
		# set icons for users with this host
		for item in self.main.ui.roster.getHostItems(jid):
			show=unicode(item.status)
			item.icon=self.main.getIcon("jid@"+jid,size=self.main.ui.roster.iconSize,status=self.main.icons[show])
		if jidT.JID(jid).userhost()==self.jid.userhost():
			print 'self discoInfo'
			self.main.buildOfflineMenu()
	def on_rosterAddUser(self, contact):
		# add user to the roster
		groups=list(contact.groups)
		name=unicode(contact.name)
		jid=unicode(contact.jid)
		while u'' in groups:
			groups.remove('')
		#log.msg("Adding user JID: "+jid+" "+contact.subscription+" "+unicode(groups))
		# add group item if we haven't it
		for gr in groups:
			if not self.roster['groups'].has_key(gr):
				self.roster['groups'][gr]=self.main._addGroup(gr)
		# get host info if we haven't it
		if len(unicode(jid).rsplit("@"))!=1:
			host=unicode(jid).rsplit("@")[1]
		else:
			host=unicode(jid)
			#log.msg("Transport:"+jid)
			self.main.transports[unicode(jid)]=None
		if not self.disco.has_key(host) and not host in self.temp_hosts:
			self.temp_hosts.append(host)
			self.getDiscoInfo(host)
		# user is not in any group
		if len(groups)==0:
			# add user item to Unknown group
			self.main.ui.roster.addUser(jid,name,None)
		else:
			for group in groups:
				# add user item to the group
				self.main.ui.roster.addUser(jid,name,group)
		# show avatar
#		self.main.cache.get_avatar(jid, self.main._loadAvatar)
		self.main._loadAvatar(self.main.homeDir+'/avatars/'+jid, self.avatars.get(jid), jid)

	def on_discoItemsBookmarksReceived(self, jid):
		# make user list for bookmarked groupchat
		item=self.main.ui.bookmarks.findItems(jid,QtCore.Qt.MatchExactly,1)[0]
		for i in range(item.childCount()):
			item.takeChild(0)
		for name in self.disco[jid][None]['items'].keys():
			user=QtGui.QTreeWidgetItem(item)
			user.setText(0,unicode(jidT.JID(name).resource))
			user.setText(1,unicode(name))
			user.setIcon(0,self.main.getIcon(size="16x16"))

	def on_rosterArrived(self):
		print 'we got roster'
		self.main.ui.splashProgress.setValue(60)
		mainWindow=self.main
		self.main.ui.loginInfo.setText(mainWindow.tr("Roster arrived."))
		self.main.ui.roster.repaint()
		self.main.ui.roster.sortItems()
		self.main.buildBookmarks() # build Bookmarks tab
		self.main.chat.reconnect()
		
		# HACK KVULI ICQ A AUTOMATICKEMU PRIHLASENI K NEMU:
		#self.sendPresence("icq.jabbim.cz",show='available', status = "")

		self.menus=[]
		#print "TTTTTTTTTTTTTT:",self.main.transports
		#for jid,typ in self.main.transports.iteritems():
			#menu=QtGui.QMenu(unicode(jid),self.main.statusMenu)
			#action=menu.addAction(self.main.getIcon("jid@"+unicode(jid),status="online",size="16x16"),self.main.status["online"])
			#action.setData(QtCore.QVariant(jid+"/online"))
			#action=menu.addAction(self.main.getIcon("jid@"+unicode(jid),status="chat",size="16x16"),self.main.status["chat"])
			#action.setData(QtCore.QVariant(jid+"/chat"))
			#action=menu.addAction(self.main.getIcon("jid@"+unicode(jid),status="away",size="16x16"),self.main.status["away"])
			#action.setData(QtCore.QVariant(jid+"/away"))
			#action=menu.addAction(self.main.getIcon("jid@"+unicode(jid),status="xa",size="16x16"),self.main.status["xa"])
			#action.setData(QtCore.QVariant(jid+"/xa"))
			#action=menu.addAction(self.main.getIcon("jid@"+unicode(jid),status="dnd",size="16x16"),self.main.status["dnd"])
			#action.setData(QtCore.QVariant(jid+"/dnd"))
			#action=menu.addAction(self.main.getIcon(status="offline",size="16x16"),self.main.status["offline"])
			#action.setData(QtCore.QVariant(jid+"/offline"))
			##app.connect(menu, QtCore.SIGNAL("triggered ( QAction *)"),self.main.statusChanged)
			#self.menus.append(menu)
		self.main.buildStatusWidgetMenu()
		
		
		
		# vymazani metakontaktu
		#self.roster_meta={}
		#self.setMetacontacts()

		# hide Unknown group, if has not users
		#if int(self.main.ui.roster.getGroupItem("Unknown").childCount())==0:
			#self.main.ui.roster.setItemHidden(self.roster['groups']['Unknown'],True)

		self.metaParents={}

		## get metacontacts
		meta={} # temp variable for metacontacts - {userTag:userJid}
		for jid,user in self.roster['users'].iteritems():
			if jid == self.jid.userhost():
				continue
			if user.tag!=None:
				if not meta.has_key(user.tag):
					meta[user.tag]=[[jid,user.order]]
				else:
					meta[user.tag].append([jid,user.order])

		#log.msg("META:"+unicode(meta))

		for tag,jids in meta.iteritems():
			if len(jids)>1:
				mainJid=None # JID of main metacontact (parent of all other)
				highestNum=0
				#highest=
				for value in jids:
					jid=value[0]
					order=int(value[1])
					#if jid!=tag:
						#mainJid=jid
					if order>=highestNum:
						highestNum=order
						mainJid=jid
						#highest.append(jid)
				if mainJid:
					first=True
					toDel=[]
					mainItem=self.main.ui.roster.getUserItems(mainJid)[0]
					mainItem.metajid=mainJid
					mainItem.tag=tag
					for item in self.main.ui.roster.getUserItems(mainJid)[1:]:
						toDel.append(item)
					for i in range(len(toDel)):
						self.main.ui.roster.users.remove(toDel[i])
					
					self.main.ui.roster.metaItems[mainJid]=[]
					for value in jids:
						item=self.main.ui.roster.getUserItems(value[0])[0].clone()
						item.tag=tag
						self.main.ui.roster.metaItems[mainJid].append(item)
						if value[0]!=mainJid:
							for i in self.main.ui.roster.getUserItems(value[0]):
								self.main.ui.roster.users.remove(i)
		log.msg("METAITEMS:"+unicode(self.main.ui.roster.metaItems))

		if self.privacy != False or self.privacy != None:
			for item in self.privacy.active.items:
				if item.value and item.typ == "jid":
					for useritem in self.main.ui.roster.getUserItems(item.value):
						useritem.privacy["block"] = self.privacy.active.isBlockedJID(item.value)
						useritem.privacy["allow"] = self.privacy.active.isAllowedJID(item.value)
						useritem.privacy["hide"] = self.privacy.active.isHiddenJID(item.value)


		#toDelJid=[] # contacts to delete
		#toDelIndex=[] # contacts to delete
		## process metacontacts
		#for tag,jids in meta.iteritems():
			## get main metacontact (first metacontact)
			#if len(jids)>1:
				#mainJid=None # JID of main metacontact (parent of all other)
				#highestNum=0
				#highest=[]
				#for value in jids:
					#jid=value[0]
					#order=int(value[1])
					#if jid!=tag:
						#mainJid=jid
					#if order>=highestNum:
						#highest.append(jid)
	
				#if mainJid!=None and len(self.main.ui.roster.getUserItems(mainJid))!=0:
					#log.msg(mainJid +" "+unicode(self.main.ui.roster.getUserItems(mainJid)))
					#self.metaParents[tag]=self.main.ui.roster.addMetaParent(tag,self.main.ui.roster.getUserItems(mainJid)[0].parent(),True)
					##self.metaParents[tag].
					#for value in jids:
						#jid=value[0]
						#order=int(value[1])
	
						#self.main.ui.roster.addMetaContact(jid,self.roster['users'][jid].name,self.metaParents[tag],True)
						#items=self.main.ui.roster.getUserItems(jid,"contact")
						#lenght=int(len(items))
						#for contact in range(lenght):
							#item=self.main.ui.roster.getUserItems(jid,"contact")[0]
							#log.msg("DELETE ITEM:"+unicode(item.text(1)))
							#if item.childCount()==0:
								#parent=item.parent()
								#if parent:
									#index=parent.indexOfChild(item)
									#if index>-1:
										#it=parent.takeChild(index)
							##toDelJid.append(jid)
								##toDelIndex.append(self.roster['users'][jid].rosterItems.index(contact))
								##parent=contact.parent()
								##parent.takeChild(parent.indexOfChild(contact))
							##self.roster['users'][jid].rosterItems.remove(item)
					#self.main.ui.roster.cloneContact(self.metaParents[tag],self.main.ui.roster.getUserItems(jid)[0])
		##for i in range(len(toDelIndex)):
			##jid=toDelJid[i]
			##index=toDelIndex[i]
			##del self.roster['users'][jid].rosterItems[index]

			###If we had some others metacontacts
			##if mainJid!=None:
				##self.metaParents[tag]=self.main.ui.roster.addMetaParent(tag,self.roster['users'][mainJid].rosterItems[0].parent(),True)
				##main=[None,None]
				##for value in jids:
					##jid=value[0]
					##order=int(value[1])
					##toDel=[] # contacts to delete
					### add metacontat to the all items of mainJid in roster
					###for item in self.roster['users'][mainJid].rosterItems:
					##self.roster['users'][jid].rosterItems.append(self.main.ui.roster.addMetaContact(jid,self.roster['users'][jid].name,self.metaParents[tag],True))
					### Delete metacontacts' top level items from roster
					##for contact in self.roster['users'][jid].rosterItems:
						##it=contact.data(32,0)
						##it=it.toList()
						##if unicode(it[1].toString())=="contact":
							##toDel.append(contact)
							##parent=contact.parent()
							##parent.takeChild(parent.indexOfChild(contact))
					### delete metacontacts top level items from pyxl
					##for item in toDel:
						##self.roster['users'][jid].rosterItems.remove(item)
				##self.main.ui.roster.cloneContact(self.metaParents[tag],self.roster['users'][jid].rosterItems[-1])
		##print self.roster['users']['sef@njs.netlab.cz'].rosterItems
		# sort roster items and refresh group stats
		#self.main.rosterHideOffline(True)
		#self.main.ui.roster.refreshStats()
		self.main.ui.roster.sortItems()


		# set the priority
		if MainWindow.config.has_key('autoPriority'):
			if MainWindow.config['autoPriority']=='True':
				pri="20"
			else:
				if self.main.config.has_key('priority'):
					pri=self.main.config['priority']
				else:
					pri="0"
		else:
			if self.main.config.has_key('priority'):
				pri=self.main.config['priority']
			else:
				pri="0"
		show=unicode(self.main.ui.loginStatus.itemData(int(self.main.ui.loginStatus.currentIndex())).toString())
		self.main.selfStatus=show
		self.main.tray.setToolTip(mainWindow.tr('Your status:')+" "+self.main.status[show])
		self.main.ui.selfAvatar.refreshToolTip()
		self.main.sendPresence(None,show,"")
		self.main.ui.statusButton.setText(unicode(""))
		self.main.ui.statusButton.setIcon(self.main.getIcon(status=show,size="16x16"))
		self.main.ui.login_cancel.hide()

	def on_authFailed(self,xmlstream):
		# Authentication error
		self.main.ui.login_connect.setEnabled(True)
# 		QtGui.QMessageBox.warning(self.main,self.main.tr("Error"),unicode(self.main.tr("Bad Jabber ID or password.")),0,1)
	
	def on_firstpresence(self,  bulk):
		# process all first presences at once
		#log.msg(unicode(bulk))
		#print "PRESENCESSSSSS"
		for presence in bulk:
			#print presence
			jid=presence[0]
			show=presence[1]
			if len(presence)==3:
				error=presence[2]
			else:
				error=None
			self.on_presence(jid,show,error,True)
		# refresh and sort and so on
		#self.main.rosterHideOffline(True)
		self.main.ui.roster.refreshStats()
		self.main.ui.roster.sortItems (1,QtCore.Qt.AscendingOrder)
		self.main.ui.roster.statusLabel.hide()
		#if self.main.ui.roster.statusLabel:
			#self.main.ui.roster.statusLabel.setParent(None)
			#self.main.ui.roster.statusLabel=None
		#if self.main.ui.roster.buttonWidget:
			#self.main.ui.roster.buttonWidget.setParent(None)
			#self.main.ui.roster.buttonWidget=None
		self.main.ui.roster.repaint()
		self.main.ui.splashProgress.setValue(100)
		mainWindow=self.main

		self.main.ui.loginInfo.setText(mainWindow.tr("Jabbim is ready."))
		self.main.ui.rosterStackedWidget.setCurrentIndex(1)
		#for key,value in self.main.plugins.iteritems():
			#value.connected()
		self.main.findPlugins()
		self.main.loadPlugins()
		self.main.autoJoinGroupchat()
	def on_invite(self,jid, room, reason, cont = False):
		print "invite",cont
		if not cont:
			self.main.showInvitation(jid, room, reason, cont)
		else:
			tab,tabIndex=self.main.chat.findTab(unicode(jid))
			if tab:
				self.main.chat.removeTab(tabIndex)
				if self.main.chat.addGroupChatTab(room,self.jid.user,name=tab.tabName):
					self.joinGC(room, self.jid.user)
				
			else:
				self.main.showInvitation(jid, room, reason, cont)

	def on_GCpresence(self,  muc, nick,  show,  status,  codes = [], reason = '', actor = None, n=None):
		
		show = unicode(show) #!
		# presence in groupchat
		if not self.groupchats.has_key(muc):
			log.msg("bad GC presence:"+unicode(muc)+"; we are not connected there")
			return
		print 'reason,actor=',[reason],[actor]
		if show=="offline":
			# get user role
			# find good tab according to jid
			for i in range(self.main.chat.ui.chatTab.count()):
				w=self.main.chat.ui.chatTab.widget(i)
				if unicode(w.jid)==unicode(muc):
					# edit user item
					w.chat.removeUser(nick,codes,reason,actor,n)
					break
		else:
			# get user role
			role=self.groupchats[muc].users[nick].role
			affiliation=self.groupchats[muc].users[nick].affiliation
			# find good tab according to jid
			for i in range(self.main.chat.ui.chatTab.count()):
				w=self.main.chat.ui.chatTab.widget(i)
				if unicode(w.jid)==unicode(muc):
					# edit user item
					w.chat.editUser(nick,show,role,affiliation)
					break
		# message skin
		if not u'303' in codes:
			mainWindow=self.main
			message="[nick] "+unicode(mainWindow.tr('is now'))+" [show] [[message]]"
			if status == None:
				message = message.replace("[[message]]",'')
			else:
				message = message.replace("[message]",unicode(status))
			message=message.replace("[show]",unicode(self.main.status[show])).replace('[nick]', nick)
			message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace('[message]',message)

			w.chat.textEditWrite(message)
		tab,index=self.main.chat.findTab(muc+"/"+nick)
		if w and tab:
			tab.chat.textEditWrite(message)
			tab.ic=self.main.getIcon(unicode(muc),size="16x16",status=self.main.icons[self.main.shows[unicode(show)]])
			self.main.chat.ui.chatTab.setTabIcon(index,tab.ic)

	def on_presence(self,jid,show,error=None,first=False):
		#print "presence",jid,show
		# normal presence handler
		#log.msg("PRESENCE "+unicode(jid.full())+" "+unicode(show))
		print 'error: ', [error]
		if error!=None:
			print "PRESENCE ERROR:"+unicode(error)
			return
		mainWindow=self.main
		#else:
			#print jid.userhost(),self.jid.userhost()
		if show=="offline":
			if jid.userhost()==self.jid.userhost():
				print 'self presence'
				if jid.resource in self.main.selfResources:
					self.main.selfResources.remove(jid.resource)
					self.main.buildOfflineMenu()
			#jid=jid.full() # get jid
			# presence has resource
			#if len(unicode(jid).rsplit("/"))!=1:
				#resource=unicode(jid).rsplit("/")[1]
				#jid=unicode(jid).rsplit("/")[0]
				#self.main.ui.roster.setStatus(jid,show,first=first)
			#else:
			self.main.ui.roster.setStatus(jid.userhost(),show,first=first)

			for i in range(self.main.chat.ui.chatTab.count()):
				w=self.main.chat.ui.chatTab.widget(i)
				if unicode(jidT.JID(w.jid).full())==unicode(jid.full()):
					w.ic=self.main.getIcon(unicode(jid.userhost()),size="16x16",status="offline")
					self.main.chat.ui.chatTab.setTabIcon(i,w.ic)
					user=self.main.ui.roster.getUserItems(unicode(jid.userhost()))
					if len(user)==0:
						user=self.main.ui.roster.getMetaItems(jid.userhost())
						if len(user)!=0:
							user=user[0]
					if len(user)!=0:
						#user=self.roster['users'][unicode(frm).rsplit("/")[0]].rosterItems[0]
						user=user[0].name
					else:
						user=unicode(jid.full())
					if str(self.main.config["showChatStatusChanges"])=="True":
						#message=self.main.skin["gc_status_message"].replace("[time]",self.main.now()).replace("[show]",mainWindow.tr("offline")).replace('[nick]', user)
						#message = message.replace("[[message]]",'')

						mainWindow=self.main
						message="[nick] "+unicode(mainWindow.tr('is now'))+" [show] [[message]]"
						message = message.replace("[[message]]",'')
						message=message.replace("[show]",unicode(self.main.status[show])).replace('[nick]', user)
						message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace('[message]',message)

						w.chat.textEditWrite(message)
						w.chat.ui.chatstate.setText("")
					break

		else:
			#jid=jid.full() # get jid
			# presence has resource
			if jid.userhost()==self.jid.userhost():
				print 'self presence'
				if not jid.resource in self.main.selfResources:
					self.main.selfResources.append(jid.resource)
					self.main.buildOfflineMenu()
			status=None
			if jid.resource:
				if self.roster['users'][jid.userhost()].resources.has_key(jid.resource):
					res=self.roster['users'][jid.userhost()].resources[jid.resource]
					status=res.status
			else:
				status=self.roster['users'][unicode(jid.userhost())].status[1]

			for i in range(self.main.chat.ui.chatTab.count()):
				w=self.main.chat.ui.chatTab.widget(i)
				if unicode(jidT.JID(w.jid).full())==unicode(jid.full()):
					w.ic=self.main.getIcon(unicode(jid.userhost()),size="16x16",status=self.main.icons[self.main.shows[unicode(show)]])
					self.main.chat.ui.chatTab.setTabIcon(i,w.ic)
					user=self.main.ui.roster.getUserItems(unicode(jid.userhost()))
					if len(user)==0:
						user=self.main.ui.roster.getMetaItems(jid.userhost())
						if len(user)!=0:
							user=user[0]
					if len(user)!=0:
						#user=self.roster['users'][unicode(frm).rsplit("/")[0]].rosterItems[0]
						user=user[0].name
					else:
						user=unicode(jid.full())
					if str(self.main.config["showChatStatusChanges"])=="True":
						mainWindow=self.main
						message="[nick] "+unicode(mainWindow.tr('is now'))+" [show] [[message]]"
						message = message.replace("[[message]]",'')
						message=message.replace("[show]",unicode(self.main.status[show])).replace('[nick]', user)
						message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace('[message]',message)
						w.chat.textEditWrite(message)
					break

			if jid.resource:
				resource=jid.resource
				jid=jid.userhost()
				# get highest resource and status
				try:
					highest=self.roster['users'][jid].resources[self.roster['users'][jid].getHighestResource()]
					status=highest.status
				except:
					print 'error in resource', [jid.full()]
				#if highest.status!=None:
					#status=highest.status.replace("\n"," ").replace("<","&lt;").replace(">","&gt;")
				# set status
				#self.main.ui.roster.setStatus(jid,highest.show,status=status,first=first)
				# get user status
				#status=self.roster['users'][jid].status[1]
				if status!=None:
					status=status.replace("\n"," ").replace("<","&lt;").replace(">","&gt;")
				# set status
				#try:
				self.main.ui.roster.setStatus(jid,highest.show,status=highest.status,first=first)
				#except:
					#print 'UGLY HACK! ', jid
			else:
				# get user status
				jid=jid.userhost()
				status=self.roster['users'][jid].status[1]
				if status!=None:
					status=status.replace("\n"," ").replace("<","&lt;").replace(">","&gt;")
				# set status
				self.main.ui.roster.setStatus(jid,show,status=status,first=first)
				
	def on_xml(self,xml):
		# append xml to the xml console, if it's enabled...
		if self.main.xmlConsole.ui.enable.isChecked():
			text=unicode(xml)
			self.main.xmlConsole.ui.xml.append(text+"\n\n")
		if self.lastxml<10:
			self.lastxml+=1
			f=open(self.main.homeDir+'/lastxml','ab')
		else:
			self.lastxml=0
			f=open(self.main.homeDir+'/lastxml','wb')
		try:
			f.write(unicode(xml).encode('utf-8','replace'))
		except:
			log.err('Chyba zapisu lastxml')
		f.close()
		#if unicode(xml).find("OUT:")!=-1:
			#now=int(time.time())
			#if len(self.xmlCount)>60:
				#if self.xmlCount[0]>now-10:
					#print "SERVER FLOOD"
					#self.xmlCount=[]
					#self.sendMessage("hanzz@njs.netlab.cz", "server flood!",composing="gone")
				#self.xmlCount=[now]
			#else:
				#self.xmlCount.append(now)

	
	def on_UpdateContact(self,jid):
		# contact is updated
		if len(self.roster['users'][jid].groups)==1:
			if len(self.roster['users'][jid].groups[0])==0:
				self.roster['users'][jid].groups=[]
		contact=self.roster['users'][jid]
		items=self.main.ui.roster.getUserItems(jid)
		toDel=[] # temp variable for deleting items at the end of this function
		toDelJid=[]
		toDelIndex=[]
		#log.msg(jid+" "+unicode(contact.groups))

		# add group item if we haven't it
		for gr in contact.groups:
			if not self.main.ui.roster.groups.has_key(gr):
				self.roster['groups'][gr]=self.main._addGroup(gr)
				self.roster['groups'][gr].setExpanded(True)

		# delete old top level item of this contact if contact is not in "toplevel group"
		#if len(contact.groups)!=0:
			#items2=self.main.ui.roster.findItems(jid, QtCore.Qt.MatchFixedString,4)
			#if len(items2)==1:
				#self.main.ui.roster.takeTopLevelItem(self.main.ui.roster.indexOfTopLevelItem(items2[0]))
		jidGroups=list(self.roster['users'][jid].groups)
		if len(jidGroups)==0:
			jidGroups=[self.main.ui.roster.specialName]
		elif len(jidGroups[0])==0:
			jidGroups=[self.main.ui.roster.specialName]
			#add=True
			#for i in items:
				#if i.group==self.main.ui.roster.specialName:
					#add=False
					#name=contact.name
					#if name==None or len(name)==0:
						#name=jid
					#i.name=unicode(name)
					#i.escapedName=unicode(name).replace("<","&lt;").replace(">","&gt;")
					#i.jid=jid
					#self.main.ui.roster.sortItems()
					#self.main.ui.roster.changePos=True
					#self.main.ui.roster.repaint()
			#if add:
				
		# go through all groups
		rosterGroups=dict(self.roster['groups'])
		print self.main.ui.roster.groups
		rosterGroups[self.main.ui.roster.specialName]=self.main.ui.roster.groups[self.main.ui.roster.specialName]
		toDel=[]
		for name,item in rosterGroups.iteritems():
			# updated contact has to be in this group
			if name in jidGroups:
				add=True
				# go through all user items, find item in this group and edit it
				for i in items:
					if item.name==i.group:
						add=False # we found item
						name=contact.name
						if name==None or len(name)==0:
							name=jid
						i.name=unicode(name)
						i.escapedName=unicode(name).replace("<","&lt;").replace(">","&gt;")
						i.jid=jid
						self.main.ui.roster.sortItems()
						self.main.ui.roster.changePos=True
						self.main.ui.roster.repaint()
				# we didn't find item
				log.msg(unicode(add))
				if add:
					# we have some item to clone (so we can't create new one)
					if len(items)!=0:
						i=items[0].clone() # clone contact item
						i.group=unicode(name)
						print "append ",i
						self.main.ui.roster.users.append(i)
						self.main.ui.roster.sortItems()
						self.main.ui.roster.changePos=True
						self.main.ui.roster.repaint()
						#self.roster['groups'][name].addChild(i) # add item to the new group
						#index=self.main.ui.roster.indexFromItem(self.roster['groups'][name],0)
						#self.main.ui.roster.expand(index)
						#self.main.ui.roster.setStatus(jid,None,i)
					else:
						# add new contact to the roster
						log.msg(unicode(self.main.ui.roster.users))
						self.main.ui.roster.addUser(contact.jid,contact.name,name)
						log.msg(unicode(self.main.ui.roster.users))
						log.msg(unicode(contact.status))
						if len(contact.status)==2:
							show=contact.status[0]
							status=contact.status[1]
						else:
							if len(contact.status)==1:
								show=contact.status[0]
							else:
								show="offline"
							status=None
						#self.main.ui.roster.setStatus(contact.jid,show,status=status)
						for user in self.main.ui.roster.getUserItems(contact.jid):
							user.icon=self.main.getIcon(contact.jid,size="32x32",status=self.main.icons[self.main.shows[unicode(show)]])
							if self.main.shows[unicode(show)]!="9":
								user.hidden=False
							else:
								user.hidden=True
							user.statusMessage=status
							user.status=self.main.shows[unicode(show)]
						self.main.ui.roster.statusLabel.hide()
						self.main.ui.roster.changePos=True
						self.main.ui.roster.sortItems()
						self.main.ui.roster.repaint()

			else:
				# user is not in this group, so we have to delete them from this group, if he is there
				for i in self.main.ui.roster.getUserItems(jid):
					if item.name==i.group:
						if item.all==1 and not item.name in toDel:
							toDel.append(unicode(item.name))
						self.main.ui.roster.users.remove(i)
						self.main.ui.roster.sortItems()
						self.main.ui.roster.repaint()
						self.main.ui.roster.statusLabel.hide()
						## delete group, if it's empty
						#if int(parent.childCount())==0:
							#toDel.append(unicode(parent.text(2)))
							#self.main.ui.roster.takeTopLevelItem(self.main.ui.roster.indexOfTopLevelItem(parent))
						break
		for i in toDel:
			if i!=self.main.ui.roster.specialName:
				del self.main.ui.roster.groups[i]
				self.main.ui.roster.sortItems()
		# delete all groups saved in toDel
		#for i in range(len(toDelJid)):
			#jid=toDelJid[i]
			#index=toDelIndex[i]
			#del self.roster['users'][jid].rosterItems[index]
		#for name in toDel:
			#del self.roster['groups'][name]

	def on_unsubscribe(self,jid):
		print "unsubscribe"
		

	def on_unsubscribed(self,jid):
		print "unsubscribed"
		mainWindow=self.main

		jid=jidT.JID(jid)
		user=self.main.ui.roster.getUserItems(unicode(jid.userhost()))
		if len(user)==0:
			user=self.main.ui.roster.getMetaItems(jid.userhost())
			if len(user)!=0:
				user=user[0]
		if len(user)!=0:
			#user=self.roster['users'][unicode(frm).rsplit("/")[0]].rosterItems[0]
			user=user[0].name
		else:
			user=unicode(jid.full())
		jid=unicode(jid.full())
		self.main.events.addBooleanEvent(self.delContact,[jid],None,[],mainWindow.tr("Remove contact?"),jid+mainWindow.tr(" removed your authorization. You won't see his status. Do you want to remove him/her from your contact list?"),height=100,name=jid,typ="unsubcsribed",icon=None)


	def on_DeleteContact(self,jid):
		# delete contact from roster
		log.msg("delete contact")
		#contact=self.roster['users'][jid]
		for i in self.main.ui.roster.getUserItems(jid):
			if self.main.ui.roster.item==i:
				self.main.ui.roster.statusLabel.hide()
			self.main.ui.roster.users.remove(i)
		self.main.ui.roster.sortItems()
		self.main.ui.roster.repaint()
						## delete group, if it's empty
		#items=self.main.ui.roster.getUserItems(jid,'contact')
		#lenght=int(len(items))
		#for i in range(lenght):
			#item=self.main.ui.roster.getUserItems(jid)[0]
			#if item.childCount()==0:
				##log.msg("DELETE ITEM:"+unicode(item.text(1)))
				#parent=item.parent()
				#if parent:
					#index=parent.indexOfChild(item)
					#if index>-1:
						#it=parent.takeChild(index)
		log.msg("DELETE COMPLETE")
		self.main.ui.roster.refreshStats()

	def on_subscribe(self, frm,status):
		#self.main.events.addSubscribeEvent(frm,status)
		#if len(self.main.ui.roster.getUserItems(frm))==0 and len(self.main.ui.roster.getMetaItems(frm)):
		mainWindow=self.main
		if self.roster['users'].has_key(frm):
			self.main.events.addBooleanEvent(self.sendPresence,[frm,None,status,None,'subscribed'],self.sendPresence,[frm,None,status,None,'unsubscribed'],header=mainWindow.tr('Authorize contact?'),text=mainWindow.tr('user ')+" "+unicode(frm)+' '+mainWindow.tr("wants to see your status."),name=frm,typ="subscribe",height=80)
		else:
			self.main.events.addAddUserEvent(frm,status)

	def _onSubscribe(self,frm,status,add=False):
		#def __init__(self,main,parent=None,jid="",group=None,name="",add=True):
		dialog=widgets.addcontact.addContactDialog(self.main,self.main,jid=frm,group="",name=frm.split('@')[0],add=add)
		dialog.exec_()
		self.sendPresence(frm,None,status,None,'subscribe')
		self.sendPresence(frm,None,status,None,'subscribed')


	def on_GCmessage(self, frm, typ, body, subject = None, xhtml = None,  chatstate = None,  delay = None, error = None):
		# handle messages from groupchat
		# get user (resource) and MUC jid (saved in frm)
		if typ=="chat":
			return self.on_message(frm, typ, body, subject, xhtml,chatstate,delay,error)
		frm=jidT.JID(frm)
		if frm.resource:
			user=frm.resource
		else:
			user=frm.userhost()
		frm=frm.userhost()
		if not body:
			body=""
		if len(body)!=0:
			# find MUC tab
			for i in range(self.main.chat.ui.chatTab.count()):
				w=self.main.chat.ui.chatTab.widget(i)
				countMessage=False
				if unicode(w.jid) == frm:
					mainWindow=self.main
					if error=="remote-server-not-found":
						if w!=None:
							message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",mainWindow.tr("Your message can't be sent. Remote server not found."))
							w.chat.textEditWrite(message)
						return
					elif error!=None:
						if w!=None:
							message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",mainWindow.tr("Your message can't be sent.")+" "+unicode(error))
							w.chat.textEditWrite(message)
						return
					if xhtml==None:
						body=unicode(body).replace('&','&amp;').replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")
						body = utils.replace_url(body)
						body=body.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")
					else:
						xhtml=xhtml.replace("&quot;",'"')
					self.main.chat.onGCMessage(w,i,body,delay,subject,user,xhtml)
					return


	def on_message(self, frm, typ, body, subject = None, xhtml = None,chatstate = None,  delay = None, error = None):
		# handle normal 'chat' messages
		# get user icon or name, if we have him in roster. Or use default icon and jid as name
		if typ=="groupchat":
			return
		log.msg("CHATSTATE:"+unicode(chatstate))
		log.msg("ERROR:"+unicode(error))
		frm=jidT.JID(frm)
		if not body:
			body=""
		user=self.main.ui.roster.getUserItems(frm.userhost())
		if len(user)==0:
			user=self.main.ui.roster.getMetaItems(frm.userhost())
			if len(user)!=0:
				user=user[0]
		log.msg("tset")
		if len(user)!=0:
			#user=self.roster['users'][unicode(frm).rsplit("/")[0]].rosterItems[0]
			#icon=user[0].icon
			icon=self.main.getIcon(unicode(frm.userhost()),status=self.main.icons[str(user[0].status)],size="16x16")
			user=user[0].name
		else:
			#if self.groupchats[frm.host].users[nick].role
			if self.groupchats.has_key(frm.userhost()):
				user=frm.resource
				icon=self.main.getIcon(unicode(frm.userhost()),size="16x16",status=self.main.icons[self.main.shows[self.groupchats[frm.userhost()].users[user].show]])
				#icon=self.main.getIcon(status="online",size="16x16")
			else:
				icon=self.main.getIcon(status="offline",size="16x16")
				user=frm.full()
		tab,tabIndex=self.main.chat.findTab(frm.full())
		mainWindow=self.main
		if error=="remote-server-not-found":
			if tab!=None:
				message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",mainWindow.tr("Your message can't be sent. Remote server not found."))
				tab.chat.textEditWrite(message)
			return
		elif error!=None:
			if tab!=None:
				message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace("[message]",mainWindow.tr("Your message can't be sent.")+" "+unicode(error))
				tab.chat.textEditWrite(message)
			return

		if len(body)!=0:
			# strip html tags and \n from messages
			if xhtml==None:
				message=unicode(body).replace('&','&amp;').replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")
				message = utils.replace_url(message)
				message=message.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")
				
			else:
				message=xhtml.replace("&quot;",'"')
				message=message.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")

				#print 'xhtml=',unicode(message)
			#file=self.main.homeDir+'/avatars/'+unicode(frm.userhost())
			#<img src="[avatar]" width="32" height="32"/>
			#if not os.path.isfile(file):
				#file="images/32x32/apps/jabbim.png"
			if unicode(body).startswith("/me"):
				message=self.main.skin["me_message"].replace("[time]",self.main.now()).replace("[user]",unicode(user).replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")).replace("[message]",message[3:])
			else:
				message=self.main.skin["message"].replace("[time]",self.main.now()).replace("[user]",unicode(user).replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")).replace("[message]",message)
			colors=self.main.getSkinColors(0)
			if colors!=None:
				message=message.replace("[foreground]",colors[0]).replace("[background]",colors[1])
				if len(colors)==3:
					message=message.replace("[additive]",colors[2])
			# find tab
			#tab=None
			#tabIndex=0
			#for i in range(self.main.chat.ui.chatTab.count()):
				#w=self.main.chat.ui.chatTab.widget(i)
				#if unicode(w.jid)==unicode(frm):
					#tab=w
					#tabIndex=i
					#break
				#if unicode(w.jid).rsplit("/")[0]==unicode(frm).rsplit("/")[0]:
					#tab=w
					#tabIndex=i
			tab,tabIndex=self.main.chat.findTab(frm.full())

						
			# we found tab
			if tab!=None:
				message=message.replace("[avatar]","<img src=\""+tab.chat.file+"\" width=\"32\" height=\""+str(tab.chat.avatarHeight)+"\" />")
				# write message and set 'message' icon
				if int(self.main.chat.ui.chatTab.currentIndex())!=tabIndex:
					self.main.chat.ui.chatTab.setTabIcon(tabIndex,QtGui.QIcon("images/16x16/actions/message.png"))
					self.main.chat.ui.chatTab.tabBar().setTabTextColor(tabIndex,QtGui.QColor(255,0,0))
					self.main.chat.ui.chatTab.setTabText(tabIndex,"("+str(tab.chat.unread+1)+") "+tab.tabName)
					self.main.events.addInfoEvent(header=mainWindow.tr("Message"),text=mainWindow.tr("From: ")+unicode(user),name=unicode(frm.full()),typ='message',icon="images/xxxxx/actions/message.png",action=self.main.chat.activate,actionDict=[frm.full()],tooltip=mainWindow.tr("New message from ")+unicode(user))
					tab.chat.unread+=1
					if not self.main.chat.isActiveWindow():
						self.main.chat.setWindowTitle("("+str(int(self.main.chat.getUnreadMessages()))+") "+tab.tabName.replace("&",""))
				elif not self.main.chat.isActiveWindow():
					self.main.events.addInfoEvent(header=mainWindow.tr("Message"),text=mainWindow.tr("From: ")+unicode(user),name=unicode(frm.full()),typ='message',icon="images/xxxxx/actions/message.png",action=self.main.chat.activate,actionDict=[frm.full()],tooltip=mainWindow.tr("New message from ")+unicode(user))
					#if int(self.main.chat.ui.chatTab.currentIndex())==tabIndex:
					self.main.chat.setWindowTitle("("+str(int(self.main.chat.getUnreadMessages())+1)+") "+tab.tabName.replace("&",""))
					tab.chat.unread+=1
				else:
					color=self.main.chat.ui.chatTab.tabBar().palette().color(QtGui.QPalette.Foreground)
					self.main.chat.ui.chatTab.setTabText(tabIndex,tab.tabName)
					self.main.chat.ui.chatTab.tabBar().setTabTextColor(self.main.chat.ui.chatTab.currentIndex(),color)
				tab.chat.ui.chatstate.setText("")
				tab.chat.textEditWrite(message)
			else:
				# add new chattab
				created=False
				if self.main.chat.isHidden():
					created=True
					self.main.chat.showMinimized()
				if len(body)>40:
						traytext=body[:40]+" ..."
				else:
						traytext=body
				text='<table><tr>'
				if len(self.main.ui.roster.getUserItems(frm.userhost()))>0 and os.path.isfile(self.main.homeDir+'/avatars/'+unicode(frm.userhost())):
					item=self.main.ui.roster.getUserItems(frm.userhost())[0]
					pixmap=item.avatar.pixmap(64,64)
					text+='<td><img src="'+self.main.homeDir+'/avatars/'+unicode(item.jid)+'" width="'+str(pixmap.width())+'" height="'+str(pixmap.height())+'"/></td>'
				text+='<td><b>'+mainWindow.tr("New message from ")+unicode(user)+'</b><br/>'
				text+='<font size="-1">'+traytext+'<br/>'
				text+="</td></tr></table>"
				self.main.events.addInfoEvent(header=mainWindow.tr("New message"),text=mainWindow.tr("From: ")+unicode(user),name=unicode(frm.full()),typ='message',icon="images/xxxxx/actions/message.png",action=self.main.chat.activate,actionDict=[],tooltip=text)
				self.main.tray.showMessage(mainWindow.tr("New message from ")+unicode(user), traytext, QtGui.QSystemTrayIcon.Information, 4000)
				self.main.chat.addChatTab(frm.full(),unicode(user),icon,message)
				if created:
					self.main.chat.setWindowState(self.main.chat.windowState() & ~QtCore.Qt.WindowActive | QtCore.Qt.WindowMinimized )
					self.main.setWindowState(self.main.windowState() & QtCore.Qt.WindowActive)

				tab,tabIndex=self.main.chat.findTab(frm.full())
				if tab:
					self.main.chat.ui.chatTab.setTabIcon(tabIndex,QtGui.QIcon("images/16x16/actions/message.png"))
					self.main.chat.ui.chatTab.tabBar().setTabTextColor(tabIndex,QtGui.QColor(255,0,0))
					self.main.chat.ui.chatTab.setTabText(tabIndex,"("+str(tab.chat.unread+1)+") "+tab.tabName)
					tab.chat.unread+=1


		
		# we found tab
		if chatstate=="composing":
			if tab!=None:
				if self.main.chat.ui.chatTab.tabBar().tabTextColor(tabIndex).name()!=QtGui.QColor(255,0,0).name():
					self.main.chat.ui.chatTab.tabBar().setTabTextColor(tabIndex,QtGui.QColor(0,128,0))
				tab.chat.ui.chatstate.setText(mainWindow.tr("is typing..."))
		elif chatstate=="active":
			if tab!=None:
				tab.chat.ui.chatstate.setText(mainWindow.tr("gives attention to chat."))
		elif chatstate=="paused":
			if tab!=None:
				tab.chat.ui.chatstate.setText(mainWindow.tr("stops typing."))
		elif chatstate=="inactive":
			if tab!=None:
				tab.chat.ui.chatstate.setText(mainWindow.tr("doesn't give attention to chat."))
		elif chatstate=="gone":
			if tab!=None:
				tab.chat.ui.chatstate.setText(mainWindow.tr("closed the chat window."))
	def on_vcardReceived(self,  jid, card):
		#print card
		#TODO: zpracovat ukladani vcardu .. hash a cesta k souboru se ulozi do db
		pass
		#log.msg("vcard "+unicode(jid))
# 		log.msg(unicode(card))
#		if card.has_key("BINVAL"):
#			typ=None
#			if card.has_key("TYPE"):
#				typ=str(card['TYPE'].split("/")[1])
#			pixmap=QtGui.QPixmap()
#			image=base64.decodestring(str(card["BINVAL"]))
#			f=open(self.main.homeDir+'/avatars/'+jid,"wb")
#			f.write(image)
#			f.close()
#			if typ:
#				pixmap.loadFromData(image,typ)
#			else:
#				pixmap.loadFromData(image)
#			log.msg(unicode(self.jid.userhost())+" "+unicode(jid))
#			if unicode(self.jid.userhost())==unicode(jid):
#				print "Setting avatar"
#				self.main.ui.selfAvatar.setPixmap(pixmap.scaledToHeight(48))
#			for item in self.main.ui.roster.getUserItems(jid):
#				item.setAvatar(QtGui.QIcon(pixmap))
#			for item in self.main.ui.roster.getMetaItems(jid):
#				item[0].setAvatar(QtGui.QIcon(pixmap))
#			sha=sha1(image).hexdigest()
#			self.main.cache.set_avatar(jid, ['avatars/'+jid, sha])
#			self.main._loadAvatar('avatars/'+jid, sha, jid)
#		else:
#			self.main.cache.set_avatar(jid, ['nic', 'nic'])

	def on_avatarUpdate(self, jid):
		print "AVATAR:",[unicode(jid)]
		#pixmap=QtGui.QPixmap()
		if not self.avatars.has_key(jid.replace('/','%')):
			return
		if self.avatars[jid.replace('/','%')]==None:
			return

		pixmap=self.main.getAvatar(jid.replace('/','%'),frame=False,status=None)

		if unicode(self.jid.userhost())==unicode(jid):
			print "Setting avatar"
			avatar=pixmap.scaledToHeight(48,QtCore.Qt.SmoothTransformation)
			self.main.selfAvatar=pixmap
			self.main.ui.selfAvatar.setPixmap(avatar)
			self.main.ui.selfAvatar.setMinimumWidth(avatar.width()+3)
		for item in self.main.ui.roster.getUserItems(jid):
			item.setAvatar(QtGui.QIcon(pixmap))
		for item in self.main.ui.roster.getMetaItems(jid):
			item[0].setAvatar(QtGui.QIcon(pixmap))

		jid = jidT.JID(jid)
		w,i=self.main.chat.findTab(jid.userhost())
		if w:
			for item in w.chat.getUserItems(jid.resource):
				text=unicode(item.text(1))
				if len(text)!=0:
					item.setIcon(1,QtGui.QIcon(pixmap))
					result=self.main.getAvatar(pixmap,size="32x32",frame=False,status=self.main.icons[text[0]])
					item.setIcon(0,QtGui.QIcon(result))
					w.chat.setTooltip(item,jid.full())
			
		
		
			

	def on_fileReceived(self, sid, id):
		if self.main.config['autoDownload'] == 'True' or unicode(sid) in self.main.allowedSids:
			filename = self.main.config['autoDownloadPath']+'/'+self.ft[sid].fileprops['name']
			if unicode(self.ft[sid].tojid).find("rpc@jabbim.cz")!=-1 and not unicode(sid) in self.main.allowedSids:
				return
			else:
				filename = self.main.realHomeDir+'/'+self.ft[sid].fileprops['name']
			if self.ft[sid].method!=None:
				return
			self.main.events.addFTDownloadEvent(unicode(self.ft[sid].tojid),unicode(self.ft[sid].tojid),"",sid)
			
			if 'http://jabber.org/protocol/bytestreams' in self.ft[sid].methods:
				self.ft[sid].method = 'http://jabber.org/protocol/bytestreams'
				self.ft[sid].file = filename
				self.receiveFile(sid, id)
			elif 'http://jabber.org/protocol/ibb' in self.ft[sid].methods:
				log.msg('IBB offer')
				self.ft[sid].method = 'http://jabber.org/protocol/ibb'
				self.ft[sid].file = filename
				self.ft[sid].fp = open(self.ft[sid].file, 'wb')
				self.receiveFile(sid, id)
			#if unicode(sid) in self.main.allowedSids:
				#self.main.allowedSids.remove(unicode(sid))

		else:
			if unicode(self.ft[sid].tojid).find("rpc@jabbim.cz")==-1:
				self.main.events.addBooleanEvent(self.ftStarted,[sid,id],None,[],self.main.tr("File transfer"),text= unicode(" %s is sending you file."%unicode(self.ft[sid].tojid)),height=40,name=unicode(self.ft[sid].tojid),typ="ftTransfer",icon=None)

	def ftStarted(self,sid,id):
		#q = QtGui.QMessageBox.question(self.main,self.main.tr("File transfer"), unicode(" %s is sending you file."%unicode(self.ft[sid].tojid)),QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		#if q == QtGui.QMessageBox.Yes:
		mainWindow=self.main
		filename = QtGui.QFileDialog.getSaveFileName(self.main, mainWindow.tr("Save File"),self.ft[sid].fileprops['name'],mainWindow.tr("*.*"))
		log.msg(unicode(filename))
		self.main.events.addFTDownloadEvent(unicode(self.ft[sid].tojid),unicode(self.ft[sid].tojid),"",sid)
		log.msg('receiving file: ' + sid)
		if 'http://jabber.org/protocol/bytestreams' in self.ft[sid].methods:
			self.ft[sid].method = 'http://jabber.org/protocol/bytestreams'
			self.ft[sid].file = filename
			self.receiveFile(sid, id)
		elif 'http://jabber.org/protocol/ibb' in self.ft[sid].methods:
			log.msg('IBB offer')
			self.ft[sid].method = 'http://jabber.org/protocol/ibb'
			self.ft[sid].file = filename
			self.ft[sid].fp = open(self.ft[sid].file, 'wb')
			self.receiveFile(sid, id)
		
	
	def on_verify(self, id, thread, props, frm, typ): #xep0070
# 		self.replyVerify(id, thread, props, frm, typ, False)
		mainWindow=self.main
		self.main.events.addBooleanEvent(self.replyVerify,[id, thread, props, frm, typ, True], self.replyVerify,[id, thread, props, frm, typ, False],header=mainWindow.tr('Auth request'),text=mainWindow.tr('URL:')+" "+unicode(props['url']) + '<br/>' +mainWindow.tr('ID:') + unicode(props['id']), height = 60,name=frm,typ="xep70")
	
	def on_connect(self):
		mainWindow=self.main
		self.main.ui.loginInfo.setText(mainWindow.tr("Jabbim is connected to the server."))
		self.main.ui.splashProgress.setValue(20)
	
	def on_authd(self):
		mainWindow=self.main
		self.main.ui.loginInfo.setText(mainWindow.tr("Jabbim is logged in."))
		self.main.ui.splashProgress.setValue(40)

class AvatarLabel(QtGui.QLabel):
	def __init__(self,main,parent):
		QtGui.QLabel.__init__(self,parent)
		self.setObjectName("selfAvatar")
		self.main=main
		self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
	
	def mouseDoubleClickEvent(self,event):
		self.main.identityEditor()
		event.accept()

	def contextMenuEvent(self,event):
		self.main.offlineMenu.move(event.globalX(),event.globalY())
		self.main.offlineMenu.popup(QtCore.QPoint(event.globalX(),event.globalY()))
		event.accept()
	
	def refreshToolTip(self):
		if self.main.client:
			text='<table><tr>'
			if os.path.isfile(self.main.homeDir+'/avatars/'+unicode(self.main.config['jid'])):
				pixmap=QtGui.QIcon(self.main.homeDir+'/avatars/'+unicode(self.main.config['jid'])).pixmap(64,64)
				text+='<td><img src="'+self.main.homeDir+'/avatars/'+unicode(self.main.config['jid'])+'" width="'+str(pixmap.width())+'" height="'+str(pixmap.height())+'"/></td>'
			#text+='<td><b>'+self.tr("Name:")+'</b> '+item.escapedName+'<br/>'
			text+='<td><b>'+self.tr("JID:")+'</b> '+unicode(self.main.config['jid'])+'<br/>'
			if self.main.client.roster["users"].has_key(unicode(self.main.config['jid'])):
				contact = self.main.client.roster["users"][unicode(self.main.config['jid'])]
		
				for res in contact.resources.keys():
					status = contact.resources[res].status
					if not status:
						status = ""
					priority = contact.resources[res].priority
					#if priority == None:
					#	priority = self.tr("Unknown")
					if priority != None:
						priority = "(%s: %s)" % (self.tr("Priority"),priority)
					else:
						priority = ""
					show=contact.resources[res].show
					if not show:
						show='online'
					text+='<img src="images/16x16/status/jabber-%s.png">' % show # hodilo by se rozlisit k jakymu poatri transportu
					if res != None:
						text+='<b>%s</b> %s<br>' % (res, priority)
					text+='<font size="-1">%s</font>' % (status)
			text+="</td></tr></table>"
			self.setToolTip(text)


class mainWindow(QtGui.QMainWindow):
	def __init__(self,parent=None):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		self.ui=widgets.mainWindow.Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.toggleInvisible.hide()
		self.ui.statusButton.hide()
		layout=QtGui.QHBoxLayout(self.ui.selfAvatarWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.ui.selfAvatar=AvatarLabel(self,self.ui.selfAvatarWidget)
		layout.addWidget(self.ui.selfAvatar)
		self.setAttribute(QtCore.Qt.WA_AlwaysShowToolTips,True)
		self.app=app
		self.selfAvatar=None #: current avatar (QPixmap or None)
		self.selfStatus="" #: current show (string according to self.shows)
		self.QT43=USE_WIZARDS #: True if Qt version == 4.3
		self.log=None
		self.plugins = {}

		# get homedir
		self.homeDir=utils.getHomeDir() #: Jabbim home directory + profile directory
		for x in range(0,len(sys.argv)):
			if sys.argv[x] == '--home':
				self.homeDir= sys.argv[x+1]
		self.realHomeDir=unicode(self.homeDir) #: Jabbim home directory
		
		# check if there is existing profile
		profiles=utils.getProfiles(self.realHomeDir)
		if len(profiles)==0:
			if USE_WIZARDS:
				self.startwiz=wizards.firststart.firstStartWizard(self,self)
				self.startwiz.show()

		# load last profile according to ~/config
		utils.loadConfig(self,[])
		if not self.config['jid']+"-profile" in profiles:
			if len(profiles)!=0:
				self.homeDir=self.realHomeDir+"/"+profiles[0]
				utils.loadConfig(self,[])
			else:
				os.remove(self.realHomeDir+'/config')
				utils.loadConfig(self,[])
		else:
			self.homeDir=self.realHomeDir+"/"+self.config['jid']+"-profile"
			utils.loadConfig(self,[])
		
		# load cache and create tables
		if sys.platform != 'win32':
			self.cache = storage.Cache(db=utils.path(self.homeDir+u'/cache.db'))
		else:
			self.cache = storage.Cache(db=(unicode(self.homeDir)+u'/cache.db').encode('utf8')) #hack!
		self.cache.create_tables().addCallback(self.tables_created).addErrback(self.tables_loaded)
		
		# look & feel :)
		self.ui.gridlayout.setMargin(1)
		self.ui.gridlayout.setSpacing(1)
		self.ui.tabWidget.setTabText(0,"")
		self.ui.tabWidget.setTabText(1,"")
		self.ui.tabWidget.setTabText(2,"")
		self.ui.tabWidget.setTabText(3,"")
		self.ui.actionAdd_Contact.setEnabled(False)
		self.ui.actionJoin_groupchat.setEnabled(False)
		self.ui.actionService_Discovery.setEnabled(False)
		self.ui.registerButton.hide()
		self.ui.groupStyleWidget.hide()
		self.ui.userStyleWidget.hide()
		self.ui.selectedItemStyle.hide()
		self.setMinimumWidth(200)
		self.ui.statusLine.hide()

		# filetransfer
		#self.filetransferTimer=QtCore.QTimer()
		#QtCore.QObject.connect(self.filetransferTimer, QtCore.SIGNAL("timeout()"),self.refreshFT)
		self.filetransferDescriptions={}
		self.ftError={}
		self.filetransfer={}
		self.filetransferQueue={}
		self.allowedSids=[]
		
		# preparing chat window
		if self.config['oneWindow']=="True":
			self.workspace=QtGui.QWorkspace(self.ui.mdiWidget)
			layout=QtGui.QHBoxLayout(self.ui.mdiWidget)
			layout.addWidget(self.workspace)
			self.chat=widgets.chatwindow.chatWindow(self.workspace,self)
			self.workspace.addWindow(self.chat)
			self.chat.showMaximized() #: chat window
		else:
			self.ui.mdiWidget.hide()
			self.ui.mdiWidget.setParent(None)
			self.setMaximumWidth(250)
			self.chat=widgets.chatwindow.chatWindow(self,self) #: chat window
		
		# variables
		self.hosts={} #: {host:type_of_host}
		self.client=None #: Pyxl client instance
		self.events=widgets.events.events(self) #: events class
		self.preferencesWindow=widgets.preferences.preferencesWindow(self,self)
		self.styleSheetText=""
		self.profilesWindow=None
		self.mucbrowser=None
		self.addcontactdialog=None
		self.statusPath="images/xxxxx/status/"
		self.transports={}
		#: {show:ID}
		self.shows={u"online":u"1",
					u"available":u"1",
					u"chat":u"2",
					u"away":u"3",
					u"xa":u"4",
					u"dnd":u"5",
					u"None":u"1",
					u"":u"1",
					u"offline":u"9",
					u"unavailable":u"9"
					}
		#: {ID:icon_text}
		self.icons={u"1":u"online",
					u"2":u"chat",
					u"3":u"away",
					u"4":u"xa",
					u"5":u"dnd",
					u"9":u"offline"
					}
		#: {show:translated_text}
		self.status={"online":self.tr("Online"),
					"available":self.tr("Online"),
					"chat":self.tr("Chatty"),
					"away":self.tr("Away"),
					"xa":self.tr("Extended away"),
					"dnd":self.tr("DND"),
					"None":self.tr("Online"),
					"offline":self.tr("Offline"),
					"invisible":self.tr("Invisible")
					}
		self.offline=False
		self.xmlConsole=XMLConsole(self)
		self.ui.showOffline.hide()


		# signals
		QtCore.QObject.connect(self.ui.login_connect, QtCore.SIGNAL("clicked()"),self.connect)
		#QtCore.QObject.connect(self.ui.toggleInvisible, QtCore.SIGNAL("clicked(bool)"),self.toggleInvisibility)
		QtCore.QObject.connect(self.ui.registerButton, QtCore.SIGNAL("clicked ()"),self.registerButtonClicked)
		QtCore.QObject.connect(self.ui.login_cancel, QtCore.SIGNAL("clicked ()"),self.connectCancel)
		QtCore.QObject.connect(self.ui.profilesList, QtCore.SIGNAL("currentIndexChanged ( const QString & )"),self.profileChanged)
		QtCore.QObject.connect(self.ui.mucBrowserButton, QtCore.SIGNAL("clicked ()"),self.mucBrowser)
		QtCore.QObject.connect(self.ui.statusMessage, QtCore.SIGNAL("clicked (bool)"),self.statusMessageClicked)
		QtCore.QObject.connect(self.ui.statusLine, QtCore.SIGNAL("returnPressed ()"),self.statusLineFinished)
		
		QtCore.QObject.connect(self.ui.actionAbout, QtCore.SIGNAL("triggered ( bool )"),self.about)
		QtCore.QObject.connect(self.ui.actionShow_XML, QtCore.SIGNAL("triggered ( bool )"),self.showXml)
		QtCore.QObject.connect(self.ui.actionPrivacy_list_editor, QtCore.SIGNAL("triggered ( bool )"),self.privacyListEditor)
		QtCore.QObject.connect(self.ui.actionAdd_Contact, QtCore.SIGNAL("triggered ( bool )"),self.addContactMainWindow)
		QtCore.QObject.connect(self.ui.actionPreferences, QtCore.SIGNAL("triggered ( bool )"),self.preferencesClicked)
		QtCore.QObject.connect(self.ui.actionProfiles, QtCore.SIGNAL("triggered ( bool )"),self.profilesClicked)
		QtCore.QObject.connect(self.ui.actionJoin_groupchat, QtCore.SIGNAL("triggered ( bool )"),self.joinGroupchat)
		QtCore.QObject.connect(self.ui.actionBrowse_rooms, QtCore.SIGNAL("triggered ( bool )"),self.mucBrowser)
		QtCore.QObject.connect(self.ui.actionQuit, QtCore.SIGNAL("triggered ( bool )"),self.trayQuit)
		QtCore.QObject.connect(self.ui.actionService_Discovery, QtCore.SIGNAL("triggered ( bool )"),self.serviceDiscovery)
		QtCore.QObject.connect(self.ui.actionIdentity, QtCore.SIGNAL("triggered ( bool )"),self.identityEditor)

		QtCore.QObject.connect(self.ui.bookmarks, QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.bookmarksContextMenu)
		QtCore.QObject.connect(self.ui.bookmarks, QtCore.SIGNAL("currentItemChanged ( QTreeWidgetItem * , QTreeWidgetItem * )"),self.bookmarksCurrentChanged)
		QtCore.QObject.connect(self.ui.bookmarks, QtCore.SIGNAL("itemActivated ( QTreeWidgetItem *, int )"),self.bookmarksClicked)
		QtCore.QObject.connect(self.ui.bookmarks, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.bookmarksClicked)
		QtCore.QObject.connect(self.ui.bookmarks, QtCore.SIGNAL("itemClicked ( QTreeWidgetItem *, int )"),self.bookmarksItemClicked)
		
		QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self.ui.bookmarks,self.deleteCurrentBookmark)
		QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self.ui.statusLine,self.statusLineCanceled)

		# set up bookmarks treeWidget
		self.ui.bookmarks.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.ui.bookmarks.header().hide()
		self.ui.bookmarks.hideColumn(1)
		
		# set up stacked widget (0==login,1==roster, 2==events and etc..)
		self.ui.rosterStackedWidget.setCurrentIndex(0)
		self.loadRoster() # load roster widget
		QtCore.QObject.connect(self.ui.rosterSearch, QtCore.SIGNAL(" textEdited ( const QString & )"),self.ui.roster.search)

		self.loadSkin() # load chat skin
		self.loadTheme() # load theme
		self.ui.roster.reskin() # reskin roster
		self.selfResources=[] #: Resources which are connected from the same JID as user
		self.buildOfflineMenu() # build menu with 'show offline', 'show away'
		
		# open log file
		if self.config['log'] == 'true':
			self.logfile = open(self.homeDir+'/'+self.config['logfile'], 'w')
			self.log=log.FileLogObserver(self.logfile)
			log.startLoggingWithObserver(self.log.emit)
		
		# show tray icon
		self.tray=QtGui.QSystemTrayIcon(QtGui.QIcon(QtGui.QIcon("images/16x16/apps/jabbim.png").pixmap(16,16,QtGui.QIcon.Disabled)))
		app.connect(self.tray,QtCore.SIGNAL("activated (QSystemTrayIcon::ActivationReason)"),self.trayActivated)
		self.tray.show()
		
		# set mainwindow size and position
		w=self.config['windowGeometry'][2]
		h=self.config['windowGeometry'][3]
		if str(w)=='None' or str(h)=='None':
			if str(w)!='None':
				self.resize(int(w),self.height())
			self.move(int(self.config['windowGeometry'][0]),int(self.config['windowGeometry'][1]))
		else:
			self.setGeometry(int(self.config['windowGeometry'][0]),int(self.config['windowGeometry'][1]),int(w),int(h))
		# set chatWindow size and position
		w=self.config['chatGeometry'][2]
		h=self.config['chatGeometry'][3]
		if str(w)=='None' or str(h)=='None':
			if str(w)!='None':
				self.chat.resize(int(w),self.height())
			self.chat.move(int(self.config['chatGeometry'][0]),int(self.config['chatGeometry'][1]))
		else:
			self.chat.setGeometry(int(self.config['chatGeometry'][0]),int(self.config['chatGeometry'][1]),int(w),int(h))

		self.reconnect = True # :# True = Jabbim will reconnect after disconnect
		self.active=True
		
		# set roster mode
		if self.config['rosterMode'] == "compact" :
			self.ui.roster.userHeight=22
			self.ui.roster.groupHeight=22
			self.scroll.verticalScrollBar().setPageStep(22)
			self.scroll.verticalScrollBar().setSingleStep(22)
			self.ui.roster.compact=True
			self.ui.roster.repaint()

		# fill login form
		self.fillLoginForm()
		self.ui.loginStatus.addItem(self.getIcon(status="online",size="16x16"), self.status["online"],QtCore.QVariant("online"))
		self.ui.loginStatus.addItem(self.getIcon(status="chat",size="16x16"), self.status["chat"],QtCore.QVariant("chat"))
		self.ui.loginStatus.addItem(self.getIcon(status="away",size="16x16"), self.status["away"],QtCore.QVariant("away"))
		self.ui.loginStatus.addItem(self.getIcon(status="xa",size="16x16"), self.status["xa"],QtCore.QVariant("xa"))
		self.ui.loginStatus.addItem(self.getIcon(status="dnd",size="16x16"), self.status["dnd"],QtCore.QVariant("dnd"))

		self.emoticonsWidget=widgets.emoticonswidget.emoticonsWidget(self,self)

		# join if we can :)
		if self.config['autoJoin']=='True':
			self.connect()
		

	def statusLineCanceled(self):
		self.ui.statusLine.hide()
		self.ui.statusMessage.show()

	def statusLineFinished(self):
		status=unicode(self.ui.statusLine.text())
		if len(status)!=0:
			self.sendPresence(None,self.selfStatus,status)
		self.ui.statusLine.hide()
		self.ui.statusMessage.show()

	def statusMessageClicked(self,b):
		self.ui.statusMessage.hide()
		self.ui.statusLine.setText("")
		self.ui.statusLine.show()
		self.ui.statusLine.setFocus(QtCore.Qt.MouseFocusReason)

	def sendFiles(self,jid):
		file=QtGui.QFileDialog.getOpenFileNames(self,self.tr("Choose files"))
		file=list(file)
		if len(file)!=0:
			new=[]
			for f in file:
				new.append(unicode(f))
			file=new
			self.showFiletransferDialog(file,jid)
			#self.senddialog=filetransfer.filetransferDialog(self.main,file,jid)
			#self.senddialog.show()

	def showFiletransferDialog(self,files,jid):
		"""
		Shows filetransfer dialog.
		@type files: list of unicode
		@param files: list of files (full path)
		@type jid: unicode
		@param jid: JID
		"""
		#if jid=="album@disk.jabbim.cz":
		self.senddialog=widgets.albumfiletransfer.albumFiletransferDialog(self,files,jid)
		#else:
			#self.senddialog=widgets.filetransfer.filetransferDialog(self,files,jid)
		self.senddialog.show()

	def buildOfflineMenu(self):
		"""
		Builds menu with 'show offline', 'show away' etc. There are selfResources (if user is connected from more than one client) too.
		"""
		# make Show offline QAction
		self.offlineMenu=QtGui.QMenu(self.ui.showOffline)
		self.showOfflineAction=self.offlineMenu.addAction(self.tr("Show Offline"))
		self.showOfflineAction.setCheckable(True)
		self.showOfflineAction.setObjectName('show_offline')
		self.showOfflineAction.setChecked(self.offline)
		QtCore.QObject.connect(self.showOfflineAction,QtCore.SIGNAL("toggled ( bool )"),self.hideOffline)

		# make Show transports QAction
		action=self.offlineMenu.addAction(self.tr("Show transports"))
		action.setCheckable(True)
		action.setObjectName('show_transports')
		if self.config['showTransports']=='True':
			action.setChecked(True)
		# make Toggle Invisibility QAction
		#self.toggleInv=self.offlineMenu.addAction(self.tr("Become invisible"))
		#self.toggleInv.setObjectName("toggle_invisible")
		# add resources connected to the same JID (selfResources)
		if len(self.selfResources)!=0:
			for resource in self.selfResources:
				menu=QtGui.QMenu(unicode(resource),self.offlineMenu)
				# resource supports adhoc commands
				if self.client.roster['users'][self.client.jid.userhost()].resources[resource].hasFeature('http://jabber.org/protocol/commands'):
					action=menu.addAction(self.tr("Commands"))
					action.setObjectName('commands')
					action.setData(QtCore.QVariant(unicode(resource)))
				# send file QAction
				action=menu.addAction(self.tr("Send file"))
				action.setObjectName('send_file')
				action.setData(QtCore.QVariant(unicode(resource)))

				self.offlineMenu.addMenu(menu)
			self.offlineMenu.addSeparator()

		self.ui.showOffline.setMenu(self.offlineMenu)
		QtCore.QObject.connect(self.offlineMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.offlineMenuChanged)

		# refresh selfAvatar tooltip, because some resource could be added
		self.ui.selfAvatar.refreshToolTip()

	def offlineMenuChanged(self,action):
		"""
		Executes command according to action.objectName(). Called when user choose one of QAction from self.offlineMenu, which si created by self.buildOfflineMenu().
		@type action: QAction
		@param action: QAction from self.offlineMenu
		"""
		cmd=unicode(action.objectName())
		if cmd=='commands':
			# show adhoc dialog
			self.cmds = widgets.commands.Commands(self, unicode(self.client.jid.userhost())+"/"+unicode(action.data().toString()))
			self.cmds.dialog.show()
		elif cmd=='send_file':
			jid=unicode(self.client.jid.userhost())+"/"+unicode(action.data().toString()) # make jid from users jid + selected resource
			file=QtGui.QFileDialog.getOpenFileNames(self,"Choose file") # get filenames
			file=list(file)
			if len(file)!=0:
				new=[]
				for f in file:
					new.append(unicode(f))
				file=new
				# show filetransfer dialog, which sends files
				self.dialog=widgets.filetransfer.filetransferDialog(self,file,jid)
				self.dialog.show()
		elif cmd=="show_transports":
			self.config['showTransports']=unicode(action.isChecked())
		elif cmd=="toggle_invisible":
			if self.toggleInv.text() == self.tr("Become invisible"):
				self.toggleInv.setText(self.tr("Become visible"))
				self.toggleInvisibility(True)
			else:
				self.toggleInv.setText(self.tr("Become invisible"))
				self.toggleInvisibility(False)


	def tables_created(self,data=None):
		"""
		Called on __init__ when new sqlite tables were created. If tables were empty, adds default values (default status messages etc.), otherwise calls self.buildStatusWidgetMenu().
		"""
		if not data[1][0]:
			self.buildStatusWidgetMenu()
			return
		print data
		t1=self.cache.set_status('online',self.tr("I'm here"))
		t2=self.cache.set_status('dnd',self.tr("Doing something important. Message me later."))
		t3=self.cache.set_status('chat',self.tr("Chat with me!"))
		t4=self.cache.set_status('xa',self.tr("Leave a message. Beep"))
		t5=self.cache.set_status('away',self.tr("Doing something else for a moment."))
		d=DeferredList([t1,t2,t3,t4,t5], consumeErrors = False)
		d.addCallback(self._defaultMsg).addErrback(self._error)

	def _defaultMsg(self, data):
		"""
		Called when default status message have been added. Calls self.buildStatusWidgetMenu().
		"""
		for x in data:
			if not x[0]:
				print x[1], dir(x[1])
		self.buildStatusWidgetMenu()

	def tables_loaded(self,data=None):
		"""
		Called when sqlite db has been loaded. Calls self.buildStatusWidgetMenu().
		"""
		print 'tables present'
		self.buildStatusWidgetMenu()

	def _error(self,result):
		"""
		Called if there was some error with using DB.
		"""
		log.msg( 'CHYBA V DATABAZI?!!! ')
		print result

	def buildTrayMenu(self):
		"""
		Builds system tray menu.
		"""
		menu=QtGui.QMenu(self)
		menu.addMenu(self.statusWidgetMenu)
		menu.addSeparator()
		action=menu.addAction(self.tr("Hide / Show"),self.trayActivated)
		menu.addAction(self.tr("Quit"),self.trayQuit)
		self.tray.setContextMenu(menu)

	def buildStatusWidgetMenu(self,data=None):
		"""
		Rebuilds (updates) status menu. Must be called without parametrs.
		"""
		if data==None:
			# get status messages from DB
			d=self.cache.get_status()
			d.addCallback(self.buildStatusWidgetMenu)
			d.addErrback(self._error)
			return
		else:
			# resort status messages
			config={}
			config['online']=[]
			config['offline']=[]
			config['chat']=[]
			config['away']=[]
			config['xa']=[]
			config['dnd']=[]
			for status in data:
				config[status[0]].append([status[1],str(status[2])])

		self.statusWidgetMenu=QtGui.QMenu(self.tr("Status"),self.ui.statusWidget)
		# make global menu. If some show has custom message, add seperator between last custom message and next show
		separator=False
		for key in ['online','chat','away','xa','dnd']:
			if separator and len(config[key])!=0:
				self.statusWidgetMenu.addSeparator()
			action=self.statusWidgetMenu.addAction(self.getIcon(status=key,size="16x16"),self.status[key])
			action.setData(QtCore.QVariant(key))
			if len(config[key])!=0:
				for val in config[key]:
					status=val[0]
					index=val[1]
					if len(status)>20:
						action=self.statusWidgetMenu.addAction(self.getIcon(status=key,size="16x16"),unicode(status)[:20]+"...")
					else:
						action=self.statusWidgetMenu.addAction(self.getIcon(status=key,size="16x16"),unicode(status))
					action.setData(QtCore.QVariant(key+"_"+unicode(index)))
				self.statusWidgetMenu.addSeparator()
				separator=False
			else:
				separator=True
		if separator:
			self.statusWidgetMenu.addSeparator()
		
		# make menu for transports
		if len(self.transports)!=0:
			for transport in list(self.transports.keys()):
				# make transports QMenu and use icon according to transports type and show
				show=self.client.roster['users'][transport].status
				if len(show)==0:
					show='offline'
				else:
					show=show[0]
				menu=QtGui.QMenu(transport,self.statusWidgetMenu)
				menu.setIcon(self.getIcon(status=show,size="16x16"))
				# add custom messages and shows QActions to the transports QMenu
				# it's the same code (principle) as above, but it uses different QAction.data(),
				# so we can recognize if user wants to send presence to the transport instead of server
				separator=False
				for key in ['online','chat','away','xa','dnd']:
					if separator and len(config[key])!=0:
						menu.addSeparator()
					action=menu.addAction(self.getIcon(status=key,size="16x16"),self.status[key])
					action.setData(QtCore.QVariant([key,unicode(transport)]))
					if len(config[key])!=0:
						for val in config[key]:
							status=val[0]
							index=val[1]
							if len(status)>20:
								action=menu.addAction(self.getIcon(status=key,size="16x16"),unicode(status)[:20]+"...")
							else:
								action=menu.addAction(self.getIcon(status=key,size="16x16"),unicode(status))
							# [show_idOfMessage,jidOfTransport]
							action.setData(QtCore.QVariant([key+"_"+unicode(index),unicode(transport)]))
						menu.addSeparator()
						separator=False
					else:
						separator=True
				if separator:
					menu.addSeparator()
				# We have to use status icon from previous instance of QMenu,
				# because transport doesn't need to have the same show in roster as we send him before
				# So FE we sent away, but in roster we have still online...
				if self.transports[transport]:
					menu.setIcon(self.transports[transport].icon())
				# updates transport menu in self.transports and add it to the self.statusWidgetMenu
				self.transports[transport]=menu
				self.statusWidgetMenu.addMenu(menu)
			self.statusWidgetMenu.addSeparator()

		# other actions
		action=self.statusWidgetMenu.addAction(self.getIcon(status="online",size="16x16"),self.tr("Add message"))
		action.setData(QtCore.QVariant("custom_message"))
		action=self.statusWidgetMenu.addAction(self.getIcon(status="online",size="16x16"),self.tr("Manage messages"))
		action.setData(QtCore.QVariant("manage_messages"))
		action=self.statusWidgetMenu.addAction(self.getIcon(status="offline",size="16x16"),self.tr("Log out"))
		action.setData(QtCore.QVariant("offline"))

		self.ui.statusWidget.setMenu(self.statusWidgetMenu)
		app.connect(self.statusWidgetMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.statusWidgetChanged)
		self.buildTrayMenu()

	def statusWidgetChanged(self,action):
		"""
		Executes command according to action.objectName(). Called when user choose one of QAction from self.statusWidgetMenu, which si created by self.buildStatusWidgetMenu().
		@type action: QAction
		@param action: QAction from self.statusWidgetMenu. if QAction.data() is string, presence is sent to the server or one of other commands is executed. If it's list, then it's in format [show,JID] and presence is sent to the JID. Show is in format "show_idOfStatusMessage" or just "show".
		"""
		data=action.data()
		if len(data.toList())==0:
			# We are sending presence to the server
			data=unicode(data.toString())
			jid=None
		else:
			# We are sending presence to the transport
			data=data.toList()
			jid=unicode(data[1].toString())
			data=unicode(data[0].toString())

		if data=='custom_message':
			# show 'add custom message' dialog
			cs = widgets.statuseditor.statusWidgetWindow(None,self,self)
			cs.exec_()
		elif data=='manage_messages':
			# show 'manage messages' dialog
			cs = widgets.statuseditor.statusEditorWindow(self,self)
			cs.exec_()
		else:
			data=data.split("_")
			if len(data)==2:
				# get statusMessage according to ID and call self._gotStatus when we have it
				show=data[0]
				messageIndex=data[1]
				d=self.cache.get_status_by_id(str(messageIndex))
				d.addCallback(self._gotStatus,jid)
				return
			elif len(data)==1:
				show=data[0]
				message=""
			# send presence
			self.sendPresence(jid,show,message)

	def _gotStatus(self,result,jid):
		"""
		Called from self.statusWidgetChange when we got statusMessage. Sends presence with message from result to JID.
		"""
		if not result:
			return
		if len(result)==0:
			return
		self.sendPresence(jid,result[0][0],result[0][1])

	def sendPresence(self,jid,show,message="",pri=None):
		"""
		Sends presence and update GUI.
		@type jid: unicode
		@param jid: JID or None for sending presence to server
		@type show: unicode
		@param show: String from this list: ["online","chat","away","xa","dnd","offline"]
		@type message: unicode
		@param message: Status message
		@type pri: integer
		@param pri: Priority
		"""
		print "sending presence",jid,show
		if not jid:
			# global presence => presence will be send to server
			if show=="offline":
				self.client.sendPresence(typ = "unavailable", status = unicode(message))
				self.client.factory.stopTrying()
				self.reconnect = False
				self.client.disconnect()
				self._disconnect()
			else:
				if not pri:
					# get priority from config
					if self.config.has_key('autoPriority'):
						if self.config['autoPriority']=='True':
							#priors={"chat":"25","online":"20","away":"15","xa":"10","dnd":"5"}
							#'autoPriority_chat','autoPriority_online','autoPriority_away','autoPriority_xa','autoPriority_dnd'
							
							pri=str(self.config["autoPriority_"+str(show)])
						else:
							if self.config.has_key('priority'):
								pri=self.config['priority']
							else:
								pri="0"
					else:
						if self.config.has_key('priority'):
							pri=self.config['priority']
						else:
							pri="0"
				self.selfStatus=show
				# update tray icon
				self.tray.setIcon(self.getCurrentTrayIcon())
				
				# send presence to the server
				self.client.sendPresence(show = unicode(show), status = unicode(message),priority=pri)
				
				# send presence to groupchats
				for muc in self.client.groupchats.itervalues():
					self.client.sendPresence(show = unicode(show), status = unicode(message), to = '%s/%s'%(muc.jid, muc.nick))
				
				# update statusWidget
				if len(message)>20:
					self.ui.statusMessage.setText(unicode(message)[:20]+"...")
				elif len(message)==0:
					self.ui.statusMessage.setText(self.status[show])
				else:
					self.ui.statusMessage.setText(unicode(message))
				self.ui.statusMessage.setIcon(self.getIcon(status=show,size="16x16"))
		else:
			# update transport's icon in statusWidgetMenu
			if self.transports.has_key(jid):
				if self.transports[jid]!=None:
					self.transports[jid].setIcon(self.getIcon(status=unicode(show),size="16x16"))
			# send presence
			self.client.sendPresence(to=jid,show = unicode(show), status = unicode(message),priority=pri)

	def profileChanged(self,jid):
		"""
		Changes profile. Called when user changes profile in Login Window. Profile can be changed only if Jabbim is not connected.
		@type jid: unicode
		@param jid: profiles Jabber ID
		"""
		self.homeDir=unicode(self.realHomeDir+"/"+jid+"-profile") # get new homedir
		utils.loadConfig(self,[]) # load profiles config
		# change log files
		if self.config['log'] == 'true':
			logfile = open(self.homeDir+'/'+self.config['logfile'], 'w')
			start=True
			if self.log:
				start=False
				log.removeObserver(self.log.emit)
			self.log=log.FileLogObserver(logfile)
			log.addObserver(self.log.emit)
			if start:
				log.startLoggingWithObserver(self.log.emit, setStdout=0)
		# change GUI according to new config
		self.fillLoginForm()
		self.loadTheme()
		self.ui.roster.reskin()
		# change cache
		if self.cache:
			self.cache.close()
			del self.cache
		if sys.platform != 'win32':
			self.cache = storage.Cache(db=utils.path(self.homeDir+u'/cache.db'))
		else:
			self.cache = storage.Cache(db=(unicode(self.homeDir)+u'/cache.db').encode('utf8')) #hack!

	def fillLoginForm(self):
		"""
		Fill login form according to config file and existing profiles
		"""
		profiles=utils.getProfiles(self.realHomeDir)
		
		# show profiles only if their count is more than 1
		if len(profiles)<=1:
			self.ui.profilesList.hide()
			self.ui.profilesLine.hide()
			self.ui.profilesHeader.hide()
		else:
			self.ui.profilesList.show()
			self.ui.profilesLine.show()
			self.ui.profilesHeader.show()

		# update profiles QComboBox
		if self.ui.profilesList.count()!=len(profiles):
			QtCore.QObject.disconnect(self.ui.profilesList, QtCore.SIGNAL("currentIndexChanged ( const QString & )"),self.profileChanged)
			self.ui.profilesList.clear()
			for profile in profiles:
				jid=profile.replace('-profile','')
				# load profile avatar
				if os.path.isfile(self.realHomeDir+"/"+profile+"/avatars/"+unicode(jid)):
					avatar=QtGui.QPixmap(self.realHomeDir+"/"+profile+"/avatars/"+unicode(jid)).scaled(22,22,QtCore.Qt.KeepAspectRatio)
					result=QtGui.QPixmap(22,22)
					result.fill(QtCore.Qt.transparent)
					painter=QtGui.QPainter(result)
					painter.drawPixmap((22-avatar.width())/2,(22-avatar.height())/2,avatar)
					painter.end()
					result=QtGui.QIcon(result)
				else:
					result=QtGui.QIcon("images/22x22/apps/jabbim.png")

				if self.config['jid']==jid:
					self.ui.profilesList.insertItem(0,result,jid)
				else:
					self.ui.profilesList.addItem(result,jid)
			self.ui.profilesList.setCurrentIndex(0)
			QtCore.QObject.connect(self.ui.profilesList, QtCore.SIGNAL("currentIndexChanged ( const QString & )"),self.profileChanged)
		
		# fill login form
		self.ui.login_password.setText(rot13.scramble(self.config['passwd']))
		self.ui.login_jid.setText(self.config['jid'])
		if self.config['autoJoin']=="True":
			self.ui.login_autoconnect.setChecked(True)
		else:
			self.ui.login_autoconnect.setChecked(False)
		if self.config['savePasswd']=="True":
			self.ui.login_savePassword.setChecked(True)
		else:
			self.ui.login_savePassword.setChecked(False)
			self.ui.login_autoconnect.setEnabled(False)

		if os.path.isfile(self.homeDir+'/avatars/'+unicode(self.config['jid'])):
			pixmap=QtGui.QIcon(self.homeDir+'/avatars/'+unicode(self.config['jid']))
			avatar=pixmap.pixmap(100,112)
			if avatar.width()<=58 and avatar.height()<=58:
				size=64
			else:
				size=128
			result=QtGui.QPixmap(size,size)
			result.fill(QtCore.Qt.transparent)
			frame=QtGui.QPixmap("images/"+str(size)+"x"+str(size)+"/frame.png")
			painter=QtGui.QPainter(result)
			#painter.fillRect(0,0,size,size,QtGui.QBrush(self.ui.login.palette().color(QtGui.QPalette.Window)))
			painter.drawPixmap((size-avatar.width())/2,(size-avatar.height())/2,avatar)
			painter.drawPixmap(0,0,frame)
			painter.end()
			self.ui.loginAvatar.setPixmap(result)
		else:
			pixmap=QtGui.QIcon("images/48x48/apps/jabbim.png")
			avatar=pixmap.pixmap(128,112)
			if avatar.width()<=58 and avatar.height()<=58:
				size=64
			else:
				size=128
			result=QtGui.QPixmap(size,size)
			result.fill(QtCore.Qt.transparent)
			frame=QtGui.QPixmap("images/"+str(size)+"x"+str(size)+"/frame.png")
			painter=QtGui.QPainter(result)
			#painter.fillRect(0,0,size,size,QtGui.QBrush(self.ui.login.palette().color(QtGui.QPalette.Window)))
			painter.drawPixmap((size-avatar.width())/2,(size-avatar.height())/2,avatar)
			painter.drawPixmap(0,0,frame)
			painter.end()
			self.ui.loginAvatar.setPixmap(result)
		self.ui.loginAvatar.setMaximumSize(QtCore.QSize(size,size))
		self.ui.loginAvatar.setMinimumSize(QtCore.QSize(size,size))
		self.ui.loginAvatar.setAlignment(QtCore.Qt.AlignCenter)


	def registerButtonClicked(self):
		# depracted
		if USE_WIZARDS:
			self.regwiz=wizards.registration.registrationWizard(self,self)
			self.regwiz.show()
		return

	def getJid(self,jid):
		"""
		Returns Twisted Jabber ID or None if JID is in bad format.
		@type jid: unicode
		@param jid: profiles Jabber ID
		"""
		try:
			jidt=jidT.JID(jid)
		except:
			return None
		return jidt

	def serviceDiscovery(self,b):
		"""
		Shows Service Discovery Dialog. Called by QAction from main menu.
		"""
		self.discovery=widgets.servicediscovery.serviceDiscoveryDialog(self,self)
		self.discovery.show()

	def event(self,ev):
		# depracted
		# WindowActivated
		if int(ev.type())==24:
			if self.active!=True:
				self.active=True
				if self.client:
					self.client.dispatcher.publishEvent('onActivity')
				print "publishing onActivity event"
			self.ui.roster.setFocus(QtCore.Qt.MouseFocusReason)
			#self.timer.stop()
		elif int(ev.type())==25:
			if self.active:
				print "INACTIVE MAINWIN"
				self.active=False
				self.chat.timer.start(30000)
		return QtGui.QMainWindow.event(self,ev)

	def privacyListEditor(self,bool=False):
		"""
		Shows Privacy List Editor. Called by QAction from main menu.
		"""
		self.ple=widgets.privacy.PrivacyListEditorDialog(self,self)
		self.ple.show()

	def identityEditor(self,bool=False):
		"""
		Shows Vcard Editor. Called by QAction from main menu.
		"""
		self.ve=widgets.vcardeditor.vcardEditorDialog(self,self.client.jid.userhost(),self)
		self.ve.show()

	def mucBrowser(self,bool=False):
		"""
		Shows MUC Browser.
		"""
		if not self.mucbrowser:
			self.mucbrowser=widgets.mucbrowser.MUCBrowserDialog(self,self)
			self.mucbrowser.show()
		else:
			if self.mucbrowser.isHidden()==True:
				self.mucbrowser=widgets.mucbrowser.MUCBrowserDialog(self,self)
				self.mucbrowser.show()

	def about(self,bool):
		"""
		Shows About Jabbim dialog.
		"""
		about=aboutDialog(self)
		about.exec_()
	
	def sendCustomStatus(self, jid, show = None):
		cs = customStatusWindow(jid, show)
		cs.exec_()

	def showInvitation(self, jid, room, reason, cont = False):
		"""
		Shows invitation to room in events.
		@type jid: unicode
		@param jid: Jabber ID of user who sends invitation
		@type room: unicode
		@param room: Jabber ID of room
		@type reason: unicode
		@param reason: Reason
		@type cont: boolean
		@param cont: True if the invitation was sent to invite third person to the 1to1 chat (chat -> groupchat)
		"""
		log.msg("%s %s %s" %(jid, room, reason))

		maintext =unicode(jid)+self.tr(" invites you to conference ")+unicode(room)+"."
		if reason != None:
			maintext += "<br>" + self.tr("Reason: ") + unicode(reason)
		self.events.addLineEditEvent(maintext = maintext ,trueCall=self.joinGC, trueDict=[room], falseCall=self.client.declineInvitation, falseDict=[jid, room],header="Groupchat Invitation",text="Nickname:",name=unicode(jid),typ="groupchatInvitation",icon=None,action=None,actionDict=None,height=150,value=self.client.jid.userhost().split("@")[0])

	def findPlugins(self):
		"""
		Finds plugins in plugins/ and ~/plugins and saves informations about them to the self.plugins
		"""
		if len(self.plugins) != 0:
			return  # we've done this already
		plugin_paths = ['plugins/', self.homeDir + '/plugins/']
		for plugin_path in plugin_paths:
			for plugin_name in os.listdir(plugin_path):
				if plugin_name == '.svn':
					continue
				dir = '%s/%s' % (plugin_path, plugin_name)
				path = '%s/%s.py' % (dir, plugin_name)

				try:
					f=open(utils.path(path))
					plug = load_source(plugin_name, path, f).Plugin(False, self.homeDir, dir)
					version = float(plug.version)
				except Exception, ex:
					log.msg(path+': BAD PLUGIN!')
					message = unicode(traceback.format_exc(), 'utf-8')
					log.msg(message)
					continue

				if not self.plugins.has_key(plugin_name) or version > self.plugins[plugin_name]['version']:
					self.plugins[plugin_name] = { 'dir': dir, 'version': version, 'module': None }

	def loadPlugins(self):
		"""
		Loads plugins according to config file (self.config['plugins'])
		"""
		for plugin_name in self.plugins.keys():
			if plugin_name in self.config['plugins']:
				try:
					self.loadPlugin(plugin_name)
				except Exception, ex:
					log.msg(plugin+': '+unicode(ex))
		#log.msg("PLUGINS:"+unicode(self.plugins))
	
	def runPluginCommand(self,command,args):
		"""
		Safely runs plugins command.
		@type command: pointer to function
		@param command: pointer to plugins function
		@type args: list
		@param args: list of arguments for function
		"""
		try:
			ret=command(*args)
			return ret
		except Exception, ex:
			log.msg('Plugin error: ' +unicode(ex))
			message = unicode(traceback.format_exc())
			log.msg(message)
	
	def loadPlugin(self,plugin):
		"""
		Loads plugin. Plugin is loaded to the self.plugins[name]['module'].
		@type plugin: unicode
		@param plugin: plugins name
		"""
		dir = self.plugins[plugin]['dir']
		path = utils.path('%s/%s.py' % (dir, plugin))
		log.msg("loading "+unicode(plugin)+" plugin...")
		try: 
			f=open((path))
		except:
			log.msg('plugin load error: '+plugin)
			return
		try:
			if not self.plugins[plugin]['module']:
				plug = load_source(plugin, path, f).Plugin(self, self.homeDir, dir) # load plugin module
				self.plugins[plugin]['module'] = plug 
				self.runPluginCommand(self.plugins[plugin]['module'].buildRosterMenu,[]) # build menu for plugin
			else:
				print "plugin already loaded"
			f.close()
		except Exception, ex:
					#log.msg(unicode(plugin)+u': '+unicode(ex))
					traceback.print_exc()
					f.close()
					pass
		log.msg("PLUGINS:"+unicode(self.plugins))

	def unloadPlugin(self,plugin):
		"""
		Unloads plugin. Plugin module is deleted and self.plugins[plugin]=None
		@type plugin: unicode
		@param plugin: plugins name
		"""
		if self.plugins[plugin]['module']:
			self.ui.menuPlugins.clear() # clear plugins menu
			self.runPluginCommand(self.plugins[plugin]['module'].remove,[]) # inform plugin that it will be removed
			self.plugins[plugin]['module'] = None
			del gc.garbage[:] # delete plugin from python
			# rebuild plugins menu
			for plug in self.plugins.itervalues():
				if plug['module']:
					self.runPluginCommand(plug['module'].buildRosterMenu,[])
		else:
			print "plugin is not loaded:",plugin
		log.msg("PLUGINS:"+unicode(self.plugins))

	def closeEvent(self,event):
		"""
		Hides window to the tray or quit if tray is not visible. Called by WM when windows is closed.
		"""
		print "TRAY VISIBLE MAIN:"+unicode(self.tray.isVisible())
		if self.tray.isVisible():
			self.hide()
			event.accept()
			return
		self.trayQuit()
		event.accept()

	def trayQuit(self,bool=True):
		"""
		Exits Jabbim.
		"""
		if self.client and self.client.privacy.active:
			self.client.privacy.active.unsetInvisible(available=False) # hack
		if os.path.isfile(self.config.filename):
			# save windows geometry and sizes of splitters in chat window
			if str(self.config["saveGeometry"])=="True":
				rect=self.geometry()
				x=int(rect.x())
				y=int(rect.y())
				width=int(rect.width())
				height=int(rect.height())
				self.config["windowGeometry"]=[x,y,width,height]
				rect=self.chat.geometry()
				x=int(rect.x())
				y=int(rect.y())
				width=int(rect.width())
				height=int(rect.height())
				self.config["chatGeometry"]=[x,y,width,height]
				for i in range(self.chat.ui.chatTab.count()):
					w=self.chat.ui.chatTab.widget(i)
					if w.typ=="chat":
						self.config['chatSplitterSizes']=list(w.chat.ui.splitter.sizes())
						self.config['chatSplitter2Sizes']=list(w.chat.ui.splitter_2.sizes())
						break
				for i in range(self.chat.ui.chatTab.count()):
					w=self.chat.ui.chatTab.widget(i)
					if w.typ=="groupchat":
						self.config['groupchatSplitSizes1']=list(w.chat.ui.splitter.sizes())
						self.config['groupchatSplitSizes2']=list(w.chat.ui.splitter_2.sizes())
						self.config['groupchatSplitSizes3']=list(w.chat.ui.splitter_3.sizes())
	
						break
				self.config.write()
			# save expanded groups
			if str(self.config['saveExpandedGroups'])=='True':
				expanded=[]
				if self.client!=None:
					for name,item in self.client.roster['groups'].iteritems():
						if item.expanded==True:
							expanded.append(name)
					self.config['expandedGroups']=expanded
					self.config.write()
		# save config to the ~/.jabbim/
		# we cat detect last loged user (=> last used profile) from it
		f=open(self.realHomeDir+"/config",'w')
		self.config.write(f)
		f.close()
		# close windows, hide tray :)
		app.closeAllWindows()
		self.tray.hide()
		# stop reactor
		reactor.stop2()

	def trayActivated(self,reason=QtGui.QSystemTrayIcon.Trigger):
		"""
		Shows or hides mainWindow. Called when is tray activated.
		"""
		if reason==QtGui.QSystemTrayIcon.Trigger:
			if not self.events.trayClicked():
				if self.isHidden():
					self.show()
					self.raise_()
					self.activateWindow()
					self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
					self.ui.roster.setFocus(QtCore.Qt.MouseFocusReason)
				else:
					if self.windowState() & QtCore.Qt.WindowMinimized:
						self.show()
						self.raise_()
						self.activateWindow()
						self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
						self.ui.roster.setFocus(QtCore.Qt.MouseFocusReason)
					else:
						self.hide()
		elif reason==QtGui.QSystemTrayIcon.MiddleClick:
			self.ui.tabWidget.setCurrentIndex(2)
			if self.isHidden():
				self.show()
				self.raise_()
				self.activateWindow()
				self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
				self.ui.roster.setFocus(QtCore.Qt.MouseFocusReason)
			else:
				if self.windowState() & QtCore.Qt.WindowMinimized:
					self.show()
					self.raise_()
					self.activateWindow()
					self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
					self.ui.roster.setFocus(QtCore.Qt.MouseFocusReason)
				else:
					self.hide()

	def loadTheme(self,text=None):
		"""
		Loads theme. If text==None, self.config['theme'] is used. Otherwise is stylesheet sets to `text`.
		@type text: unicode
		@param text: stylesheet css
		"""
		self.setStyleSheet("") # windows hack
		
		if self.config['theme']=="None" and not text:
			# theme isn't used
			text=""
			self.ui.roster.theme=False
		else:
			self.ui.roster.theme=True
		if text==None:
			# open theme according to self.config
			theme=open("themes/"+self.config['theme']+"/style.css")
			text=theme.read()
			self.setStyleSheet(text)
			self.xmlConsole.setStyleSheet(text)
			self.chat.setStyleSheet(text)
			theme.close()
		else:
			# use text for stylesheet css
			self.setStyleSheet(text)
			self.xmlConsole.setStyleSheet(text)
			self.chat.setStyleSheet(text)
			if text:
				if len(text)==0:
					self.ui.roster.theme=False
		self.styleSheetText=text
		self.ui.roster.reskin(text) # reskin roster

	def addContactMainWindow(self):
		"""
		Shows Add Contact Dialog.
		"""
		if not self.addcontactdialog:
			self.addcontactdialog=widgets.addcontact.addContactDialog(self,self)
			self.addcontactdialog.show()
		else:
			if self.addcontactdialog.isHidden()==True:
				self.addcontactdialog=widgets.addcontact.addContactDialog(self,self)
				self.addcontactdialog.show()

	def bookmarksClicked(self,item,i):
		"""
		Joins MUC when user clicked on bookmark in Bookmarks tab.
		"""
		data=item.data(0,32)
		lst=data.toList()
		jid=unicode(lst[0].toString()) # get jid
		nickname=unicode(lst[1].toString()) # get nickname
		# send jabber command
		if self.chat.addGroupChatTab(jid,nickname):
			#self.main.groupchat[room+"@"+server]=[nickname,[]]
			self.client.joinGC(jid, nickname)

	def buildBookmarks(self):
		"""
		Adds bookmarks items to self.ui.bookmarks (QTreeWidget)
		"""
		self.ui.bookmarks.clear()
		for k,v in self.client.bookmarks['conference'].iteritems():
			# add bookmark to the bookmarks list
			item=QtGui.QTreeWidgetItem(self.ui.bookmarks)
			item.setText(0,unicode(v.name))
			item.setText(1,unicode(v.jid.full()))
			item.setData(0,32,QtCore.QVariant([unicode(v.jid.full()),unicode(v.nick),unicode(v.password)]))
			item.setIcon(0,QtGui.QIcon("images/16x16/categories/muc.png"))

	def joinGC(self,jid,nickname):
		"""
		Joins to groupchat.
		@type jid: unicode
		@param jid: Groupchats Jabber ID
		@type nickname: unicode
		@param nickname: users nickname
		"""
		if self.chat.addGroupChatTab(jid,nickname):
			self.client.joinGC(jid, nickname)

	def autoJoinGroupchat(self):
		"""
		Joins to groupchats which have autojoin flag.
		"""
		for k,v in self.client.bookmarks['conference'].iteritems():
			if (v.autojoin==True or unicode(v.autojoin).lower()=="true") or (v.autojoin==1 or v.autojoin=="1"):
				jid=unicode(v.jid.full())
				nickname=v.nick
				if self.chat.addGroupChatTab(jid,nickname):
					self.client.joinGC(jid, nickname)

	def joinGroupchat(self,bool):
		"""
		Called when user activate Join Groupchat QAction from main menu.
		"""
		#self.mucBrowser(bool)
		if USE_WIZARDS:
			self.joingroupchatwizard=wizards.joingroupchat.joinGroupchatWizard(self,self)
			self.joingroupchatwizard.show()


	def deleteCurrentBookmark(self):
		"""
		Deletes currently selected bookmark.
		"""
		item=self.ui.bookmarks.currentItem()
		if item:
			del self.client.bookmarks['conference'][unicode(item.text(0))]
			self.client.setBookmarks()
			self.buildBookmarks()

	def bookmarksContextMenu(self,pos):
		"""
		Makes bookmarks context menu. Called when user right-click on bookmark.
		"""
		# make groupchat bookmarks menu
		item=self.ui.bookmarks.itemFromIndex(self.ui.bookmarks.indexAt(pos)) # get selected item
		jid=unicode(item.text(1)) # get item jid
		menu=QtGui.QMenu(self.ui.bookmarks) # make menu
		if item.parent()==None:
			# Join bookmarked groupchat
			action=menu.addAction(self.tr("Join"))
			action.setData(item.data(0,32))
			action.setObjectName("join_bookmark")
			action=menu.addAction(self.tr("User list"))
			action.setData(item.data(0,32))
			action.setObjectName("show_users")
			# separator
			menu.addSeparator()
			# Edit bookmark
			action=menu.addAction(self.tr("Edit bookmark"))
			action.setData(item.data(0,32))
			action.setObjectName("edit_bookmark")
			# Delete bookmark
			action=menu.addAction(self.tr("Delete bookmark"))
			action.setData(item.data(0,32))
			action.setObjectName("delete_bookmark")

		menu.connect(menu, QtCore.SIGNAL("triggered ( QAction * )"),self.groupchatContextMenuTriggered)
		menu.popup(self.ui.bookmarks.mapToGlobal(pos))

	def groupchatContextMenuTriggered(self,action):
		"""
		Executes command according to action.objectName(). Called when user choose one of QAction from bookmarks menu.
		@type action: QAction
		@param action: QAction from bookmarks menu
		"""
		cmd=action.objectName()
		if cmd=="join":
			# join groupchat from Groupchats list
			jid=action.data() # get jid
			jid=unicode(jid.toString())
			room=jid.split("@")[0] # get room
			server=jid.split("@")[1] # get server
			# show join groupchat dialog
			newchat=joinGroupChatWindow(self,room=room,server=server)
			ret=newchat.exec_()
		elif cmd=="join_bookmark":
			# join bookmarked groupchat
			data=action.data()
			lst=data.toList()
			jid=unicode(lst[0].toString()) # get jid
			nickname=unicode(lst[1].toString()) # get nickname
			# send jabber command
			if self.chat.addGroupChatTab(jid,nickname):
				self.client.joinGC(jid, nickname)
		elif cmd=="edit_bookmark":
			item=self.ui.bookmarks.currentItem()
			data=action.data()
			lst=data.toList()
			jid=unicode(lst[0].toString()) # get jid
			if len(jid.split("@"))!=1:
				room=jid.split("@")[0]
				server=jid.split("@")[1]
			else:
				room=jid
			name=unicode(item.text(0))
			nickname=unicode(lst[1].toString()) # get nickname
			password=unicode(lst[2].toString()) # get password
			autojoin=self.client.bookmarks['conference'][name].autojoin
			if password=="None":
				password=""
			edit=widgets.preferences.editBookmark(self,room,server,name,nickname,password,autojoin,self)
			edit.exec_()
		elif cmd=="delete_bookmark":
			item=self.ui.bookmarks.currentItem()
			#self.ui.bookmarks.takeTopLevelItem(self.ui.bookmarks.indexOfTopLevelItem(item))
			del self.client.bookmarks['conference'][unicode(item.text(0))]
			self.client.setBookmarks()
			self.buildBookmarks()
		elif cmd=="show_users":
			item=self.ui.bookmarks.currentItem()
			if int(item.childCount())!=0:
				# delete all users in groupchat
				for i in range(item.childCount()):
					item.takeChild(0)
			# set item expanded
			self.ui.bookmarks.setItemExpanded(item,True)
			self.client.getDiscoItems(unicode(item.text(1)),callback=self.client.on_discoItemsBookmarksReceived,callback_par=unicode(item.text(1)))

	def bookmarksItemClicked(self,item,i):
		if item.isExpanded():
			self.ui.bookmarks.collapseItem(item)
		else:
			self.ui.bookmarks.expandItem(item)

	def bookmarksCurrentChanged(self,item,old):
		if item != None and item.parent()==None:
			self.client.getDiscoItems(unicode(item.text(1)),callback=self.client.on_discoItemsBookmarksReceived,callback_par=unicode(item.text(1)))

	def profilesClicked(self,bool):
		if not self.profilesWindow:
			self.profilesWindow=widgets.profiles.profilesWindow(self,self)
			self.profilesWindow.show()
		else:
			if self.profilesWindow.isHidden()==True:
				self.profilesWindow=widgets.profiles.profilesWindow(self,self)
				self.profilesWindow.show()

	def preferencesClicked(self,bool):
		if self.preferencesWindow.isHidden()==True:
			self.preferencesWindow.show()
			self.preferencesWindow.reloadPreferences()

	def loadJabbimExtraConfig(self,config,fallback):
		try:
			config=ConfigObj(config,encoding='UTF8')
			return True,config
		except:
			config=ConfigObj(fallback,encoding='UTF8')
			return False,config

	def loadSkin(self):
		"""
		Loads chat skin. Skin is loaded to self.skin.
		"""
		self.skin=ConfigObj("chatskins/"+self.config["chatSkin"],encoding='UTF8')
		if len(self.skin)==0:
			self.skin=ConfigObj(self.realHomeDir+"/chatskins/"+self.config["chatSkin"],encoding='UTF8')
		self.skin=self.skin['chatskin']
		if not self.skin.has_key("spaces_between_lines"):
			self.skin["spaces_between_lines"]='0'
	
	def getSkinColors(self,i):
		"""
		Returns colors from chat skins. This is useful for using different colors for different nicknames in Groupchat.
		Every user in groupchat have his own ID and according to ID is choosen one color.
		@type i: integer
		@param i: ID of user (color)
		@rtype: list
		@return: list of colors [#000000,#FFFFFF,#EFEFEF]
		"""
		colors=[]
		for key,value in self.skin.iteritems():
			if key.startswith("color"):
				colors.append(value)
		if len(colors)==0:
			return None
		if len(colors)==1:
			return colors[0]
		if i>len(colors)-1:
			return colors[i%(len(colors)-1)]
		else:
			return colors[i]

	def now(self):
		"""
		Returns current time in format hh:mm:ss
		@rtype: unicode
		@return: current time in format hh:mm:ss
		"""
		h,m,s=time.localtime()[3:6]
		return "%02d:%02d:%02d" % (h,m,s)

	def showXml(self,bool):
		self.xmlConsole.show()

	def hideOffline(self,bool):
		"""
		Hides or shows offline users
		@type bool: boolean
		@param bool: True == offline users are shown, False offline users are hidden
		"""
		self.events.addAddUserEvent('hanzz@njs.netlab.cz','offline users are shown, False offline users are hidden')
		self.offline=not bool
		self.ui.roster.showOffline=bool
		self.ui.roster.reshow=True
		if self.ui.roster.item:
			if self.ui.roster.item.typ=="user":
				if int(self.ui.roster.item.status)==9 and not bool:
					self.ui.roster.statusLabel.hide()
		self.ui.roster.sortItems()
		self.ui.roster.repaint()

	def toggleInvisibility(self, bool):
		# depracted these days because ejabberd doesn't support invisibility (there are bugs fixed in svn)
		# Should be ok these days :-)
		if self.client.privacy.active:
			if bool:
				self.client.privacy.active.setInvisible()
				for gc in self.client.groupchats.keys():
					tab, indextab = self.chat.findTab(gc)
					self.ui.chatTab.removeTab(indextab)
			else:
				self.client.privacy.active.unsetInvisible()

	def loadRoster(self):
		"""
		Loads roster widget.
		"""
		layout=QtGui.QHBoxLayout(self.ui.rosterWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.scroll=scrollBar(self.ui.rosterWidget)
		self.scroll.setWidgetResizable (True)
		self.ui.roster=widgets.rosterLiveWidget.rosterWidget(self,self)
		self.scroll.setWidget(self.ui.roster)
		layout.addWidget(self.scroll)

	def _connected(self):
		"""
		Shows roster, changes tray icon, enable menu items etc... Called by Pyxl when we are connected.
		"""
		print 'connected in main'
		self.ui.roster.reskin()
		self.ui.actionAdd_Contact.setEnabled(True)
		self.ui.actionJoin_groupchat.setEnabled(True)
		self.ui.actionService_Discovery.setEnabled(True)
		self.ui.selfName.setText("<h3>"+unicode(self.client.jid.userhost()).split("@")[0]+"</h3>")
		self.client.getVCard(unicode(self.client.jid.userhost()))
		self.ui.showOffline.show()
		self.tray.showMessage(self.tr("Jabbim"),self.tr("Jabbim is ready! You are connected! :) "))
		self.tray.setIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))
		print 'end connected in main'

	def disconnect(self):
		"""
		Stops reactor
		"""
		#if self.client!=None:
		reactor.stop2()

	def getAvatar(self,pixmap,size="auto",frame=False,status=None):
		"""
		Returns avatar of contact.
		@type pixmap: unicode or QtGui.QIcon or QtGui.QPixmap
		@param pixmap: unicode - Jabber ID of contact with "@" replaced with "%";
		@type size: unicode
		@param size: auto, 16x16, 32x32, 64x64, 128x128
		@type frame: boolean
		@param frame: True - Frame is painted around the avatar.
		@type status: unicode or None
		@param status: String from this list: ["online","chat","away","xa","dnd","offline"]. Status icon will be painted to the corner.
		@rtype: QtGui.QPixmap
		@return: avatar
		"""
		if not pixmap:
			return None
		if isinstance(pixmap,unicode) or isinstance(pixmap,str):
			file=self.homeDir+'/avatars/'+unicode(pixmap)
			if not os.path.isfile(file):
				return None
			icon=QtGui.QIcon(file)
		elif isinstance(pixmap,QtGui.QPixmap):
			icon=QtGui.QIcon(pixmap)
		else:
			icon=pixmap
		if size!="auto":
			x=int(size.split('x')[0])
			y=int(size.split('x')[1])
		
		if frame and size!='auto':
			if size=="128x128":
				avatar=icon.pixmap(100,100)
				if avatar.width()<=50 and avatar.height()<=50:
					size="64x64"
				x=int(size.split('x')[0])
				y=int(size.split('x')[1])
			elif size=="64x64":
				avatar=icon.pixmap(50,50)
			elif size=="32x32":
				avatar=icon.pixmap(25,25)
			else:
				return False
	
			result=QtGui.QPixmap(x,y)
			result.fill(QtCore.Qt.transparent)
			if os.path.exists("themes/"+self.config['theme']+"/frame-"+str(size)+".png"):
				frame=QtGui.QPixmap("themes/"+self.config['theme']+"/frame-"+str(size)+".png")
			else:
				frame=QtGui.QPixmap("images/"+str(size)+"/frame.png")
			painter=QtGui.QPainter(result)
			painter.drawPixmap((x-avatar.width())/2,(y-avatar.height())/2,avatar)
			painter.drawPixmap(0,0,frame)
			painter.end()
		elif size!="auto" and not frame:

			if size=="128x128":
				avatar=icon.pixmap(100,100)
				if avatar.width()<=50 and avatar.height()<=50:
					size="64x64"
				x=int(size.split('x')[0])
				y=int(size.split('x')[1])
			elif size=="64x64":
				avatar=icon.pixmap(50,50)
			elif size=="32x32":
				avatar=icon.pixmap(25,25)
			else:
				return False

			result=QtGui.QPixmap(x,y)
			result.fill(QtCore.Qt.transparent)
			painter=QtGui.QPainter(result)
			painter.drawPixmap((x-avatar.width())/2,(y-avatar.height())/2,avatar)
			if status:
				icon=self.getIcon(status=unicode(status),size="16x16")
				if icon:
					painter.drawPixmap(16,16,icon.pixmap(16,16))
			painter.end()
		elif size=="auto" and not frame:
			return QtGui.QPixmap(file)
			
		return result

	def getCurrentTrayIcon(self):
		"""
		Returns current tray icon according to show.
		@rtype: QtGui.QIcon
		@return: current tray icon
		"""
		icon=QtGui.QIcon("images/16x16/apps/jabbim.png")
		if self.selfStatus!='online':
			result=icon.pixmap(16,16)
			painter=QtGui.QPainter(result)
			icon=self.getIcon(status=unicode(self.selfStatus),size="16x16")
			painter.drawPixmap(0,0,icon.pixmap(16,16))
			painter.end()
		else:
			result=icon
		return QtGui.QIcon(result)

	def getIcon(self,jid=None,typ=None,size="32x32",status=None,usertype=None):
		"""
		Returns status icon.
		@type jid: unicode
		@param jid: Jabber ID
		@type size: unicode
		@param size: 16x16 or 32x32
		@type status: unicode
		@param status: String from this list: ["online","chat","away","xa","dnd","offline"]
		@rtype: QtGui.QIcon
		@return: status icon
		"""
		if size=="22x22":
			size="32x32"
		# return status icon
		#print "geticon",jid,typ,size,status,usertype
		path=self.statusPath.replace("xxxxx",size)
		typ=unicode(typ)
		
		if usertype!=None:
			file=path+usertype+"-online.png"
			if os.path.exists(file):
				icon=QtGui.QIcon(file)
				return icon
		
		if status==None:
			status=self.icons[self.shows[typ]]
		if jid!=None:
			#file=path+self.getUserType(jid)+"-"+self.icons[self.show[typ]]+".png"
			if len(jid.split("@"))>1:
				host=jid.split("@")[1]
			else:
				host=None
			if self.hosts.has_key(host):
				usertype=self.hosts[host]
				file=path+usertype+"-"+status+".png"
				if os.path.exists(file):
					icon=QtGui.QIcon(file)
				else:
					#print "File not exist",file," <-",jid,typ
					#print "using",path+"jabber-"+self.icons[self.shows[status]]+".png"
					icon=QtGui.QIcon(path+"jabber-"+self.icons[self.shows[status]]+".png")
			else:
				#print "using",path+"jabber-"+self.icons[self.shows[status]]+".png"
				icon=QtGui.QIcon(path+"jabber-"+self.icons[self.shows[status]]+".png")
		else:
			if status==None:
				icon=QtGui.QIcon(path+"jabber-online.png")
			else:
				icon=QtGui.QIcon(path+"jabber-"+status+".png")
		return icon

	def newProfile(self,jid,password,savePassword):
		self.homeDir=self.realHomeDir+"/"+jid+"-profile"
		#if not os.path.isdir(self.homeDir):
			#os.mkdir(self.homeDir)
		utils.makeHomeDir(self.homeDir)
		f=open(self.homeDir+"/config",'w')
		self.config.write(f)
		f.close()
		utils.loadConfig(self,[]) # load config files
		self.config['savePasswd']=unicode(savePassword)
		if savePassword==True:
			self.config['passwd']=rot13.scramble(password)
		else:
			self.config['passwd']=""
		self.config['jid']=jid
		self.config.write()

	def connectCancel(self):
		print "DISCONNECT"
		if self.client:
			if self.client.factory:
				self.client.factory.stopTrying()
		self.reconnect = False
		if self.client:
			self.client.disconnect()
		self._disconnect()

	def connect(self):
		# Connect to the server
		jid=unicode(self.ui.login_jid.text()) 
		if not re.match(r'.+@.+', jid): 
			self.ui.login_jid.setFocus(QtCore.Qt.OtherFocusReason) 
			if jid.find('@') == -1: 
				self.ui.login_jid.setText(jid + '@') 
			return 
		if len(unicode(self.ui.login_password.text())) == 0:
			return
		self.ui.rosterStackedWidget.setCurrentIndex(2)
		self.ui.login_connect.setEnabled(False)
		self.ui.profilesList.setEnabled(False)
		#if not os.path.isfile(self.main.homeDir+'/lastxml':
		reactor.callLater(0.1,self.connect__)
	
	def connect__(self):
		jid=unicode(self.ui.login_jid.text())
		password=unicode(self.ui.login_password.text())
		self.ui.loginInfo.setText(self.tr("Connecting to the server..."))
		profiles=utils.getProfiles(self.realHomeDir)
		if len(jid)!=0 and len(jid.split("@"))==2 and len(password)!=0:
	
			if jid+"-profile" in profiles:
				self.homeDir=self.realHomeDir+"/"+jid+"-profile"
				utils.loadConfig(self,[]) # load config files
				if len(jid)!=0 and len(jid.split("@"))==2 and len(password)!=0:
					
					if (jid!=self.config['jid'] or ( unicode(self.ui.login_savePassword.isChecked())=="True" and unicode(rot13.scramble(password))!=unicode(self.config['passwd']))) or (unicode(self.config['savePasswd'])!=unicode(self.ui.login_savePassword.isChecked()) or unicode(self.ui.login_autoconnect.isChecked())!=self.config['autoJoin']):
						ret=QtGui.QMessageBox.question(self,self.tr("Login information"), self.tr("Save current login information?"),3,4)
						if ret==3:
							self.config['savePasswd']=self.ui.login_savePassword.isChecked()
							if self.ui.login_savePassword.isChecked()==True:
								self.config['passwd']=rot13.scramble(password)
							else:
								self.config['passwd']=""
							self.config['jid']=jid
							if self.ui.login_autoconnect.isEnabled():
								self.config['autoJoin']=unicode(self.ui.login_autoconnect.isChecked())
							else:
								self.config['autoJoin']="False"
							self.config.write()
			else:
				#ret=QtGui.QMessageBox.question(self,self.tr("New profile"), self.tr("Profile for this JID doesn't exist. Do you want to create it?"),3,4)
				#if ret==3:
				self.homeDir=self.realHomeDir+"/"+jid+"-profile"
				utils.makeHomeDir(self.homeDir)
				#if not os.path.isdir(self.homeDir):
					#os.mkdir(self.homeDir)
				f=open(self.homeDir+"/config",'w')
				self.config.write(f)
				f.close()
				utils.loadConfig(self,[]) # load config files
				self.config['savePasswd']=self.ui.login_savePassword.isChecked()
				if self.ui.login_savePassword.isChecked()==True:
					self.config['passwd']=rot13.scramble(password)
				else:
					self.config['passwd']=""
				self.config['jid']=jid
				self.config.write()
	

			f=open(self.realHomeDir+"/config",'w')
			self.config.write(f)
			f.close()
			
			if self.client==None:
				if self.config.has_key('resource'):
					resource=''.join(self.config['resource'])
				else:
					resource='jabbim'
				self.client = clientClass(unicode(jid).lower()+"/"+resource, password, jid.split("@")[1], 5222,self,reactor)
				self.client.xmlLang = unicode(QtCore.QLocale.system().name())[:2]
				self.client.log=True
			f=open(self.realHomeDir+"/config",'w')
			self.config.write(f)
			f.close()
			self.reconnect = True
			if self.config['specifyHost'] == 'True':
				self.client.connect(self.config['connectHost'], self.config['connectPort'])
			else:
				self.client.connect()
	
	def _loadAvatar(self,file, hash, jid):
		if os.path.isfile(unicode(file)):
			jid=jidT.JID(jid).userhost()
			pixmap=QtGui.QPixmap()
			f=open(unicode(file),"rb")
			image=f.read()
			f.close()
			pixmap.loadFromData(image)
			for item in self.ui.roster.getUserItems(jid):
##				log.msg(utils.cprint("yellow","setting icon: "+jid))
				item.setAvatar(QtGui.QIcon(pixmap))
			for item in self.ui.roster.getMetaItems(jid):
				item[0].setAvatar(QtGui.QIcon(pixmap))
		else:
			log.msg("BAD FILE FOR AVATAR:"+unicode(file))
		self.client.roster['users'][jid].setAvatar(file, hash)
	
	def _addGroup(self, group):
		item=self.ui.roster.addGroup(unicode(group))
		if group in self.config['expandedGroups']:
			item.setExpanded(True)
			#self.ui.roster.repaint()
		return item
	
	def _addUser(self, itemjid, name, grp):
		return self.ui.roster.addUser(itemjid,name,grp)

	def _badJabberPassword(self):
		QtGui.QMessageBox.warning(self,self.tr("Error"),unicode(self.tr("Bad Jabber ID or password.")),0,1)

	def _serverNotFound(self):
		QtGui.QMessageBox.warning(self,self.tr("Error"),unicode(self.tr("Server is not found.")),0,1)

	def _disconnect(self, error = None): # error = None | dns | lost | auth | failed
		self.tray.setIcon(QtGui.QIcon(QtGui.QIcon("images/16x16/apps/jabbim.png").pixmap(16,16,QtGui.QIcon.Disabled)))
		if self.client:
			if error=="auth":
				reactor.callLater(0,self._badJabberPassword)
				#QtGui.QMessageBox.warning(self,self.tr("Error"),unicode(self.tr("Bad Jabber ID or password.")),0,1)
			elif error=="dns":
				reactor.callLater(0,self._serverNotFound)
				#QtGui.QMessageBox.warning(self,self.tr("Error"),unicode(self.tr("Server is not found.")),0,1)
			if self.client.factory:
				self.client.factory.stopTrying()
			self.reconnect = False

# 		elif error == 'lost' and MainWindow.reconnect:
# 			# connection lost, let's wait for a while and then reconnect

# 			MainWindow.plugins=[]
# 			MainWindow.client = None
# # 			log.err('Connection Lost')
# 			reactor.callLater(3, MainWindow.connect)
		
		#MainWindow.ui.statusButton.setText(unicode(MainWindow.status["offline"]))
		#MainWindow.ui.statusButton.setIcon(MainWindow.getIcon("offline",size="16x16"))
		#MainWindow.ui.statusButton.hide()
		MainWindow.ui.rosterStackedWidget.setCurrentIndex(0)
		MainWindow.ui.showOffline.hide()
		MainWindow.ui.actionAdd_Contact.setEnabled(False)
		MainWindow.ui.actionJoin_groupchat.setEnabled(False)
		MainWindow.ui.actionService_Discovery.setEnabled(False)
		self.ui.login_cancel.show()
		self.ui.profilesList.setEnabled(True)

		#MainWindow.client.roster = {'users':{},'groups':{}}
		#MainWindow.client.roster_meta = {} # jid: {'tag':tag,  'order': 1}
		#MainWindow.client.first_presence = []
		#MainWindow.client.first_wait = True
		#MainWindow.client.bookmarks = {'conference':{}, 'url': {}}
		#MainWindow.client.roster['groups']['Unknown']=MainWindow.ui.roster.addGroup('Unknown')
		#MainWindow.client.temp_hosts=[]
		MainWindow.ui.roster.sortedGroups=[]
		MainWindow.ui.roster.sorted={}
		MainWindow.ui.roster.users=[]
		#MainWindow.ui.roster.groups={}
		MainWindow.ui.roster.disconnect()
		#MainWindow.ui.roster.makeHiddenItem()
		MainWindow.ui.login_connect.setEnabled(True)
		#MainWindow.plugins={}
		for i in MainWindow.plugins.keys():
			MainWindow.unloadPlugin(i)
		if self.client:
			for jid in self.client.groupchats.keys():
				for i in range(self.chat.ui.chatTab.count()):
					w=self.chat.ui.chatTab.widget(i)
					if unicode(w.jid) == jid:
						w.chat.ui.line.setEnabled(False)
						w.chat.ui.users.clear()
						w.chat.addRoles()
						message=self.skin["status_message"].replace("[time]",self.now()).replace("[message]",unicode(self.tr("You are now offline.")))
						w.chat.textEditWrite(message)
		MainWindow.client = None
		if error == 'lost' and MainWindow.reconnect:
 			# connection lost, let's wait for a while and then reconnect
			MainWindow.tray.showMessage(self.tr("Connection lost! "),self.tr("Trying to reconnect ..  ") , QtGui.QSystemTrayIcon.Warning, 5000)
 			MainWindow.plugins={}
 			MainWindow.client = None
			log.err('Connection Lost')
 			reactor.callLater(3, MainWindow.connect)
		print "disconnected....."


class XMLConsole(QtGui.QMainWindow):
	def __init__(self,data,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.ui=widgets.xmlConsole.Ui_xmlConsole()
		self.ui.setupUi(self)
		QtCore.QObject.connect(self.ui.send,QtCore.SIGNAL("clicked()"),self.send)
		QtCore.QObject.connect(self.ui.message,QtCore.SIGNAL("clicked()"),self.message)
		QtCore.QObject.connect(self.ui.presence,QtCore.SIGNAL("clicked()"),self.presence)

	def message(self):
		self.ui.textEdit.setText("<message to='USER@DOMAIN' from='"+MainWindow.client.jid.full()+"'>\n<body>Body text</body>\n</message>")

	def presence(self):
		self.ui.textEdit.setText("<presence from='"+MainWindow.client.jid.full()+"'>\n<show>???</show>\n<status>???</status>\n</presence>")

	def send(self):
		text=unicode(self.ui.textEdit.toPlainText())
		try:
			MainWindow.client.xmlstream.send(text)
		except:
			print "can't send"
		self.ui.textEdit.setText("")




class customStatusWindow(QtGui.QDialog):
	def __init__(self,jid,show=None,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(False)
		self.ui=widgets.status.Ui_status()
		self.ui.setupUi(self)
		self.timer=QtCore.QTimer()
		app.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.timeout)
		app.connect(self.ui.status, QtCore.SIGNAL("cursorPositionChanged ()"),self.timerStop)
		app.connect(self.ui.status, QtCore.SIGNAL("textChanged ()"),self.timerStop)
		self.ui.statusBox.hide()
		self.ui.save.hide()
		self.timer.start(1000)
		self.i=4
		self.jid=jid
		self.show=show
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
			self.timer.stop()
	def accept(self):
		MainWindow.client.sendPresence(to=self.jid,show = unicode(self.show), status = unicode(self.ui.status.toPlainText ()))
		self.done(1)


class statusWindow(QtGui.QDialog):
	def __init__(self,data,show=None,parent=None):
		apply(QtGui.QDialog.__init__,(self,MainWindow))
		self.setModal(False)
		self.ui=widgets.status.Ui_status()
		self.ui.setupUi(self)
		self.timer=QtCore.QTimer()
		app.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.timeout)
		app.connect(self.ui.status, QtCore.SIGNAL("cursorPositionChanged ()"),self.timerStop)
		app.connect(self.ui.status, QtCore.SIGNAL("textChanged ()"),self.timerStop)
		self.ui.status.setFocus()
		self.timer.start(1000)
		self.i=4
		self.data=data
		self.show=show
		self.timeout()
		for s in MainWindow.config['statusMessages']:
			self.ui.statusBox.addItem(unicode(s))
		app.connect(self.ui.statusBox, QtCore.SIGNAL("activated ( const QString & )"),self.ui.status.setPlainText)
		app.connect(self.ui.statusBox, QtCore.SIGNAL("highlighted ( int)"),self.timerStop)


	def timerStop(self):
		self.timer.stop()
		self.ui.time.setText("")
	
	def timeout(self,data=None):
		if self.i!=0:
			self.ui.time.setText(self.tr("Window will be closed in ")+unicode(self.i)+self.tr(" seconds."))
			self.i-=1
		else:
			self.timer.stop()
			self.accept()
	def accept(self):
		if not unicode(self.ui.status.toPlainText()) in MainWindow.config['statusMessages'] and len(unicode(self.ui.status.toPlainText()))!=0 and self.ui.save.isChecked():
			MainWindow.config['statusMessages'].append(unicode(self.ui.status.toPlainText()))
		if self.data=="offline":
			MainWindow.client.sendPresence(typ = "unavailable", status = unicode(self.ui.status.toPlainText ()))
			MainWindow.client.factory.stopTrying()
			MainWindow.reconnect = False
			MainWindow.client.disconnect()
			MainWindow._disconnect()

		else:
			jid=None
			if self.show:
				jid=self.data
				self.data=self.show
			icon=QtGui.QIcon("images/16x16/apps/jabbim.png")
			if self.data!='online':
				result=icon.pixmap(16,16)
				painter=QtGui.QPainter(result)
				icon=MainWindow.getIcon(status=unicode(self.data),size="16x16")
				painter.drawPixmap(0,0,icon.pixmap(16,16))
				painter.end()
			else:
				result=icon
			MainWindow.tray.setIcon(QtGui.QIcon(result))
			#app.postEvent(jab,customEvent(["set_status",self.groupchat,self.data,unicode(self.ui.status.toPlainText ())]))
			#jab.setStatus(MainWindow.groupchat,self.data,unicode(self.ui.status.toPlainText ()))
			if MainWindow.config.has_key('autoPriority'):
				if MainWindow.config['autoPriority']=='True':
					#priors={"chat":"25","online":"20","away":"15","xa":"10","dnd":"5"}
					pri=priors[str(self.data)]
				else:
					if MainWindow.config.has_key('priority'):
						pri=MainWindow.config['priority']
					else:
						pri="0"
			else:
				if MainWindow.config.has_key('priority'):
						pri=MainWindow.config['priority']
				else:
					pri="0"
			#if not jid:
				#MainWindow.ui.showWidget.label.setText(unicode(self.ui.status.toPlainText()).replace("\n"," ")[:25])
			if jid:
				#typ="available"
				#if self.data=="offline":
					#typ="unavailable"
				print self.data
				MainWindow.client.sendPresence(to=jid,show = unicode(self.data), status = unicode(self.ui.status.toPlainText ()),priority=pri)
			else:
				MainWindow.client.sendPresence(show = unicode(self.data), status = unicode(self.ui.status.toPlainText ()),priority=pri)
			#musime updatovat MUCy
			if not jid:
				for muc in MainWindow.client.groupchats.itervalues():
					MainWindow.client.sendPresence(show = unicode(self.data), status = unicode(self.ui.status.toPlainText ()), to = '%s/%s'%(muc.jid, muc.nick))

		self.done(1)

class aboutDialog(QtGui.QDialog):
	def __init__(self,parent):
		QtGui.QDialog.__init__(self,parent)
		self.setModal(True)
		self.ui=widgets.about.Ui_about_window()
		self.ui.setupUi(self)
		
class scrollBar(QtGui.QScrollArea):
	def __init__(self,parent=None):
		QtGui.QScrollArea.__init__(self,parent)
		self.y=0
		self.verticalScrollBar().setPageStep(32)
		self.verticalScrollBar().setSingleStep(32)
		self.setObjectName("scroll")
	#def updateScrollBars(self):
		#QtGui.QScrollArea.updateScrollBars(self)
		#self.verticalScrollBar().setPageStep(32)

#look=QtGui.QStyleFactory.create("cleanlooks")
#class style(QtGui.QStyle):
	#def polish(self,palette):
		#palette.setBrush(QtGui.QPalette.Button, QtCore.Qt.red);
	#def drawPrimitive(self, element,option, painter,widget=None):
		#return look.drawPrimitive(self, element,option, painter,widget)

if __name__ == "__main__":
	translator=QtCore.QTranslator()
	translator.load("locales/jabbim_"+unicode(QtCore.QLocale.system().name())[:2]+".qm")
	print "trying to load locales:","locales/jabbim_"+unicode(QtCore.QLocale.system().name())[:2]+".qm"
	app.installTranslator(translator)
	#app.setStyle(style())
	MainWindow = mainWindow()
	MainWindow.show()
	reactor.run()
