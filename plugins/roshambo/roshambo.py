import sys
sys.path.append('.')
import os,time, random, xmlrpclib
from include import plugins
from PyQt4 import QtCore, QtGui
from twisted.python import log
from twisted.words.protocols.jabber.xmlstream import IQ
from twisted.words.xish.domish import Element
from twisted.internet import threads

class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'roshambo'
		self.description = 'Kamen - nuzky - papir'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'Roshambo Plugin'
		self.version = '0.042'
		self.category = ['jgames']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.sessions = {}
		#self.config['notify'] = {'description':'', 'default':'True', 'value': '','type':'boolean'}
		if main:
			self.loadConfig()
			self.invite = uic.loadUi("%s/invite.ui" % self.pluginDir)
			self.invite.setWindowIcon(self.main.windowIcon())
			QtCore.QObject.connect(self.invite.pushButton, QtCore.SIGNAL("clicked()"), self.sendInvite)
			self.registerHandler('on_authd', self.authd)
# 			QtCore.QObject.connect(self.window.enableBox, QtCore.SIGNAL("stateChanged(int)"),self.enableToggled)
# 			QtCore.QObject.connect(self.window.clearButton, QtCore.SIGNAL("clicked()"),self.clearLog)
	
	def authd(self):
		self.main.client.xmlstream.addObserver("/iq[@type='set'][@id]/x[@xmlns='jabbim:games']/game", self.onInvite)
		self.main.client.xmlstream.addObserver("/iq[@type='set'][@id]/query[@xmlns='jabber:iq:rpc'][@sid]", self.onRPC)
		return True
	
	def buildRosterMenu(self):
		menu=self.rosterMenu()
		menu.addAction("Challenge!",self.showSlot)
		
	
	def showSlot(self):
		self.invite.comboBox.clear()
		for user in self.main.client.roster['users'].itervalues():
			if len(user.resources)>0:
				log.msg(unicode(user.resources))
				self.invite.comboBox.addItem(user.jid)
		self.invite.show()
	
	def sendInvite(self):
		jid = self.invite.comboBox.currentText()
		resource = self.main.client.roster['users'][unicode(jid)].getHighestResource()
		iq = IQ(self.main.client.xmlstream, 'set')
		iq['to'] = unicode(jid)+'/'+resource
		q = iq.addElement('x', 'jabbim:games')
		q.addElement('game', content = 'roshambo')
		sid = str(random.randint(1000, sys.maxint))
		self.sessions[sid] = Session(self, sid, unicode(jid) +'/'+resource, True)
		q['sid'] = sid
		self.main.client.disp(iq['id'])
		d = iq.send()
		self.main.client.on_xml(iq.toXml())
		d.addCallback(self._onInvite, sid).addErrback(self._onInviteErr, sid)
		self.invite.hide()
	
	def _onInvite(self, el, sid):
		log.msg('invite accepted!')
		self.sessions[sid].ui.log.append('invite accepted!')
		self.sessions[sid].ui.send.setEnabled(True)
		
	def _onInviteErr(self, err, sid):
		log.msg('invite not accepted')
		self.sessions[sid].ui.log.append('invite not accepted!')
	
	def onInvite(self, el):
		log.msg('invite received')
		self.main.client.disp(el['id'])
		iq = Element((None,'iq'))
		iq['to'] = el['from']
		iq['type'] = 'result'
		iq['id'] = el['id']
		q = iq.addElement('x','jabbim:games')
		sid = el.firstChildElement()['sid']
		self.sessions[sid] = Session(self, sid, el['from'], False)
		self.main.client.on_xml(iq.toXml())
		self.main.client.xmlstream.send(iq)
		log.msg('reply sent')
	
	def onRPC(self, el):
		self.main.client.disp(el['id'])
		query = el.firstChildElement()
		sid = query['sid']
		reply = False
		if sid in self.sessions:
			reply = self.sessions[sid].receiveRPC(query.firstChildElement().toXml())
		if reply != False:
			iq = Element((None,'iq'))
			iq['to'] = el['from']
			iq['type'] = 'result'
			iq['id'] = el['id']
			q = iq.addElement('query','jabber:iq:rpc')
			q['sid'] = sid
			q.addRawXml(reply)
			self.main.client.on_xml(iq.toXml())
			self.main.client.xmlstream.send(iq)
		
		else:
			pass #zpracujeme chybu nejak
	
	def remove(self):
		plugins.PluginBase.remove()
		self.main.client.xmlstream.removeObserver("/iq[@type='set'][@id]/x[@xmlns='jabbim:games']/game", self.onInvite)
		self.main.client.xmlstream.removeObserver("/iq[@type='set'][@id]/query[@xmlns='jabber:iq:rpc'][@sid]", self.onRPC)

class Session:
	def __init__(self,plugin, sid, jid, ini):
		self. sid = sid
		self.ini = ini
		self.plugin = plugin
		self.jid = jid
		self.ui = uic.loadUi("%s/game.ui" % self.plugin.pluginDir)
		self.score = {'ja':0, 'on':0}
		self.turn = 0
		self.rpc = {'ready': self.onReady, 'turn': self.onTurn, 'quit': self.onQuit}
		self.state = 'waiting'
		self.opstate = 'waiting'
		self.ui.show()
		QtCore.QObject.connect(self.ui.cancel, QtCore.SIGNAL("clicked()"), self.cancel)
		QtCore.QObject.connect(self.ui.send, QtCore.SIGNAL("clicked()"), self.ready)
	
	def ready(self):
		self.ui.log.append('we are ready')
		self.state = 'ready'
		self.ui.send.setEnabled(False)
		if self.ui.kamen.isChecked():
			self.turn = 'rock'
		elif self.ui.nuzky.isChecked():
			self.turn = 'scissors'
		elif self.ui.papir.isChecked():
			self.turn = 'paper'
		command = xmlrpclib.dumps((self.state,), 'ready').replace("<?xml version='1.0'?>", '')
		self.sendRPC(command).addCallback(self._readyOK).addErrback(self._readyFail)
# 		if self.opstate == 'ready':
# 			command = xmlrpclib.dumps((self.turn,), 'turn').replace("<?xml version='1.0'?>", '')
# 			self.sendRPC(command)
			
	def _readyOK(self, el):
		pass
	
	def _readyFail(self, err):
		self.state = 'error'
		self.ui.log.append('something bad happened')
	
	def cancel(self):
		#pridat informaci pro druhou stranu
		command = xmlrpclib.dumps((self.score,), 'quit').replace("<?xml version='1.0'?>", '')
		self.sendRPC(command)
		self.ui.destroy()
		del self.plugin.sessions[self.sid]
	
	def sendRPC(self, command):
		iq = IQ(self.plugin.main.client.xmlstream, 'set')
		iq['to'] = self.jid
		q = iq.addElement('query', 'jabber:iq:rpc')
		q['sid'] = self.sid
		q.addRawXml(command)
		self.plugin.main.client.disp(iq['id'])
		d = iq.send()
		self.plugin.main.client.on_xml(iq.toXml())
		return d
	
	def receiveRPC(self, xml):
		command = xmlrpclib.loads(xml)
		log.msg(unicode(command))
		reply = False
		if self.rpc.has_key(command[1]):
			reply = self.rpc[command[1]](command[0])
		else:
			reply = False
		return reply
		

	
	def onReady(self, cmd):
		log.msg('oponent is ready')
		self.ui.log.append('oponent is ready')
		self.opstate = 'ready'
		if self.ini:
			log.msg('let\'s go!')
			command = xmlrpclib.dumps((self.turn,), 'turn').replace("<?xml version='1.0'?>", '')
			self.sendRPC(command)
		else:
			self.ui.send.setEnabled(True)
		return xmlrpclib.dumps((), 'ready', True).replace("<?xml version='1.0'?>", '')
	
	def onTurn(self, cmd):
		self.ui.log.append('%s vs %s'%(self.turn, cmd[0]))
		ja = self.turn
		on = cmd[0]
		win = None
		if ja == on:
			win = None
		elif ja == 'rock' and on == 'scissors':
			win = True
		elif ja == 'paper' and on == 'rock':
			win = True
		elif ja == 'scissors' and on == 'paper':
			win = True
		else:
			win = False
		if win == True:
			self.ui.log.append('VICTORY!')
			self.score['ja'] = self.score['ja'] +1
		elif win == False:
			self.ui.log.append('Your oponent was lucky this time. Try it again!')
			self.score['on'] = self.score['on'] +1
		else:
			self.ui.log.append('It\'s a tie! Try it again!')
		self.ui.log.append('Score: %d vs %d'%(self.score['ja'], self.score['on']))
		if not self.ini:
			command = xmlrpclib.dumps((self.turn,), 'turn').replace("<?xml version='1.0'?>", '')
			self.sendRPC(command)
		else:
			self.ui.send.setEnabled(True)
		
		
		
	
	def onQuit(self, cmd):
		self.ui.log.append('Other side has left the battlefield')
		self.ui.send.setEnabled(False)

	
		

