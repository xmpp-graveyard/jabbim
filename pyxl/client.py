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
import sys, time, random, os, re
import socks5, events, base64
from twisted import names
from twisted.python import log
from twisted.internet import protocol, error
from twisted.names import client as dns
from socket import getaddrinfo
import socket
from twisted.internet import threads, defer, reactor
from twisted.words.protocols import jabber
from twisted.words.protocols.jabber import client
import jid
from twisted.words.xish import domish
from twisted.words.xish.domish import Element
##from twisted.internet import reactor, address
from twisted.words.protocols.jabber.xmlstream import IQ, TimeoutError
from twisted.internet.protocol import Protocol, ClientFactory, Factory

from twisted.internet.task import LoopingCall
from calendar import timegm
from derived import derived
from contact import *
from groupchat import  *
from base64 import b64encode, b64decode
from privacy import *
from adhoc import *
import rc
import traceback
from configobj import ConfigObj
import locale
import rpc
import presence,  message,  ft,  jingle
#import bosh_wokkel
try:
	from hashlib import sha1
except:
	log.msg('Please upgrade to python2.5')
	from sha import new as sha1
from PyQt4 import QtGui,QtCore

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
		self.reactor = reactor
		self.jid = jid.JID(JID)
		self.password  = password
		self.host = self.jid.host
		self.port = port
		self.factory = None
		self.connection = None
		self.main=main # mainWindow
		self.xmlstream = None
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

		self.isVip=False
		
		self.discofeatures = {} # node: [feature1, feature2]
		self.discoitems = {None:[],"http://jabber.org/protocol/commands":[]}
		self.ft_proxies = {
		'proxy.jabbim.cz':[] 
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
#		self.registerFeature('http://jabber.org/protocol/bytestreams#udp')
		self.registerFeature('http://jabber.org/protocol/disco#info', 'http://jabber.org/protocol/commands', identity={"category":"automation","type":"command-list", "name":self.main.tr("Extra actions")})
		self.registerFeature('jabber:x:data', 'http://jabber.org/protocol/commands')
		self.registerFeature('http://jabber.org/protocol/commands','http://jabber.org/protocol/commands')
		self.registerFeature('http://jabber.org/protocol/si/profile/file-transfer')
		self.registerFeature('http://jabber.org/protocol/si')
		self.registerFeature("urn:xmpp:receipts")
		self.registerFeature('http://www.xmpp.org/extensions/xep-0224.html#ns')
		self.registerFeature('http://jabber.org/protocol/rosterx')
		self.registerFeature('http://jabber.org/protocol/muc')
		self.registerFeature('http://jabber.org/protocol/tune')
		self.registerFeature('http://jabber.org/protocol/tune+notify')
		self.registerFeature('http://jabber.org/protocol/mood')
		self.registerFeature('http://jabber.org/protocol/mood+notify')
		self.registerFeature('http://jabber.org/protocol/activity')
		self.registerFeature('http://jabber.org/protocol/activity+notify')
		self.registerFeature('http://www.xmpp.org/extensions/xep-0194.html#ns')
		self.registerFeature('http://www.xmpp.org/extensions/xep-0194.html#ns+notify')
		self.registerFeature('http://dev.jabbim.cz/jabbim#favroster')
		self.registerFeature('urn:xmpp:tmp:jingle')
		self.registerFeature('urn:xmpp:tmp:jingle:apps:file-transfer')
		self.registerFeature('urn:xmpp:tmp:jingle:transports:bytestreams')
		self.registerFeature('urn:xmpp:tmp:bob')
		self.identity = 'client/pc'
		
		self.caps_cache = {} # 'ext': (identity,[feature1, feature2])
		self.rebuildCaps()
		self.evil = False
		self.log = True
		self.xmlLang = 'cs'
		self.dispatcher = events.EventDispatcher()
		self.avatars = {} # jid:hash
#		path = self.main.homeDir+'/avatars/'
#		for jd in os.listdir(path):
#			fd = open(path+jd, 'rb')
#			hash = sha1(fd.read()).hexdigest()
#			fd.close()
#			self.avatars[jd] = hash
		self.avatars = {}
		self.avatarDef = ConfigObj(self.main.realHomeDir+'/avatars/avatars.def',encoding='UTF8')
		self.avatarImg = {} #hash:QPixmap
		self.bobDef = ConfigObj(self.main.realHomeDir+'/bobCache/bob.def',encoding='UTF8')
		self.bobCacheDir =self.main.realHomeDir+'/bobCache/'
#		self.bobMine = ConfigObj(self.main.realHomeDir+'/bobCache/mine.def',encoding='UTF8')
		
		path = self.main.realHomeDir+'/avatars/'

		self.main.cache.get_caps().addCallback(self._cacheCaps)
		self.dispatcher.registerHandler('on_message', self.on_message, 'on_message')
		self.dispatcher.registerHandler('on_presence', self.on_presence, 'on_presence')
		self.dispatcher.registerHandler('on_GCpresence', self.on_GCpresence, 'on_GCpresence')
		self.dispatcher.registerHandler('on_GCpresenceError', self.on_GCpresenceError, 'on_GCpresenceError')
		self.dispatcher.registerHandler('on_GCmessage', self.on_GCmessage, 'on_GCmessage')
		self.dispatcher.registerHandler('on_authd', self.on_authd, 'on_authd')
		
		self.dispatcher.registerHandler('on_ftEnd', self.on_ftEnd, 'on_ftEnd')
		self.dispatcher.registerHandler('on_ftTransfered', self.on_ftTransfered, 'on_ftTransfered')
		self.dispatcher.registerHandler('on_pep', self.on_pep, 'on_pep') #docasne
		self.xping = LoopingCall(self.heartbeat)
		self.hbFails = 0
		self.connections = [] # [(host1, port1), (host2, port2), ..]
		self.messageReceipts = {} # id:(zprava)
		self.oldstatus = None

		self.socks5Port = '33333'
		self.socks5IP = [] #
		self.pep = False
		self.IBBonly = False #use only IBB in SI transfers if this is True [we are in restricted enviroment]
		#self.reactor.callFromThread(self.on_init)

		self.rpc = rpc.rpc(self)
		self.presence = presence.PresenceInit(self)
		self.message = message.MessageInit(self)
		self.FT = ft.FTInit(self)
		self.jingle = jingle.JingleInit(self)
		
		self.proxy = None
	

	def chyba(self, err):
#		print err
		err.printBriefTraceback()
	
	def getAvatarImg(self, jd):
		#vrati QPixmap nebo None
		if not jd or jd=="None":
			return self.avatarImg.get(None, None)
		jd = self.main.getJid(jd)
		if self.groupchats.has_key(jd.userhost()):
			jid = jd.full()
		else:
			jid = jd.userhost()
		if self.avatarDef.has_key(jid):
			return self.avatarImg.get(self.avatarDef[jid], None)
	
	def cacheCaps(self, ext, features, identity):
		self.caps_cache[ext] = [identity,features]
		self.main.cache.set_caps(ext, features, identity)

	def _cacheCaps(self, result):
		for line in result:
			if line != None:
				caps = self.caps_cache.get(line[0], ['',[]])
				if line[1] not in caps[1]:
					caps[1].append(line[1])
				if caps[0] == '':
					caps[0] = line[2]
				self.caps_cache[line[0]] = caps
				
	def rebuildCaps(self):
		features = []
		for f in self.discofeatures[None]:
			features.append(f[0])
		self.caps_ext = self.calcCapsExt(features = features, identity = [self.identity])
		self.cacheCaps(self.caps_ext, features, self.identity)
			

	def heartbeat(self):
		log.msg('heartbeat')
		iq = IQ(self.xmlstream, 'get')
		iq['xml:lang'] = self.xmlLang
		q = iq.addElement('ping', 'urn:xmpp:ping')
		self.disp(iq['id'])
		iq.timeout = 90
		if self.connection != None:
			d = iq.send()
			d.addCallback(self._heartbeat)
			d.addErrback(self._heartbeatErr)
			return d
	
	def _heartbeat(self, el):
		log.msg('heartbeat ok')
		self.hbFails = 0
	
	def _heartbeatErr(self, err):
		if err.type == TimeoutError:
			log.msg('heartbeat failed')
			self.hbFails += 1
			if self.hbFails >= 3:
				self.xping.stop()
	#			if self.factory:
	#				self.factory.stopTrying()
				try:
					self.connection.loseConnection()
				except:
					print 'chyba v loseConnection(nejsme pripojeni?)'
				self.connectionLost(self.connection)
			else:
				log.msg('heartbeat fails count: '+ unicode(self.hbFails))


	def connect(self, host = None, port = '5222', boshURL = '',JID='',password='',server=''):#http://].jabbim.cz:80
		#cleanup
		self.roster = {'users':{},'groups':{}}
		self.first_presence = []
		self.first_wait = True
		self.bookmarks = {'conference':{}, 'url': {}}
		self.idlist = []
		self.hbFails = 0
		self.discoitems = {None:[],"http://jabber.org/protocol/commands":[]}
		self.isVip=False
		self.reactor.callFromThread(self.on_init)
		print 'XXXX ', JID,  self.jid.full(),  self.oldstatus
		if JID != self.jid.full():
			self.oldstatus = None
			print 'deleted'
		self.jid = jid.JID(JID)
		self.password  = password
		self.host = self.jid.host
		self.port = int(port)
		
		if boshURL != '':
			try:
				from urlparse import urlparse
				parts = urlparse(boshURL)[1].split(':')
				bhost = parts[0]
				bport = parts[1]
			except:
				print 'bosh parse failure'
				boshURL = ''
		if host != None:
			self._connect(host, int(port))
		elif boshURL != '':
			print 'going bosh: ', bhost, int(bport), boshURL
			self._connect(bhost, int(bport), boshURL)
		else:
			log.msg('dns - ' + unicode(time.time()) + '_xmpp-client._tcp.'+self.jid.host)
			if sys.platform == 'win32':
				import IPConfig
				proxy = IPConfig.getProxy()
				if proxy != None:
					casti =proxy.split(':')
					if len(casti) ==1:
						p = '80'
					else:
							p = casti[1]
					h = casti[0]
					self.proxy = {'host':h,  'port': p,  'type': 'http'}
				srv = IPConfig.IPConfig().get_dns()
				dnssrv = []
				for server in srv:
					if len(server.strip())>0 and server.strip() != '0.0.0.0':
						dnssrv.append((server, 53))
				if len(dnssrv) > 0:
					r = dns.Resolver(servers=dnssrv)
					d = r.lookupService('_xmpp-client._tcp.'+self.jid.host, timeout = [2,10])
				else:
					log.msg('using root resolver')
					d = dns.lookupService('_xmpp-client._tcp.'+self.jid.host, timeout = [2,10])
			else:
				d = dns.lookupService('_xmpp-client._tcp.'+self.jid.host, timeout = [2,10])
				import urllib
				proxies = urllib.getproxies()
				if proxies.has_key('http'):
					from urlparse import urlparse
					parts = urlparse(proxies['http'])[1].split(':')
					if len(parts) == 1:
						p = '80'
					else:
						p = parts[1]
					h = parts[0]
					self.proxy = {'host':h,  'port': p}


#			d.addCallback(self._dnsLookup)
#			d.addErrback(self._dnsLookupErr)
#			dns.getHostByName('localhost').addCallback(self.tst)
			txt = dns.lookupText('_xmppconnect.'+self.jid.host, timeout = [2,10])
			defer.DeferredList([d, txt]).addCallback(self._dnsLookup).addErrback(self._dnsLookupErr)

	def _dnsLookup(self, results):
		print 'DNS'
		self.connections = []
		resp = results[0][1]
		print resp
		if len(resp[0]) ==0:
			self._dnsLookupErr(resp)
			return
		for r in resp[0]:
			self.connections.append((unicode(r.payload.target), int(r.payload.port)))
			print (unicode(r.payload.target), int(r.payload.port))
		
		txt =results[1][1]

		for r in txt[0]:
			parts= r.payload.data[0].split('=')
			if parts[0] == '_xmpp-client-xbosh':
				self.connections.append((parts[1], ))
		
		self.doConnect()
#		self._connect(unicode(r[4][0]), int(r[4][1]))
	
	def _dnsLookupErr(self, resp):
		print 'err:', resp
		print dir(resp)
		self.connections.append((self.host, self.port))
		self.connections.append(('http://bind.jabbim.cz:80/', )) #just give them chance
		self.doConnect()
		#self._connect('talk.google.com', self.port)

	def doConnect(self):
		#pops first connection from list and tries to connect to it
		print 'do connect ',  self.connections
		if len(self.connections) == 0:
			self.main._disconnect(error = 'failed')
			self.reactor.callFromThread(self.on_disconnect)
			return
		pop = self.connections.pop(0)
		if len(pop) ==2:
			host = pop[0]
			port = pop[1]
			self._connect(host,port)
		elif len(pop) == 1:
			boshURL = pop[0]
			try:
				from urlparse import urlparse
				parts = urlparse(boshURL)[1].split(':')
				bhost = parts[0]
				if len(parts) ==1:
					bport = 80
				else:
					bport = parts[1]
			except:
				print 'bosh parse failure'
				self.doConnect()
			self._connect(bhost, int(bport), boshURL)

				
	def _connect(self, host, port, boshURL = ''): 

		if boshURL != '':
			print '.'+boshURL+'.'
			from bosh import client as bclient

			self.factory = bclient.BOSHClientFactory(self.jid, self.password, unicode(boshURL), bosh_attrs = {"wait": "10", 'xml:lang':self.xmlLang},  proxy  = self.proxy)
#			self.factory = bosh_wokkel.BOSHClient(self.jid, self.password, unicode(boshURL), bosh_attrs = {"wait": "10", 'xml:lang':self.xmlLang})
			print self.factory
			self.IBBonly = True
		else:
			self.factory = client.XMPPClientFactory(self.jid,self.password)
			if unicode(port) == '443':
				self.IBBonly = True
		self.factory.addBootstrap('//event/stream/authd',self._authd)
##		self.factory.addBootstrap("//event/client/basicauth/invaliduser", self._invaliduser)
##		self.factory.addBootstrap("//event/client/basicauth/authfailed", self._authfailed)
		self.factory.addBootstrap("//event/xmpp/initfailed", self._authfailed)
		self.factory.addBootstrap('/iq[@type="result"]/bind', self._bind)
		self.factory.addBootstrap('//event/stream/error', self._streamEnd)
		self.factory.addBootstrap('//event/stream/end', self._streamEnd)
		self.factory.addBootstrap('/*', self.bootLog)
		
		self.factory.clientConnectionLost = self.connectionLost
		self.factory.clientConnectionFailed = self.connectionFailed
		print '-'+host+'?', port
		#self.connection = reactor.connectTCP(host,port, self.factory)

		if self.proxy != None and self.IBBonly:
			self.connection = reactor.connectTCP(self.proxy['host'],int(self.proxy['port']), self.factory)
			print self.proxy
		else:
			self.connection = reactor.connectTCP(host,port, self.factory)
		self.reactor.callFromThread(self.on_connect)
		print dir(self.factory)
		print dir(self.connection)
		print self.factory.protocol
#		self.connection.buildProtocol()
#		self.factory.buildProtocol()
#		self.factory.protocol.factory = self.factory
#		self.factory.protocol.host = host
#		self.factory.protocol.port = port
#		self.factory.protocol.connect(self.factory.protocol)
		

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
			self.reactor.callFromThread(self.on_xml,u'BOOT: ' + el.toXml())
			
	def connectionLost(self, connector, reason=protocol.connectionDone):
		
		if self.IBBonly:
			self.connection.connect()
#			self.connection.factory.bosh_client.manager.restart()

			return
		log.msg('connection lost!')
		try:
			self.xping.stop()
		except:
			pass
		if self.factory:
			self.factory.stopTrying()
		if self.connection:
			self.connection.disconnect()
		else:
			self.connection = None
		self.factory = None
		print 'receipts ' + unicode(self.messageReceipts)
		try:
			self.main.delayedMessages = self.messageReceipts
		except:
			pass
		self.reactor.callFromThread(self.main._disconnect,'lost')

		self.reactor.callFromThread(self.on_disconnect)
	
	def connectionFailed(self, connector, reason=protocol.connectionDone):
		log.msg('connection failed!')
		print self.connections
		if len(self.connections)>0:
			self.doConnect()
		else:
			self.main._disconnect(error = 'failed')
			self.reactor.callFromThread(self.on_disconnect)

	def _streamEnd(self, el):
		print 'stream end'
		try:
			self.xping.stop()
		except:
			pass
		if self.factory:
			self.factory.stopTrying()
		pass
		
	def _bind(self, el):
		#experimental
		log.msg('bind')
		bind = el.firstChildElement()
		jd = bind.firstChildElement().__str__()
		self.jid = jid.JID(jd)
		
	def disconnect(self):
		
		print self.oldstatus
		try:
			self.xping.stop()
		except:
			pass
		if self.connection:
			self.connection.disconnect()
		if self.factory:
			self.factory.stopTrying()
		self.connection = None
		self.factory = None
		self.reactor.callFromThread(self.on_disconnect)

	def _authd(self, xmlstream):
		log.msg('authed')
##		self.dispatcher.publishEvent('authed')
		self.xmlstream = xmlstream
		self.xmlstream.removeObserver('/*', self.bootLog)
		self.xmlstream.rawDataInFn = self.rawDataIn
		self.xmlstream.rawDataOutFn = self.rawDataOut
		self.xmlstream.addObserver("/presence", self.presence.onPresence, 1)
		self.xmlstream.addObserver("/message", self.message.onMessage, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/query[@xmlns='jabber:iq:roster']", self.onRosterAdd, 1)
		self.xmlstream.addObserver("/*", self.onXML)
		self.xmlstream.addObserver("/presence[@type='subscribe']", self.presence.onSubscribe, 1)
		self.xmlstream.addObserver("/presence[@type='unsubscribe']", self.presence.onUnSubscribe, 1)
		self.xmlstream.addObserver("/presence[@type='subscribed']", self.presence.onSubscribed, 1)
		self.xmlstream.addObserver("/presence[@type='unsubscribed']", self.presence.onUnSubscribed, 1)
		self.xmlstream.addObserver("/presence[@type='error']", self.presence.onPresenceError, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='jabber:iq:version']", self.onVersion, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='http://jabber.org/protocol/disco#info']", self.onDiscoInfo, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='http://jabber.org/protocol/disco#items']", self.onDiscoItems, 1) 
		self.xmlstream.addObserver("/iq[@type='set'][@id]/command[@xmlns='http://jabber.org/protocol/commands'][@node]", self.onCommand, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='jabber:iq:last']", self.onLast, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/time[@xmlns='urn:xmpp:time']", self.onTime202, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/query[@xmlns='jabber:iq:time']", self.onTime90, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/si[@xmlns='http://jabber.org/protocol/si' ][ @profile='http://jabber.org/protocol/si/profile/file-transfer']", self.FT.onFileReceive, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/query[@xmlns='http://jabber.org/protocol/bytestreams']/streamhost", self.FT.onStreamhosts, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/open[@xmlns='http://jabber.org/protocol/ibb']", self.FT.onIBBStart, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/close[@xmlns='http://jabber.org/protocol/ibb']", self.FT.onIBBEnd, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/data[@xmlns='http://jabber.org/protocol/ibb']", self.FT.onIBBData, 1)
		self.xmlstream.addObserver("/message/data[@xmlns='http://jabber.org/protocol/ibb']", self.FT.onIBBData, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/confirm[@xmlns='http://jabber.org/protocol/http-auth']", self.onVerify, 1)
		self.xmlstream.addObserver("/message/confirm[@xmlns='http://jabber.org/protocol/http-auth']", self.onVerify, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/ping[@xmlns='urn:xmpp:ping']", self.onPing, 1)
		self.xmlstream.addObserver("/message/x[@xmlns='http://jabber.org/protocol/muc#user']/invite", self.message.onInvite, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/query[@xmlns='jabber:iq:privacy']", self.onPrivacyPush, 1)
		self.xmlstream.addObserver("/*/evil[@xmlns='http://jabber.org/protocol/evil']", self.onEvil, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/x[@xmlns='http://jabber.org/protocol/rosterx']", self.onRosterX, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/query[@xmlns='jabber:iq:rpc']", self.rpc.onRPC, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/jingle[@action='session-initiate']", self.jingle.onJingleInitiate, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/jingle[@action='session-accept']", self.jingle.onJingleAccept, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/jingle[@action='session-terminate']", self.jingle.onJingleTerminate, 1)
		self.xmlstream.addObserver("/iq[@type='set'][@id]/jingle[@action='content-replace']", self.jingle.onJingleContentReplace, 1)
		self.xmlstream.addObserver("/iq[@type='get'][@id]/data[@xmlns='urn:xmpp:tmp:bob']", self.onBOBData, 1)

		self.xping.start(100, False)		
		self.getPrivacy().addCallback(self.getMetacontacts).addErrback(self.getMetacontacts)
#		self.getMetacontacts()
		self.getBookmarks()
		d=self.getDiscoInfo(self.jid.host, callback = self._pepSupport)
		self.getDiscoItems(self.jid.host, callback = self._gotServices)
#		self.reactor.callFromThread(self.on_authd)
		self.roster['users'][self.jid.userhost()] = Contact(self, self.jid.userhost(), '', 'both', [], []) #add selfcontact to our representation of roster
		self.reactor.callLater(0,self.main._connected)
		#self.main._connected()
		print 'pre commands'
		self.commands = Commands(self.main)
		try:
			public = self.main.config['adhocAllow']
		except:
			public = False
			
		self.commands.registerNode("http://jabber.org/protocol/rc#set-status", "Change status", rc.fSetStatus, public = public)
		self.commands.registerNode("http://jabber.org/protocol/rc#leave-groupchats", "Leave groupchats", rc.fLeaveGC, public = public)
		self.commands.registerNode("http://dev.jabbim.cz/jabbim/rc#resend-file", "Resend file", rc.ResendFile, public = public)
		self.commands.registerNode("http://jabber.org/protocol/rc#forward", "Forward unread messages", rc.ForwardMsg, public = public)
#		print 'post commands'
#		def pis(co):
#			print co
		self.callRemote('rpc@jabbim.cz/service', 'isVIP', (self.jid.userhost(),)).addCallback(self._isVip)
		print "calling on_authd"
		self.dispatcher.publishEvent('on_authd')

	def _isVip(self,data):
		if int(data[0][0])==1:
			self.isVip=True

	def _gotServices(self, res):
		for jid in self.disco[self.jid.host][None]['items'].iterkeys():
			self.getDiscoInfo(jid)
			print jid
		
	def _pepSupport(self, res):
		log.msg('pep support arrived')
		for key,  val in self.disco[self.jid.host][None]['identities'].iteritems():
			log.msg(key+ unicode(val))
			if val['type'] == 'pep' :
				log.msg( 'we got a PEP support')
				self.pep = True
#				self.sendPEP('tune', {})
	
	def _pepReceived(self,  el):
		log.msg(el.toXml())
	
	def registerFeature(self, feature, node = None, identity = None):#{"category":None,"type":None,"name":None}):
		if self.discofeatures.has_key(node):
			self.discofeatures[node].append((feature,))
		else:
			self.discofeatures[node] = []
			self.discofeatures[node].append((feature, identity))
	
	def unregisterFeature(self, feature, node = None):
		if self.discofeatures.has_key(node):
			if (feature,) in self.discofeatures[node]:
				self.discofeatures[node].remove((feature,))

	#def registerItem(self, jid = None, name = None, node = None, parentnode = None):
	#	log.msg("registering disco#item")
	#	if jid == None:
	#		jid = self.jid.full()
	#	self.discoitems[parentnode].append({"jid":jid,"name":name,"node":node})


	def onRosterAdd(self,el):
		log.msg("roster item add")
		self.disp(el['id'])
		#log.msg(el.toXml())
		if el == None:
			print 'wtf?', el
			return
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
						contact.subscription = subscription
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
#		self.avatars[jid] = None
		self.avatarDef[jid] = 'None'
		self.avatarDef.write()
		self.reactor.callFromThread(self.on_avatarUpdate,jid)
		
		return err

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
		if card.has_key("PHOTO-BINVAL") and len(card["PHOTO-BINVAL"])!=0:
			image=base64.decodestring(str(card["PHOTO-BINVAL"]))
			hash = sha1(image).hexdigest()
			f=open(self.main.realHomeDir+'/avatars/'+hash,"wb")

			f.write(image)
			f.close()

			self.avatarDef[el['from']] = hash
			self.avatarDef.write()
			#try:
			self.avatarImg[hash] = self.main.loadAvatar(hash)#self.main.getAvatar(hash,size="32x32",frame=True)
			#except:
				#self.avatarImg[hash] = None
			#try:
			self.reactor.callFromThread(self.on_avatarUpdate,el['from'])
			#except:
				#print 'chyba v updatu avatara'
		else:
			self.avatarDef[el['from']] = None
			self.avatarDef.write()
		self.reactor.callFromThread(self.on_vcardReceived,el['from'],el)
		return vcard



	def _bookmarksSet(self, el):
		log.msg('bookmarks set sucessfully')

	def _bookmarksErrReceived(self, err):
		print err
		self.reactor.callFromThread(self.on_bookmarksFail)
		pass #no tak neprisly no
	def _bookmarksReceived(self, el):
		log.msg( 'bookmarks received')
		try:
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
									self.bookmarks['conference'][jid] = Bookmark(name, 'conference', jid, autojoin, nick,  password)
								if bookmark.name == 'url':
									url = bookmark['url']
									if bookmark.hasAttribute('name'):
										name = bookmark['name']
									else:
										name = url
									self.bookmarks['conference'][name] = Bookmark(name, 'url', url = url)
		except Exception, ex:
			log.msg('Storage error: ' +unicode(ex))
			message = traceback.format_exc()
			log.msg(message)


	
	def _metacontactsErrReceived(self,  err):
		log.msg('meta error')
		self.getRoster()
		self.reactor.callFromThread(self.on_metaFail,err)
		
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
		print params
		self.sendPresence(to = params['jid'], status = params['msg'], typ = 'subscribe')



	def onXML(self, el):
		if not el.hasAttribute('from'):
			print el.toXml()
			return
		if el.hasAttribute('id') and el.name == 'iq':
			if not el['id'] in self.idlist and (el['type'] != 'result' or el['type'] != 'error'):
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
				self.reactor.callFromThread(self.on_xml,u'IN: ' + unicode(buf, 'utf8', 'replace'))
			except:
				self.reactor.callFromThread(self.on_xml,u'IN: ' + buf)
	
	def rawDataOut(self, buf):
		if self.log:
			try:
				self.reactor.callFromThread(self.on_xml,u'OUT: ' + unicode(buf, 'utf8', 'replace'))
			except:
				self.reactor.callFromThread(self.on_xml,u'OUT: ' + buf)
			
	def _onRosterArrive(self, el):
		log.msg( 'roster arrived')
		ln = 0
		hosts = [] #for disco info
		
		for child in el.elements():
			if child.name == "query":
				allGroups=['Unknown']
				for item in child.elements():
					ln = ln + 1
					groups = []
					try:
						item['jid'] = item['jid'].strip()
						j = jid.JID(item['jid'])
					except jid.InvalidFormat:
						log.err('invalid jid in roster: '+item['jid'])
						continue
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
					host = jid.JID(item['jid'].strip()).host
					if not host in hosts:
						hosts.append(host)
					contact = Contact(self, item['jid'], name, item['subscription'], [], groups, tag =  tag, order =  order, ask = ask)
					self.roster['users'][item['jid']] = contact
					self.reactor.callFromThread(self.on_rosterAddUser,contact)

		for host in hosts:
			if self.getIdentity(host) == None:
				self.getDiscoInfo(host)
				
		
		
		log.msg( 'roster arrived')
#		print self.oldstatus
#		if self.oldstatus != None:
#			show,  status = self.oldstatus
#			self.sendPresence(show = show,  status = status)
#		else:
#			self.sendPresence()
		cekej = 1
#		if ln*0.05 < cekej:
#			cekej = ln*0.05
		self.reactor.callFromThread(self.on_rosterArrived)
		self.reactor.callLater(cekej,  self.presence.onFirstPresence)


	def _authfailed(self,xmlstream):
		log.msg( "auth_failed")
		print 'init failed!'
		print unicode(xmlstream)
		self.main._disconnect(error = 'auth')
		self.disconnect()
		self.on_authFailed(xmlstream)

	def _invaliduser(self,xmlstream):
		log.msg( "invalid_user")
		#self.on_invalidUser(self)

	def _featuresReceived(self, el, ext, jd):
		#log.msg( 'features received')
		#print el.toXml()
##		self.disp(el['id'])
		features = []
		identity = ''
		query = el.firstChildElement()
		for child in  query.elements():
			if child.name == 'feature':
				features.append(child['var'])
			if child.name == 'identity':
				identity = '%s/%s'%(child['category'], child['type'])
		if ext != None:
			self.cacheCaps(ext, features, identity)
		frm = jid.JID(el['from'])
		resource = frm.resource
		if self.roster['users'].has_key(frm.userhost()):
			self.roster['users'][frm.userhost()].setFeatures(resource, features, identity)
	
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
		if len(self.client_os)>0:
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
		if node == '%s#%s'%(self.caps_node, self.version): #magie: pokud se nas nekdo zepta na caps nasi verze, tak mu rekneme default
			node == None

		if not self.discofeatures.has_key(node):
			node = None
		if node != None:
			q['node'] = node
		else:
			id = q.addElement('identity')
			id['category'] = self.identity.split('/')[0]
			id['name'] = self.client_name
			id['type'] = self.identity.split('/')[1]
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
		#log.msg("ITEMS: "+`self.discoitems`)
		self.disp(el['id'])
		try:
			lang = el["xml:lang"]
		except:
			lang = None
			print el.toXml()
			try:
				lang = el[(u'http://www.w3.org/XML/1998/namespace', u'lang')]
			except:
				pass

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
				if node == "http://jabber.org/protocol/commands":
					try:
						public = self.commands.nodes[item['node']][3]
					except KeyError:
						public = False
					ji = jid.JID(el['from']).userhost()
					if type(public) == bool:
						allowed = public
					else:
						allowed = (ji in public) or (ji == self.jid.userhost())
				else:
					allowed = True
					
				if allowed:
					i = q.addElement("item")
					i["jid"] = item["jid"]
					if item["name"] != None:
						try:
							i["name"] = self.main.tr(item["name"], lang)
						except:
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
		try:
			public = self.commands.nodes[node][3]
		except KeyError:
			#pokud se pta na node co nemame
			public = False
		ji = jid.JID(el['from']).userhost()
		if type(public) == bool:
			allowed = public
		else:
			allowed = (ji in public) or (ji == self.jid.userhost())
			
		print public, allowed, ji
		try:
			lang = el["xml:lang"]
		except:
			lang = None
			try:
				lang = el[(u'http://www.w3.org/XML/1998/namespace', u'lang')]
			except:
				pass
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
			print 'fire it up!'
			self.commands.sessions[sid].execStage(
					self.commands.sessions[sid].nextstages[action],
					el["id"],
					x2dict(x),
					lang
					)
			log.msg("ok, continuing in current session")


		except KeyError, RuntimeError:
			if allowed:
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
				

	def onBOBData(self,  el):
		self.disp(el['id'])
		data = el.data
		cid = el.data['cid']
		if self.bobDef.has_key(cid):
			fp = open(self.bobDef[cid],  'rb')
			dt = fp.read()
			fp.close()
			el.data.addContent(b64encode(dt))
			el.swapAttributeValues('to',  'from')
			el['type'] = 'result'
		else:
			el.swapAttributeValues('to',  'from')
			el['type'] = 'error'
			el.addElement('error')
			el.error.addElement('not-found')
		self.xmlstream.send(el)
	
	def getBOBData(self,  to,  cid):
		def _loadBOBLink(cid):
			if cid != None:
				print 'cache hit'
				return self.bobDef[cid]
			else:
				return cid
		
		def _writeBOBData(el,  cid):
			print 'data received!'
			frm = jid.JID(el['from'])
			data = b64decode(unicode(el.data))
			#TODO detect hash type
			if sha1(data).hexdigest() == cid.split('@')[0]:
				fp = open(self.bobCacheDir+cid,  'wb')
				fp.write(data)
				fp.close()
			else:
				print 'cid is not hash!?'
			self.bobDef.write()	
			return self.bobCacheDir+cid
		
		to = jid.JID(to)
		if self.bobDef.has_key(cid):
			return threads.deferToThread(_loadBOBLink, cid)
			
		self.bobDef[cid] = self.bobCacheDir+cid
		if not self.hasFeature(to.full(), 'urn:xmpp:tmp:bob'):
			return threads.deferToThread(_loadBOBLink, None)
		iq = IQ(self.xmlstream, 'get')
		self.disp(iq['id'])
		iq['to'] = to.full()
		iq.addElement('data',  'urn:xmpp:tmp:bob')
		iq.data['cid'] = cid
		return iq.send().addCallback(_writeBOBData,  cid)

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
				if node.has_key('err'):
					if node.has_key('items'):
						node = {'features':[], 'identities':{},  'items': node['items']}
					else:
						node = {'features':[], 'identities':{},  'items': {}}
					self.disco[frm] = {}
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
				#log.msg(unicode(node))
				node['identities'][name] = child.attributes
				cat = child.getAttribute('category')
				typ = child.getAttribute('type')
				if cat == 'proxy' and typ == 'bytestreams':
					if not self.ft_proxies.has_key(frm):
						self.ft_proxies[frm] = []
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
				if node.has_key('err'):
					if node.has_key('features'):
						features = node['features']
					else:
						features = []
					if node.has_key('identities'):
						identities = node['identities']
					else:
						identities = {}
					node = {'features':features, 'identities':identities,  'items': {}}
					self.disco[frm] = {}
		else:
			self.disco[frm] = {}
			node = {'features':[], 'identities':{},'items':{}}
		node['items'] = {}

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
		return err

	def onPrivacyPush(self, el):
		name = el.firstChildElement().firstChildElement()["name"]
		try:
			if name != self.privacy.active.name:
				return			# Je nam to u prdele,  protoze jiny listy nez active nevedem
		except AttributeError:			# dokud nezjistim kde se bere ze active je None :/
			return
		iq	= IQ(self.xmlstream, "get")
		query	= iq.addElement("query", "jabber:iq:privacy")
		list_	= query.addElement("list")
		list_.attributes = {"name":name}
		d	= iq.send()
		self.disp(iq["id"])
		d.addCallback(self._activeRecieved, False).addErrback(self.chyba)

	def getPrivacy(self):	
		log.msg('requesting priacy lists')
		iq = IQ(self.xmlstream, 'get')
		q = iq.addElement('query', 'jabber:iq:privacy')
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
		log.msg('privacy lists received')
		query = el.firstChildElement()
		lists = []
		active = None
		for child in query.elements():
			if child.name == "list":
				lists.append(child.attributes["name"])
			if child.name == "active":
				active = child.attributes["name"]
		log.msg("lists: %s; active: %s" % (", ".join(lists), active))
		
		def getActive(el,name):
			log.msg("Requesting active privacy list: %s." % name)
			iq	= IQ(self.xmlstream, "get")
			query	= iq.addElement("query", "jabber:iq:privacy")
			list_	= query.addElement("list")
			list_.attributes = {"name":name}
			d	= iq.send()
			self.disp(iq["id"])
			d.addCallback(self._activeRecieved, True).addErrback(self.chyba)

		if active:
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
			self.disp(iq["id"])
			log.msg("Creating new privacy list: %s." %  defaultlistname)
			d.addCallback(getActive, defaultlistname).addErrback(self.chyba)
			self.privacy.setActive(defaultlistname)
			self.privacy.setDefault(defaultlistname)

		for l in lists:
			self.privacy.lists[l] = None	# Bude nas zajimat jen active
							# Dalsi se nactou az pozdejc, jinak je to plejtvani


	def _activeRecieved(self, el, b=True):
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
		self.privacy.active = PrivacyList(name, items, self.main, b)
		self.privacy.lists[name] = self.privacy.active
		self.privacy.default = self.privacy.active
		if b:
			self.privacy.active.unsetInvisible(available=False) ## HACK
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
		q.addElement('utc', content = unicode(time.strftime("%Y%m%dT%T", time.gmtime())))
		timezone=time.strftime("%Z", time.gmtime())
		try:
			timezone=unicode(timezone, 'utf-8')
		except:
			try:
				timezone=unicode(timezone,locale.getpreferredencoding())
			except:
				timezone="Unknown"
		q.addElement('tz', content = timezone)
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
	
	def onRosterX(self, el):
		self.disp(el['id'])
		frm = el['from']
		x = el.firstChildElement()
		self._processRosterX(frm, x, el['id'])
	
	def _processRosterX(self, frm, x, id = None):
		# for now only additions are processed
		out = []
		for item in x.elements():
			action = item.getAttribute('action', 'add')
			if action == 'add':
				if self.getContactByJid(item['jid']) == None:
					groups = []
					for gr in item.elements():
						groups.append(unicode(gr))
					itm = item.attributes
					if len(groups)>0:
						itm['group'] = groups[0]
					out.append(itm)
		if len(out)>0:
			self.on_rosterx(frm, out, id)
	
	def _rosterxResult(self, frm, id, ok = False):
		if ok:
			iq = Element((None,'iq'))
			iq['to'] = frm
			iq['id'] = id
			iq['type'] = 'result'
		else:
			iq = Element((None,'iq'))
			iq['to'] = frm
			iq['id'] = id
			iq['type'] = 'error'
			error = iq.addElement('error')
			error['type'] = 'cancel'
			error['code'] = '501'
			error.addElement('not-authorized')
		self.xmlstream.send(iq)
		
	def disp(self, id):
		self.idlist.append(id)




