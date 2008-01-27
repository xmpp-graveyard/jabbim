#-*-coding:UTF-8-*-
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
import sys, time, random, os
import socks5, events, base64
from twisted import names
from twisted.python import log
from twisted.internet import protocol, error
from twisted.names import client as dns
from socket import getaddrinfo
import socket
from twisted.internet import threads
from twisted.words.protocols import jabber
from twisted.words.protocols.jabber import client,jid
from twisted.words.xish import domish
from twisted.words.xish.domish import Element
##from twisted.internet import reactor, address
from twisted.words.protocols.jabber.xmlstream import IQ, TimeoutError
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.protocols import socks
from twisted.internet.task import LoopingCall

from derived import derived
from contact import *
from groupchat import  *
from base64 import b64encode, b64decode
from privacy import *
from adhoc import *
import rc
#from bosh import client as bclient
#import bosh_wokkel
try:
	from hashlib import sha1
except:
	log.msg('Please upgrade to python2.5')
	from sha import new as sha1

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
	def __init__(self, JID, password, host, port, main,  reactor = None, SSL = True):
		#derived.__init__(self)
		self. reactor = reactor
		self.jid = jid.JID(JID)
		self.password  = password
		self.host = self.jid.host
		self.port = port
		self.factory = None
		self.connection = None
		self.main=main # mainWindow
		self.ssl = SSL
		self.lastxml=10
		self.roster = {'users':{},'groups':{}}
		self.roster_meta = {} # jid: {'tag':tag,  'order': 1}
		self.first_presence = []
		self.first_wait = True
		self.bookmarks = {'conference':{}, 'url': {}}
		self.idlist = []
		self.disco = {} # jid:{node1:{items:{attrs}, identity: {attrs}, features:[], err: {'info':'', 'items':''}}}
		self.groupchats = {} # jid:Groupchat
		self.privacy = Privacy(self.main)
		self.client_name = 'Jabbim'
		self.version = '0.4SVN' # tohle asi neni nejlepsi zpusob
		self.client_os = ''
		self.caps_node = 'http://dev.jabbim.cz/jabbim/caps'
		self.caps_version = self.version
		
		self.discofeatures = {} # node: [feature1, feature2]
		self.discoitems = {None:[],"http://jabber.org/protocol/commands":[]}
		self.ft_proxies = {
		'proxy.netlab.cz':["77.48.19.1", "7777"] 
		}
		self.ft = {}
		self.last = 0
		self.registerFeature('jabber:iq:version')
		self.registerFeature('jabber:iq:last')
		self.registerFeature('http://jabber.org/protocol/xhtml-im')
		self.registerFeature('http://jabber.org/protocol/disco#info')
		self.registerFeature('urn:xmpp:time')
		self.registerFeature('urn:xmpp:ping')
		self.registerFeature('jabber:iq:time')
		self.registerFeature('http://jabber.org/protocol/chatstates')
		self.registerFeature('http://jabber.org/protocol/commands')
		self.registerFeature('http://kopete.kde.org/protocol/file-preview')
		self.registerFeature('http://jabber.org/protocol/bytestreams')
		self.registerFeature('http://jabber.org/protocol/ibb')
		self.registerFeature('http://jabber.org/protocol/bytestreams#udp')
		self.registerFeature('http://jabber.org/protocol/disco#info', 'http://jabber.org/protocol/commands', identity={"category":"automation","type":"command-list", "name":self.main.tr("Extra actions")})
		self.registerFeature('jabber:x:data', 'http://jabber.org/protocol/commands')
		self.registerFeature('http://jabber.org/protocol/commands','http://jabber.org/protocol/commands')
		
		self.caps_cache = {} # 'node': [feature1, feature2]
		features = []
		for f in self.discofeatures[None]:
			features.append(f[0])
		self.caps_ext = self.calcCapsExt(features = features)
 		self.cacheCaps(self.caps_ext, features)
		self.evil = False
		self.log = True
		self.xmlLang = 'cs'
		self.dispatcher = events.EventDispatcher()
		self.avatars = {} # jid:hash
		path = self.main.homeDir+'/avatars/'
		for jd in os.listdir(path):
			fd = open(path+jd, 'rb')
			hash = sha1(fd.read()).hexdigest()
			fd.close()
			self.avatars[jd] = hash
		self.reactor.callFromThread(self.on_init)
		self.main.cache.get_caps().addCallback(self._cacheCaps)
		self.dispatcher.registerHandler('on_message', self.on_message, 'on_message')
		self.dispatcher.registerHandler('on_presence', self.on_presence, 'on_presence')
		self.dispatcher.registerHandler('on_GCpresence', self.on_GCpresence, 'on_GCpresence')
		self.dispatcher.registerHandler('on_authd', self.on_authd, 'on_authd')
		self.xping = LoopingCall(self.heartbeat)
		
	def chyba(self, err):
		err.printBriefTraceback()
	
	def cacheCaps(self, ext, features):
		self.caps_cache[ext] = features
		self.main.cache.set_caps(ext, features)

	def _cacheCaps(self, result):
		for line in result:
			self.caps_cache[line[0]] = line[1]
			

	def heartbeat(self):
		log.msg('heartbeat')
		iq = IQ(self.xmlstream, 'get')
		iq['xml:lang'] = self.xmlLang
		q = iq.addElement('ping', 'urn:xmpp:ping')
		self.disp(iq['id'])
		iq.timeout = 60
		d = iq.send()
		d.addCallback(self._heartbeat)
		d.addErrback(self._heartbeatErr)
		return d
	
	def _heartbeat(self, el):
		log.msg('heartbeat ok')
	
	def _heartbeatErr(self, err):
		if err.type == TimeoutError:
			log.msg('heartbeat failed')
			self.xping.stop()
#			if self.factory:
#				self.factory.stopTrying()
			self.connectionLost(self.connection)


	def connect(self, host = None, port = '5222'):
		if host != None:
			self._connect(host, int(port))
		else:
			log.msg('dns - ' + unicode(time.time()) + '_xmpp-client._tcp.'+self.jid.host)
			if sys.platform == 'win32':
				import IPConfig
				srv = IPConfig.IPConfig().get_dns()
				dnssrv = []
				for server in srv:
					if len(server.strip())>0:
						dnssrv.append((server, 53))
				if len(dnssrv) > 0:
					r = dns.Resolver(servers=dnssrv)
					d = r.lookupService('_xmpp-client._tcp.'+self.jid.host, timeout = [2,10])
				else:
					log.msg('using root resolver')
					d = dns.lookupService('_xmpp-client._tcp.'+self.jid.host, timeout = [2,10])
			else:
				d = dns.lookupService('_xmpp-client._tcp.'+self.jid.host, timeout = [2,10])
			d.addCallback(self._dnsLookup)
			d.addErrback(self._dnsLookupErr)
	
	def _dnsLookup(self, resp):

		r = random.choice(resp[0])
		self._connect(unicode(r.payload.target), int(r.payload.port))
#		self._connect(unicode(r[4][0]), int(r[4][1]))
	
	def _dnsLookupErr(self, resp):
		print 'err:', resp
		print dir(resp)
		self._connect(self.host, self.port)
		#self._connect('talk.google.com', self.port)

				
	def _connect(self, host, port): 
		
		self.factory = client.XMPPClientFactory(self.jid,self.password)
#		self.factory = bclient.BOSHClientFactory(self.jid, self.password, 'http://soumar.jabbim.cz:5280/http-bind', bosh_attrs = {"wait": "100"})
		self.factory.addBootstrap('//event/stream/authd',self._authd)
##		self.factory.addBootstrap("//event/client/basicauth/invaliduser", self._invaliduser)
##		self.factory.addBootstrap("//event/client/basicauth/authfailed", self._authfailed)
		self.factory.addBootstrap("//event/xmpp/initfailed", self._authfailed)
		self.factory.addBootstrap('/iq[@type="result"]/bind', self._bind)
		self.factory.addBootstrap('//event/stream/error', self._streamEnd)
		self.factory.addBootstrap('/*', self.bootLog)
		
		self.factory.clientConnectionLost = self.connectionLost
		self.factory.clientConnectionFailed = self.connectionFailed
		self.connection = self.reactor.connectTCP(host,port,self.factory)
		print host,port
#		self.connection = self.reactor.connectTCP('soumar.jabbim.cz',5280,self.factory)
		self.on_connect()
#		print dir(self.factory)
#		p = self.factory.buildProtocol('tcp:localhost:8080')
#		print dir(p)
#		self.connection = self.reactor.connectTCP('conn443.netlab.cz',443,self.factory)
#		def stf(prt):
#			print 'conn: ', prt
#			
#		sfact = socks.SOCKSv4Factory('./socks.log')
#		sfact.startedConnecting = stf
#		sck = self.reactor.connectTCP('localhost', 1080, sfact )
#		print dir(sck)
#		
#		self.connection = sfact.buildProtocol('f').connectClass(host, port, client.XMPPClientFactory, self.jid,self.password)
		log.msg('started - ' + unicode(time.time()))
	
	def bootLog(self, el):
		if self.log:
			self.on_xml(u'BOOT: ' + el.toXml())
			
	def connectionLost(self, connector, reason=protocol.connectionDone):
		log.msg('connection lost!')
		if self.factory:
			self.factory.stopTrying()
		self.connection = None
		self.factory = None
		self.main._disconnect(error = 'lost')

		self.on_disconnect()
	
	def connectionFailed(self, connector, reason=protocol.connectionDone):
		log.msg('connection failed!')
		self.main._disconnect(error = 'failed')
		self.on_disconnect()

	def _streamEnd(self, el):
		self.xping.stop()
		pass
		
	def _bind(self, el):
		#experimental
		log.msg('bind')
		bind = el.firstChildElement()
		jd = bind.firstChildElement().__str__()
		self.jid = jid.JID(jd)
		
	def disconnect(self):
		if self.connection:
			self.connection.disconnect()
		if self.factory:
			self.factory.stopTrying()
		self.connection = None
		self.factory = None
		self.on_disconnect()

	def _authd(self, xmlstream):
		log.msg('authed')
##		self.dispatcher.publishEvent('authed')
		self.xmlstream = xmlstream
		self.xmlstream.removeObserver('/*', self.bootLog)
		self.xmlstream.rawDataInFn = self.rawDataIn
		self.xmlstream.rawDataOutFn = self.rawDataOut
		self.xmlstream.addObserver("/presence", self.onPresence, 1)
		self.xmlstream.addObserver("/message", self.onMessage, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/query[@xmlns='jabber:iq:roster']", self.onRosterAdd, 1)
		self.xmlstream.addObserver("/*", self.onXML)
		self.xmlstream.addObserver("/presence[@type='subscribe']", self.onSubscribe, 1)
		self.xmlstream.addObserver("/presence[@type='unsubscribe']", self.onUnSubscribe, 1)
		self.xmlstream.addObserver("/presence[@type='subscribed']", self.onSubscribed, 1)
		self.xmlstream.addObserver("/presence[@type='unsubscribed']", self.onUnSubscribed, 1)
		self.xmlstream.addObserver("/presence[@type='error']", self.onPresenceError, 1)
		#self.xmlstream.addObserver("/presence[@type='unavailable']", self.onUnavailable, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='jabber:iq:version']", self.onVersion, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='http://jabber.org/protocol/disco#info']", self.onDiscoInfo, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='http://jabber.org/protocol/disco#items']", self.onDiscoItems, 1) 
		self.xmlstream.addObserver("/iq[@type='set'][@id]/command[@xmlns='http://jabber.org/protocol/commands'][@node]", self.onCommand, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='jabber:iq:last']", self.onLast, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/time[@xmlns='urn:xmpp:time']", self.onTime202, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='jabber:iq:time']", self.onTime90, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/si[@xmlns='http://jabber.org/protocol/si' ][ @profile='http://jabber.org/protocol/si/profile/file-transfer']", self.onFileReceive, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/query[@xmlns='http://jabber.org/protocol/bytestreams']/streamhost", self.onStreamhosts, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/open[@xmlns='http://jabber.org/protocol/ibb']", self.onIBBStart, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/close[@xmlns='http://jabber.org/protocol/ibb']", self.onIBBEnd, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/data[@xmlns='http://jabber.org/protocol/ibb']", self.onIBBData, 1)
		self.xmlstream.addObserver("/message/data[@xmlns='http://jabber.org/protocol/ibb']", self.onIBBData, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/confirm[@xmlns='http://jabber.org/protocol/http-auth']", self.onVerify, 1)
		self.xmlstream.addObserver("/message/confirm[@xmlns='http://jabber.org/protocol/http-auth']", self.onVerify, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/ping[@xmlns='urn:xmpp:ping']", self.onPing, 1)
		self.xmlstream.addObserver("/message/x[@xmlns='http://jabber.org/protocol/muc#user']/invite", self.onInvite, 1)
		self.xmlstream.addObserver("/*/evil[@xmlns='http://jabber.org/protocol/evil']", self.onEvil, 1)
	
		self.xping.start(120, False)		
		self.getMetacontacts()
		self.getBookmarks()
		self.getDiscoInfo(self.jid.host)#,  callback = self._pepSupport)
		self.getDiscoItems(self.jid.host, callback = self._gotServices)
		self.getPrivacy()
#		self.reactor.callFromThread(self.on_authd)
		self.dispatcher.publishEvent('on_authd')
		self.main._connected()
		print 'pre commands'
		self.commands = Commands(self.main)
		self.commands.registerNode("http://jabber.org/protocol/rc#set-status", self.main.tr("Change status"), rc.fSetStatus)
		self.commands.registerNode("http://jabber.org/protocol/rc#leave-groupchats", self.main.tr("Leave groupchats"), rc.fLeaveGC)
		self.commands.registerNode("http://dev.jabbim.cz/jabbim/rc#resend-file", self.main.tr("Resend file"), rc.ResendFile)
#		print 'post commands'
		def pis(co):
			print co
		self.callRemote('rpc@jabbim.cz/service', 'getFile', ('smileys/white.zip',)).addCallback(pis)


	def _gotServices(self, res):
		for jid in self.disco[self.jid.host][None]['items'].iterkeys():
			self.getDiscoInfo(jid)
			print jid
		
	def _pepSupport(self):
		log.msg('pep support arrived')
		for key,  val in self.disco[self.jid.host][None]['identities'].iteritems():
			log.msg(key+ unicode(val))
			if val['type'] == 'pep' :
				log.msg( 'we got a PEP support')
				self.pep = True
				self.registerFeature('http://jabber.org/protocol/tune')
				self.registerFeature('http://jabber.org/protocol/tune+notify')
	
	def sendPEP(self,  typ,  attrs):
		iq = IQ(self.xmlstream, 'set')
		pb = iq.addElement('pubsub', 'http://jabber.org/protocol/pubsub' ).addElement('publish')
		pb['node'] = 'http://jabber.org/protocol/' + typ
		tune = pb.addElement('item').addElement(typ, 'http://jabber.org/protocol/' + typ)
		for key, val in attrs.iteritems():
			tune.addElement(key,  content = val)
#		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._pepReceived).addErrback(self.chyba)

	def _pepReceived(self,  el):
		log.msg(el.toXml())
	
	def registerPEP(self,  to,  typ): #typ = tune|mood|activity
		iq = IQ(self.xmlstream, 'set')
		iq['to'] = to
		sb = iq.addElement('pubsub',  'http://jabber.org/protocol/pubsub').addElement('subscribe')
		sb['jid'] = self.jid.userhost()
		sb['node'] ='http://jabber.org/protocol/'+typ
#		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._pepReceived).addErrback(self.chyba)

	def registerFeature(self, feature, node = None, identity = None):#{"category":None,"type":None,"name":None}):
		if self.discofeatures.has_key(node):
			self.discofeatures[node].append((feature,))
		else:
			self.discofeatures[node] = []
			self.discofeatures[node].append((feature, identity))

	#def registerItem(self, jid = None, name = None, node = None, parentnode = None):
	#	log.msg("registering disco#item")
	#	if jid == None:
	#		jid = self.jid.full()
	#	self.discoitems[parentnode].append({"jid":jid,"name":name,"node":node})


	def onRosterAdd(self,el):
		log.msg("roster item add")
		self.disp(el['id'])
		#log.msg(el.toXml())
		for child in el.elements():
			if child.name == "query":
				allGroups=[]
				#for k,v in self.roster['groups'].iteritems():
					#allGroups.append(k)
				for item in child.elements():
					groups = []
					itemjid = item['jid']
					for group in item.elements():
						if group.name == 'group':
							groups.append(unicode(group))
							#if unicode(group) not in allGroups:
								# add group item to ther roster
								#self.roster['groups'][unicode(group)] = self.reactor.callFromThread(self.main._addGroup, group)
								#allGroups.append(unicode(group))
					if item.hasAttribute('name'):
						name = item['name']
					else:
						name = ''
					subscription = ''
					if item.hasAttribute('ask'):
						ask = item['ask']
					else:
						ask = None
					if item.hasAttribute('subscription'):
						subscription = item['subscription']
					if subscription == 'remove'  and self.roster['users'].has_key(itemjid):
						log.msg('deleting contact')
						self.reactor.callFromThread(self.on_DeleteContact,itemjid)
						del self.roster['users'][itemjid]
					elif not self.roster['users'].has_key(itemjid) and subscription != 'remove':
						log.msg(subscription)
						rosterItems=[]
						#if len(groups)==0:
							# add user item to Unknown group
						contact = Contact(self, itemjid, name, subscription, rosterItems, groups, ask = ask)
						self.roster['users'][itemjid] = contact
						self.reactor.callFromThread(self.on_rosterAddUser,contact)
							#rosterItems.append(self.main._addUser(itemjid,name,self.roster['groups']['Unknown']))
						#for group in groups:
							#self.on_rosterAddUser(contact)
							# add user item to the group
							#rosterItems.append(self.main._addUser(itemjid,name,self.roster['groups'][group]))
						
					elif subscription != 'remove'  and self.roster['users'].has_key(itemjid):
						contact = self.roster['users'][itemjid]
						contact.name = name
						contact.groups = groups
						self.reactor.callFromThread(self.on_UpdateContact,itemjid)
		iq = Element((None, 'iq'))
		iq['from'] = self.jid.full()
		iq['to'] = self.jid.host
		iq['id'] = el['id']
		iq['type'] = 'result'
#		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)


		
	def _rosterUpdateDone(self, el, callback, params):
		if callback != None:
			self.reactor.callFromThread(callback, params)




	def _noVcard(self, err, jid): 
		print jid, 'no vcard available' 
		log.msg('chci ulozit ' + jid )
#		self.reactor.callFromThread(self.main.cache.set_avatar,jid, ['nic', 'nic'])
		self.avatars[jid] = None
		self.on_avatarUpdate(jid)

	def _vcardReceived(self, el):
		log.msg('vcard received')
		vcard = el.firstChildElement()
		card = {} 
		if vcard == None :
			return
		for x in vcard.elements():
			pref = ''

			if len(x.children)>0:
				pref = x.name + '-'
				got=False
				for y in x.elements():
					got=True
					card[pref + y.name]=unicode(y)
				if not got:
					card[x.name]=unicode(x)
			else:
				card[x.name]=unicode(x)
				
		if card.has_key("PHOTO-BINVAL"):
			image=base64.decodestring(str(card["PHOTO-BINVAL"]))
			f=open(self.main.homeDir+'/avatars/'+unicode(el['from']).replace('/', '%'),"wb")

			f.write(image)
			f.close()

			self.avatars[el['from'].replace("/","%")] = sha1(image).hexdigest()
			#try:
			self.on_avatarUpdate(el['from'])
			#except:
				#print 'chyba v updatu avatara'
		else:
			self.avatars[el['from']] = None
		self.reactor.callFromThread(self.on_vcardReceived,el['from'], vcard)
		return vcard



	def _bookmarksSet(self, el):
		log.msg('bookmarks set sucessfully')

	def _bookmarksErrReceived(self, err):
		self.on_bookmarksFail()
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


	def _metacontactsSet(self,  el):
		log.msg( 'metacontacts set')

	def addContact(self, jid, msg, name='', groups=[]):
		log.msg( 'add contact')
		self.sendRosterUpdate(jid, name, 'none', groups, self._contactAdded, params = {'msg':msg, 'jid':jid})
	
	def _contactAdded(self, params):
		self.sendPresence(to = params['jid'], status = params['msg'], typ = 'subscribe')



	def onXML(self, el):
		if not el.hasAttribute('from'):
			print el.toXml()
			return
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
#				self.on_xml(el.toXml())
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
#			self.on_xml(el.toXml())
			self.xmlstream.send(el)
	
#	def logIt(self, el):
#		if self.log:
#			self.on_xml(el.toXml())
	def rawDataIn(self, buf):
		if self.log:
			try:
				self.on_xml(u'IN: ' + unicode(buf, 'utf8', 'replace'))
			except:
				self.on_xml(u'IN: ' + buf)
	
	def rawDataOut(self, buf):
		if self.log:
			try:
				self.on_xml(u'OUT: ' + unicode(buf, 'utf8', 'replace'))
			except:
				self.on_xml(u'OUT: ' + buf)
			
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
					if item.hasAttribute('ask'):
						ask = item['ask']
					else:
						ask = None
					#print "PYXL ASK:",ask
					#print item['jid'],groups
					tag = None
					order = 1
					if self.roster_meta.has_key(item['jid']):
						tag = self.roster_meta[item['jid']]['tag']
						order = self.roster_meta[item['jid']]['order']
					contact = Contact(self, item['jid'], name, item['subscription'], [], groups, tag =  tag, order =  order, ask = ask)
					self.roster['users'][item['jid']] = contact
					self.reactor.callFromThread(self.on_rosterAddUser,contact)
		
		self.roster['users'][self.jid.userhost()] = Contact(self, self.jid.userhost(), self.jid.user, 'both', [], [])
		
		log.msg( 'roster arrived')
		self.sendPresence()
		cekej = 20
		if ln*0.05 < cekej:
			cekej = ln*0.05
		self.reactor.callFromThread(self.on_rosterArrived)
		self.reactor.callLater(cekej,  self.onFirstPresence)




	def _authfailed(self,xmlstream):
		log.msg( "auth_failed")
		print unicode(xmlstream)
		self.main._disconnect(error = 'auth')
		self.on_authFailed(xmlstream)

	def _invaliduser(self,xmlstream):
		log.msg( "invalid_user")
		#self.on_invalidUser(self)

	def onMessage(self, el):
		log.msg( 'message received')
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
		body = subject =xhtml = chatstate = delay = error =  None
		for child in el.elements():
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
#				xbdy = ''
#				for elm in xbody.elements():
#					xbdy = xbdy + elm.toXml()
#				log.msg(xbdy)
#				if len(xbdy) == 0:
#					xhtml = unicode(xbody)
#				else:
#					xhtml = xbdy
				xbody.attributes = {}
				del(xbody.defaultUri)
				del(xbody.uri)
				xhtml = xbody.toXml().replace('<body>','').replace('</body>', '')
			if child.name in ['active',  'inactive',  'composing',  'paused',  'gone']:
				chatstate = child.name
				try:
					if not 'http://jabber.org/protocol/chatstates' in self.roster['users'][frmjid.userhost()].resources[frmjid.resource].features:
						self.roster['users'][frmjid.userhost()].resources[frmjid.resource].features.append('http://jabber.org/protocol/chatstates')
				except:
					pass #proste user neni v rosteru, nebo je to muc, nebo cojavim ;)
			if child.name == 'delay':
				delay = child['stamp']
			if child.name == 'x':
				if child.defaultUri == 'jabber:x:delay' :
					delay = child.getAttribute('stamp')
				if child.defaultUri == 'jabber:x:event':
					elm = child.firstChildElement()
					if elm:
						chatstate = elm.name
				if child.defaultUri == 'http://jabber.org/protocol/muc#user': # invitation
					return
			if child.name == 'confirm': # xep0070 - processed elsewhere
				return

		if self.groupchats.has_key(jid.JID(frm).userhost()):
			self.on_GCmessage(frm,typ,body,subject, xhtml,  chatstate,  delay)
			self.dispatcher.publishEvent('on_GCmessage', frm,typ,body,subject, xhtml,  chatstate,  delay, error)
		else:
# 			self.on_message(frm,typ,body,subject, xhtml,  chatstate,  delay)
			if typ!="groupchat":
				self.dispatcher.publishEvent('on_message', frm,typ,body,subject, xhtml,  chatstate,  delay, error)

	def onInvite(self, el):
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
		self.on_invite(jid, room, reason, cont)
#		self.main.showInvitation(jid, room, reason, cont)

	def onSubscribe(self, el):
		log.msg( 'on subscribe')
		status = ''
		for child in el.elements():
			if child.name == 'status':
				status = unicode(child)
		self.on_subscribe(el['from'], status)

	def onUnavailable(self, el):
		log.msg( 'on subscribed')
		self.on_unavailable(el['from'])

	def onSubscribed(self, el):
		log.msg( 'on subscribed')
		self.on_subscribed(el['from'])

	def onUnSubscribe(self, el):
		log.msg('on unsubscribe')
		self.on_unsubscribe(el['from'])

	def onUnSubscribed(self, el):
		log.msg( 'on unsubscribed')
##		self.sendRosterUpdate(jid, '', 'remove', [])
		self.on_unsubscribed(el['from'])	

	
	def onFirstPresence(self):
		log.msg( 'first presences')
		self.first_wait = False
		self.reactor.callFromThread(self.on_firstpresence, self.first_presence)
		self.dispatcher.publishEvent('first presence')
	
	def onPresence(self, el):
		#log.msg('presence > ')
		frm = jid.JID(el['from'])
		fromjid = frm.userhost()
		resource = frm.resource
		print "PRESENCE"
		show = status = priority = nick = typ = affiliation = role = truejid = hash = error = reason = actor = None
		codes = []
		if el.hasAttribute('type'):
		#	if el['type'] != 'unavailable':
		#		return
		#	else:
		#		typ = 'unavailable'
			typ = el['type']
		if typ == 'error':
			error = 'error'
		features = []
		for child in el.elements():
			if child.name == 'error':
				error = 'error'
				for x in child.elements():
					if x.name != 'text':
						error = x.name
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
				caps_node = child.getAttribute('node')

				ext = child.getAttribute('ext')
				if self.caps_cache.has_key(ext):
					features = self.caps_cache[ext]
				else:	
					if typ !='unavailable':
						self.getFeatures(frm, ext)
			if child.name == 'x' and child.defaultUri == 'http://jabber.org/protocol/muc#user':
				for item in child.elements():
					if item.name == 'item':
						affiliation = item['affiliation']
						role = item['role']
						if item.hasAttribute('nick'):
							nick=unicode(item['nick'])
						if item.hasAttribute('jid'):
							truejid = item['jid']
						for itm in item.elements():
							if itm.name == 'reason':
								reason = unicode(itm)
							elif itm.name == 'actor':
								actor = itm.getAttribute('jid')
						print reason, actor
					if item.name == 'status' :
						codes.append(item['code'])
			elif child.name == 'x' and child.defaultUri == 'vcard-temp:x:update':
				hash = unicode(child.firstChildElement())
				print fromjid, hash

#avatars
		wantAvatar=True
		if self.groupchats.has_key(fromjid):
			if self.main.client.disco.has_key(frm.host):
				if self.main.client.disco[frm.host][None].has_key("identities"):
					if self.main.client.disco[frm.host][None].has_key("identities"):
						for identity,values in self.main.client.disco[frm.host][None]["identities"].iteritems():
							if values['type']=='irc':
								wantAvatar=False

		if wantAvatar:
			if self.avatars.has_key(fromjid):
				if self.avatars[fromjid] == hash:
					pass #vsechno je ok, mame spravneho avatara
				elif self.avatars[fromjid] != hash and hash != None:
					self.getVCard(fromjid)
			elif self.avatars.has_key(frm.full()):
				if self.avatars[frm.full()] == hash:
					pass #vsechno je ok, mame spravneho avatara
				elif self.avatars[frm.full()] != hash and hash != None:
					self.getVCard(frm.full())
			else:
				if self.groupchats.has_key(fromjid):
					self.getVCard(frm.full())
				else:
					self.getVCard(fromjid)
				


		if show == None and not el.hasAttribute('type'):
			show = 'online'
		elif el.hasAttribute('type'):
			if el['type'] =='unavailable':
				show = 'offline'
			else:
				return

		if self.groupchats.has_key(fromjid):
			if show=="offline":
#				self.reactor.callFromThread(self.on_GCpresence, fromjid, resource,  show,  status,  codes)
				self.dispatcher.publishEvent('on_GCpresence',fromjid, resource,  show,  status,  codes, reason, actor, nick)
			self.groupchats[fromjid].setStatus(resource,  show,  status)
			if self.groupchats[fromjid].users.has_key(resource):
				self.groupchats[fromjid].setInfo(resource,  affiliation,  role,  truejid)
				#self.groupchats[fromjid]
			if show!="offline":
#				self.reactor.callFromThread(self.on_GCpresence,fromjid, resource,  show,  status,  codes)
				self.dispatcher.publishEvent('on_GCpresence',fromjid, resource,  show,  status,  codes, reason, actor, nick)
			return

		elif self.roster['users'].has_key(fromjid):
			first = self.roster['users'][unicode(fromjid)].setStatus(resource, show,status)
			if self.roster['users'][fromjid].resources.has_key(resource):
				self.roster['users'][fromjid].setPriority(resource, priority)
				self.roster['users'][fromjid].setFeatures(resource, features)

#			chci_card = True 
#			if self.roster['users'][fromjid].avatar_hash == 'nic': 
#				chci_card = False 
#			elif hash == None and self.roster['users'][fromjid].avatar_hash !='': 
#				chci_card = False 
#				pass 
#			elif self.roster['users'][fromjid].avatar_hash == hash: 
#				## print fromjid, 'ma spravneho avatara' 
#				chci_card = False 
#				pass  
#			if chci_card :
###				print fromjid, hash, self.roster['users'][fromjid].avatar_hash 
#				self.getVCard(fromjid)

			if first and self.first_wait:
				self.first_presence.append((frm,show, error))
			else:
#				self.reactor.callFromThread(self.on_presence,frm,show, error)
				self.dispatcher.publishEvent('on_presence',frm,show, error)

		else:
##			print 'contact not in roster'
			pass

	def onPresenceError(self,  el):
		#zatim jenom GC errory .. ani nevim jestli ma smysl zachytavat i jine ..
#		self.on_xml(el.toXml())
		frm = jid.JID(el['from'])
		fromjid = frm.userhost()
		resource = jid.JID(el['from']).resource
		if self.groupchats.has_key(fromjid):
			for child in  el.elements():
				if child.name == 'error':
					for elm in child.elements():
						text = name = None
						if elm.name == 'text':
							text = unicode(elm)
						else:
							text = unicode(elm.name)
					self.on_GCpresenceError(fromjid, child.getAttribute('code'),  child.getAttribute('type'),  name, text, resource)

					self.dispatcher.publishEvent('on_GCpresenceError',child.getAttribute('code'),  child.getAttribute('type'),  name , text)
			del self.groupchats[fromjid]		


	def _featuresReceived(self, el, ext, jd):
		log.msg( 'features received')
##		self.disp(el['id'])
		features = []
		query = el.firstChildElement()
		for child in  query.elements():
			if child.name == 'feature':
				features.append(child['var'])
		self.cacheCaps(ext, features)
		frm = jid.JID(el['from'])
		resource = frm.resource
		if self.roster['users'].has_key(frm.userhost()):
			self.roster['users'][frm.userhost()].setFeatures(resource, features)
	
	def calcCapsExt(self, identity = ['client/pc'], features = []):
		identity.sort()
		features.sort()
		print identity, features
		out = '<'.join(identity) + '<' + '<'.join(features)
		out = b64encode(sha1(out).digest())
		return out
		

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
		q.addElement('os', content = self.client_os)
#		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)


		
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
		self.reactor.callFromThread(self.on_versionreceive, el['from'], (name, version, os))

	def onDiscoInfo(self, el):
		log.msg( 'received disco#info request')
		self.disp(el['id'])
		iq = Element((None,'iq'))
		iq['to'] = el['from']
		iq['type'] = 'result'
		iq['id'] = el['id']
		q = iq.addElement('query', 'http://jabber.org/protocol/disco#info')

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
		else:
			id = q.addElement('identity')
			id['category'] = 'client'
			id['name'] = self.client_name
			id['type'] = 'pc'
		for feature in self.discofeatures[node]:
			f = q.addElement('feature')
			f['var'] = feature[0]
			if len(feature) > 1:
				if type(feature[1]) == type({}):
					log.msg("FEATURESM: %s" % `feature`)
					ide = q.addElement("identity")
					for k in feature[1].keys():
						ide[k] = feature[1][k]

#		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)

	def onDiscoItems(self, el):
		log.msg( 'received disco#items request')
		log.msg("ITEMS: "+`self.discoitems`)
		self.disp(el['id'])
		iq = Element((None,'iq'))
		iq['to'] = el['from']
		iq['type'] = 'result'
		iq['id'] = el['id']
		q = iq.addElement('query', 'http://jabber.org/protocol/disco#items')
		node = None
		for child in el.elements():
			if child.name == "query":
				if child.hasAttribute("node"):
					node = child["node"]
		if node != None:
			q["node"] = node
		try:
			for item in self.discoitems[node]:
				i = q.addElement("item")
				i["jid"] = item["jid"]
				if item["name"] != None:
					i["name"] = item["name"]
				if item["node"] != None:
					i["node"] = item["node"]
		except KeyError:
			pass

		self.xmlstream.send(iq)

	def onCommand(self, el):
		self.disp(el['id'])
		log.msg("On command event")
		command = el.firstChildElement()
		node = command["node"]
		public = self.commands.nodes[node][3]
		ji = jid.JID(el['from']).userhost()
		allowed = public or (ji == self.jid.userhost())
		try:
			lang = el["xml:lang"]
		except:
			lang = None
		try:
			try:
				action = command["action"]
			except:
				action = "execute"
			sid = unicode(command["sessionid"])
			x = None
			for child in command.elements():
				if child.name == "x":
					x = child
			#x = command.firstChildElement()
			#log.msg(unicode(dir(self.commands)))
			if x == None:
				return
			if not allowed:
				raise RuntimeError("forbidden")
			self.commands.sessions[sid].execStage(
					self.commands.sessions[sid].nextstages[action],
					el["id"],
					x2dict(x),
					lang
					)
			log.msg("ok, continuing in current session")


		except KeyError, RuntimeError:
			if jid.JID(el["from"]).userhost() == self.jid.userhost() or self.commands.nodes[node][3]:
				self.commands.startSession(node, el["from"], el["id"])
				log.msg("Starting new session")
			else:
				iq = IQ(self.xmlstream, "error")
				iq["to"] = el["from"]
				iq["id"] = el["id"]
				error = iq.addElement("error")
				error["code"] = "403"
				error["type"] = "cancel"
				error.addElement("forbidden", "urn:ietf:params:xml:ns:xmpp-stanzas")
				iq.send()
				

	def onLast(self, el):
		log.msg('received last request')
		self.disp(el['id'])
		iq = Element((None,'iq'))
		iq['to'] = el['from']
		iq['type'] = 'result'
		iq['id'] = el['id']
		q = iq.addElement('query','jabber:iq:last')
		if self.last > 0:
			q['seconds'] = str(self.last)

#		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)




	def _discoInfoReceived(self, el, node,  callback,callback_par):
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
				log.msg(unicode(node))
				node['identities'][name] = child.attributes
		self.disco[frm][node_name] = node
		if self.disco[frm][node_name].has_key('err'):
			if self.disco[frm][node_name]['err'].has_key('info'):
				del self.disco[frm][node_name]['err']['info'] #timhle smazem pripadny error ktery zustal po predchozim dotazu

		self.reactor.callFromThread(self.on_discoInfoReceived, frm, node_name)
		if callback != None:
			callback(callback_par)

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

		self.reactor.callFromThread(self.on_discoInfoReceived ,jid, node_name)



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
		self.reactor.callFromThread(self.on_discoItemsReceived, frm, node_name)
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
		self.reactor.callFromThread(self.on_discoInfoReceived, jid, node_name)


	def getPrivacy(self):	
		log.msg('requesting priacy lists')
		#FIXME: predelat # Asi ok
		iq = IQ(self.xmlstream, 'get')
		q = iq.addElement('query', 'jabber:iq:privacy')
#		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._privacyReceived).addErrback(self._noPrivacy).addErrback(self.chyba)
		return d
		
	def _noPrivacy(self, err):
		log.msg('jabber:iq:privacy is unsupported here .. damned gtalk')
		self.privacy = False
		self.on_privacyFail()
		return err

	def _privacyReceived(self, el):
		self.on_privacyReceived()
		#FIXME: dodelat
		log.msg('privacy lists received')
		query = el.firstChildElement()
		lists = []
		active = None
		#default = None
		for child in query.elements():
			if child.name == "list":
				lists.append(child.attributes["name"])
			if child.name == "active":
				active = child.attributes["name"]
			#if child.name == "default":
			#	default = child.attributes["name"]
			#### active == default
		log.msg("lists: %s; active: %s" % (", ".join(lists), active))
		
		def getActive(el,name):
			log.msg("Requesting active privacy list: %s." % name)
			iq	= IQ(self.xmlstream, "get")
			query	= iq.addElement("query", "jabber:iq:privacy")
			list_	= query.addElement("list")
			list_.attributes = {"name":name}
			d	= iq.send()
#			self.on_xml(iq.toXml())
			self.disp(iq["id"])
			d.addCallback(self._activeRecieved).addErrback(self.chyba)

		if active:
		#	lists.remove(active)
			getActive(None,active)

		else: # Pokud nemame, jeden si vytvorime
			defaultlistname = "common"
			lists.append(defaultlistname)
			iq	= IQ(self.xmlstream, "set")
			query	= iq.addElement("query", "jabber:iq:privacy")
			list_	= query.addElement("list")
			list_.attributes = {"name":defaultlistname} 	 # Asi neni idealni reseni
			item	= list_.addElement("item")
			item.attributes = {"order":"0","action":"allow","type":"jid","value":self.jid.userhost()}
			d	= iq.send()
#			self.on_xml(iq.toXml())
			self.disp(iq["id"])
			log.msg("Creating new privacy list: %s." %  defaultlistname)
			d.addCallback(getActive, defaultlistname).addErrback(self.chyba)
			self.privacy.setActive(defaultlistname)
			self.privacy.setDefault(defaultlistname)

		for l in lists:
			self.privacy.lists[l] = None	# Bude nas zajimat jen active
							# Dalsi se nactou az pozdejc, jinak je to plejtvani


	def _activeRecieved(self, el):
		log.msg("Active Privacy List recieved.")
		query	= el.firstChildElement()
		list_	= query.firstChildElement()
		name	= list_.attributes["name"]
		items	= []
		for child in list_.elements():
			order	= child.attributes["order"]
			action	= child.attributes["action"]
			if child.attributes.has_key("type"):
				typ	= child.attributes["type"]
				value	= child.attributes["value"]
			else:
				typ = value = None
			stanzas = []
			for stanza in child.elements():
				stanzas.append(stanza.name)
			item = PrivacyListItem(action, order, typ, value, stanzas)
			items.append(item)
		self.privacy.active = PrivacyList(name, items, self.main)
		self.privacy.lists[name] = self.privacy.active
		self.privacy.default = self.privacy.active
		##

	def on_privacyReceived(self):
		pass

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
#		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)



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
#		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)

	def onVerify(self, el):
		sender = el['from']
		props = None
		thread = None
		typ = el.name
		id = el.getAttribute('id')
		for e in el.elements():
			if e.name == 'confirm':
				props = e.attributes
			if e.name == 'thread':
				thread = unicode(e)
		if el.name == 'iq':
			self.disp(el['id'])
		self.on_verify(id, thread, props, sender, typ)
	
	def replyVerify(self, id, thread, props, frm, typ, result = False):
		if typ=='iq' and result:
			el = Element((None,'iq'))
			el['type'] = 'result'
			el['id'] = id
		
		elif typ=='iq' and not result:
			el = Element((None,'iq'))
			el['type'] = 'error'
			el['id'] = id
			confirm = el.addElement('confirm', 'http://jabber.org/protocol/http-auth')
			confirm.attributes = props
			err = el.addElement('error')
			err['code'] = '401'
			err['type'] = 'auth'
			err.addElement('not-authorized','urn:ietf:params:xml:xmpp-stanzas')
		elif typ=='message' and result:
			el = Element((None,'message'))
			el.addElement('thread', content = thread)
			confirm = el.addElement('confirm', 'http://jabber.org/protocol/http-auth')
			confirm.attributes = props
		elif typ=='message' and not result:
			el = Element((None,'message'))
			el['type'] = 'error'
			el.addElement('thread', content = thread)
			confirm = el.addElement('confirm', 'http://jabber.org/protocol/http-auth')
			confirm.attributes = props
			err = el.addElement('error')
			err['code'] = '401'
			err['type'] = 'auth'
			err.addElement('not-authorized','urn:ietf:params:xml:xmpp-stanzas')
		el['to'] = frm
#		self.on_xml(el.toXml())
		self.xmlstream.send(el)


	def _onRegisterGet(self, el, callback, jid):
		legacy = {}
		forms = None
		query = el.firstChildElement()
		for child in query.elements():
			if child.name == 'x':
				forms = child
			else:
				legacy[child.name] = unicode(child)
		print forms
		if callback != None:
			callback(jid, legacy, forms)
		return (jid, legacy, forms)
	
	def _onSearchGet(self, el, jid):
		legacy = {}
		forms = None
		query = el.firstChildElement()
		for child in query.elements():
			if child.name == 'x':
				forms = child
			else:
				legacy[child.name] = unicode(child)
		return (jid, legacy, forms)
	
	def _onSearchResult(self, el, jid):
		legacy = {}
		forms = None
		query = el.firstChildElement()
		for child in query.elements():
			if child.name == 'x':
				forms = child
			else:
				legacy[child.name] = unicode(child)
		return (jid, legacy, forms)
				
	def _onMUCConfigReceived(self, el, callback, jid):
		forms = None
		query = el.firstChildElement()
		for child in query.elements():
			if child.name == 'x':
				forms = child
		if callback != None:
			callback(jid, forms)
		return (jid,  forms)
	
	def _onMUCListGet(self, el, jid):
		query = el.firstChildElement()
		items = {}
		for child in query.elements():
			items[child['jid']] = child.attributes
			items[child['jid']]['reason'] = unicode(child)
		return jid, items
	
	def _onMUCLists(self, results, jid, types):
		
		seznamy = {}
		for x in range(0, len(types)):
			seznamy[types[x]] = results[x][1]
		return (jid, seznamy)
		

	
	def sendFile(self, outjid, filename, fp, desc = None, preview = None, previewType = 'image/jpeg', typ = None): #typ = None/ibb/socks5
		sid = str(random.randint(1000, sys.maxint))
		
		log.msg('sending file to '+ outjid)
		iq = IQ(self.xmlstream, 'set')
		
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
		self.ft[sid] = socks5.FTSend(self, sid, filename, outjid, fp, desc, frmjid)
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
#		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._ftreplyReceived, sid).addErrback(self._ftFailed, sid)#addErrback(self.chyba)
		return sid
	
	def _ftFailed(self, err, sid):
		self.on_ftEnd(sid, 'Canceled')
	
	def _ftstreamhostquery(self, el):
		print 'proxy rika: ', el.toXml()
	
	def _ftreplyReceived(self, el, sid):
		typ = None
		si = el.firstChildElement()
		for elem in si.elements():
			if elem.name == 'feature':
				typ = unicode(elem.firstChildElement().firstChildElement().firstChildElement())
		log.msg('FT: ' + typ)
		if typ == 'http://jabber.org/protocol/ibb':
			self.ibbSend(sid)
		elif typ == 'http://jabber.org/protocol/bytestreams':
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
#			self.on_xml(iq.toXml())
			d = iq.send()
			self.disp(iq['id'])
			d.addCallback(self._ftreplyhostReceived, sid)
			d.addErrback(self._ftreplyhostErrReceived, sid)
	
	def _ftreplyhostReceived(self, el, sid):
		print el.toXml()
		q = el.firstChildElement()
		streamhost = q.firstChildElement()
		host = streamhost['jid']
		self.ft[sid].streamhost = host
		self.ft[sid].medium = time.time()
		addr = sha1("%s%s%s" % (sid, self.jid.full(), el['from'])).hexdigest()
		
		f = ClientFactory()
		f.protocol = socks5.Send

		factory = socks5.ClientFactory(self.ft_proxies[host][0], int(self.ft_proxies[host][1]),addr, 0,  f, xmpp = self, xmpp_sid = sid) 
		self.ft[sid].connector = self.reactor.connectTCP(self.ft_proxies[host][0], int(self.ft_proxies[host][1]), factory)

	def _ftreplyhostErrReceived(self, err, sid):
		print 'replyhost', err
		self.on_ftEnd(self.sid, 'replyhost error')
	
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
			elif e.name == 'feature':
				x = e.firstChildElement()
				for field in x.elements():
					if field.getAttribute('var') == 'stream-method':
						for option in field.elements():
							methods.append(unicode(option.firstChildElement()))
		sid = si['id']
		self.ft[sid] = socks5.FTReceive(self, el['from'], sid, file, methods, el['to'],el['id'])
		self.on_fileReceived(sid, el['id'])
	
# 	def on_FileReceived(self, sid, id):
# 		if 'http://jabber.org/protocol/bytestreams' in self.ft[sid].methods:
# 			self.ft[sid].method = 'http://jabber.org/protocol/bytestreams'
# 			self.ft[sid].file = self.ft[sid].fileprops['name']
# 			self.receiveFile(sid, id)
# 		elif 'http://jabber.org/protocol/ibb' in self.ft[sid].methods:
# 			log.msg('IBB offer')
# 			self.ft[sid].method = 'http://jabber.org/protocol/ibb'
# 			self.ft[sid].file = self.ft[sid].fileprops['name']
# 			self.ft[sid].fp = open(self.ft[sid].file, 'w')
# 			self.receiveFile(sid, id)
	
	def receiveFile(self, sid, id):
		iq = Element((None,'iq'))
		obj = self.ft[sid]
		iq['to'] = obj.tojid
		iq['from'] = obj.frmjid
		iq['id'] = id
		iq['type'] = 'result'
		si = iq.addElement('si', 'http://jabber.org/protocol/si')
		si.addElement('file', 'http://jabber.org/protocol/si/profile/file-transfer')
		feature = si.addElement('feature', 'http://jabber.org/protocol/feature-neg')
		x = feature.addElement('x', 'jabber:x:data')
		x['type'] = 'submit'
		field = x.addElement('field')
		field['var'] = 'stream-method'
		value = field.addElement('value', content = obj.method)
#		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)
	
		
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
		iq = IQ(self.xmlstream, 'set')
		iq['to'] = self.ft[sid].tojid
		if self.ft[sid].frmjid != None:
			iq['from'] = self.ft[sid].frmjid
		opn = iq.addElement('open', 'http://jabber.org/protocol/ibb')
		opn['sid'] = sid
		opn['block-size'] = '4096'
#		self.on_xml(iq.toXml())
		d = iq.send()
		self.disp(iq['id'])
		d.addCallback(self._ftIBBStart, sid)
		d.addErrback(self._ftIBBError, sid)
	
	def _ftIBBError(self, err, sid):
		print err
		self.ft[sid].error = 'IBB error.'
		self.ft[sid].finish()
	
	def _ftIBBStart(self,el, sid):
		iq = IQ(self.xmlstream, 'set')
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
		self.on_ftTransfered(sid, len(dt))
		d.addCallback(self._ftIBBContinue, sid)
		d.addErrback(self._ftIBBError, sid)
		
	def _ftIBBContinue(self,el, sid):
		iq = IQ(self.xmlstream, 'set')
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
			iq = IQ(self.xmlstream, 'set')
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
		self.on_ftTransfered(sid, len(dt))
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
		self.xmlstream.send(iq)
	
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
		self.xmlstream.send(iq)
		
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
			self.xmlstream.send(iq)
			
		pass
	
	def onIBBEnd(self, iq):
		self.disp(iq['id'])
		close = iq.firstChildElement()
		log.msg('IBB end')
		sid = close['sid']
		self.ft[sid].ibbProcess()
		self.ft[sid].finish()

	def onPing(self, el):
		log.msg('sending pong')
		self.disp(el['id'])
		iq = Element((None, 'iq'))
		iq['to'] = el['from']
		iq['type'] = 'result'
		iq['id'] = el['id']
#		self.on_xml(iq.toXml())
		self.xmlstream.send(iq)

	def onEvil(self, el):
		log.msg('we are tainted by evil')
		frm = el['from'] 
		typ = el.name
		self.dispatcher.publishEvent('on_evil', frm, typ)
		
	def disp(self, id):
		self.idlist.append(id)

