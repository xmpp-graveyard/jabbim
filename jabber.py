"""
jabber.py is jabber backend for client side of jabber based game.
Copyright (C) 2007 Richard Szlachta

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

import threading, sys, time, sha, time
import xmpp
from xmpp.protocol import *
from Queue import Queue

# here we realize jabber communication via using interface provided by xmpp
class Jabber:
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

	def __init__(self):
		pass

	def VCardHandler(self,i,rep,jid,onlyAvatar):
		if not isResultNode(rep) or rep.getVCardPayload()==None or len(rep.getVCardPayload())==0:
			if onlyAvatar==True:
				self.inc.put(["avatar_show",{},jid])
			else:
				self.inc.put(["vcard_show",{}])
			return
		vcard={}
		for i in rep.getVCardPayload():
			if not isinstance(i,unicode):
				vcard=self.parse(vcard,i)
		if onlyAvatar==True:
			self.inc.put(["avatar_show",vcard,jid])
		else:
			self.inc.put(["vcard_show",vcard])
		
	def parse(self,vcard,i):
		if len(i.getChildren())==0:
			vcard[i.getName()]=unicode(i.getData())
		else:
			test={}
			for x in i.getChildren():
				vcard[i.getName()]=self.parse(test,x)
		return vcard

	def getVCard(self,jid,onlyAvatar=False):
		# get vcard informations
		xmpp.vcard.getVcard(self.conn,jid,self.VCardHandler,onlyAvatar)
	
	def getIntoRoom(self,room,nick):
		# join to conference
		p = xmpp.Presence(to='%s/%s'%(room, nick))
		self.conn.send(p)
		self.confNames.append(room)
		self.conf.append([])
		self.confNicks.append([])
		self.linesRead.append(0)

	def getOffRoom(self,room,nick):
		p = xmpp.Presence(to='%s/%s'%(room, nick), typ="unavailable")
		p.setShow("offline")
		self.conn.send(p)
		try:
			Conf = self.confNames.index(room)
			self.confNames.remove(room)
			self.conf[Conf] = Null
			self.confNicks[Conf] = Null
		except:
			pass

	def setStatus(self,rooms,status="online", text=""):
		presence = xmpp.Presence()
		presence.setStatus(text)
		presence.setShow(status)
		self.conn.send(presence)
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
		# get service discovery register information (register forms, instructions etc)
		self.inc.put(["discovery_register",xmpp.features.getRegInfo(self.conn,jid),str(jid)])

	def disco(self,rep,jid,typ,node):
		# discovery info and items handler
		ret=[]
		identities , features = [] , []
		for i in rep:
			if not isinstance(i,unicode):
				if typ=="items":
					if i.getName()=='agent' and i.getTag('name'): i.setAttr('name',i.getTagData('name'))
					self.discoveryQueue.put([typ,i.attrs,str(jid),node])
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
					self.discoveryQueue.put([typ,identities,features,str(jid)])

	def discoveryItems(self,server=None,node=None):
		# send discovery items request
		if server==None:
			server=self.server
		xmpp.features.discoverItems(self.conn,server,self.disco,node=node)

	def discoveryInfo(self,server=None):
		# send discovery info request
		if server==None:
			server=self.server
		xmpp.features.discoverInfo(self.conn,server,self.disco)

	def groupchatConfigHandler(self,i,rep,muc):
		self.inc.put(["group_chat_config",rep,muc])

	def getGroupchatConfig(self,muc):
		# get groupchat config form
		iq=Iq(to=muc,typ='get',queryNS=NS_MUC_OWNER,xmlns=None)
		print unicode(iq)
		self.conn.SendAndCallForResponse(iq,self.groupchatConfigHandler,args={"muc":muc})
	
	def setGroupchatConfig(self,host,info):
		# get groupchat config form
		#iq=Iq(to=muc,typ='get',queryNS=NS_MUC_OWNER,xmlns=None)
		#self.conn.SendAndCallForResponse(iq,self.groupchatConfigHandler,args={"muc":muc})
		iq=Iq(to=host,typ='set',queryNS=NS_MUC_OWNER,xmlns=None)
		iq.getTag("query").addChild("x",{"xmlns":"jabber:x:data","type":"submit"})
		if type(info)<>type({}): info=info.asDict()
		for i in info.keys():
			iq.getTag("query").getTag('x').addChild("field",{"var":i})
			iq.getTag("query").getTag('x').getTag("field",{"var":i}).setTagData("value",info[i])
		print unicode(iq)
		self.conn.send(iq)
		try:
			self.listGames(int(host[:2]))
		except: pass
		
		#if isResultNode(resp): return 1

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
		self.inc.put(["bookmarks", bookmarks])

	def getBookmarks(self):
		# get bookmarks (XEP-0048)
		xmpp.features.getBookmarks(self.conn,self.bookmarksHandle)

	def setBookmarks(self,data):
		# se bookmarks (XEP-0048)
		return xmpp.features.setConference(self.conn,data)

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
		if 1==1:
		#try:
			text=mess.getBody() # get message text
			if text!=None:
				# replace html tags in message
				text=text.replace("<","&lt;").replace(">","&gt;")
			subject=mess.getSubject() # get message subject (for MUC subject for example)
			if subject!=None:
				# prelace html tags in subject
				subject=subject.replace("<","&lt;").replace(">","&gt;")
			user=mess.getFrom() # get sender of message
			resource=mess.getFrom().getResource() # get message resource
			typ=mess.getType() # fet type of message
			print unicode(user),typ
			if typ=="chat":
				# put chat message to the message_queue
				jid = str(str(user).rsplit("/")[0]).lower()
				self.message_queue.append(["chat_message", jid,user,text,resource])
			elif typ=="groupchat":
				# put groupchat message to the message_queue
				jid = str(str(user).rsplit("/")[0]).lower()
				if len(str(user).rsplit("/"))==1:
					# no nickname => groupchat_server_message
					self.message_queue.append(["groupchat_server_message", jid,text,subject])
				else:
					# normal groupchat_message
					user=str(user).rsplit("/")[1]
					self.message_queue.append(["groupchat_message", jid,user,text])
			if self.ready==True:
				# GUI is ready for messages, so we can send messages to GUI
				if len(self.message_queue)!=0:
					for i in self.message_queue:
						self.inc.put(i)
					self.message_queue=[]


	def presenceHandle(self, conn, pres):
		# presence handle
		user = pres.getFrom() # get user
		nick = pres.getFrom().getResource() # get nick (it's resource in MUC)
		prType = pres.getType() # get type
		jid = pres.getFrom().getNode() + "@" + pres.getFrom().getDomain() # get jid
		jid=str(jid).lower()
		print prType,jid,nick,self.ready

		if prType=="subscribe":
			# subscribe request
			self.presence_queue.append(["subscribe", jid])
		elif prType=="subscribed":
			# subscribed information
			self.presence_queue.append(["subscribed", jid])
		else:
			# normal presence
			self.presence_queue.append(["nick_update",jid,pres,nick])
		if self.ready==True:
			# GUI is ready for presences, so we can send presences to GUI
			if len(self.presence_queue)!=0:
				for i in self.presence_queue:
					self.inc.put(i)
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

	def groupchatSend(self, room, text):
		# Send message to the room
		a = xmpp.protocol.Message(room,text,"groupchat")
		self.conn.send(a)

	def chatSend(self, jid, text):
		# Send normal message for jid
		a = xmpp.protocol.Message(jid,text,"chat")
		self.conn.send(a)

	def xmppPingReply(self, conn, iq):
		iq = iq.buildReply('result')
		self.conn.send(iq)
		raise NodeProcessed
		
	# StepOn and GoOn ;)
	def StepOn(self, conn):
		if not self.connected:
			return 0
		try:
			self.conn.Process(1)
		except KeyboardInterrupt: return 0
		return 1

	def GoOn(self, conn):
		while self.StepOn(self.conn): pass
	
	
	def disconnect(self):
		# disconnect
		self.conn.disconnect()
		self.connected = False
		print "Disconecting."

	def off(self):
		# disconnect handler
		pass
	
	def connect_thrd(self):
		user,server,password,resource=self.user,self.server,self.password,self.resource
		proxy=self.proxy
		
		self.conn=xmpp.Client(server,debug=[])
		
		conres=self.conn.connect(proxy=proxy)
		
		self.connected = True
		
		if not conres:
			self.connected = False
			self.err.put("con")
			time.sleep(1) # maybe we actually don't need it here, but it looks hax0rz, don't ya think ?
			sys.exit(1)
			
		
		elif conres<>'tls':
			return 0
				
		authres = self.conn.auth(user,password,resource)
		
		if not authres:
			self.err.put("auth")
			self.connected = False
			time.sleep(1) # maybe we actually don't need it here, but it looks hax0rz, don't ya think ?
			sys.exit(1)

		
		if authres<>'sasl':
			return 1

		self.conn.RegisterHandler('message', self.incoming)
		self.conn.RegisterHandler('iq',self.iqHandle)
		self.conn.RegisterHandler('presence',self.presenceHandle)
		self.conn.RegisterDisconnectHandler(self.off)
		self.conn.RegisterHandler('iq', self.xmppPingReply, 'get', NS_XMPP_PING)
		
		self.roster = self.conn.getRoster()
		self.inc.put(["roster_update", self.roster])
		self.ready=False
		while not self.ready:
			try:
				self.ready = self.outc.get(timeout = 0)
			except:
				self.ready = False

		self.conn.sendInitPresence()
		self.discoveryItems()
		self.inc.put(["con_ready"])
		#self.discovery=xmpp.features.discoverInfo(self.conn,server)

		#print xmpp.features.setConference(self.conn,"jabber@conf.netlab.cz","Jabber","false","HanzZik","")

		if self.connected:
			self.GoOn(self.conn)
			return 2
	
	
	# see connect_thrd(self)
	def connect(self):
		
		global v1
		v1 = threading.Thread(target = self.connect_thrd)
		# daemonized thread will be auto-killed when terminating application
		v1.setDaemon(True)
		v1.start()
