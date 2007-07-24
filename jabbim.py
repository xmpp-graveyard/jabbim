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
sys.path.append('.')
try: from PyQt4 import QtCore, QtGui
except: print "PyQt4 is not installed."
import qt4reactor
app = QtGui.QApplication(sys.argv)
qt4reactor.install(app)
from twisted.internet import reactor
from twisted.python import log
import shutil
import time,base64
try:
	from hashlib import sha1
except:
	log.msg('Please upgrade to python2.5')
	from sha import new as sha1

import widgets
import pyxl
from pyxl import storage

from configobj import ConfigObj
from include import utils
import urllib
from imp import load_source
from urllib import quote, unquote
from include import plugins
from os.path import basename

#mutex=QtCore.QMutex()

class clientClass(pyxl.client.Client):

	def on_init(self):
		self.roster['groups']['Unknown']=self.main._addGroup('Unknown')
		self.temp_hosts=[]

	def on_GCpresenceError(self, fromjid, code, typ, name):
		log.msg("ERROR")
		QtGui.QMessageBox.warning(self.main,self.main.tr("Error"),unicode(fromjid+" "+code+" "+typ+" "+name),0,1)

	def on_GCpresenceError(self, fromjid, code, typ, name):
		QtGui.QMessageBox.warning(self.main,self.main.tr("Error"),unicode(fromjid+" "+code+" "+typ+" "+name),0,1)

	def on_roleErr(self,  muc,  err,  nick):
		QtGui.QMessageBox.warning(self.main,self.main.tr("Error"),unicode(muc+" "+err+" "+nick),0,1)
	
	def on_affiliationErr(self,  muc,  err,  nick):
		QtGui.QMessageBox.warning(self.main,self.main.tr("Error"),unicode(muc+" "+err+" "+nick),0,1)

	def on_ftEnd(self, sid, error = None): #pokud je error None je vse v poradku, jinak strucny popis chyby.
		self.main.ftError[sid]=error
		del self.ft[sid]

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
		for item in self.main.ui.roster.getHostItems("@"+jid):
			show=unicode(item.text(1))[0]
			item.setIcon(0,self.main.getIcon("jid@"+jid,size="32x32",status=self.main.icons[show]))

	def on_rosterAddUser(self, contact):
		#locker=QtCore.QMutexLocker(mutex)
		# add user to the roster
		groups=list(contact.groups)
		name=unicode(contact.name)
		jid=unicode(contact.jid)
		log.msg("JID: "+jid+" "+contact.subscription)
		for gr in groups:
			if not self.roster['groups'].has_key(gr):
				self.roster['groups'][gr]=self.main._addGroup(gr)
		# get host info
		if len(unicode(jid).rsplit("@"))!=1:
			host=unicode(jid).rsplit("@")[1]
			if not self.disco.has_key(host) and not host in self.temp_hosts:
				#self.main.getUserType(host)
				self.temp_hosts.append(host)
				self.getDiscoInfo(host)

		# user is not in any group
		if len(groups)==0:
			#add user item to Unknown group
			self.main.ui.roster.addUser(jid,name,self.roster['groups']['Unknown'],first=True)
		else:
			for group in groups:
				# add user item to the group
				self.main.ui.roster.addUser(jid,name,self.roster['groups'][unicode(group)],first=True)
		# show avatar if he has him
		self.main.cache.get_avatar(jid, self.main._loadAvatar)

	def on_discoItemsBookmarksReceived(self, jid):
		# make user list for bookmarked groupchat
		item=self.main.ui.bookmarks.findItems(jid,QtCore.Qt.MatchExactly,1)[0]
		for name in self.disco[jid][None]['items'].keys():
			user=QtGui.QTreeWidgetItem(item)
			user.setText(0,unicode(name))
			user.setText(1,unicode(name))
			user.setIcon(0,self.main.getIcon(size="16x16"))

	def on_rosterArrived(self):
		# build Bookmarks tab

		self.main.buildBookmarks()
		self.main.autoJoinGroupchat()
		# vymazani metakontaktu
		#self.roster_meta={}
		#self.setMetacontacts()

		# hide Unknown group, if has not users
		if int(self.main.ui.roster.getGroupItem("Unknown").childCount())==0:
			self.main.ui.roster.setItemHidden(self.roster['groups']['Unknown'],True)

		self.metaParents={}

		## get metacontacts
		#meta={} # temp variable for metacontacts - {userTag:userJid}
		#for jid,user in self.roster['users'].iteritems():
			#if user.tag!=None:
				#if not meta.has_key(user.tag):
					#meta[user.tag]=[[jid,user.order]]
				#else:
					#meta[user.tag].append([jid,user.order])

		#log.msg("META:"+unicode(meta))


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
		self.main.rosterHideOffline(True)
		#self.main.ui.roster.refreshStats()
		self.main.ui.roster.sortItems (1,QtCore.Qt.AscendingOrder)


		for k,v in self.roster['groups'].iteritems():
			self.main.ui.add_group.addItem(unicode(k))

##		log.msg( "METAPARENTS"+unicode(self.metaParents))

	def on_authFailed(self,xmlstream):
		# Authentication error
		self.main.ui.login_connect.setEnabled(True)
		QtGui.QMessageBox.warning(self.main,self.main.tr("Error"),unicode(self.main.tr("Bad Jabber ID or password.")),0,1)
	
	def on_firstpresence(self,  bulk):
		# process all first presences at once
		for presence in bulk:
			#print presence
			jid=presence[0]
			show=presence[1]
			self.on_presence(jid,show,True)
		# refresh group stats
		self.main.rosterHideOffline(True)
		self.main.ui.roster.refreshStats()
		self.main.ui.roster.sortItems (1,QtCore.Qt.AscendingOrder)

	def on_GCpresence(self,  muc, nick,  show,  status,  codes = []):
		if show=="offline":
			# get user role
			# find good tab according to jid
			for i in range(self.main.chat.ui.chatTab.count()):
				w=self.main.chat.ui.chatTab.widget(i)
				if unicode(w.jid)==unicode(muc):
					# edit user item
					w.chat.removeUser(nick)
					#del self.groupchats[muc].users[nick]
					break
		else:
			# get user role
			role=self.groupchats[muc].users[nick].role
			# find good tab according to jid
			for i in range(self.main.chat.ui.chatTab.count()):
				w=self.main.chat.ui.chatTab.widget(i)
				if unicode(w.jid)==unicode(muc):
					# edit user item
					w.chat.editUser(nick,show,role)
					break

	def on_presence(self,jid,show,first=False):
		log.msg("PRESENCE")
		if show=="offline":
			jid=jid.full() # get jid
			# presence has resource
			if len(unicode(jid).rsplit("/"))!=1:
				resource=unicode(jid).rsplit("/")[1]
				jid=unicode(jid).rsplit("/")[0]
				# contact has more than one resource
				if len(self.roster['users'][jid].resources)>1:
					# set status by highest resource
					highest=self.roster['users'][jid].resources[self.roster['users'][jid].getHighestResource()]
					self.main.ui.roster.setStatus(jid,highest.show,first=first)
				else:
					# set status by this presence
					self.main.ui.roster.setStatus(jid,show,first=first)
			else:
				self.main.ui.roster.setStatus(jid,show,first=first)
		else:
			jid=jid.full() # get jid
			# presence has resource
			if len(unicode(jid).rsplit("/"))!=1:
				resource=unicode(jid).rsplit("/")[1]
				jid=unicode(jid).rsplit("/")[0]
				# get highest resource and status
				highest=self.roster['users'][jid].resources[self.roster['users'][jid].getHighestResource()]
				status=None
				if highest.status!=None:
					status=highest.status.replace("\n"," ").replace("<","&lt;").replace(">","&gt;")
				# set status
				self.main.ui.roster.setStatus(jid,highest.show,status=status,first=first)
			else:
				# get user status
				status=self.roster['users'][jid].status[1]
				if status!=None:
					status=status.replace("\n"," ").replace("<","&lt;").replace(">","&gt;")
				# set status
				self.main.ui.roster.setStatus(jid,show,status=status,first=first)
				
	def on_xml(self,xml):
		# append xml to the xml console, it it's enabled...
		if self.main.xmlConsole.ui.enable.isChecked():
			text=unicode(xml)
			self.main.xmlConsole.ui.xml.append(text+"\n\n")
	
	def on_UpdateContact(self,jid):
		# contact is updated
		contact=self.roster['users'][jid]
		items=self.main.ui.roster.getUserItems(jid)
		toDel=[] # temp variable for deleting items at the end of this function
		toDelJid=[]
		toDelIndex=[]
		log.msg(jid+" "+unicode(contact.groups))
		for gr in contact.groups:
			if not self.roster['groups'].has_key(gr):
				self.roster['groups'][gr]=self.main._addGroup(gr)
		# go through all groups
		for name,item in self.roster['groups'].iteritems():
			# updated contact has to be in this group
			if name in self.roster['users'][jid].groups:
				add=True
				# go through all user items, find item in this group and edit it
				for i in items:
					parent=i.parent()
					if item==parent:
						add=False # we found item
						name=contact.name
						if name==None or len(name)==0:
							name=jid
						i.setText(0,unicode(name))
						i.setText(1,unicode(i.text(1))[0]+unicode(name).lower())
						i.setText(2,unicode(name))
						i.setData(32,0,QtCore.QVariant([unicode(jid),unicode('contact')]))
						self.main.ui.roster.setStatus(jid,self.main.icons[unicode(i.text(1))[0]],i)
						self.main.ui.roster.sortItems(1,QtCore.Qt.AscendingOrder)
				# we didn't find item
				if add:
					# we have some item to clone (so we can't create new one)
					if len(items)!=0:
						i=items[0].clone() # clone contact item
						#self.roster['users'][jid].rosterItems.append(i)
						# don't know, if we need this code now, so keep coomented...
						#for x in range(int(i.childCount())):
							#child=i.child(x)
							#it=child.data(32,0)
							#it=it.toList()
							#data=unicode(it[0].toString())
							#typ=unicode(it[1].toString())
							#if typ=="meta":
								#self.roster['users'][data].rosterItems.append(child)
						self.roster['groups'][name].addChild(i) # add item to the new group
						index=self.main.ui.roster.indexFromItem(self.roster['groups'][name],0)
						self.main.ui.roster.expand(index)
						self.main.ui.roster.setStatus(jid,None,i)
					else:
						# add new contact to the roster
						self.main.ui.roster.addUser(contact.jid,contact.name,self.roster['groups'][name])
						self.main.ui.roster.sortItems(1,QtCore.Qt.AscendingOrder)
						self.main.ui.roster.setStatus(jid,None)
						self.main.ui.roster.refreshStats()
			else:
				# user is not in this group, so we have to delete them from this group, if he is there
				for i in self.main.ui.roster.getUserItems(jid):
					parent=i.parent()
					if item==parent:
						#toDelJid.append(unicode(jid))
						#toDelIndex.append(self.roster['users'][unicode(jid)].rosterItems.index(i))
						parent.takeChild(parent.indexOfChild(i))
						# delete group, if it's empty
						if int(parent.childCount())==0:
							toDel.append(unicode(parent.text(2)))
							self.main.ui.roster.takeTopLevelItem(self.main.ui.roster.indexOfTopLevelItem(parent))
						break
		# delete all groups saved in toDel
		#for i in range(len(toDelJid)):
			#jid=toDelJid[i]
			#index=toDelIndex[i]
			#del self.roster['users'][jid].rosterItems[index]
		#for name in toDel:
			#del self.roster['groups'][name]

	def on_unsubscribe(self,jid):
		self.on_DeleteContact(jid)

	def on_DeleteContact(self,jid):
		# delete contact from roster
		log.msg("delete contact")
		#contact=self.roster['users'][jid]
		items=self.main.ui.roster.getUserItems(jid,'contact')
		lenght=int(len(items))
		for i in range(lenght):
			item=self.main.ui.roster.getUserItems(jid)[0]
			if item.childCount()==0:
				#log.msg("DELETE ITEM:"+unicode(item.text(1)))
				parent=item.parent()
				if parent:
					index=parent.indexOfChild(item)
					if index>-1:
						it=parent.takeChild(index)
						#it.view=0
						#del it
						#it=0
			#else:
				#for bla in range(int(item.childCount())):
					##log.msg("CHILD:"+unicode(item.child(bla).text(1)))
					#log.msg(unicode(item.child(bla)))
		log.msg("DELETE COMPLETE")
		#for name,item in self.roster['groups'].iteritems():
			#for i in items:
				#parent=i.parent()
				#if item==parent:
					#parent.takeChild(parent.indexOfChild(i))
					##if parent.childCount()==0:
						##self.main.ui.roster.takeTopLevelItem(self.main.ui.roster.indexOfTopLevelItem(parent))
						##del self.roster['groups'][unicode(parent.text(2))]
					#break
		#for name,item in self.metaParents.iteritems():
			#for i in items:
				#parent=i.parent()
				#if item==parent:
					#parent.takeChild(parent.indexOfChild(i))
					#if parent.childCount()==0:
						#group=parent.parent()
						#group.takeChild(group.indexOfChild(parent))
						##if group.childCount()==0:
							##self.main.ui.roster.takeTopLevelItem(self.main.ui.roster.indexOfTopLevelItem(group))
							##del self.roster['groups'][unicode(group.text(2))]
					#break
		self.main.ui.roster.refreshStats()

	def on_subscribe(self, frm,status):
		#self.ui.infoDockWidget.show()
		item=QtGui.QListWidgetItem(self.main.ui.eventsListWidget)
		item.setSizeHint(QtCore.QSize(100,40))
		item.widget=widgets.rosterWidget.SubscribeWidget(unicode(frm),item,self.main,self.main.ui.eventsListWidget,unicode(status))
		self.main.ui.eventsListWidget.setItemWidget(item,item.widget)

	def on_GCmessage(self, frm, typ, body, subject = None, xhtml = None,  chatstate = None,  delay = None):
		# handle messages from groupchat
		# get user (resource) and MUC jid (saved in frm)
		if len(unicode(frm).rsplit("/"))==2:
			user=unicode(frm).rsplit("/")[1]
			frm=unicode(frm).rsplit("/")[0]
		else:
			user=frm
		body=unicode(body).replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>")
		# find MUC tab
		for i in range(self.main.chat.ui.chatTab.count()):
			w=self.main.chat.ui.chatTab.widget(i)
			if unicode(w.jid)==frm:
				# set room topic
				if subject!=None:
					w.chat.ui.info.setText(unicode(subject))
					#w.chat.ui.info.setCursorPosition(0)
				# set links, if we found them
				for word in unicode(body).split(' '):
					if word.find("http://")!=-1:
						body=body.replace(word,'<a href="'+unicode(urllib.unquote(word))+'">'+word+'</a>')
				# no delay message
				if delay==None or len(delay)==0:
					# it's our message
					if unicode(w.name)==unicode(user):
						message=self.main.skin["my_message"].replace("[time]",self.main.now()).replace("[user]",user).replace("[message]",unicode(body))
					else:
						# it's message for us
						if unicode(body).lower().find(unicode(w.name).lower())!=-1:
							message=self.main.skin["message_for_me"].replace("[time]",self.main.now()).replace("[user]",user).replace("[message]",unicode(body))
						else:
							message=self.main.skin["message"].replace("[time]",self.main.now()).replace("[user]",user).replace("[message]",unicode(body))
					# write message
					w.chat.textEditWrite(message)
					return
				else:
					# get delay from string
					delay=unicode(delay)
					delay="%s-%s-%s %s:%s:%s" % (delay[0:4],delay[4:6],delay[6:8],delay[9:11],delay[12:14],delay[15:17])
					# our delayed message
					if unicode(w.name)==unicode(user):
						message=self.main.skin["my_message_history"].replace("[time]",delay).replace("[user]",user).replace("[message]",unicode(body))
					else:
						# delayed message for us
						if unicode(body).lower().find(unicode(w.name).lower())!=-1:
							message=self.main.skin["message_for_me_history"].replace("[time]",delay).replace("[user]",user).replace("[message]",unicode(body))
						else:
							message=self.main.skin["message_history"].replace("[time]",delay).replace("[user]",user).replace("[message]",unicode(body))
					w.chat.textEditWrite(message)

	def on_message(self, frm, typ, body, subject = None, xhtml = None,chatstate = None,  delay = None):
		# handle normal 'chat' messages
		# get user icon or name, if we have him in roster. Or use default icon and jid as name
		user=self.main.ui.roster.getUserItems(unicode(frm).rsplit("/")[0])
		if len(user)!=0:
			#user=self.roster['users'][unicode(frm).rsplit("/")[0]].rosterItems[0]
			icon=user[0].icon(0)
			user=user[0].text(2)
		else:
			icon=self.main.getIcon(status="offline",size="16x16")
			user=frm
		# strip html tags and \n from messages
		if xhtml==None:
			message=unicode(body).replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>")
		else:
			message=xhtml
		message=self.main.skin["message"].replace("[time]",self.main.now()).replace("[user]",unicode(user)).replace("[message]",message)
		# find tab
		tab=None
		tabIndex=0
		for i in range(self.main.chat.ui.chatTab.count()):
			w=self.main.chat.ui.chatTab.widget(i)
			if unicode(w.jid)==unicode(frm):
				tab=w
				tabIndex=i
				break
			if unicode(w.jid).rsplit("/")[0]==unicode(frm).rsplit("/")[0]:
				tab=w
				tabIndex=i
		# we found tab
		if tab!=None:
			# write message and set 'message' icon
			if int(self.main.chat.ui.chatTab.currentIndex())!=tabIndex:
				self.main.chat.ui.chatTab.setTabIcon(tabIndex,QtGui.QIcon("images/16x16/actions/message.png"))
				self.main.chat.ui.chatTab.tabBar().setTabTextColor(i,QtGui.QColor(255,0,0))
			tab.chat.textEditWrite(message)
		else:
			# add new chattab
			self.main.chat.addChatTab(frm,unicode(user),icon,message)

	def on_vcardReceived(self,  jid, card):
		#print card
		#TODO: zpracovat ukladani vcardu .. hash a cesta k souboru se ulozi do db
		log.msg("vcard "+unicode(jid))
		if card.has_key("BINVAL"):
			pixmap=QtGui.QPixmap()
			image=base64.decodestring(str(card["BINVAL"]))
			f=open(self.main.homeDir+'/avatars/'+jid,"wb")
			f.write(image)
			f.close()
			pixmap.loadFromData(image)
			for item in self.main.ui.roster.getUserItems(jid):
##				log.msg(utils.cprint("yellow","setting icon: "+jid))
				item.setIcon(3,QtGui.QIcon(pixmap))
			#for item in self.main.ui.roster.getMetaItems(jid):
##				log.msg(utils.cprint("yellow","setting icon: "+jid))
				#item.setIcon(3,QtGui.QIcon(pixmap))
			sha=sha1(image).hexdigest()
			#self.main.cache.set_avatar(jid, ['avatars/'+jid, sha])
			#self.main._loadAvatar('avatars/'+jid, sha, jid)
		else:
			self.main.cache.set_avatar(jid, ['nic', 'nic'])


class mainWindow(QtGui.QMainWindow):
	def __init__(self,parent=None):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		self.ui=widgets.mainWindow.Ui_MainWindow()
		self.ui.setupUi(self)
		self.homeDir=utils.getHomeDir() # get home dir
		print self.homeDir
		utils.loadConfig(self) # load config files
		self.cache = storage.Cache(db=self.homeDir+'/cache.db')
		

		self.ui.gridlayout.setMargin(1)
		self.ui.gridlayout.setSpacing(1)

		self.ui.tabWidget.setTabText(0,"")
		self.ui.tabWidget.setTabText(1,"")
		self.ui.tabWidget.setTabText(2,"")

		self.filetransferTimer=QtCore.QTimer()
		self.ftError={}
		QtCore.QObject.connect(self.filetransferTimer, QtCore.SIGNAL("timeout()"),self.refreshFT)
		self.copyPlugins()
		# variables
		self.hosts={} # temp variable for {hos:type_of_host}
		self.filetransfer={}
		self.filetransferQueue=[]
		self.client=None # pyxl client instance
		self.chat=widgets.chatwindow.chatWindow(self,self)
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
		self.offline=False
		self.xmlConsole=XMLConsole(self)

		self.ui.showOffline.hide()


		# mainwindows signals
		app.connect(self.ui.login_connect, QtCore.SIGNAL("clicked()"),self.connect)
		app.connect(app,QtCore.SIGNAL("lastWindowClosed() "),self.disconnect)
		app.connect(self.ui.showOffline, QtCore.SIGNAL("clicked(bool)"),self.hideOffline)
		app.connect(self.ui.actionShow_XML, QtCore.SIGNAL("triggered ( bool )"),self.showXml)
		app.connect(self.ui.actionPreferences, QtCore.SIGNAL("triggered ( bool )"),self.preferencesClicked)
		app.connect(self.ui.actionJoin_Groupchat, QtCore.SIGNAL("triggered ( bool )"),self.joinGroupchat)
		QtCore.QObject.connect(self.ui.bookmarks, QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.bookmarksContextMenu)
		app.connect(self.ui.addContact, QtCore.SIGNAL("clicked ()"),self.addContactMainWindow)
		app.connect(self.ui.newBookmark, QtCore.SIGNAL("clicked ()"),self.newBookmark)
		QtCore.QObject.connect(self.ui.bookmarks, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.bookmarksClicked)

		# fill login form
		self.ui.login_password.setText(self.config['passwd'])
		self.ui.login_jid.setText(self.config['jid'])
		if self.config['savePasswd']=="True":
			self.ui.login_savePassword.setChecked(True)
		# set up bookmarks treeWidget
		self.ui.bookmarks.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.ui.bookmarks.header().hide()
		self.ui.bookmarks.hideColumn(1)
		# set up stacked widget (0==login,1==roster and etc..)
		self.ui.rosterStackedWidget.setCurrentIndex(0)
		self.loadRoster() # load roster widget
		self.loadSkin() # load chat skin

		# Status menu
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
		#self.config['rosterIconSize']="22x22"
		#self.addInfoSubscribe()
		#self.addInfoSubscribe()
		#self.addInfoSubscribe()
		self.loadTheme()
		if self.config['log'] == 'true':
			logfile = open(self.config['logfile'], 'w')
			log.startLogging(logfile)

		self.tray=QtGui.QSystemTrayIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))
		menu=QtGui.QMenu(self)
		menu.addMenu(self.statusMenu)
		menu.addSeparator()
		action=menu.addAction(self.tr("Hide / Show"),self.trayActivated)
		menu.addAction(self.tr("Quit"),self.trayQuit)
		app.connect(self.tray,QtCore.SIGNAL("activated (QSystemTrayIcon::ActivationReason)"),self.trayActivated)
		self.tray.setContextMenu(menu)
		self.tray.show()
		w=self.config['windowGeometry'][2]
		h=self.config['windowGeometry'][3]
		if str(w)=='None' or str(h)=='None':
			if str(w)!='None':
				self.resize(int(w),self.height())
			self.move(int(self.config['windowGeometry'][0]),int(self.config['windowGeometry'][1]))
		else:
			self.setGeometry(int(self.config['windowGeometry'][0]),int(self.config['windowGeometry'][1]),int(w),int(h))

	#def addInfoSubscribe(self):
		#widget=subscribeWidget(self.ui.infoDockWidget)
		#self.ui.infoLayout.addWidget(widget)

	#def resizeEvent (self,event):
		#self.setUpdatesEnabled(False)
		#QtGui.QMainWindow(self).resizeEvent(event)
		#self.setUpdatesEnabled(True)


	def copyPlugins(self):
		plugins=os.listdir("plugins/")
		for plugin in plugins:
			path = 'plugins/%s/%s.py'%( plugin, plugin)
			path2 = '%s/plugins/%s/%s.py'%(self.homeDir, plugin, plugin)
			copy = False
			v1 = v2 = 0
			try: 
				f=open(path)
				plug = load_source(plugin, path, f).Plugin(False, self.homeDir)
			except:
				print 'spatny plugin', plugin
				continue
			#takze mam asi spravny plugin, kouknem se jestli je v homediru
			try: 
				f2=open(path2)
				plug2 = load_source(plugin, path, f2).Plugin(False, self.homeDir)
			except:
				copy = True
			try:
				v1 = float(plug.version)
			except:
				continue
	
			try:
				v2 = float(plug2.version)
			except:
				copy = True
	
			if v1>v2:
				copy = True
			if copy:
				log.msg('copy plugin to homedir: '+plugin)
				try:
					shutil.copytree("plugins/"+plugin, self.homeDir+"/plugins/"+plugin)
				except:
					shutil.rmtree(self.homeDir+"/plugins/"+plugin)
					shutil.copytree("plugins/"+plugin, self.homeDir+"/plugins/"+plugin)

	def loadPlugins(self):
		self.plugins = {}
		plugins=os.listdir(self.homeDir + "/plugins/")
		for plugin in plugins:
			if plugin in self.config['plugins']:
				path = '%s/plugins/%s/%s.py'%(self.homeDir, plugin, plugin)
				try: 
					f=open(path)
				except:
					log.msg('plugin load error: '+plugin)
					continue
				plug = load_source(plugin, path, f).Plugin(self, self.homeDir)
				f.close()
				self.plugins[plug.name] = plug
				
		log.msg("PLUGINS:"+unicode(self.plugins))

	def refreshFT(self):
		log.msg("refresh")
		toDel=[]
		print 
		for sid,widget in self.filetransfer.iteritems():
			if self.client.ft.has_key(sid):
				size=float(self.client.ft[sid].size)
				sent=float(self.client.ft[sid].transfered)
				widget.widget.progressBar.setValue(int((sent/size)*100))
			else:
				log.msg("ft.finished")
				widget.widget.progressBar.setValue(100)
				if widget.widget.complete==None:
					if self.ftError[sid]==None:
						widget.widget.stats.setText(self.tr("Complete"))
					else:
						widget.widget.stats.setText(self.tr("Error")+" "+unicode(self.ftError[sid]))
					widget.widget.complete=True
					widget.widget.closeClicked()
					toDel.append(sid)
				else:
					toDel.append(sid)
					if self.ftError[sid]==None:
						widget.widget.stats.setText(self.tr("Complete"))
					else:
						widget.widget.stats.setText(self.tr("Error")+" "+unicode(self.ftError[sid]))
					widget.widget.complete=True
				#toDel.append(sid)
		halt=True
		for sid in toDel:
			#self.
			#self.ui.eventsListWidget.takeItem(self.ui.eventsListWidget.row(self.filetransfer[sid]))
			queueId=None
			print self.filetransferQueue,self.filetransfer[sid].file
			for i in self.filetransferQueue:
				if self.filetransfer[sid].file in i:
					print i
					queueId=self.filetransferQueue.index(i)
					self.filetransferQueue[queueId].remove(self.filetransfer[sid].file)
					break
			log.msg("QUEUE:"+unicode(queueId))
			if queueId!=None:
				if len(self.filetransferQueue[queueId])!=0:
					self.filetransferTimer.stop()
					jid=self.filetransfer[sid].jid
					file=self.filetransferQueue[queueId][0]
					file=unicode(file)
					#self.jab.sendFile(jid,unicode(file))
					sid2=self.client.sendFile(jid, basename(file), file)
					item=QtGui.QListWidgetItem(self.ui.eventsListWidget)
					item.setSizeHint(QtCore.QSize(100,60))
					item.file=file
					item.jid=jid
					item.sent=self.filetransfer[sid].sent+1
					#if self.ftError[sid]==None:
						#item.broken=self.filetransfer[sid].broken
					#else:
						#item.broken=self.filetransfer[sid].broken.append(self.filetransfer[sid].file)
					item.all=self.filetransfer[sid].all
					log.msg("SENDING "+str(item.sent)+"/"+str(item.all))
					item.widget=widgets.rosterWidget.FTWidget(basename(file),item,self,sid2,self.ui.eventsListWidget,"("+str(item.sent)+"/"+str(item.all)+")")
					self.ui.eventsListWidget.setItemWidget(item,item.widget)
					self.filetransfer[sid2]=item
					self.filetransferTimer.start(500)
					if self.ftError[sid]==None:
						self.ui.eventsListWidget.takeItem(self.ui.eventsListWidget.row(self.filetransfer[sid]))
			else:
				log.msg(unicode(self.filetransferQueue))
				log.msg(unicode(self.filetransfer[sid].file))
			del self.filetransfer[sid]
		if len(self.client.ft)==0 and halt:
			log.msg("STOPPING TIMER")
			self.filetransferTimer.stop()
	def closeEvent(self,event):
		self.hide()
		event.ignore()

	def trayQuit(self):
		# turn off jabbim
		if str(self.config["saveGeometry"])=="True":
			rect=self.geometry()
			x=int(rect.x())
			y=int(rect.y())
			width=int(rect.width())
			height=int(rect.height())
			self.config["windowGeometry"]=[x,y,width,height]
			self.config.write()
		if str(self.config['saveExpandedGroups'])=='True':
			expanded=[]
			if self.client!=None:
				for name,item in self.client.roster['groups'].iteritems():
					index=self.ui.roster.indexFromItem(item,0)
					if self.ui.roster.isExpanded(index)==True:
						expanded.append(name)
				self.config['expandedGroups']=expanded
				self.config.write()

		self.tray.hide()
		app.closeAllWindows()
		self.disconnect()
		#sys.exit(0)

	def trayActivated(self,reason=QtGui.QSystemTrayIcon.Trigger):
		# show or hide main window
		if reason==QtGui.QSystemTrayIcon.Trigger:
			if self.isHidden():
				self.show()
			else:
				self.hide()

	def loadTheme(self,text=None):
		# windows hack
		self.setStyleSheet("")
		if text==None:
			theme=open("themes/"+self.config['theme']+"/style.css")
			text=theme.read()
			self.setStyleSheet(text)
			self.xmlConsole.setStyleSheet(text)
			self.chat.setStyleSheet(text)
			theme.close()
		else:
			self.setStyleSheet(text)
			self.xmlConsole.setStyleSheet(text)
			self.chat.setStyleSheet(text)


	def addContactMainWindow(self):
		# add contact
		jid=unicode(self.ui.add_jid.text())
		nickname=unicode(self.ui.add_nickname.text())
		group=unicode(self.ui.add_group.currentText())
		message=unicode(self.ui.add_message.toPlainText())
		
		self.client.addContact(jid,message,nickname,[group])
		
		self.ui.add_jid.setText("")
		self.ui.add_nickname.setText("")
		self.ui.add_message.setPlainText("")

	def bookmarksClicked(self,item,i):
		# join bookmarked groupchat
		data=item.data(0,32)
		lst=data.toList()
		jid=unicode(lst[0].toString()) # get jid
		nickname=unicode(lst[1].toString()) # get nickname
		# send jabber command
		if self.chat.addGroupChatTab(jid,nickname):
			#self.main.groupchat[room+"@"+server]=[nickname,[]]
			self.client.joinGC(jid, nickname)

	def buildBookmarks(self):
		self.ui.bookmarks.clear()
		for k,v in self.client.bookmarks['conference'].iteritems():
			# add bookmark to the bookmarks list
			item=QtGui.QTreeWidgetItem(self.ui.bookmarks)
			item.setText(0,unicode(v.name))
			item.setText(1,unicode(v.jid.full()))
			item.setData(0,32,QtCore.QVariant([unicode(v.jid.full()),unicode(v.nick),unicode(v.password)]))
			item.setIcon(0,QtGui.QIcon("images/16x16/categories/muc.png"))

	def autoJoinGroupchat(self):
		for k,v in self.client.bookmarks['conference'].iteritems():
			if (v.autojoin==True or v.autojoin=="True") or (v.autojoin==1 or v.autojoin=="1"):
				jid=unicode(v.jid.full())
				nickname=v.nick
				if self.chat.addGroupChatTab(jid,nickname):
					self.client.joinGC(jid, nickname)

	def joinGroupchat(self,bool):
		file=self.config['theme']
		style=open("themes/"+file+"/style.css")
		newchat=widgets.joingroupchat.joinGroupChatWindow(self)
		newchat.setStyleSheet(style.read())
		style.close()
		ret=newchat.exec_()

	def bookmarksContextMenu(self,pos):
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
		# set menu position and show
		menu.move(self.ui.bookmarks.mapToGlobal(pos))
		menu.show()

	#def reskin(self):
		#self.setStyleSheet(text)
		#self.chat.setStyleSheet(text)


	def newBookmark(self):
		# make new bookmark
		edit=widgets.preferences.editBookmark(self,"","","","","",False,self,False)
		ret=edit.exec_()

	def groupchatContextMenuTriggered(self,action):
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
		#self.ui.roster.sortItems (1,QtCore.Qt.AscendingOrder)
		self.ui.roster.refreshStats()
		self.offline=not bool
		self.rosterHideOffline(not bool)

	def rosterHideOffline(self,bool):
		for group,item in self.client.roster['groups'].iteritems():
			# return stats (online,offline,all users) for group
			for i in range(int(item.childCount())):
				child=item.child(i)
				if int(unicode(child.text(1))[0])==9:
					self.ui.roster.setItemHidden(child, bool)
				else:
					print unicode(child.text(1))[0]
				for x in range(int(child.childCount())):
					child2=child.child(x)
					if int(unicode(child2.text(1))[0])==9:
						self.ui.roster.setItemHidden(child2, bool)
			self.ui.roster.hidden( bool)

	def statusChanged(self,action):
		# status changed
		data=action.data()
		data=data.toString()
		setstatus=statusWindow(data)
		if setstatus.exec_()==1:
			self.ui.statusButton.setText(unicode(action.text()))
			self.ui.statusButton.setIcon(self.getIcon(status=data,size="16x16"))

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
		self.tray.showMessage(self.tr("Jabbim"),self.tr("Jabbim is ready! You are connected! :) "))


	def disconnect(self):
		#if self.client!=None:
		reactor.stop2()

	def getIcon(self,jid=None,typ=None,size="32x32",status=None,usertype="jabber"):
		if size=="22x22":
			size="32x32"
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
				icon=QtGui.QIcon(path+"jabber-online.png")
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
			
			if jid!=self.config['jid'] or (password!=self.config['passwd'] and self.config['savePasswd']=="True") or self.config['savePasswd']!=unicode(self.ui.login_savePassword.isChecked()):
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
			self.client = clientClass(jid+"/jabbim", password, jid.split("@")[1], 5222,self,reactor)
			self.client.log=True
		self.loadPlugins()
		self.ui.login_connect.setEnabled(False)
		self.client.connect()
	
	def _loadAvatar(self,file, hash, jid):
		if os.path.isfile(self.homeDir+'/'+unicode(file)):
			pixmap=QtGui.QPixmap()
			f=open(self.homeDir+'/'+unicode(file),"rb")
			image=f.read()
			f.close()
			pixmap.loadFromData(image)
			for item in self.ui.roster.getUserItems(jid):
##				log.msg(utils.cprint("yellow","setting icon: "+jid))
				item.setIcon(3,QtGui.QIcon(pixmap))
		self.client.roster['users'][jid].setAvatar(file, hash)
	
	def _addGroup(self, group):
		item=self.ui.roster.addGroup(unicode(group))
		if group in self.config['expandedGroups']:
			index=self.ui.roster.indexFromItem(item,0)
			self.ui.roster.expand(index)
		return item
	
	def _addUser(self, itemjid, name, grp):
		return self.ui.roster.addUser(itemjid,name,grp)

	def _disconnect(self, error = None): # error = None | dns | lost | auth | failed
		if error=="auth":
			QtGui.QMessageBox.warning(self,self.tr("Error"),unicode(self.tr("Bad Jabber ID or password.")),0,1)
		elif error=="dns":
			QtGui.QMessageBox.warning(self,self.tr("Error"),unicode(self.tr("Server is not found.")),0,1)
		
		MainWindow.ui.statusButton.setText(unicode(MainWindow.status["offline"]))
		MainWindow.ui.statusButton.setIcon(MainWindow.getIcon("offline",size="16x16"))
		MainWindow.ui.statusButton.hide()
		MainWindow.ui.rosterStackedWidget.setCurrentIndex(0)
		MainWindow.ui.showOffline.hide()

		#MainWindow.client.roster = {'users':{},'groups':{}}
		#MainWindow.client.roster_meta = {} # jid: {'tag':tag,  'order': 1}
		#MainWindow.client.first_presence = []
		#MainWindow.client.first_wait = True
		#MainWindow.client.bookmarks = {'conference':{}, 'url': {}}
		#MainWindow.client.roster['groups']['Unknown']=MainWindow.ui.roster.addGroup('Unknown')
		#MainWindow.client.temp_hosts=[]
		MainWindow.ui.roster.clear()
		MainWindow.ui.roster.makeHiddenItem()
		MainWindow.ui.login_connect.setEnabled(True)
		MainWindow.plugins=[]
		MainWindow.client = None


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
##			MainWindow.client.factory.stopTrying()
			MainWindow.client.sendPresence(typ = "unavailable", status = unicode(self.ui.status.toPlainText ()))
			MainWindow.client.factory.stopTrying()
			#MainWindow.client.disconnect()
			MainWindow.client.disconnect()
			del MainWindow.client
			MainWindow.client = None
			MainWindow._disconnect()
			#MainWindow.client.disconnect()
			#print MainWindow.client.roster
			#reactor.stop2()
			pass
		else:
			#app.postEvent(jab,customEvent(["set_status",self.groupchat,self.data,unicode(self.ui.status.toPlainText ())]))
			#jab.setStatus(MainWindow.groupchat,self.data,unicode(self.ui.status.toPlainText ()))
			MainWindow.client.sendPresence(show = unicode(self.data), status = unicode(self.ui.status.toPlainText ()))
		self.done(1)


translator=QtCore.QTranslator()
translator.load("locales/jabbim_"+unicode(QtCore.QLocale.system().name())[:2]+".qm")
print "trying to load locales:","locales/jabbim_"+unicode(QtCore.QLocale.system().name())[:2]+".qm"
app.installTranslator(translator)

MainWindow = mainWindow()
MainWindow.show()
reactor.run()

