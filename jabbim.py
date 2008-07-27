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
import sys,os
sys.path.append('.')
try: from PyQt4 import QtCore, QtGui
except: print "PyQt4 is not installed."

#if sys.argv[1]=="remote":
#	app=QtCore.QCoreApplication([])

try:
	QtGui.QWizard
	USE_WIZARDS=True
except:
	USE_WIZARDS=False
import qt4reactor
#if sys.platform=="win32":
	#import win32gui


class jabbimApplication(QtGui.QApplication):
	"""
	Main Jabbim application class.
	"""
	def __init__(self,args=[]):
		QtGui.QApplication.__init__(self,args)
		self.shutdown=False
		self.sleep=False
		self.setApplicationName("Jabbim")
		
	def winEventFilter(self,msg):
		# WM_POWERBROADCAST
		if msg.message==536:
			# PBT_APMSUSPEND
			if msg.wParam==4 and not self.sleep:
				print "emit sleep()"
				self.emit(QtCore.SIGNAL("sleep()"))
				self.sleep=True
			elif msg.wParam==7 and self.sleep:
				print "emit wakeup()"
				self.emit(QtCore.SIGNAL("wakeUp()"))
				self.sleep=False
			return (True,1)
		# Snarl clicked (notification.py hook)
		elif msg.message==1025 and msg.wParam==34:
			if self.main.snarlMessages.has_key(int(msg.lParam)):
				self.main.snarlMessages[int(msg.lParam)][0](*self.main.snarlMessages[int(msg.lParam)][1])
				del self.main.snarlMessages[int(msg.lParam)]
			return (True,1)
		return (False,1)

	def commitData(self,manager):
		"""
		Called when application is closed by Window manager
		"""
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
from os.path import basename,dirname, isfile
from twisted.words.protocols.jabber.xmlstream import IQ
from pyxl import jid as jidT
import ctypes
from twisted.web.microdom import parseString,Element
from twisted.web.client import downloadPage
from twisted.web import xmlrpc, server #for xmlrpc plugin
import shutil #xmlrpc
from twisted.python.filepath import FilePath
from widgets.extra import extraDialog
from locale import strcoll
import weakref

class clientClass(pyxl.client.Client):
	"""
	Pyxl client class.
	"""
	def on_init(self):
		"""
		Called in pyxl __init__ function. Initializes all variables for Jabbim side of pyxl
		"""
		self.temp_hosts=[] #: contains hosts which are probed for disco#info
		# set OS informations
		if self.main.config['sendOSInfo'] == 'True':
			self.client_os = utils.get_os_info()
		else:
			self.client_os = ''
		self.version=self.main.version
		self.bookmarksEnabled=True #: True if bookmarks is enabled by server
		self.xmlCount=[]
		# load plugins
		self.loadPlugins()

	def on_pep(self, frm, ns, payload):
		"""
		Called when PEP informations of contact frm is changed.
		"""
		# it's our own pep
		if frm == self.jid.userhost():
			self.main.ui.selfAvatar.refreshToolTip()
		# change information in chat tab if we have opened it
		tab,index=self.main.chat.findTab(frm,typ=['chat'])
		change=[]
		# user mood
		if ns=="http://jabber.org/protocol/mood":
			change.append("mood")
			t = ''
			m = txt = ''
			for el in payload.elements():
				if el.name == 'text':
					txt = unicode(el)
				else :
					m = el.name
			# set user mood for contacts in roster
			if self.main.moodIcons.has_key(m):
				for item in self.main.ui.roster.getUserItems(frm):
					item.mood=self.main.moodIcons[m].pixmap(16,16)
			else:
				for item in self.main.ui.roster.getUserItems(frm):
					item.mood=None
			self.main.ui.roster.repaint()
			if frm == self.jid.userhost() : #our own mood
				if m == '':
					m = 'none'
				if self.main.moodIcons.has_key(m):
					self.main.ui.moodButton.setIcon(self.main.moodIcons[m])
				if self.main.moodMenu.currentAction:
					font=self.main.moodMenu.currentAction.font()
					font.setBold(False)
					self.main.moodMenu.currentAction.setFont(font)
				if self.main.moodActions.has_key(m):
					self.main.moodMenu.currentAction = self.main.moodActions[m]
					font=self.main.moodMenu.currentAction.font()
					font.setBold(True)
					self.main.moodMenu.currentAction.setFont(font)
		# user tune
		elif ns=='http://jabber.org/protocol/tune':
			change.append("tune")
			tune=payload
			listening=False
			song=""
			if type(tune) == list:
				for x in tune:
					print x
			elif tune!=None:
				artist = title = ''
				for el in tune.elements():
					if el.name == 'artist':
						artist = unicode(el)
					elif el.name == 'title':
						title = unicode(el)
				t = '%s  %s'%(artist, title)
				if len(t.strip())>0:
					listening=True
			# set user tune information for contacts in roster
			if listening:
				listening=QtGui.QIcon("images/22x22/icons/headphones.png").pixmap(16,16)
				song=t
			for item in self.main.ui.roster.getUserItems(frm):
				item.tune=listening
				item.song=song
				item.height=self.main.ui.roster.rosterStyle.heightForItem(item)
			self.main.ui.roster.repaint()
		if tab:
			tab.chat.refreshLabel(change)
			tab.chat.refreshToolTip()
	def on_bookmarksFail(self):
		"""
		Called if bookmarks are not supported by server.
		"""
		self.main.ui.tabWidget.setTabEnabled(1,False)
		self.bookmarksEnabled=False
		mainWindow=self.main
		self.main.tray.showMessage(MainWindow.tr("Error"),mainWindow.tr("Your server doesn't support Private XML Storage. Some functions will be disabled."))

	def on_privacyFail(self):
		"""
		Called if privacy lists are not supported by server.
		"""
		self.main.ui.actionPrivacy_list_editor.setEnabled(False)

	def on_GCpresenceError(self, fromjid, code, typ, name, text, resource = ""):
		"""
		Called if there was error on joining the groupchat
		"""
		mainWindow=self.main
		if int(code)==409:
			# nickname conflict
			# rejoin with oldNick_ if tab for this room exists
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				if str(self.main.config["autochangenickMUC"])=="True":
					tab.chat.nick=resource+"_"
					self.joinGC(fromjid, resource+"_",sendRooms=self.main.config['sendRooms']==True)
				else:
					self.main.chat.ui.chatTab.removeTab(index)
					if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
					self.main.events.addLineEditEvent(maintext=unicode(fromjid)+"<br/>"+mainWindow.tr('This nickname is used by someone else. Please choose another.'), trueCall=self.main.joinGC, trueDict=[fromjid], falseCall=None,falseDict=None,header=mainWindow.tr("Nickname conflict"),text=mainWindow.tr("New name:"),name=unicode(fromjid),typ="groupchatError",icon=None,action=None,actionDict=None,height=150, value=resource,trueText=mainWindow.tr("Join"),falseText=mainWindow.tr("Decline"))
		elif int(code)==401:
			log.msg("room is password protected")
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
				self.main.events.addInfoEvent(header=mainWindow.tr("Wrong password"),text=mainWindow.tr("Room is password protected"),name=unicode(fromjid),typ='groupchatError')
		elif int(code)==407:
			log.msg("room is member only")
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
				self.main.events.addInfoEvent(header=mainWindow.tr("Member only"),text=mainWindow.tr("Room is only for members"),name=unicode(fromjid),typ='groupchatError')
		elif int(code)==403:
			log.msg("room user benned")
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
				self.main.events.addInfoEvent(header=mainWindow.tr("Banned"),text=mainWindow.tr("You are banned from entering this room."),name=unicode(fromjid),typ='groupchatError')
		elif int(code)==503:
			log.msg("Room Occupant Limit Has Been Reached")
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
				self.main.events.addInfoEvent(header=mainWindow.tr("Max Users"),text=mainWindow.tr("Room occupant limit has been reached"),name=unicode(fromjid),typ='groupchatError')
		elif int(code)==404:
			log.msg("Room not exist")
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
				self.main.events.addInfoEvent(header=mainWindow.tr("Room not exist"),text=mainWindow.tr("Room is creating try it again"),name=unicode(fromjid),typ='groupchatError')
		elif int(code)==405:
			log.msg("Room is reserved")
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
				self.main.events.addInfoEvent(header=mainWindow.tr("Room reserved"),text=mainWindow.tr("Not allowed create room"),name=unicode(fromjid),typ='groupchatError')
		elif int(code)==406:
			log.msg("Roomnicks are locked")
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
				self.main.events.addInfoEvent(header=mainWindow.tr("Locked Nicknames"),text=mainWindow.tr("Not allowed change nickname"),name=unicode(fromjid),typ='groupchatError')
		else:
			# remove groupchatWidget from chatWindow
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
					self.main.chat.hide()
			# add event with detailed description of the error
			self.main.events.addInfoEvent(header=mainWindow.tr("Groupchat Error"),text=text,name=unicode(fromjid),typ='groupchatError')

	def on_roleErr(self,  muc,  err,  nick):
		pass
	
	def on_affiliationErr(self,  muc,  err,  nick):
		pass

	def on_ftTransfered(self, sid, bytes,end=False):
		"""
		Updates progress bars for filetransfer with id 'sid'.
		@type sid: unicode
		@param sid: filetransfer ID
		@type bytes: integer
		@param bytes: count of transfered bytes
		"""
		mainWindow=self.main
		widget=self.main.events.filetransferWidget[self.main.events.filetransfer[sid]['queueId']] # event widget
		# normal widget => progress bars in events tab or in chatwidget
		if widget.typ=='normal':
			queueId=self.main.events.filetransfer[sid]['queueId'] # filetransfer queue ID
			if not end:
				# Filetransfer is alive, so we have to update progressbar
				size=float(self.ft[sid].size)
				sent=float(self.ft[sid].transfered)
				widget.widget.progressBar.setValue(int((sent/size)*100))
			else:
				# Filetransfer finished
				print 'ft.finished'
				
				widget.widget.progressBar.setValue(100)
				if widget.widget.complete==None:
					# User wants to close transfer
					# TODO: we have to do something here (inform user that transfer was stopped for example...)
					self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(widget.widget.item))
					widget.widget.complete=True
				else:
					# file has been sent/received :)
					tab,index=self.main.chat.findTab(self.main.events.filetransferWidget[queueId].jid,typ=['chat'])
					# update errors list
					self.main.events.filetransferWidget[self.main.events.filetransfer[sid]['queueId']].errors.append(self.main.ftError[sid])
					# file upload
					if widget.download==False:
						# delete this file from upload queue
						del self.main.events.filetransferQueue[queueId][self.main.events.filetransferWidget[self.main.events.filetransfer[sid]['queueId']].file]
						emptyQueue=len(self.main.events.filetransferQueue[queueId])==0
						# no error
						if self.main.ftError[sid]==None:
							widget.widget.stats.setText(mainWindow.tr("Complete"))
							# inform user in chatwidget too, if there is some opened conversation with recipient
							if tab:
								file=self.main.events.filetransferWidget[queueId].file
								tab.chat.textEditWrite(self.main.webkitThemeFactory.genChatStatus(unicode(mainWindow.tr("File "))+" "+unicode(basename(file))+" "+ unicode(mainWindow.tr('has been sent')),self.main.now()))
								tab.chat.lastMessageFrom=""
						# file declined
						elif self.main.ftError[sid].lower()=='canceled':
							widget.widget.progressBar.setValue(0)
							widget.widget.stats.setText(mainWindow.tr("File declined"))
							self.main.tray.showMessage(mainWindow.tr('File transfer'),unicode(mainWindow.tr("User declined to receive file"))+" "+basename(unicode(widget.file)), QtGui.QSystemTrayIcon.Critical, 4000)
							# inform user in chatwidget too, if there is some opened conversation with recipient
							if tab:
								tab.chat.textEditWrite(self.main.webkitThemeFactory.genChatStatus(unicode(mainWindow.tr("User declined to receive file"))+" "+basename(unicode(widget.file)),self.main.now()))
								tab.chat.lastMessageFrom=""
						# unknown error
						else:
							widget.widget.progressBar.setValue(0)
							widget.widget.stats.setText(mainWindow.tr("Error")+" "+unicode(self.main.ftError[sid]))
							self.main.tray.showMessage(mainWindow.tr('File transfer'),unicode(mainWindow.tr("File "))+unicode(widget.file)+unicode(mainWindow.tr(" can't be sent ")), QtGui.QSystemTrayIcon.Critical, 4000)
							# inform user in chatwidget too, if there is some opened conversation with recipient
							if tab:
								file=self.main.events.filetransferWidget[queueId].file
								tab.chat.textEditWrite(self.main.webkitThemeFactory.genChatStatus(unicode(mainWindow.tr("File "))+" "+basename(file)+" "+unicode(mainWindow.tr('can\'t be sent:'))+" "+unicode(self.main.ftError[sid]),self.main.now()))
								tab.chat.lastMessageFrom=""
						# some files are in queue, so we have to start to upload next file
						if not emptyQueue:
							self.main.events.nextFTUploadEvent(sid,queueId)
							widget.widget.complete=True
						# queue is empty => all files have been sent
						else:
							# check this queues error list, if there is something different then None, some files haven't been sent
							widget.widget.complete=True
							error=False
							for b in self.main.events.filetransferWidget[self.main.events.filetransfer[sid]['queueId']].errors:
								if b!=None:
									error=True
									break
							if not error:
								self.main.tray.showMessage(mainWindow.tr('File transfer'),unicode(mainWindow.tr("All files for"))+" "+widget.jid+" "+unicode(mainWindow.tr("have been sent")), QtGui.QSystemTrayIcon.Information, 4000)
							else:
								self.main.tray.showMessage(mainWindow.tr('File transfer'),unicode(mainWindow.tr("Some files for"))+" "+widget.jid+" "+unicode(mainWindow.tr("haven't been sent")), QtGui.QSystemTrayIcon.Critical, 4000)
							# inform user in chatwidget too, if there is some opened conversation with recipient
							if tab:
								if not error:
									tab.chat.textEditWrite(self.main.webkitThemeFactory.genChatStatus(unicode(mainWindow.tr("All files have been sent")),self.main.now()))
									tab.chat.lastMessageFrom=""
								else:
									tab.chat.textEditWrite(self.main.webkitThemeFactory.genChatStatus(unicode(mainWindow.tr("Some files can't be sent")),self.main.now()))
									tab.chat.lastMessageFrom=""
								# remove progress bar from chatWidget
								if tab.chat.filetransfer.has_key(queueId):
									tab.chat.ui.ftwidget.layout().removeWidget(tab.chat.filetransfer[queueId])
									tab.chat.filetransfer[queueId].setParent(None)
									del tab.chat.filetransfer[queueId]
					# file download
					else:
						widget.widget.complete=True
						# no error
						if self.main.ftError[sid]==None:
							widget.widget.stats.setText(mainWindow.tr("Complete"))
							self.main.tray.showMessage(mainWindow.tr('File transfer'),unicode(mainWindow.tr("File "))+unicode(widget.file)+unicode(mainWindow.tr(" has been downloaded")), QtGui.QSystemTrayIcon.Information, 4000)
							# inform user in chatwidget too, if there is some opened conversation with sender
							if tab:
								file=self.main.events.filetransferWidget[queueId].file
								tab.chat.textEditWrite(self.main.webkitThemeFactory.genChatStatus(unicode(mainWindow.tr("File "))+" "+basename(file)+" "+ unicode(mainWindow.tr('has been downloaded')),self.main.now()))
								tab.chat.lastMessageFrom=""
								# remove progress bar from chatWidget
								if tab.chat.filetransfer.has_key(queueId):
									tab.chat.ui.ftwidget.layout().removeWidget(tab.chat.filetransfer[queueId])
									tab.chat.filetransfer[queueId].setParent(None)
									del tab.chat.filetransfer[queueId]
						# unknown error
						else:
							widget.widget.progressBar.setValue(0)
							widget.widget.stats.setText(unicode(mainWindow.tr("Error"))+" "+unicode(self.main.ftError[sid]))
							self.main.tray.showMessage(mainWindow.tr('File transfer'),unicode(mainWindow.tr("File "))+unicode(widget.file)+unicode(mainWindow.tr(" can't be downloaded ")), QtGui.QSystemTrayIcon.Critical, 4000)
							# inform user in chatwidget too, if there is some opened conversation with sender
							if tab:
								file=self.main.events.filetransferWidget[queueId].file
								tab.chat.textEditWrite(self.main.webkitThemeFactory.genChatStatus(unicode(mainWindow.tr("File "))+" "+basename(file)+" "+unicode(mainWindow.tr('can\'t be downloaded:'))+" "+unicode(self.main.ftError[sid]),self.main.now()))
								tab.chat.lastMessageFrom=""
								# remove progress bar from chatWidget
								if tab.chat.filetransfer.has_key(queueId):
									tab.chat.ui.ftwidget.layout().removeWidget(tab.chat.filetransfer[queueId])
									tab.chat.filetransfer[queueId].setParent(None)
									del tab.chat.filetransfer[queueId]
					# delete this filetransfer information
					del self.main.events.filetransfer[sid]
		# widget which shows progress of Jabbim Extra download
		else:
			if not end:
				# Filetransfer is alive
				size=float(self.ft[sid].size)
				sent=float(self.ft[sid].transfered)
				widget.setValue(int((sent/size)*100))
			else:
				# Filetransfer finished
				log.msg("ft.finished")
				widget.setValue(100)
				del self.main.events.filetransfer[sid]

	def on_ftEnd(self, sid, error = None): #pokud je error None je vse v poradku, jinak strucny popis chyby.
		"""
		Called when filetransfer finished
		"""
		self.dispatcher.publishEvent('on_ftEnd', sid, error)
		self.main.ftError[sid]=error
		# self.main.allowedSids contains SIDs which are used for transfering Jabbim Extra
		if sid in self.main.allowedSids:
			# continuing with jabbim extra
			print "Part of jabbim extra has been downloaded"
			file=self.ft[sid].file
			print "extracting",file,'to',dirname(file)
			try:
				root=utils.extractZip(file,dirname(file))
			except:
				message = unicode(traceback.format_exc(), 'utf-8')
				print message
			self.main.allowedSids.remove(sid)
			self.main.preferencesWindow.reloadView(file,root)
			self.main.preferencesWindow.reloadPlugins_()
		self.dispatcher.publishEvent('FTFinishedEvent', sid, error)
		#del self.ft[sid]
		self.on_ftTransfered(sid, 0,True) # we have to delete filetransfer and etc
		

	def on_discoInfoReceived(self, jid, node):
		"""
		Called when disco#info arrived.
		"""
		jid=self.main.getJid(jid).userhost()
		if True:
			typ=self.getHostType(jid,jid)
			if typ:
				if not self.main.transports.has_key(jid) and self.roster['users'].has_key(jid):
					# don't show this contacts as transports in menu
					if not typ in ['weather','smtp','sms','rss']:
						self.main.transports[jid]=None
						self.main.buildStatusWidgetMenu()

				for host in self.disco.keys():
					for i in self.main.ui.roster.getUserItems(host):
						i.transport=True
		# set icons for users with this host
		for item in self.main.ui.roster.getHostItems(jid):
			show=unicode(item.status)
			item.icon=self.main.getIcon("jid@"+jid,size=self.main.ui.roster.iconSize,status=self.main.icons[show])
		if jidT.JID(jid).userhost()==self.jid.userhost():
			print 'self discoInfo'
			self.main.buildOfflineMenu()

	def getHostType(self,host,jid):
		host=host.split('/')[0]
		try:
			name=self.disco[host][None]['identities'].keys()[0]
			typ=self.disco[host][None]['identities'][name]['type']
		except:
			typ=None
		if typ!=None:
			# parse types
			if typ=="pep" or typ=="im":
				typ="jabber"
			elif typ=="file":
				typ="disk"
			elif typ=='gadu-gadu':
				typ='gadugadu'
			elif typ=='x-tlen':
				typ='tlen'
			if jid.find("weather")!=-1:
				typ='weather'
		return typ

	def on_rosterAddUser(self, contact):
		"""
		Called when adds user to the roster
		"""
		start=time.time()
		groups=list(contact.groups)
		name=unicode(contact.name)
		jid=unicode(contact.jid)
		# remove empty groups
		while u'' in groups:
			groups.remove('')

		# add groupItem if we haven't it
		for gr in groups:
			if not self.roster['groups'].has_key(gr):
				self.roster['groups'][gr]=self.main._addGroup(gr)
		transport=False
		# get host info if we haven't it
		if len(unicode(jid).rsplit("@"))!=1:
			host=unicode(jid).rsplit("@")[1].split('/')[0]
		else:
			host=unicode(jid).split('/')[0]
			transport=True
		identity=self.getIdentity(jid)
		print identity
		if not identity and not host in self.temp_hosts:
			self.temp_hosts.append(host)
			self.getDiscoInfo(host)
		if transport:
			typ=self.getHostType(host,jid)
			if typ and not typ in ['weather','smtp','sms','rss']:
				self.main.transports[jid]=None
				self.main.buildOfflineMenu()
				self.main.buildStatusWidgetMenu()
		# user is not in any group
		if len(groups)==0:
			# add user item to Unknown group
			it=self.main.ui.roster.addUser(jid,name,None)
		else:
			for group in groups:
				# add user item to the group
				it=self.main.ui.roster.addUser(jid,name,group)
				if transport:
					it.transport=True

		# load avatar
		#self.main._loadAvatar(self.main.homeDir+'/avatars/'+jid, self.avatars.get(jid), jid)

	def makeTempMeta(self):
		"""
		@depracted
		"""
		meta={} # temp variable for metacontacts - {userTag:userJid}
		for jid,user in self.roster['users'].iteritems():
			if jid == self.jid.userhost():
				continue
			if user.tag!=None:
				if not meta.has_key(user.tag):
					meta[user.tag]=[[jid,user.order]]
				else:
					meta[user.tag].append([jid,user.order])
		self.meta=meta
		return meta

	def renameByVcard(self,el,jid):
		"""
		Renames contact with 'jid' acording to vcard.
		"""
		if el:
			data=el.firstChildElement()
			nickname=fullname=family=given=None
			for x in data.elements():
				name=unicode(x.name)
				if name=="NICKNAME":
					nickname=(unicode(x))
				elif name=="FN":
					fullname=(unicode(x))
				else:
					for y in x.elements():
						child=unicode(y.name)
						if name=="N" and child=="GIVEN":
							given=unicode(y)
						elif name=="N" and child=="FAMILY":
							family=unicode(y)
			newName=None
			if nickname:
				newName=nickname
			elif fullname:
				newName=fullname
			elif given and family:
				newName=given+" "+family
			if newName and jid != self.jid.userhost():
				contact=self.roster['users'][jid]
				self.sendRosterUpdate(contact.jid, newName, contact.subscription, self.roster['users'][jid].groups)
			elif newName and jid == self.jid.userhost():
				self.main.ui.selfName.setText('<h3>'+newName+'</h3>') #we need to set name in roster
				self.main.selfName=newName

	def on_discoItemsBookmarksReceived(self, jid):
		"""
		Called when disco#items of bookmarked groupchat arrived.
		"""
		item=self.main.ui.bookmarks.findItems(jid,QtCore.Qt.MatchExactly,1)[0] # find item
		for i in range(item.childCount()):
			item.takeChild(0)
		for name in self.disco[jid][None]['items'].keys():
			user=QtGui.QTreeWidgetItem(item)
			user.setText(0,unicode(jidT.JID(name).resource))
			user.setText(1,unicode(name))
			user.setIcon(0,self.main.getIcon(size="16x16"))

	def on_rosterArrived(self):
		"""
		Called when roster arrived.
		"""
		start=time.time()
		print 'we got roster'
		self.main.ui.splashProgress.setValue(60)
		mainWindow=self.main
		self.main.ui.loginInfo.setText(mainWindow.tr("Roster arrived."))
		self.main.buildBookmarks() # build Bookmarks tab
		self.main.chat.reconnect()
		self.main.buildOfflineMenu()
		self.main.buildStatusWidgetMenu()

		self.metaParents={}

		# get metacontacts in better form
		meta=self.makeTempMeta()

		# handle metacontacts... this will be replaced in the future...
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

		# update privacy list of userItems in roster widget
		if self.privacy != False:
			for item in self.privacy.active.items:
				if item.value and item.typ == "jid":
					for useritem in self.main.ui.roster.getUserItems(item.value):
						useritem.privacy["block"] = self.privacy.active.isBlockedJID(item.value)
						useritem.privacy["allow"] = self.privacy.active.isAllowedJID(item.value)
						useritem.privacy["hide"] = self.privacy.active.isHiddenJID(item.value)

		for host in self.disco.keys():
			for i in self.main.ui.roster.getUserItems(host):
				i.transport=True
				i.icon=self.main.getIcon("jid@"+host,size=self.main.ui.roster.iconSize,status=self.main.icons[str(i.status)])
			for i in self.main.ui.roster.getHostItems(host):
				i.icon=self.main.getIcon("jid@"+host,size=self.main.ui.roster.iconSize,status=self.main.icons[str(i.status)])

		# update roster
		self.main.ui.roster.sortItems()
		self.main.ui.roster.repaint()

		# send first presence to server
		lst=self.main.ui.loginStatus.itemData(int(self.main.ui.loginStatus.currentIndex())).toList()

		show, status = [unicode(val.toString()) for val in lst]
		self.main.selfStatus=show
		#self.main.tray.setToolTip(mainWindow.tr('Your status:')+" "+self.main.status[show])
		self.main.ui.selfAvatar.refreshToolTip()
		print 'old ',  self.oldstatus
		self.main.sendPresence(None,show,status)
		self.main.ui.statusButton.setText(unicode(""))
		self.main.ui.statusButton.setIcon(self.main.getIcon(status=show,size="16x16"))
		self.main.ui.login_cancel.hide()

	def on_rosterx(self, frm, items, id):
		mainWindow = self.main
		if len(items)==1:
			item = items[0]
			self.main.events.addBooleanEvent(self.rosterx,[frm, items, id],None,[],mainWindow.tr("Receive contact?"),frm+mainWindow.tr(" is sending you a contact  ") + item['jid'],height=100,name=frm,typ="",icon=None)
		else:
			names = ''
			for item in items:
				names += item['jid']+'\n'
			print names
			self.main.events.addBooleanEvent(self.rosterx,[frm, items, id],None,[],mainWindow.tr("Receive contacts?"),frm+mainWindow.tr(" is sending you a contacts  ") + names,height=60*len(items),name=frm,typ="",icon=None)
		pass

	def rosterx(self, frm, items, id):
		mainWindow = self.main
		msg = mainWindow.tr("Hi! I am adding you to my roster using the jabber client Jabbim! Please authorize me to see you when you are available. Thanks!") #from _ui file
		print msg
		for item in items:
			jid, name, group = item['jid'], item.get('name', None), item.get('group', None),
			if name == None:
				name = ''
			if group == None:
				groups = []
			else:
				groups = [group]
			self.addContact(jid, unicode(msg), name, groups)

		if id != None:
			self._rosterxResult(frm, id, True)

	def on_authFailed(self,xmlstream):
		"""
		Authentication error.
		"""
		self.main.ui.login_connect.setEnabled(True)
	
	def on_firstpresence(self,  bulk):
		"""
		Process all first presences at once.
		"""
		start=time.time()
		for presence in bulk:
			jid=presence[0]
			show=presence[1]
			if len(presence)==3:
				error=presence[2]
			else:
				error=None
			self.on_presence(jid,show,error,True)

		mainWindow=self.main

		# update roster
		self.main.ui.roster.sortItems()
		#self.main.ui.roster.statusLabel.hide()
		self.main.ui.roster.repaint()

		# update splash window
		self.main.ui.splashProgress.setValue(100)
		self.main.ui.loginInfo.setText(mainWindow.tr("Jabbim is ready."))
		self.main.ui.rosterStackedWidget.setCurrentIndex(1)
		# load plugins, autoconnect
		self.reactor.callLater(2,self.autoJoin)

	def loadPlugins(self):
		self.main.findPlugins()
		self.main.loadPlugins()

	def autoJoin(self):
		if self.main.config['autoJoinMUC'] == 'True':
			self.main.autoJoinGroupchat()
		if self.main.delayedMessages != None:
			print 'delayed!'
			for msg in self.main.delayedMessages.itervalues():
				print msg
				self.sendMessage(**msg)
			self.main.delayedMessages = None
			self.messageReceipts = {}
		
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
		"""
		Called when groupchat presence arrived.
		"""
		show = unicode(show)
		# we are not in this room
		if not self.groupchats.has_key(muc):
			log.msg("bad GC presence:"+unicode(muc)+"; we are not connected there")
			return
		
		# find tab for this room
		tab,index=self.main.chat.findTab(muc,True,['groupchat'])
		if not tab:
			# we don't have opened tab for this room => nothing to do...
			return
		tabFull,indexFull=self.main.chat.findTab(muc+'/'+nick,True,['chat'])
		# we have opened conversation with this resource

		if show=="offline":
			# remove user from contact list
			tab.chat.removeUser(nick,codes,reason,actor,n)
			if tabFull:
				# update tab icon
				tabFull.ic=self.main.getIcon(size="16x16",status="offline")
				self.main.chat.ui.chatTab.setTabIcon(indexFull,tabFull.ic)
		else:
			# get user role and affiliation
			role=self.groupchats[muc].users[nick].role
			affiliation=self.groupchats[muc].users[nick].affiliation
			# edit user item in contact list
			tab.chat.editUser(nick,show,role,affiliation)
			if tabFull:
				# update tab icon
				tabFull.ic=self.main.getIcon(size="16x16",status=show)
				self.main.chat.ui.chatTab.setTabIcon(indexFull,tabFull.ic)

		# show status message in conversation textEdit
		if not u'303' in codes:
			print codes
			mainWindow=self.main
			if u'201' in codes:
				message=self.main.webkitThemeFactory.genGroupchatAction(unicode(mainWindow.tr("You are created this room.")),self.main.now())
				tab.chat.textEditWrite(message)
			if u'170' in codes:
				message=self.main.webkitThemeFactory.genGroupchatAction(unicode(mainWindow.tr("This room is logged")),self.main.now())
				tab.chat.textEditWrite(message)
			if u'100' in codes:
				message=self.main.webkitThemeFactory.genGroupchatAction(unicode(mainWindow.tr("Room is not anonymous")),self.main.now())
				tab.chat.textEditWrite(message)
			
				
			if self.main.config['showMucStatus'] == 'False' and  (not 'PART' in codes) and (not 'JOIN' in codes):
				return
			message="[nick] [jid]"+unicode(mainWindow.tr('is now'))+" [show] [[message]]"
			if status == None:
				message = message.replace("[[message]]",'')
			else:
				message = message.replace("[message]",unicode(status))

			if self.main.client.groupchats[muc].users[nick].truejid!="" and self.main.client.groupchats[muc].users[nick].truejid!=None:
				message=message.replace("[jid]",'('+unicode(self.main.client.groupchats[muc].users[nick].truejid)+') ')
			else:
				message=message.replace("[jid]","")
			message=message.replace("[show]",unicode(self.main.status[show])).replace('[nick]', nick)
			#message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace('[message]',message)
			message=self.main.webkitThemeFactory.genGroupchatStatus(message,self.main.now())
			if len(message)!=0:
				tab.chat.textEditWrite(message)
			if tabFull:
				tabFull.chat.textEditWrite(message)
				tabFull.chat.lastMessageFrom=""
		# refresh lastMessageFrom
		tab.chat.lastMessageFrom=""

	def on_presence(self,jid,show,error=None,first=False):
		"""
		Called when normal presence arrived.
		"""
		if error!=None:
			print "PRESENCE ERROR:"+unicode(error)
			return
		start=time.time()
		mainWindow=self.main
		status=None
		contact = self.getContactByJid(jid.userhost())

		# get tab for this contact
		tabFull,indexFull=self.main.chat.findTab(jid.full(),True,typ=['chat']) # tab with resource
		tab,index=self.main.chat.findTab(jid.full(),False,typ=['chat']) # tab without resource
		if tab and not tabFull:
			tabFull=tab
			indexFull=index

		# show info about status change in conversation textEdit
		if str(self.main.config["showChatStatusChanges"])=="True" and tabFull:
			# get senders username
			user=self.main.ui.roster.getNameByJID(jid.userhost())
			# append message to textEdit
			message="[nick] "+unicode(mainWindow.tr('is now'))+" [show] [[message]]"
			s = ''
			if contact != None:
				if contact.resources.has_key(jid.resource):
					s = contact.resources[jid.resource].status
			if s:
				message=message.replace("[message]",unicode(s))
			else:
				message=message.replace("[[message]]","")
			message=message.replace("[show]",unicode(self.main.status[show])).replace('[nick]', user)
			message=self.main.webkitThemeFactory.genChatStatus(message,self.main.now())
			#message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace('[message]',message)
			if len(message)!=0:
				tabFull.chat.textEditWrite(message)
			# refresh variables
			tabFull.chat.ui.chatstate.setText("")
			tabFull.chat.lastMessageFrom=""

		if not tabFull:
			metaTab,metaIndex=self.main.chat.findTabByMeta(jid.full())
		else:
			metaTab=tabFull

		# we have opened conversation with this JID (no only with this resource)
		if metaTab:
			metaTab.chat.buildResourceMenu()
			metaTab.chat.buildMetaMenu()
			metaTab.chat.refreshToolTip()
		status_=None
		if show=="offline":
			# self presence
			if jid.userhost()==self.jid.userhost():
				# rebuild self contacts menu
				if jid.resource in self.main.selfResources:
					self.main.selfResources.remove(jid.resource)
					self.main.buildOfflineMenu()
			# set status in roster
			self.main.ui.roster.setStatus(jid.userhost(),show,first=first)
			if jid.resource:
				self.main.ui.roster.setStatus(jid.full(),show,first=first)

			# we have opened conversation with this resource
			if tabFull:
				# update tab icon
				tabFull.ic=self.main.getIcon(unicode(jid.userhost()),size="16x16",status="offline")
				self.main.chat.ui.chatTab.setTabIcon(indexFull,tabFull.ic)

		else:
			# self presence
			if jid.userhost()==self.jid.userhost():
				# rebuild self contacts menu
				if not jid.resource in self.main.selfResources:
					self.main.selfResources.append(jid.resource)
					self.main.buildOfflineMenu()
				else:
					self.main.ui.selfAvatar.refreshToolTip()

			# we have opened conversation with this resource
			if tabFull:
				# update tab icon
				tabFull.ic=self.main.getIcon(unicode(jid.userhost()),size="16x16",status=self.main.icons[self.main.shows[unicode(show)]])
				self.main.chat.ui.chatTab.setTabIcon(indexFull,tabFull.ic)

			if jid.resource:
				resource=jid.resource
				# get highest resource
				try:
					highest=self.roster['users'][jid.userhost()].resources[self.roster['users'][jid.userhost()].getHighestResource()]
					status=highest.status
				except:
					status=None
					print 'error in resource', [jid.userhost()]
				# get status message
				if status!=None:
					status_=status
					status=status.replace("\n"," ").replace("<","&lt;").replace(">","&gt;")
				# update contact in roster
				try:
					self.main.ui.roster.setStatus(jid.userhost(),highest.show,status=highest.status,first=first)
					self.main.ui.roster.setStatus(jid.full(),highest.show,status=highest.status,first=first)
				except:
					print 'Error in resource ', jid.userhost()
			else:
				# get status message
				status=self.roster['users'][jid.userhost()].status[1]
				if status!=None:
					status=status.replace("\n"," ").replace("<","&lt;").replace(">","&gt;")
					status_=status
				# update contact in roster
				self.main.ui.roster.setStatus(jid.userhost(),show,status=status,first=first)
		# presence is from transport
		if self.main.transports.has_key(jid.full()):
			if self.main.transports[jid.full()]!=None:
				self.main.transports[jid.full()].setIcon(self.main.getIcon('1@'+jid.userhost(),status=unicode(show),size="16x16"))

				text='<table><tr>'
				if os.path.isfile(self.main.homeDir+'/avatars/'+unicode(self.main.config['jid'])):
					pixmap=QtGui.QIcon(self.main.homeDir+'/avatars/'+unicode(self.main.config['jid'])).pixmap(64,64)
					text+='<td><img src="'+self.main.homeDir+'/avatars/'+unicode(self.main.config['jid'])+'" width="'+str(pixmap.width())+'" height="'+str(pixmap.height())+'"/></td>'
				#text+='<td><b>'+self.main.tr("Name:")+'</b> '+item.escapedName+'<br/>'
				text+='<td><b>'+self.main.tr("JID:")+'</b> '+unicode(jid.full())+'<br/>'

				#status = unicode(message)
				#priority = pri
				#if priority != None:
					#priority = "(%s: %s)" % (self.main.tr("Priority"),priority)
				#else:
					#priority = ""
				usertype=unicode(self.getHostType(jid.userhost(),jid.userhost()))
				if os.path.isfile('images/16x16/status/'+usertype+"-"+show+".png"):
					text+='<img src="images/16x16/status/'+usertype+"-"+show+'.png" />'
				else:
					text+='<img src="images/16x16/status/jabber-%s.png">' % show
				#if len(priority)!=0:
					#text+='%s<br/>' % priority
				if status:
					text+='<font size="-1">%s</font>' % (status)
				text+="</td></tr></table>"
				self.main.transports[jid.full()].setToolTip(text)
		self.dispatcher.publishEvent('presenceEvent', jid, self.main.ui.roster.getNameByJID(jid.full()), show, status_, first)

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

	def on_UpdateContact(self,jid):
		"""
		Called when contact in roster is updated.
		"""
		# replace [''] with []
		if len(self.roster['users'][jid].groups)==1:
			if len(self.roster['users'][jid].groups[0])==0:
				self.roster['users'][jid].groups=[]
		# get all userItems of this JID
		items=self.main.ui.roster.getUserItems(jid)
		toDel=[] # temp variable for deleting items at the end of this function
		contact=self.roster['users'][jid]
		
		# add groupItems if we haven't it
		for gr in contact.groups:
			if not self.main.ui.roster.groups.has_key(gr):
				self.roster['groups'][gr]=self.main._addGroup(gr)
				self.roster['groups'][gr].setExpanded(True)

		# get all groupItems which contains this contact
		jidGroups=list(self.roster['users'][jid].groups)
		# if contact isn't in any group, use "No group" groupItem (aka specialName)
		if len(jidGroups)==0:
			jidGroups=[self.main.ui.roster.specialName]
		elif len(jidGroups[0])==0:
			jidGroups=[self.main.ui.roster.specialName]

		# get all groupItems which are presented in roster
		rosterGroups=dict(self.roster['groups'])
		rosterGroups[self.main.ui.roster.specialName]=self.main.ui.roster.groups[self.main.ui.roster.specialName]

		for name,item in rosterGroups.iteritems():
			# updated contact is in this group
			if name in jidGroups:
				add=True
				# go through all contacts items, find item in this group and edit it
				for i in items:
					if item.name==i.group:
						add=False # we found item, so we don't have to add it in the future
						name=contact.name
						if name==None or len(name)==0:
							name=jid
						i.name=unicode(name)
						i.escapedName=unicode(name).replace("<","&lt;").replace(">","&gt;")
						i.jid=jid
						# update roster
						self.main.ui.roster.sortItems()
						#self.main.ui.roster.changePos=True
						self.main.ui.roster.repaint()
				# we didn't find item so we have to add it to this group
				if add:
					# there is another item for this contact in different group => we can clone it and change group
					if len(items)!=0:
						i=items[0].clone() # clone contact item
						i.group=unicode(name)
						self.main.ui.roster.users.append(i)
						# update roster
						self.main.ui.roster.sortItems()
						#self.main.ui.roster.changePos=True
						self.main.ui.roster.repaint()
					# we have to create new item
					else:
						# add new contact to the roster
						self.main.ui.roster.addUser(contact.jid,contact.name,name)
						# get contacts show and status
						if len(contact.status)==2:
							show=contact.status[0]
							status=contact.status[1]
						else:
							if len(contact.status)==1:
								show=contact.status[0]
							else:
								show="offline"
							status=None
						# set show and status message
						for user in self.main.ui.roster.getUserItems(contact.jid):
							user.icon=self.main.getIcon(contact.jid,size="32x32",status=self.main.icons[self.main.shows[unicode(show)]])
							if self.main.shows[unicode(show)]!="9":
								user.hidden=False
							else:
								user.hidden=True
							user.statusMessage=status
							user.status=self.main.shows[unicode(show)]
						# update roster
						#self.main.ui.roster.statusLabel.hide()
						#self.main.ui.roster.changePos=True
						self.main.ui.roster.sortItems()
						self.main.ui.roster.repaint()
			# contact is not in this group, but he is still visible in roster, so we have to delete him
			else:
				for i in self.main.ui.roster.getUserItems(jid):
					if item.name==i.group:
						if item.all==1 and not item.name in toDel:
							toDel.append(unicode(item.name))
						self.main.ui.roster.users.remove(i)
						# update roster
						self.main.ui.roster.sortItems()
						self.main.ui.roster.repaint()
						#self.main.ui.roster.statusLabel.hide()
						break
		# delete all items marked as 'to delete'
		for i in toDel:
			if i!=self.main.ui.roster.specialName:
				del self.main.ui.roster.groups[i]
				self.main.ui.roster.sortItems()

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
		self.main.events.addBooleanEvent(self.delContact,[jid],None,[],mainWindow.tr("Remove contact?"),jid+unicode(mainWindow.tr(" removed your authorization. You won't see his status. Do you want to remove him/her from your contact list?")),height=100,name=jid,typ="unsubcsribed",icon=None)


	def on_DeleteContact(self,jid):
		"""
		Called when contact is deleted from roster.
		"""
		# go through all contact userItems and remove them
		for i in self.main.ui.roster.getUserItems(jid):
			#if self.main.ui.roster.item==i:
				#self.main.ui.roster.statusLabel.hide()
			self.main.ui.roster.users.remove(i)
		# update roster
		self.main.ui.roster.sortItems()
		self.main.ui.roster.repaint()

	def on_subscribe(self, frm,status):
		mainWindow=self.main
		if self.roster['users'].has_key(frm):
			frm=self.main.getJid(frm)
			if frm.userhost() in self.main.autoAdd.keys():
				self.sendPresence(frm.userhost(),None,status,None,'subscribed')
				del self.main.autoAdd[frm.userhost()]
			else:
				frm=frm.userhost()
				self.main.events.addBooleanEvent(self.sendPresence,[frm,None,status,None,'subscribed'],self.sendPresence,[frm,None,status,None,'unsubscribed'],header=mainWindow.tr('Authorize contact?'),text=mainWindow.tr('user ')+" "+unicode(frm)+' '+mainWindow.tr("wants to see your status."),name=frm,typ="subscribe",height=80)
		else:
			frm=self.main.getJid(frm)
			if frm.host in self.main.autoAdd.keys():
				self.addContact(frm.userhost(),"","",[self.main.autoAdd[frm.host]['group']])
				self.sendPresence(frm.userhost(),None,status,None,'subscribe')
				self.sendPresence(frm.userhost(),None,status,None,'subscribed')
			elif frm.userhost() in self.main.autoAdd.keys():
				self.addContact(frm.userhost(),"",self.main.autoAdd[frm.userhost()]['name'],[self.main.autoAdd[frm.userhost()]['group']])
				self.sendPresence(frm.userhost(),None,status,None,'subscribe')
				self.sendPresence(frm.userhost(),None,status,None,'subscribed')
				del self.main.autoAdd[frm.userhost()]
			else:
				self.main.events.addAddUserEvent(frm.userhost(),status)

	def _onSubscribe(self,frm,status,add=False):
		#def __init__(self,main,parent=None,jid="",group=None,name="",add=True):
		dialog=widgets.addcontact.addContactDialog(self.main,self.main,jid=frm,group="",name=frm.split('@')[0],add=add)
		dialog.exec_()
		self.sendPresence(frm,None,status,None,'subscribe')
		self.sendPresence(frm,None,status,None,'subscribed')


	def on_GCmessage(self, frm, typ, body, subject = None, xhtml = None,  chatstate = None,  delay = None, error = None):
		"""
		Handles messages from groupchat.
		"""
		# get user (resource) and MUC jid (saved in frm)
		start=time.time()
		if typ=="chat":
			return self.on_message(frm, typ, body, subject, xhtml,chatstate,delay,error)
		frm=jidT.JID(frm)
		if frm.resource:
			user=frm.resource
		else:
			user=frm.userhost()
		frm=frm.userhost()
		if xhtml:
			sXhtml=xhtml.strip().lower()
			if sXhtml.find("<script")!=-1:
				return
		#images in xhtml
		#if xhtml != None:
			#xhtml = self.main.getImages(xhtml,frm)
		if not body:
			body=""

		# find MUC tab
		for i in range(self.main.chat.ui.chatTab.count()):
			w=self.main.chat.ui.chatTab.widget(i)
			countMessage=False
			if unicode(w.jid) == frm:
				mainWindow=self.main
				#print 'error',error
				if error=="remote-server-not-found":
					if w!=None:
						message=self.main.webkitThemeFactory.genChatStatus(unicode(mainWindow.tr("Your message can't be sent. Remote server not found.")),self.main.now())
						w.chat.textEditWrite(message)
						w.chat.lastMessageFrom=""
					return
				elif error!=None:
					if w!=None:
						message=self.main.webkitThemeFactory.genChatStatus(unicode(mainWindow.tr("Your message can't be sent."))+" "+unicode(error),self.main.now())
						w.chat.textEditWrite(message)
						w.chat.lastMessageFrom=""
					return
				if len(body)!=0 and subject==None:
					if xhtml==None:
						body=unicode(body).replace('&','&amp;').replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")
						body = utils.replace_url(body,w.chat)
						body=body.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")
					else:
						xhtml=xhtml.replace("&quot;",'"')
					self.main.chat.onGCMessage(w,i,body,delay,subject,user,xhtml)
				if subject != None:
					
					w.chat.changeTopic(subject.replace("\n","<br/> "))
					
					if user != frm:
						message = unicode(subject)
					else:
						message = unicode(body)
					
					message=message.replace('&','&amp;').replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")
					message=utils.replace_url(message,w.chat)
					message=message.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")
					
					if user != frm:
						message = "%s %s %s" % (user, unicode(mainWindow.tr("has set the subject to:")), message)
					
					message = self.main.webkitThemeFactory.genChatStatus(message,self.main.now())
					
					w.chat.textEditWrite(message)
					w.chat.lastMessageFrom=""
				
				return


	def on_message(self, frm, typ, body, subject = None, xhtml = None,chatstate = None,  delay = None, error = None):
		"""
		Handles normal 'chat' messages.
		"""
		# get user icon or name, if we have him in roster. Or use default icon and jid as name
		if typ=="groupchat":
			return
		frm=jidT.JID(frm)
		if not body:
			body=""
		mainWindow=self.main
		# get user name
		user=self.main.ui.roster.getNameByJID(frm.full())
		icon=self.main.ui.roster.getIconByJID(frm.full())

		# test if xhtml contains dangerous tags
		if xhtml:
			sXhtml=xhtml.strip().lower()
			if sXhtml.find("<script")!=-1:
				return

		# get chatwidget of this conversation
		if self.groupchats.has_key(frm.userhost()):
			tab,tabIndex=self.main.chat.findTab(frm.full(),True)
			user=frm.resource
		else:
			tab,tabIndex=self.main.chat.findTab(frm.full())

		# handle errors
		if error=="remote-server-not-found":
			if tab!=None:
				message=self.main.webkitThemeFactory.genChatStatus(mainWindow.tr("Your message can't be sent. Remote server not found."),self.main.now())
				tab.chat.textEditWrite(message)
				tab.chat.lastMessageFrom=""
			return
		elif error!=None:
			if tab!=None:
				message=self.main.webkitThemeFactory.genChatStatus(mainWindow.tr("Your message can't be sent.")+" "+unicode(error),self.main.now())
				tab.chat.textEditWrite(message)
				tab.chat.lastMessageFrom=""
			return

		if len(body)!=0:
			# parse message body/xhtml
			if delay==None:
				timeText=self.main.now()
			else:
				timeText=time.strftime('%Y-%m-%d&nbsp;%H:%M:%S', time.localtime(delay))

			
			next=False
			if tab:
				if xhtml==None:
					message=unicode(body).replace('&','&amp;').replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")
					message = utils.replace_url(message,tab.chat)
					message=message.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")
				else:
					message=xhtml.replace("&quot;",'"')
					message=message.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")
				tab.chat.appendLastMessage(['in',user,message,timeText,tab.chat.file])
				if tab.chat.lastMessageFrom==unicode(user):
					insert=True
					message=self.main.webkitThemeFactory.genIncomingNextContent(user,message,timeText,tab.chat.file)
					next=True
				if not next:
					insert=False
					message=self.main.webkitThemeFactory.genIncomingContent(user,message,timeText,tab.chat.file)
				

			#colors=self.main.getSkinColors(0)
			#if colors!=None:
				#message=message.replace("[foreground]",colors[0]).replace("[background]",colors[1])
				#if len(colors)==3:
					#message=message.replace("[additive]",colors[2])

			# we have tab for this conversation opened
			if tab!=None:
				tab.chat.lastMessageFrom=unicode(user)
				# i think we don't have to check this....
				#try:
					#link = tab.chat.file
					#height = str(tab.chat.avatarHeight)
				#except:
					#print 'wtf? no chat.tab.file!'
					#link = 'images/32x32/apps/jabbim.png'
					#height = '32'
				#message=message.replace("[avatar]","<img src=\""+link+"\" width=\"32\" height=\""+height+"\" />")
				current=self.main.chat.ui.chatTab.currentWidget()
				# write message and set 'message' icon
				if int(self.main.chat.ui.chatTab.currentIndex())!=tabIndex:
					self.main.chat.ui.chatTab.setTabIcon(tabIndex,QtGui.QIcon("images/16x16/actions/message.png"))
					self.main.chat.ui.chatTab.tabBar().setTabTextColor(tabIndex,QtGui.QColor(255,0,0))
					self.main.chat.ui.chatTab.setTabText(tabIndex,"("+str(tab.chat.unread+1)+") "+tab.tabName)
					self.main.events.addInfoEvent(header=mainWindow.tr("Message"),text=mainWindow.tr("From: ")+unicode(user),name=unicode(frm.full()),typ='message',icon="images/xxxxx/actions/message.png",action=self.main.chat.activate,actionDict=[frm.full()],tooltip=mainWindow.tr("New message from ")+unicode(user))
					self.dispatcher.publishEvent('chatMessageEvent', frm,user,body,subject, xhtml, chatstate, delay,self.main.events.ID-1)
					tab.chat.unread+=1
					if not self.main.chat.isActiveWindow():
						#if current:
							#self.main.chat.setWindowTitle("("+str(int(self.main.chat.getUnreadMessages()))+") "+current.tabName.replace("&",""))
						self.main.chat.setWindowTitle("("+str(int(self.main.chat.getUnreadMessages()))+") "+tab.tabName.replace("&","")) 
				elif not self.main.chat.isActiveWindow():
					self.main.events.addInfoEvent(header=mainWindow.tr("Message"),text=mainWindow.tr("From: ")+unicode(user),name=unicode(frm.full()),typ='message',icon="images/xxxxx/actions/message.png",action=self.main.chat.activate,actionDict=[frm.full()],tooltip=mainWindow.tr("New message from ")+unicode(user))
					self.dispatcher.publishEvent('chatMessageEvent', frm,user,body,subject, xhtml, chatstate, delay,self.main.events.ID-1)
					#if int(self.main.chat.ui.chatTab.currentIndex())==tabIndex:
					#if current:
						#self.main.chat.setWindowTitle("("+str(int(self.main.chat.getUnreadMessages())+1)+") "+current.tabName.replace("&",""))
					self.main.chat.setWindowTitle("("+str(int(self.main.chat.getUnreadMessages())+1)+") "+tab.tabName.replace("&","")) 
					tab.chat.unread+=1
				else:
					color=self.main.chat.ui.chatTab.tabBar().palette().color(QtGui.QPalette.Foreground)
					self.main.chat.ui.chatTab.setTabText(tabIndex,tab.tabName)
					self.main.chat.ui.chatTab.tabBar().setTabTextColor(self.main.chat.ui.chatTab.currentIndex(),color)
					self.dispatcher.publishEvent('chatMessageEvent', frm,user,body,subject, xhtml, chatstate, delay,None)
				tab.chat.ui.chatstate.setText("")
				tab.chat.textEditWrite(message,insert)
				if tab.chat.first==True:
					tab.chat.first=False
				elif tab.chat.first==None:
					tab.chat.first=True
				#if tab.chat.first==True:
				if self.main.getJid(tab.chat.jid).resource !=frm.resource:
					tab.chat.jid=frm.full()
					tab.jid=frm.full()
					tab.chat.buildResourceMenu()
			else:
				# we have to add new chattab
				created=False
				if self.main.chat.isHidden():
					created=True
					self.main.chat.showMinimized()
				if len(body)>40:
						traytext=body[:40]+" ..."
				else:
						traytext=body
				text='<table><tr>'
				#if len(self.main.ui.roster.getUserItems(frm.userhost()))>0 and os.path.isfile(self.main.homeDir+'/avatars/'+unicode(frm.userhost())):
					#item=self.main.ui.roster.getUserItems(frm.userhost())[0]
					#pixmap=item.avatar.pixmap(64,64)
					#text+='<td><img src="'+self.main.homeDir+'/avatars/'+unicode(item.jid)+'" width="'+str(pixmap.width())+'" height="'+str(pixmap.height())+'"/></td>'
				text+='<td><b>'+mainWindow.tr("New message from ")+unicode(user)+'</b><br/>'
				text+='<font size="-1">'+traytext+'<br/>'
				text+="</td></tr></table>"
				self.main.events.addInfoEvent(header=mainWindow.tr("New message"),text=mainWindow.tr("From: ")+unicode(user),name=unicode(frm.full()),typ='message',icon="images/xxxxx/actions/message.png",action=self.main.chat.activate,actionDict=[],tooltip=text)
				if self.groupchats.has_key(frm.userhost()):
					self.main.chat.addChatTab(frm.full(),unicode(user),icon,True,full=True)
					tab,tabIndex=self.main.chat.findTab(frm.full(),True)
				else:
					self.main.chat.addChatTab(frm.full(),unicode(user),icon,True)
					tab,tabIndex=self.main.chat.findTab(frm.full())
				if created:
					self.main.chat.setWindowState(self.main.chat.windowState() & ~QtCore.Qt.WindowActive | QtCore.Qt.WindowMinimized )
					self.main.setWindowState(self.main.windowState() & QtCore.Qt.WindowActive)

				
				if tab:
					tab.chat.lastMessageFrom=unicode(user)
					if xhtml==None:
						message=unicode(body).replace('&','&amp;').replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")
						message = utils.replace_url(message,tab.chat)
						message=message.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")
					else:
						message=xhtml.replace("&quot;",'"')
						message=message.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")
					message=self.main.webkitThemeFactory.genIncomingContent(unicode(user),message,self.main.now(),tab.chat.file)
					#message=message.replace("[avatar]","<img src=\""+tab.chat.file+"\" width=\"32\" height=\""+unicode(tab.chat.avatarHeight)+"\" />")
					tab.chat.textEditWrite(message)
					self.main.chat.ui.chatTab.setTabIcon(tabIndex,QtGui.QIcon("images/16x16/actions/message.png"))
					self.main.chat.ui.chatTab.tabBar().setTabTextColor(tabIndex,QtGui.QColor(255,0,0))
					self.main.chat.ui.chatTab.setTabText(tabIndex,"("+str(tab.chat.unread+1)+") "+tab.tabName)
					tab.chat.appendLastMessage(['in',user,message,timeText,tab.chat.file])
					tab.chat.unread+=1
				self.dispatcher.publishEvent('firstChatMessageEvent', frm,user,body,subject, xhtml, chatstate,  delay, self.main.events.ID-1)

		if tab!=None:
			# handle checkstate messages:
			if chatstate=="composing":
				if self.main.chat.ui.chatTab.tabBar().tabTextColor(tabIndex).name()!=QtGui.QColor(255,0,0).name():
					self.main.chat.ui.chatTab.tabBar().setTabTextColor(tabIndex,QtGui.QColor(0,128,0))
				tab.chat.ui.chatstate.setText(mainWindow.tr("is typing..."))
			elif chatstate=="active":
				tab.chat.ui.chatstate.setText(mainWindow.tr("gives attention to chat."))
			elif chatstate=="paused":
				tab.chat.ui.chatstate.setText(mainWindow.tr("stops typing."))
			elif chatstate=="inactive":
				tab.chat.ui.chatstate.setText(mainWindow.tr("doesn't give attention to chat."))
			elif chatstate=="gone":
				tab.chat.ui.chatstate.setText(mainWindow.tr("closed the chat window."))

	def on_vcardReceived(self,  jid, card):
		"""
		Called when vcard is received.
		"""
		#TODO: zpracovat ukladani vcardu .. hash a cesta k souboru se ulozi do db
		if not self.roster['users'].has_key(jid):
			print jid+' is not in roster'
			return
		# Rename contact if he havent got nickname
		contact=self.roster['users'][jid]
		if (contact.name=="" or contact.name==contact.jid) or not contact.name:
			print 'trying to rename '+jid
			self.renameByVcard(card,jid)

	def on_avatarUpdate(self, jid):
		"""
		Called when avatar is upated.
		"""
		if not self.avatarDef.has_key(jid):
			return None
		# get avatar for this jid
		pixmap=self.main.getAvatar(jid,frame=False,status=None)
		if pixmap==None:
			return None
		# self avatar
		print "update avatar for",[jid]
		if unicode(self.jid.userhost())==unicode(jid):
			avatar=self.main.getAvatar(pixmap,size="64x64",frame=True)
			self.main.selfAvatar=pixmap
			self.main.ui.selfAvatar.setPixmap(avatar)
			self.main.ui.selfAvatar.setMinimumWidth(avatar.width()+3)

		# set avatar for userItems in roster
		#for item in self.main.ui.roster.getUserItems(jid):
			#item.setAvatar(QtGui.QIcon(pixmap))
		#for item in self.main.ui.roster.getMetaItems(jid):
			#item[0].setAvatar(QtGui.QIcon(pixmap))

		# set avatar for contacts in MUC
		jid = jidT.JID(jid)
		print "avatar look for",jid.userhost()
		w,i=self.main.chat.findTab(jid.userhost(),False,['groupchat'])
		print w
		if w:
			print [jid.resource]
			for item in w.chat.getUserItems(jid.resource):
				text=unicode(item.text(1))
				if len(text)!=0:
					item.setIcon(1,QtGui.QIcon(pixmap))
					
					result=self.main.getAvatar(pixmap,size="32x32",frame=False,status=self.main.icons[text[0]])
					item.setIcon(0,QtGui.QIcon(result))
					item.setToolTip(0,w.chat.getGroupchatTooltip(jid.full(),item))
					#w.chat.setTooltip(item,jid.full())

	def on_fileReceived(self, sid, id):
		autoDownload=False
		if unicode(sid) in self.main.allowedSids:
			if unicode(self.ft[sid].tojid).find("rpc@jabbim.cz")!=-1 and not unicode(sid) in self.main.allowedSids:
				return
			else:
				filename = self.main.realHomeDir+'/'+self.ft[sid].fileprops['name']
			autoDownload=True
		elif self.main.allowedJids.has_key(self.main.getJid(unicode(self.ft[sid].tojid)).userhost()+"/"+self.ft[sid].fileprops['name']):
			filename=self.main.allowedJids[self.main.getJid(unicode(self.ft[sid].tojid)).userhost()+"/"+self.ft[sid].fileprops['name']]+"/"+self.ft[sid].fileprops['name']
			autoDownload=True
		elif self.main.config['autoDownload'] == 'True' and unicode(self.ft[sid].tojid).find("rpc@jabbim.cz")==-1:
			filename = self.main.config['autoDownloadPath']+'/'+self.ft[sid].fileprops['name']
			autoDownload=True
		if autoDownload:
			if self.ft[sid].method!=None:
				return
			self.main.events.addFTDownloadEvent(unicode(self.ft[sid].tojid),basename(self.ft[sid].fileprops['name']),"",sid)
			
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
		else:
			if unicode(self.ft[sid].tojid).find("rpc@jabbim.cz")==-1:
				if self.ft[sid].fileprops.has_key('preview'):
					image=base64.decodestring(str(unicode(self.ft[sid].fileprops['preview'])))
					pixmap=QtGui.QPixmap()
					pixmap.loadFromData(image)
				else:
					pixmap=None
				#eventWidget=self.main.events.addBooleanEvent(self.ftStarted,[sid,id],None,[],self.main.tr("File transfer"),text= unicode(" %s is sending you file."%unicode(self.ft[sid].tojid)),height=40,name=unicode(self.ft[sid].tojid),typ="ftTransfer",icon=None)
				eventWidget=self.main.events.addFTReceivedEvent(sid,id,unicode(self.ft[sid].tojid),pixmap)
				tab,index=self.main.chat.findTab(unicode(self.ft[sid].tojid),typ=['chat'])
				if tab:
					mainWindow=self.main
					#w=widgets.chatwidget.FTAskWidget(self.ft[sid].fileprops['name'],eventWidget,tab.chat,tab.chat.ui.ftwidget)
					#QtCore.QObject.connect(eventWidget.submitButton,QtCore.SIGNAL("clicked(bool)"),w.accept)
					#QtCore.QObject.connect(eventWidget.closeButton,QtCore.SIGNAL("clicked(bool)"),w.reject)
					#if pixmap:
						#w.setPreview(pixmap)
					#tab.chat.ui.ftwidget.layout().addWidget(w)
					message=mainWindow.tr("User is sending you file")+" "+unicode(self.ft[sid].fileprops['name'])+". <a href=\"javascript:messageObject.acceptFT('"+unicode(sid)+"');\">["+mainWindow.tr("Accept")+"]</a> <a href=\"javascript:messageObject.rejectFT('"+unicode(sid)+"');\">["+mainWindow.tr("Decline")+"]</a>"
					tab.chat.ui.webkit.messageObject.ft[unicode(sid)]=eventWidget
					tab.chat.textEditWrite('<div id="ft'+unicode(sid)+'">'+self.main.webkitThemeFactory.genChatStatus(unicode(message),self.main.now())+"</div>")
					tab.chat.lastMessageFrom=""

	def _declineFT(self,sid):
		tab,index=self.main.chat.findTab(unicode(self.ft[sid].tojid),typ=['chat'])
		if tab:
			tab.chat.ui.webkit.page().mainFrame().evaluateJavaScript("removeById('ft"+unicode(sid)+"');")
			del tab.chat.ui.webkit.messageObject.ft[unicode(sid)]
		return self.declineFT(sid)

	def ftStarted(self,sid,id):
		#q = QtGui.QMessageBox.question(self.main,self.main.tr("File transfer"), unicode(" %s is sending you file."%unicode(self.ft[sid].tojid)),QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		#if q == QtGui.QMessageBox.Yes:
		mainWindow=self.main
		filename = QtGui.QFileDialog.getSaveFileName(self.main, mainWindow.tr("Save File"),self.ft[sid].fileprops['name'],mainWindow.tr("*.*"))
		tab,index=self.main.chat.findTab(unicode(self.ft[sid].tojid),typ=['chat'])
		if tab:
			tab.chat.ui.webkit.page().mainFrame().evaluateJavaScript("removeById('ft"+unicode(sid)+"');")
			del tab.chat.ui.webkit.messageObject.ft[unicode(sid)]
		if filename and len(filename)!=0:
			filename=unicode(filename)
			log.msg(unicode(filename))
			self.main.events.addFTDownloadEvent(unicode(self.ft[sid].tojid),basename(self.ft[sid].fileprops['name']),"",sid)
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
		self.main.ui.loginInfo.setText(mainWindow.tr("Jabbim is connecting to the server."))
		self.main.ui.splashProgress.setValue(20)
	
	def on_authd(self):
		print "on_authd called"
		mainWindow=self.main
		self.main.ui.loginInfo.setText(mainWindow.tr("Jabbim is logged in."))
		self.main.ui.splashProgress.setValue(40)
		print "i'm on_authd end...z"

class AvatarLabel(QtGui.QLabel):
	def __init__(self,main,parent):
		QtGui.QLabel.__init__(self,parent)
		self.setObjectName("selfAvatar")
		self.main=main
		self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
		self.setMinimumWidth(64)
		self.setAlignment(QtCore.Qt.AlignCenter)
	
	def mouseDoubleClickEvent(self,event):
		self.main.identityEditor()
		event.accept()

	def contextMenuEvent(self,event):
		self.main.offlineMenu.move(event.globalX(),event.globalY())
		self.main.offlineMenu.popup(QtCore.QPoint(event.globalX(),event.globalY()))
		event.accept()
	
	def refreshToolTip(self):
		if self.main.client:
			text = self.main.getToolTip(self.main.client.jid.userhost())
			self.setToolTip(text)
			# set tooltip also for tray icon
			# and utils.getWindowsVersion()!="vista"
			if sys.platform == 'win32':
				#contact = self.main.client.getContactByJid(jid)
				text=unicode(self.main.status.get(self.main.selfStatus, ''))
				self.main.tray.setToolTip(text)
			else:
				self.main.tray.setToolTip(text)

class avatarLoader(QtCore.QThread):
	def __init__(self,parent,path,avatarDef):
		QtCore.QThread.__init__(self,parent)
		self.path=path
		self.avatarDef=avatarDef

	def run(self):
		path=unicode(self.path)
		avatarDef=dict(self.avatarDef)
		hashe = []
		try:
			for hash in avatarDef.itervalues():
				if not hash in hashe and hash and hash!="None":
					hashe.append(unicode(str(hash)))
		except:
			message = unicode(traceback.format_exc(), 'utf-8')
			print message
		print "avatarLoader started",hashe
		frame=QtGui.QImage("images/32x32/frame.png")
		for hash in hashe:
			try:
				avatar=QtGui.QImage(path+'/'+hash)
				width=int(avatar.width())
				height=int(avatar.height())
				avatar=avatar.scaled(25,25,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
				result=QtGui.QImage(32,32,QtGui.QImage.Format_ARGB32)
				result.fill(QtCore.Qt.transparent)
				# we have to implement this one:
				#if os.path.exists("themes/"+self.config['theme']+"/frame-32.png"):
					#frame=QtGui.QImage("themes/"+self.config['theme']+"/frame-32.png")
				#else:
				painter=QtGui.QPainter(result)
				painter.drawImage((32-avatar.width())/2,(32-avatar.height())/2,avatar)
				painter.drawImage(0,0,frame)
				painter.end()
				self.emit(QtCore.SIGNAL("imageLoaded(QString,QImage,int,int)"),QtCore.QString(hash),QtGui.QImage(result),int(width),int(height))
			except:
				message = unicode(traceback.format_exc(), 'utf-8')
				print message
		

class mainWindow(QtGui.QMainWindow):
	def __init__(self,parent=None):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		self.ui=widgets.mainWindow.Ui_MainWindow()
		self.ui.setupUi(self)
		self.reator=reactor
		self.setObjectName("Jabbim class")
		#self.setWindowFlags(QtCore.Qt.Tool)#|QtCore.Qt.FramelessWindowHint)
		self.ui.toggleInvisible.hide()
		self.ui.statusButton.hide()
		self.qtStyles=map(unicode,list(QtGui.QStyleFactory.keys()))
		self.qtStylesDefault=app.style()
		app.main=self
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
		self.config=None #: config dict (loaded by configObj)
		self.cache=None
		self.connectStarted=0
		self.snarlMessages={}
		self.autoAdd={}
		self.version = '0.5 SVN' + utils.getSvnVersion() #: version string
		#self.setWindowOpacity (0.5) 
		

		QtCore.QObject.connect(app, QtCore.SIGNAL("sleep()"),self.systemSleep)
		QtCore.QObject.connect(app, QtCore.SIGNAL("wakeUp()"),self.systemWakeUp)

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

		self.reactor=reactor
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

		self.loadRoster() # load roster widget
		self.loadRosterStyle()
		QtCore.QObject.connect(self.ui.rosterSearch, QtCore.SIGNAL(" textEdited ( const QString & )"),self.ui.roster.search)
		QtCore.QObject.connect(self.ui.rosterSearchClose, QtCore.SIGNAL("clicked()"),self.ui.roster.search)

			
		self.ui.tabWidgetButton=QtGui.QToolButton(self.ui.tabWidget)
		self.ui.tabWidgetButton.setIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))
		self.ui.tabWidgetButton.setPopupMode(QtGui.QToolButton.InstantPopup)
		self.ui.tabWidgetButton.setArrowType(QtCore.Qt.NoArrow)
		self.ui.tabWidget.setCornerWidget(self.ui.tabWidgetButton)

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
		self.ui.actionStart_Chat.setEnabled(False)
		self.ui.actionPrivacy_list_editor.setEnabled(False)
		self.ui.actionIdentity.setEnabled(False)
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
		self.allowedJids={} # {jid:path_to_download_files}
		
		
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
		self.moodIcons={}
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
		self.setupShortcuts()
		self.delayedMessages = None
		#: {show:ID}
		self.shows={u"online":u"1",
					u"available":u"1",
					u"chat":u"0",
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
					u"0":u"chat",
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
		#mood:translation
		self.moods = {
					"none":self.tr("None"),
					"afraid":self.tr("afraid"),
					"amazed":self.tr("amazed"),
					"angry":self.tr("angry"),
					"annoyed":self.tr("annoyed"),
					"anxious":self.tr("anxious"),
					"aroused":self.tr("aroused"),
					"ashamed":self.tr("ashamed"),
					"bored":self.tr("bored"),
					"brave":self.tr("brave"),
					"calm":self.tr("calm"),
					"cold":self.tr("cold"),
					"confused":self.tr("confused"),
					"contented":self.tr("contented"),
					"cranky":self.tr("cranky"),
					"curious":self.tr("curious"),
					"depressed":self.tr("depressed"),
					"disappointed":self.tr("disappointed"),
					"disgusted":self.tr("disgusted"),
					"distracted":self.tr("distracted"),
					"embarrassed":self.tr("embarrassed"),
					"excited":self.tr("excited"),
					"flirtatious":self.tr("flirtatious"),
					"frustrated":self.tr("frustrated"),
					"grumpy":self.tr("grumpy"),
					"guilty":self.tr("guilty"),
					"happy":self.tr("happy"),
					"hot":self.tr("hot"),
					"humbled":self.tr("humbled"),
					"humiliated":self.tr("humiliated"),
					"hungry":self.tr("hungry"),
					"hurt":self.tr("hurt"),
					"impressed":self.tr("impressed"),
					"in_awe":self.tr("in_awe"),
					"in_love":self.tr("in_love"),
					"indignant":self.tr("indignant"),
					"interested":self.tr("interested"),
					"intoxicated":self.tr("intoxicated"),
					"invincible":self.tr("invincible"),
					"jealous":self.tr("jealous"),
					"lonely":self.tr("lonely"),
					"mean":self.tr("mean"),
					"moody":self.tr("moody"),
					"nervous":self.tr("nervous"),
					"neutral":self.tr("neutral"),
					"offended":self.tr("offended"),
					"playful":self.tr("playful"),
					"proud":self.tr("proud"),
					"relieved":self.tr("relieved"),
					"remorseful":self.tr("remorseful"),
					"restless":self.tr("restless"),
					"sad":self.tr("sad"),
					"sarcastic":self.tr("sarcastic"),
					"serious":self.tr("serious"),
					"shocked":self.tr("shocked"),
					"shy":self.tr("shy"),
					"sick":self.tr("sick"),
					"sleepy":self.tr("sleepy"),
					"stressed":self.tr("stressed"),
					"surprised":self.tr("surprised"),
					"thirsty":self.tr("thirsty"),
					"worried":self.tr("worried")
		}
		self.moodActions = {}
		self.activities = {
					"none":self.tr("None"),
					"buying_groceries":self.tr("buying_groceries"),
					"cleaning":self.tr("cleaning"),
					"cooking":self.tr("cooking"),
					"doing_maintenance":self.tr("doing_maintenance"),
					"doing_the_dishes":self.tr("doing_the_dishes"),
					"doing_the_laundry":self.tr("doing_the_laundry"),
					"gardening":self.tr("gardening"),
					"running_an_errand":self.tr("running_an_errand"),
					"walking_the_dog":self.tr("walking_the_dog"),
					"having_a_beer":self.tr("having_a_beer"),
					"having_coffee":self.tr("having_coffee"),
					"having_tea":self.tr("having_tea"),
					"having_a_snack":self.tr("having_a_snack"),
					"having_breakfast":self.tr("having_breakfast"),
					"having_dinner":self.tr("having_dinner"),
					"having_lunch":self.tr("having_lunch"),
					"cycling":self.tr("cycling"),
					"hiking":self.tr("hiking"),
					"jogging":self.tr("jogging"),
					"playing_sports":self.tr("playing_sports"),
					"running":self.tr("running"),
					"skiing":self.tr("skiing"),
					"swimming":self.tr("swimming"),
					"working_out":self.tr("working_out"),
					"at_the_spa":self.tr("at_the_spa"),
					"brushing_teeth":self.tr("brushing_teeth"),
					"getting_a_haircut":self.tr("getting_a_haircut"),
					"shaving":self.tr("shaving"),
					"taking_a_bath":self.tr("taking_a_bath"),
					"taking_a_shower":self.tr("taking_a_shower"),
					"day_off":self.tr("day_off"),
					"hanging_out":self.tr("hanging_out"),
					"on_vacation":self.tr("on_vacation"),
					"scheduled_holiday":self.tr("scheduled_holiday"),
					"sleeping":self.tr("sleeping"),
					"gaming":self.tr("gaming"),
					"going_out":self.tr("going_out"),
					"partying":self.tr("partying"),
					"reading":self.tr("reading"),
					"rehearsing":self.tr("rehearsing"),
					"shopping":self.tr("shopping"),
					"socializing":self.tr("socializing"),
					"sunbathing":self.tr("sunbathing"),
					"watching_tv":self.tr("watching_tv"),
					"watching_a_movie":self.tr("watching_a_movie"),
					"in_real_life":self.tr("in_real_life"),
					"on_the_phone":self.tr("on_the_phone"),
					"on_video_phone":self.tr("on_video_phone"),
					"commuting":self.tr("commuting"),
					"cycling":self.tr("cycling"),
					"driving":self.tr("driving"),
					"in_a_car":self.tr("in_a_car"),
					"on_a_bus":self.tr("on_a_bus"),
					"on_a_plane":self.tr("on_a_plane"),
					"on_a_train":self.tr("on_a_train"),
					"on_a_trip":self.tr("on_a_trip"),
					"walking":self.tr("walking"),
					"coding":self.tr("coding"),
					"in_a_meeting":self.tr("in_a_meeting"),
					"studying":self.tr("studying"),
					"writing":self.tr("writing")}

		self.activityGroups = {"doing_chores":[self.tr("doing_chores"),"buying_groceries","cleaning","cooking","doing_maintenance","doing_the_dishes","doing_the_laundry","gardening","running_an_errand","walking_the_dog"],
					"drinking":[self.tr("drinking"),"having_a_beer","having_coffee","having_tea"],
					"eating":[self.tr("eating"),"having_a_snack","having_breakfast","having_dinner","having_lunch"],
					"exercising":[self.tr("exercising"),"cycling","hiking","jogging","playing_sports","running","skiing","swimming","working_out"],
					"grooming":[self.tr("grooming"),"at_the_spa","brushing_teeth","getting_a_haircut","shaving","taking_a_bath","taking_a_shower"],
					# no substate... we don't allow it<= "having_appointment":self.tr("having_appointment"),
					"inactive":[self.tr("inactive"),"day_off","hanging_out","on_vacation","scheduled_holiday","sleeping"],
					"relaxing":[self.tr("relaxing"),"gaming","going_out","partying","reading","rehearsing","shopping","socializing","sunbathing","watching_tv","watching_a_movie"],
					"talking":[self.tr("talking"),"in_real_life","on_the_phone","on_video_phone"],
					"traveling":[self.tr("traveling"),"commuting","cycling","driving","in_a_car","on_a_bus","on_a_plane","on_a_train","on_a_trip","walking"],
					"working":[self.tr("working"),"coding","in_a_meeting","studying","writing"]}

		self.offline=False
		self.xmlConsole=XMLConsole(self)
		self.ui.showOffline.hide()
		self.ui.offlineButton.hide()

		# signals
		QtCore.QObject.connect(self.ui.login_connect, QtCore.SIGNAL("clicked()"),self.connect)
		#QtCore.QObject.connect(self.ui.toggleInvisible, QtCore.SIGNAL("clicked(bool)"),self.toggleInvisibility)
		QtCore.QObject.connect(self.ui.registerButton, QtCore.SIGNAL("clicked ()"),self.registerButtonClicked)
		QtCore.QObject.connect(self.ui.login_cancel, QtCore.SIGNAL("clicked ()"),self.connectCancel)
		QtCore.QObject.connect(self.ui.profilesList, QtCore.SIGNAL("currentIndexChanged ( const QString & )"),self.profileChanged)
		QtCore.QObject.connect(self.ui.mucBrowserButton, QtCore.SIGNAL("clicked ()"),self.mucBrowser)
		QtCore.QObject.connect(self.ui.statusMessage, QtCore.SIGNAL("clicked (bool)"),self.statusMessageClicked)
		#QtCore.QObject.connect(self.ui.statusLine, QtCore.SIGNAL("returnPressed ()"),self.statusLineFinished)
		QtCore.QObject.connect(self.ui.statusLine, QtCore.SIGNAL("editingFinished () "),self.statusLineFinished)
		QtCore.QObject.connect(self.ui.offlineButton, QtCore.SIGNAL("clicked ( bool)"),self.hideOffline)
		
		QtCore.QObject.connect(self.ui.actionAbout, QtCore.SIGNAL("triggered ( bool )"),self.about)
		QtCore.QObject.connect(self.ui.actionSupport, QtCore.SIGNAL("triggered ( bool )"),self.support)
		QtCore.QObject.connect(self.ui.actionSendJabbimLog, QtCore.SIGNAL("triggered ( bool )"),self.sendLog)
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
		QtCore.QObject.connect(self.ui.actionStart_Chat, QtCore.SIGNAL("triggered ( bool )"), self.startChatDialog)

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

		self.loadSkin() # load chat skin
		self.loadSounds() # load chat skin
		self.loadTheme() # load theme
		self.loadMoods() # load user moods icon
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

		#self.setGeometry(rect.width()-250,rect.y(),250,rect.y()+rect.height())
#		self.setWindowOpacity(0.5)
			
		self.reconnect = True # :# True = Jabbim will reconnect after disconnect
		self.active=True
		
		# fill login form
		self.fillLoginForm()
		# load cache and create tables
		if sys.platform != 'win32':
			self.cache = storage.Cache(db=utils.path(self.homeDir+u'/cache.db'))
		else:
			self.cache = storage.Cache(db=(unicode(self.homeDir)+u'/cache.db').encode('utf8')) #hack!
		self.cache.create_tables().addCallback(self.tables_created)
		self.ui.loginStatus.addItem(self.getIcon(status="online",size="16x16"), self.status["online"],QtCore.QVariant(QtCore.QStringList(["online",  ''])))
		self.ui.loginStatus.addItem(self.getIcon(status="chat",size="16x16"), self.status["chat"],QtCore.QVariant(QtCore.QStringList(["chat", ''])))
		self.ui.loginStatus.addItem(self.getIcon(status="away",size="16x16"), self.status["away"],QtCore.QVariant(QtCore.QStringList(["away", ''])))
		self.ui.loginStatus.addItem(self.getIcon(status="xa",size="16x16"), self.status["xa"],QtCore.QVariant(QtCore.QStringList(["xa", ''])))
		self.ui.loginStatus.addItem(self.getIcon(status="dnd",size="16x16"), self.status["dnd"],QtCore.QVariant(QtCore.QStringList(["dnd", ''])))

		self.emoticonsWidget=widgets.emoticonswidget.emoticonsWidget(self,self)

		#if self.config['rosterMode'] == "compact":
		#	self.ui.roster.setRosterStyle(widgets.compactrosterstyle.rosterStyle)
		#else:
#			self.ui.roster.setRosterStyle(widgets.defaultrosterstyle.rosterStyle)
		if self.config['rosterScrollBar']=="True":
			self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
			QtCore.QObject.disconnect(self.scroll.verticalScrollBar(),QtCore.SIGNAL("valueChanged ( int )"),self.ui.roster.sliderChanged)
		else:
			self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
			QtCore.QObject.connect(self.scroll.verticalScrollBar(),QtCore.SIGNAL("valueChanged ( int )"),self.ui.roster.sliderChanged)

		#self.loadRosterStyle() # load roster style

		# join if we can :)
		if self.config['autoJoin']=='True':
			self.connect()

	def systemSleep(self):
		print "sleep emitted, disconnecting"
		self.sendPresence(None,"offline",self.tr("System is suspended"))
	
	def systemWakeUp(self):
		print "wakeUp emitted, connecting"
		self.connect()

	#{ Public functions

	def getJid(self,jid):
		"""
		Returns Twisted Jabber ID or None if JID is in bad format.
		@type jid: unicode
		@param jid: profiles Jabber ID
		@rtype: twisted JID
		@return: Twisted Jabber ID or None
		"""
		try:
			jidt=jidT.JID(jid)
		except:
			return None
		return jidt

	def sendFiles(self,jid):
		"""
		Opens dialog for sending files.
		@type jid: unicode
		@param jid: JID
		"""
		# get files
		dialog = QtGui.QFileDialog()
		dialog.setResolveSymlinks(True)
		file=dialog.getOpenFileNames(self,self.tr("Choose files"))
		file=list(file)

		new=[] # temp variable
		for f in file:
			if unicode(f).endswith('.lnk'):
				f = utils.getFilenameFromLnk(unicode(f))
			if isfile(unicode(f)):
				new.append(unicode(f))
		file=new # path to files
		if len(file)!=0:
			self.showFiletransferDialog(file,jid)

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

	
	def getImage(self,file,size=None):
		"""
		Returns deffered where is QImage loaded.
		@type file: unicode
		@param file: path to file
		@type size: list of integers
		@param size: [width,height] which are used for resizing image
		"""
		d=threads.deferToThread(self._getImage,file,size)
		return d
	
	def getToolTip(self,jid, name = None):
		"""
		returns html for setToolTip
		@type jid: unicode
		@param jid: jid of contact 
		"""
		jidfull = jid
		jid = jidT.JID(jid).userhost()
 
		text='<table><tr>'
		if self.client.avatarDef.get(jid, False):
			if self.client.avatarImg.has_key(self.client.avatarDef[jid]):
				if self.client.avatarImg[self.client.avatarDef[jid]] and self.client.avatarDef[jid]!="None":
					width=self.client.avatarImg[self.client.avatarDef[jid]][1]
					if width!=0:
						height=self.client.avatarImg[self.client.avatarDef[jid]][2]
						height=height/(float(width)/64.0)
						text+='<td><img src="'+self.realHomeDir+'/avatars/'+unicode(self.client.avatarDef[jid])+'" width="64" height="'+str(height)+'"/></td>'
		else:
			#if there is no avatar for given JID, then try to use avatar from any metacontact
			meta = self.ui.roster.getMetaItems(jid)
			print meta
			for itm in meta:
				j = itm[1]
				print j
				if self.client.avatarDef.get(j, False):
					if self.client.avatarImg.has_key(self.client.avatarDef[j]):
						if self.client.avatarImg[self.client.avatarDef[j]] and self.client.avatarDef[j]!="None":
							width=self.client.avatarImg[self.client.avatarDef[j]][1]
							if width!=0:
								height=self.client.avatarImg[self.client.avatarDef[j]][2]
								height=height/(float(width)/64.0)
								text+='<td><img src="'+self.realHomeDir+'/avatars/'+unicode(self.client.avatarDef[j])+'" width="64" height="'+str(height)+'"/></td>'
								break
						
		if name != None:
			text+='<td><b>'+self.tr("Name:")+'</b> '+name+'<br/>'
		else:
			text+='<td>'
		text+='<b>'+self.tr("JID:")+'</b> '+jidfull+'<br/>'
		contact = self.client.getContactByJid(jid)
		if contact == None:
			contact = self.client.getMucContactByJid(jidfull)
			if contact != None:
				status = contact.status
				if not status:
					status = ""
				text+='<img src="images/16x16/status/jabber-%s.png">' % contact.show 
				text+='<b>%s</b> '%unicode(self.status.get(contact.show, ''))
				if len(status) != 0:
					text+='<br /><font size="-1">%s</font>' % (status.replace('\n', '<br />'))
			text+="</td></tr></table>"
			return text
			
		if unicode(contact.subscription) == 'from':
			text+='<b>'+self.tr("Subscription:")+'</b> '+self.tr(" from")+'<br/>'
		elif unicode(contact.subscription) == 'to':
			text+='<b>'+self.tr("Subscription:")+'</b> '+self.tr(" to")+'<br/>'
		elif unicode(contact.subscription) == 'none':
			text+='<b>'+self.tr("Subscription:")+'</b> '+self.tr(" none")+'<br/>'	
		n =0

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
			if n>0:
				text+='<br />'
			text+='<img src="images/16x16/status/jabber-%s.png">' % contact.resources[res].show # hodilo by se rozlisit k jakymu poatri transportu
			text+='<b>%s</b> ' % unicode(self.status.get(contact.resources[res].show, ''))
			if res != None:
#							text+='<b>%s</b> %s<br>' % ( res, priority)
				text+='%s' % (priority)
			identity = contact.resources[res].identity
			if identity != '' and identity != None and identity != 'client/pc' and identity.startswith('client'):
				text+=' %s' % (identity)
			if len(status) != 0:
				text+='<br /><font size="-1">%s</font>' % (status.replace('\n', '<br />'))
			n+=1
		tune = contact.getPEP('http://jabber.org/protocol/tune')
		if type(tune) == list:
			for x in tune:
				print x
		elif tune!=None:
			artist = title = ''
			for el in tune.elements():
				if el.name == 'artist':
					artist = unicode(el)
				elif el.name == 'title':
					title = unicode(el)
			t = '%s: %s'%(artist, title)
			if len(t.strip())>1:
				text+='<br /><img src="images/22x22/icons/headphones.png" /><font size="-1">%s</font>' % (t) #ikonka se este muze menit ;)
		
		mood = contact.getPEP('http://jabber.org/protocol/mood')
		if mood != None:
			t = ''
			m = txt = icon = ''
			for el in mood.elements():
				if el.name == 'text':
					txt = unicode(el)
				else:
					m = self.moods.get(el.name)
					if self.moodIcons.has_key(el.name):
						icon="<img src=\"%s\" />" % self.moodIcons[el.name].src
					else:
						icon=""
			if txt != '':
				t = m+ ' - %s'%txt
			else:
				t = m
			text+='<br />%s<font size="-1">%s</font>' % (icon,t)
		
		activity = contact.getPEP('http://jabber.org/protocol/activity')
		if activity != None:
			txt = ''
			general = ''
			spec = ''
			for el in activity.elements():
				if el.name == 'text':
					txt = unicode(el)
				else :
					general = el.name
					if self.activityGroups.has_key(general):
						general=self.activityGroups[general][0]
					spec = el.firstChildElement().name
					if self.activities.has_key(spec):
						spec=self.activities[spec]

			text+='<br /><font size="-1"><b>%s</b> %s %s</font>' % (general, spec, txt)
		chat = contact.getPEP('http://www.xmpp.org/extensions/xep-0194.html#ns')
		if chat != None:
			if type(chat) == list:
				print 'vice roomu'
				text+='<br /><b>'+self.tr('User is chatting in:')+'</b>'
				for itm in chat:
					uri = name = ''
					for el in itm.elements():
						if el.name == 'uri':
							uri = unicode(el)
							if uri.startswith('xmpp:'):
								uri = uri.replace('xmpp:', '')
						elif el.name == 'name':
							name = unicode(el)
					text+= '<br /><font size="-1">%s %s</font>'%(name, uri)
			else:
				print 'jeden room'
				uri = name = ''
				if len(chat.children)>0:
					text+='<br /><b>'+self.tr('User is chatting in:')+'</b>'
					for el in chat.elements():
						if el.name == 'uri':
							uri = unicode(el)
							if uri.startswith('xmpp:'):
								uri = uri.replace('xmpp:', '')
						elif el.name == 'name':
							name = unicode(el)
						text+= '<br /><font size="-1">%s %s</font>'%(name, uri)					
		text+="</td></tr></table>"
		return text

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
#				self.client.factory.stopTrying()
				self.reconnect = False
				self.client.disconnect()
				# update avatar tooltip and tray tooltip
				self.ui.selfAvatar.refreshToolTip()
			else:
				self.client.oldstatus = (show, message)
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
				icon=QtGui.QIcon("images/16x16/apps/jabbim.png")
				if self.selfStatus!='online':
					result=icon.pixmap(16,16)
					painter=QtGui.QPainter(result)
					icon=self.getIcon(status=unicode(self.selfStatus),size="16x16")
					painter.drawPixmap(0,0,icon.pixmap(16,16))
					painter.end()
				else:
					result=icon
				self.currentTrayIcon=QtGui.QIcon(result)
				self.tray.setIcon(self.getCurrentTrayIcon())
				# update avatar tooltip and tray tooltip
				self.ui.selfAvatar.refreshToolTip()
				
				# send presence to the server
				self.client.sendPresence(show = unicode(show), status = unicode(message),priority=pri)
				
				# send presence to groupchats
				for muc in self.client.groupchats.itervalues():
					self.client.sendPresence(show = unicode(show), status = unicode(message), to = '%s/%s'%(muc.jid, muc.nick))
				
				# send presence to all transports
				#for transport in self.transports.keys():
					#self.client.sendPresence(show = unicode(show), status = unicode(message), to = transport)
				
				# update statusWidget
				if len(message)>20:
					self.ui.statusMessage.setText(unicode(message)[:20]+"...")
				elif len(message)==0:
					self.ui.statusMessage.setText(unicode(self.status[show]))
				else:
					self.ui.statusMessage.setText(unicode(message))
				self.ui.statusMessage.setIcon(self.getIcon(status=show,size="16x16"))

		else:
			if self.transports[jid]!=None:
				self.transports[jid].setIcon(self.getIcon('1@'+jid,status=unicode(show),size="16x16"))

				text='<table><tr>'
				if os.path.isfile(self.homeDir+'/avatars/'+unicode(self.config['jid'])):
					pixmap=QtGui.QIcon(self.homeDir+'/avatars/'+unicode(self.config['jid'])).pixmap(64,64)
					text+='<td><img src="'+self.homeDir+'/avatars/'+unicode(self.config['jid'])+'" width="'+str(pixmap.width())+'" height="'+str(pixmap.height())+'"/></td>'
				#text+='<td><b>'+self.tr("Name:")+'</b> '+item.escapedName+'<br/>'
				text+='<td><b>'+self.tr("JID:")+'</b> '+unicode(jid)+'<br/>'

				#status = unicode(message)
				#priority = pri
				#if priority != None:
					#priority = "(%s: %s)" % (self.tr("Priority"),priority)
				#else:
					#priority = ""
				usertype=unicode(self.client.getHostType(jid,jid))
				if os.path.isfile('images/16x16/status/'+usertype+"-"+show+".png"):
					text+='<img src="images/16x16/status/'+usertype+"-"+show+'.png" />'
				else:
					text+='<img src="images/16x16/status/jabber-%s.png">' % show
				#if len(priority)!=0:
					#text+='%s<br/>' % priority
				if message:
					text+='<font size="-1">%s</font>' % (message)
				text+="</td></tr></table>"
				self.transports[jid].setToolTip(text)
				
			# send presence
			self.client.sendPresence(to=jid,show = unicode(show), status = unicode(message),priority=pri)

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

	def getAvatarSrc(self,jid):
		hash=""
		if self.client.avatarDef.has_key(jid):
			hash=self.client.avatarDef[jid]
		if hash=="":
			file=os.getcwd()+"/images/32x32/apps/jabbim.png"
		else:
			file=self.realHomeDir+'/avatars/'+unicode(hash)
		return file
			
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
		if not self.client:
			return None
		#keysToDel=[]
		#for key,avatar in self.client.avatarImg.iteritems():
			#if len(unicode(key).split('/'))!=1:
				#if sys.getrefcount(avatar)==4:
					#print "Unused chached avatar",key,avatar,sys.getrefcount(avatar)
					#keysToDel.append(str(key))
		#for key in keysToDel:
			#del self.client.avatarImg[key]
		if not pixmap:
			return None
		if isinstance(pixmap,unicode) or isinstance(pixmap,str):
			hash=""
			if self.client.avatarDef.has_key(pixmap):
				hash=self.client.avatarDef[pixmap]
			if hash=="":
				file=self.realHomeDir+'/avatars/'+unicode(pixmap)
			else:
				file=self.realHomeDir+'/avatars/'+unicode(hash)
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
				frame1=QtGui.QPixmap("themes/"+self.config['theme']+"/frame-"+str(size)+".png")
			else:
				frame1=QtGui.QPixmap("images/"+str(size)+"/frame.png")
			painter=QtGui.QPainter(result)
			painter.drawPixmap((x-avatar.width())/2,(y-avatar.height())/2,avatar)
			painter.drawPixmap(0,0,frame1)
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
			result=QtGui.QPixmap(file)

		return result

	def getCurrentTrayIcon(self):
		"""
		Returns current tray icon according to show.
		@rtype: QtGui.QIcon
		@return: current tray icon
		"""
		return self.currentTrayIcon

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
				host=jid.split("@")[1].split('/')[0]
			else:
				host=jid.split('/')[0]
			if self.client.disco.has_key(host):
				usertype=unicode(self.client.getHostType(host,jid))
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

	def now(self,shift=0):
		"""
		Returns current time in format hh:mm:ss
		@rtype: unicode
		@return: current time in format hh:mm:ss
		"""
		h,m,s=time.localtime(time.time()+shift)[3:6]
		return "%02d:%02d:%02d" % (h,m,s)

	def joinGC(self,jid,nickname):
		"""
		Joins to groupchat.
		@type jid: unicode
		@param jid: Groupchats Jabber ID
		@type nickname: unicode
		@param nickname: users nickname
		"""
		if self.chat.addGroupChatTab(jid,nickname):
			self.client.joinGC(jid, nickname,sendRooms=self.config['sendRooms']=="True")

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

	#{ Private functions

	def setupShortcuts(self):
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["nextTab"]), self.chat,self.chat.next)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["previousTab"]), self.chat,self.chat.previous)
 		
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["removeTab"]), self.chat,self.chat.removeTab)
 
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabOne"]), self.chat,self.chat.tabOne)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabTwo"]), self.chat,self.chat.tabTwo)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabThree"]), self.chat,self.chat.tabThree)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabFour"]), self.chat,self.chat.tabFour)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabFive"]), self.chat,self.chat.tabFive)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabSix"]), self.chat,self.chat.tabSix)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabSeven"]), self.chat,self.chat.tabSeven)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabEight"]), self.chat,self.chat.tabEight)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabNine"]), self.chat,self.chat.tabNine)
 
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["moveRight"]), self.chat,self.chat.moveRight,self.chat.moveRight)
		QtGui.QShortcut(QtGui.QKeySequence(self.config["moveLeft"]), self.chat,self.chat.moveLeft,self.chat.moveLeft)

	def statusLineCanceled(self):
		"""
		Called when user cancels to change topic by statusLine
		"""
		self.ui.statusLine.hide()
		self.ui.statusMessage.show()

	def statusLineFinished(self):
		"""
		Called when user finish with changing status message by statusLine
		"""
		status=unicode(self.ui.statusLine.text())
		contact = self.client.roster['users'][self.client.jid.userhost()]
		print [status,contact.resources[self.client.jid.resource].status]
		if len(status)==0 and not contact.resources[self.client.jid.resource].status:
			status=None
		
		if contact.resources[self.client.jid.resource].status!=status:
			self.sendPresence(None,self.selfStatus,status)
		self.ui.statusLine.hide()
		self.ui.statusMessage.show()

	def statusMessageClicked(self,b):
		"""
		Called when user click on statusMessage.
		"""
		self.ui.statusMessage.hide()
		contact = self.client.roster['users'][self.client.jid.userhost()]
		if contact.resources[self.client.jid.resource].status:
			self.ui.statusLine.setText(unicode(contact.resources[self.client.jid.resource].status))
		else:
			self.ui.statusLine.setText("")
		self.ui.statusLine.show()
		self.ui.statusLine.setFocus(QtCore.Qt.MouseFocusReason)

	def buildOfflineMenu(self):
		"""
		Builds menu with 'show offline', 'show away' etc. There are selfResources (if user is connected from more than one client) too.
		"""
		# make Show offline QAction
		self.offlineMenu=QtGui.QMenu()
		
		# change vcard action
		self.showChangeAvatar=self.offlineMenu.addAction(self.tr("Change profile photo"))
		self.showChangeAvatar.setCheckable(False)
		self.showChangeAvatar.setObjectName('change_avatar')
		self.showChangeAvatar.setIcon(QtGui.QIcon("images/16x16/categories/v-card.png"))
		QtCore.QObject.connect(self.showChangeAvatar, QtCore.SIGNAL("triggered ( bool )"),self.identityEditor)
		self.offlineMenu.addSeparator()
		
		# show offline contacts action
		self.showOfflineAction=self.offlineMenu.addAction(self.tr("Show Offline"))
		self.showOfflineAction.setCheckable(True)
		self.showOfflineAction.setObjectName('show_offline')
		self.showOfflineAction.setChecked(self.offline)
		QtCore.QObject.connect(self.showOfflineAction,QtCore.SIGNAL("toggled ( bool )"),self.hideOffline)

		# show transports action
		action=self.offlineMenu.addAction(self.tr("Show transports"))
		action.setCheckable(True)
		action.setObjectName('show_transports')
		if self.config['showTransports']=='True':
			action.setChecked(True)
		# make Toggle Invisibility QAction
		#self.toggleInv=self.offlineMenu.addAction(self.tr("Become invisible"))
		#self.toggleInv.setObjectName("toggle_invisible")
		
		# add resources connected to the our JID (selfResources)
		if len(self.selfResources)!=0:
			for resource in self.selfResources:
				if resource!=self.client.jid.resource:
					menu=QtGui.QMenu(unicode(resource),self.offlineMenu)
					# resource supports adhoc commands
					action=menu.addAction(self.tr("Commands"))
					action.setObjectName('commands')
					action.setData(QtCore.QVariant(unicode(resource)))
					# send file QAction
					action=menu.addAction(self.tr("Send file"))
					action.setObjectName('send_file')
					action.setData(QtCore.QVariant(unicode(resource)))
	
					self.offlineMenu.addMenu(menu)
			self.offlineMenu.addSeparator()

		#self.ui.showOffline.setMenu(self.offlineMenu)
		QtCore.QObject.connect(self.offlineMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.offlineMenuChanged)
		QtCore.QObject.connect(self.offlineMenu, QtCore.SIGNAL("hovered ( QAction *)"),self.offlineMenuHovered)
		
		# refresh selfAvatar tooltip, because some resource could be added
		self.ui.selfAvatar.refreshToolTip()
		self.ui.tabWidgetButton.setMenu(self.offlineMenu)

	def offlineMenuHovered(self, action):
		"""
		Called when offline menu is hovered.
		"""
		cmd=unicode(action.objectName())
		if cmd=='commands' and action.menu() == None:
			# show adhoc menu
			self.cmds = widgets.commands.Commands(self, unicode(self.client.jid.userhost())+"/"+unicode(action.data().toString()), action)

	def offlineMenuChanged(self,action):
		"""
		Executes command according to action.objectName(). Called when user choose one of QAction from self.offlineMenu, which si created by self.buildOfflineMenu().
		@type action: QAction
		@param action: QAction from self.offlineMenu
		"""
		cmd=action.objectName()
		if cmd=='send_file':
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
			self.ui.roster.setSize()
			self.ui.roster.repaint()
		elif cmd=="toggle_invisible":
			if self.toggleInv.text() == self.tr("Become invisible"):
				self.toggleInv.setText(self.tr("Become visible"))
				self.toggleInvisibility(True)
			else:
				self.toggleInv.setText(self.tr("Become invisible"))
				self.toggleInvisibility(False)

	def tables_created(self,data):
		"""
		Called on __init__ when new sqlite tables were created. If tables were empty, adds default values (default status messages etc.), otherwise calls self.buildStatusWidgetMenu().
		"""
		print "tables_created"
		d = None
		for result in data:
			assert result[0]
			print "table '%s' was %s" % (result[1]['table_name'], ('loaded','created')[result[1]['created']])
			if result[1]['created'] and result[1]['table_name'] == 'status':
				t1=self.cache.set_status('online',self.tr("I'm here"))
				t2=self.cache.set_status('dnd',self.tr("Doing something important. Message me later."))
				t3=self.cache.set_status('chat',self.tr("Chat with me!"))
				t4=self.cache.set_status('xa',self.tr("Leave a message. Beep"))
				t5=self.cache.set_status('away',self.tr("Doing something else for a moment."))
				d = DeferredList([t1,t2,t3,t4,t5], consumeErrors = False)
				d.addCallback(self.status_table_updated).addErrback(self._error)
		if d == None:
			self.buildStatusWidgetMenu()

	def status_table_updated(self, data=None):
		"""
		Called when status table is modified. Calls self.buildStatusWidgetMenu().
		"""
		print 'status table updated'
		self.buildStatusWidgetMenu()

	def _error(self,result):
		"""
		Called if there was some error with using DB.
		"""
		log.msg( 'CHYBA V DATABAZI?!!! ')
		print result

	def _getImage(self,file,size):
		image=QtGui.QImage(file)
		if size:
			image=image.scaled(size[0],size[1],QtCore.Qt.KeepAspectRatio)#,QtCore.Qt.SmoothTransformation)
		return image

	def buildTrayMenu(self):
		"""
		Builds system tray menu.
		"""
		menu=QtGui.QMenu(self)
		if self.client:
			menu.addMenu(self.statusWidgetMenu)
		else:
			menu.addAction(self.tr("Connect"),self.connect)
		if len(self.config['commandsInTray'])!=0 and self.client:
			menu.addSeparator()
			for jid in self.config['commandsInTray']:
				action=menu.addAction(self.ui.roster.getNameByJID(jid))
				action.setObjectName("cmd"+unicode(jid))
				action.setData(QtCore.QVariant(jid))
		menu.addSeparator()
		action=menu.addAction(self.tr("Hide / Show"),self.trayActivated)
		menu.addAction(self.tr("Quit"),self.trayQuit)
		menu.connect(menu, QtCore.SIGNAL("hovered ( QAction * )"),self.trayMenuHovered)
		self.tray.setContextMenu(menu)

	def trayMenuHovered(self,action):
		cmd=unicode(action.objectName())
		if cmd.startswith("cmd") and action.menu() == None:
			jid=unicode(action.data().toString())
			self.cmdMenu = widgets.commands.Commands(self, jid, action)

	def buildMoodMenuAction(self, m, current_mood):
		action = self.moodMenu.addAction(self.moods[m])
		if m != 'none' and self.moodIcons.has_key(m):
			action.setIcon(self.moodIcons[m])
		action.setData(QtCore.QVariant(m))
		action.setObjectName('mood')
 		if current_mood == m:
 			font = QtGui.QFont()
 			font.setBold(True)
 		else:
 			font = QtGui.QFont()
 			font.setBold(False)
 		action.setFont(font)
		self.moodActions[m] = action
		return action

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
		if not self.client:
			self.statusWidgetMenu.setEnabled(False)
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
					font=action.font()
					font.setItalic(True)
					action.setFont(font)
				self.statusWidgetMenu.addSeparator()
				separator=False
			else:
				separator=True
		if separator:
			self.statusWidgetMenu.addSeparator()
		

		if self.client != None and self.client.pep :
			self.ui.moodButton.show()
			# User Mood hack
			#self.moodMenu = self.statusWidgetMenu.addMenu(self.tr('Mood'))
			self.moodMenu = QtGui.QMenu(self.tr('Mood'))
 			items = self.moods.items()
 			items.sort(cmp=lambda a,b: strcoll(unicode(a[1]),unicode(b[1])))
 			keys = [ k for k,_ in items ]
 			current_mood = 'none'
			# XXX: getPEP always returns None here for me. I only receive
			# the initial mood later in on_pep. If it's always like that,
			# we can remove the following code and simplify some more.
			contact = self.client.getContactByJid(self.client.jid.userhost())
 			if contact != None:
 				moods = contact.getPEP('http://jabber.org/protocol/mood')
 				log.msg("buildStatusWidgetMenu getPEP moods=%s" % str(moods))
 				if moods != None:
 					for el in moods.elements():
 						if el.name in self.moods.keys():
 							current_mood = el.name
 							break

			current_action = self.buildMoodMenuAction('none', current_mood)
			self.moodMenu.addSeparator()
			for m in keys:
				if m != "none":
					action = self.buildMoodMenuAction(m, current_mood)
					if current_mood == m:
						current_action = action

			self.moodMenu.currentAction=current_action
			if self.moodIcons.has_key(current_mood):
				self.ui.moodButton.setIcon(self.moodIcons[current_mood])
			app.connect(self.moodMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.moodChanged)
			moodButtonRoot=QtGui.QMenu(self.ui.moodButton)
			moodButtonRoot.addMenu(self.moodMenu)
			if self.config['sendMood'] != 'True':
				self.moodMenu.setEnabled(False)
			activity =  QtGui.QMenu(self.tr('Activity'),moodButtonRoot)
			#activity =  self.statusWidgetMenu.addMenu(self.tr('Activity'))
			app.connect(activity, QtCore.SIGNAL("triggered ( QAction *)"),self.activityChanged)
			if self.config['sendActivity'] != 'True':
				activity.setEnabled(False)
			t = self.activities['none']
			action = activity.addAction(t)
			action.setObjectName('activity')
			action.setData(QtCore.QVariant(QtCore.QStringList(['none'])))
			activity.addSeparator()
			for group, txt in self.activityGroups.iteritems():
				menu = activity.addMenu(txt[0])
				#keys = self.activities.keys()
				#keys.sort()
				for a in txt[1:]:
					t = self.activities[a]
					action = menu.addAction(t)
					action.setObjectName('activity')
					action.setData(QtCore.QVariant(QtCore.QStringList([group, a])))
			moodButtonRoot.addMenu(activity)
			self.ui.moodButton.setMenu(moodButtonRoot)
		else:
			self.ui.moodButton.hide()
		
		# make menu for transports
		if len(self.transports)!=0:
			self.ui.line1.show()
			for transport in list(self.transports.keys()):
				# make transports QMenu and use icon according to transports type and show
				show=self.client.roster['users'][transport].status
				if len(show)==0:
					show='offline'
				else:
					show=show[0]

				# We have to use status icon from previous instance of QMenu,
				# because transport doesn't need to have the same show in roster as we send him before
				# So FE we sent away, but in roster we have still online...
				if self.transports[transport]:
					continue
					#ic=QtGui.QIcon(self.transports[transport].icon())
					#self.ui.hboxlayout4.removeWidget(self.transports[transport])
					#self.transports[transport].setParent(None)
					#self.transports[transport].deleteLater()
				else:
					ic=self.getIcon("1@"+transport,status=show,size="16x16")

				self.transports[transport]=QtGui.QToolButton(self.ui.offlineButton.parent())
				self.transports[transport].setMaximumSize(QtCore.QSize(16777215,20))
				self.transports[transport].setIcon(ic)

				text='<table><tr>'
				if os.path.isfile(self.homeDir+'/avatars/'+unicode(self.config['jid'])):
					pixmap=QtGui.QIcon(self.homeDir+'/avatars/'+unicode(self.config['jid'])).pixmap(64,64)
					text+='<td><img src="'+self.homeDir+'/avatars/'+unicode(self.config['jid'])+'" width="'+str(pixmap.width())+'" height="'+str(pixmap.height())+'"/></td>'
				#text+='<td><b>'+self.tr("Name:")+'</b> '+item.escapedName+'<br/>'
				text+='<td><b>'+self.tr("JID:")+'</b> '+unicode(transport)+'<br/>'

				usertype=unicode(self.client.getHostType(transport,transport))
				if os.path.isfile('images/16x16/status/'+usertype+"-offline.png"):
					text+='<img src="images/16x16/status/'+usertype+'-offline.png" />'
				else:
					text+='<img src="images/16x16/status/jabber-offline.png">'
				#text+='<font size="-1">%s</font>' % (status)
				text+="</td></tr></table>"
				self.transports[transport].setToolTip(text)

				menu=QtGui.QMenu(transport,self.transports[transport])
				menu.setIcon(self.getIcon(status=show,size="16x16"))
				# add custom messages and shows QActions to the transports QMenu
				# it's the same code (principle) as above, but it uses different QAction.data(),
				# so we can recognize if user wants to send presence to the transport instead of server
				separator=False
				for key in ['online','chat','away','xa','dnd']:
					if separator and len(config[key])!=0:
						menu.addSeparator()
					action=menu.addAction(self.getIcon("1@"+transport,status=key,size="16x16"),self.status[key])
					action.setData(QtCore.QVariant(QtCore.QStringList([key,unicode(transport)])))
					if len(config[key])!=0:
						for val in config[key]:
							status=val[0]
							index=val[1]
							if len(status)>20:
								action=menu.addAction(self.getIcon("1@"+transport,status=key,size="16x16"),unicode(status)[:20]+"...")
							else:
								action=menu.addAction(self.getIcon("1@"+transport,status=key,size="16x16"),unicode(status))
							# [show_idOfMessage,jidOfTransport]
							action.setData(QtCore.QVariant(QtCore.QStringList([key+"_"+unicode(index),unicode(transport)])))
							font=action.font()
							font.setItalic(True)
							action.setFont(font)
						menu.addSeparator()
						separator=False
					else:
						separator=True
				action=menu.addAction(self.getIcon('1@'+transport,status="offline",size="16x16"),self.tr("Log out"))
				action.setData(QtCore.QVariant(QtCore.QStringList(['offline',unicode(transport)])))
				if separator:
					menu.addSeparator()

				# updates transport menu in self.transports and add it to the self.statusWidgetMenu
				#self.transports[transport]=menu
				
				
				self.transports[transport].setPopupMode(QtGui.QToolButton.InstantPopup)
				self.transports[transport].setArrowType(QtCore.Qt.NoArrow)
				app.connect(menu, QtCore.SIGNAL("triggered ( QAction *)"),self.statusWidgetChanged)
				self.transports[transport].setMenu(menu)
				self.ui.hboxlayout4.addWidget(self.transports[transport])
				#self.statusWidgetMenu.addMenu(menu)
			#self.statusWidgetMenu.addSeparator()
		else:
			self.ui.line1.hide()

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

	def moodChanged(self,action):
		"""
		Executes command according to action.objectName(). Called when user choose one of QAction from self.mood menu, which si created by self.buildStatusWidgetMenu().
		@type action: QAction
		@param action: QAction from self.statusWidgetMenu.
		"""
		data=action.data()
		cmd = action.objectName()

		if cmd == 'mood':
			m = unicode(data.toString())
			log.msg('setting mood to '+m)
			if m=="none":
				self.client.sendPEP('http://jabber.org/protocol/mood', self.client.getMoodPayload(None))
			else:
				self.client.sendPEP('http://jabber.org/protocol/mood', self.client.getMoodPayload(m))
			if self.moodIcons.has_key(m):
				self.ui.moodButton.setIcon(self.moodIcons[m])
			if self.moodMenu.currentAction:
				font=self.moodMenu.currentAction.font()
				font.setBold(False)
				self.moodMenu.currentAction.setFont(font)
			self.moodMenu.currentAction=action
			font=self.moodMenu.currentAction.font()
			font.setBold(True)
			self.moodMenu.currentAction.setFont(font)

	def activityChanged(self,action):
		"""
		Executes command according to action.objectName(). Called when user choose one of QAction from self.mood menu, which si created by self.buildStatusWidgetMenu().
		@type action: QAction
		@param action: QAction from self.statusWidgetMenu.
		"""
		data=action.data()
		cmd = action.objectName()

		if cmd == 'activity':
			data = data.toList()
			group = unicode(data[0].toString())
			if group == "none":
				a = group = None
			else:
				a = unicode(data[1].toString())
			log.msg('setting activity to %s/%s'%(group, a))
			self.client.sendPEP('http://jabber.org/protocol/activity', self.client.getActivityPayload(group, a))

	def statusWidgetChanged(self,action):
		"""
		Executes command according to action.objectName(). Called when user choose one of QAction from self.statusWidgetMenu, which si created by self.buildStatusWidgetMenu().
		@type action: QAction
		@param action: QAction from self.statusWidgetMenu. if QAction.data() is string, presence is sent to the server or one of other commands is executed. If it's list, then it's in format [show,JID] and presence is sent to the JID. Show is in format "show_idOfStatusMessage" or just "show".
		"""
		data=action.data()
		cmd = action.objectName()
		if cmd=="mood":
			return
		if cmd == 'activity':
			return
		print 'presence'
		print data.toList(),unicode(data.toString())
		if len(data.toList())==0:
			# We are sending presence to the server
			data=unicode(data.toString())
			jid=None
		else:
			# We are sending presence to the transport
			data=data.toList()
			jid=unicode(data[1].toString())
			data=unicode(data[0].toString())
			print jid,data
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
		#if self.config['rosterMode'] == "compact":
		#	self.ui.roster.setRosterStyle(widgets.compactrosterstyle.rosterStyle)
		#else:
		#	self.ui.roster.setRosterStyle(widgets.defaultrosterstyle.rosterStyle)
		if self.config['rosterScrollBar']=="True":
			self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
			QtCore.QObject.disconnect(self.scroll.verticalScrollBar(),QtCore.SIGNAL("valueChanged ( int )"),self.ui.roster.sliderChanged)
		else:
			self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
			QtCore.QObject.connect(self.scroll.verticalScrollBar(),QtCore.SIGNAL("valueChanged ( int )"),self.ui.roster.sliderChanged)
		self.loadRosterStyle() # load roster style
		# change cache
		if self.cache:
			self.cache.close()
			del self.cache
		# load cache and create tables
		if sys.platform != 'win32':
			self.cache = storage.Cache(db=utils.path(self.homeDir+u'/cache.db'))
		else:
			self.cache = storage.Cache(db=(unicode(self.homeDir)+u'/cache.db').encode('utf8')) #hack!
		self.cache.create_tables().addCallback(self.tables_created)

	def fillLoginForm(self):
		"""
		Fill login form according to config file and existing profiles
		"""
		profiles=utils.getProfiles(self.realHomeDir)
		avatarDef = ConfigObj(self.realHomeDir+'/avatars/avatars.def',encoding='UTF8')
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
				file=""
				if avatarDef.has_key(unicode(jid)):
					file=self.realHomeDir+"/avatars/"+avatarDef[unicode(jid)]
				if os.path.isfile(file):
					avatar=QtGui.QPixmap(file)
					if avatar.isNull():
						result=QtGui.QIcon("images/22x22/apps/jabbim.png")
					else:
						avatar=avatar.scaled(22,22,QtCore.Qt.KeepAspectRatio)
						result=QtGui.QPixmap(22,22)
						result.fill(QtCore.Qt.transparent)
						painter=QtGui.QPainter(result)
						painter.drawPixmap((22-avatar.width())/2,(22-avatar.height())/2,avatar)
						painter.end()
						result=QtGui.QIcon(result)
				else:
					#result=QtGui.QIcon(self.getAvatar(unicode(jid),size="32x32",frame=False))
					#if not result:
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
			self.ui.login_autoconnect.setEnabled(True)
		else:
			self.ui.login_savePassword.setChecked(False)
			self.ui.login_autoconnect.setEnabled(False)
		file=""
		if avatarDef.has_key(self.config['jid']):
			file=self.realHomeDir+"/avatars/"+avatarDef[self.config['jid']]
		if os.path.isfile(file):
			pixmap=QtGui.QIcon(file)
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
		# set showOffline
		if self.config['showOffline']=='True':
			self.offline=False
			#self.buildOfflineMenu()
			self.hideOffline(True)

	def registerButtonClicked(self):
		# depracted
		if USE_WIZARDS:
			self.regwiz=wizards.registration.registrationWizard(self,self)
			self.regwiz.show()
		return

	def serviceDiscovery(self,b):
		"""
		Shows Service Discovery Dialog. Called by QAction from main menu.
		"""
		self.discovery=widgets.servicediscovery.serviceDiscoveryDialog(self,self)
		self.discovery.show()
		if USE_WIZARDS and self.client.jid.host in ['jabbim.cz','jabber.cz','njs.netlab.cz','jabbim.com','jabbim.pl']:
			self.discovery2=wizards.jabbimservicemanager.jabbimServiceManager(self,self)
			self.discovery2.show()


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

	def startChatDialog(self, b=False):
		message=jid=""
		while 1:
			items=QtCore.QStringList ()
			items.append(jid)
			pole=self.config['chatDialogHistory']
			pole.reverse()
			for j in pole:
				items.append(j)
			jid,b=QtGui.QInputDialog.getItem(self,self.tr("Chat with new user"),message+self.tr("Enter Jabber ID:"), items, 0, True)
			#jid,b=QtGui.QInputDialog.getText(self,self.tr("Chat with new user"),message+self.tr("Enter Jabber ID:"), QtGui.QLineEdit.Normal, jid)
			jid=unicode(jid)
			if b==True and len(jid)!=0:
				try:
					isJid=jidT.JID(jid)
				except:
					isJid=None
					message=jid+" "+self.tr("is not valid Jabber ID")+"\n"
				if isJid:
					self.chat.addChatTab(jid,jid,self.getIcon(jid,status='offline',size="16x16"))
					if isJid.userhost() not in self.config['chatDialogHistory']:
						self.config['chatDialogHistory'].append(isJid.userhost())
					self.chat.activate()
					break
			else:
				break

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
		#if not self.mucbrowser:
			#self.mucbrowser=widgets.mucbrowser.MUCBrowserDialog(self,self)
			#self.mucbrowser.show()
		#else:
			#if self.mucbrowser.isHidden()==True:
				#self.mucbrowser=widgets.mucbrowser.MUCBrowserDialog(self,self)
				#self.mucbrowser.show()
		self.joinGroupchat(bool)

	def about(self,bool):
		"""
		Shows About Jabbim dialog.
		"""
		about=aboutDialog(self)
		about.exec_()
	
	def support(self, bool):
		print 'support pressed'
		if self.client:
			if self.chat.addGroupChatTab("jabbim@conf.netlab.cz",self.client.jid.user):
				self.client.joinGC("jabbim@conf.netlab.cz",self.client.jid.user,self.config['sendRooms']=="True")
		else:
			anchor="http://live.jabbim.cz/muckl/muckl.html?conf_room=jabbim&nick="
			QtGui.QDesktopServices.openUrl(QtCore.QUrl(anchor))
	
	def sendLog(self, bool):
		from twisted.web.microdom import unescape
		if self.client:
			try:
				log=open(self.homeDir+'/'+self.config['logfile'], 'r')
			except:
				print "can't open",self.homeDir+'/'+self.config['logfile']
				return
			text=unicode(log.read())
			log.close()
			text=unescape(text)
			self.client.sendMessage("paste@jabbim.cz",self.config['jid'].replace("@",".")+" Jabbim.log\n"+text)
	
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
		self.events.addLineEditEvent(maintext = maintext ,trueCall=self.joinGC, trueDict=[room], falseCall=self.client.declineInvitation, falseDict=[jid, room],header="Groupchat Invitation",text="Nickname:",name=unicode(jid),typ="groupchatInvitation",icon=None,action=None,actionDict=None,height=150,value=self.client.jid.userhost().split("@")[0],trueText=self.tr("Join"),falseText=self.tr("Decline"))

	def findPlugins(self):
		"""
		Finds plugins in plugins/ and ~/plugins and saves informations about them to the self.plugins
		"""
		if len(self.plugins) != 0:
			return  # we've done this already
		plugin_paths = ['plugins/', self.realHomeDir + '/plugins/']
		for plugin_path in plugin_paths:
			for plugin_name in os.listdir(plugin_path):
				dir = '%s/%s' % (plugin_path, plugin_name)
				if plugin_name == '.svn' or isfile(dir):
					continue
				path = '%s/%s.py' % (dir, plugin_name)

				try:
					f = open(utils.path(path))
					module = load_source(plugin_name, path.encode(sys.getfilesystemencoding()), f)
					f.close()
					plug = module.Plugin(False, self.homeDir, dir)
					version = float(plug.version)
				except Exception, ex:
					log.msg(path+': BAD PLUGIN!')
					message = unicode(traceback.format_exc(), 'utf-8')
					log.msg(message)
					continue

				if not self.plugins.has_key(plugin_name) or version > self.plugins[plugin_name]['version']:
					self.plugins[plugin_name] = { 'dir': dir, 'version': version, 'module': None }

	def startExtraDonwload(self,file):
		d=extraDialog("",self,self,file)
		d.exec_()

	def loadPlugins(self):
		"""
		Loads plugins according to config file (self.config['plugins'])
		"""
		for plugin_name in self.plugins.keys():
			if plugin_name in self.config['plugins']:
				try:
					self.loadPlugin(plugin_name)
				except Exception, ex:
					log.msg(plugin_name+': '+unicode(ex))
		#log.msg("PLUGINS:"+unicode(self.plugins))
	
	def loadPlugin(self,plugin):
		"""
		Loads plugin. Plugin is loaded to the self.plugins[name]['module'].
		@type plugin: unicode
		@param plugin: plugins name
		"""
		dir = self.plugins[plugin]['dir']
		path = utils.path('%s/%s.py' % (dir, plugin))
		log.msg("loading "+unicode(plugin)+" plugin")

		try: 
			f=open((path))
		except:
			log.msg('plugin load error: '+plugin)
			return
		try:
			if not self.plugins[plugin]['module']:
				#plug =  # load plugin module
				module = load_source(plugin, path, f)
				f.close()
				self.plugins[plugin]['module']=module.Plugin(self, self.homeDir, dir)
				self.runPluginCommand(self.plugins[plugin]['module'].buildMainWindowMenu,[]) # build menu for plugin
			else:
				print "plugin already loaded"
				f.close()
		except Exception, ex:
					#log.msg(unicode(plugin)+u': '+unicode(ex))
					traceback.print_exc()
					f.close()
					pass
		#log.msg("PLUGINS:"+unicode(self.plugins))

	def unloadPlugin(self,plugin):
		"""
		Unloads plugin. Plugin module is deleted and self.plugins[plugin]=None
		@type plugin: unicode
		@param plugin: plugins name
		"""
		if self.plugins[plugin]['module']:
			self.ui.menuPlugins.clear() # clear plugins menu
			self.runPluginCommand(self.plugins[plugin]['module']._remove,[]) # inform plugin that it will be removed
			
			l=gc.get_referents(self.plugins[plugin]['module'])
			for x in range(len(l)):
				del l[0]
			l=gc.get_referrers(self.plugins[plugin]['module'])
			for x in range(len(l)):
				del l[0]
			#del self.plugins[plugin]['module']
			self.plugins[plugin]['module']=None
			#del self.plugins[plugin]
			del gc.garbage[:] # delete plugin from python
			# rebuild plugins menu
			for plug in self.plugins.itervalues():
				if plug['module']:
					self.runPluginCommand(plug['module'].buildMainWindowMenu,[])
		#else:
			#print "plugin is not loaded:",plugin
		#log.msg("PLUGINS:"+unicode(self.plugins))

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
		try:
			privacy=self.client.privacy.active
			#privacy=True
		except:
			privacy=False
		if privacy:
			
			self.client.privacy.active.unsetInvisible(available=False) # hack
		for i in MainWindow.plugins.keys():
			MainWindow.unloadPlugin(i)
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
						try:
							self.config['groupchatSplitSizes3']=list(w.chat.ui.splitter_3.sizes())
							self.config['groupchatSplitSizes1']=list(w.chat.ui.splitter.sizes())
							self.config['groupchatSplitSizes2']=list(w.chat.ui.splitter_2.sizes())
						except:
							pass
	
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
		app.shutdown=True
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

	def loadTheme(self,text=None,file=None):
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
			app.setStyle(self.qtStylesDefault)
		else:
			self.ui.roster.theme=True
		if text==None:
			# open theme according to self.config
			conf=ConfigObj("themes/"+self.config['theme']+"/theme.ini",encoding='UTF8')
			style=False
			if conf!=None and len(conf)!=0:
				if conf.has_key('style'):
					if conf['style'] in self.qtStyles:
						app.setStyle(QtGui.QStyleFactory.create(conf['style']))
						style=True
			if not style:
				print "setting default style"
				app.setStyle(self.qtStylesDefault)
			theme=open("themes/"+self.config['theme']+"/style.css")
			text=theme.read()
			self.setStyleSheet(text)
			self.xmlConsole.setStyleSheet(text)
			self.chat.setStyleSheet(text)
			theme.close()
		else:
			# use text for stylesheet css
			if file:
				conf=ConfigObj("themes/"+file+"/theme.ini",encoding='UTF8')
				style=False
				if conf!=None and len(conf)!=0:
					if conf.has_key('style'):
						if conf['style'] in self.qtStyles:
							app.setStyle(QtGui.QStyleFactory.create(conf['style']))
							style=True
				if not style:
					print "setting default style"
					app.setStyle(self.qtStylesDefault)
			self.setStyleSheet(text)
			self.xmlConsole.setStyleSheet(text)
			self.chat.setStyleSheet(text)
			if text:
				if len(text)==0:
					self.ui.roster.theme=False
		self.styleSheetText=text
		self.ui.roster.reskin(text) # reskin roster

	def addContactMainWindow(self,jid=""):
		"""
		Shows Add Contact Dialog.
		"""
		if not self.addcontactdialog:
			self.addcontactdialog=widgets.addcontact.addContactDialog(self,self,jid=jid)
			self.addcontactdialog.show()
		else:
			if self.addcontactdialog.isHidden()==True:
				self.addcontactdialog=widgets.addcontact.addContactDialog(self,self,jid=jid)
				self.addcontactdialog.show()

	def bookmarksClicked(self,item,i):
		"""
		Joins MUC when user clicked on bookmark in Bookmarks tab.
		"""
		data=item.data(0,32)
		lst=data.toList()
		jid=unicode(lst[0].toString()) # get jid
		nickname=unicode(lst[1].toString()) # get nickname
		password = unicode(lst[2].toString()) # get password
		# send jabber command
		if self.chat.addGroupChatTab(jid,nickname):
			#self.main.groupchat[room+"@"+server]=[nickname,[]]
			self.client.joinGC(jid, nickname, password,self.config['sendRooms']=="True")

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
			item.setData(0,32,QtCore.QVariant(QtCore.QStringList([unicode(v.jid.full()),unicode(v.nick),unicode(v.password)])))
			item.setIcon(0,QtGui.QIcon("images/16x16/categories/muc.png"))

	def autoJoinGroupchat(self):
		"""
		Joins to groupchats which have autojoin flag.
		"""
		for k,v in self.client.bookmarks['conference'].iteritems():
			if (v.autojoin==True or unicode(v.autojoin).lower()=="true") or (v.autojoin==1 or v.autojoin=="1"):
				jid=unicode(v.jid.full())
				nickname=v.nick
				if self.chat.addGroupChatTab(jid,nickname):

					self.client.joinGC(jid, nickname, v.password,self.config['sendRooms']=="True")

	def joinGroupchat(self,bool):
		"""
		Called when user activate Join Groupchat QAction from main menu.
		"""
		#self.mucBrowser(bool)
		#if USE_WIZARDS:
			#self.joingroupchatwizard=wizards.joingroupchat.joinGroupchatWizard(self,self)
			#self.joingroupchatwizard.show()
		self.joingroupchatwizard=widgets.joingroupchat.joinGroupChatWindow(self,parent=self)
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
		if cmd=="join_bookmark":
			# join bookmarked groupchat
			data=action.data()
			lst=data.toList()
			jid=unicode(lst[0].toString()) # get jid
			nickname=unicode(lst[1].toString()) # get nickname
			password=unicode(lst[2].toString()) # get password
			if len(password)==0:
				password=None
			# send jabber command
			if self.chat.addGroupChatTab(jid,nickname):
				self.client.joinGC(jid, nickname,password,self.config['sendRooms']=="True")
				#self.client.joinGC(jid, nickname, v.password)
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
			autojoin=self.client.bookmarks['conference'][jid].autojoin
			if password=="None" or not password:
				password=""
			edit=widgets.preferences.editBookmark(self,room,server,name,nickname,password,autojoin,self)
			edit.exec_()
		elif cmd=="delete_bookmark":
			item=self.ui.bookmarks.currentItem()
			#self.ui.bookmarks.takeTopLevelItem(self.ui.bookmarks.indexOfTopLevelItem(item))
			del self.client.bookmarks['conference'][unicode(item.text(1))]
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

	def isValidExtraPart(self,config):
		if not config.has_key('header'):
			print "error, config doesn't have 'header' section"
			return False
		if not config['header'].has_key('type'):
			print "error, config doesn't have 'type' key in 'header' section"
			##############################################################
			# We're tolerant for RPC emoticons, so I have to enable them #
			##############################################################
			typ='emoticons' # will be commented
			#return False # will be uncommented
		else: # will be commented
			typ=unicode(config['header']['type']) # will be commented
		keys=['name','license','author','version','description']
		if typ=="moodIcons":
			keys.append('frontImage')
			if not config.has_key('moods'):
				print "error, config doesn't have 'moods' section"
				return False
		elif typ=="emoticons":
			keys.append('frontImage')
			##############################################################
			# We're tolerant for RPC emoticons, so I have to enable them #
			##############################################################
			keys=[] # will be commented
			if not config.has_key('emoticons'):
				print "error, config doesn't have 'emoticons' section"
				return False
		elif typ=='chatskin':
			if not config.has_key('chatskin'):
				print "error, config doesn't have 'chatskin' section"
				return False
		for key in keys:
			if not config['header'].has_key(key):
				print "error, config doesn't have '"+key+"' key in 'header' section"
				return False
		return True

	def loadJabbimExtraConfig(self,config,fallback):
		print 'loading JabbimExtra config',config
		# try to load config
		try:
			config=ConfigObj(config,encoding='UTF8')
			loaded=True
		except:
			loaded=False
		# check config validity
		if loaded:
			loaded=self.isValidExtraPart(config)
		# config is valid
		if loaded:
			return True,config
		else:
			# try to load fallback config
			try:
				config=ConfigObj(fallback,encoding='UTF8')
				loaded=True
			except:
				loaded=False
			# check config validity
			if loaded:
				loaded=self.isValidExtraPart(config)
			if loaded:
				return False,config
			else:
				return None,None

	def loadMoods(self):
		"""
		Loads user mood icons
		"""
		loaded,config=self.loadJabbimExtraConfig('moods/'+self.config['moods'],'moods/default/default.cfg')
		if loaded!=None:
			if loaded:
				src=dirname("moods/"+self.config["moods"])+"/"
			else:
				src=dirname("moods/default/")
			self.ui.moodButton.setIcon(QtGui.QIcon(src+config['header']['frontImage']))
			self.moodIcons=config['moods']
			for mood in self.moodIcons.keys():
				path=unicode(src+self.moodIcons[mood])
				self.moodIcons[mood]=QtGui.QIcon(path)
				self.moodIcons[mood].src=os.getcwd()+"/"+unicode(path)
			self.moodIcons["none"]=QtGui.QIcon(self.moodIcons[mood].pixmap(16,16,QtGui.QIcon.Disabled))

	def loadSounds(self):
		src=dirname("sounds/"+self.config["soundPack"])
		self.sounds=ConfigObj("sounds/"+self.config["soundPack"],encoding='UTF8')
		if len(self.sounds)==0:
			self.sounds=ConfigObj(self.realHomeDir+"/sounds/"+self.config["soundPack"],encoding='UTF8')
			src=dirname(self.realHomeDir+"/sounds/"+self.config["soundPack"])
		src+="/"
		self.sounds=self.sounds['sounds']
		for sound in self.sounds.keys():
			self.sounds[sound]=src+self.sounds[sound]

	def playsound(self,sound):
		if self.sounds.has_key(sound):
			if sys.platform == 'linux2': # linux sounds are produced using aplay
				os.system('aplay -q '+self.sounds[sound].strip('\n')+' &')
			else:
				QtGui.QSound.play(self.sounds[sound].strip('\n'))
			return True
		return False

	def loadRosterStyle(self):
		self.rosterStyle=None
		if len(self.config['rosterStyle'])==0:
			self.config['rosterStyle']="ng/config.cfg"
			self.config.write()
		path="rosterstyles/"+unicode(self.config['rosterStyle'].split("/")[0])+"/style.py"
		if not isfile(path):
			path=self.realHomeDir+"/rosterstyles/"+unicode(self.config['rosterStyle'].split("/")[0])+"/style.py"
			if not isfile(path):
				path="rosterstyles/ng/style.py"

		
		variant=self.realHomeDir+"/rosterstyles/"+unicode(self.config['rosterStyle'])
		if not isfile(variant):
			variant="rosterstyles/"+unicode(self.config['rosterStyle'])
			if not isfile(variant):
				variant="rosterstyles/ng/config.cfg"
		
		try:
			f=open(unicode(path))
		except:
			return
		try:
			#plug =  # load plugin module
			module = load_source('rosterStyle', path, f)
			f.close()
			self.ui.roster.setRosterStyle(module.rosterStyle,variant)
		except Exception, ex:
					#log.msg(unicode(plugin)+u': '+unicode(ex))
					traceback.print_exc()
					f.close()
					pass

	def loadSkin(self):
		"""
		Loads chat skin. Skin is loaded to self.skin.
		"""
		loaded,self.skin=self.loadJabbimExtraConfig("chatskins/"+self.config['chatSkin'],"chatskins/cool/cool.cfg")
		self.skin=self.skin['chatskin']
		if not self.skin.has_key("spaces_between_lines"):
			self.skin["spaces_between_lines"]='0'
		self.webkitThemeFactory=widgets.webkitthemes.webkitThemeFactory(self.config['chatTheme'],self.config['groupchatTheme'],self.realHomeDir)
		for i in range(self.chat.ui.chatTab.count()):
			w=self.chat.ui.chatTab.widget(i)
			w.chat.loadWebkit()
	
	def showXml(self,bool):
		self.xmlConsole.show()

	def hideOffline(self,bool):
		"""
		Hides or shows offline users
		@type bool: boolean
		@param bool: True == offline users are shown, False offline users are hidden
		"""
		#self.events.addAddUserEvent('hanzz@njs.netlab.cz','offline users are shown, False offline users are hidden')
		self.config['showOffline']=unicode(bool)
		self.showOfflineAction.setChecked(bool)
		self.ui.offlineButton.setChecked(bool)
		self.offline=bool
		self.ui.roster.showOffline=bool
		self.ui.roster.reshow=True
		#if self.ui.roster.item:
			#if self.ui.roster.item.typ=="user":
				#if int(self.ui.roster.item.status)==9 and not bool:
					#self.ui.roster.statusLabel.hide()
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
		self.ui.actionStart_Chat.setEnabled(True) 
		self.ui.actionPrivacy_list_editor.setEnabled(True) 
		self.ui.actionIdentity.setEnabled(True)
		self.buildStatusWidgetMenu()
		try:
			self.statusWidgetMenu.setEnabled(False)
		except:
			pass
		self.ui.selfName.setText("<h3>"+unicode(self.client.jid.userhost()).split("@")[0]+"</h3>")
		self.selfName=unicode(self.client.jid.userhost()).split("@")[0]
		self.client.getVCard(unicode(self.client.jid.userhost()))
		self.ui.showOffline.hide()
#		self.tray.showMessage(self.tr("Jabbim"),self.tr("Jabbim is ready! You are connected! :) "))
		self.tray.setIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))
		pixmap=self.getAvatar(self.client.jid.userhost(),frame=False,status=None)
		if pixmap:
			avatar=self.getAvatar(pixmap,size="64x64",frame=True)
			self.selfAvatar=pixmap
			self.ui.selfAvatar.setPixmap(avatar)
			self.ui.selfAvatar.setMinimumWidth(avatar.width()+3)

		print 'end connected in main'

	def disconnect(self):
		"""
		Stops reactor
		"""
		#if self.client!=None:
		reactor.stop2()

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
		
	def getImages(self, xhtml,frm):
		print xhtml
		dom = parseString(unicode('<p>'+xhtml+'</p>'))
		#seznam = {}
		for el in dom.getElementsByTagName('img'):
			src = el.getAttribute('src')
			if src != None and src.startswith('http'):
				novy = self.realHomeDir+'/temp/'+sha1(src).hexdigest()
				el.setAttribute('src', novy)
				if not el.hasAttribute('width') or not el.hasAttribute('height'):
					el.setAttribute('width', '64')
					el.setAttribute('height', '64')
				#newnode = parseString("<a href=\"http://seznam.cz\">"+unicode(el.toxml(),'utf-8')+"</a>").documentElement
				newnode=Element('a')
				newnode.setAttribute('href', unicode(src))
				newnode.appendChild(el.cloneNode())
				print unicode(newnode.toxml(),'utf-8')
				el.parentNode.replaceChild(newnode,el)
				fp = open(novy,'wb')
				fp.close()
				fp = open(novy+"_copy",'wb')
				d = downloadPage(str(src), fp)
				d.addCallback(self._imageReceived, fp,novy,frm)
		try:
			ret=unicode(dom.toxml(), 'utf-8').replace("<:img","<img")
		except:
			print 'wtf?'
			ret = None
		return ret
	
	def _imageReceived(self,neco,fp,file,frm):
		print 'image downloaded'
		fp.close()
		os.rename(file+"_copy",file)
		for i in range(self.chat.ui.chatTab.count()):
			w=self.chat.ui.chatTab.widget(i)
			if unicode(w.jid) == frm:
				# update viewport to refresh image
				w.chat.ui.textEdit.viewport().update()

	def connect(self,delay=None):
		# Connect to the server
		if delay:
			reactor.callLater(delay,self.connect)
			return
		
		
		print 'connecting'
		self.connectStarted=int(time.time())
		jid=unicode(self.ui.login_jid.text()).strip()
		if not re.match(r'.+@.+', jid): 
			self.ui.login_jid.setFocus(QtCore.Qt.OtherFocusReason) 
			if jid.find('@') == -1: 
				self.ui.login_jid.setText(jid + '@')
			return 
		if len(unicode(self.ui.login_password.text())) == 0:
			return
		if not self.getJid(jid):
			reactor.callLater(0,self.jidError)
			return
		self.ui.selfAvatar.setPixmap(QtGui.QPixmap('images/32x32/apps/jabbim.png'))
		self.ui.rosterStackedWidget.setCurrentIndex(2)
		self.ui.login_connect.setEnabled(False)
		self.ui.profilesList.setEnabled(False)
		self.ui.loginInfo.setText(self.tr("Connecting to the server..."))
		reactor.callLater(0,self.connect__)

	def jidError(self):
		QtGui.QMessageBox.critical(self, self.tr("Bad JID"),self.tr("You have an error in your Jabber ID."))

	def connect__(self):
		start=time.time()
		# get variables
		jid=unicode(self.ui.login_jid.text()).strip()
		password=unicode(self.ui.login_password.text())
		# get profiles
		profiles=utils.getProfiles(self.realHomeDir)
	
		# this profile exists
		if jid+"-profile" in profiles:
			self.homeDir=self.realHomeDir+"/"+jid+"-profile"
			utils.loadConfig(self,[]) # load config files
			# login informations have been updated
			if (jid!=self.config['jid'] or (unicode(self.ui.login_savePassword.isChecked())=="True" and unicode(rot13.scramble(password))!=unicode(self.config['passwd']))) or (unicode(self.config['savePasswd'])!=unicode(self.ui.login_savePassword.isChecked()) or unicode(self.ui.login_autoconnect.isChecked())!=self.config['autoJoin']):
				ret=QtGui.QMessageBox.question(self,self.tr("Login information"), self.tr("Save current login information?"),3,4)
				if ret==3:
					# update config file
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
		# this profile not exists, so we have to create it
		else:
			#ret=QtGui.QMessageBox.question(self,self.tr("New profile"), self.tr("Profile for this JID doesn't exist. Do you want to create it?"),3,4)
			#if ret==3:
			self.homeDir=self.realHomeDir+"/"+jid+"-profile"
			utils.makeHomeDir(self.homeDir)
			# copy actual config to new profile dir
			f=open(self.homeDir+"/config",'w')
			self.config.write(f)
			f.close()
			# load config file
			utils.loadConfig(self,[])
			# update config file
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

		# save last used config to real homedir (no profile homedir)
		f=open(self.realHomeDir+"/config",'w')
		self.config.write(f)
		f.close()
		
		# create clientClass
		if self.config.has_key('resource'):
			resource=''.join(self.config['resource'])
		else:
			resource='jabbim'
		if self.client==None:
			self.client = clientClass(unicode(jid).lower()+"/"+resource, password, jid.split("@")[1], 5222,self,reactor)
		path = self.realHomeDir+'/avatars/'
		if self.client.avatarDef.has_key(self.client.jid.userhost()):
			self.client.avatarImg[self.client.avatarDef[self.client.jid.userhost()]] = self.loadAvatar(self.client.avatarDef[self.client.jid.userhost()])
		self.client.avatarImg[None]=[self.getAvatar(QtGui.QPixmap("images/32x32/apps/jabbim.png"),size="32x32",frame=True),32,32]
		self.client.avatarImg[u'None']=[self.getAvatar(QtGui.QPixmap("images/32x32/apps/jabbim.png"),size="32x32",frame=True),32,32]
		#d=threads.deferToThread(self.loadAvatars,unicode(path),dict(self.client.avatarDef))
		#d.addCallback(self.gotAvatars)
		
		# sets None for all avatars
		hashe = []
		for hash in self.client.avatarDef.itervalues():
			if not hash in hashe and hash and hash!="None":
				hashe.append(unicode(str(hash)))
		for key in hashe:
			self.client.avatarImg[key]=None
		# load avatars
		self.imageLoader=avatarLoader(self,unicode(path),dict(self.client.avatarDef))
		QtCore.QObject.connect(self.imageLoader,QtCore.SIGNAL("imageLoaded(QString,QImage,int,int)"),self.avatarLoaded,QtCore.Qt.QueuedConnection)
		self.imageLoader.start()
		
		#self.gotAvatars(self.loadAvatars(unicode(path),dict(self.client.avatarDef)))
		try:
			self.client.xmlLang= unicode(QtCore.QLocale.system().name())[:2]
		except:
			try:
				self.client.xmlLang = unicode(os.environ["LANG"][:2])
			except:
				log.err('error in setting locale')
		self.client.log=True

		# connect
		self.reconnect = True
		if self.config['specifyHost'] == 'True':
			self.client.connect(self.config['connectHost'], self.config['connectPort'],JID=unicode(jid).lower()+"/"+resource,password=password,server=jid.split("@")[1])
		elif self.config['boshURL'] != '':
			self.client.connect(boshURL = self.config['boshURL'],JID=unicode(jid).lower()+"/"+resource,password=password,server=jid.split("@")[1])
		else:
			self.client.connect(JID=unicode(jid).lower()+"/"+resource,password=password,server=jid.split("@")[1])
		
	#def _loadAvatar(self,file, hash, jid):
		#if os.path.isfile(unicode(file)):
			#jid=jidT.JID(jid).userhost()
			#pixmap=QtGui.QPixmap(unicode(file))
			#for item in self.ui.roster.getUserItems(jid):
				#item.setAvatar(QtGui.QIcon(pixmap))
			#for item in self.ui.roster.getMetaItems(jid):
				#item[0].setAvatar(QtGui.QIcon(pixmap))
		#else:
			#log.msg("BAD FILE FOR AVATAR:"+unicode(file))
		#self.client.roster['users'][jid].setAvatar(file, hash)

	def avatarLoaded(self,key,image,width,height):
		"""
		Called by avatarLoader when image with hash 'key' is loaded.
		"""
		self.client.avatarImg[unicode(key)]=[QtGui.QPixmap.fromImage(image),int(width),int(height)]

	#def loadAvatars(self,path,avatarDef):
		#avatarImg={}

		#hashe = []
		#try:
			#for hash in avatarDef.itervalues():
				#if not hash in hashe and hash and hash!="None":
					#hashe.append(unicode(str(hash)))
		#except:
			#message = unicode(traceback.format_exc(), 'utf-8')
			#print message
##		path = self.main.homeDir+'/avatars/'
		#print "loadAvatars",hashe
		#frame=QtGui.QImage("images/32x32/frame.png")
		#for hash in hashe:
			#try:
				##self.avatarImg[hash] = self.main.getAvatar(hash)
				#avatar=QtGui.QImage(path+'/'+hash)
				#width=int(avatar.width())
				#height=int(avatar.height())
				#avatar=avatar.scaled(25,25,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
				#result=QtGui.QImage(32,32,QtGui.QImage.Format_ARGB32)
				#result.fill(QtCore.Qt.transparent)
				##if os.path.exists("themes/"+self.config['theme']+"/frame-32.png"):
					##frame=QtGui.QImage("themes/"+self.config['theme']+"/frame-32.png")
				##else:
				#painter=QtGui.QPainter(result)
				#painter.drawImage((32-avatar.width())/2,(32-avatar.height())/2,avatar)
				#painter.drawImage(0,0,frame)
				#painter.end()
				#avatarImg[hash] = [result,width,height]
			#except:
				#avatarImg[hash] = None
				#message = unicode(traceback.format_exc(), 'utf-8')
				#print message
		#return avatarImg

	def loadAvatar(self,hash):
		path=self.realHomeDir+"/avatars"
		avatar=QtGui.QImage(path+'/'+hash)
		width=int(avatar.width())
		height=int(avatar.height())
		avatar=avatar.scaled(25,25,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
		result=QtGui.QImage(32,32,QtGui.QImage.Format_ARGB32)
		result.fill(QtCore.Qt.transparent)
		#if os.path.exists("themes/"+self.config['theme']+"/frame-32.png"):
			#frame=QtGui.QImage("themes/"+self.config['theme']+"/frame-32.png")
		#else:
		frame=QtGui.QImage("images/32x32/frame.png")
		painter=QtGui.QPainter(result)
		painter.drawImage((32-avatar.width())/2,(32-avatar.height())/2,avatar)
		painter.drawImage(0,0,frame)
		painter.end()
		return [QtGui.QPixmap.fromImage(result),width,height]

	#def gotAvatars(self,avatarImg):
		#self.client.avatarImg=avatarImg
		#for key in self.client.avatarImg.keys():
			#self.client.avatarImg[key][0]=QtGui.QPixmap.fromImage(self.client.avatarImg[key][0])
			##print 'avatarSize',self.client.avatarImg[key].width(),self.client.avatarImg[key][0].height()
		#self.client.avatarImg[None]=[self.getAvatar(QtGui.QPixmap("images/32x32/apps/jabbim.png"),size="32x32",frame=True),32,32]
		#self.client.avatarImg[u'None']=[self.getAvatar(QtGui.QPixmap("images/32x32/apps/jabbim.png"),size="32x32",frame=True),32,32]
		#print 'LOADED AVATARS',self.client.avatarImg

	
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
		print 'disconnect reason '+unicode(error)
		self.tray.setIcon(QtGui.QIcon(QtGui.QIcon("images/16x16/apps/jabbim.png").pixmap(16,16,QtGui.QIcon.Disabled)))
		if self.client:
			if error=="auth":
				reactor.callLater(0,self._badJabberPassword)
				self.reconnect = False
			elif error=="dns":
				reactor.callLater(0,self._serverNotFound)
				self.reconnect = False
			if self.client.factory:
				self.client.factory.stopTrying()
		else:
			return
		self.config.write()
		MainWindow.ui.rosterStackedWidget.setCurrentIndex(0)
		MainWindow.ui.showOffline.hide()
		MainWindow.ui.actionAdd_Contact.setEnabled(False)
		MainWindow.ui.actionJoin_groupchat.setEnabled(False)
		MainWindow.ui.actionService_Discovery.setEnabled(False)
		MainWindow.ui.actionStart_Chat.setEnabled(False) 
		MainWindow.ui.actionPrivacy_list_editor.setEnabled(False) 
		MainWindow.ui.actionIdentity.setEnabled(False)
#		self.client=None
		self.selfResources=[]
		if self.client.oldstatus:
			self.ui.loginStatus.setItemData(MainWindow.ui.loginStatus.findText(MainWindow.status[self.client.oldstatus[0]]),  QtCore.QVariant([self.client.oldstatus[0], self.client.oldstatus[1]]))
			self.ui.loginStatus.setCurrentIndex(MainWindow.ui.loginStatus.findText(MainWindow.status[self.client.oldstatus[0]]))
		
		try:
			self.statusWidgetMenu.setEnabled(False)
		except:
			pass
		self.ui.login_cancel.show()
		self.ui.profilesList.setEnabled(True)

		MainWindow.ui.roster.sortedGroups=[]
		MainWindow.ui.roster.sorted={}
		MainWindow.ui.roster.users=[]
		MainWindow.ui.roster.disconnect()
		MainWindow.ui.login_connect.setEnabled(True)
		self.ui.eventsListWidget.clear()
		del self.events.events
		self.events.events=[]
		self.events.refreshTray()
		for i in MainWindow.plugins.keys():
			MainWindow.unloadPlugin(i)

		for transport in self.transports.keys():
			if self.transports[transport]:
				self.ui.hboxlayout4.removeWidget(self.transports[transport])
				self.transports[transport].setParent(None)
				self.transports[transport].deleteLater()
		self.transports={}

		if self.client:
			for jid in self.client.groupchats.keys():
				for i in range(self.chat.ui.chatTab.count()):
					w=self.chat.ui.chatTab.widget(i)
					if unicode(w.jid) == jid:
						w.chat.ui.line.setEnabled(False)
						w.chat.ui.users.clear()
						w.chat.addRoles()
						message=self.webkitThemeFactory.genChatStatus(unicode(self.tr("You are now offline.")),self.now())
						w.chat.textEditWrite(message)
						w.chat.lastMessageFrom=""
		if error == 'lost' and MainWindow.reconnect:
#			self.client.oldstatus = self.client.getContactByJid(self.client.jid.full()).status
			self.reconnect = False
			msg = None
			try:
				MainWindow.client.xping.stop()
				
			except:
				print 'can\'t stop xping'
 			# connection lost, let's wait for a while and then reconnect
			MainWindow.tray.showMessage(self.tr("Connection lost! "),self.tr("Trying to reconnect ..  ") , QtGui.QSystemTrayIcon.Warning, 5000)
 			MainWindow.plugins={}
# 			MainWindow.client = None
			log.err('Connection Lost')
			if msg != None and len(msg)>0:
				MainWindow.delayedMessages = msg
 			reactor.callLater(5, MainWindow.connect)
		#else:
			 #= None
		self.buildTrayMenu()
		print "disconnected....."


class XMLConsole(QtGui.QMainWindow):
	def __init__(self,data,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.ui=widgets.xmlConsole.Ui_xmlConsole()
		self.ui.setupUi(self)
		QtCore.QObject.connect(self.ui.send,QtCore.SIGNAL("clicked()"),self.send)
		QtCore.QObject.connect(self.ui.message,QtCore.SIGNAL("clicked()"),self.message)
		QtCore.QObject.connect(self.ui.presence,QtCore.SIGNAL("clicked()"),self.presence)
		QtCore.QObject.connect(self.ui.iq,QtCore.SIGNAL("clicked()"),self.iq)
		
	def iq(self):
		self.ui.textEdit.setText("<iq to='USER@DOMAIN' from='"+MainWindow.client.jid.full()+"'>\n<query xmlns=''>\n</iq>")	
		
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
		if type(self.jid) != list:
			MainWindow.client.sendPresence(to=self.jid,show = unicode(self.show), status = unicode(self.ui.status.toPlainText ()))
		else:
			show = unicode(self.show)
			status = unicode(self.ui.status.toPlainText())
			for jid in self.jid:
				MainWindow.client.sendPresence(to=jid, show = show, status = status)
		self.done(1)

class aboutDialog(QtGui.QDialog):
	def __init__(self,parent):
		QtGui.QDialog.__init__(self,parent)
		self.setModal(True)
		self.ui=widgets.about.Ui_about_window()
		self.ui.setupUi(self,parent.version)
		self.ui.version.setTextFormat(QtCore.Qt.RichText)
		self.ui.version.setText(self.ui.version.text()+"<br/>"+"PyQt: "+unicode(QtCore.PYQT_VERSION_STR)+"<br/>Qt: "+unicode(QtCore.QT_VERSION_STR))
		
class scrollBar(QtGui.QScrollArea):
	def __init__(self,parent=None):
		QtGui.QScrollArea.__init__(self,parent)
		self.y=0
		self.verticalScrollBar().setPageStep(32)
		self.verticalScrollBar().setSingleStep(32)
		self.setObjectName("scroll")

if __name__ == "__main__":
	translator=QtCore.QTranslator()
	translator.load("locales/jabbim_"+unicode(QtCore.QLocale.system().name())[:2]+".qm")
	print "trying to load locales:","locales/jabbim_"+unicode(QtCore.QLocale.system().name())[:2]+".qm"
	app.installTranslator(translator)
	MainWindow = mainWindow()
	if MainWindow.config['startInTray']=="True":
		MainWindow.close()
	else:
		MainWindow.show()
	reactor.run()
