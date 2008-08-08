import sys, time, random
import socks5, events
from twisted import names
from twisted.python import log
from twisted.internet import protocol, error
from twisted.names import client as dns

from twisted.words.protocols import jabber
from twisted.words.protocols.jabber import client,jid
from twisted.words.xish import domish
from twisted.words.xish.domish import Element
from twisted.internet import reactor
from twisted.words.protocols.jabber.xmlstream import IQ
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.words.protocols.jabber.client import *

def basicClientFactory(jid, secret):
    a = RegisteringAuthenticator(jid, secret)
    return xmlstream.XmlStreamFactory(a)

class RegisteringAuthenticator(BasicAuthenticator):
	def _registerResultEvent(self, iq):
		print dir(self)
		if iq["type"] == "result":
			# Registration succeeded -- go ahead and auth
			self.streamStarted(self.rootElement)
		else:
			# Registration failed
			if iq.error['code'] == '500':
				reactor.callLater(5,  self.registerAccount,  self.jid.user,  self.password)
				print 'wait error, trying in 5 seconds'
			self.xmlstream.dispatch(iq, self.REGISTER_FAILED_EVENT)
	
	def streamStarted(self, rootElement):
		BasicAuthenticator.streamStarted(self, rootElement)
		self.rootElement = rootElement


class RegisteringClient:
	def __init__(self, username, server, resource,password, port, reactor):
		self.jid = jid.JID('%s@%s/%s'%(username, server, resource))
		self.password  = password
		self.host = self.jid.host
		self.port = port
		self.factory = None
		self.connection = None
		self.reactor = reactor
		self.tryNum=0
		pass
	
	def connect(self):
		log.msg('dns - ' + unicode(time.time()) + '_xmpp-client._tcp.'+self.jid.host)
		d = dns.lookupService('_xmpp-client._tcp.'+self.jid.host, timeout = [2,10])
		d.addCallback(self._dnsLookup)
		d.addErrback(self._dnsLookupErr)
	
	def _dnsLookup(self, resp):
		r = random.choice(resp[0])
		self._connect(unicode(r.payload.target), int(r.payload.port))
	
	def _dnsLookupErr(self, resp):
#		print 'err:', resp
		self._connect(self.host, self.port)



	def _connect(self, host, port): 
		self.factory = basicClientFactory(self.jid,self.password)
#		self.factory.authenticator = RegisteringAuthenticator(self.jid,  self.password)
		self.factory.addBootstrap('//event/stream/start',self._streamstart)
		self.factory.addBootstrap('//event/stream/authd',self._authd)
#		self.factory.addBootstrap("//event/client/basicauth/invaliduser", self._invaliduser)
		self.factory.addBootstrap("//event/client/basicauth/authfailed", self._authfailed)
		self.factory.addBootstrap("//event/xmpp/initfailed", self._authfailed)
		self.factory.addBootstrap("//event/client/basicauth/registerfailed", self._regfailed)
		self.factory.addBootstrap('/iq[@type="result"]/bind', self._bind)
#		print dir(self.factory.protocol)


		self.factory.clientConnectionLost = self.connectionLost
		self.factory.clientConnectionFailed = self.connectionFailed
		self.connection = self.reactor.connectTCP(host,port,self.factory)
		log.msg('started - ' + unicode(time.time()))
	
	def _streamstart(self, xml):
		self.xmlstream = xml
		self.xmlstream.rawDataInFn = self.xml
		self.xmlstream.rawDataOutFn = self.xml
	
	def xml(self, buf):
		log.msg(u'XML: ' + unicode(buf, 'utf8', 'replace'))
	
	def connectionLost(self, connector, reason=protocol.connectionDone):
		log.msg('connection lost!')
		self.tryNum+=1
		if self.tryNum<2:
			self.connect()
		

	
	def connectionFailed(self, connector, reason=protocol.connectionDone):
		log.msg('connection failed!')


	def _streamEnd(self, el):
		pass
		
	def _bind(self, el):
		#experimental
		log.msg('bind')
		bind = el.firstChildElement()
		jd = bind.firstChildElement().__str__()
		self.jid = jid.JID(jd)
		
	def disconnect(self):
		self.connection.disconnect()
		self.factory.stopTrying()
		self.connection = None
		self.factory = None
	
	def _regfailed(self, el):
		log.msg('reg failed')
		print el.toXml()
	
	#def _authd(self, el):

		log.msg('we are lucky, indeed')

	def _authfailed(self, el):
		log.msg('auth failed')
#		print el.toXml()
		print dir(self)
		self.factory.authenticator.registerAccount(self.jid.user, self.password)
		print 'trying to register'
	
	def _invaliduser(self, el):
		log.msg('invalid user')
		self.factory.authenticator.registerAccount(self.jid.user, self.password)
		print 'trying to register'
		print el.toXml()
