import sys,  re
from calendar import timegm
from twisted.python import log
import jid
from twisted.words.xish import domish
from twisted.words.xish.domish import Element

class MessageInit:
	def __init__(self,  client):
		self.client = client
		self.dispatcher = self.client.dispatcher
	
	def send(self,  xml):
		self.client.xmlstream.send(xml)
	
	def onMessage(self, el):
		try:
			typ = el['type']
		except:
			typ = 'normal'
		frm = el['from']
		frmjid = jid.JID(frm)
		if frmjid.resource:
			frm=unicode(frmjid.userhost()).lower()+"/"+frmjid.resource
		else:
			frm=unicode(frm).lower()
		body = subject =xhtml = chatstate = delay = error = attention = receipts = pep = event = None
		for child in el.elements():
			if child.name == "request":
				if child.defaultUri == "urn:xmpp:receipts":
					message=Element((None, "message"))
					message["to"] = el["from"]
					message["from"] = self.client.jid.full()
					try:
						message["id"] = el["id"]
					except KeyError:
						pass # kdyby to nejakej chytrak poslal bez id, muze jabbim shodit
					message.addElement("received", "urn:xmpp:receipts")
					self.send(message)
			if child.name == "body":
				body = unicode(child)
			if child.name == 'error':
				error = 'error'
				for x in child.elements():
					if x.name != 'text':
						error = x.name
			if child.name == "subject":
				subject = unicode(child)
			if child.name == 'html':
				xbody = child.firstChildElement()
				xbody.attributes = {}
				del(xbody.defaultUri)
				del(xbody.uri)
				xhtml = xbody.toXml().replace('<body>','').replace('</body>', '')
			if child.name in ['active',  'inactive',  'composing',  'paused',  'gone']:
				chatstate = child.name
				try:
					if not 'http://jabber.org/protocol/chatstates' in self.client.roster['users'][frmjid.userhost()].resources[frmjid.resource].features:
						self.client.roster['users'][frmjid.userhost()].resources[frmjid.resource].features.append('http://jabber.org/protocol/chatstates')
				except:
					pass #proste user neni v rosteru, nebo je to muc, nebo cojavim ;)
			if child.name == 'delay':
				# xep-0203:
				#  The format MUST adhere to the dateTime format specified in XEP-0082
				#  and MUST be expressed in UTC.
				stamp = child.getAttribute('stamp')
				m = re.match(r'(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)(\.\d+)?Z', stamp)
				if m:
					delay = timegm( map(int, m.groups()[0:6]) + [0,0,0] )
			if child.name == 'x':
				if child.defaultUri == 'jabber:x:delay' :
					# xep-0091:
					#   The format SHOULD be "CCYYMMDDThh:mm:ss"
					#   ... not the format defined in XEP-0082.
					#   The timezone is be understood as UTC.
					stamp = child.getAttribute('stamp')
					m = re.match(r'(\d\d\d\d)(\d\d)(\d\d)T(\d\d):(\d\d):(\d\d)', stamp)
					if m:
						delay = timegm( map(int, m.groups()[0:6]) + [0,0,0] )
				if child.defaultUri == 'jabber:x:event':
					elm = child.firstChildElement()
					if elm:
						chatstate = elm.name
				if child.defaultUri == 'http://jabber.org/protocol/muc#user': # invitation
					return
				if child.defaultUri == 'http://jabber.org/protocol/rosterx':
					self.client._processRosterX(frm, child)


			if child.name == 'confirm': # xep0070 - processed elsewhere
				return
			
			if child.name == 'attention':
				attention = True
			if child.name == 'received':
				try:
					del self.client.messageReceipts[el['id']]
				except:
					log.err('Couldn\'t remove nonexisten message id')
				print self.client.messageReceipts
				return
			
			if child.name == 'event' and child.defaultUri == 'http://jabber.org/protocol/pubsub#event':
				items = child.firstChildElement()
				itm = items.firstChildElement()
				pep = items.getAttribute('node')
				
				if itm != None:
					children = []
					for elm in itm.elements():
						children.append(elm)
					if len(children)==1:
						payload = children[0]
					else:
						payload = children
					
					event = {}
#					for at in payload.elements():
#						event[at.name] = unicode(at)
				else:
					
					payload = None
				print el.toXml()
				c = self.client.getContactByJid(frm)
				if c != None:
					c.setPEP(pep, payload) #zapisem si to do kontaktu
				self.dispatcher.publishEvent('on_pep', frm, pep, payload)
						
		
		if error == None and el.getAttribute('type') == 'error':
			error = 'Unknown Error'
		
		if attention == True and delay == None and typ == 'headline':
			self.dispatcher.publishEvent('on_attention', frm, body, subject, xhtml, error)
			return

		if self.client.groupchats.has_key(jid.JID(frm).userhost()):
#			self.on_GCmessage(frm,typ,body,subject, xhtml,  chatstate,  delay)
			self.dispatcher.publishEvent('on_GCmessage', frm,typ,body,subject, xhtml,  chatstate,  delay, error)
		else:
# 			self.on_message(frm,typ,body,subject, xhtml,  chatstate,  delay)
			if typ!="groupchat":
				self.dispatcher.publishEvent('on_message', frm,typ,body,subject, xhtml,  chatstate,  delay, error)

	def onInvite(self, el):
		if el['type'] =='error':
			for child in el.elements():
				error = 'error'
				for x in child.elements():
					if x.name != 'text':
						error = x.name
			self.dispatcher.publishEvent('on_GCmessage', el['from'],'error','',None, None,  None, None, error)
			return 
		room = el["from"]
		for child in el.children:
			if child.name == "x":
				invite = child.firstChildElement()
				break
		jid = invite["from"]
		reason = None
		cont = False
		for child in invite.children:
			if child.name == "reason":
				reason = unicode(child)
			if child.name == "continue":
				cont = True
		log.msg("invitation recieved to: %s; from %s; reason: %s" % (room, jid, reason))
		self.client.reactor.callFromThread(self.client.on_invite,jid, room, reason, cont)
#		self.main.showInvitation(jid, room, reason, cont)
