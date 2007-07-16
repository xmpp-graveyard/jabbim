import sys, time, random, sha

import socks5
from twisted.python import log
from twisted.internet import protocol
from twisted.names import client as dns

from twisted.words.protocols import jabber
from twisted.words.protocols.jabber import client,jid
from twisted.words.xish import domish
from twisted.words.xish.domish import Element
from twisted.internet import reactor
from twisted.words.protocols.jabber.xmlstream import IQ
from twisted.internet.protocol import Protocol, ClientFactory

from derived import derived
from contact import *
from groupchat import  *
##from storage import *
##class Log:
##	def msg(self, zprava):
##		pass
##	def err(self, zprava):
##		pass
##log = Log()

class Bookmark:
	def __init__(self, name, typ, JID = None, autojoin = False, nick = None, password = None, url = None):
		self.name = name
		self.typ = typ #url/conference
		self.jid = jid.JID(JID)
		self.autojoin = autojoin
		self.nick = nick
		self.password = password
		self.url = url

class Client(derived):
	def __init__(self, JID, password, host, port, main, SSL = True):
		#derived.__init__(self)
		self.jid = jid.JID(JID)
		self.password  = password
		self.host = self.jid.host
		self.port = port
		self.factory = None
		self.connection = None
		self.main=main # mainWindow
		self.ssl = SSL
		self.roster = {'users':{},'groups':{}}
		self.roster_meta = {} # jid: {'tag':tag,  'order': 1}
		self.first_presence = []
		self.first_wait = True
		self.bookmarks = {'conference':{}, 'url': {}}
		self.idlist = []
		self.disco = {} # jid:{node1:{items:{attrs}, identity: {attrs}, features:[], err: {'info':'', 'items':''}}}
		self.groupchats = {} # jid:Groupchat
		self.privacy_lists = {}
		self.privacy_active = None
		self.privacy_default = None
		self.client_name = 'Jabbim'
		self.version = '0.0.1' # tohle asi neni nejlepsi zpusob
		self.client_os = ''
		self.caps_node = 'http://dev.jabbim.cz/jabbim/caps'
		self.caps_version = self.version
		self.caps_ext = None
		self.discofeatures = {} # node: [feature1, feature2]
		self.ft_proxies = {
		'proxy.netlab.cz':["77.48.19.1", "7777"] ,
		'proxy.jabber.org':['208.245.212.98', '7777'],
		'serafim.cd.chalmers.se' : ['serafim.cd.chalmers.se', '7777']
		}
		
		self.last = 0
		self.registerFeature('jabber:iq:version')
		self.registerFeature('jabber:iq:last')
		self.registerFeature('http://jabber.org/protocol/xhtml-im')
		self.registerFeature('http://jabber.org/protocol/disco#info')
		self.registerFeature('urn:xmpp:time')
		self.registerFeature('jabber:iq:time')
		self.registerFeature('http://jabber.org/protocol/chatstates')
		self.caps_cache = {} # 'node': [feature1, feature2]
		self.cacheCaps('%s#%s'%(self.caps_node, self.caps_version), self.discofeatures[None])
		self.log = True
		self.on_init()

	def cacheCaps(self, node, features):
		self.caps_cache[node] = features

	def sendPresence(self, to = None, show = None, status = None, priority = None, typ = None, caps = True):
		presence = Element((None, 'presence'))
		presence['from'] = self.jid.full()
		if to:
			presence['to'] = to
		if status:
			presence.addElement('status', content = status)
		if show:
			presence.addElement('show', content = show)
		if priority:
			presence.addElement('priority', content = priority)
		if typ:
			presence['type'] = typ
		if caps:
			c = presence.addElement('c', 'http://jabber.org/protocol/caps')
			c['node'] = self.caps_node
			c['ver'] = self.caps_version
			if self.caps_ext != None:
				c['ext'] = self.caps_ext

		log.msg('sending out presence to: ' + to)
		self.on_xml(presence.toXml())
		self.xmlstream.send(presence)

	def sendMessage(self, to, body, typ='chat', subject = None, composing = None, xhtml = None,  muc = False):
		message = Element((None,'message'))
		message['to'] = to
		message.addElement('body', content = body)
		message['type'] = typ
		JID = jid.JID(to)
		if typ == 'normal' and subject:
			message.addElement('subject', content = subject)
		if xhtml != None:
			html = message.addElement('html','http://jabber.org/protocol/xhtml-im')
			body = html.addElement('body', 'http://www.w3.org/1999/xhtml')
			body.addRawXml(xhtml)
		if composing:
			if self.roster['users'].has_key(JID.userhost()):
				if self.roster['users'].resources.has_key(JID.resouce):
					if self.roster['users'].resources[JID.resource].hasFeature('http://jabber.org/protocol/chatstates'):
						message.addElement(composing, 'http://jabber.org/protocol/chatstates' )
				else:
					if self.roster['users'].resources[self.roster['users'].getHighestResource()].hasFeature('http://jabber.org/protocol/chatstates'):
						message.addElement(composing, 'http://jabber.org/protocol/chatstates' )

		self.on_xml(message.toXml())
		self.xmlstream.send(message)

	def connect(self):
		d = dns.lookupService('_xmpp-client._tcp.'+self.jid.host)
		d.addCallback(self._dnsLookup)
		d.addErrback(self._dnsLookupErr)
	
	def _dnsLookup(self, resp):
		r = random.choice(resp[0])
		self._connect(unicode(r.payload.target), int(r.payload.port))
	
	def _dnsLookupErr(self, resp):
		self._connect(self.host, self.port)
	
	def _connect(self, host, port): 

		self.factory = client.XMPPClientFactory(self.jid,self.password)
		self.factory.addBootstrap('//event/stream/authd',self._authd)
##		self.factory.addBootstrap("//event/client/basicauth/invaliduser", self._invaliduser)
##		self.factory.addBootstrap("//event/client/basicauth/authfailed", self._authfailed)
##		self.factory.addBootstrap("//event/stream/error", self._authfailed)
		self.factory.addBootstrap('/iq[@type="result"]/bind', self._bind)
##		self.factory.addBootstrap("/*", self.logIt)
		self.connection=reactor.connectTCP(host,port,self.factory)

	def _bind(self, el):
		#experimental
		bind = el.firstChildElement()
		jd = bind.firstChildElement().__str__()
		self.jid = jid.JID(jd)
		
	def disconnect(self):
		self.connection.disconnect()
		self.factory.stopTrying()
		self.connection = None
		self.factory = None

	def _authd(self, xmlstream):
		self.main._connected()
		self.xmlstream = xmlstream
		self.xmlstream.addObserver("/presence", self.onPresence, 1)
		self.xmlstream.addObserver("/message", self.onMessage, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/query[@xmlns='jabber:iq:roster']", self.onRosterAdd, 1)
		self.xmlstream.addObserver("/*", self.onXML)
		self.xmlstream.addObserver("/presence[@type='subscribe']", self.onSubscribe, 1)
		self.xmlstream.addObserver("/presence[@type='unsubscribe']", self.onUnSubscribe, 1)
		self.xmlstream.addObserver("/presence[@type='subscribed']", self.onSubscribed, 1)
		self.xmlstream.addObserver("/presence[@type='unsubscribed']", self.onUnSubscribed, 1)
		self.xmlstream.addObserver("/presence[@type='error`']", self.onPresenceError, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='jabber:iq:version']", self.onVersion, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='http://jabber.org/protocol/disco#info']", self.onDiscoInfo, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='jabber:iq:last']", self.onLast, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/time[@xmlns='urn:xmpp:time']", self.onTime202, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='jabber:iq:time']", self.onTime90, 1)
		self.getMetacontacts()
		self.getBookmarks()
		self.getDiscoInfo(self.jid.host,  callback = self._pepSupport)
		self.getDiscoItems(self.jid.host)
		#self.getVCard('sef@njs.netlab.cz')
#		self.sendPEPTune()
#		self.registerPEP('sefator@jabber.se')
#		self.getPrivacy()
#		self.joinGC('jdev@conf.netlab.cz',  'Sefator')
##		self.sendFile('public@disk.jabbim.cz', 'test.txt', '10010', None)
		self.on_authd()
	def _pepSupport(self):
		log.msg('pep support arrived')
#		print self.jid.host,  self.disco
#		print self.disco[self.jid.host][None]
		for key,  val in self.disco[self.jid.host][None]['identities'].iteritems():
			log.msg(key+ unicode(val))
			if val['type'] == 'pep' :
				log.msg( 'we got a PEP support')
				self.pep = True
				self.registerFeature('http://jabber.org/protocol/tune')
				self.registerFeature('http://jabber.org/protocol/tune+notify')
#		print self.disco[self.jid.host][None]['identities']
	def sendPEP(self,  typ,  attrs):
		iq = IQ(self.xmlstream, 'set')
		pb = iq.addElement('pubsub', 'http://jabber.org/protocol/pubsub' ).addElement('publish')
		pb['node'] = 'http://jabber.org/protocol/' + typ
		tune = pb.addElement('item').addElement(typ, 'http://jabber.org/protocol/' + typ)
		for key, val in attrs.iteritems():
			tune.addElement(key,  content = val)
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._pepReceived)

	def _pepReceived(self,  el):
		log.msg(el.toXml())
	
	def registerPEP(self,  to,  typ): #typ = tune|mood|activity
		iq = IQ(self.xmlstream, 'set')
		iq['to'] = to
		sb = iq.addElement('pubsub',  'http://jabber.org/protocol/pubsub').addElement('subscribe')
		sb['jid'] = self.jid.userhost()
		sb['node'] ='http://jabber.org/protocol/'+typ
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._pepReceived)

	def registerFeature(self, feature, node = None):
		if self.discofeatures.has_key(node):
			self.discofeatures[node].append(feature)
		else:
			self.discofeatures[node] = []
			self.discofeatures[node].append(feature)

	def getRoster(self):
		log.msg('get roster')
		iq = IQ(self.xmlstream, 'get')
		iq['type'] = 'get'
		q = iq.addElement('query')
		q['xmlns']='jabber:iq:roster'
		self.disp(iq['id'])
		d = iq.send()
		self.on_xml(iq.toXml())
		d.addCallback(self._onRosterArrive)

	def onRosterAdd(self,el):
		log.msg("roster item add")
		self.disp(el['id'])
		for child in el.elements():
			if child.name == "query":
				allGroups=[]
				for k,v in self.roster['groups'].iteritems():
					allGroups.append(k)
				for item in child.elements():
					groups = []
					itemjid = item['jid']
					for group in item.elements():
						if group.name == 'group':
							groups.append(unicode(group))
							if unicode(group) not in allGroups:
								# add group item to ther roster
								self.roster['groups'][unicode(group)] = self.main._addGroup(group)
								allGroups.append(unicode(group))
					if item.hasAttribute('name'):
						name = item['name']
					else:
						name = ''
					subscription = ''
					if item.hasAttribute('subscription'):
						subscription = item['subscription']
					#print item['jid'],groups
					if subscription == 'remove'  and self.roster['users'].has_key(itemjid):
						log.msg('deleting contact')
						self.on_DeleteContact(itemjid)
						del self.roster['users'][itemjid]
					elif not self.roster['users'].has_key(itemjid):
						rosterItems=[]
						#if len(groups)==0:
							# add user item to Unknown group
						contact = Contact(self, itemjid, name, subscription, rosterItems, groups)
						self.roster['users'][itemjid] = contact
						self.on_rosterAddUser(contact)
							#rosterItems.append(self.main._addUser(itemjid,name,self.roster['groups']['Unknown']))
						#for group in groups:
							#self.on_rosterAddUser(contact)
							# add user item to the group
							#rosterItems.append(self.main._addUser(itemjid,name,self.roster['groups'][group]))
						
					elif subscription != 'remove'  and self.roster['users'].has_key(itemjid):
						print "update"
						contact = self.roster['users'][itemjid]
						contact.name = name
						contact.groups = groups
						self.on_UpdateContact(itemjid)
		iq = Element((None, 'iq'))
		iq['from'] = self.jid.full()
		iq['to'] = self.jid.host
		iq['id'] = el['id']
		iq['type'] = 'result'
		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)

	def sendRosterUpdate(self, jid, name, subscription, groups):
		iq = Element((None, 'iq'))
		iq.addUniqueId()
		iq['from'] = self.jid.full()
		iq['type'] = 'set'
		q = iq.addElement('query')
		q['xmlns']='jabber:iq:roster'
		item = q.addElement('item')
		item['jid'] = jid
		item['name'] = name
		item['subscription'] = subscription
		for group in groups:
			item.addElement('group', content = group)
		self.disp(iq['id'])
		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)

	def getVCard(self, jid):
		log.msg( 'requesting vcard for ' + unicode(jid))
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		iq.addElement('vCard', 'vcard-temp')
		self.disp(iq['id'])
		d = iq.send()
		self.on_xml(iq.toXml())
		d.addCallback(self._vcardReceived)
		d.addErrback(self._noVcard, jid) 

	def _noVcard(self, err, jid): 
		#               print jid, ' no vcard available' 
		log.msg('chci ulozit ' + jid )
		self.main.cache.set_avatar(jid, ['nic', 'nic'])

	def _vcardReceived(self, el):
		log.msg( 'vcard received')
		vcard = el.firstChildElement()
		card = {} 
		if vcard == None :
			return
		for x in vcard.elements():
			if len(x.children)>0:
				for y in x.elements():
					card[y.name]=unicode(y)
			else:
				card[x.name]=unicode(x)
		self.on_vcardReceived(el['from'], card)

	def getBookmarks(self):
		log.msg('get bookmarks')
		iq = IQ(self.xmlstream, 'get')
		q = iq.addElement('query', 'jabber:iq:private')
		q.addElement('storage', 'storage:bookmarks')
		self.on_xml(iq.toXml())
		self.disp(iq['id'])
		d = iq.send()
		d.addCallback(self._bookmarksReceived)
		d.addErrback(self._bookmarksErrReceived)

	def setBookmarks(self):
		iq = IQ(self.xmlstream, 'set')
		q = iq.addElement('query', 'jabber:iq:private')
		storage = q.addElement('storage', 'storage:bookmarks')
		for bookmark in self.bookmarks['conference'].itervalues():
			b = storage.addElement('conference')
			b['jid'] = bookmark.jid.userhost()
			b['name'] = bookmark.name
			b['autojoin'] = unicode(bookmark.autojoin)
			if bookmark.nick:
				b.addElement('nick', content = bookmark.nick)
			if bookmark.password:
				b.addElement('password', content = bookmark.password)

		for bookmark in self.bookmarks['url'].itervalues():
			b = storage.addElement('url')
			b['name'] = bookmark.name
			b['url'] = bookmark.url

		self.disp(iq['id'])
		self.on_xml(iq.toXml())
		d = iq.send()
		d.addCallback(self._bookmarksSet)

	def _bookmarksSet(self, el):
		log.msg('bookmarks set sucessfully')

	def _bookmarksErrReceived(self, err):
		pass #no tak neprisly no
	def _bookmarksReceived(self, el):
		log.msg( 'bookmarks received')
		for child in el.elements():
			if child.name == 'query':
				for els in child.elements():
					if els.name == 'storage':
						for bookmark in els.elements():
							if bookmark.name == 'conference':
								jid = bookmark['jid']
								if bookmark.hasAttribute('name'):
									name = bookmark['name']
								else:
									name = jid
								autojoin = False
								if bookmark.hasAttribute('autojoin'):
									autojoin = bookmark['autojoin']
								nick = self.jid.user
								password = None
								for elm in bookmark.elements():
									if elm.name == 'nick':
										nick = unicode(elm)
									if elm.name == 'password':
										password = unicode(elm)

								self.bookmarks['conference'][name] = Bookmark(name, 'conference', jid, autojoin, nick,  password)
							if bookmark.name == 'url':
								url = bookmark['url']
								if bookmark.hasAttribute('name'):
									name = bookmark['name']
								else:
									name = url
								self.bookmarks['conference'][name] = Bookmark(name, 'url', url = url)


	def getMetacontacts(self):
		log.msg('get meta contacts')
		iq = IQ(self.xmlstream, 'get')
		q = iq.addElement('query', 'jabber:iq:private')
		q.addElement('storage', 'storage:metacontacts')
		self.on_xml(iq.toXml())
		self.disp(iq['id'])
		d = iq.send()
		d.addCallback(self._metacontactsReceived)
		d.addErrback(self._metacontactsErrReceived)
	
	def _metacontactsErrReceived(self,  err):
		log.msg('meta error')
		self.getRoster()
		self.on_metaFail(err)
		
	def _metacontactsReceived(self,  el):
		log.msg( 'metacontacts received')
		q = el.firstChildElement()
		storage = q.firstChildElement()
		for item in storage.elements():
			order = 1
			if item.hasAttribute('order'):
				order = int(item['order'])
			self.roster_meta[item['jid']] = {'tag': item['tag'],  'order': order}
		self.getRoster()

	def setMetacontacts(self):
		log.msg( 'sending metacontacts')
		iq = IQ(self.xmlstream, 'set')
		q = iq.addElement('query', 'jabber:iq:private')
		storage = q.addElement('storage', 'storage:metacontacts')
		for jid,  val in self.roster_meta.iteritems():
			m = storage.addElement('meta')
			m['jid'] = jid
			m['tag'] = val['tag']
			m['order'] = str(val['order'])
		self.disp(iq['id'])
		self.on_xml(iq.toXml())
		d = iq.send()
		d.addCallback(self._metacontactsSet)
	def _metacontactsSet(self,  el):
		log.msg( 'metacontacts set')

	def addContact(self, jid, msg, name='', groups=[]):
		log.msg( 'add contact')
		self.sendRosterUpdate(jid, name, 'none', groups)
		#self.sendPresence(to = jid, status = msg, typ = 'subscribe')

	def delContact(self, jid):
		self.sendRosterUpdate(jid, '', 'remove', [])
		#self.sendPresence(to = jid, typ = 'unsubscribe')
		if self.roster_meta.has_key(jid):
			del self.roster_meta[jid]
			self.setMetacontacts()

	def onXML(self, el):
		if el.hasAttribute('id') and el.name == 'iq':
			if not el['id'] in self.idlist:
				log.msg('nezpracovane iq '+ el.toXml())
				el['type']  = 'error'
				el['to'] = el['from']
				el['from'] = self.jid.full()
				err = el.addElement('error')
				err['code'] = '501'
				err['type'] = 'cancel'
				err.addElement('feature-not-implemented')
				self.disp(el['id'])
				self.on_xml(el.toXml())
				self.xmlstream.send(el)
		elif not el.hasAttribute('id') and  el.name == 'iq' :
			log.msg( 'iq bez id'+ el.toXml())
			el['type']  = 'error'
			el['to'] = el['from']
			el['from'] = self.jid.full()
			err = el.addElement('error')
			err['code'] = '400'
			err['type'] = 'modify'
			err.addElement('bad-request')
			self.on_xml(el.toXml())
			self.xmlstream.send(el)
	def logIt(self, el):
		if self.log:
			self.on_xml(el.toXml())
	def _onRosterArrive(self, el):
		log.msg( 'roster arrived')
		ln = 0
		for child in el.elements():
			if child.name == "query":
				allGroups=['Unknown']
				for item in child.elements():
					ln = ln + 1
					groups = []
					for group in item.elements():
						if group.name == 'group':
							groups.append(unicode(group))
							if unicode(group) not in allGroups:
								# add group item to ther roster
								self.roster['groups'][unicode(group)] = self.main._addGroup(unicode(group))
								allGroups.append(unicode(group))
					if item.hasAttribute('name'):
						name = item['name']
					else:
						name = ''
					#print item['jid'],groups
					tag = None
					order = 1
					if self.roster_meta.has_key(item['jid']):
						tag = self.roster_meta[item['jid']]['tag']
						order = self.roster_meta[item['jid']]['order']
					contact = Contact(self, item['jid'], name, item['subscription'], [], groups, tag =  tag, order =  order)
					self.roster['users'][item['jid']] = contact
					self.on_rosterAddUser(contact)

		log.msg( 'roster arrived')
		presence = Element(('jabber:client','presence'))
		self.on_xml(presence.toXml())
		self.xmlstream.send(presence)
		cekej = 20
		if ln*0.05 < cekej:
			cekej = ln*0.05
		print ln,  cekej
		reactor.callLater(cekej,  self.onFirstPresence)
		#self.onFirstPresence()
		self.on_rosterArrived()

	def _authfailed(self,xmlstream):
		log.msg( "auth_failed")
		self.on_authFailed(xmlstream)

	def _invaliduser(self,xmlstream):
		log.msg( "invalid_user")
		#self.on_invalidUser(self)

	def onMessage(self, el):
		log.msg( 'message received')
		typ = el['type']
		frm = el['from']

		body = subject =xhtml = chatstate = delay = None
		for child in el.elements():
			if child.name == "body":
				body = unicode(child)
			if child.name == "subject":
				subject = unicode(child)
			if child.name == 'html':
				body = child.children[0]
				xhtml = body.toXml()
			if child.name in ['active',  'inactive',  'composing',  'paused',  'gone']:
				chatstate = child.name
			if child.name == 'delay':
				delay = child['stamp']
			if child.name == 'x':
				if child.defaultUri == 'jabber:x:delay' :
					delay = child.getAttribute('stamp')

		if self.groupchats.has_key(jid.JID(frm).userhost()):
			self.on_GCmessage(frm,typ,body,subject, xhtml,  chatstate,  delay)
		else:
			self.on_message(frm,typ,body,subject, xhtml,  chatstate,  delay)

	def onSubscribe(self, el):
		log.msg( 'on subscribe')
		status = ''
		for child in el.elements():
			if child.name == 'status':
				status = unicode(child)
		self.on_subscribe(el['from'], status)

	def onSubscribed(self, el):
		log.msg( 'on subscribed')
		self.on_subscribed(el['from'])

	def onUnSubscribe(self, el):
		log.msg('on unsubscribe')
		self.on_unsubscribe(el['from'])

	def onUnSubscribed(self, el):
		log.msg( 'on unsubscribed')
		self.on_unsubscribed(el['from'])	

	
	def onFirstPresence(self):
		log.msg( 'first presences')
		self.first_wait = False
		self.on_firstpresence(self.first_presence)
	
	def onPresence(self, el):
##		print 'presence > ', el['from']
		frm = jid.JID(el['from'])
		fromjid = frm.userhost()
		resource = jid.JID(el['from']).resource

		show = status = priority = typ = affiliation = role = truejid = hash = None
		codes = []
		if el.hasAttribute('type'):
			if el['type'] != 'unavailable':
				return
			else:
				typ = 'unavailable'
		features = []
		for child in el.elements():
			if child.name == 'show':
				show = child.__str__()
			elif child.name == 'status':
				status = child.__str__()
				pass
			elif child.name == 'priority':
				priority = child.__str__()
				if priority == None:
					log.msg( el.toXml())
			elif child.name == 'c':
				caps_node = child['node']

				if child.hasAttribute('ext'):
					caps_node = '%s#%s'%(caps_node, child['ext'])
				else:
					caps_node = '%s#%s'%(caps_node, child['ver'])
				if self.caps_cache.has_key(caps_node):
					features = self.caps_cache[caps_node]
				else:	
					if typ !='unavailable':
						self.getFeatures(frm, caps_node)
			if child.name == 'x' and child.defaultUri == 'http://jabber.org/protocol/muc#user':
				for item in child.elements():
					if item.name == 'item':
						affiliation = item['affiliation']
						role = item['role']
						if item.hasAttribute('jid'):
							truejid = item['jid']
					if item.name == 'status' :
						codes.append(item['code'])
			elif child.name == 'x' and child.defaultUri == 'vcard-temp:x:update':
				hash = unicode(child.firstChildElement())

		if show == None and not el.hasAttribute('type'):
			show = 'online'
		elif el.hasAttribute('type'):
			if el['type'] =='unavailable':
				show = 'offline'
		if self.roster['users'].has_key(fromjid):
			first = self.roster['users'][unicode(fromjid)].setStatus(resource, show,status)
			if self.roster['users'][fromjid].resources.has_key(resource):
				self.roster['users'][fromjid].setPriority(resource, priority)
				self.roster['users'][fromjid].setFeatures(resource, features)

			chci_card = True 
			if self.roster['users'][fromjid].avatar_hash == 'nic': 
				chci_card = False 
			elif hash == None and self.roster['users'][fromjid].avatar_hash !='': 
				chci_card = False 
				pass 
			elif self.roster['users'][fromjid].avatar_hash == hash: 
				## print fromjid, 'ma spravneho avatara' 
				chci_card = False 
				pass  
			if chci_card :
##				print fromjid, hash, self.roster['users'][fromjid].avatar_hash 
				self.getVCard(fromjid)
			if first and self.first_wait:
				self.first_presence.append((frm,show))
			else:
				self.on_presence(frm,show)
		elif self.groupchats.has_key(fromjid):
			if show=="offline":
				self.on_GCpresence(fromjid, resource,  show,  status,  codes)
			self.groupchats[fromjid].setStatus(resource,  show,  status)
			if self.groupchats[fromjid].users.has_key(resource):
				self.groupchats[fromjid].setInfo(resource,  affiliation,  role,  truejid)
				#self.groupchats[fromjid]
			if show!="offline":
				self.on_GCpresence(fromjid, resource,  show,  status,  codes)
			return
		else:
##			print 'contact not in roster'
			pass

	def onPresenceError(self,  el):
		#zatim jenom GC errory .. ani nevim jestli ma smysl zachytavat i jine ..
		frm = jid.JID(el['from'])
		fromjid = frm.userhost()
		resource = jid.JID(el['from']).resource
		if self.groupchats.has_key(fromjid):
			err = el.firstChildElement()
			errel = err.firstChildElement()
			self.on_GCpresenceError(fromjid, err['code'],  err['type'],  errel.name )
		
	def getFeatures(self, jid, caps_node):
		log.msg('requesting features'+ caps_node)
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid.full()
		iq['from'] = self.jid.full()
		q = iq.addElement('query', 'http://jabber.org/protocol/disco#info')
		if caps_node != None:
			q['node'] = caps_node
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._featuresReceived, caps_node)

	def _featuresReceived(self, el, node):
		log.msg( 'features received')
##		self.disp(el['id'])
		features = []
		query = el.firstChildElement()
		for child in  el.query.elements():
			if child.name == 'feature':
				features.append(child['var'])
		self.caps_cache[node] = features
		frm = jid.JID(el['from'])
		resource = frm.resource
		if self.roster['users'].has_key(frm.userhost()):
			self.roster['users'][frm.userhost()].setFeatures(resource, features)


	def onVersion(self, el):
		log.msg('sending version info')
		self.disp(el['id'])
		iq = Element((None, 'iq'))
		iq['to'] = el['from']
		iq['type'] = 'result'
		iq['id'] = el['id']
		q = iq.addElement('query', 'jabber:iq:version')
		q.addElement('name', content = self.client_name)
		q.addElement('version', content = self.version)
		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)

	def getVersion(self, jid):
		log.msg('requesting version info')
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		q = iq.addElement('query', 'jabber:iq:version')
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._versionReceived)
		
	def _versionReceived(self, el):
		log.msg('version info received')
		name = version = os = None
		query = el.firstChildElement()
		for child in  query.elements():
			if child.name == 'name':
				name = unicode(child)
			if child.name == 'version':
				version = unicode(child)
			if child.name == 'os':
				os = unicode(child)
		self.on_versionreceive(el['from'], (name, version, os))

	def onDiscoInfo(self, el):
		log.msg( 'received disco#info request')
		self.disp(el['id'])
		iq = Element((None,'iq'))
		iq['to'] = el['from']
		iq['type'] = 'result'
		iq['id'] = el['id']
		q = iq.addElement('query', 'http://jabber.org/protocol/disco#info')
		id = q.addElement('identity')
		id['category'] = 'client'
		id['name'] = self.client_name
		id['type'] = 'pc'

		for child in el.elements():
			if child.name == 'query':
				if child.hasAttribute('node'):
					node = child['node']
				else:
					node = None
		if node == '%s#%s'%(self.caps_node, self.caps_version): #magie: pokud se nas nekdo zepta na caps nasi verze, tak mu rekneme default
			node == None

		if not self.discofeatures.has_key(node):
			node = None
		if node != None:
			q['node'] = node
		for feature in self.discofeatures[node]:
			f = q.addElement('feature')
			f['var'] = feature

		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)

	def onLast(self, el):
		log.msg('received last request')
		self.disp(el['id'])
		iq = Element((None,'iq'))
		iq['to'] = el['from']
		iq['type'] = 'result'
		iq['id'] = el['id']
		q = iq.addElement('query','jabber:iq:last')
		if self.last > 0:
			q['seconds'] = self.last

		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)


	def getDiscoInfo(self, jid, node = None,  callback = None):
		log.msg( 'requesting disco#info: '+jid)
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		iq['from'] = self.jid.full()
		q = iq.addElement('query', 'http://jabber.org/protocol/disco#info')
		if node != None:
			q['node'] = node
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._discoInfoReceived, node,  callback)
		d.addErrback(self._discoInfoErrReceived, (node, jid))

	def _discoInfoReceived(self, el, node,  callback):
		log.msg('disco#info received')
		node_name = node
		frm = el['from']
		if self.disco.has_key(frm):
			if self.disco[frm].has_key(node_name):
				node = self.disco[frm][node_name]
		else:
			self.disco[frm] = {}
			node = {'features':[], 'identities':{},  'items': {}}
		query = el.firstChildElement()
		for child in query.elements():
			if child.name == 'feature':
				node['features'].append(child['var'])
			if child.name == 'identity':
				if child.hasAttribute('name'):
					name = child['name']
				else:
					name = frm
				log.msg( node)
				node['identities'][name] = child.attributes
		self.disco[frm][node_name] = node
		if self.disco[frm][node_name].has_key('err'):
			if self.disco[frm][node_name]['err'].has_key('info'):
				del self.disco[frm][node_name]['err']['info'] #timhle smazem pripadny error ktery zustal po predchozim dotazu

		self.on_discoInfoReceived(frm, node_name)
		if callback != None:
			callback()

	def _discoInfoErrReceived(self, err, info):
		log.msg('disco#info error received')
		node_name = info[0]
		jid = info[1]
		try:
			el = err.value.getElement()
		except:
			log.err( unicode(err)+unicode( info))
			return
		if self.disco.has_key(jid):
			if self.disco[jid].has_key(node_name):
				node = self.disco[jid][node_name]
		else:
			self.disco[jid] = {}
			node = {'err':{'info':''}}

		node['err'] = el.firstChildElement().name
		self.disco[jid][node_name] = node

		self.on_discoInfoReceived(jid, node_name)

	def getDiscoItems(self, jid, node = None, callback = None, callback_par = None):
		log.msg('requesting disco#items ')
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		iq['from'] = self.jid.full()
		q = iq.addElement('query', 'http://jabber.org/protocol/disco#items')
		if node != None:
			q['node'] = node
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._discoItemsReceived, node, callback, callback_par)
		d.addErrback(self._discoItemsErrReceived, (node, jid))

	def _discoItemsReceived(self, el, node, callback, callback_par):
		log.msg( 'disco#items received')
		node_name = node
		frm = el['from']
		if self.disco.has_key(frm):
			if self.disco[frm].has_key(node_name):
				node = self.disco[frm][node_name]
		else:
			self.disco[frm] = {}
			node = {'features':[], 'identities':{},'items':{}}

		query = el.firstChildElement()
		for child in query.elements():
			if child.name == 'item':
				node['items'][child['jid']] = child.attributes

		self.disco[frm][node_name] = node

		if self.disco[frm][node_name].has_key('err'):
			if self.disco[frm][node_name]['err'].has_key('items'):
				del self.disco[frm][node_name]['err']['items'] #timhle smazem pripadny error ktery zustal po predchozim dotazu
		self.on_discoItemsReceived(frm, node_name)
		if callback:
			callback(callback_par)

	def _discoItemsErrReceived(self, err, info):
		log.msg( 'disco#items error received')
		node_name = info[0]
		jid = info[1]
		try:
			el = err.value.getElement()
		except:
			log.err( err)
			return
		if self.disco.has_key(jid):
			if self.disco[jid].has_key(node_name):
				node = self.disco[jid][node_name]
		else:
			self.disco[jid] = {}
			node = {'err':{'items':''}}

		node['err'] = el.firstChildElement().name
		self.disco[jid][node_name] = node
		self.on_discoInfoReceived(jid, node_name)


	def getPrivacy(self):	
		log.msg( 'requesting priacy lists')
		#FIXME: predelat
		iq = IQ(self.xmlstream, 'get')
		q = iq.addElement('query', 'jabber:iq:privacy')
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._privacyReceived)

	def _privacyReceived(self, el):
		#FIXME: predelat
		log.msg( 'privacy lists received' )
		query = el.firstChildElement()
		for child in query.elements():
			if child.name == 'active':
				self.privacy_active = child['name']
			if child.name == 'default':
				self.privacy_active = child['name']
			if child.name == 'list':
				listname = child['name']
				self.privacy_lists[listname] =[]  #pozor na soucasne volani set a get
				for item in child.elements():
					it = {}
					it['attrs'] = item.attributes
					it['types'] = []
					for stanza in item.elements:
						it['types'].append(stanza.name)
					self.privacy_lists['listname'].append(it)
		self.on_privacyReceived()


	def onTime202(self, el):
		log.msg('received time202 request')
		self.disp(el['id'])
		iq = Element((None,'iq'))
		iq['to'] = el['from']
		iq['type'] = 'result'
		iq['id'] = el['id']
		q = iq.addElement('time','urn:xmpp:time')
		q.addElement('tzo', content = "%+03d:00"% (-time.timezone/(60*60)))
		q.addElement('utc', content = time.strftime("%Y-%m-%dT%TZ", time.gmtime()))
		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)

	def getTime202(self, jid):
		log.msg( 'requesting time202 info')
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		iq.addElement('time','urn:xmpp:time')
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._time202Received)

	def _time202Received(self, el):
		log.msg('time202 received')
		t = el.firstChildElement()
		tzo = utc = ''
		for child in t.elements():
			if child.name == 'tzo':
				tzo = child.__str__()
			elif child.name == 'utc':
				utc = child.__str__()
		self.on_time202Received(jid, utc, tzo)

	def onTime90(self, el):
		log.msg( 'received time90 request')
		self.disp(el['id'])
		iq = Element((None,'iq'))
		iq['to'] = el['from']
		iq['type'] = 'result'
		iq['id'] = el['id']
		q = iq.addElement('query', 'jabber:iq:time')
		q.addElement('utc', content = time.strftime("%Y%m%dT%T", time.gmtime()))
		q.addElement('tz', content = time.strftime("%Z", time.gmtime()))
##		q.addElement('display', content = unicode(time.strftime(u"%c", time.localtime())))
		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)


	def joinGC(self,  jid, nick):
		gc = Groupchat(self,  jid, nick)
		self.groupchats[jid] = gc
		gc.join()

	def leaveGC(self,  jid):
		self.groupchats[jid] .leave()
		del self.groupchats[jid]
		log.msg( 'left MUC: '+ jid)

	
	def sendFile(self, jid, filename, size, fp):
		iq = IQ(self.xmlstream, 'set')
		iq['to'] = jid
		sid = str(random.randint(1000, sys.maxint))
		si = iq.addElement('si', 'http://jabber.org/protocol/si')
		si['id'] = sid
		si['profile'] = 'http://jabber.org/protocol/si/profile/file-transfer'
		file = si.addElement('file', 'http://jabber.org/protocol/si/profile/file-transfer')
		file['name'] = filename
		file['size'] = size
		feature = si.addElement('feature', 'http://jabber.org/protocol/feature-neg')
		x = feature.addElement('x', 'jabber:x:data')
		x['type'] = 'form'
		field = x.addElement('field')
		field['var'] = 'stream-method'
		field['type'] = 'list-single'
		field.addRawXml('<option><value>http://jabber.org/protocol/bytestreams</value></option>')
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._ftreplyReceived, sid)
	
	def _ftreplyReceived(self, el, sid):
		print el.toXml()
		iq = IQ(self.xmlstream, 'set')
		iq['to'] = el['from']
		q = iq.addElement('query', 'http://jabber.org/protocol/bytestreams')
		q['sid'] = sid
		q['mode'] = 'tcp'
		for proxy, data in self.ft_proxies.iteritems():
			streamhost = q.addElement('streamhost')
			streamhost['host'] = data[0]
			streamhost['jid'] = proxy
			streamhost['port'] = data[1]
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._ftreplyhostReceived, sid)
		d.addErrback(self._ftreplyhostErrReceived)
	
	def _ftreplyhostReceived(self, el, sid):
		print el.toXml()
		q = el.firstChildElement()
		streamhost = q.firstChildElement()
		host = streamhost['jid']
		addr = sha.new("%s%s%s" % (sid, self.jid.full(), el['from'])).hexdigest()
		f = ClientFactory()
		f.protocol = FTTest
		factory = socks5.ClientFactory(host, int(self.ft_proxies[host][1]), addr, 0, f, xmpp = self, xmpp_sid = sid) 
		d = reactor.connectTCP(host, int(self.ft_proxies[host][1]), factory)
		print (d)
		reactor.callLater(2,self.ftActivate,host, sid, factory)
		
	def ftActivate(self, jid, sid, factory):
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		q = iq.addElement('query', 'http://jabber.org/protocol/bytestreams')
		q['sid'] = sid
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._ftactivated, factory)
	
	def _ftactivated(self, el, factory):
		print 'prenasime'
		print dir(factory), factory, dir(factory.otherFactory.protocol.transport)
		factory.otherFactory.protocol.transport.write('uuuuuuuuuuuuuu')
		
	
	def _ftreplyhostErrReceived(self, err):
		print err
	
	def disp(self, id):
		self.idlist.append(id)

class FTTest(Protocol):
	def connectionMade(self):
		print 'jsme spojeni s proxy'
		self.transport.write('uaaaaaaffffffffffffffffffdddddddddddddddddffffffffffffffwwwwwwwwwwwwweeeeeeeeeessssssssssddddddddddddwwwwwwwwwwwddddddddddddddddddddddddwwwwaaaaaaaaaaaaaaa')
		print dir(self.factory)


	def connectionLost(self, reason):
		print 'ztrata spojeni : ', reason
	
	def dataReceived(self, data):
		print 'neco nam prislo'
