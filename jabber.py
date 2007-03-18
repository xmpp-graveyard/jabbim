
"""
jabber.py is jabber backend for client side of jabber based game.
Copyright (C) 2007 Richard Szlachta

This program is free software; you can rediunicodeibute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is diunicodeibuted in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""

import threading, sys, time, sha, time
import xmpp
from xmpp.protocol import *
from Queue import Queue
try:
	# for timers and events
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
class groupchat:

	def groupchatSend(self, room, text):
		# Send message to the room
		a = xmpp.protocol.Message(room,text,"groupchat")
		self.conn.send(a)

	def getIntoRoom(self,room,nick):
		# join to conference
		self.addStoreQueue(room,nick) # keep incoming presences and messages to this room when we connecting
		p = xmpp.Presence(to='%s/%s'%(room, nick))
		self.conn.SendAndCallForResponse(p,self._getIntoRoomHandler,args={'room':room,'nick':nick},myid="getintoroom")
		# send message to GUI, because we are opened the room
		self.mutex.lock()
		event=customEvent(["room_opened",room,nick,""])
		self.main.customEvent(event)
		self.mutex.unlock()
		#self.inc.put(["room_opened",room,nick,""])

	def _getIntoRoomHandler(self,i,rep,room,nick):
		# join to conference handler
		if isErrorNode(rep):
			# we get error
			code=str(rep.getErrorCode())
			print str(rep.getError())
			self.mutex.lock()
			event=customEvent("muc-"+code,'err')
			self.main.customEvent(event)
			self.mutex.unlock()
			#self.err.put("muc-"+code)
			#self.deleteStoreQueue(room) # stop keeping messages
		else:
			# we are connected
			self.presenceHandle(self.conn,rep)
			#self.inc.put(["room_opened",room,nick,rep.getAffiliation()])

	def getOffRoom(self,room,nick):
		# get off room
		p = xmpp.Presence(to='%s/%s'%(room, nick), typ="unavailable")
		p.setShow("offline")
		self.conn.send(p)

	def groupchatSetAdminList(self,jid,items,role=None,affiliation=None,toDel=None):
		# muc#admin support
		# sets muc#admin lists
		iq=Iq(to=jid,typ='set',queryNS=NS_MUC_ADMIN,xmlns=None)
		for item in items:
			if role!=None:
				iq.getTag("query").addChild("item",{"jid":item,"role":role})
			else:
				iq.getTag("query").addChild("item",{"jid":item,"affiliation":affiliation})
		# some item to delete. todel=[jid_to_del,role_or_affiliation_used_for_deleting]
		if toDel!=None:
			if role!=None:
				iq.getTag("query").addChild("item",{"jid":toDel[0],"role":toDel[1]})
			else:
				iq.getTag("query").addChild("item",{"jid":toDel[0],"affiliation":toDel[1]})
		self.conn.SendAndCallForResponse(iq,self._groupchatSetAdminListHandler,args={"jid":jid,'role':role,'affiliation':affiliation,'toDel':toDel,'items':items},myid="groupchatsetadminlist")

	def _groupchatSetAdminListHandler(self,i,rep,jid,role,affiliation,toDel,items):
		# sets muc#admin handler
		if isErrorNode(rep):
			# we get error
			code=str(rep.getErrorCode())
			print unicode(rep)
			print str(rep.getError())
			self.mutex.lock()
			event=customEvent("muc_set_admin_list-"+code,'err')
			self.main.customEvent(event)
			self.mutex.unlock()
			#self.err.put("muc_set_admin_list-"+code)
		else:
			# items setted => send info to GUI
			self.mutex.lock()
			event=customEvent(["group_chat_admin_list_setted",jid,role,affiliation,toDel,items])
			self.main.customEvent(event)
			self.mutex.unlock()
			#self.inc.put(["group_chat_admin_list_setted",jid,role,affiliation,toDel,items])

	def getGroupchatConfig(self,muc):
		# get groupchat config form (muc#owner)
		iq=Iq(to=muc,typ='get',queryNS=NS_MUC_OWNER,xmlns=None)
		self.conn.SendAndCallForResponse(iq,self._groupchatConfigHandler,args={"muc":muc},myid="groupchatconfig")

	def _groupchatConfigHandler(self,i,rep,muc):
		# sets muc#admin handler
		if isErrorNode(rep):
			# we get error
			code=str(rep.getErrorCode())
			print unicode(rep)
			print str(rep.getError())
			self.mutex.lock()
			event=customEvent("muc_config-"+code,'err')
			
			self.main.customEvent(event)
			self.mutex.unlock()
			#self.err.put("muc_config-"+code)
		else:
			# send form to GUI
			self.mutex.lock()
			event=customEvent(["group_chat_config",rep,muc])
			
			self.main.customEvent(event)
			self.mutex.unlock()
			#self.inc.put(["group_chat_config",rep,muc])

	def getGroupchatAdminList(self,muc,role=None,affiliation=None):
		# get groupchat admin list (muc#admin)
		iq=Iq(to=muc,typ='get',queryNS=NS_MUC_ADMIN,xmlns=None)
		if role!=None:
			iq.getTag("query").addChild("item",{"role":role})
		else:
			iq.getTag("query").addChild("item",{"affiliation":affiliation})
		self.conn.SendAndCallForResponse(iq,self._getGroupchatAdminListHandler,args={"muc":muc,'role':role,'affiliation':affiliation},myid="groupchatadminlist")

	def _getGroupchatAdminListHandler(self,i,rep,muc,role,affiliation):
		# groupchat admin list handler
		if not isResultNode(rep):
			# we get error
			code=str(rep.getErrorCode())
			print unicode(rep)
			print str(rep.getError())
			self.mutex.lock()
			event=customEvent("groupchat_admin_list-"+code,'err')
			
			self.main.customEvent(event)
			self.mutex.unlock()
			#self.err.put("groupchat_admin_list-"+code)
		else:
			# get jids and save them to the list items
			items=[]
			for i in rep.getQueryPayload():
				if not isinstance(i,unicode):
					if i.getName()=="item":
						jid = i.getAttr("jid")
						items.append(jid)
			# inform GUI
			self.mutex.lock()
			event=customEvent(["group_chat_admin_list",items,muc,role,affiliation])
			
			self.main.customEvent(event)
			self.mutex.unlock()
			#self.inc.put(["group_chat_admin_list",items,muc,role,affiliation])

	def setGroupchatConfig(self,host,info):
		# set groupchat config
		iq=Iq(to=host,typ='set',queryNS=NS_MUC_OWNER,xmlns=None)
		# makes iq
		iq.getTag("query").addChild("x",{"xmlns":"jabber:x:data","type":"submit"})
		if type(info)<>type({}): info=info.asDict()
		for i in info.keys():
			iq.getTag("query").getTag('x').addChild("field",{"var":i})
			iq.getTag("query").getTag('x').getTag("field",{"var":i}).setTagData("value",info[i])
		#self.conn.send(iq)
		self.conn.SendAndCallForResponse(iq,self._setGroupchatConfigHandler,myid="setgroupchatconfig")
		# little hack for jgames
		try:
			self.listGames(int(host[:2]))
		except: pass

	def _setGroupchatConfigHandler(self,i,rep):
		# set groupchat config handler
		if not isResultNode(rep):
			# we get error
			code=str(rep.getErrorCode())
			print unicode(rep)
			print str(rep.getError())
			self.mutex.lock()
			event=customEvent("groupchat_set_config-"+code,'err')
			
			self.main.customEvent(event)
			self.mutex.unlock()
			#self.err.put("groupchat_set_config-"+code)

class vcard:
	
	def getVCard(self,jid,onlyAvatar=False):
		# get vcard informations
		xmpp.vcard.getVcard(self.conn,jid,self._getVCardHandler,onlyAvatar)

	def _getVCardHandler(self,i,rep,jid,onlyAvatar):
		# getVCard handler
		# if we get bad result, send to GUI empty vcard
		if not isResultNode(rep) or rep.getVCardPayload()==None or len(rep.getVCardPayload())==0:
			if onlyAvatar==True:
				self.mutex.lock()
				event=customEvent(["avatar_show",{},jid])
				
				self.main.customEvent(event)
				self.mutex.unlock()
				#self.inc.put(["avatar_show",{},jid])
			else:
				self.mutex.lock()
				event=customEvent(["vcard_show",{}])
				
				self.main.customEvent(event)
				self.mutex.unlock()
				#self.inc.put(["vcard_show",{}])
			return
		vcard={}
		# VCard parsing
		for i in rep.getVCardPayload():
			if not isinstance(i,unicode):
				vcard=self.parse(vcard,i)
		# send vcard to GUI
		if onlyAvatar==True:
			self.mutex.lock()
			event=customEvent(["avatar_show",vcard,jid])
			
			self.main.customEvent(event)
			self.mutex.unlock()
			#self.inc.put(["avatar_show",vcard,jid])
		else:
			self.mutex.lock()
			event=customEvent(["vcard_show",vcard])
			
			self.main.customEvent(event)
			self.mutex.unlock()
			#self.inc.put(["vcard_show",vcard])

	def parse(self,vcard,i):
		# vcard parsing function
		if len(i.getChildren())==0:
			vcard[i.getName()]=unicode(i.getData())
		else:
			test={}
			for x in i.getChildren():
				vcard[i.getName()]=self.parse(test,x)
		return vcard


# here we realize jabber communication via using interface provided by xmpp
class Jabber(QtCore.QThread,groupchat,vcard):
	user = ""
	server = ""
	resource = "Jabbim"
	password = ""
	proxy=None
	ready=False
	queue=[]
	message_queue=[]
	presence_queue=[]
	err = Queue()
	inc = Queue()
	discoveryQueue = Queue()
	outc = Queue()
	conf = []
	confNames = []
	confNicks = []
	linesRead = []
	StoreQueue={}
	events=[]

	def __init__(self,mutex):
		self.mutex=mutex
		QtCore.QThread.__init__(self)

	def getStoreQueue(self,jid):
		# get store queue messages
		if self.ready==True:
			# GUI is ready for presences, so we can send presences to GUI
			if self.StoreQueue.has_key(jid):
				if len(self.StoreQueue[jid])!=0:
					for i in self.StoreQueue[jid][1]:
						self.mutex.lock()
						event=customEvent(i)
						
						self.main.customEvent(event)
						self.mutex.unlock()
						#self.inc.put(i)
			print "ready for deleting"
			self.deleteStoreQueue(jid)

	def deleteStoreQueue(self,jid):
		# delete queue item
		del self.StoreQueue[jid]
		print "deleting store queue for",jid

	def addStoreQueue(self,jid,nick):
		# add new item for queue
		print "adding store queue for",jid
		self.StoreQueue[jid]=[nick,[]]

	def setStatus(self,rooms,status="online", text=""):
		# set status and status message
		presence = xmpp.Presence()
		presence.setStatus(text)
		presence.setShow(status)
		self.conn.send(presence)
		# we have to set status for opened room too
		for room,data in rooms.iteritems():
			presence.setTo(room + "/" + data[0])
			self.conn.send(presence)

	def unregister(self,host):
		# unregister transport
		print xmpp.features.unregister(self.conn,host)

	def register(self,host,info):
		# register transport
		print xmpp.features.register(self.conn,host,info)

	def getRegInfo(self,jid):
		# get service discovery register information (register forms, inunicodeuctions etc)
		self.mutex.lock()
		event=customEvent(["discovery_register",xmpp.features.getRegInfo(self.conn,jid),unicode(jid)])
		
		self.main.customEvent(event)
		self.mutex.unlock()
		#self.inc.put(["discovery_register",xmpp.features.getRegInfo(self.conn,jid),unicode(jid)])

	def disco(self,rep,jid,typ,node,back):
		# discovery info and items handler
		ret=[]
		identities , features = [] , []
		for i in rep:
			if not isinstance(i,unicode):
				if typ=="items":
					if i.getName()=='agent' and i.getTag('name'): i.setAttr('name',i.getTagData('name'))
					self.mutex.lock()
					event=customEvent([back,typ,i.attrs,unicode(jid),node],'discovery')
					
					self.main.customEvent(event)
					self.mutex.unlock()
					#self.discoveryQueue.put([back,typ,i.attrs,unicode(jid),node])
					#ret.append(i.attrs)
				if typ=="info":
					for i in rep:
						if not isinstance(i,unicode):
							if i.getName()=='identity': identities.append(i.attrs)
							elif i.getName()=='feature': features.append(i.getAttr('var'))
							elif i.getName()=='agent':
								if i.getTag('name'): i.setAttr('name',i.getTagData('name'))
								if i.getTag('description'): i.setAttr('name',i.getTagData('description'))
								identities.append(i.attrs)
								if i.getTag('groupchat'): features.append(NS_GROUPCHAT)
								if i.getTag('register'): features.append(NS_REGISTER)
								if i.getTag('search'): features.append(NS_SEARCH)
					self.mutex.lock()
					event=customEvent([back,typ,identities,features,unicode(jid)],'discovery')
					
					self.main.customEvent(event)
					self.mutex.unlock()
					#self.discoveryQueue.put([back,typ,identities,features,unicode(jid)])

	def discoveryItems(self,server=None,node=None,back=None):
		# send discovery items request
		if server==None:
			server=self.server
		xmpp.features.discoverItems(self.conn,server,self.disco,node=node,back=back)

	def discoveryInfo(self,server=None,back=None):
		# send discovery info request
		if server==None:
			server=self.server
		xmpp.features.discoverInfo(self.conn,server,self.disco)

	def bookmarksHandle(self,i,rep):
		# getBookmarks request handler and parser (XEP-0048)
		bookmarks={}
		if isResultNode(rep):
			for i in rep.getQueryPayload():
				if i.getName()=="storage":
					for x in i.getChildren():
						if x.getName()=="conference":
							attrs=x.getAttrs()
							if attrs.has_key("jid"):
								data={}
								if attrs.has_key("name"):
									data["name"]=attrs["name"]
								else:
									data["name"]=attrs["jid"]
								if attrs.has_key("autojoin"):
									data["autojoin"]=attrs["autojoin"]
								else:
									data["autojoin"]="0"
								if x.getTag("nick")!=None:
									data["nick"]=x.getTag("nick").getData()
								else:
									data["nick"]=""
								if x.getTag("password")!=None:
									data["password"]=x.getTag("password").getData()
								else:
									data["password"]=""
								bookmarks[attrs["jid"]]=data
		self.mutex.lock()
		event=customEvent(["bookmarks", bookmarks])
		
		self.main.customEvent(event)
		self.mutex.unlock()
		#self.inc.put(["bookmarks", bookmarks])

	def sendFile(self,to,file,desc=''):
		#si=self.conn.SFileTransfer()
		a=self.conn.SIFileTransfer.sendSIFile(to,file,desc)

	def getBookmarks(self):
		# get bookmarks (XEP-0048)
		xmpp.features.getBookmarks(self.conn,self.bookmarksHandle)

	def setBookmarks(self,data):
		# se bookmarks (XEP-0048)
		xmpp.features.setConference(self.conn,data,self.setBookmarksHandle)

	def setBookmarksHandle(self,conn,rep):
		# se bookmarks (XEP-0048)
		if isErrorNode(rep):
			# we get error
			code=str(rep.getErrorCode())
			print str(rep.getError())
			self.mutex.lock()
			event=customEvent("setPrivateData-"+code,'err')
			
			self.main.customEvent(event)
			self.mutex.unlock()
			#self.err.put("muc-"+code)
			#self.deleteStoreQueue(room) # stop keeping messages
		else:
			# we are connected
			self.mutex.lock()
			event=customEvent(["private_data_set"])
			
			self.main.customEvent(event)
			self.mutex.unlock()
			#self.inc.put(["room_opened",room,nick,rep.getAffiliation()])


	def listGames(self, gameType):
		iq = xmpp.protocol.Iq(
		to = "games.jabbim.cz",
		attrs={"type":"get"},
		node = """
<iq>
 <jgames xmlns="http://njs.netlab.cz/game">
  <game action="list" type="%02d"/>
 </jgames>
</iq>
		""" % (gameType)
		)
		self.conn.SendAndCallForResponse(iq,self.listGamesHandler)
	def listGamesHandler(self,i,rep):
		games=[]
		if not isResultNode(rep):
			return
		a = rep.getPayload()
		for x in a:
			try:
				items=x.getChildren()
				for item in items:
					jid = item.getAttr("jid")
					name = item.getAttr("name")
					status = item.getAttr("status")
					games.append([jid,name,status])
			except:
				pass
		self.inc.put(["game_list", games])

	def incoming(self, conn, mess):
		# Incoming messages handler
		
		if 1==1: # ok.. it's for my comfort, when i'm using try statement
			text=mess.getBody() # get message text
			if text!=None:
				# replace html tags in message
				text=text.replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>")
			subject=mess.getSubject() # get message subject (for MUC subject for example)
			if subject!=None:
				# replace html tags in subject
				subject=subject.replace("<","&lt;").replace(">","&gt;")
			user=mess.getFrom() # get sender of message
			timestamp=mess.getTimestamp() # get timestamp
			resource=mess.getFrom().getResource() # get message resource
			typ=mess.getType() # get type of message
			new=True # temp variable
			jid=""
			if typ=="chat":
				# put chat message to the message_queue
				jid = unicode(unicode(user).rsplit("/")[0]).lower()
				self.message_queue.append(["chat_message", jid,user,text,resource])
			elif typ=="normal":
				# put chat message to the message_queue
				jid = unicode(unicode(user).rsplit("/")[0]).lower()
				self.message_queue.append(["chat_message", jid,user,text,resource])
			elif typ=="headline":
				# put headline message to the message_queue
				jid = unicode(unicode(user).rsplit("/")[0]).lower()
				urls=[] # urls in jabber:x:oob
				descs=[] # descs in jabber:x:oob
				for x in mess.getTags('x',namespace=NS_X_OOB):
					# get url
					urls.append(x.getTag("url").getData())
					# get descs, if we have some
					try:
						descs.append(x.getTag("desc").getData())
					except:
						descs.append(u"None")
				self.message_queue.append(["headline_message",jid,text,subject,urls,descs,timestamp])
			elif typ=="groupchat":
				# put groupchat message to the message_queue
				jid = unicode(unicode(user).rsplit("/")[0]).lower()
				if len(unicode(user).rsplit("/"))==1:
					# no nickname => groupchat_server_message
					self.message_queue.append(["groupchat_server_message", jid,text,subject])
				else:
					# normal groupchat_message
					user=unicode(user).rsplit("/")[1]
					self.message_queue.append(["groupchat_message", jid,user,text,timestamp])
			else:
				# unknown message type
				new=False
				print "Unknown chat type",unicode(typ)
			# if jid is in StoreQueue, we store the message
			if self.StoreQueue.has_key(jid) and new:
				self.StoreQueue[jid][1].append(self.message_queue[-1])
				del self.message_queue[-1]
			else:
				if self.ready==True:
					# GUI is ready for messages, so we can send messages to GUI
					if len(self.message_queue)!=0:
						for i in self.message_queue:
							self.mutex.lock()
							event=customEvent(i)
							
							self.main.customEvent(event)
							self.mutex.unlock()
							#self.inc.put(i)
						self.message_queue=[]

	def presenceHandle(self, conn, pres):
		if isErrorNode(pres):
			return
		# presence handle
		user = pres.getFrom() # get user
		nick = pres.getFrom().getResource() # get nick (it's resource in MUC)
		prType = pres.getType() # get type
		jid = pres.getFrom().getNode() + "@" + pres.getFrom().getDomain() # get jid
		jid=unicode(jid).lower()

		if prType=="subscribe":
			# subscribe request
			self.presence_queue.append(["subscribe", jid])
		elif prType=="subscribed":
			# subscribed information
			self.presence_queue.append(["subscribed", jid])
		else:
			# normal presence
			self.presence_queue.append(["nick_update",jid,pres,nick])
		# if jid is in StoreQueue, we store the presence
		if self.StoreQueue.has_key(jid):
			self.StoreQueue[jid][1].append(self.presence_queue[-1])
			del self.presence_queue[-1]
		else:
			if self.ready==True:
				# GUI is ready for presences, so we can send presences to GUI
				if len(self.presence_queue)!=0:
					for i in self.presence_queue:
						self.mutex.lock()
						event=customEvent(i)
						
						self.main.customEvent(event)
						self.mutex.unlock()
					self.presence_queue=[]

	def iqHandle(self, conn, iq):
		#print "iq", unicode(iq)
		#print iq.getChildren()
		a = iq.getPayload()
		for x in a:
			try:
				act = x.getTagAttr("game", "action")
				#print act
				if act == "created":
					self.gsid = x.getTagAttr("game", "gsid")
					#print "gsid", self.gsid
				if act == "new":
					if x.getTagAttr("error", "type") == "cancel":
						#print "server denies your requerst"
						pass
			except:
				pass
		#pass

	def chatSend(self, jid, text):
		# Send chat message for jid
		a = xmpp.protocol.Message(jid,text,"chat")
		self.conn.send(a)

	def xmppPingReply(self, conn, iq):
		iq = iq.buildReply('result')
		self.conn.send(iq)
		raise NodeProcessed
		
	# StepOn and GoOn ;)
	def StepOn(self, conn):
		if self.connected==False:
			return 0
		try:
			self.conn.Process(1)
		except KeyboardInterrupt: return 0
		except: time.sleep(1)
		return 1

	def GoOn(self, conn):
		while self.StepOn(self.conn): pass
	
	
	def disconnect(self):
		# disconnect
		self.connected = "quit"
		try:
			self.conn.disconnect()
		except: pass
		print "Disconecting."

	def off(self):
		# disconnect handler
		#if self.connected!="quit":
			#print "reconnecting"
			#self.connected="reconnect"
			#self.conn=xmpp.Client(self.server)#,debug=[])
			##jabberLogin(self,user,server,password,resource,proxy)
			#try: self.conn.Dispatcher.PlugOut()
			#except: pass
			#if not self.conn.connect(proxy=self.proxy): return
			#print "reauthing"
			#if not self.conn.auth(self.user,self.password,self.resource): return
			#self.conn.Dispatcher.restoreHandlers(self.handlerssave)
			#self.conn.pluginFiletransfer()
			#self.connected=True
			#self.alive=True
			#print "connected"
			#event=customEvent(["reconnect",self.user,self.server,self.password,self.resource,self.proxy])
			#self.main.customEvent(event)
		self.connected=False
		print "off"
		self.mutex.lock()
		event=customEvent(["disconnected"])
		
		self.main.customEvent(event)
		self.mutex.unlock()

	def streamErrorHandler(self,conn,error):
		name,text='error',error.getData()
		for tag in error.getChildren():
			if tag.getNamespace()==NS_XMPP_STREAMS:
				if tag.getName()=='text': text=tag.getData()
				else: name=tag.getName()
		if name=="conflict":
			self.connected=False
			print "conflict detect => turn off"
		else:
			print "STREAM ERROR",name,text

	def connect_thrd(self):
		print "start",self
		user,server,password,resource=self.user,self.server,self.password,self.resource
		proxy=self.proxy
		
		self.conn=xmpp.Client(server,debug=[])
		
		conres=self.conn.connect(proxy=proxy)
		self.alive=True
		self.connected = True
		
		if not conres:
			self.connected = False
			self.mutex.lock()
			event=customEvent("con",'err')
			
			self.main.customEvent(event)
			self.mutex.unlock()
			time.sleep(1) # maybe we actually don't need it here, but it looks hax0rz, don't ya think ?
			sys.exit(1)
			
		
		elif conres<>'tls':
			return 0
				
		authres = self.conn.auth(user,password,resource)
		
		if not authres:
			self.mutex.lock()
			event=customEvent("auth",'err')
			
			self.main.customEvent(event)
			self.mutex.unlock()
			self.connected = False
			self.alive=False
			time.sleep(1) # maybe we actually don't need it here, but it looks hax0rz, don't ya think ?
			sys.exit(1)

		
		if authres<>'sasl':
			return 1
		self.conn.RegisterHandler('error',self.streamErrorHandler,xmlns=NS_STREAMS)
		self.conn.RegisterHandler('message', self.incoming)
		#self.conn.RegisterHandler('iq',self.iqHandle)
		self.conn.RegisterHandler('presence',self.presenceHandle)
		self.conn.RegisterDisconnectHandler(self.off)
		self.conn.RegisterHandler('iq', self.xmppPingReply, 'get', NS_XMPP_PING)
		#self.conn.pluginFiletransfer()
		self.roster = self.conn.getRoster()
		self.mutex.lock()
		event=customEvent(["roster_update", self.roster])
		
		self.main.customEvent(event)
		self.mutex.unlock()
		#self.inc.put(["roster_update", self.roster])
		self.ready=False
		while not self.ready:
			try:
				self.ready = self.outc.get(timeout = 0)
			except:
				self.ready = False
		#self.ready=True
		self.conn.sendInitPresence()
		self.discoveryItems()
		event2=customEvent(["con_ready"])
		QtGui.QApplication.postEvent(self.main,event2)
		#self.inc.put(["con_ready"])
		#self.discovery=xmpp.features.discoverInfo(self.conn,server)
		#print xmpp.features.setConference(self.conn,"jabber@conf.netlab.cz","Jabber","false","HanzZik","")
		self.handlerssave=self.conn.Dispatcher.dumpHandlers()
		if self.connected:
			self.GoOn(self.conn)
			#if self.connected=="reconnect":
				#print "new try"
				#self.connect_thrd()
			return 2
		

	def isalive(self):
		if self.alive==True:
			
			self.alive=False
			print "ping"
			iq=Iq(to=self.server,typ='get',queryNS=NS_TIME,xmlns=None)
			self.conn.SendAndCallForResponse(iq,self._alive,myid="connectiontest")
		else:
			#print self.connected
			#if self.connected!=False:
				#self.conn.disconnect()
			#else:
			if self.alive==2:
				print "disconnect"
				self.connected=False
				self.mutex.lock()
				event=customEvent(["disconnected"])
				
				self.main.customEvent(event)
				self.mutex.unlock()
				#sys.exit(1)
				#self.off()
			elif self.alive==False:
				print "second ping"
				self.alive=2
				iq=Iq(to=self.server,typ='get',queryNS=NS_TIME,xmlns=None)
				self.conn.SendAndCallForResponse(iq,self._alive,myid="connectiontest")

	
	def _alive(self,conn,iq):
		print "pong"
		self.alive=True

	# see connect_thrd(self)
	def run(self):
		print "run"
		self.connect_thrd()
		#global v1
		#v1 = threading.Thread(target = self.connect_thrd)
		## daemonized thread will be auto-killed when terminating application
		#v1.setDaemon(True)
		#v1.start()
		print "finish",self

	def customEvent(self,event):
		data=event.data
		
		if data[0]=="isalive":
			if self.connected==True:
				self.isalive()
			
		elif data[0]=="disconnect":
			self.disconnect()
			
		elif data[0]=="get_into_room":
			jid=data[1]
			nickname=data[2]
			if nickname==None:
				nickname=self.user
			self.getIntoRoom(jid,nickname)
		
		elif data[0]=="set_bookmarks":
			bookmarks=data[1]
			self.setBookmarks(data[1])
			
		elif data[0]=="discovery_items":
			try:
				jid=data[1]
			except:
				jid=None
			try:
				back=data[2]
			except:
				back=None
			self.discoveryItems(jid,back=back)
		
		elif data[0]=="discovery_info":
			try:
				jid=data[1]
			except:
				jid=None
			self.discoveryInfo(jid)
		
		elif data[0]=="set_status":
			try:
				status=data[2]
			except:
				status="online"
			try:
				text=data[3]
			except:
				text=""
			self.setStatus(data[1],status,text)

		elif data[0]=="get_bookmarks":
			self.getBookmarks()
			
		elif data[0]=="get_store_queue":
			self.getStoreQueue(data[1]) # getStoreQueue
		
		elif data[0]=="roster_authorize":
			self.roster.Authorize(data[1])



class customEvent(QtCore.QEvent):
	def __init__(self,data,typ="inc"):
		apply(QtCore.QEvent.__init__,(self,QtCore.QEvent.User))
		self.data=list(data)
		self.typ=unicode(typ)
