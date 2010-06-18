'''
Created on 16.4.2010

@author: sef
'''
import pyxl
from include import utils
from twisted.python import log
from PyQt4 import QtGui, QtCore
from include.constants import RESOURCEPATH

import traceback
import time
from widgets import dataforms
import os
import widgets
from pyxl import jid as jidT
import weakref
from os.path import basename,dirname, isfile
import base64


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
		if self.main.config['proxyHost'] != '':
			if self.main.config['proxyPort'] =="":
				port = '80'
			else:
				port = self.main.config['proxyPort']
			self.proxy = {'host':self.main.config['proxyHost'],  'port':port}

		self.version=self.main.version
		self.bookmarksEnabled=True #: True if bookmarks is enabled by server
		self.xmlCount=[]
		if self.main.config['useXHTML'] == 'False':
			self.unregisterFeature('http://jabber.org/protocol/xhtml-im')
			self.rebuildCaps()

	def on_pep(self, frm, ns, payload):
		"""
		Called when PEP informations of contact frm is changed.
		"""
		log.msg('on_pep')
		# it's our own pep
		if frm == self.jid.userhost():
			log.msg('received my own PEP payload')
			log.msg(payload)
			log.msg(ns)
			self.main.ui.selfAvatar.refreshToolTip()
		# change information in chat tab if we have opened it
		tab,index=self.main.chat.findTab(frm,typ=['chat'])
		change=[]
		if payload == None:
			return # this is propably not that good idea
		# user mood
		if isinstance(payload,list):
			log.msg( "mood list")

			if len(payload)!=0:
				payload=payload[0]
			else:
				return
		if ns=="http://jabber.org/protocol/mood":
			log.msg("mood received")
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
					self.main.ui.roster.repaintItem(item)
			else:
				for item in self.main.ui.roster.getUserItems(frm):
					item.mood=None
					self.main.ui.roster.repaintItem(item)
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
				pass #WTF?
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
				listening=QtGui.QIcon(RESOURCEPATH+"images/22x22/icons/headphones.png").pixmap(16,16)
				song=t
			for item in self.main.ui.roster.getUserItems(frm):
				item.tune=listening
				item.song=song
				item.height=self.main.ui.roster.rosterStyle.heightForItem(item)
				self.main.ui.roster.repaintItem(item)
		if tab:
			tab.chat.refreshLabel(change)
			tab.chat.refreshToolTip()
	def on_bookmarksFail(self):
		"""
		Called if bookmarks are not supported by server.
		"""
		self.main.ui.mainTabWidget.setTabEnabled(3,False)
		self.bookmarksEnabled=False
		mainWindow=self.main
		self.main.tray.showMessage(mainWindow.tr("Error"),mainWindow.tr("Your server doesn't support Private XML Storage. Some functions will be disabled."))

#	def on_privacyFail(self):
#		"""
#		Called if privacy lists are not supported by server.
#		"""
#		self.main.ui.actionPrivacy_list_editor.setEnabled(False)

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
					tab.chat.nick=self.main.selfName+"_"
					self.joinGC(fromjid, resource+"_",sendRooms=self.main.config['sendRooms']==True)
				else:
					self.main.chat.ui.chatTab.removeTab(index)
					if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
					#self.main.events.addLineEditEvent(maintext=unicode(fromjid)+"<br/>"+mainWindow.tr('This nickname is used by someone else. Please choose another.'), trueCall=self.main.joinGC, trueDict=[fromjid], falseCall=None,falseDict=None,header=mainWindow.tr("Nickname conflict"),text=mainWindow.tr("New name:"),name=unicode(fromjid),typ="groupchatError",icon=None,action=None,actionDict=None,height=150, value=resource,trueText=mainWindow.tr("Join"),falseText=mainWindow.tr("Decline"))
					maintext = unicode(fromjid) + " <br/> " +  mainWindow.tr("This nickname is used by someone else. Please choose another. ")
					event=mainWindow.events.addLineEditEvent()
					event.setAcceptHandler(mainWindow.joinGC,[unicode(fromjid)])
					event.setRejectHandler(mainWindow.client.declineInvitation,[unicode(fromjid), unicode(fromjid)])
					widget=event.getWidgets()[0]
					widget.setText(maintext)
					widget.setLabel(mainWindow.tr("Nickname:"))
					widget.setLineEditText(resource)
					widget.setAcceptText(mainWindow.tr("Join"))
					widget.setRejectText(mainWindow.tr("Cancel"))
					widget.ui.accept.setIcon(QtGui.QIcon(RESOURCEPATH+'images/16x16/actions/ok.png'))
		elif int(code)==401:
			log.msg("room is password protected")
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
				#self.main.events.addInfoEvent(header=mainWindow.tr("Wrong password"),text=mainWindow.tr("Room is password protected"),name=unicode(fromjid),typ='groupchatError')
				maintext=unicode(fromjid) + "<br/> " + mainWindow.tr("Room is password protected")
				event=mainWindow.events.addBooleanEvent("info","other")
				widget=event.getWidgets()[0]
				widget.setText(maintext)
				widget.setRejectText(mainWindow.tr("Close"))
		elif int(code)==407:
			log.msg("room is member only")
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
				#self.main.events.addInfoEvent(header=mainWindow.tr("Member only"),text=mainWindow.tr("Room is only for members"),name=unicode(fromjid),typ='groupchatError')
				maintext=unicode(fromjid) + "<br/> " + mainWindow.tr("Room is only for members")
				event=mainWindow.events.addBooleanEvent("info","other")
				widget=event.getWidgets()[0]
				widget.setText(maintext)
				widget.setRejectText(mainWindow.tr("Close"))
		elif int(code)==403:
			log.msg("room user banned")
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
				#self.main.events.addInfoEvent(header=mainWindow.tr("Banned"),text=mainWindow.tr("You are banned from entering this room."),name=unicode(fromjid),typ='groupchatError')
				maintext=unicode(fromjid) + "<br/> " + mainWindow.tr("You are banned from entering this room.")
				event=mainWindow.events.addBooleanEvent("info","other")
				widget=event.getWidgets()[0]
				widget.setText(maintext)
				widget.setRejectText(mainWindow.tr("Close"))
		elif int(code)==503:
			log.msg("Room Occupant Limit Has Been Reached")
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
				#self.main.events.addInfoEvent(header=mainWindow.tr("Max Users"),text=mainWindow.tr("Room occupant limit has been reached"),name=unicode(fromjid),typ='groupchatError')
				maintext=unicode(fromjid) + "<br/> " + mainWindow.tr("Room occupant limit has been reached")
				event=mainWindow.events.addBooleanEvent("info","other")
				widget=event.getWidgets()[0]
				widget.setText(maintext)
				widget.setRejectText(mainWindow.tr("Close"))
		elif int(code)==404:
			log.msg("Room not exist")
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
				#self.main.events.addInfoEvent(header=mainWindow.tr("Room not exist"),text=mainWindow.tr("Room is creating try it again"),name=unicode(fromjid),typ='groupchatError')
				maintext=unicode(fromjid) + "<br/> " + mainWindow.tr("Room is creating try it again")
				event=mainWindow.events.addBooleanEvent("info","other")
				widget=event.getWidgets()[0]
				widget.setText(maintext)
				widget.setRejectText(mainWindow.tr("Close"))
		elif int(code)==405:
			log.msg("Room is reserved")
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
				#self.main.events.addInfoEvent(header=mainWindow.tr("Room reserved"),text=mainWindow.tr("Not allowed create room"),name=unicode(fromjid),typ='groupchatError')
				maintext=unicode(fromjid) + "<br/> " + mainWindow.tr("Not allowed create room")
				event=mainWindow.events.addBooleanEvent("info","other")
				widget=event.getWidgets()[0]
				widget.setText(maintext)
				widget.setRejectText(mainWindow.tr("Close"))
		elif int(code)==406:
			log.msg("Roomnicks are locked")
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
						self.main.chat.hide()
				#self.main.events.addInfoEvent(header=mainWindow.tr("Locked Nicknames"),text=mainWindow.tr("Not allowed change nickname"),name=unicode(fromjid),typ='groupchatError')
				maintext=unicode(fromjid) + "<br/> " + mainWindow.tr("Not allowed change nickname")
				event=mainWindow.events.addBooleanEvent("info","other")
				widget=event.getWidgets()[0]
				widget.setText(maintext)
				widget.setRejectText(mainWindow.tr("Close"))
		else:
			# remove groupchatWidget from chatWindow
			tab,index=self.main.chat.findTab(fromjid)
			if tab:
				self.main.chat.ui.chatTab.removeTab(index)
				if int(self.main.chat.ui.chatTab.count())==0:
					self.main.chat.hide()
			# add event with detailed description of the error
			#self.main.events.addInfoEvent(header=mainWindow.tr("Groupchat Error"),text=text,name=unicode(fromjid),typ='groupchatError')
			maintext=unicode(fromjid) + "<br/> " + mainWindow.tr("Groupchat Error")
			event=mainWindow.events.addBooleanEvent("info","other")
			widget=event.getWidgets()[0]
			widget.setText(maintext)
			widget.setRejectText(mainWindow.tr("Close"))

	def on_roleErr(self,  muc,  err,  nick):
		pass

	def on_affiliationErr(self,  muc,  err,  nick):
		pass

	def on_receipt(self, frm, id):
		if self.main.config['showReceipts'] == 'True':
			#cwd = unicode(os.getcwd(), sys.getfilesystemencoding())
			#self.main.refreshImage(cwd + '/images/16x16/actions/ok.png', id, frm)
			self.main.removeChatElement(id,frm)


	def on_ftTransfered(self, sid, bytes,end=False):
		"""
		Updates progress bars for filetransfer with id 'sid'.
		@type sid: unicode
		@param sid: filetransfer ID
		@type bytes: integer
		@param bytes: count of transfered bytes
		"""
		mainWindow=self.main
		if not self.main.events.ftEvents.has_key(sid):
			return #prenos neni v eventech?
		event=self.main.events.ftEvents[sid]
		if not end:
			event.setFileTransfered(int(self.ft[sid].transfered))
		else:
			log.msg("ft.finished "+ unicode(self.main.ftError[sid]))
			if event.typ=="ftUpload":
				if len(event.queue)!=0:
					self.main.events.nextFTUploadEvent(sid)
				else:
					event.transferFinished()

			else:
				event.transferFinished()

		return
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
				log.msg( 'ft.finished')

				widget.widget.progressBar.setValue(100)
				if widget.widget.complete==None:
					# User wants to close transfer
					# TODO: we have to do something here (inform user that transfer was stopped for example...)
					#self.main.ui.eventsListWidget.takeItem(self.main.ui.eventsListWidget.row(widget.widget.item))
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
		log.msg("ftEnd")
		self.main.ftError[sid]=error
		# self.main.allowedSids contains SIDs which are used for transfering Jabbim Extra
		if sid in self.main.allowedSids.keys():
			print "EVENT REJECT"
			if unicode(self.ft[sid].fromjid.full()).find("rpc@jabbim.cz")!=-1:
				# continuing with jabbim extra
				log.msg("Part of jabbim extra has been downloaded")
				file=self.ft[sid].filepath
				log.msg("extracting " + unicode(file) +' to ' + unicode(dirname(file)))
				try:
					root=utils.extractZip(file,dirname(file))
					done=True
				except:
					message = unicode(traceback.format_exc(), 'utf-8')
					log.err( message)
					done=False
				if done:
					self.main.preferencesWindow.loadThemePackages()
					self.main.preferencesWindow.reloadPlugins_()
			event=self.main.events.ftEvents[sid]
			event.reject()

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

			self.main.buildOfflineMenu()

	def getHostType(self,host,jid):
		host=host.split('/')[0]
		try:
			name=self.disco[host][(host,None)]['identities'].keys()[0]
			typ=self.disco[host][(host,None)]['identities'][name]['type']
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
				#rename chat tab
				tab, index = self.main.chat.findTab(jid)

				if tab != None:
					tab.chat.setName(newName)
			elif newName and jid == self.jid.userhost():
				self.main.ui.selfName.setText('<h3>'+newName+'</h3>') #we need to set name in roster
				self.main.selfName=newName

	def on_rosterArrived(self):
		"""
		Called when roster arrived.
		"""
		start=time.time()
		log.msg('we got roster')
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
		if self.main.config['keepStatus'] == "True" and self.main.config['keepedStatus'] != '':
			self.main.sendPresence(None,show,self.main.config['keepedStatus'])
		else:
			self.main.sendPresence(None,show,status)
		print "Sending firse presence to server..."
		#self.main.ui.statusButton.setText(unicode(""))
		#self.main.ui.statusButton.setIcon(self.main.getIcon(status=show,size="16x16"))
		self.main.ui.login_cancel.hide()
		
#		#userRating - disabled
#		log.msg( "loading users for userRating")
#		for jid,user in self.roster['users'].iteritems():
#			self.main.userRating.users[jid]=userrating.User(jid)
#		log.msg("users for userRating loaded: "+ unicode(self.main.userRating.users))
#		self.main.loadUserRating()

	def on_rosterx(self, frm, items, id, typ):
		mainWindow = self.main
		if typ == 'add':
			if self.main.getJid(frm).host == "fb.jabbim.cz":
				frm = self.main.getJid(frm)
				self.rosterx(frm, items, id, typ)
				return
			if len(items)==1:
				item = items[0]
				event=self.main.events.addBooleanEvent("subscribe","authorizations")
				event.setAcceptHandler(self.rosterx,[frm, items, id,typ])
				widget=event.getWidgets()[0]
				widget.setText(frm+unicode(mainWindow.tr(" is sending you contact. Do you want to receive them?"))+unicode(item["jid"]))
				widget.setAcceptText(mainWindow.tr("Yes"))
				widget.setRejectText(mainWindow.tr("No"))
				widget.ui.accept.setIcon(QtGui.QIcon(RESOURCEPATH+'images/16x16/actions/ok.png'))
			else:
				names = ''
				for item in items:
					names += " <br/> " + item['jid']

				event=self.main.events.addBooleanEvent("subscribe","authorizations")
				event.setAcceptHandler(self.rosterx,[frm, items, id, typ])
				widget=event.getWidgets()[0]
				widget.setText(frm+unicode(mainWindow.tr(" is sending you contacts. Do you want to receive them?"))+unicode(names))
				widget.setAcceptText(mainWindow.tr("Yes"))
				widget.setRejectText(mainWindow.tr("No"))
				widget.ui.accept.setIcon(QtGui.QIcon(RESOURCEPATH+'images/16x16/actions/ok.png'))
		elif typ == 'delete':
			if len(items)==1:
				item = items[0]
				event=self.main.events.addBooleanEvent("unsubscribe","authorizations")
				event.setAcceptHandler(self.rosterx,[frm, items, id,typ])
				widget=event.getWidgets()[0]
				widget.setText(frm+unicode(mainWindow.tr(" is requesting removal of a contact. Do you want to proceed?"))+unicode(item.jid))
				widget.setAcceptText(mainWindow.tr("Yes"))
				widget.setRejectText(mainWindow.tr("No"))
				widget.ui.accept.setIcon(QtGui.QIcon(RESOURCEPATH+'images/16x16/actions/ok.png'))
				widget.ui.reject.setIcon(QtGui.QIcon(RESOURCEPATH+'images/16x16/actions/prosess_stop.png'))
			else:
				names = ''
				for item in items:
					names += " <br/> " + item['jid']

				event=self.main.events.addBooleanEvent("unsubscribe","authorizations")
				event.setAcceptHandler(self.rosterx,[frm, items, id, typ])
				widget=event.getWidgets()[0]
				widget.setText(frm+unicode(mainWindow.tr(" is requesting removal of a contacts. Do you want to proceed?"))+unicode(names))
				widget.setAcceptText(mainWindow.tr("Yes"))
				widget.setRejectText(mainWindow.tr("No"))
				widget.ui.accept.setIcon(QtGui.QIcon(RESOURCEPATH+'images/16x16/actions/ok.png'))
				widget.ui.reject.setIcon(QtGui.QIcon(RESOURCEPATH+'images/16x16/actions/prosess_stop.png'))
		pass

	def rosterx(self, frm, items, id, typ):
		mainWindow = self.main
		msg = unicode(mainWindow.tr("Hi! I am adding you to my roster using the jabber client Jabbim! Please authorize me to see you when you are available. Thanks!"))
		if typ == 'add':
			for item in items:
				jid, name, group = item['jid'], item.get('name', None), item.get('group', None),
				if name == None:
					name = ''
				if group == None:
					groups = []
				else:
					groups = [group]
				self.addContact(jid, unicode(msg), name, groups)
		elif typ == 'delete':
			for item in items:
				jid = item['jid']
				self.delContact(jid)

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
		print "first presence srated"
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
		self.main.ui.splashImage.hide()
		self.main.ui.menuPlugins.clear() # clear plugins menu
		self.main.pluginManager.buildMainWindowMenu()
		# autoconnect
		self.reactor.callLater(2,self.autoJoin)

	def loadPlugins(self):
		self.main.findPlugins()
		self.main.loadPlugins()

	def autoJoin(self):
		if self.main.config['autoJoinMUC'] == 'True':
			self.main.autoJoinGroupchat()
		if self.main.delayedMessages != None:
			for msg in self.main.delayedMessages.itervalues():
				self.sendMessage(**msg)
			self.main.delayedMessages = None
			self.messageReceipts = {}
		lang=unicode(QtCore.QLocale.system().name())[:2]
		jid=self.jid.userhost()
#		#jabbim content -- disabled`
#		self.main.ui.contentView.load(QtCore.QUrl("http://content.jabbim.com/?jid=%s&lang=%s"%(jid,lang)))

	def on_invite(self,jid, room, reason, cont = False):
		log.msg("invite" + unicode(cont))
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

			mainWindow=self.main
			if u'201' in codes:
				#new room created
				message=self.main.webkitThemeFactory.genGroupchatAction(unicode(mainWindow.tr("You have created this room.")),self.main.now())
				tab.chat.textEditWrite(message)
				#tab.chat.roomConfigClicked()
				self.getMUCConfig(muc).addCallback(self._mucConfig, tab)
			if u'170' in codes:
				message=self.main.webkitThemeFactory.genGroupchatAction(unicode(mainWindow.tr("This room is logged")),self.main.now())
				tab.chat.textEditWrite(message)
			if u'100' in codes:
				message=self.main.webkitThemeFactory.genGroupchatAction(unicode(mainWindow.tr("Room is not anonymous")),self.main.now())
				tab.chat.textEditWrite(message)


			if (self.main.config['showMucStatus'] == 'False' and  (not 'PART' in codes) and (not 'JOIN' in codes)) or self.main.config['showMucJoinPart']=="False":
				return
			message="[nick] [jid]"+unicode(mainWindow.tr('is now'))+" [show] [[message]]"
			if status == None:
				message = message.replace("[[message]]",'')
			else:
				status = utils.replace_url(unicode(status),self.main,tab.chat)
				message = message.replace("[message]",unicode(status))

			if self.main.client.groupchats[muc].users[nick].truejid!="" and self.main.client.groupchats[muc].users[nick].truejid!=None:
				message=message.replace("[jid]",'('+unicode(self.main.client.groupchats[muc].users[nick].truejid)+') ')
			else:
				message=message.replace("[jid]","")
			message=message.replace("[show]",unicode(self.main.status[show])).replace('[nick]', nick)
			#message=self.main.skin["status_message"].replace("[time]",self.main.now()).replace('[message]',message)
			message2=self.main.webkitThemeFactory.genGroupchatStatus(message,self.main.now())
			if len(message)!=0:
				tab.chat.textEditWrite(message2)
			if tabFull:
				message=self.main.webkitThemeFactory.genChatStatus(message,self.main.now())
				tabFull.chat.textEditWrite(message)
				tabFull.chat.lastMessageFrom=""
		# refresh lastMessageFrom
		tab.chat.lastMessageFrom=""
	def _mucConfig(self, data, tab):
		if not data:
			return

		jid,form=data

		tab.chat.dialog=dataforms.dataFormsDialog(self.main,form,jid,"muc",tab.chat)
		tab.chat.dialog.show()

	def on_presence(self,jid,show,error=None,first=False):
		"""
		Called when normal presence arrived.
		"""
		if error!=None:
			log.err("PRESENCE ERROR:"+unicode(error))
			return
		start=time.time()
		mainWindow=self.main
		status=None
		contact = self.getContactByJid(jid.userhost())

		if self.main.ui.roster.isSameStatus(jid.userhost(),show) and not jid.userhost()==self.jid.userhost():
			return

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
				#process status message
				s = utils.replace_url(unicode(s),self.main,tabFull.chat)
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
					log.err('error in resource '+ unicode([jid.userhost()]))
				# get status message
				if status!=None:
					status_=status
					status=status.replace("\n"," ").replace("<","&lt;").replace(">","&gt;")
				# update contact in roster
				try:
					self.main.ui.roster.setStatus(jid.userhost(),highest.show,status=highest.status,first=first)
					self.main.ui.roster.setStatus(jid.full(),highest.show,status=highest.status,first=first)
				except:
					log.err('Error in resource ', jid.userhost())
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
		if self.lastxml < 50:
			self.lastxml += 1
		else:
			# rotate the lastxml log file
			try:
				self.lastxml = 0
				if self.lastxml_fd:
					self.lastxml_fd.close()
					self.lastxml_fd = None
					os.rename(self.main.homeDir+'/lastxml', self.main.homeDir+'/lastxml.1')
			except:
				log.err('Error rotating lastxml')
		if not self.lastxml_fd:
			try:
				self.lastxml_fd = open(self.main.homeDir+'/lastxml','wb')
			except:
				log.err('Error opening lastxml')
		self.lastxml_fd.write(xml.encode('utf-8') + "\n\n")
		self.lastxml_fd.flush()
		self.dispatcher.publishEvent('onXmlEvent', xml)

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
		log.msg("unsubscribe")

	def on_unsubscribed(self,jid):
		log.msg("unsubscribed")
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
##		self.main.events.addBooleanEvent(self.delContact,[jid],None,[],mainWindow.tr("Remove contact?"),jid+unicode(mainWindow.tr(" removed your authorization. You won't see his status. Do you want to remove him/her from your contact list?")),height=100,name=jid,typ="unsubcsribed",icon=None)
		event=self.main.events.addBooleanEvent("unsubscribed","authorizations")
		event.setAcceptHandler(self.delContact,[jid])
		widget=event.getWidgets()[0]
		user=self.main.ui.roster.getNameByJID(jid)
		widget.setText(user+unicode(mainWindow.tr(" removed your authorization. You won't see his status. Do you want to remove him/her from your contact list?")))
		widget.setAcceptText(mainWindow.tr("Yes"))
		widget.setRejectText(mainWindow.tr("No"))
		widget.ui.accept.setIcon(QtGui.QIcon('images/16x16/actions/ok.png'))
		widget.ui.reject.setIcon(QtGui.QIcon('images/16x16/actions/prosess_stop.png'))



	def on_DeleteContact(self,jid):
		"""
		Called when contact is deleted from roster.
		"""
		# go through all contact userItems and remove them
		for i in self.main.ui.roster.getUserItems(jid):
			#if self.main.ui.roster.item==i:
				#self.main.ui.roster.statusLabel.hide()
			log.msg("removing" + unicode(i) + unicode(i.jid))
			self.main.ui.roster.users.remove(i)
		# update roster
		self.main.ui.roster.sortItems()
		self.main.ui.roster.repaint()
		#remove transport button
		if self.main.transports.has_key(jid):
			self.main.ui.transportsToolbar.removeAction(self.main.transports[jid])
			

	def on_subscribe(self, frm,status):
		mainWindow=self.main
		if self.main.getJid(frm).host == "fb.jabbim.cz":
			frm = self.main.getJid(frm)
			self.sendPresence(frm.userhost(),None,status,None,'subscribed')
			return
		if self.roster['users'].has_key(frm):
			frm=self.main.getJid(frm)
			if frm.userhost() in self.main.autoAdd.keys():
				self.sendPresence(frm.userhost(),None,status,None,'subscribed')
				del self.main.autoAdd[frm.userhost()]
			else:
				frm=frm.userhost()
				events=self.main.events.getEvents("subscribe","authorizations")
				if len(events)==0:
					event=self.main.events.addBooleanEvent("subscribe","authorizations")
					widget=event.getWidgets()[0]
					widget.jids=[frm]
				else:
					event=events[0]
					widget=event.getWidgets()[0]
					widget.jids.append(frm)
				event.setAcceptHandler(self._onSubscribe,[list(widget.jids),status,False])
				event.setRejectHandler(self._onSubscribeReject,[list(widget.jids),status,False])

				test=""
				for j in widget.jids:
					user=self.main.ui.roster.getNameByJID(j)
					test+=" <br/> "+user

				widget.setText(unicode(mainWindow.tr('Users '))+" "+unicode(test)+' '+unicode(mainWindow.tr("want to see your status. Do you want to authorize these users?")))
				widget.setAcceptText(mainWindow.tr("Yes"))
				widget.setRejectText(mainWindow.tr("No"))
				widget.ui.accept.setIcon(QtGui.QIcon('images/16x16/actions/ok.png'))
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

	def _onSubscribe(self,frms,status,add=False):
		#def __init__(self,main,parent=None,jid="",group=None,name="",add=True):
		def _onTransportFeatures(frm):
			log.msg('transport features received')
			if self.hasIdentity(frm, 'gateway'):
				self.main.transports[frm] = None   # we have to add new transport to menu and send him status [needed by hicq]
				self.main.buildStatusWidgetMenu()
				self.sendPresence(frm)
		for frm in frms:
			if not self.roster['users'].has_key(frm):
				dialog=widgets.addcontact.addContactDialog(self.main,self.main,jid=frm,group="",name=frm.split('@')[0],add=add)
				dialog.exec_()
			self.sendPresence(frm,None,status,None,'subscribe')
			self.sendPresence(frm,None,status,None,'subscribed')
			
			
			jd = self.main.getJid(frm)
			if jd.user == None and self.main.transports.has_key(frm):
				self.getFeatures(frm).addCallback(_onTransportFeatures, frm)
				
				

	def _onSubscribeReject(self,frms,status,add=False):
		#def __init__(self,main,parent=None,jid="",group=None,name="",add=True):
		for frm in frms:
			self.sendPresence(frm,None,status,None,'unsubscribed')

	def on_GCmessage(self, msg):
		"""
		Handles messages from groupchat.
		"""
		#check for BoB images
		msg = self.main.getBOBImages(msg)
		#unpack legacy vars
		frm, typ, body, subject ,  xhtml,chatstate ,  delay, error = msg.legacyUnpack()
		#delete xhtml formatting if config says so
		if self.main.config['useXHTML'] == 'False':
			xhtml = None
		# get user (resource) and MUC jid (saved in frm)
		start=time.time()
		if typ=="chat":
			return self.on_message(msg)
		frm=jidT.JID(frm)
		mainWindow=self.main
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
		#replace /me
		if body.startswith('/me'):
			body = body.replace('/me', '*'+user)
			if xhtml != None:
				xhtml = xhtml.replace('/me', '*'+user,1)
		# find MUC tab
		for i in range(self.main.chat.ui.chatTab.count()):
			w=self.main.chat.ui.chatTab.widget(i)
			countMessage=False
			if unicode(w.jid) == frm:
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
						body = utils.replace_url(body,self.main,w.chat)
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
					message=utils.replace_url(message,self.main,w.chat)
					message=message.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")

					if user != frm:
						message = "%s %s %s" % (user, unicode(mainWindow.tr("has set the subject to:")), message)

					message = self.main.webkitThemeFactory.genGroupchatStatus(message,self.main.now())

					w.chat.textEditWrite(message)
					w.chat.lastMessageFrom=""

				return


	def on_message(self, msg):
		"""
		Handles normal 'chat' messages.
		"""
		if hasattr(msg,"ID"):
			ID=unicode(msg.ID)
		else:
			ID=""
		#check for BoB images
		msg = self.main.getBOBImages(msg)
		#unpack legacy vars
		frm, typ, body, subject ,  xhtml,chatstate ,  delay, error = msg.legacyUnpack()
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

		#replace /me
		if body != None and body.startswith('/me'):

			body = body.replace('/me', '*'+user)
			if xhtml != None:
				xhtml = xhtml.replace('/me', '*'+user,1)


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
		msg.user=user
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
					message = utils.replace_url(message,self.main,tab.chat)
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

					# MESSAGE EVENT
					if not tab.chat.unreadEvent:
						tab.chat.unreadEvent=weakref.ref(self.main.events.addBooleanEvent())
					if not tab.chat.unreadEvent():
						tab.chat.unreadEvent=weakref.ref(self.main.events.addBooleanEvent())
					tab.chat.unreadEvent().setAcceptHandler(self.main.chat.activate,[frm.full()])
					#tab.chat.unreadEvent.setRejectHandler(self.main.events.removeEvent,[int(tab.chat.unreadEvent.ID)])
					widget=tab.chat.unreadEvent().getWidgets()[0]
					c=str(tab.chat.unread+1)
					if c=="1":
						widget.setText(unicode(mainWindow.tr("New message from:"))+" "+unicode(user))
					else:
						widget.setText(unicode(mainWindow.tr("New messages")) +" ("+c+") "+unicode(mainWindow.tr("from:"))+" "+unicode(user))
					widget.setAcceptText(unicode(mainWindow.tr("Read")))
					widget.setRejectText(unicode(mainWindow.tr("Ignore")))
					widget.ui.accept.setIcon(QtGui.QIcon('images/16x16/actions/message.png'))

					self.dispatcher.publishEvent('chatMessageEvent', msg,tab.chat.unreadEvent)
					tab.chat.unread+=1
					if not self.main.chat.isActiveWindow():
						#if current:
							#self.main.chat.setWindowTitle("("+str(int(self.main.chat.getUnreadMessages()))+") "+current.tabName.replace("&",""))
						self.main.chat.setWindowTitle("("+str(int(self.main.chat.getUnreadMessages()))+") "+tab.tabName.replace("&",""))
				elif not self.main.chat.isActiveWindow():
					# MESSAGE EVENT
					if not tab.chat.unreadEvent:
						tab.chat.unreadEvent=weakref.ref(self.main.events.addBooleanEvent())
					if not tab.chat.unreadEvent():
						tab.chat.unreadEvent=weakref.ref(self.main.events.addBooleanEvent())
					tab.chat.unreadEvent().setAcceptHandler(self.main.chat.activate,[frm.full()])
					#tab.chat.unreadEvent.setRejectHandler(self.main.events.removeEvent,[int(tab.chat.unreadEvent.ID)])
					widget=tab.chat.unreadEvent().getWidgets()[0]
					c=str(tab.chat.unread+1)
					if c=="1":
						widget.setText(unicode(mainWindow.tr("New message from:"))+" "+unicode(user))
					else:
						widget.setText(unicode(mainWindow.tr("New messages")) +" ("+c+") "+unicode(mainWindow.tr("from:"))+" "+unicode(user))
					widget.setAcceptText(unicode(mainWindow.tr("Read")))
					widget.setRejectText(unicode(mainWindow.tr("Ignore")))
					widget.ui.accept.setIcon(QtGui.QIcon('images/16x16/actions/message.png'))

					self.dispatcher.publishEvent('chatMessageEvent',msg, tab.chat.unreadEvent)
					#if int(self.main.chat.ui.chatTab.currentIndex())==tabIndex:
					#if current:
						#self.main.chat.setWindowTitle("("+str(int(self.main.chat.getUnreadMessages())+1)+") "+current.tabName.replace("&",""))
					self.main.chat.setWindowTitle("("+str(int(self.main.chat.getUnreadMessages())+1)+") "+tab.tabName.replace("&",""))
					tab.chat.unread+=1
				else:
					color=self.main.chat.ui.chatTab.tabBar().palette().color(QtGui.QPalette.Foreground)
					self.main.chat.ui.chatTab.setTabText(tabIndex,tab.tabName)
					self.main.chat.ui.chatTab.tabBar().setTabTextColor(self.main.chat.ui.chatTab.currentIndex(),color)
					self.dispatcher.publishEvent('chatMessageEvent',msg,None)
				tab.chat.ui.chatstate.setText("")
				tab.chat.textEditWrite(message,insert,ID)
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
					# MESSAGE EVENT
					tab.chat.unreadEvent=weakref.ref(self.main.events.addBooleanEvent())
					tab.chat.unreadEvent().setAcceptHandler(self.main.chat.activate,[frm.full()])
					#tab.chat.unreadEvent.setRejectHandler(self.main.events.removeEvent,[int(tab.chat.unreadEvent.ID)])
					widget=tab.chat.unreadEvent().getWidgets()[0]
					widget.setText(unicode(mainWindow.tr("New message from:"))+" "+unicode(user))
					widget.setAcceptText(unicode(mainWindow.tr("Read")))
					widget.setRejectText(unicode(mainWindow.tr("Ignore")))
					widget.ui.accept.setIcon(QtGui.QIcon('images/16x16/actions/message.png'))

					tab.chat.lastMessageFrom=unicode(user)
					if xhtml==None:
						message=unicode(body).replace('&','&amp;').replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")
						message = utils.replace_url(message,self.main,tab.chat)
						message=message.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")
					else:
						message=xhtml.replace("&quot;",'"')
						message=message.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")
					message=self.main.webkitThemeFactory.genIncomingContent(unicode(user),message,self.main.now(),tab.chat.file)
					#message=message.replace("[avatar]","<img src=\""+tab.chat.file+"\" width=\"32\" height=\""+unicode(tab.chat.avatarHeight)+"\" />")
					tab.chat.textEditWrite(message,ID=ID)
					self.main.chat.ui.chatTab.setTabIcon(tabIndex,QtGui.QIcon("images/16x16/actions/message.png"))
					self.main.chat.ui.chatTab.tabBar().setTabTextColor(tabIndex,QtGui.QColor(255,0,0))
					self.main.chat.ui.chatTab.setTabText(tabIndex,"("+str(tab.chat.unread+1)+") "+tab.tabName)
					tab.chat.appendLastMessage(['in',user,message,timeText,tab.chat.file])
					tab.chat.unread+=1
				self.dispatcher.publishEvent('firstChatMessageEvent', msg, tab.chat.unreadEvent)

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
			#jid is not in roster
			return
		# Rename contact if he havent got nickname
		contact=self.roster['users'][jid]
		if (contact.name=="" or contact.name==contact.jid) or (not contact.name or (contact.name==contact.jid.split('@')[0] and len(contact.jid.split('@')[0])==9 and contact.jid.split('@')[0].isdigit())):
			log.msg('trying to rename '+jid)
			self.renameByVcard(card,jid)

	def on_avatarUpdate(self, jid):
		"""
		Called when avatar is upated.
		"""
		if not self.main.avatarDef.has_key(jid):
			return None
		# get avatar for this jid
		pixmap=self.main.getAvatar(jid,frame=False,status=None)
		if pixmap==None:
			return None
		# self avatar
		log.msg("update avatar for " +unicode([jid]))
		if unicode(self.jid.userhost())==unicode(jid):
			avatar=self.main.getAvatar(pixmap,size="32x32",frame=True)
			self.main.selfAvatar=pixmap
			self.main.ui.selfAvatar.setPixmap(avatar)
			self.main.ui.selfAvatar.setMinimumWidth(avatar.width()+3)
			for i in range(self.main.chat.ui.chatTab.count()):
				w=self.main.chat.ui.chatTab.widget(i)
				if w.typ == 'chat' or w.typ == 'groupchat':
					w.chat.loadSelfAvatar()
			

		# set avatar for userItems in roster
		#for item in self.main.ui.roster.getUserItems(jid):
			#item.setAvatar(QtGui.QIcon(pixmap))
		#for item in self.main.ui.roster.getMetaItems(jid):
			#item[0].setAvatar(QtGui.QIcon(pixmap))

		# set avatar for contacts in MUC
		jid = jidT.JID(jid)
		log.msg("avatar look for " +jid.userhost())
		w,i=self.main.chat.findTab(jid.userhost(),False,['groupchat'])

		if w:

			for item in w.chat.getUserItems(jid.resource):
				text=unicode(item.text(1))
				if len(text)!=0:
					item.setIcon(1,QtGui.QIcon(pixmap))

					result=self.main.getAvatar(pixmap,size="32x32",frame=False,status=self.main.icons[text[0]])
					item.setIcon(0,QtGui.QIcon(result))
					item.setToolTip(0,w.chat.getGroupchatTooltip(jid.full(),item))
					#w.chat.setTooltip(item,jid.full())
			

	def on_receivedFiles(self, id,  frm,  files, size):
		mainWindow=self.main
		jid=self.main.getJid(frm)
		event=self.main.events.addBooleanEvent('fileDownload','filetransfers')
		event.setAcceptHandler(self._acceptFTTree,[id,frm,files])
		event.setRejectHandler(self._declineFTTree,[id,frm])
		widget=event.getWidgets()[0]
		user=self.main.ui.roster.getNameByJID(jid.userhost())
		widget.setText(unicode(user)+" "+unicode(mainWindow.tr("is sending you "))+unicode(mainWindow.tr("%n files","",len(files)))+" ("+str(self.toNormalSize(int(size)))+")")
		widget.setAcceptText(unicode(mainWindow.tr("Accept")))
		widget.setRejectText(unicode(mainWindow.tr("Reject")))
		widget.ui.accept.setIcon(QtGui.QIcon('images/16x16/actions/ok.png'))
		self.dispatcher.publishEvent('FTFileReceivedEvent', weakref.ref(event))

		tab,index=self.main.chat.findTab(unicode(jid.userhost()),typ=['chat'])
##		if tab:
##			mainWindow=self.main
##			message=mainWindow.tr("User is sending you file")+" "+unicode(self.ft[sid].fileprops['name'])+". <a href=\"javascript:messageObject.acceptFT('"+unicode(sid)+"');\">["+mainWindow.tr("Accept")+"]</a> <a href=\"javascript:messageObject.rejectFT('"+unicode(sid)+"');\">["+mainWindow.tr("Decline")+"]</a>"
##			tab.chat.ui.webkit.messageObject.ft[unicode(sid)]=event
##			tab.chat.textEditWrite('<div id="ft'+unicode(sid)+'">'+self.main.webkitThemeFactory.genChatStatus(unicode(message),self.main.now())+"</div>")
##			tab.chat.lastMessageFrom=""

	def _declineFTTree(self,id,frm):
		log.msg("_declineFTTree")
##		tab,index=self.main.chat.findTab(unicode(self.ft[sid].fromjid),typ=['chat'])
##		if tab:
##			tab.chat.ui.webkit.page().mainFrame().evaluateJavaScript("removeById('ft"+unicode(sid)+"');")
##			del tab.chat.ui.webkit.messageObject.ft[unicode(sid)]
		return self.declineFiles(id,frm)

	def _acceptFTTree(self,id,frm,files,later=True):
		if later:
			reactor.callLater(0,self._acceptFTTree,id,frm,files,False)
			return
		#q = QtGui.QMessageBox.question(self.main,self.main.tr("File transfer"), unicode(" %s is sending you file."%unicode(self.ft[sid].tojid)),QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		#if q == QtGui.QMessageBox.Yes:
		mainWindow=self.main
		path = QtGui.QFileDialog.getExistingDirectory(self.main,mainWindow.tr("Save Files"))
		if path and len(path)!=0:
			paths=[]
			path=unicode(path)
			for sid,file in files.iteritems():
				if not path+"/"+dirname(file) in paths:
					paths.append(path+"/"+dirname(file))
					if not os.path.isdir(path+"/"+dirname(file)):
						os.makedirs(path+"/"+dirname(file))
				self.main.allowedSids[unicode(sid)]=path+"/"+file

##		tab,index=self.main.chat.findTab(unicode(self.ft[sid].fromjid),typ=['chat'])
##		if tab:
##			tab.chat.ui.webkit.page().mainFrame().evaluateJavaScript("removeById('ft"+unicode(sid)+"');")
##			del tab.chat.ui.webkit.messageObject.ft[unicode(sid)]
##		if filename and len(filename)!=0:
##			filename=unicode(filename)
##			log.msg(unicode(filename))
##			self.main.events.addFTDownloadEvent(unicode(self.ft[sid].fromjid),basename(self.ft[sid].fileprops['name']),"",sid,self.ft[sid].fileprops['size'])
##			log.msg('receiving file: ' + sid)
##
##			self.ft[sid].method = 'http://jabber.org/protocol/bytestreams'
##			self.ft[sid].filepath = filename
			self.receiveFiles(id,frm)

	def on_fileReceived(self, sid, id):
		mainWindow=self.main
		autoDownload=False
		if unicode(sid) in self.main.allowedSids.keys():
			#if unicode(self.ft[sid].fromjid).find("rpc@jabbim.cz")==-1:
				#filename = self.main.allowedSids[unicode(sid)]
			#else:
				#return
			filename = self.main.allowedSids[unicode(sid)]
				#filename = self.main.realHomeDir+'/'+self.ft[sid].fileprops['name']
			autoDownload=True
		elif self.main.allowedJids.has_key(self.ft[sid].fromjid.userhost()+"/"+self.ft[sid].fileprops['name']):
			filename=self.main.allowedJids[self.main.getJid(unicode(self.ft[sid].fromjid)).userhost()+"/"+self.ft[sid].fileprops['name']]+"/"+self.ft[sid].fileprops['name']
			autoDownload=True
		elif self.main.config['autoDownload'] == 'True' and unicode(self.ft[sid].fromjid).find("rpc@jabbim.cz")==-1:
			filename = self.main.config['autoDownloadPath']+'/'+self.ft[sid].fileprops['name']
			autoDownload=True
		if autoDownload:
			self.main.events.addFTDownloadEvent(unicode(self.ft[sid].fromjid.full()),filename,"",sid,self.ft[sid].fileprops['size'])
			self.receiveFile(sid, id,  filename)
		else:
			if unicode(self.ft[sid].fromjid).find("rpc@jabbim.cz")==-1:
				if self.ft[sid].fileprops.has_key('preview'):
					image=base64.decodestring(str(unicode(self.ft[sid].fileprops['preview'])))
					pixmap=QtGui.QPixmap()
					pixmap.loadFromData(image)
				else:
					pixmap=None
				#eventWidget=self.main.events.addBooleanEvent(self.ftStarted,[sid,id],None,[],self.main.tr("File transfer"),text= unicode(" %s is sending you file."%unicode(self.ft[sid].tojid)),height=40,name=unicode(self.ft[sid].tojid),typ="ftTransfer",icon=None)
				#eventWidget=self.main.events.addFTReceivedEvent(sid,id,unicode(self.ft[sid].tojid.userhost()),pixmap)
				event=self.main.events.addBooleanEvent('fileDownload','filetransfers')
				event.setAcceptHandler(self.ftStarted,[sid,id])
				event.setRejectHandler(self._declineFT,[sid,id])
				widget=event.getWidgets()[0]
				user=self.main.ui.roster.getNameByJID(self.ft[sid].fromjid.userhost())
				widget.setText(unicode(user)+" "+unicode(mainWindow.tr("is sending you file"))+" "+unicode(self.ft[sid].fileprops['name'])+" ("+str(self.toNormalSize(int(self.ft[sid].fileprops['size'])))+")")
				widget.setAcceptText(unicode(mainWindow.tr("Accept")))
				widget.setRejectText(unicode(mainWindow.tr("Reject")))
				widget.ui.accept.setIcon(QtGui.QIcon('images/16x16/actions/ok.png'))
				self.dispatcher.publishEvent('FTFileReceivedEvent', weakref.ref(event))
				tab,index=self.main.chat.findTab(unicode(self.ft[sid].fromjid.userhost()),typ=['chat'])
				if tab:
					mainWindow=self.main
					#w=widgets.chatwidget.FTAskWidget(self.ft[sid].fileprops['name'],eventWidget,tab.chat,tab.chat.ui.ftwidget)
					#QtCore.QObject.connect(eventWidget.submitButton,QtCore.SIGNAL("clicked(bool)"),w.accept)
					#QtCore.QObject.connect(eventWidget.closeButton,QtCore.SIGNAL("clicked(bool)"),w.reject)
					#if pixmap:
						#w.setPreview(pixmap)
					#tab.chat.ui.ftwidget.layout().addWidget(w)
					message=mainWindow.tr("User is sending you file")+" "+unicode(self.ft[sid].fileprops['name'])+". <a href=\"javascript:messageObject.acceptFT('"+unicode(sid)+"');\">["+mainWindow.tr("Accept")+"]</a> <a href=\"javascript:messageObject.rejectFT('"+unicode(sid)+"');\">["+mainWindow.tr("Decline")+"]</a>"
					tab.chat.ui.webkit.messageObject.ft[unicode(sid)]=event
					tab.chat.textEditWrite('<div id="ft'+unicode(sid)+'">'+self.main.webkitThemeFactory.genChatStatus(unicode(message),self.main.now())+"</div>")
					tab.chat.lastMessageFrom=""

	def toNormalSize(self,size):
		try:
			original=int(size)
			new=int(size/1000) # kB
			if new==0:
				return str(round(original,2.0))+" B" # B
			size=new
			new=int(size/1000) # MB
			if new==0:
				return str(round(original/1000.0,2))+" kB" # kB
			return str(round(original/1000000.0,2))+" MB" # MB
		except:
			return 'N/A'

	def _declineFT(self,sid,  id):
		log.msg("_declineFT")
		tab,index=self.main.chat.findTab(unicode(self.ft[sid].fromjid),typ=['chat'])
		if tab:
			tab.chat.ui.webkit.page().mainFrame().evaluateJavaScript("removeById('ft"+unicode(sid)+"');")
			del tab.chat.ui.webkit.messageObject.ft[unicode(sid)]
		return self.declineFT(sid,  id)

	def ftStarted(self,sid,id):
		#q = QtGui.QMessageBox.question(self.main,self.main.tr("File transfer"), unicode(" %s is sending you file."%unicode(self.ft[sid].tojid)),QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		#if q == QtGui.QMessageBox.Yes:
		mainWindow=self.main
		directory = mainWindow.config['lastDownloadDir']
		filename = QtGui.QFileDialog.getSaveFileName(self.main, mainWindow.tr("Save File"), directory + '/' + self.ft[sid].fileprops['name'],mainWindow.tr("*.*"))
		mainWindow.config['lastDownloadDir'] = os.path.dirname(unicode(filename))
		tab,index=self.main.chat.findTab(unicode(self.ft[sid].fromjid.full()),typ=['chat'])
		if tab:
			tab.chat.ui.webkit.page().mainFrame().evaluateJavaScript("removeById('ft"+unicode(sid)+"');")
			del tab.chat.ui.webkit.messageObject.ft[unicode(sid)]
		if filename and len(filename)!=0:
			filename=unicode(filename)
			log.msg(unicode(filename))
			self.main.events.addFTDownloadEvent(unicode(self.ft[sid].fromjid.full()),filename,"",sid,self.ft[sid].fileprops['size'])
			log.msg('receiving file: ' + sid)

			self.ft[sid].method = 'http://jabber.org/protocol/bytestreams'
			self.ft[sid].filepath = filename
			self.receiveFile(sid, id, filename)


	def on_verify(self, id, thread, props, frm, typ): #xep0070
# 		self.replyVerify(id, thread, props, frm, typ, False)
		mainWindow=self.main
		#self.main.events.addBooleanEvent(self.replyVerify,[id, thread, props, frm, typ, True], self.replyVerify,[id, thread, props, frm, typ, False],header=mainWindow.tr('Auth request'),text=mainWindow.tr('URL:')+" "+unicode(props['url']) + '<br/>' +mainWindow.tr('ID:') + unicode(props['id']), height = 60,name=frm,typ="xep70")
		event=self.main.events.addBooleanEvent("verify","authorizations")
		event.setAcceptHandler(self.replyVerify,[id, thread, props, frm, typ, True])
		event.setRejectHandler(self.replyVerify,[id, thread, props, frm, typ, False])
		widget=event.getWidgets()[0]
		widget.setText(mainWindow.tr('URL:')+" "+unicode(props['url']) + ' <br/> ' +unicode(mainWindow.tr('ID:'))+" " + unicode(props['id']))
		widget.setAcceptText(mainWindow.tr("Yes"))
		widget.setRejectText(mainWindow.tr("No"))
		widget.ui.accept.setIcon(QtGui.QIcon('images/16x16/actions/ok.png'))

	def on_connect(self):
		mainWindow=self.main
		self.main.ui.loginInfo.setText(mainWindow.tr("Jabbim is connecting to the server."))
		self.main.ui.splashProgress.setValue(20)

	def on_authd(self):

		mainWindow=self.main
		self.main.ui.loginInfo.setText(mainWindow.tr("Jabbim is logged in."))
		self.main.ui.splashProgress.setValue(40)