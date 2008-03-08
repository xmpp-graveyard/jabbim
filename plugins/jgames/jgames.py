try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
import sys
import os
sys.path.append('.')
from include import plugins, utils
from widgets import dataforms
import time
from twisted.words.protocols.jabber.xmlstream import IQ
from pyxl.xmlrpclib import loads, dumps

#class config:
	#def __init__(self,main):
		#self.main=main
		#self.config={}
		#self.config['on_first_message']={'type':'boolean','label':self.main.tr("Notify on first message from user"),'value':'True','groupbox':self.main.tr('Tray icon')}
		#self.config['on_muc_highlight']={'type':'boolean','label':self.main.tr("Notify if groupchat message contains your nickname"),'value':'True','groupbox':self.main.tr('Tray icon')}
		#self.config['sound_first_message']={'type':'boolean','label':self.main.tr("Play sound on first message from user"),'value':'True','groupbox':self.main.tr('Sounds')}
		#self.config['sound_gc_message']={'type':'boolean','label':self.main.tr("Play sound if groupchat message contains your nickname"),'value':'True','groupbox':self.main.tr('Sounds')}
		#self.config['sound_on_login']={'type':'boolean','label':self.main.tr("Play sound on login"),'value':'True','groupbox':self.main.tr('Sounds')}
		#self.config['osd_transparent']={'type':'boolean','label':self.main.tr("Use transparent background"),'value':'False','groupbox':self.main.tr('OSD')}
		#self.config['osd_time']={'type':'number-spin','label':self.main.tr("Display time (seconds):"),'value':'2','groupbox':self.main.tr('OSD')}
		#self.config['osd_on_presence']={'type':'boolean','label':self.main.tr("Use OSD for presences"),'value':'True','groupbox':self.main.tr('OSD')}
		#self.config['osd_on_message']={'type':'boolean','label':self.main.tr("Use OSD for messages"),'value':'True','groupbox':self.main.tr('OSD')}

		#self.config['osd_x']={'type':'hidden','label':self.main.tr("Use OSD for presences"),'value':'10','groupbox':self.main.tr('OSD')}
		#self.config['osd_y']={'type':'hidden','label':self.main.tr("Use OSD for presences"),'value':'10','groupbox':self.main.tr('OSD')}

class board(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self,None)
		self.x=None
		self.y=None
		self.setMinimumWidth(480)
		self.setMinimumHeight(480)
	
	def paintEvent(self,event):
		if self.x:
			QtGui.QWidget.paintEvent(self,event)
			painter=QtGui.QPainter(self)
			painter.setClipping(True)
			painter.setClipRegion(event.region())
			painter.drawPixmap(self.x,self.y,self.img)

class gameObj:
	def __init__(self, gid, plugin):
		self.gid = gid
		self.plugin = plugin
		self.functions = {'test':self.test} # function name:method
		self.dialog=board()
		self.dialog.img=QtGui.QPixmap(self.plugin.pluginDir+'/img.png')
	
	def test(self,neco,data):
		x,y=data
		self.dialog.x=int(x)
		self.dialog.y=int(x)
		self.dialog.repaint()
	
	def dispatchUpdate(self, call, id, frm):
		if call[1] in self.functions:
			d = self.functions[call[1]](frm,call[0])
			if d:
				d.addCallback(self.plugin._replyUpdate, call[1], frm, id)
			else:
				print 'chyba!', d
	
	

class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'jgames'
		self.description = 'JGames - games over Jabber'
		self.author = "Jan 'HanzZ' Kaluza"
		self.name = 'JGames'
		self.version = '0.1'
		self.category = ['jgames']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.installTranslator()
		#self.configDialog=config(self)
		#self.showInPreferences=True
		#self.preferencesIcon=QtGui.QIcon(plugindir+"/audio.png")
		self.games = {} # gid:GameObj
		if main:
			self.loadConfig()
			self.browser=self.loadDialog(self.pluginDir+"/browser_ui.py",self.main)
			QtCore.QObject.connect(self.browser,QtCore.SIGNAL("accepted()"),self.joinGame)
			self.browser.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setText(self.tr("Join"))
			self.group=QtGui.QButtonGroup(self.main)
			QtCore.QObject.connect(self.group,QtCore.SIGNAL("buttonClicked ( QAbstractButton * )"),self.buttonClicked)
			self.main.client.xmlstream.addObserver("/iq[@type='set'][@id]/query[@xmlns='games.jabbim.cz']/update", self.onUpdate)
			self.main.client.xmlstream.addObserver("/iq[@type='set'][@id]/query[@xmlns='games.jabbim.cz']/start", self.onStart)
		else:
			self.loadConfig(homedir)
	
	def onStart(self, el):
		self.main.client.disp(el['id'])
		q = el.firstChildElement()
		gid = q['gid']
		self.games[gid].dialog.show()
			
	def getSession(self, gid):
		return self.games.get(gid, None)
	
	def onUpdate(self, el):
		self.main.client.disp(el['id'])
		q = el.firstChildElement()
		l = q.firstChildElement()
		call = loads(l.firstChildElement().toXml())
		ss = self.getSession(q['gid'])
		if ss!=None:
			ss.dispatchUpdate(call, el['id'], el['from'])
	
	def _replyUpdate(self, result, func, frm, id):
		iq = Element((None, 'iq'))
		iq ['to'] = frm
		iq['type'] = 'result'
		iq['id'] = id

		q = iq.addElement('query', 'games.jabbim.cz')
		q['gid'] = self.gid
		i = q.addElement('input')
		i.addRawXml(dumps(result, methodresponse = True))
		print iq.toXml()
		self.main.client.xmlstream.send(iq)
	
	def getConfig(self, gid):
		iq = IQ(self.main.client.xmlstream, 'get')
		iq['xml:lang'] = self.main.client.xmlLang
		iq['type'] = 'get'
		iq['to'] = 'games.jabbim.cz'
		q = iq.addElement('query')
		q['xmlns']='games.jabbim.cz'
		q['gid'] = gid
		q.addElement('config')
		self.main.client.disp(iq['id'])
		d = iq.send()
	#	self.on_xml(iq.toXml())
		d.addCallback(self._onConfigArrive).addErrback(self.main.client.chyba)
		return d
	
	def _onConfigArrive(self, el):
		q = el.firstChildElement()
		return q.firstChildElement() #dataform
	
	def setConfig(self, gid, data):
		iq = IQ(self.main.client.xmlstream, 'set')
		iq['xml:lang'] = self.main.client.xmlLang
		iq['type'] = 'set'
		iq['to'] = 'games.jabbim.cz'
		q = iq.addElement('query')
		q['xmlns']='games.jabbim.cz'
		q['gid'] = gid
		q.addElement('config')
		x = q.addChild(data)
		x['type'] = 'submit'
		self.main.client.disp(iq['id'])
		d = iq.send()
		return d
	
	def createGame(self, game, description = None):
		iq = IQ(self.main.client.xmlstream, 'set')
		iq['xml:lang'] = self.main.client.xmlLang
		iq['type'] = 'set'
		iq['to'] = 'games.jabbim.cz'
		q = iq.addElement('query')
		q['xmlns']='games.jabbim.cz'
		s = q.addElement('session')
		s['game'] = game
		if description != None:
			s['desc'] = description
		self.main.client.disp(iq['id'])
		d = iq.send()
		d.addCallback(self._gameCreated)
		return d
	
	def _gameCreated(self, el):
		q = el.firstChildElement()
		s = q.firstChildElement()
		return s['gid'], s['muc'], s['owner']
		
	def listGames(self, game):
		iq = IQ(self.main.client.xmlstream, 'get')
		iq['xml:lang'] = self.main.client.xmlLang
		iq['type'] = 'get'
		iq['to'] = 'games.jabbim.cz'
		q = iq.addElement('query')
		q['xmlns']='games.jabbim.cz'
		s = q.addElement('list')
		s['game'] = game
		s['action'] = 'list'
		self.main.client.disp(iq['id'])
		d = iq.send()
		d.addCallback(self._gameList)
		return d
	
	def _gameList(self, el):
		print 'received gamelist'
		q = el.firstChildElement()
		l = q.firstChildElement()
		print l.toXml()
		out = []
		for item in l.elements():
			print item.toXml()
			out.append(item.attributes)
		return out

	def buildMainWindowMenu(self):
		menu=self.mainWindowMenu()
		menu.addAction(self.tr("Create new game"),self.testSlot)
		menu.addAction(self.tr("Browse games"),self.gameList)

	def gameList(self):
		d=self.listGames('basic')
		d.addCallback(self._gamesList)

	def _gamesList(self,data):
		# [{u'status': u'pregame', u'gid': u'b2f321292c7eaa57d702a1f9d48aa5bd261453cf', u'muc': u'b2f321292c7eaa57d702a1f9d48aa5bd261453cf@conf.netlab.cz', u'desc': u'popis hry'},
		# {u'status': u'pregame', u'gid': u'72f0c572afba24fdaf5504f19bafa26e14f81491', u'muc': u'72f0c572afba24fdaf5504f19bafa26e14f81491@conf.netlab.cz', u'desc': u'popis hry'},
		# {u'status': u'pregame', u'gid': u'8a2ea894693e5599a7f6640b68f28f24b01ae502', u'muc': u'8a2ea894693e5599a7f6640b68f28f24b01ae502@conf.netlab.cz', u'desc': u'popis hry'}]
		self.browser.ui.treeWidget.clear()
		for game in data:
			item=QtGui.QTreeWidgetItem(self.browser.ui.treeWidget)
			item.setText(0,game['status'])
			item.setText(1,game['desc'])
			item.setData(0,32,QtCore.QVariant(unicode(game['muc'])))
			item.setData(1,32,QtCore.QVariant(unicode(game['gid'])))
		self.browser.show()

	def testSlot(self):
		print "new game slot"
		d=self.createGame('basic')
		d.addCallback(self.gameCreated)

	def gameCreated(self,data):
		if not data:
			return
		gid,muc,owner=data
		print "game created",gid,muc
		print "requesting config"
		self.games[gid] = gameObj(gid, self)
		d=self.getConfig(gid)
		d.addCallback(self.configReceived,gid,muc)
	
	def configReceived(self,form,gid,muc):
		print form,gid
		if form!=None:
			self.dialog=dataforms.abstractDataFormsDialog(self.main,form,"games.jabbim.cz",None,self.main)
			QtCore.QObject.connect(self.dialog,QtCore.SIGNAL("accepted()"),self.sendConfig)
			self.dialog.gid=gid
			self.dialog.muc=muc
			self.dialog.show()

	def sendConfig(self):
		form=self.dialog.getForm()
		self.setConfig(self.dialog.gid,form)
		self.joinGame(self.dialog.muc,self.dialog.gid)
		#self.listGames('basic').addCallback(self.test)

	def startGame(self,gid):
		iq = IQ(self.main.client.xmlstream, 'set')
		iq['xml:lang'] = self.main.client.xmlLang
		iq['type'] = 'set'
		iq['to'] = 'games.jabbim.cz'
		q = iq.addElement('query')
		q['xmlns']='games.jabbim.cz'
		q['gid']=str(gid)
		q.addElement('start')
		self.main.client.disp(iq['id'])
		d = iq.send()
		#d.addCallback(self._gameCreated)
		return d

	def buttonClicked(self,button):
		if button.typ=='start':
			self.startGame(button.gid)

	def joinGame(self,muc=None,gid=None):
		owner=True
		if not muc:
			item=self.browser.ui.treeWidget.currentItem()
			if not item:
				return
			muc=unicode(item.data(0,32).toString())
			gid=unicode(item.data(1,32).toString())
			owner=False
		if self.main.chat.addGroupChatTab(muc,self.main.client.jid.user,name="Game"):
			if owner:
				tab,index=self.main.chat.findTab(muc,True,['groupchat'])
				widget=QtGui.QWidget(tab.chat.ui.pluginWidget.parent())
				l=QtGui.QHBoxLayout(widget)
				button=QtGui.QToolButton()
				button.setText(self.tr('Configure game'))
				button.setToolTip(self.tr("Configure game"))
				button.setMinimumHeight(tab.chat.ui.sendButton.height())
				button.setMaximumHeight(tab.chat.ui.sendButton.height())
				l.addWidget(button)
				
				button=QtGui.QToolButton()
				button.setText(self.tr('Start game'))
				button.setToolTip(self.tr("Start game"))
				button.setMinimumHeight(tab.chat.ui.sendButton.height())
				button.setMaximumHeight(tab.chat.ui.sendButton.height())
				button.typ='start'
				button.gid=gid
				l.addWidget(button)
				self.group.addButton(button)

	
				tab.chat.ui.pluginWidget.parent().layout().addWidget(widget)
			self.main.client.joinGC(muc,self.main.client.jid.user)

	def test(self, res):
		print res

	def buildContactMenu(self,menu,contact):
		return
		self.action=menu.addAction(self.tr("Play Piskvorky"))
		self.action.setData(QtCore.QVariant(unicode(contact.jid)))
		self.action.setObjectName("jgames_piskvorky")
		#self.action.setIcon(QtGui.QIcon("%s/history.png" % self.pluginDir))
		QtCore.QObject.connect(self.action,QtCore.SIGNAL("triggered ( bool )"),self.testSlot)
	
