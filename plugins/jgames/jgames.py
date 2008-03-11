try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
import sys
import os
sys.path.append('.')
from include import plugins, utils
from widgets import dataforms,groupchat
import time
from twisted.words.protocols.jabber.xmlstream import IQ
from pyxl.xmlrpclib import loads, dumps
from twisted.words.xish.domish import Element
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

class gameWidget(groupchat.groupChatWidget):
	def __init__(self,main,jid,tab,nickname="",parent=None,ui=None):
		groupchat.groupChatWidget.__init__(self,main,jid,tab,nickname="",parent=None,ui=ui)
		self.ui.info.hide()
		self.ui.selfAvatar.hide()
	
	def editUser(self,nick,status,role=None,affiliation=None):
		groupchat.groupChatWidget.editUser(self,nick,status,role,affiliation)
		self.ui.users.setMinimumHeight((len(self.main.client.groupchats[self.jid].users)+self.ui.users.topLevelItemCount())*32)
		self.ui.users.setMaximumHeight((len(self.main.client.groupchats[self.jid].users)+self.ui.users.topLevelItemCount())*32)

class board(QtGui.QWidget):
	def __init__(self,parent):
		QtGui.QWidget.__init__(self,parent)
		self.side=20
		self.first=None
		self.second=None
		self.countX=25
		self.countY=25
		self.desk=[]
		self.x=QtGui.QPixmap("images/piskvorky/x.png")
		self.o=QtGui.QPixmap("images/piskvorky/o.png")
		self.turn=""
		self.variable=0
		self.last=[]
		self.firstSymbol=None
		self.secondSymbol=None
		self.state=[None,""]
	
	def mouseReleaseEvent(self,qe):
		if self.gameObj.plugin.main.getJid(self.turn).userhost()==self.gameObj.plugin.main.client.jid.userhost():
			x=qe.x()/self.side
			y=qe.y()/self.side
			if (x+1>self.countX or y+1>self.countY) or (x+1<0 or y+1<0):
				print "You clicked out of desk."
			elif self.desk[y][x]!=0:
				print "Field is not free."
			else:
				self.desk[y][x]=self.variable
				self.repaint()
				self.turn="a@b.cz"
				self.gameObj.plugin.sendInput('update', ((x,y,self.variable),), 'games.jabbim.cz', self.gameObj.gid)
	
	def paintEvent(self,event):
		if self.countX:
			QtGui.QWidget.paintEvent(self,event)
			painter=QtGui.QPainter(self)
			painter.setClipping(True)
			painter.setClipRegion(event.region())
			painter.setRenderHint(painter.Antialiasing)

			painter.setPen(QtGui.QPen(QtGui.QColor(200,200,200), 1))
			painter.fillRect(0,0,self.countX*self.side,self.countY*self.side,QtGui.QBrush(QtGui.QColor(255,255,255)))

			for x in range(self.countX+1):
				painter.drawLine(x*self.side,0,x*self.side,self.countY*self.side)
			for y in range(self.countY+1):
				painter.drawLine(0,y*self.side,self.countX*self.side,y*self.side)
			for y in range(len(self.desk)):
				for x in range(len(self.desk[y])):
					if self.desk[y][x]==-1:
						painter.drawPixmap(x*self.side,y*self.side,self.x)
					elif self.desk[y][x]==1:
						painter.drawPixmap(x*self.side,y*self.side,self.o)
			
			painter.setPen(QtGui.QPen(QtCore.Qt.green, 3))
			if len(self.last)!=0:
				painter.drawRect(self.last[0]*self.side,self.last[1]*self.side,self.side,self.side)
			if self.state[0]:
				f=painter.font()
				f.setPixelSize(60)
				painter.setFont(f)
				painter.setPen(QtGui.QPen(QtCore.Qt.black, 3))
				if self.state[0]=='victory':
					if self.gameObj.plugin.main.getJid(self.state[1]).userhost()==self.gameObj.plugin.main.client.jid.userhost():
						painter.drawText(0,0,self.width(),self.height(), QtCore.Qt.AlignCenter, "You WIN!")
					else:
						painter.drawText(0,0,self.width(),self.height(), QtCore.Qt.AlignCenter, "You LOSE!")

class gameObj:
	def __init__(self, gid, plugin,tab):
		self.gid = gid
		self.plugin = plugin
		self.functions = {}
		self.functions['updateStatus']=self.updateStatus
		self.functions['update']=self.update
		self.functions['turn']=self.turn
		self.tab=tab
		gameWidget=tab.ui.gameWidget
		l=QtGui.QHBoxLayout(gameWidget)
		
		
		self.dialog=board(gameWidget)
		self.dialog.gameObj=self
		self.dialog.img=QtGui.QPixmap(self.plugin.pluginDir+'/img.png')
		l.addWidget(self.dialog)
		self.dialog.setMinimumSize(self.dialog.countX*self.dialog.side+2,self.dialog.countY*self.dialog.side+2)
		self.dialog.setMaximumSize(self.dialog.countX*self.dialog.side+2,self.dialog.countY*self.dialog.side+2)

	def turn(self,jid,data):
		jid=data[0]
		self.dialog.turn=jid
		if self.plugin.main.getJid(self.dialog.first).userhost()==self.plugin.main.getJid(self.dialog.turn).userhost():
			if self.dialog.firstSymbol==-1:
				file="images/piskvorky/x.png"
			else:
				file="images/piskvorky/o.png"
		else:
			if self.dialog.secondSymbol==-1:
				file="images/piskvorky/x.png"
			else:
				file="images/piskvorky/o.png"
		message=' <img src="%s"/> '%(file)+jid+' is on the turn'
		message=self.plugin.main.skin["status_message"].replace("[time]",self.plugin.main.now()).replace('[message]',message)
		self.tab.textEditWrite(message)

	def update(self,jid,data):
		for change in data:
			x=change[0]
			y=change[1]
			var=change[2]
			self.dialog.last=[x,y]
			self.dialog.desk[y][x]=var
		self.dialog.repaint()

	def updateStatus(self,jid,data):
		# data=({'y': 25, 'x': 25, 'second': 'hanzz@njs.netlab.cz/jabbimKubuntu', 'first': 'pyjim@jabber.cz/jabbimSvn'},)
		data=data[0]
		if data.has_key('y'):
			self.dialog.countY=data['y']
		if data.has_key('x'):
			self.dialog.countX=data['x']
		if data.has_key('first'):
			self.dialog.first=data['first']
		if data.has_key('second'):
			self.dialog.first=data['second']
		if data.has_key('firstSymbol'):
			self.dialog.firstSymbol=int(data['firstSymbol'])
		if data.has_key('secondSymbol'):
			self.dialog.secondSymbol=int(data['secondSymbol'])
		if self.plugin.main.getJid(self.dialog.first).userhost()==self.plugin.main.client.jid.userhost():
			self.dialog.variable=self.dialog.firstSymbol
		else:
			self.dialog.variable=self.dialog.secondSymbol

		if len(self.dialog.desk)==0:
			for y in range(self.dialog.countY):
				ar=[]
				for x in range(self.dialog.countX):
					ar.append(0)
				self.dialog.desk.append(ar)
		self.dialog.setMinimumSize(self.dialog.countX*self.dialog.side+2,self.dialog.countY*self.dialog.side+2)
		self.dialog.setMaximumSize(self.dialog.countX*self.dialog.side+2,self.dialog.countY*self.dialog.side+2)
		self.dialog.show()
		self.dialog.repaint()
	
	def dispatchUpdate(self, call, id, frm):
		if call[1] in self.functions:
			d = self.functions[call[1]](frm,call[0])
			if d:
				d.addCallback(self.plugin._replyUpdate, call[1], frm, id, self.gid)
			elif d == None:
				self.plugin._replyUpdate((True,), call[1], frm, id, self.gid)
			else:
				print 'chyba!', d
	def finish(self, attr, reason):
		#v attr je type, value: typ = victory/error/restart, value= JID .. nebo tak neco ;)
		#2008/03/11 14:44 +0200 [-] {u'type': u'victory', u'value': u'pyjim@jabber.cz/jabbimSvn'}
		#2008/03/11 14:44 +0200 [-] ['__class__', '__cmp__', '__contains__', '__delattr__', '__delitem__', '__doc__', '__eq__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__str__', 'clear', 'copy', 'fromkeys', 'get', 'has_key', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']
		self.dialog.state=[attr['type'],attr['value']]
		self.dialog.repaint()
	
	

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
			self.jgamesWidget=self.loadModule(self.pluginDir+"/jgameswidget_ui.py")
			QtCore.QObject.connect(self.group,QtCore.SIGNAL("buttonClicked ( QAbstractButton * )"),self.buttonClicked)
			self.main.client.xmlstream.addObserver("/iq[@type='set'][@id]/query[@xmlns='games.jabbim.cz']/update", self.onUpdate, priority = 1)
			self.main.client.xmlstream.addObserver("/iq[@type='set'][@id]/query[@xmlns='games.jabbim.cz']/start", self.onStart, priority = 1)
			self.main.client.xmlstream.addObserver("/iq[@type='set'][@id]/query[@xmlns='games.jabbim.cz']/finish", self.onFinish, priority = 1)
		else:
			self.loadConfig(homedir)
	
	def on_remove(self):
		print "REMOVING JGAMES PLUGIN"
		self.main.client.xmlstream.removeObserver("/iq[@type='set'][@id]/query[@xmlns='games.jabbim.cz']/update", self.onUpdate)
		self.main.client.xmlstream.removeObserver("/iq[@type='set'][@id]/query[@xmlns='games.jabbim.cz']/start", self.onStart)
		self.main.client.xmlstream.removeObserver("/iq[@type='set'][@id]/query[@xmlns='games.jabbim.cz']/finish", self.onFinish)
		
	def onStart(self, el):
		frm = self.main.getJid(el['from'])
		if frm.host != 'games.jabbim.cz':
			return
		self.main.client.disp(el['id'])
		q = el.firstChildElement()
		gid = q['gid']
		self.games[gid].dialog.show()
	
	def onFinish(self, el):
		frm = self.main.getJid(el['from'])
		if frm.host != 'games.jabbim.cz':
			return
		self.main.client.disp(el['id'])
		q = el.firstChildElement()
		gid = q['gid']
		f = q.firstChildElement()
		ss = self.getSession(q['gid'])
		if ss!=None:
			ss.finish(f.attributes, unicode(f))
			
	def getSession(self, gid):
		return self.games.get(gid, None)
	
	def onUpdate(self, el):
		print 'update received'
		frm = self.main.getJid(el['from'])
		if frm.host != 'games.jabbim.cz':
			return
		self.main.client.disp(el['id'])
		q = el.firstChildElement()
		l = q.firstChildElement()
		call = loads(l.firstChildElement().toXml())
		ss = self.getSession(q['gid'])
		if ss!=None:
			ss.dispatchUpdate(call, el['id'], el['from'])
	
	def _replyUpdate(self, result, func, frm, id, gid):
		iq = Element((None, 'iq'))
		iq ['to'] = frm
		iq['type'] = 'result'
		iq['id'] = id

		q = iq.addElement('query', 'games.jabbim.cz')
		q['gid'] = gid
		i = q.addElement('input')
		i.addRawXml(dumps(result, methodresponse = True))
		print iq.toXml()
		self.main.client.xmlstream.send(iq)
	
	
	def sendInput(self, func, params, komu, gid):
		iq = IQ(self.main.client.xmlstream, 'set')
		iq['type'] = 'set'
		iq['to'] = komu
		q = iq.addElement('query')
		q['xmlns']='games.jabbim.cz'
		q['gid'] = gid
		up = q.addElement('input')
		up.addRawXml(dumps(params, func, False))
		self.main.client.disp(iq['id'])
		d = iq.send().addCallback(self._onInputResult)
		return d
		
	def _onInputResult(self, el):
		query = el.firstChildElement()
		up = query.firstChildElement()
		call = loads(up.firstChildElement().toXml())
		return call
	
	
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
	
	def createGame(self, game, description = None, gid = None):
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
		if gid != None:
			s['gid'] = gid
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
		d=self.listGames('piskvorky')
		d.addCallback(self._gamesList)

	def _gamesList(self,data):
		# [{u'status': u'pregame', u'gid': u'b2f321292c7eaa57d702a1f9d48aa5bd261453cf', u'muc': u'b2f321292c7eaa57d702a1f9d48aa5bd261453cf@conf.netlab.cz', u'desc': u'popis hry'},
		# {u'status': u'pregame', u'gid': u'72f0c572afba24fdaf5504f19bafa26e14f81491', u'muc': u'72f0c572afba24fdaf5504f19bafa26e14f81491@conf.netlab.cz', u'desc': u'popis hry'},
		# {u'status': u'pregame', u'gid': u'8a2ea894693e5599a7f6640b68f28f24b01ae502', u'muc': u'8a2ea894693e5599a7f6640b68f28f24b01ae502@conf.netlab.cz', u'desc': u'popis hry'}]
		self.browser.ui.treeWidget.clear()
		for game in data:
			item=QtGui.QTreeWidgetItem(self.browser.ui.treeWidget)
			item.setText(0,game['status'])
			if game.has_key('desc'):
				item.setText(1,game['desc'])
			item.setData(0,32,QtCore.QVariant(unicode(game['muc'])))
			item.setData(1,32,QtCore.QVariant(unicode(game['gid'])))
		self.browser.show()

	def testSlot(self):
		print "new game slot"
		d=self.createGame('piskvorky')
		d.addCallback(self.gameCreated)

	def gameCreated(self,data):
		if not data:
			return
		gid,muc,owner=data
		print "game created",gid,muc
		print "requesting config"
		#self.games[gid] = gameObj(gid, self)
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

	def showConfigDialog(self,gid):
		d=self.getConfig(gid)
		d.addCallback(self.configReceived2,gid)

	def configReceived2(self,form,gid):
		if form!=None:
			self.dialog=dataforms.abstractDataFormsDialog(self.main,form,"games.jabbim.cz",None,self.main.chat)
			QtCore.QObject.connect(self.dialog,QtCore.SIGNAL("accepted()"),self.sendConfig2)
			self.dialog.gid=gid
			self.dialog.show()

	def sendConfig2(self):
		form=self.dialog.getForm()
		self.setConfig(self.dialog.gid,form)

	def sendConfig(self):
		form=self.dialog.getForm()
		self.setConfig(self.dialog.gid,form)
		self.joinGame(self.dialog.muc,self.dialog.gid)
		#self.listGames('piskvorky').addCallback(self.test)

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
		elif button.typ=='config':
			self.showConfigDialog(button.gid)
			

	def joinGame(self,muc=None,gid=None):
		owner=True
		if not muc:
			item=self.browser.ui.treeWidget.currentItem()
			if not item:
				return
			muc=unicode(item.data(0,32).toString())
			gid=unicode(item.data(1,32).toString())
			owner=False
		#def __init__(self,main,jid,tab,nickname="",parent=None,ui=Ui_groupchatwidget):
		if self.main.chat.addCustomTab(muc,self.main.client.jid.user,"Game",gameWidget,[self.main,muc,None,self.main.client.jid.user,None,self.jgamesWidget.Ui_groupchatwidget],'groupchat'):
			self.main.chat.activate()
			tab,index=self.main.chat.findTab(muc,True,['groupchat'])
			tab.chat.nick=self.main.client.jid.user
			tab.chat.on_owner=self.showAdminButtons
			tab.chat.gid=gid
			self.main.client.joinGC(muc,self.main.client.jid.user)
			self.games[gid] = gameObj(gid, self,tab.chat)
			self.createGame(game = 'piskvorky',gid=gid) #nekde predavej typ hry ..

	def showAdminButtons(self,tab):
		print "owner"
		#widget=QtGui.QWidget(tab.ui.pluginWidget.parent())
		#l=QtGui.QHBoxLayout(widget)
		l=tab.ui.pluginWidget.layout()
		button=QtGui.QToolButton()
		button.setText(self.tr('Configure game'))
		button.setToolTip(self.tr("Configure game"))
		button.setMinimumHeight(tab.ui.sendButton.height())
		button.setMaximumHeight(tab.ui.sendButton.height())
		button.typ='config'
		button.gid=tab.gid
		l.addWidget(button)
		self.group.addButton(button)
		
		button=QtGui.QToolButton()
		button.setText(self.tr('Start game'))
		button.setToolTip(self.tr("Start game"))
		button.setMinimumHeight(tab.ui.sendButton.height())
		button.setMaximumHeight(tab.ui.sendButton.height())
		button.typ='start'
		button.gid=tab.gid
		l.addWidget(button)
		self.group.addButton(button)

		#tab.ui.pluginWidget.parent().layout().addWidget(widget)

	def test(self, res):
		print res

	def buildContactMenu(self,menu,contact):
		return
		self.action=menu.addAction(self.tr("Play Piskvorky"))
		self.action.setData(QtCore.QVariant(unicode(contact.jid)))
		self.action.setObjectName("jgames_piskvorky")
		#self.action.setIcon(QtGui.QIcon("%s/history.png" % self.pluginDir))
		QtCore.QObject.connect(self.action,QtCore.SIGNAL("triggered ( bool )"),self.testSlot)
	
