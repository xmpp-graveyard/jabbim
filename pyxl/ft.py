import sys,  re,  time,  random
from calendar import timegm
from twisted.python import log
import jid
from twisted.words.xish import domish
from twisted.words.xish.domish import Element
try:
	from hashlib import sha1
except:
	log.msg('Please upgrade to python2.5')
	from sha import new as sha1
from base64 import b64encode, b64decode
from twisted.protocols import socks
from twisted.words.protocols.jabber.xmlstream import IQ, TimeoutError
from twisted.internet.protocol import Protocol, ClientFactory, Factory
from socket import getaddrinfo
import socks5, events, base64
from twisted.internet import threads, defer, reactor

class FTInit:
	def __init__(self,  client):
		self.client = client
		self.dispatcher = self.client.dispatcher
		self.groupchats = self.client.groupchats
		self.ft = self.client.ft
		self.socks5Srv = None
		self.socks5IP = self.client.socks5IP
		self.socks5Port = self.client.socks5Port
		self.main = self.client.main
		self.ft_proxies = self.client.ft_proxies
		self.client.sendFile = self.sendFile
		self.client.declineFT = self.declineFT
		self.client.receiveFile = self.receiveFile
		self.disp = self.client.disp
		self.xmlLang = self.client.xmlLang
		self.chyba = self.client.chyba
		self.getIPAddr = self.client.getIPAddr
		self.client.ftStart = self.ftStart
	
	def send(self,  xml):
		self.client.xmlstream.send(xml)
	
	def sendFile(self, outjid, filename, fp, desc = None, preview = None, previewType = 'image/jpeg', typ = None,  sid = None): #typ = None/ibb/socks5
		if sid == None:
			sid = str(random.randint(1000, sys.maxint))
		log.msg('sending file to '+ outjid)
		iq = IQ(self.client.xmlstream, 'set')
		outjd = jid.JID(outjid)
		frmjid = None
		if self.groupchats.has_key(outjd.userhost()):
			if self.groupchats[outjd.userhost()].users[outjd.resource].truejid == None:
				frmjid = outjd.userhost() + '/' + self.groupchats[outjd.userhost()].nick
				iq['from'] = frmjid
				typ = 'ibb'
			else:
				outjid = self.groupchats[outjd.userhost()].users[outjd.resource].truejid
				
		iq['to'] = outjid
		self.ft[sid] = socks5.FTSend(self.client, sid, filename, outjid, fp, desc, frmjid)
		self.ft[sid].start = time.time()
		
		si = iq.addElement('si', 'http://jabber.org/protocol/si')
		si['id'] = sid
		si['profile'] = 'http://jabber.org/protocol/si/profile/file-transfer'
		si['mime-type'] = 'text/plain'
		file = si.addElement('file', 'http://jabber.org/protocol/si/profile/file-transfer')
		file['name'] = filename
		file['size'] = unicode(self.ft[sid].size)
		if preview != None:
			prev = file.addElement('preview', 'http://kopete.kde.org/protocol/file-preview', content = preview)
			prev['type'] = previewType
		if desc != None:
			file.addElement('desc', content = unicode(desc))
		file.addElement('range')
		feature = si.addElement('feature', 'http://jabber.org/protocol/feature-neg')
		x = feature.addElement('x', 'jabber:x:data')
		x['type'] = 'form'
		field = x.addElement('field')
		field['var'] = 'stream-method'
		field['type'] = 'list-single'
		if typ == None:
			field.addRawXml('<option><value>http://jabber.org/protocol/bytestreams</value></option>')
			field.addRawXml('<option><value>http://jabber.org/protocol/ibb</value></option>')
		elif typ == 'ibb':
			field.addRawXml('<option><value>http://jabber.org/protocol/ibb</value></option>')
		elif typ == 'socks5':
			field.addRawXml('<option><value>http://jabber.org/protocol/bytestreams</value></option>')

		self.disp(iq['id'])
		d = iq.send()
		d.addCallback(self._ftreplyReceived, sid).addErrback(self._ftFailed, sid)
		return sid

	
	def _onIPAddr(self, addr):
		if not (unicode(addr),self.socks5Port) in self.socks5IP:
			self.socks5IP.append((unicode(addr),self.socks5Port))
		if self.main.config['FTHost'] != '':
			if self.main.config['FTPort'] != '' :
				if not (self.main.config['FTHost'],self.main.config['FTPort'] ) in self.socks5IP:			
					self.socks5IP.append((self.main.config['FTHost'],self.main.config['FTPort'] ))
			else:
				if not (self.main.config['FTHost'],self.socks5Port ) in self.socks5IP:
					self.socks5IP.append((self.main.config['FTHost'], self.socks5Port))
		print self.socks5IP
		
		try:
			from nattraverso.portmapper import get_port_mapper
		except:
			log.msg('nattraverso not found, UPnP mapping is not available')
			return
		
		return get_port_mapper().addCallbacks(self.got_port_mapper, self.error_occured)

	def got_port_mapper(self, mapper):
		print "\tGot port mapper:", mapper
		print "Retreiving existing mappings"
		return mapper.get_port_mappings().addCallback(self.got_mappings).addErrback(self.error_occured)
	
	def error_occured(self, err):
		print "\tError occured:", err
	
	def got_mappings(self, mappings):
		print '\tExisting mappings:\n\t', mappings
		
	def _checkProxies(self):
		print 'checking list of proxies', self.ft_proxies
		dlist = []
		for proxy, data in self.ft_proxies.iteritems():
			if len(data) != 2:
				dlist.append(self.getProxyInfo(proxy))
		if len(dlist) != 0:
			d = defer.DeferredList(dlist).addCallback(self._updatedProxyInfo)
			return d
		return None
	
	def _updatedProxyInfo(self, results):
		print self.ft_proxies
	
	def getProxyInfo(self, proxy):
		iq = IQ(self.client.xmlstream, 'get')
		iq['xml:lang'] = self.xmlLang
		iq['type'] = 'get'
		iq['to'] = proxy
		q = iq.addElement('query')
		q['xmlns']='http://jabber.org/protocol/bytestreams'
		self.disp(iq['id'])
		d = iq.send()
		d.addCallback(self._onProxyInfo).addErrback(self.chyba)
		return d
	
	def _onProxyInfo(self, el):
		q = el.firstChildElement()
		info = q.firstChildElement()
		self.ft_proxies[el['from']] = [info.getAttribute('host'), info.getAttribute('port')]
	
	def _ftFailed(self, err, sid):
		print err
		self.client.on_ftEnd(sid, 'Canceled')
	
	def _ftstreamhostquery(self, el):
		print 'proxy rika: ', el.toXml()
	
	def _ftreplyReceived(self, el, sid):
		typ = None
		si = el.firstChildElement()
		offset = 0
		for elem in si.elements():
			if elem.name == 'feature':
				typ = unicode(elem.firstChildElement().firstChildElement().firstChildElement())
			elif elem.name == 'file':
				if len(elem.children)==1:
					r = elem.firstChildElement()
					offset = int(r.getAttribute('offset', 0))
					self.ft[sid].fp.seek(offset)
					
		log.msg('FT: ' + typ)
		if typ == 'http://jabber.org/protocol/ibb':
			self.ibbSend(sid)
		elif typ == 'http://jabber.org/protocol/bytestreams':
			if self.socks5Srv == None:
				try:
					factory = socks5.SOCKSv5Factory(self)
					self.socks5Srv = self.client.reactor.listenTCP(int(self.socks5Port), factory)
					self.socks5IP = []
					self.socks5IP.append(('127.0.0.1', '33333'))
	
				except:
					print 'unable to connect to port'
			d = self._checkProxies()
			def _doSend(self, client):
				iq = IQ(client.client.xmlstream, 'set')
				iq['to'] = el['from']
				q = iq.addElement('query', 'http://jabber.org/protocol/bytestreams')
				q['sid'] = sid
				q['mode'] = 'tcp'
					
				addr = sha1("%s%s%s" % (sid, client.client.jid.full(), el['from'])).hexdigest()
				client.socks5Srv.factory.sessions[addr] = sid
				for data in client.socks5IP:
					streamhost = q.addElement('streamhost')
					streamhost['host'] = data[0]
					streamhost['jid'] = client.client.jid.full()
					streamhost['port'] = data[1]
	
				for proxy, data in client.ft_proxies.iteritems():
					streamhost = q.addElement('streamhost')
					streamhost['host'] = data[0]
					streamhost['jid'] = proxy
					streamhost['port'] = data[1]
	

				d = iq.send()
				client.disp(iq['id'])
				d.addCallback(client._ftreplyhostReceived, sid)
				d.addErrback(client._ftreplyhostErrReceived, sid)
			
			if d != None:
				d.addCallback(self.getIPAddr).addCallback(self._onIPAddr).addCallback(_doSend, self)
			else:
				self.getIPAddr().addCallback(self._onIPAddr)
				_doSend(None, self)

	
	def _ftreplyhostReceived(self, el, sid):
		print el.toXml()
		q = el.firstChildElement()
		streamhost = q.firstChildElement()
		host = streamhost['jid']
		self.ft[sid].streamhost = host
		self.ft[sid].medium = time.time()
		addr = sha1("%s%s%s" % (sid, self.client.jid.full(), el['from'])).hexdigest()
		if host != self.client.jid.full():
			try:
				if len(self.socks5Srv.factory.sessions)==0:
					self.socks5Srv.loseConnection()
			except:
				pass
			f = ClientFactory()
			f.protocol = socks5.Send

			factory = socks5.ClientFactory(self.ft_proxies[host][0], int(self.ft_proxies[host][1]),addr, 0,  f, xmpp = self.client, xmpp_sid = sid) 
			self.ft[sid].connector = self.client.reactor.connectTCP(self.ft_proxies[host][0], int(self.ft_proxies[host][1]), factory)
		else:
			print 'tady se to usmazi'
#			print socks5.Send()

			self.ft[sid]._activated()
		

	def _ftreplyhostErrReceived(self, err, sid):
		print 'replyhost', err
		self.client.on_ftEnd(sid, 'replyhost error')
	
	def ftStart(self, sid, protocol):
		log.msg(sid)
		if self.ft.has_key(sid):
			self.ft[sid].ftstart = time.time()
			self.ft[sid].protocol = protocol
			self.ft[sid].activate()
	
	def onFileReceive(self, el):
		print el.toXml()
		self.disp(el['id'])
		file = {}
		methods = []
		si = el.firstChildElement()
		for e in si.elements():
			if e.name == 'file':
				file = e.attributes
				for elm in e.elements():
					if elm.name == 'preview':
						file['preview'] = unicode(elm)
						file['previewType'] = elm.getAttribute('type', 'image/jpeg')
					elif elm.name == 'desc':
						file['desc'] = unicode(elm)
					elif elm.name == 'range':
						file['range'] = True
			elif e.name == 'feature':
				x = e.firstChildElement()
				for field in x.elements():
					if field.getAttribute('var') == 'stream-method':
						for option in field.elements():
							methods.append(unicode(option.firstChildElement()))
		sid = si['id']
		self.ft[sid] = socks5.FTReceive(self.client, el['from'], sid, file, methods, el['to'],el['id'])
		self.client.on_fileReceived(sid, el['id'])
		self.dispatcher.publishEvent('FTStartedEvent', sid, el['id'])
	
	def declineFT(self, sid):
		if not self.ft.has_key(sid):
			return False
		obj = self.ft[sid]
		iq = Element((None, 'iq'))
#		iq['xml:lang'] = self.xmlLang
		iq['to'] = obj.tojid
		iq['id'] = obj.answerId
		iq['type'] = 'error'
		err = iq.addElement('error', content = 'Declined')
		err['code'] = '403'
		self.send(iq)
		return True
	
	def receiveFile(self, sid, id, rang = False):
		iq = Element((None,'iq'))
		obj = self.ft[sid]
		iq['to'] = obj.tojid
		iq['from'] = obj.frmjid
		iq['id'] = id
		iq['type'] = 'result'
		si = iq.addElement('si', 'http://jabber.org/protocol/si')
		f = si.addElement('file', 'http://jabber.org/protocol/si/profile/file-transfer')
		if rang == True:
			size = os.stat(obj.file).st_size
			r = f.addElement('range')
			r['offset'] = size
		feature = si.addElement('feature', 'http://jabber.org/protocol/feature-neg')
		x = feature.addElement('x', 'jabber:x:data')
		x['type'] = 'submit'
		field = x.addElement('field')
		field['var'] = 'stream-method'
		value = field.addElement('value', content = obj.method)
#		self.on_xml(iq.toXml())
		self.send(iq)
	
		
	def onStreamhosts(self, el):
		self.disp(el['id'])
		query = el.firstChildElement()
		sid = query['sid']
		if self.ft.has_key(sid):
			if isinstance(self.ft[sid], socks5.FTReceive):
				for streamhost in query.elements():
					if streamhost.name == 'streamhost':
						self.ft[sid].streamhosts.append(streamhost.attributes)
				self.ft[sid].streamhostsID = el['id']
				self.ft[sid].connectStreamHost()
		print el.toXml()

	def ibbSend(self, sid):
		iq = IQ(self.client.xmlstream, 'set')
		iq['to'] = self.ft[sid].tojid
		if self.ft[sid].frmjid != None:
			iq['from'] = self.ft[sid].frmjid
		opn = iq.addElement('open', 'http://jabber.org/protocol/ibb')
		opn['sid'] = sid
		opn['block-size'] = '4096'
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._ftIBBStart, sid)
		d.addErrback(self._ftIBBError, sid)
	
	def _ftIBBError(self, err, sid):
		print err
		self.ft[sid].error = 'IBB error.'
		self.ft[sid].finish()
	
	def _ftIBBStart(self,el, sid):
		iq = IQ(self.client.xmlstream, 'set')
		iq['to'] = self.ft[sid].tojid
		if self.ft[sid].frmjid != None:
			iq['from'] = self.ft[sid].frmjid
		data = iq.addElement('data', 'http://jabber.org/protocol/ibb')
		data['sid'] = sid
		data['seq'] = unicode(self.ft[sid].ibbSeq)
		dt = ''
		dt = self.ft[sid].fp.read(4096)
		if not dt:
			self.ft[sid].error = 'IBB cannot start.'
			self.ft[sid].finish()
			return
		data.addContent(b64encode(dt))		
#		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		self.ft[sid].ibbSeq = self.ft[sid].ibbSeq +1
		self.ft[sid].transfered = self.ft[sid].transfered + len(dt)
		self.client.on_ftTransfered(sid, len(dt))
		d.addCallback(self._ftIBBContinue, sid)
		d.addErrback(self._ftIBBError, sid)
		
	def _ftIBBContinue(self,el, sid):
		iq = IQ(self.client.xmlstream, 'set')
		iq['to'] = self.ft[sid].tojid
		if self.ft[sid].frmjid != None:
			iq['from'] = self.ft[sid].frmjid
		data = iq.addElement('data', 'http://jabber.org/protocol/ibb')
		data['sid'] = sid
		data['seq'] = unicode(self.ft[sid].ibbSeq)
		dt = ''
		dt = self.ft[sid].fp.read(4096)
		if not dt:
			print 'konec!', data['seq']
			iq = IQ(self.client.xmlstream, 'set')
			iq['to'] = self.ft[sid].tojid
			if self.ft[sid].frmjid != None:
				iq['from'] = self.ft[sid].frmjid
			opn = iq.addElement('close', 'http://jabber.org/protocol/ibb')
			opn['sid'] = sid
#			self.on_xml(iq.toXml())
			d = iq.send()
			self.disp(iq['id'])

			self.ft[sid].finish()
			return
		data.addContent(b64encode(dt))		
#		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		self.ft[sid].ibbSeq = self.ft[sid].ibbSeq +1
		self.ft[sid].transfered = self.ft[sid].transfered + len(dt)
		self.client.on_ftTransfered(sid, len(dt))
		d.addCallback(self._ftIBBContinue, sid)
		d.addErrback(self._ftIBBError, sid)
		
	def receiveFileIBB(self, sid, id):
		iq = Element((None,'iq'))
		obj = self.ft[sid]
		iq['to'] = obj.tojid
		if self.ft[sid].frmjid != None:
			iq['from'] = self.ft[sid].frmjid
		iq['id'] = id
		iq['type'] = 'result'
		self.send(iq)
	
	def onIBBStart(self, el):
		log.msg('IBB start')
		self.disp(el['id'])
		opn = el.firstChildElement()
		sid = opn['sid']
		iq = Element((None,'iq'))
		iq['to'] = el['from']
		if self.ft[sid].frmjid != None:
			iq['from'] = self.ft[sid].frmjid
		iq['id'] = el['id']
		iq['type'] = 'result'
		self.send(iq)
		
	def onIBBData(self, el):
		log.msg('on data')
		for e in el.elements():
			if e.name == 'data':
				sid = e['sid']
				seq = int(e['seq'])
				self.ft[sid].ibbCache[seq] = unicode(e)
				self.ft[sid].ibbProcess()
		if el.name == 'iq':
			self.disp(el['id'])
			iq = Element((None,'iq'))
			iq['to'] = el['from']
			if self.ft[sid].frmjid != None:
				iq['from'] = self.ft[sid].frmjid
			iq['id'] = el['id']
			iq['type'] = 'result'
			self.send(iq)

	
	def onIBBEnd(self, iq):
		self.disp(iq['id'])
		close = iq.firstChildElement()
		log.msg('IBB end')
		sid = close['sid']
		self.ft[sid].ibbProcess()
		self.ft[sid].finish()
