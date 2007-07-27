import sys,os,time, random
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui, uic
from twisted.python import log
from twisted.words.protocols.jabber.xmlstream import IQ
from twisted.words.xish.domish import Element

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'roshambo'
		self.description = 'Kamen - nuzky - papir'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'Roshambo Plugin'
		self.version = '0.007'
		self.category = ['jgames']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.sessions = {}
		#self.config['notify'] = {'description':'', 'default':'True', 'value': '','type':'boolean'}
		if main:
			self.loadConfig()
			self.invite = uic.loadUi("%s/plugins/%s/invite.ui"%(self.homeDir, self.fname))
			self.invite.setWindowIcon(self.main.windowIcon())
			QtCore.QObject.connect(self.invite.pushButton, QtCore.SIGNAL("clicked()"), self.sendInvite)
			
# 			QtCore.QObject.connect(self.window.enableBox, QtCore.SIGNAL("stateChanged(int)"),self.enableToggled)
# 			QtCore.QObject.connect(self.window.clearButton, QtCore.SIGNAL("clicked()"),self.clearLog)
			
	def buildRosterMenu(self):
		menu=self.rosterMenu()
		menu.addAction("Challenge!",self.showSlot)
		self.main.client.xmlstream.addObserver("/iq[@type='set'][@id]/x[@xmlns='jabbim:games']/game", self.onInvite)
	
	def showSlot(self):
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
		self.sessions[sid] = Session(self, sid, unicode(jid) +'/'+resource)
		q['sid'] = sid
		self.main.client.disp(iq['id'])
		d = iq.send()
		self.main.client.on_xml(iq.toXml())
		d.addCallback(self._onInvite, sid).addErrback(self._onInviteErr, sid)
		self.invite.hide()
	
	def _onInvite(self, el, sid):
		log.msg('invite accepted!')
		self.sessions[sid].ui.log.append('invite accepted!')
		self.sessions[sid].ui.send.enable()
		
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
		self.main.client.on_xml(iq.toXml())
		self.main.client.xmlstream.send(iq)
		

class Session:
	def __init__(self,plugin, sid, jid):
		self. sid = sid
		self.plugin = plugin
		self.jid = jid
		self.ui = uic.loadUi("%s/plugins/%s/game.ui"%(self.plugin.homeDir, self.plugin.fname))
		self.score = {'ja':0, 'on':0}
		self.turn = 0
		self.ui.show()
		QtCore.QObject.connect(self.ui.cancel, QtCore.SIGNAL("clicked()"), self.cancel)
	
	def cancel(self):
		#pridat informaci pro druhou stranu
		self.ui.destroy()
		del self.plugin.sessions[self.sid]

