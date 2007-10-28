"""
Copyright (C) 2007 	Jan 'Hanzz' Kaluza (hanzz at njs.netlab.cz)
Copyright (C) 2007	Jiri 'Sef' Gabrys	(sef at njs.netlab.cz)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""

from twisted.python import log
from twisted.words.protocols import jabber
from twisted.words.protocols.jabber import client,jid
from twisted.words.xish import domish
from twisted.words.xish.domish import Element
from twisted.words.protocols.jabber.xmlstream import IQ
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import defer
from contact import *
from groupchat import  *

MUCLISTTYPES = {
'voice': ('http://jabber.org/protocol/muc#admin', 'participant', 'role'),
'ban': 	('http://jabber.org/protocol/muc#admin', 'outcast', 'affiliation'),
'member': ('http://jabber.org/protocol/muc#admin', 'member', 'affiliation'),
'moderator': ('http://jabber.org/protocol/muc#admin', 'moderator', 'role'),
'owner': 	('http://jabber.org/protocol/muc#admin', 'owner', 'affiliation'),
'admin': 	('http://jabber.org/protocol/muc#admin', 'owner', 'affiliation')}
class derived:
	def on_authFailed(self,xmlstream):
		pass
	def on_init(self):
		pass
	def on_presence(self,frm,show):
		pass
	def on_GCpresenceError(self,  fromjid,  code,  type,  name, text):
		pass
	def on_firstpresence(self,  bulk):
		for pres in bulk:
			print pres[0], pres[1]
			self.on_presence(pres[0], pres[1])
		pass
	def on_shutdown(self):
		pass
	def on_xml(self, xml):
		pass
	def on_authd(self):
		pass
	def on_metaFail(self, err):
		pass
	def on_UpdateContact(self,jid):
		pass
	def on_DeleteContact(self,jid):
		pass
	
	def on_subscribe(self,kdo, msg):
		pass
	def on_unsubscribe(self, kdo):
		pass
	def on_unsubscribed(self, kdo):
		pass
	def on_subscribed(self, kdo):
		pass
	
	def on_message(self, frm, typ, body, subject = None, xhtml = None,  chatstate = None,  delay = None):
		pass
	def on_GCmessage(self, frm, typ, body, subject = None, xhtml = None,  chatstate = None,  delay = None):
		pass
	
	def on_GCpresence(self,  muc, nick,  show,  status,  codes = []):
		pass
	
	def on_versionreceive(self, jid, version):
		#version = (name, version, os)
		pass
	
	def on_discoInfoReceived(self, jid, node):
		# v self.disco[jid][node] jsou info data nebo error
		pass
	def on_discoItemsReceived(self, jid, node):
		# v self.disco[jid][node] jsou info data nebo error
		pass
	
	def on_privacyReceived(self):
		print self.privacy_lists
		pass

	def on_time202Received(self, jid, utc, tzo):
		pass
	
	def on_rosterAddUser(self, contact):
		pass
	
	def on_rosterArrived(self):
		pass
	
	def on_roleErr(self,  muc,  err,  nick):
		pass
	
	def on_affiliationErr(self,  muc,  err,  nick):
		pass
	def on_vcardReceived(self,  jid, card):
		pass
	
	def on_fileReceived(self, jid, file, methods, id):
		pass
	
	def on_ftEnd(self, sid, error = None): #pokud je error None je vse v poradku, jinak strucny popis chyby.
		del self.ft[sid]
	
	def on_ftTransfered(self, sid, bytes): #pocet prenesenych bajtu pro prenos se SID
		pass
		
	def on_disconnect(self):
		pass
	
	def on_verify(self, id, thread, props, frm, typ): #xep0070
		self.replyVerify(id, thread, props, frm, typ, False)
		pass
	def on_connect(self):
		pass
	def on_invite(self, jid, room, reason = None):
		pass
	########################################################################################################################
	
	########################################################################################################################
	def sendPresence(self, to = None, show = None, status = None, priority = None, typ = None, caps = True):
		"""Posle presenci na zvoleny jid"""
		presence = Element((None, 'presence'))
		presence['from'] = self.jid.full()
		if to:
			presence['to'] = to
		else:
			self.roster['users'][self.jid.userhost()].setStatus(self.jid.resource, show, status)
		if status:
			presence.addElement('status', content = status)
		if show:
			presence.addElement('show', content = show)
		if priority:
			presence.addElement('priority', content = unicode(priority))
		if typ:
			presence['type'] = typ
		if caps:
			c = presence.addElement('c', 'http://jabber.org/protocol/caps')
			c['node'] = self.caps_node
			c['ver'] = self.caps_version
			if self.caps_ext != None:
				c['ext'] = self.caps_ext

		log.msg('sending out presence to: ' + unicode(to))
#		self.on_xml(presence.toXml())
		self.xmlstream.send(presence)

	def sendMessage(self, to, body=None, typ='chat', subject = None, composing = None, xhtml = None,  muc = False):
		# Posle zpravu na jid
		self.dispatcher.publishEvent('on_message_send', to, body, typ, subject,composing, xhtml,  muc)
		message = Element((None,'message'))
		message['to'] = to
		if body != None and body.strip() != '':
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
				if self.roster['users'][JID.userhost()].resources.has_key(JID.resource):
					#log.msg(unicode(self.roster['users'][JID.userhost()].resources[JID.resource].features))
					if self.roster['users'][JID.userhost()].resources[JID.resource].hasFeature('http://jabber.org/protocol/chatstates'):
						message.addElement(composing, 'http://jabber.org/protocol/chatstates' )
				else:
					if len(self.roster['users'][JID.userhost()].resources)>0:
						if self.roster['users'][JID.userhost()].resources[self.roster['users'][JID.userhost()].getHighestResource()].hasFeature('http://jabber.org/protocol/chatstates'):
							message.addElement(composing, 'http://jabber.org/protocol/chatstates' )
		if len(message.children) == 0:
			return
#		self.on_xml(message.toXml())
		self.xmlstream.send(message)


	def sendInvitation(self, jid, room, reason = None):
		message = Element((None,'message'))
		message['to'] = room
		x = message.addElement('x','http://jabber.org/protocol/muc#user')
		invite =  x.addElement('invite') 
		invite['to'] = unicode(jid)
		if reason != None:
			invite.addElement("reason", content = unicode(reason))

#		self.on_xml(message.toXml())
		self.xmlstream.send(message)


	def declineInvitation(self, jid, room, reason = None):
		message = Element((None,'message'))
		message['to'] = room
		x = message.addElement('x','http://jabber.org/protocol/muc#user')
		decline =  x.addElement('decline') 
		decline['to'] = unicode(jid)
		if reason != None:
			decline.addElement("reason", content = unicode(reason))

#		self.on_xml(message.toXml())
		self.xmlstream.send(message)


	def getRoster(self):
		""" Posle zadost o roster na server """
		log.msg('get roster')
		iq = IQ(self.xmlstream, 'get')
		iq['type'] = 'get'
		q = iq.addElement('query')
		q['xmlns']='jabber:iq:roster'
		self.disp(iq['id'])
		d = iq.send()
#		self.on_xml(iq.toXml())
		d.addCallback(self._onRosterArrive).addErrback(self.chyba)
	
	def getMUCConfig(self, jid, callback = None):
		""" Posle zadost o registracni formular na dany jid """
		log.msg('get muc config')
		iq = IQ(self.xmlstream, 'get')
		iq['type'] = 'get'
		iq['to'] = jid
		q = iq.addElement('query')
		q['xmlns']='http://jabber.org/protocol/muc#owner'
		self.disp(iq['id'])
		d = iq.send()
#		self.on_xml(iq.toXml())
		d.addCallback(self._onMUCConfigReceived, callback, jid).addErrback(self.chyba)
		return d
		
	def setMUCConfig(self, jid, forms):
		""" Posle zadost o registracni formular na dany jid """
		log.msg('set muc config')
		iq = IQ(self.xmlstream, 'set')
		iq['type'] = 'set'
		iq['to'] = jid
		q = iq.addElement('query')
		q['xmlns']='http://jabber.org/protocol/muc#owner'
		x = q.addChild(forms)
		x['type'] = 'submit'
		self.disp(iq['id'])
		d = iq.send()
#		self.on_xml(iq.toXml())
		return d
	
	def getRegisterForm(self, jid, callback = None):
		""" Posle zadost o registracni formular na dany jid """
		log.msg('get reg form')
		iq = IQ(self.xmlstream, 'get')
		iq['type'] = 'get'
		iq['to'] = jid
		q = iq.addElement('query')
		q['xmlns']='jabber:iq:register'
		self.disp(iq['id'])
		d = iq.send()
#		self.on_xml(iq.toXml())
		d.addCallback(self._onRegisterGet, callback, jid).addErrback(self.chyba)
		return d
	
	def setRegisterForm(self, jid, legacy=None, forms = None, remove = False):
		log.msg('set reg form')
		iq = IQ(self.xmlstream, 'set')
		iq['type'] = 'set'
		iq['to'] = jid
		q = iq.addElement('query')
		q['xmlns']='jabber:iq:register'
		if remove:
			q.addElement('remove')
		else:
			if legacy != None:
				for k,v in legacy.iteritems():
					if k == 'instructions':
						continue
					q.addElement(k, content = v)
			elif forms != None:
				x = q.addChild(forms)
				x['type'] = 'submit'
			else:
				return False
		self.disp(iq['id'])
		d = iq.send()
#		self.on_xml(iq.toXml())
		return d

	def getSearchForm(self, jid):
		""" Posle zadost o formular pro hledani na dany jid """
		log.msg('get reg form')
		iq = IQ(self.xmlstream, 'get')
		iq['type'] = 'get'
		iq['to'] = jid
		q = iq.addElement('query')
		q['xmlns']='jabber:iq:search'
		self.disp(iq['id'])
		d = iq.send()
#		self.on_xml(iq.toXml())
		d.addCallback(self._onSearchGet, jid).addErrback(self.chyba)
		return d
	
	def setSearchForm(self, jid, legacy=None, forms = None):
		log.msg('set search form')
		iq = IQ(self.xmlstream, 'set')
		iq['type'] = 'set'
		iq['to'] = jid
		q = iq.addElement('query')
		q['xmlns']='jabber:iq:search'
		if legacy != None:
			for k,v in legacy.iteritems():
				if k == 'instructions':
					continue
				q.addElement('k', content = v)
		elif forms != None:
			x = q.addChild(forms)
			x['type'] = 'submit'
		else:
			return False
		self.disp(iq['id'])
		d = iq.send()
#		self.on_xml(iq.toXml())
		return d.addCallback(self._onSearchResult, jid)	
		
	def sendRosterUpdate(self, jid, name, subscription, groups, callback=None, params=None):
		""" Zmeni zaznam v rosteru o zadanem JIDu """
		#print jid, name, subscription, groups
		iq = IQ(self.xmlstream, 'get')
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
		d = iq.send()
#		self.on_xml(iq.toXml())
		d.addCallback(self._rosterUpdateDone, callback, params).addErrback(self.chyba)
	
	def getVCard(self, jid):
		""" Posle zadost o vcard """
		log.msg( 'requesting vcard for ' + unicode(jid))
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		iq.addElement('vCard', 'vcard-temp')
		self.disp(iq['id'])
		iq.timeout = 60
		log.msg("Sending VCARD IQ")
		d = iq.send()
		log.msg("XML LOG")
#		self.on_xml(iq.toXml())
		log.msg("ADDING: callback")
		d.addCallback(self._vcardReceived).addErrback(self._noVcard, jid)
		log.msg("END: getVCard")
		
	def getBookmarks(self):
		log.msg('get bookmarks')
		iq = IQ(self.xmlstream, 'get')
		q = iq.addElement('query', 'jabber:iq:private')
		q.addElement('storage', 'storage:bookmarks')
#		self.on_xml(iq.toXml())
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
#		self.on_xml(iq.toXml())
		d = iq.send()
		d.addCallback(self._bookmarksSet).addErrback(self.chyba)
		

	def getMetacontacts(self):
		log.msg('get meta contacts')
		iq = IQ(self.xmlstream, 'get')
		q = iq.addElement('query', 'jabber:iq:private')
		q.addElement('storage', 'storage:metacontacts')
#		self.on_xml(iq.toXml())
		self.disp(iq['id'])
		d = iq.send()
		d.addCallback(self._metacontactsReceived)
		d.addErrback(self._metacontactsErrReceived)

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
#		self.on_xml(iq.toXml())
		d = iq.send()
		d.addCallback(self._metacontactsSet).addErrback(self.chyba)
	
	def delContact(self, jid):
		self.sendRosterUpdate(jid, '', 'remove', [])
		if self.roster_meta.has_key(jid):
			del self.roster_meta[jid]
			self.setMetacontacts()

	def getFeatures(self, jid, caps_node = None):
		log.msg('requesting features'+ caps_node)
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid.full()
		iq['from'] = self.jid.full()
		q = iq.addElement('query', 'http://jabber.org/protocol/disco#info')
		if caps_node != None:
			q['node'] = caps_node
			log.msg("CAPS:"+caps_node)
#		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._featuresReceived, caps_node).addErrback(self.chyba)

	def getVersion(self, jid):
		log.msg('requesting version info')
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		q = iq.addElement('query', 'jabber:iq:version')
#		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._versionReceived).addErrback(self.chyba)

	def getDiscoInfo(self, jid, node = None,  callback = None, callback_par = None):
		log.msg( 'requesting disco#info: '+jid)
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		iq['from'] = self.jid.full()
		q = iq.addElement('query', 'http://jabber.org/protocol/disco#info')
		if node != None:
			q['node'] = node
#		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._discoInfoReceived, node,  callback, callback_par)
		d.addErrback(self._discoInfoErrReceived, (node, jid))
		
	def getDiscoItems(self, jid, node = None, callback = None, callback_par = None):
		log.msg('requesting disco#items ')
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		iq['from'] = self.jid.full()
		q = iq.addElement('query', 'http://jabber.org/protocol/disco#items')
		if node != None:
			q['node'] = node
#		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._discoItemsReceived, node, callback, callback_par)
		d.addErrback(self._discoItemsErrReceived, (node, jid))
		
	def getTime202(self, jid):
		log.msg( 'requesting time202 info')
		iq = IQ(self.xmlstream, 'get')
		iq['to'] = jid
		iq.addElement('time','urn:xmpp:time')
#		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._time202Received).addErrback(self.chyba)
		
	def joinGC(self,  jid, nick):
		gc = Groupchat(self,  jid, nick)
		self.groupchats[jid] = gc
		gc.join()


	def leaveGC(self,  jid):
		self.groupchats[jid] .leave()
		del self.groupchats[jid]
		log.msg( 'left MUC: '+ jid)
############## MUC admin ##################
	def getMUCList(self, jid, typ = 'voice'):
		log.msg('get muc list')

		iq = IQ(self.xmlstream, 'get')
		iq['type'] = 'get'
		iq['to'] = jid
		q = iq.addElement('query')
		q['xmlns']='http://jabber.org/protocol/muc#admin'
		item = q.addElement('item')
		item[MUCLISTTYPES[typ][2]] = MUCLISTTYPES[typ][1]
		self.disp(iq['id'])
		d = iq.send()
#		self.on_xml(iq.toXml())
		d.addCallback(self._onMUCListGet, jid).addErrback(self.chyba)
		return d
	
	def setMUCList(self, jid, items, typ, remove = False):

		iq = IQ(self.xmlstream, 'get')
		iq['type'] = 'set'
		iq['to'] = jid
		q = iq.addElement('query')
		q['xmlns']='http://jabber.org/protocol/muc#admin'
		for item in items.itervalues():
			itm = q.addElement('item')
			if item.has_key('reason') and item['reason'].strip() != '':
				itm.addElement('reason', content = item['reason'])
			del item['reason']
			itm.attributes = item
		self.disp(iq['id'])
		d = iq.send()
#		self.on_xml(iq.toXml())
		return d
	
	def getMUCLists(self, jid, types = ['ban', 'member', 'admin', 'owner']):
		seznam = []
		for typ in types:
			seznam.append(self.getMUCList(jid, typ))
		
		
		dl = defer.DeferredList(seznam).addCallback(self._onMUCLists, jid, types)
		return dl
