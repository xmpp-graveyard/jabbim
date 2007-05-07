import sys
from twisted.python import log
from twisted.internet import protocol

 
from twisted.words.protocols import jabber
from twisted.words.protocols.jabber import client,jid
from twisted.words.xish import domish
from twisted.internet import reactor
from twisted.words.protocols.jabber.xmlstream import IQ

class Contact:
	#TODO: vyresit vice resource, prioritu a stav ke kazde
	def __init__(self, jid, name, subscription, item, groups = [], status = ()):
		self.jid = jid
		self.name = name
		self.subscription = subscription
		self.groups = groups
		self.status = status
		self.rosterItem = item

	def setStatus(self, status):
		self.status = status
	
	
class Client:
	def __init__(self, JID, password, host, port,main):
		self.jid = jid.JID(JID)
		self.password  = password
		self.host = host
		self.port = port
		self.factory = None
		self.connection = None
		self.main=main # mainWindow
		self.roster = {}
		log.startLogging(sys.stdout)

	def connect(self):
		self.factory = client.basicClientFactory(self.jid,self.password)
		self.factory.addBootstrap('//event/stream/authd',self._authd)
		self.factory.addBootstrap("//event/client/basicauth/invaliduser", self._authfail)
		self.factory.addBootstrap("//event/client/basicauth/authfailed", self._authfail)
		self.factory.addBootstrap("//event/stream/error", self._authfail)
		self.connection=reactor.connectTCP(self.host,self.port,self.factory)
	
	def disconnect(self):
		self.connection.disconnect()
	
	def _authd(self, xmlstream):
		self.main._connected()
		xmlstream.addObserver("/presence", self.onPresence)
		xmlstream.addObserver("/message", self.onMessage)
		iq = IQ(xmlstream, 'get')
		print unicode(iq)
		iq['from'] = unicode(self.jid)
		iq['type'] = 'get'
		q = iq.addElement('query')
		q['xmlns']='jabber:iq:roster'
		try:
			d = iq.send()
			d.addCallback(self._onRosterArrive, xmlstream)
		except Exception, e:
			print e
		
	
	def _onRosterArrive(self, el, xmlstream):
		print 'roster arrived'
		for child in el.elements():
			if child.name == "query":
				for item in child.elements():
					print item['jid']
					groups = []
					for group in item.elements():
						if group.name == 'group':
							groups.append(group.__str__())
					if item.hasAttribute('name'):
						name = item['name']
					else:
						name = ''
					rosterItem = self.main.ui.roster.addUser(item['jid'],name,None)
					contact = Contact(item['jid'], name, item['subscription'], rosterItem, groups)
					self.roster[item['jid']] = contact
		presence = domish.Element(('jabber:client','presence'))
		xmlstream.send(presence)

	
	def _authfail(self, xmlstream):
		print 'auth failed'
	
	def onMessage(self, el):
		for child in el.elements():
			if child.name == "body":
				body = child.__str__()
				print body
		
	
	def onPresence(self, el):
		print el['from']
		frm = jid.JID(el['from']).userhost()
		show = status = priority = None
		for child in el.elements():
			if child.name == 'show':
				show = child.__str__()
			elif child.name == 'status':
				status = child.__str__()
			elif child.name == 'priority':
				priority = child.__str__()
		if self.roster.has_key(frm):
			self.roster[unicode(frm)].setStatus((show,status))
##			self.roster.setResource(resource, priority)
		else:
			print 'contact not in roster'
		pass