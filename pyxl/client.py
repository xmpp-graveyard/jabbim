import sys, time
from twisted.python import log
from twisted.internet import protocol

 
from twisted.words.protocols import jabber
from twisted.words.protocols.jabber import client,jid
from twisted.words.xish import domish
from twisted.internet import reactor
from twisted.words.protocols.jabber.xmlstream import IQ

from derived import derived
from contact import *
from groupchat import  *

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
	def __init__(self, JID, password, host, port, main):
		#derived.__init__(self)
		self.jid = jid.JID(JID)
		self.password  = password
		self.host = host
		self.port = port
		self.factory = None
		self.connection = None
		self.main=main # mainWindow
		self.roster = {'users':{},'groups':{}}
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
		self.log = True
		self.logfile = sys.stdout
		self.on_init()
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
	
	def cacheCaps(self, node, features):
		self.caps_cache[node] = features
	
	def sendPresence(self, to = None, show = None, status = None, priority = None, typ = None, caps = True):
		presence = domish.Element((None, 'presence'))
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
			presence['typ'] = typ
		if caps:
			c = presence.addElement('c', 'http://jabber.org/protocol/caps')
			c['node'] = self.caps_node
			c['ver'] = self.caps_version
			if self.caps_ext != None:
				c['ext'] = self.caps_ext
		
		print 'sending out presence to: ' , to
		self.on_xml(presence.toXml())
		self.xmlstream.send(presence)
	
	def sendMessage(self, to, body, typ='chat', subject = None, composing = None, xhtml = None,  muc = False):
		#TODO: composing events
		message = domish.Element((None,'message'))
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
		if self.log:
			log.startLogging(self.logfile)
		self.factory = client.basicClientFactory(self.jid,self.password)
		self.factory.addBootstrap('//event/stream/authd',self._authd)
		self.factory.addBootstrap("//event/client/basicauth/invaliduser", self._invaliduser)
		self.factory.addBootstrap("//event/client/basicauth/authfailed", self._authfailed)
		self.factory.addBootstrap("//event/stream/error", self._authfailed)
		self.connection=reactor.connectTCP(self.host,self.port,self.factory)
	
	def disconnect(self):
		self.connection.disconnect()
	
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
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='jabber:iq:version']", self.onVersion, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='http://jabber.org/protocol/disco#info']", self.onDiscoInfo, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='jabber:iq:last']", self.onLast, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/time[@xmlns='urn:xmpp:time']", self.onTime202, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='jabber:iq:time']", self.onTime90, 1)
		self.getRoster()
		self.getBookmarks()
		self.getDiscoInfo(self.jid.host)
		self.getDiscoItems(self.jid.host)
#		self.getPrivacy()
#		self.joinGC('jdev@conf.netlab.cz',  'Sefator')



	def registerFeature(self, feature, node = None):
		if self.discofeatures.has_key(node):
			self.discofeatures[node].append(feature)
		else:
			self.discofeatures[node] = []
			self.discofeatures[node].append(feature)
	
	def getRoster(self):
		print 'get roster'
		iq = IQ(self.xmlstream, 'get')
		iq['from'] =self.jid.full()
		iq['type'] = 'get'
		q = iq.addElement('query')
		q['xmlns']='jabber:iq:roster'
		self.disp(iq['id'])
		d = iq.send()
		self.on_xml(iq.toXml())
		d.addCallback(self._onRosterArrive)
		
	def onRosterAdd(self,el):
		print "roster item add"
		self.disp(el['id'])
		for child in el.elements():
			if child.name == "query":
				allGroups=[]
				for k,v in self.roster['groups'].iteritems():
					allGroups.append(k)
				for item in child.elements():
					groups = []
					for group in item.elements():
						if group.name == 'group':
							groups.append(unicode(group))
							if unicode(group) not in allGroups:
								# add group item to ther roster
								self.roster['groups'][unicode(group)] = self.main.ui.roster.addGroup(unicode(group))
								allGroups.append(unicode(group))
					if item.hasAttribute('name'):
						name = item['name']
					else:
						name = ''
					subscription = ''
					if item.hasAttribute('subscription'):
						subscription = item['subscription']
					#print item['jid'],groups
					if subscription == 'remove'  and self.roster['users'].has_key(item['jid']):
						print 'deleting contact'
						self.on_DeleteContact(item['jid'])
						del self.roster['users'][item['jid']]
					elif not self.roster['users'].has_key(item['jid']):
						rosterItems=[]
						if len(groups)==0:
							# add user item to Unknown group
							rosterItems.append(self.main.ui.roster.addUser(item['jid'],name,self.roster['groups']['Unknown']))
						for group in groups:
							# add user item to the group
							rosterItems.append(self.main.ui.roster.addUser(item['jid'],name,self.roster['groups'][group]))
						contact = Contact(self, item['jid'], name, subscription, rosterItems, groups)
						self.roster['users'][item['jid']] = contact
					elif subscription != 'remove'  and self.roster['users'].has_key(item['jid']):
						contact = self.roster['users'][item['jid']]
						contact.name = name
						contact.groups = groups
						self.on_UpdateContact(item['jid'])
		iq = domish.Element((None, 'iq'))
		iq['from'] = self.jid.full()
		iq['to'] = self.jid.host
		iq['id'] = el['id']
		iq['type'] = 'result'
		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)
		
	def sendRosterUpdate(self, jid, name, subscription, groups):
		iq = domish.Element((None, 'iq'))
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
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		iq.addElement('vCard', 'vcard-temp')
		self.disp(iq['id'])
		d = iq.send()
		self.on_xml(iq.toXml())
		d.addCallback(self._vcardReceived)
	
	def _vcardReceived(self, el):
		print 'vcard received'
	
	def getBookmarks(self):
		'get bookmarks'
		iq = IQ(self.xmlstream, 'get')
		q = iq.addElement('query', 'jabber:iq:private')
		q.addElement('storage', 'storage:bookmarks')
		self.on_xml(iq.toXml())
		self.disp(iq['id'])
		d = iq.send()
		d.addCallback(self._bookmarksReceived)
		
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
		print 'bookmarks set sucessfully'
		
	def _bookmarksReceived(self, el):
		print 'bookmarks received'
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
	
	def addContact(self, jid, msg):
		print 'add contact'
		self.sendRosterUpdate(jid, None, 'none', [])
		self.sendPresence(to = jid, status = msg, typ = 'subscribe')
	def delContact(self, jid):
		self.sendRosterUpdate(jid, None, 'remove', [])
		self.sendPresence(to = jid, typ = 'unsubscribe')
		
	def onXML(self, el):
		if self.log:
			self.on_xml(el.toXml())
		if el.hasAttribute('id') and el.name == 'iq':
			if not el['id'] in self.idlist:
				print 'nezpracovane iq ', el.toXml()
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
			print 'iq bez id', el.toXml()
			el['type']  = 'error'
			el['to'] = el['from']
			el['from'] = self.jid.full()
			err = el.addElement('error')
			err['code'] = '400'
			err['type'] = 'modify'
			err.addElement('bad-request')
			self.on_xml(el.toXml())
			self.xmlstream.send(el)

	def _onRosterArrive(self, el):
		print 'roster arrived'
		for child in el.elements():
			if child.name == "query":
				allGroups=['Unknown']
				for item in child.elements():
					groups = []
					for group in item.elements():
						if group.name == 'group':
							groups.append(unicode(group))
							if unicode(group) not in allGroups:
								# add group item to ther roster
								self.roster['groups'][unicode(group)] = self.main.ui.roster.addGroup(unicode(group))
								allGroups.append(unicode(group))
					if item.hasAttribute('name'):
						name = item['name']
					else:
						name = ''
					#print item['jid'],groups
					rosterItems=[]
					if len(groups)==0:
						# add user item to Unknown group
						rosterItems.append(self.main.ui.roster.addUser(item['jid'],name,self.roster['groups']['Unknown']))
					for group in groups:
						# add user item to the group
						rosterItems.append(self.main.ui.roster.addUser(item['jid'],name,self.roster['groups'][group]))
					contact = Contact(self, item['jid'], name, item['subscription'], rosterItems, groups)
					self.roster['users'][item['jid']] = contact
			
		presence = domish.Element(('jabber:client','presence'))
		self.on_xml(presence.toXml())
		self.xmlstream.send(presence)

	def _authfailed(self,xmlstream):
		print "auth_failed"
		self.on_authFailed(xmlstream)

	def _invaliduser(self,xmlstream):
		print "invalid_user"
		#self.on_invalidUser(self)
	
	def onMessage(self, el):
		print 'message received'
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
			elif child.name == 'x':
				if child.hasAttribute('jabber:x:delay'):
					delay = child['stamp']


		if self.groupchats.has_key(jid.JID(frm).userhost()):
			self.on_GCmessage(frm,typ,body,subject, xhtml,  chatstate,  delay)
		else:
			self.on_message(frm,typ,body,subject, xhtml,  chatstate,  delay)

	def onSubscribe(self, el):
		print 'on subscribe'
		status = ''
		for child in el.elements():
			if child.name == 'status':
				status = unicode(child)
		self.on_subscribe(el['from'], status)
	
	def onSubscribed(self, el):
		print 'on subscribed'
		self.on_subscribed(el['from'])
		
	def onUnSubscribe(self, el):
		print 'on unsubscribe'
		self.on_unsubscribe(el['from'])
		
	def onUnSubscribed(self, el):
		print 'on unsubscribed'
		self.on_unsubscribed(el['from'])	
	
	def onPresence(self, el):
##		print 'presence > ', el['from']
		frm = jid.JID(el['from'])
		resource = jid.JID(el['from']).resource

		show = status = priority = typ = None
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
					print el.toXml()
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

		if show == None and not el.hasAttribute('type'):
			show = 'online'
		elif el.hasAttribute('type'):
			if el['type'] =='unavailable':
				show = 'offline'
		if self.roster['users'].has_key(frm.userhost()):
			self.roster['users'][unicode(frm.userhost())].setStatus(resource, show,status)
			self.roster['users'][frm.userhost()].setPriority(resource, priority)
			self.roster['users'][frm.userhost()].setFeatures(resource, features)
			self.on_presence(frm,show)
		elif self.groupchats.has_key(frm.userhost()):
			self.groupchats[frm.userhost()].setStatus(resource,  show,  status)
			#self.groupchats[frm.userhost()]
			self.on_GCpresence(frm.userhost(), resource,  show,  status)
			return
		else:
##			print 'contact not in roster'
			pass



	def getFeatures(self, jid, caps_node):
		print 'requesting features', caps_node
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
		print 'features received'
##		self.disp(el['id'])
		features = []
		query = el.firstChildElement()
		for child in  el.query.elements():
			if child.name == 'feature':
				features.append(child['var'])
		self.caps_cache[node] = features
		frm = jid.JID(el['from'])
		resource = jid.JID(el['from']).resource
		if self.roster['users'].has_key(frm.userhost()):
			self.roster['users'][frm.userhost()].setFeatures(resource, features)
		
		
	def onVersion(self, el):
		print 'sending version info'
		try:
			self.disp(el['id'])
		except:
			print el.toXml()
		iq = domish.Element((None, 'iq'))
		iq['to'] = el['from']
		iq['type'] = 'result'
		iq['id'] = el['id']
		q = iq.addElement('query', 'jabber:iq:version')
		q.addElement('name', content = self.client_name)
		q.addElement('version', content = self.version)
		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)
	
	def getVersion(self, jid):
		print 'requesting version info'
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		q = iq.addElement('query', 'jabber:iq:version')
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._versionReceived)
	def _versionReceived(self, el):
		print 'version info received'
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
		print 'received disco#info request'
		self.disp(el['id'])
		iq = domish.Element((None,'iq'))
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
					node = inq['node']
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
		print 'received last request'
		self.disp(el['id'])
		iq = domish.Element((None,'iq'))
		iq['to'] = el['from']
		iq['type'] = 'result'
		iq['id'] = el['id']
		q = iq.addElement('query','jabber:iq:last')
		if self.last > 0:
			q['seconds'] = self.last
		
		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)
	
	
	def getDiscoInfo(self, jid, node = None):
		print 'requesting disco#info'
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		iq['from'] = self.jid.full()
		q = iq.addElement('query', 'http://jabber.org/protocol/disco#info')
		if node != None:
			q['node'] = node
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._discoInfoReceived, node)
		d.addErrback(self._discoInfoErrReceived, (node, jid))

	def _discoInfoReceived(self, el, node):
		print 'disco#info received'
		node_name = node
		if self.disco.has_key(el['from']):
			if self.disco[el['from']].has_key(node_name):
				node = self.disco[el['from']][node_name]
		else:
			self.disco[el['from']] = {}
			node = {'features':[], 'identities':{}}
		query = el.firstChildElement()
		for child in query.elements():
			if child.name == 'feature':
				node['features'].append(child['var'])
			if child.name == 'identity':
				node['identities'][child['name']] = child.attributes
		self.disco[el['from']][node_name] = node
		if self.disco[el['from']][node_name].has_key('err'):
			if self.disco[el['from']][node_name]['err'].has_key('info'):
				del self.disco[el['from']][node_name]['err']['info'] #timhle smazem pripadny error ktery zustal po predchozim dotazu
		self.on_discoInfoReceived(el['from'], node_name)
	
	def _discoInfoErrReceived(self, err, info):
		print 'disco#info error received'
		node_name = info[0]
		jid = info[1]
		el = err.value.getElement()
		if self.disco.has_key(jid):
			if self.disco[jid].has_key(node_name):
				node = self.disco[jid][node_name]
		else:
			self.disco[jid] = {}
			node = {'err':{'info':''}}

		node['err'] = el.firstChildElement().name
		self.disco[jid][node_name] = node
		self.on_discoInfoReceived(jid, node_name)
		
	def getDiscoItems(self, jid, node = None):
		print 'requesting disco#items : '
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		iq['from'] = self.jid.full()
		q = iq.addElement('query', 'http://jabber.org/protocol/disco#items')
		if node != None:
			q['node'] = node
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._discoItemsReceived, node)
		d.addErrback(self._discoItemsErrReceived, (node, jid))
	
	def _discoItemsReceived(self, el, node):
		print 'disco#items received'
		node_name = node
		if self.disco.has_key(el['from']):
			if self.disco[el['from']].has_key(node_name):
				node = self.disco[el['from']][node_name]
		else:
			self.disco[el['from']] = {}
			node = {'items':{}}

		query = el.firstChildElement()
		for child in query.elements():
			if child.name == 'items':
				node['items'][child['name']] = child.attributes
		
		self.disco[el['from']][node_name] = node
		
		if self.disco[el['from']][node_name].has_key('err'):
			if self.disco[el['from']][node_name]['err'].has_key('items'):
				del self.disco[el['from']][node_name]['err']['items'] #timhle smazem pripadny error ktery zustal po predchozim dotazu
		self.on_discoItemsReceived(el['from'], node_name)
	
	def _discoItemsErrReceived(self, err, info):
		print 'disco#items error received'
		node_name = info[0]
		jid = info[1]
		el = err.value.getElement()
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
		print 'requesting priacy lists'
		#FIXME: predelat
		iq = IQ(self.xmlstream, 'get')
		q = iq.addElement('query', 'jabber:iq:privacy')
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._privacyReceived)
	
	def _privacyReceived(self, el):
		#FIXME: predelat
		print 'privacy lists received' 
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
		print 'received time202 request'
		self.disp(el['id'])
		iq = domish.Element((None,'iq'))
		iq['to'] = el['from']
		iq['type'] = 'result'
		iq['id'] = el['id']
		q = iq.addElement('time','urn:xmpp:time')
		q.addElement('tzo', content = "%+03d:00"% (-time.timezone/(60*60)))
		q.addElement('utc', content = time.strftime("%Y-%m-%dT%TZ", time.gmtime()))
		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)
	
	def getTime202(self, jid):
		print 'requesting time202 info'
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		iq.addElement('time','urn:xmpp:time')
		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._time202Received)
	
	def _time202Received(self, el):
		print 'time202 received'
		t = el.firstChildElement()
		tzo = utc = ''
		for child in t.elements():
			if child.name == 'tzo':
				tzo = child.__str__()
			elif child.name == 'utc':
				utc = child.__str__()
		self.on_time202Received(jid, utc, tzo)
	
	def onTime90(self, el):
		print 'received time90 request'
		self.disp(el['id'])
		iq = domish.Element((None,'iq'))
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
		print 'left MUC: ',  jid
	
	def disp(self, id):
		self.idlist.append(id)
