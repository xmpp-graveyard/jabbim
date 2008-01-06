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

from twisted.internet.interfaces import ITransport
from twisted.internet.base      import BaseConnector
from twisted.internet           import  tcp
##from twisted.internet           import  reactor
from twisted.internet           import protocol, defer
from twisted.python             import log, failure
import struct, re, socket, sys, sha
from zope.interface import implements
from sockserror import *
from twisted.internet import interfaces
from twisted.words.xish.domish import Element
from twisted.words.protocols.jabber.xmlstream import IQ
# Used to distinguish IP address from domain name
# TODO: should this be optimized somehow?
#
_ip_regex = re.compile ("\d\d?\d?\.\d\d?\d?\.\d\d?\d?\.\d\d?\d?")
from twisted.protocols.basic  import FileSender
import  os.path, time
from base64 import b64encode, b64decode

class ClientProtocol (protocol.Protocol):
	""" This protocol that talks to SOCKS5 server from client side.
	"""
	__implements__ = ITransport,
	disconnecting = 0
	def __init__(self, sockshost, socksport, host, port, factory, otherProtocol,
		method="CONNECT", login=None, password=None, xmpp = None, xmpp_sid = None):
		""" Initializes SOCKS session
		
		@type sockshost: string
		@param sockshost: Domain name or ip address of intermediate SOCKS 
		server.
		
		@type socksport: int
		@param socksport: Port number of intermediate server.
		
		@type host: string
		@param host: Domain name or ip address where should connect or bind.
		
		@type port: int
		@param port: Port number where to connect or bind.
		
		@type otherProtocol: object
		@param otherProtocol: Initialised protocol instance, which will receive
			all I/O and events after SOCKS connected.
		
		@type login: string
		@param login: Sets user name if SOCKS server requires us to
			authenticate.
		
		@type password: string
		@param password: Sets user password if SOCKS server requires us
			to authenticate.
		
		@type method: string
		@param method: What to do: may be \"CONNECT\" only. Other
			methods are currently unsupported.
		"""
		# login and password are limited to 256 chars
		#
		if login is not None and len (login) > 255:
			raise LoginTooLongError()
		
		if password is not None and len (password) > 255:
			raise PasswordTooLongError()
		
		# save information
		#
		self.method         = method
		self.host           = host
		self.port           = port
		self.login          = login
		self.password       = password
		self.state          = "mustNotReceiveData"
		self.otherProtocol  = otherProtocol
		self.factory        = factory
		self.xmpp = xmpp
		self.xmpp_sid = xmpp_sid

	def connectionMade(self):
		# prepare connection string with available authentication methods
		#
	
		print ("SOCKS5.connectionMade")
		methods = "\x00"
		if not self.login is None: methods += "\x02"
	
		connstring = struct.pack ("!BB", 5, len (methods))
	
		self.transport.write (connstring + methods)
		self.state = "gotHelloReply"

	def dataReceived (self, data):
		print ("SOCKS state=" + self.state)
		method = getattr(self, 'socks_%s' % (self.state), 
			self.socks_thisMustNeverHappen)
		method (data)

	def socks_thisMustNeverHappen (self, data):
		self.transport.loseConnection()
		raise UnhandledStateError ("This SOCKS5 self.state (%s) "\
			"must never happen %s" % (self.state, self))

	def socks_mustNotReceiveData (self, data):
		""" This error might occur when server tells something into connection
		right after connection is established. Server in this case is
		certainly not SOCKS.
		"""
		self.transport.loseConnection()
		self.factory.clientConnectionFailed (self, failure.Failure (
			UnexpectedDataError ("Server must not send data before client %s" % 
self)))

	def socks_gotHelloReply (self, data):
		""" Receive server greeting and send authentication or ask to
		execute requested method right now.
		"""
		if data == "\x05\xFF":
			# No acceptable methods. We MUST close
			#
			print("No acceptable methods, closing connection")
			self.transport.loseConnection()
			return

		elif data == "\x05\x00":
			# Anonymous access allowed - let's issue connect
			#
			self.sendCurrentMethod()

		elif data == "\x05\x02":
			# Authentication required
			#
			self.sendAuth()

		else:
			self.transport.loseConnection()
			self.factory.clientConnectionFailed (self, failure.Failure (
				UnhandledData ("Server returned unknown reply in gotHelloReply")))

		# From now on SOCKS server considered alive - we've got reply
		#
		self.factory.status = "connected"

	def socks_gotAuthReply (self, data):
		""" Called when client received server authentication reply,
			we or close connection or issue "CONNECT" command
		"""
		if data == "\x05\x00":
			self.sendCurrentMethod()

	def sendAuth (self):
		""" Prepare login/password pair and send it to the server
		"""
		command = "\x05%s%s%s%s" % (chr (len (self.login)), self.login,
			chr (len (self.password)), self.password)
		self.transport.write (command)

		self.state = "gotAuthReply"

	def sendCurrentMethod (self):
		method = getattr(self, 'socks_method_%s' % (self.method), 
			self.socks_method_UNKNOWNMETHOD)
		method()

	def socks_method_UNKNOWNMETHOD (self):
		self.transport.loseConnection()
		self.factory.clientConnectionFailed (self, failure.Failure (
			UnknownMethod ("Method %s is unknown %s" % (self.method, self))))

	def socks_method_CONNECT (self):
		# Check if we have ip address or domain name
		#
		print("socks_method_CONNECT host = " + self.host)

	# The FaceTime SOCKS5 proxy treats IP addr the same way as hostname
	   # if _ip_regex.match (self.host):
	   #     # we have dotted quad IP address
	   #     addressType = 1
	   #     address = socket.inet_aton (self.host)
	   # else:
	   #     # we have host name
	   #     address = self.host
	   #     addressType = 3

		address = self.host
		addressType = 3
		addressLen = len(address)

		#Protocol version=5, Command=1 (CONNECT), Reserved=0
		#command = struct.pack ("!BBBB", 5, 1, 0, addressType)

		command = struct.pack ("!BBBBB", 5, 1, 0, addressType,addressLen)
		portstr = struct.pack ("!H", self.port)

		self.transport.write (command + address + portstr)
		self.state = "gotConnectReply"

	def socks_gotConnectReply (self, data):
		""" Called after server accepts or rejects CONNECT method.
		"""
		if data[:2] == "\x05\x00":
			# No need to analyze other fields of reply, we are done
			#
			self.state = "done"
			self.factory.status = "established"

			self.otherProtocol.transport = self
			self.otherProtocol.connectionMade()
			self.otherProtocol.ft = self.xmpp.ft[self.xmpp_sid]
			self.xmpp.ftStart(self.xmpp_sid, self.otherProtocol)
			return 

		errcode = ord (data[1])

		if errcode < len (SOCKS_errors):
			self.transport.loseConnection()
			self.factory.clientConnectionFailed (self, failure.Failure (
				ConnectError ("%s %s" % (SOCKS_errors[errcode], self))))
		else:
			self.transport.loseConnection()
			self.factory.clientConnectionFailed (self, failure.Failure (
				ConnectError ("Unknown SOCKS error after CONNECT request issued %s" % (self))))
		
		self.otherProtocol.ft = self.xmpp.ft[self.xmpp_sid]
		self.otherProtocol.ft.connectFailure()

	def socks_done (self, data):
		""" Proxy received data to other protocol.
		"""
		self.otherProtocol.dataReceived (data)
	#
	# Transport relaying
	#
	def write(self, data):
		self.transport.write(data)

	def writeSequence(self, data):
		self.transport.writeSequence(data)

	def loseConnection(self):
		self.disconnecting = 1
		self.transport.loseConnection()

	def getPeer(self):
		return self.transport.getPeer()

	def getHost(self):
		return self.transport.getHost()
	
	def registerProducer(self, producer, streaming):
		self.transport.registerProducer(producer, streaming)

	def unregisterProducer(self):
		self.transport.unregisterProducer()

	def stopConsuming(self):
		self.transport.stopConsuming()

class ClientConnector (tcp.Connector):
	"""Object used to connect to some host using intermediate server
	supporting SOCKS5 protocol.

	This IConnector manages one connection.
	"""
	def __init__(self, sockshost, socksport, host, port, otherFactory,
		reactor=None, method="CONNECT", login=None, password=None,
		timeout=None, readableID=None):
		""" Creates IConnector to connect through SOCKS

		@type sockshost: string
		@param sockshost: SOCKS5 compliant server address.

		@type socksport: int
		@param socksport: Port to use when connecting to SOCKS.

		@type timeout: float
		@param timeout: Time to wait until client connects, then fail.

		@type readableID: string
		@param readableID: Some human readable ID for this connection.

		See ClientProtocol constructor for details on other params.
		"""
		factory = ClientFactory (method=method, sockshost=sockshost,
			socksport=socksport, host=host, port=port, login=login,
			password=password, otherFactory=otherFactory, timeout=timeout,
			readableID=readableID)

		tcp.Connector.__init__ (self, host=sockshost, port=socksport,
			factory=factory, timeout=timeout, bindAddress=None,
			reactor=reactor)

class ClientFactory (protocol.ClientFactory):
	def __init__(self, sockshost, socksport, host, port, otherFactory,
		method="CONNECT", login=None, password=None, timeout=60,
		readableID=None, xmpp = None, xmpp_sid = None):
		""" Factory creates SOCKS5 client protocol to connect through it.
		See ClientProtocol constructor for details on params.
		
		@type globalTimeout: int
		@param globalTimeout: Seconds before connection is completely and
			unconditionally closed as is.

		@type readableID: string
		@param readableID: Some human readable ID for this connection.
		"""
		self.sockshost      = sockshost
		self.socksport      = socksport
		self.host           = host
		self.port           = port
		self.method         = method
		self.login          = login
		self.password       = password
		self.otherFactory   = otherFactory
		self.timeout        = timeout
		self.readableID     = readableID
		self.xmpp = xmpp
		self.xmpp_sid = xmpp_sid

		# This variable contains current status of SOCKS connection,
		# useful for diagnosting connection, without knowing SOCKS
		# internal states. One of: "unconnected", "connected" (SOCKS
		# server replied and is alive), "established"
		#
		self.status = "unconnected"

	def startedConnecting (self, connector):
		# Set global timeout
		#
		if self.timeout is not None:
		   log.msg ("Set timeout %d sec" % self.timeout)
		   delayedcall = self.xmpp.reactor.callLater (self.timeout, self.onTimeout, connector)
		   setattr (self, "delayed_timeout_call", delayedcall)

		# inherited
		#
		protocol.ClientFactory.startedConnecting (self, connector)

	def onTimeout (self, connector):
		""" Timeout occured, can't continue and should stop immediately
		and unconditionally in the whatever state I am.
		"""
		connector.disconnect()
		log.msg ("%s timeout %d sec" % (self, self.timeout))
		self.clientConnectionFailed (self, failure.Failure (
			GlobalTimeoutError ("Timeout %s" % self)))

	def stopFactory(self):
		""" Do cleanups such as cancelling timeout
		"""
		try:
			if self.timeout is not None:
			   self.delayed_timeout_call.cancel()
		except:
			pass
		self.xmpp.ft[self.xmpp_sid].finish()
		protocol.ClientFactory.stopFactory (self)

	def buildProtocol (self, a):
		""" Connection is successful, create protocol and let it talk to peer.
		"""
		proto = ClientProtocol (sockshost=self.sockshost,
			socksport=self.socksport, host=self.host, port=self.port,
			method=self.method, login=self.login, password=self.password,
			otherProtocol=self.otherFactory.buildProtocol (self.sockshost),
			factory=self, xmpp = self.xmpp, xmpp_sid = self.xmpp_sid)

		proto.factory = self
		return proto

	def __repr__ (self):
		return "<SOCKS %s>" % self.readableID

	def clientConnectionLost(self, connector, reason):
		# If flag indicates that connection may not be lost
		#
		rmap = {"reason": reason, "socks": self.status}
		if self.xmpp.ft[self.xmpp_sid].size > 	self.xmpp.ft[self.xmpp_sid].transfered:
			self.xmpp.ft[self.xmpp_sid].error = "Connection lost"
			
		try:
			if self.status != "established":
				# Tell about error
				#
				log.msg ("Connection LOST before SOCKS established %s" % self)
				self.otherFactory.clientConnectionFailed (connector, rmap)

			else:
				self.otherFactory.clientConnectionLost (connector, rmap)

		except:
			ei = sys.exc_info()
			if not str (ei[0]).count ("AlreadyCalled"):
				raise
	
	def clientConnectionFailed(self, connector, reason):
		# I can't know where to get deferred, let factory do this itself
		#
		rmap = {"reason": reason, "socks": self.status}

		try:
			if self.status != "established":
				log.msg ("Connection FAILED before SOCKS established %s" % self)
				self.otherFactory.clientConnectionFailed (connector, rmap)
				self.xmpp.ft[self.xmpp_sid].connectFailure()
				self.xmpp.ft[self.xmpp_sid].error = "Can't connect."
			else:
				self.otherFactory.clientConnectionFailed (connector, rmap)
		except:
			ei = sys.exc_info()
			if not str (ei[0]).count ("AlreadyCalled"):
				raise


class ProxyClientCreator(protocol.ClientCreator):

	def connectSocks5Proxy(self,remotehost,remoteport,proxy,proxyport,id):
	   d = defer.Deferred()
	   f = protocol._InstanceFactory(self.reactor, self.protocolClass(*self.args, **self.kwargs),d)
	   self.reactor.connectWith(ClientConnector,	host=remotehost,port=remoteport, sockshost=proxy, socksport=proxyport, otherFactory=f, readableID=id)
	   return d


class Send(protocol.Protocol):
	implements(interfaces.IConsumer)
	
	def registerProducer(self, producer, streaming):
		return self.transport.registerProducer(producer, streaming)
	
	def unregisterProducer(self):
		self.transport.unregisterProducer()
		self.transport.loseConnection()

	def write(self, data):
##		print 'prenasim: ', len(data)
		try:
			self.ft.connector.factory.delayed_timeout_call.cancel()
		except:
			pass
		if self.ft:
			self.ft.transfered = self.ft.transfered + len(data)
			self.ft.client.on_ftTransfered(self.ft.sid, len(data))
		return self.transport.write(data)

# class IBBSend:
# 	implements(interfaces.IConsumer)
# 	
# 	def registerProducer(self, producer, streaming):
# 		return self.factory.transport.registerProducer(producer, streaming)
# 	
# 	def unregisterProducer(self):
# 		self.factory.transport.unregisterProducer()
# 	
# 	def write(self, data):
# 		if self.ft:
# 			self.ft.transfered = self.ft.transfered + len(data)
# 		return self.factory.transport.write(data)
	
class Receive(protocol.Protocol):
	def dataReceived(self, data):
		if self.ft.fp != None:
			self.ft.fp.write(data)
			self.ft.transfered = self.ft.transfered + len(data)
			try:
				self.ft.client.on_ftTransfered(self.ft.sid, len(data))
			except:
				pass
		try:
			self.ft.connector.factory.delayed_timeout_call.cancel()
		except:
			pass

class FTSend:
	def __init__(self, client, sid, filename, tojid, file, description= None, frmjid = None):
		self.sid = sid
		self.filename = filename
		self.fp = open(file, 'rb')
		self.size = os.path.getsize(file)
		self.description = description
		self.client = client
		self.tojid = tojid
		self.protocol = None
		self.transfered = 0
		self.streamhost = None
		self.connector = None
		self.error = None	
		self.fs = None	
		self.ibbSeq = 0
		self.frmjid = frmjid


	
	def activate(self):
		log.msg('received activate for '+self.filename)
		iq = IQ(self.client.xmlstream, 'set')
		iq['to'] = self.streamhost
		if self.frmjid != None:
			iq['from'] = self.frmjid
		q = iq.addElement('query', 'http://jabber.org/protocol/bytestreams')
		q['sid'] = self.sid
		q.addElement('activate', content = self.tojid)
		self.client.on_xml(iq.toXml())
		d = iq.send()
		self.client.disp(iq['id'])
		d.addCallback(self._activated).addErrback(self._activateFailed)
	
	def _activateFailed(self, err):
		log.msg('activate failed with: ' + unicode(err))
		self.client.on_ftEnd(self.sid, 'activate error')
		
	def _activated(self, el):
		FileSender().beginFileTransfer(self. fp, self.protocol)#. addCallback(self._finished)
	
	def _finished(self, last):
		log.msg('finished transfer for ' + self.filename)
		log.msg('times: %i - %i - %i - %i'%(self.start, self.medium, self.ftstart, time.time())) 
	
	def finish(self):
		log.msg("konec prenosu")
		if self.fp != None:
			self.fp.close()
		self.client.on_ftEnd(self.sid, self.error)

	def connectFailure(self):
		pass
		

class FTReceive:
	def __init__(self, client,jid, sid, file, methods, frmjid):
		self.client = client
		self.tojid = jid
		self.sid = sid
		self.fileprops = file
		self.methods = methods
		self.fp = None
		self.method = None
		self.file = None #sem to chceme ulozit
		self.streamhosts = []
		self.streamhostsID = None
		self.activeStreamhost = None
		self.size = int(self.fileprops['size'])
		self.transfered = 0
		self.ibbSeq = 0
		self.ibbCache = {}
		self.connector = None
		self.error = None
		self.frmjid = frmjid
	
	def connectStreamHost(self):
		streamhost = self.streamhosts.pop(0)
		self.activeStreamhost = streamhost
		f = protocol.ClientFactory()
		f.protocol = Receive
		addr = sha.new("%s%s%s" % (self.sid,  self.tojid, self.frmjid)).hexdigest()
		factory = ClientFactory(streamhost['host'], int(streamhost['port']),addr, 0,  f, xmpp = self.client, xmpp_sid = self.sid) 
		self.connector = self.client.reactor.connectTCP(streamhost['host'], int(streamhost['port']), factory)
	
	def connectFailure(self):
		log.msg('connect failed')
		if len(self.streamhosts)>0:
			self.connectStreamHost()
		else:
			log.msg('nemuzu se spojit')
	
	def activate(self):
		print 'activate!'
		iq = Element((None,'iq'))
		iq['to'] = self.tojid
		iq['from'] = self.frmjid
		iq['id'] = self.streamhostsID
		iq['type'] = 'result'
		query = iq.addElement('query', 'http://jabber.org/protocol/bytestreams')
		used = query.addElement('streamhost-used')
		used['jid'] = self.activeStreamhost['jid']
		print iq.toXml()
		self.fp = open(self.file, 'w')
		self.client.xmlstream.send(iq)
	
	def ibbProcess(self):
		c = True
		while c:
			if self.ibbCache.has_key(self.ibbSeq):
				print self.ibbSeq
				data = b64decode(self.ibbCache[self.ibbSeq])
				self.transfered = self.transfered + len(data)
				self.client.on_ftTransfered(self.sid, len(data))
				self.fp.write(data)
				self.ibbSeq = self.ibbSeq + 1
			else:
				c = False
			
		
	
	def finish(self):
		log.msg("konec prenosu")
		if self.fp != None:
			self.fp.close()
		self.client.on_ftEnd(self.sid, self.error)
