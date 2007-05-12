from twisted.words.xish import domish

class Groupchat:
	def __init__(self,  client,  JID,  nick):
		self.client = client
		self.jid = JID
		self.nick = nick
		self.users = {} #nick: MUCContact

	def join(self):
		print 'joining MUC: ',  self.jid
		presence = domish.Element((None, 'presence'))
		presence['to'] = '%s/%s'%(self.jid,  self.nick)
		presence.addElement('x', 'http://jabber.org/protocol/muc')
		self.client.on_xml(presence.toXml())
		self.client.xmlstream.send(presence)

	
	def leave(self,  status = None):
		print 'leaving MUC: ',  self.jid
		presence = domish.Element((None, 'presence'))
		presence['to'] = self.jid
		presence['type'] = 'unavailable'
		if status:
			presence['status'] = status
		presence.addElement('x', 'http://jabber.org/protocol/muc')
		self.client.on_xml(presence.toXml())
		self.client.xmlstream.send(presence)

	
	def setStatus(self,  nick,  show,  status):
		if self.users.has_key(nick):
			self.users[nick].setStatus(show, status)
		else:
			self.users[nick] = MUCContact(self, nick, show, status)

class MUCContact:
	def __init__(self,  muc, nick,  show,  status):
		self.muc = muc
		self.nick = nick
		self.show = show
		self.status = status
	
	def setStatus(self,  show,  status):
		if show == 'offline':
			del  self.muc.users[self.nick]
			self.muc = None
		else:
			self.show = show
			self.status = status
