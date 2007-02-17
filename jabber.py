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
from Queue import Queue

# here we realize jabber communication via using interface provided by xmpp
class Jabber:

	# info about user
	user = "piskworker"
	usernick = "Tester"
	server = "jabber.cz"
	resource = "Pyjim"
	password = "piskworker"
	
	# info about server
	gameAuth = "piskworker@jabber.cz/Gajim"
	# this is used to determine if message comes from gameserver of it is form someone else
	gameServer = "games.jabbim.cz"
	
	# well, we will push communication throught these queeeee things
	err = Queue()
	inc = Queue()
	outc = Queue()
	
	# here we store text from chatroom
	conf = []
	# and here store where we store those texts
	confNames = []
	# nicknames go here
	confNicks = []
	
	# helper
	linesRead = []

	# do you have any certificate verificating your python knowledge?
	# yes?
	# and you are reading comment above __init__ like you see it first time in your live?
	# then quickly return that certificate!
	def __init__(self):
		#self.MainWindow=MainWindow
		#self.MainWindow.jabberErrorHandler(113)
		pass
	

	def now(self):
		h,m,s=time.localtime()[3:6]
		return "%02d:%02d:%02d" % (h,m,s)
	
	# this function allows to join conference
	def getIntoRoom(self, room,nick):
		p = xmpp.Presence(to='%s/%s'%(room, nick))
		self.conn.send(p)
		self.confNames.append(room)
		self.conf.append([])
		self.confNicks.append([])
		self.linesRead.append(0)
		#print self.confNames
		
	def getOffRoom(self, room):
		p = xmpp.Presence(to='%s/%s'%(room, self.usernick), typ="unavailable")
		p.setShow("offline")
		self.conn.send(p)
		
		try:
			Conf = self.confNames.index(room)
			self.confNames.remove(room)
			self.conf[Conf] = Null
			self.confNicks[Conf] = Null
		except:
			pass
		
	#4 d3bug .. i mean fof debug
	def printChat(self):
		for i in self.conf:
			for n in i:
				print n
				
	# this returns new lines in particual chatroom
	# argument room is full name of room eg. "programovani@conf.netlab.cz"
	def newChatLines(self, room):
		if room in self.confNames:
			index = self.confNames.index(room)
			a = self.conf[index][(self.linesRead[index]):]
			self.linesRead[index] += len(a)
			return a

	# returns old lines...
	def oldChatLines(self, room):
		if room in self.confNames:
			index = self.confNames.index(room)
			a = self.conf[index][:(self.linesRead[index])]
			return a
	
	# who is in particular room ?
	def usersInRoom(self, room):
		if room in self.confNames:
			index = self.confNames.index(room)
			a = self.confNicks[index]
			return a
		
	# what the heck ya think will func named setStaus do?
	# it will not make dinner for you!
	def setStatus(self, status="online", text=""):
		presence = xmpp.Presence()
		presence.setStatus(text)
		presence.setShow(status)
		self.conn.send(presence)
		for room in self.confNames:
			presence.setTo(room + "/" + self.usernick)
			self.conn.send(presence)

	# main and only handler for incoming messages
	def incoming(self, conn, mess):
		
		# some nasty things can happen there, that's why whole funcion body is in try statement
		# actually it can happen that text is something different than text (some un-slice-able object)
		try:
			# Replacing html tags...
			text=mess.getBody().replace("<","&lt;").replace(">","&gt;")
			user=mess.getFrom()
			nick=mess.getFrom().getResource()
			typ=mess.getType()
			print user,typ
			if typ=="chat":
				jid = str(user).rsplit("/")[0]
				self.inc.put(["chat_message", jid,user,text])
			elif typ=="groupchat":
				jid = str(user).rsplit("/")[0]
				if len(str(user).rsplit("/"))==1:
					self.inc.put(["groupchat_server_message", jid,text])
				else:
					user=str(user).rsplit("/")[1]
					self.inc.put(["groupchat_message", jid,user,text])

			# this implements /me IRC style messages
			
			#if len(text) > 3:
				#if text[0:3] == "/me":
					#text = "* %s %s" % (nick, text[4:])
					#meStyleAct = True
				#else:
					#meStyleAct = False
			#else:
				#meStyleAct = False
			
			# this may look tricky. i'll shall explain:
			# when message comes from conference, it has format of
			# name@subdomain.server.tld/UserOfConference
			# e.g. "programovani@conf.netlab.cz/Ricardo"
			# so we have to split it and get just conf. name
			
			#if len(split) == 2:
				#Conf = split[0]
				#User = nick
				
				#if Conf in self.confNames:
					#index = self.confNames.index(Conf)
					#if not meStyleAct:
						#color="black"
						#if text.lower().find(self.usernick.lower())!=-1:
							#color="red"
						#if User==self.usernick:
							#color="blue"
						#self.conf[index].append(('[<font color="gray">'+self.now()+'</font>] <font color="'+color+'"><b>'+ User + '</b>: ' + text+'</font>'))
					#else:
						#self.conf[index].append(('[<font color="gray">'+self.now()+'</font>] ' + text))
					
			#if len(split) >= 1:
				#split2 = split[0].rsplit("@")
				#if len(split2) == 2:
					#if split2[1] <> self.gameServer:
						#pass
						##print type(user)
						##a = xmpp.protocol.Message(to = user, body = "I am sorry. This is auto sorry.")
						##self.conn.send(a)
			##print self.conf
			
			#self.income.put([text, sender])
		except:
			print "exception allmost catched"

	# this handles presnece stantzas
	def presenceHandle(self, conn, pres):
		user = pres.getFrom()
		nick = pres.getFrom().getResource()
		#print pres.getFrom().getNode(), pres.getFrom().getDomain()
		prType = pres.getType()
		jid = pres.getFrom().getNode() + "@" + pres.getFrom().getDomain()
		print prType,jid
		if prType=="subscribe":
			self.inc.put(["subscribe", jid])
		else:
			self.inc.put(["nick_update",jid,pres,nick])
		#if Conf in self.confNames:
			#index = self.confNames.index(Conf)
			
			#listed = False
			
			#for record in self.confNicks[index]:
				#if record[0] == nick:
					#listed = True
			
			#if not listed:
				#self.confNicks[index].append([nick, "unknown", "unknown"])
			
			##if not nick in self.confNicks[index]:
			##	self.confNicks[index].append([nick, "unknown", "unknown"])
				
			
			#for record in self.confNicks[index]:
				#if record[0] == nick:
					##print pres.getStatus(), pres.getShow()
					#record[1] = pres.getStatus()
					#record[2] = pres.getShow()
					
			
			#if prType == "unavailable":
				#for record in self.confNicks[index]:
					#if record[0] == nick:
						#self.confNicks[index].remove(record)
			
			#self.inc.put(["nick_update", Conf])
				
		##print pres.getShow()
		##print pres.getStatus()
		##print nick

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
		a = xmpp.protocol.Message(room,text,"groupchat")
		self.conn.send(a)

	# this allows us to send message into conferency
	def sendToConf(self, room, text):
		a = xmpp.protocol.Message(room,text,"chat")
		self.conn.send(a)


	# StepOn and GoOn ;)
	def StepOn(self, conn):
		
		try:
			self.conn.Process(1)
		except KeyboardInterrupt: return 0
		return 1

	def GoOn(self, conn):
		
		while self.StepOn(self.conn): pass
	
	
	# what should i say here ?
	def disconnect(self):
		
		self.conn.disconnect()
		self.connected = False
		print "Disconecting."
	
	
	# this function is encapsulated in thread, because it would get main window stucked when connecting
	# thread which encapsulates it is defined in connect(self)
	def connect_thrd(self):
		
		user,server,password,resource=self.user,self.server,self.password,self.resource
		
		self.conn=xmpp.Client(server, debug=[])
		
		conres=self.conn.connect()
		
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
		else:
			self.inc.put(["con_ready"])
		
		if authres<>'sasl':
			return 1
		
		self.conn.RegisterHandler('message', self.incoming)
		self.conn.RegisterHandler('iq',self.iqHandle)
		self.conn.RegisterHandler('presence',self.presenceHandle)
		#conn.RegisterDisconnectHandler(self.off)
		
		
		self.roster = self.conn.getRoster()
		self.inc.put(["roster_update", self.roster])
		self.conn.sendInitPresence()
		

		#self.discovery=xmpp.features.discoverInfo(self.conn,"icq.netlab.cz")
		#print self.discovery
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