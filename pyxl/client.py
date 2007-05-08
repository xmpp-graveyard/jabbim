import sys
from twisted.python import log
from twisted.internet import protocol

 
from twisted.words.protocols import jabber
from twisted.words.protocols.jabber import client,jid
from twisted.words.xish import domish
from twisted.internet import reactor
from twisted.words.protocols.jabber.xmlstream import IQ

from derived import derived

class Contact:
	#TODO: vyresit vice resource, prioritu a stav ke kazde
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
		iq = IQ(self.xmlstream, 'get')
		iq['from'] = unicode(self.jid)
		iq['type'] = 'get'
		q = iq.addElement('query')
		q['xmlns']='jabber:iq:roster'
		try:
			d = iq.send()
			self.on_xml(iq.toXml())
			d.addCallback(self._onRosterArrive)
		except Exception, e:
			print e

	def onRosterAdd(self,el):
		print "roster item add"
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
					subscription = ''
					if item.hasAttribute('subscription'):
						subscription = item['subscription']
					#print item['jid'],groups
					if subscription == 'remove'  and self.roster['users'].has_key(item['jid']):
						print 'deleting contact'
						del self.roster['users'][item['jid']]
						self.on_DeleteContact(item['jid'])
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
		for child in el.elements():
			if child.name == "body":
				body = child.__str__()
				print body
		
	
	def onPresence(self, el):
		print el['from']
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
		if self.roster['users'].has_key(frm.userhost()):
			if show == None and not el.hasAttribute('unavailable'):
				show = 'online'
			elif el.hasAttribute('unavailable'):
				show = 'offline'
			self.roster['users'][unicode(frm.userhost())].setStatus(resource, show,status)
			self.on_presence(frm,show)
			self.roster['users'][frm.userhost()].setPriority(resource, priority)
		else:
			print 'contact not in roster'
		pass
