import sys
from twisted.python import log
from twisted.internet import protocol

 
from twisted.words.protocols import jabber
from twisted.words.protocols.jabber import client,jid
from twisted.words.xish import domish
from twisted.internet import reactor
from twisted.words.protocols.jabber.xmlstream import IQ

from derived import derived

class Bookmark:
	def __init__(self, name, typ, JID = None, autojoin = False, nick = None, password = None, url = None):
		self.name = name
		self.typ = typ #url/conference
		self.jid = jid.JID(JID)
		self.autojoin = autojoin
		self.nick = nick
		self.password = password
		self.url = url
		

class Contact:
	
	def __init__(self, jid, name, subscription, items=[], groups = [], status = ()):
		self.jid = jid
		self.name = name
		self.subscription = subscription
		self.groups = groups
		self.status = status
		self.rosterItems = items # user can be in many groups => more items
		self.resources={} #resource:(show,status,priority)



	def setStatus(self, resource, show, status):
		if self.resources.has_key(resource):
			self.resources[resource] = {'show': show, 'status': status}
		else:
			self.resources[resource] = {'show': show, 'status': status, 'priority' : 0}
		if resource == self.getHighestResource():
			self.status = (show, status)
			
	def setPriority(self, resource, priority):
		if self.resources.has_key(resource):
			self.resources[resource]['priority'] = priority
		else:
			self.resources[resource] = {'show': None, 'status': '', 'priority' : priority}
			
	def getHighestResource(self):
		prio = None
		highest = None
		for res,val in self.resources.iteritems():
##			print val
			if val.has_key('priority') :
				if val['priority']>prio:
					highest = res
					prio = val['priority']
		return highest

	def getUserItems(self):
		# get user QTreeWidget item from every group
		return self.rosterItems
	
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
		self.log = True
		self.logfile = sys.stdout
		self.on_init()

	def sendPresence(self, to = None, show = None, status = None, priority = None, typ = None):
		presence = domish.Element((None, 'presence'))
		presence['from'] = unicode(self.jid)
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
		print 'sending out presence to: ' , to
		self.on_xml(presence.toXml())
		self.xmlstream.send(presence)
	
	def sendMessage(self, to, body, typ='chat', subject = None, composing = None):
		#TODO: composing events
		message = domish.Element((None,'message'))
		message['to'] = to
		message.addElement('body', content = body)
		message['type'] = typ
		if type == 'normal' and subject:
			message.addElement('subject', content = subject)
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
		self.xmlstream.addObserver("/presence", self.onPresence)
		self.xmlstream.addObserver("/message", self.onMessage)
		self.xmlstream.addObserver("/iq[@type='set']/query[@xmlns='jabber:iq:roster']", self.onRosterAdd)
		self.xmlstream.addObserver("/*", self.onXML)
		self.xmlstream.addObserver("/presence[@type='subscribe']", self.onSubscribe)
		self.xmlstream.addObserver("/presence[@type='unsubscribe']", self.onUnSubscribe)
		self.xmlstream.addObserver("/presence[@type='subscribed']", self.onSubscribed)
		self.xmlstream.addObserver("/presence[@type='unsubscribed']", self.onUnSubscribed)
		self.getRoster()
		self.getBookmarks()

	def getRoster(self):
		print 'get roster'
		iq = IQ(self.xmlstream, 'get')
		iq['from'] =self.jid.full()
		iq['type'] = 'get'
		q = iq.addElement('query')
		q['xmlns']='jabber:iq:roster'
		d = iq.send()
		self.on_xml(iq.toXml())
		d.addCallback(self._onRosterArrive)
		
	def onRosterAdd(self,el):
		print "roster item add"
		for child in el.elements():
			if child.name == "query":
				allGroups=[]
				for k,v in self.roster['groups'].iteritems():
					allGroups.append(k)
				for item in child.elements():
					groups = []
					for group in item.elements():
						if group.name == 'group':
							groups.append(group.__str__())
							if group.__str__() not in allGroups:
								# add group item to ther roster
								self.roster['groups'][group.__str__()] = self.main.ui.roster.addGroup(group.__str__())
								allGroups.append(group.__str__())
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
						contact = Contact(item['jid'], name, subscription, rosterItems, groups)
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
		iq['from'] = self.jid.full()
		iq['type'] = 'set'
		q = iq.addElement('query')
		q['xmlns']='jabber:iq:roster'
		item = q.addElement('item')
		item['jid'] = jid
		item['name'] = name
		item['subscription'] = subscription
		for group in groups:
			item.addElement(group)
		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)
	
	def getVCard(self, jid):
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		iq.addElement('vCard', 'vcard-temp')
		d = iq.send()
		self.on_xml(iq.toXml())
		d.addCallback(self._vcardReceived)
	
	def _vcardReceived(self, el):
		print 'vcard received'
	
	def getBookmarks(self):
		'get bookmarks'
		iq = IQ(self.xmlstream, 'get')
##		iq['to'] = self.jid.host
		q = iq.addElement('query', 'jabber:iq:private')
		q.addElement('storage', 'storage:bookmarks')
		self.on_xml(iq.toXml())
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
								name = bookmark['name']
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
								name = bookmark['name']
								url = bookmark['url']
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

	def _onRosterArrive(self, el):
		print 'roster arrived'
		for child in el.elements():
			if child.name == "query":
				allGroups=['Unknown']
				for item in child.elements():
					groups = []
					for group in item.elements():
						if group.name == 'group':
							groups.append(group.__str__())
							if group.__str__() not in allGroups:
								# add group item to ther roster
								self.roster['groups'][group.__str__()] = self.main.ui.roster.addGroup(group.__str__())
								allGroups.append(group.__str__())
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
					contact = Contact(item['jid'], name, item['subscription'], rosterItems, groups)
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
		#TODO: xhtml-im a composing events
		print 'message received'
		typ = el['type']
		frm = el['from']
		body = subject = ''
		for child in el.elements():
			if child.name == "body":
				body = unicode(child)
			if child.name == "subject":
				subject = unicode(child)
		self.on_message(frm,typ,body,subject)
		
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
		print 'presence > ', el['from']
		frm = jid.JID(el['from'])
		resource = jid.JID(el['from']).resource
		show = status = priority = None
		for child in el.elements():
			if child.name == 'show':
				show = child.__str__()
			elif child.name == 'status':
				status = unicode(child)
			elif child.name == 'priority':
				priority = child.__str__()
		if el.hasAttribute('type'):
			if el['type'] != 'unavailable':
				return
		if self.roster['users'].has_key(frm.userhost()):
			if show == None and not el.hasAttribute('type'):
				show = 'online'
			elif el.hasAttribute('unavailable'):
				if el['type'] !='unavailable':
					show = 'offline'
			self.roster['users'][unicode(frm.userhost())].setStatus(resource, show,status)
			self.on_presence(frm,show)
			self.roster['users'][frm.userhost()].setPriority(resource, priority)
		else:
##			print 'contact not in roster'
			pass
		pass
