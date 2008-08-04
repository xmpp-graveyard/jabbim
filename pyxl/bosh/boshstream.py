from twisted.web2.client.http import HTTPClientProtocol, ClientRequest
from twisted.web2.client.interfaces import IHTTPClientManager
from twisted.internet import reactor, protocol, defer
from twisted.words.xish import domish, utility, xmlstream
from twisted.web2 import http_headers

from zope.interface import implements
import urlparse
import random
from hashlib import sha1
import time
#from twisted.web.client import getPage

# -*- test-case-name: twisted.web.test.test_webclient -*-
# Copyright (c) 2001-2008 Twisted Matrix Laboratories.
# See LICENSE for details.

"""
HTTP client.
"""

import os, types
from urlparse import urlunparse

from twisted.web import http
from twisted.internet import defer, protocol, reactor
from twisted.python import failure
from twisted.python.util import InsensitiveDict
from twisted.web import error


class PartialDownloadError(error.Error):
    """Page was only partially downloaded, we got disconnected in middle.

    The bit that was downloaded is in the response attribute.
    """


class HTTPPageGetter(http.HTTPClient):

	quietLoss = 0
	followRedirect = 1
	failed = 0

	def connectionMade(self):
		pass
		
	def getPage(self):
		method = getattr(self.factory, 'method', 'GET')
		self.sendCommand(method, self.factory.path)
		self.sendHeader('Host', self.factory.headers.get("host", self.factory.host))
		self.sendHeader('User-Agent', self.factory.agent)
		if self.factory.cookies:
			l=[]
			for cookie, cookval in self.factory.cookies.items():
				l.append('%s=%s' % (cookie, cookval))
			self.sendHeader('Cookie', '; '.join(l))
		data = getattr(self.factory, 'postdata', None)
		if data is not None:
			self.sendHeader("Content-Length", str(len(data)))
		for (key, value) in self.factory.headers.items():
			if key.lower() != "content-length":
				# we calculated it on our own
				self.sendHeader(key, value)
		self.endHeaders()
		self.headers = {}

		if data is not None:
			self.transport.write(data)

	def handleHeader(self, key, value):
		key = key.lower()
		l = self.headers[key] = self.headers.get(key, [])
		l.append(value)

	def handleStatus(self, version, status, message):
		self.version, self.status, self.message = version, status, message
		self.factory.gotStatus(version, status, message)

	def handleEndHeaders(self):
		self.factory.gotHeaders(self.headers)
		m = getattr(self, 'handleStatus_'+self.status, self.handleStatusDefault)
		m()

	def handleStatus_200(self):
		pass

	handleStatus_201 = lambda self: self.handleStatus_200()
	handleStatus_202 = lambda self: self.handleStatus_200()

	def handleStatusDefault(self):
		self.failed = 1

	def handleStatus_301(self):
		l = self.headers.get('location')
		if not l:
			self.handleStatusDefault()
			return
		url = l[0]
		if self.followRedirect:
			scheme, host, port, path = \
				_parse(url, defaultPort=self.transport.getPeer().port)
			self.factory.setURL(url)

			if self.factory.scheme == 'https':
				from twisted.internet import ssl
				contextFactory = ssl.ClientContextFactory()
				reactor.connectSSL(self.factory.host, self.factory.port,
								   self.factory, contextFactory)
			else:
				reactor.connectTCP(self.factory.host, self.factory.port,
								   self.factory)
		else:
			self.handleStatusDefault()
			self.factory.noPage(
				failure.Failure(
					error.PageRedirect(
						self.status, self.message, location = url)))
		self.quietLoss = 1
		self.transport.loseConnection()

	handleStatus_302 = lambda self: self.handleStatus_301()

	def handleStatus_303(self):
		self.factory.method = 'GET'
		self.handleStatus_301()

	def connectionLost(self, reason):
		if not self.quietLoss:
			http.HTTPClient.connectionLost(self, reason)
			self.factory.noPage(reason)

	def handleResponse(self, response):
		if self.quietLoss:
			return
		if self.failed:
			self.factory.noPage(
				failure.Failure(
					error.Error(
						self.status, self.message, response)))
		if self.factory.method.upper() == 'HEAD':
			# Callback with empty string, since there is never a response
			# body for HEAD requests.
			self.factory.page('')
		elif self.length != None and self.length != 0:
			self.factory.noPage(failure.Failure(
				PartialDownloadError(self.status, self.message, response)))
		else:
			self.factory.page(response)
		# server might be stupid and not close connection. admittedly
		# the fact we do only one request per connection is also
		# stupid...
		#self.transport.loseConnection()

	def timeout(self):
		self.quietLoss = True
		self.transport.loseConnection()
		self.factory.noPage(defer.TimeoutError("Getting %s took longer than %s seconds." % (self.factory.url, self.factory.timeout)))

class HTTPClientFactory(protocol.ClientFactory):
	"""Download a given URL.

	@type deferred: Deferred
	@ivar deferred: A Deferred that will fire when the content has
		  been retrieved. Once this is fired, the ivars `status', `version',
		  and `message' will be set.

	@type status: str
	@ivar status: The status of the response.

	@type version: str
	@ivar version: The version of the response.

	@type message: str
	@ivar message: The text message returned with the status.

	@type response_headers: dict
	@ivar response_headers: The headers that were specified in the
		  response from the server.
	"""

	protocol = HTTPClientProtocol

	url = None
	scheme = None
	host = ''
	port = None
	path = None

	def __init__(self, url="", method='GET', postdata=None, headers=None,
				 agent="Twisted PageGetter", timeout=0, cookies=None,
				 followRedirect=1):
		self.timeout = timeout
		self.agent = agent

		if cookies is None:
			cookies = {}
		self.cookies = cookies
		if headers is not None:
			self.headers = InsensitiveDict(headers)
		else:
			self.headers = InsensitiveDict()
		if postdata is not None:
			self.headers.setdefault('Content-Length', len(postdata))
			# just in case a broken http/1.1 decides to keep connection alive
			self.headers.setdefault("connection", "Keep-Alive")
		self.postdata = postdata
		self.method = method

		self.setURL(url)

		self.waiting = 1
		self.deferred = defer.Deferred()
		self.response_headers = None

	def getPage(self,url,postdata=None,headers=None,method=None):
		if headers is not None:
			self.headers = InsensitiveDict(headers)
		else:
			self.headers = InsensitiveDict()
		if postdata is not None:
			self.headers.setdefault('Content-Length', len(postdata))
			# just in case a broken http/1.1 decides to keep connection alive
			self.headers.setdefault("connection", "Keep-Alive")
		self.postdata = postdata
		self.method = method

		self.setURL(url)
		self.waiting = 1
		self.deferred = defer.Deferred()
		self.response_headers = None
		#self.p.getPage()
		return self


	def __repr__(self):
		return "<%s: %s>" % (self.__class__.__name__, self.url)

	def setURL(self, url):
		self.url = url
		scheme, host, port, path = _parse(url)
		if scheme and host:
			self.scheme = scheme
			self.host = host
			self.port = port
		self.path = path

	def buildProtocol(self, addr):
		p = protocol.ClientFactory.buildProtocol(self, addr)
		if self.timeout:
			timeoutCall = reactor.callLater(self.timeout, p.timeout)
			self.deferred.addBoth(self._cancelTimeout, timeoutCall)
		self.p=p
		return p

	def _cancelTimeout(self, result, timeoutCall):
		if timeoutCall.active():
			timeoutCall.cancel()
		return result

	def gotHeaders(self, headers):
		self.response_headers = headers
		if headers.has_key('set-cookie'):
			for cookie in headers['set-cookie']:
				cookparts = cookie.split(';')
				cook = cookparts[0]
				cook.lstrip()
				k, v = cook.split('=', 1)
				self.cookies[k.lstrip()] = v.lstrip()

	def gotStatus(self, version, status, message):
		self.version, self.status, self.message = version, status, message

	def page(self, page):
		if self.waiting:
			self.waiting = 0
			self.deferred.callback(page)

	def noPage(self, reason):
		if self.waiting:
			self.waiting = 0
			self.deferred.errback(reason)

	def clientConnectionFailed(self, _, reason):
		if self.waiting:
			self.waiting = 0
			self.deferred.errback(reason)


def _parse(url, defaultPort=None):
    """
    Split the given URL into the scheme, host, port, and path.

    @type url: C{str}
    @param url: An URL to parse.

    @type defaultPort: C{int} or C{None}
    @param defaultPort: An alternate value to use as the port if the URL does
    not include one.

    @return: A four-tuple of the scheme, host, port, and path of the URL.  All
    of these are C{str} instances except for port, which is an C{int}.
    """
    url = url.strip()
    parsed = http.urlparse(url)
    scheme = parsed[0]
    path = urlunparse(('','')+parsed[2:])
    if defaultPort is None:
        if scheme == 'https':
            defaultPort = 443
        else:
            defaultPort = 80
    host, port = parsed[1], defaultPort
    if ':' in host:
        host, port = host.split(':')
        port = int(port)
    if path == "":
        path = "/"
    return scheme, host, port, path


def getPage(url, contextFactory=None, *args, **kwargs):
    """Download a web page as a string.

    Download a page. Return a deferred, which will callback with a
    page (as a string) or errback with a description of the error.

    See HTTPClientFactory to see what extra args can be passed.
    """
    scheme, host, port, path = _parse(url)
    factory = HTTPClientFactory(url, *args, **kwargs)
    if scheme == 'https':
        from twisted.internet import ssl
        if contextFactory is None:
            contextFactory = ssl.ClientContextFactory()
        reactor.connectSSL(host, port, factory, contextFactory)
    else:
        reactor.connectTCP(host, port, factory)
    return factory.deferred



STREAM_CONNECTED_EVENT = intern("//event/stream/connected")
STREAM_START_EVENT = intern("//event/stream/start")
STREAM_END_EVENT = intern("//event/stream/end")
STREAM_ERROR_EVENT = intern("//event/stream/error")

FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])

def dump(src, length=8):
    N=0; result=''
    while src:
       s,src = src[:length],src[length:]
       hexa = ' '.join(["%02X"%ord(x) for x in s])
       s = s.translate(FILTER)
       result += "%04X   %-*s   %s\n" % (N, length*3, hexa, s)
       N+=length
    return result


class BOSHParser:
    """
    Wrapping an element stream for parsing <body/> documents
    """

    def parse(self, buf):
        self._reset()
        self.stream.parse(buf)
        return self.body, self.xmpp_elements
    
    def onDocumentStart(self, rootelem):
        if rootelem.name == 'body':
            self.body = rootelem

    def onElement(self, element):
        if isinstance(element, domish.Element):
            self.xmpp_elements.append(element)
        else:
            pass

    def _reset(self):
        self.stream = domish.elementStream()
        self.stream.DocumentStartEvent = self.onDocumentStart
        self.stream.ElementEvent = self.onElement
        self.stream.DocumentEndEvent = self.onDocumentEnd
        self.body = ""
        self.xmpp_elements = []

    def onDocumentEnd(self):
        pass


class BOSHStream(utility.EventDispatcher):
	"""
	Transport implementing a bidirectional stream over an HTTP channel
	as in XEP-0124 (http://www.xmpp.org/extensions/xep-0124.html)
	"""

	implements(IHTTPClientManager)

	MAX_RECONNECT_INTERVAL = 10

	def __init__(self):
		utility.EventDispatcher.__init__(self)
		self.parser = BOSHParser()
		self.rawDataOutFn = None
		self.rawDataInFn = None
		self.sid = None
		self.rid = random.randint(0, 1000000)
		self.send_queue = [] # objects awaiting for being sent
		self.out_queue = [] # objects awaiting for ack
		self.resend_queue = [] # bodies that must be resent
		self.initialized = False
		self.reconnect_interval = 0
		self.seed=random.randint(1000, 1000000)
		self.n=random.randint(0, 1000000)
		self.timestamp=time.time()
		self.ready=False
		self.slot=[False,False]


	def _build_first_request(self):
		url = urlparse.urlparse(self.factory.bosh_url)
		try:
			self.host, port = url[1].split(":")
			self.port = int(port)
		except:
			self.host = url[1]
			self.port = 80
		self.path = url[2].encode("utf-8")
		self.bosh_attrs = self.factory.bosh_attrs
		# now queue the first body for initializing the session
		body = domish.Element(("http://jabber.org/protocol/httpbind", "body"))
		body["rid"] = `self.rid`
		#body['newkey'] = str(sha1(str(self.seed)).hexdigest())
		
		self.rid += 1
		for k,v in self.factory.bosh_attrs.items():
			body[k.encode('utf-8')] = v.encode("utf-8")
		body['route']="xmpp:"+body['to']+":5222"
		body['wait']="300"
		self.resend_queue.append(body)
		print 'first request'
		


	def send(self, obj):
		"""
		Send some payload to the server
		@param obj: a valid xml chunk or a L{domish.Element} that must be sent to the server
		"""
		#if domish.IElement.providedBy(obj):
		#    obj = obj.toXml()

		#if self.rawDataOutFn:
		#    self.rawDataOutFn(obj)
		
		self.send_queue.append(obj)
		self._try_to_send()


	def _try_to_send(self,check=False):
		"""
		"""
		# check if there are too many packets out
		if check:
			if time.time()-self.timestamp<2:
				if not self.ready:
					self.ready=True
					reactor.callLater(2,self._try_to_send)
				return
		

		print 'to send'
		if len(self.out_queue) >= 2:
			for b in self.out_queue:
				print [b.toXml().encode("utf-8")]
			return
		print 'to send1'
		if not self.resend_queue and len(self.send_queue) == 0 and len(self.out_queue)!=0:
			return

		print 'to send2'
		self.ready=False
		self.timestamp=time.time()
		if self.resend_queue:
			body = self.resend_queue.pop(0)
		else:
			# ok, we can send a request
			body = domish.Element(("http://jabber.org/protocol/httpbind", "body"))
		
			if self.sid: body["sid"] = self.sid
			body["rid"] = `self.rid`
			self.rid += 1
		
			while self.send_queue:
				obj = self.send_queue.pop(0)
				if domish.IElement.providedBy(obj):
					body.addChild(obj)
				else:
					body.addRawXml(obj)
	
		if self.rawDataOutFn:
			self.rawDataOutFn(body.toXml())
		thead = http_headers.Headers()
		thead.addRawHeader("Content-Type", "text/xml; charset=utf-8")
		thead.addRawHeader("Proxy-Connection","keep-alive")
		thead.addRawHeader("Host", self.host.encode("utf-8"))

		print body.toXml().encode("ascii")
		#print dump(buffer(body.toXml().encode("ascii"),0))
		
		req = ClientRequest(
			"POST", 
			"/", 
			thead,
			unicode(body.toXml()).encode("utf-8")
		)
#		for i in range(2):
#			if not self.slot[i]:
#				if i==0:
		self.slot[0]=True
		self.proto.submitRequest(req, False).addCallback(self.got_response,int(0)).addErrback(self.got_error)
		self.out_queue.append(body)
		print 'send submitRequest'
#				else:
#					self.slot[1]=True
#					url = 'http://bind.jabbim.cz:80'
#					self.secondFactory.p.submitRequest(req, False).addCallback(self.got_response,int(i)).addErrback(self.got_error)
#					self.out_queue.append(body)
#					print 'send getPage'
#				break


	def got_data2(self, data,x): 
		self.slot[x]=False
		try:
			if self.rawDataInFn: self.rawDataInFn(data)
			body, xmpp_elements = self.parser.parse(data)
			if not self.initialized:
				self.session_created(body)
			for el in xmpp_elements:
				if domish.IElement.providedBy(el):
					self.dispatch(el)    
			# this is an ack for the outgoing packets
			self.out_queue.pop(0)
			if len(self.out_queue)==0:
				self._try_to_send(False)
		except domish.ParserError:
			# i'm unsure about this because if we receive only part
			# of the message we send it (but in this case I'm not sure that
			#got_data is called)
			print "dispatch error"
			self.dispatch(self, STREAM_ERROR_EVENT)
			self.transport.loseConnection()
					
	def got_response(self, resp,x):
		self.slot[x]=False
		# this is an ack for the outgoing packets
		self.out_queue.pop(0)
		if len(self.out_queue)==0 and not self.initiating:
			body = domish.Element(("http://jabber.org/protocol/httpbind", "body"))
	
			if self.sid: body["sid"] = self.sid
			body["rid"] = `self.rid`
			self.rid += 1
			thead = http_headers.Headers()
			thead.addRawHeader("Content-Type", "text/xml; charset=utf-8")
			thead.addRawHeader("Proxy-Connection","keep-alive")
			
			thead.addRawHeader("Host", self.host.encode("utf-8"))

			print body.toXml().encode("ascii")
			#print dump(buffer(body.toXml().encode("ascii"),0))
			
			req = ClientRequest(
				"POST", 
				"/", 
				thead,
				unicode(body.toXml()).encode("utf-8")
			)
			#for i in range(2):
			#	if not self.slot[i]:
			#		if i==0:
			#			self.slot[0]=True
			self.proto.submitRequest(req, False).addCallback(self.got_response,int(0)).addErrback(self.got_error)
			self.out_queue.append(body)
			print 'send submitRequest'
			#		else:
			#			self.slot[1]=True
			#			url = 'http://bind.jabbim.cz:80'
			#			self.secondFactory.p.submitRequest(req, False).addCallback(self.got_response,int(i)).addErrback(self.got_error)
			#			self.out_queue.append(body)
			#			print 'send getPage'
			#		break
		print 'read the body'
		temp=resp.stream.read()
		if temp:
			temp.addCallback(self.got_data,resp).addErrback(self.got_error)
		else:
			print "None readed?!"
			print self.out_queue.pop(0)
		return

	def got_data(self, d, resp,data=""): 
		if d:
			data+=d
		temp=resp.stream.read()
		if temp:
			temp.addCallback(self.got_data,resp,data)
			return
		print [data]
		try:

			if self.rawDataInFn: self.rawDataInFn(data)
			body, xmpp_elements = self.parser.parse(data)
			if not self.initialized:
				self.session_created(body)
			for el in xmpp_elements:
				if domish.IElement.providedBy(el):
					self.dispatch(el)
		except domish.ParserError:
			# i'm unsure about this because if we receive only part
			# of the message we send it (but in this case I'm not sure that
			#got_data is called)
			print "dispatch error"
			self.dispatch(self, STREAM_ERROR_EVENT)
			self.transport.loseConnection()

	def got_error(self, fault):
		print "FUCK",fault,unicode(fault),dir(fault)
		self.dispatch(self, STREAM_ERROR_EVENT)
		self.transport.loseConnection()

	def session_created(self, body):
		print "session created"
		print type(body)
		if body.hasAttribute("sid"):
			self.sid = body["sid"]
			self.dispatch(self, STREAM_START_EVENT)
			self.initialized = True
		else:
			self.dispatch(self, STREAM_ERROR_EVENT)

	def clientBusy(self, proto):
		pass

	def clientIdle(self, proto):
		reactor.callLater(0, self._try_to_send)

	def clientPipelining(self, proto):
		print "PIPELINE",proto
		reactor.callLater(0, self._try_to_send)

	def clientGone(self, proto):
		""" try to reconnect """
		reactor.callLater(0, self.connect)

	def connect(self):

		d = protocol.ClientCreator(
			reactor, HTTPClientProtocol, manager = self
		).connectTCP(self.host, self.port)
		d.addCallback(self.connect_done)
		d.addErrback(self.connect_failed)
		print 'connect!'

	def connect_done(self, proto):
		self.secondFactory = HTTPClientFactory()
		#reactor.connectTCP("bind.jabbim.cz", 80, self.secondFactory)
		print "secondFactory",self.secondFactory
		print "PROTO",proto,type(proto)
		if not self.initialized:
			self._build_first_request()
		self.proto = proto
		if not self.initialized:
			self.dispatch(self, STREAM_CONNECTED_EVENT)
			# XXX I don't like this: we should find some more elegant way
			#if hasattr(self, "connectionMade"):
			#    self.connectionMade()
		self.reconnect_interval = 0
		reactor.callLater(0, self._try_to_send)

	def connect_failed(self, fault):
		reactor.callLater(self.reconnect_interval, self.connect)
		if self.reconnect_interval < self.MAX_RECONNECT_INTERVAL:
			self.reconnect_interval += 1

	def restart(self):
		body = domish.Element(("http://jabber.org/protocol/httpbind", "body"))
		
		body["xmlns:xmpp"] = "urn:xmpp:xbosh"
		body["xmpp:restart"] = "true"
		body["sid"] = self.sid
		body["rid"] = `self.rid`
		self.rid += 1
		self.resend_queue.append(body)
		self._try_to_send()
 
class XmlStreamFactoryMixin(object):  
	""" 
	XmlStream factory mixin that takes care of event handlers.  
	 
	To make sure certain event observers are set up before incoming data is  
	processed, you can set up bootstrap event observers using C{addBootstrap}.  
	 
	The C{event} and C{fn} parameters correspond with the C{event} and  
	C{observerfn} arguments to L{utility.EventDispatcher.addObserver}.  
	""" 
# 	protocol = BOSHStream
 
	def __init__(self, *args, **kwargs):  
		self.bootstraps = []  
		self.args = args  
		self.kwargs = kwargs  
 
	def buildProtocol(self, addr):  
		""" 
		Create an instance of XmlStream.  
		 
		The returned instance will have bootstrap event observers registered  
		and will proceed to handle input on an incoming connection.  
		""" 
		xs = self.protocol(*self.args, **self.kwargs)  
		xs.factory = self  
		for event, fn in self.bootstraps:  
			xs.addObserver(event, fn)  
		return xs 
	def addBootstrap(self, event, fn):  
		""" 
		Add a bootstrap event handler.  
		""" 
		self.bootstraps.append((event, fn))  
 
	def removeBootstrap(self, event, fn):  
		""" 
		Remove a bootstrap event handler.  
		""" 
		self.bootstraps.remove((event, fn))
		
class BOSHTTPClient(HTTPClientProtocol):
    
    def connectionMade(self):
        self.manager.connect_done(self)


class BOSHStreamFactory(XmlStreamFactoryMixin, protocol.ClientFactory):

    def buildProtocol(self, addr):
        xs = XmlStreamFactoryMixin.buildProtocol(self, addr)
        bosh_client = BOSHTTPClient(manager = xs)
        bosh_client.factory = self
        return bosh_client

