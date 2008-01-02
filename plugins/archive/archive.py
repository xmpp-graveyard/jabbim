import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from urllib import quote, unquote
from twisted.python import log
from configobj import ConfigObj
from twisted.internet import threads
from twisted.words.protocols.jabber import jid as jidT

class calendar(QtGui.QCalendarWidget):
	def __init__(self,parent):
		QtGui.QCalendarWidget.__init__(self,parent)
		self.dates=[]
		self.setFirstDayOfWeek(QtCore.Qt.Monday)

	def setDates(self,dates):
		self.dates=dates
		if len(self.dates)!=0:
			self.setSelectedDate(self.dates[-1].addMonths(1))
			self.setSelectedDate(self.dates[-1])
		#self.repaint()

	def paintCell(self,painter,rect,date):
		#painter.save()
		#painter.translate(x,y)
		#painter.fillRect(rect,QtGui.QBrush(QtGui.QColor(255,0,0)))
		font=QtGui.QApplication.font()
		
		if not date in self.dates:
			painter.setFont(font)
			color=None
		else:
			font.setBold(True)
			painter.setFont(font)
			color=True
		if date==self.selectedDate():
			painter.fillRect(rect,QtGui.QBrush(self.palette().color(QtGui.QPalette.Highlight)))
			painter.setPen(self.palette().color(QtGui.QPalette.HighlightedText))
			painter.drawText(rect, QtCore.Qt.AlignCenter, str(date.day()))
		else:
			if int(date.month())==int(self.monthShown()):
				#painter.setPen(self.palette().color(QtGui.QPalette.Highlight))
				if color:
					painter.fillRect(rect,QtGui.QBrush(self.palette().color(QtGui.QPalette.AlternateBase)))
				painter.setPen(self.palette().color(QtGui.QPalette.Text))
				painter.drawText(rect, QtCore.Qt.AlignCenter, str(date.day()))
			else:
				painter.setPen(self.palette().color(QtGui.QPalette.Disabled,QtGui.QPalette.Text))
				painter.drawText(rect, QtCore.Qt.AlignCenter, str(date.day()))
				
		#painter.restore()
		#QtGui.QCalendarWidget.paintCell(self,painter,rect,date)


class FileBackend:
	def __init__(self,archive):
		#self.archive=archive
		self.homeDir=unicode(archive.main.homeDir)
		self.jid=unicode(archive.jid)

	def saveMessage(self, to, body, typ, subject, xhtml, direction):
		jid = quote(to.split('/')[0])
		t=time.time()
		d=time.localtime(t)
		dat=str(d[0])+"-"+str(d[1])+"-"+str(d[2])
		try:
			fp = open(self.homeDir+'/archive/'+self.jid+'/'+jid+'/'+dat+'.history', 'a')
		except:
			os.mkdir(self.homeDir+'/archive/'+self.jid+'/'+jid)
			fp = open(self.homeDir+'/archive/'+self.jid+'/'+jid+'/'+dat+'.history', 'a')
	
		if xhtml != None:
			telo = xhtml.replace('|', '&#124;').replace("\n","<br/>")
		else:
			telo = body.replace('|', '&#124;').replace("\n","<br/>")
		if typ=="groupchat":
			if len(to.split('/'))>1:
				jid=to.split('/')[1]

		if subject==None:
			subject=""
		subject=subject.replace('|', '&#124;').replace("\n","<br/>")
		#print unicode(subject)
		msg = '|'.join([unicode(t), direction, jid, typ, unicode(subject), telo])
		msg = msg.encode('utf8')
		fp.write(msg+'\n')
		fp.close()

	def getDates(self,jid):
		ret=[]
		for file in os.listdir(self.homeDir+'/archive/'+self.jid+'/'+jid):
			if file.split('.')[1]=="history":
				dat=file.split('.')[0]
				ret.append(dat)
		return ret

	def getMessages(self,jid,date,maxTime=None):
		try:
			fp = open(self.homeDir+'/archive/'+self.jid+'/'+jid+'/'+date+'.history')
		except:
			log.err('no history file')
			return None
		ret=[] # timestamp,direction,from,message
		#zpravy = fp.readlines()
		#print zpravy
		#for msg in zpravy:
			#print msg
		#msg=fp.readline()
		#while len(msg)==0:
		if not maxTime:
			for msg in fp.xreadlines():
				parsed=msg.split('|')
				ret.append([float(parsed[0]),str(parsed[1]),unicode(parsed[2],"utf8"),unicode(parsed[5],"utf8")])
		else:
			maxTime=maxTime.split(":") # [20,0,0]
			now=time.localtime()
			for msg in fp.xreadlines():
				parsed=msg.split('|')
				d=time.localtime(float(parsed[0]))
				#html+=action[5].replace("[time]",str(d[3])+":"+str(d[4])+":"+str(d[5]))
				intervalHour=abs(int(d[3])-int(now[3])) # 20
				intervalMin=abs(int(d[4])-int(now[4])) # 2
				intervalSec=abs(int(d[5])-int(now[5]))
				#if intervalHour>=24:
					#intervalHour-=24
				#if intervalMin>=60:
					#intervalMin-=60
				#if intervalSec>=60:
					#intervalSec-=60
				if intervalHour<int(maxTime[0]):
					ret.append([float(parsed[0]),str(parsed[1]),unicode(parsed[2],"utf8"),unicode(parsed[5],"utf8")])
				elif intervalHour<=int(maxTime[0]) and intervalMin<=int(maxTime[1]):
					ret.append([float(parsed[0]),str(parsed[1]),unicode(parsed[2],"utf8"),unicode(parsed[5],"utf8")])
		fp.close()
		return ret

	def getLastMessages(self,jid,count,maxTime):
		dates=self.getDates(jid)
		print dates
		if len(dates)==0:
			return ""
		d=dates[0]
		if maxTime=="0:0:0":
			newestStr=unicode(d)
			d=unicode(d).split('-')
			newest=QtCore.QDate(int(d[0]),int(d[1]),int(d[2]))
			for date in dates:
				d=unicode(date).split('-')
				d=QtCore.QDate(int(d[0]),int(d[1]),int(d[2]))
				if d>newest:
					newest=d
					newestStr=unicode(date)
		else:
			d=time.localtime()
			newestStr=str(d[0])+"-"+str(d[1])+"-"+str(d[2])

		
		messages=self.getMessages(jid,newestStr,maxTime)
		if not messages:
			return []
		return messages[-count:]


class config:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['messagesNumber']={'type':'number-spin','label':self.main.tr("Number of messages from last conversation, which are show in chat:"),'value':'5'}
		self.config['messagesTime']={'type':'time-interval','label':self.main.tr("Cas, po kterem se zpravy z posledni konverzace nezobrazi:"),'value':'1:0:0'}

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'archive'
		self.description = 'Message Archiving'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'Archive Plugin'
		self.version = '0.189'
		self.category = ['archive']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.developMode=True

		self.installTranslator()
		self.configDialog=config(self)


		if main:
			self.loadConfig(homedir)

			self.jid = quote(self.main.client.jid.userhost())
			self.backend=FileBackend(self)

			if not os.path.isdir(self.main.homeDir+'/archive'):
				os.mkdir(self.main.homeDir+'/archive')
					
			if not os.path.isdir(self.main.homeDir+'/archive/'+self.jid):
				os.mkdir(self.main.homeDir+'/archive/'+self.jid)
			self.registerHandler('on_message', self.on_message)
			self.registerHandler('on_GCmessage', self.on_message)
			self.registerHandler('on_message_send', self.on_message_send)
			self.loadConfig()
			self.window = self.loadWindow("%s/plugins/%s/historyBrowser.ui.py"%(self.homeDir, self.fname))
			self.window.setWindowIcon(self.main.windowIcon())
			layout=QtGui.QHBoxLayout(self.window.ui.calendarWidget)
			self.window.ui.calendar=calendar(self.window.ui.calendarWidget)
			layout.addWidget(self.window.ui.calendar)
			#log.msg(unicode(dir(self.window)))
			QtCore.QObject.connect(self.window.ui.seznam, QtCore.SIGNAL("itemClicked ( QTreeWidgetItem * , int ) "),self.itemClicked)
			QtCore.QObject.connect(self.window.ui.calendar, QtCore.SIGNAL("selectionChanged()"),self.calChanged)
			self.group=QtGui.QButtonGroup(self.window)
			QtCore.QObject.connect(self.group,QtCore.SIGNAL("buttonClicked ( QAbstractButton * )"),self.buttonClicked)
			self.skin=self.getConfig("skins/gajim.conf")
			self.window.ui.seznam.header().hide()
		else:
			self.loadConfig(homedir)

	def buildRosterMenu(self):
		menu=self.rosterMenu()
		menu.addAction("Archive browser",self.showSlot)
	
	def buttonClicked(self,button):
		jid=button.jid
		self.showSlot(jid)
		

	
	def buildChatWidget(self,jid,layout,widget):
		button=QtGui.QToolButton()
		#button.setText("History")
		button.setIconSize(QtCore.QSize(16,16))
		button.setIcon(QtGui.QIcon("%s/plugins/%s/history.png"%(self.homeDir, self.fname)))
		button.jid=unicode(jid)
		button.setToolTip("History")

		self.group.addButton(button)
		layout.addWidget(button)
		jid = jidT.JID(jid)
		if os.path.isdir(self.main.homeDir+'/archive/'+self.jid+'/'+quote(jid.userhost())):
			me=unicode(self.main.client.jid.user)
	
			
			user=self.main.ui.roster.getUserItems(unicode(jid.userhost()))
			if len(user)==0:
				user=self.main.ui.roster.getMetaItems(jid.userhost())
				if len(user)!=0:
					user=user[0]
			if len(user)!=0:
				#user=self.roster['users'][unicode(frm).rsplit("/")[0]].rosterItems[0]
				it=user[0]
				user=user[0].name
			else:
				it=None
				user=unicode(jid.full())
			
			avatar="<img src=\""+widget.file+"\" width=\"16\" height=\""+str(widget.avatarHeight/2)+"\" />"
			
			file=self.main.homeDir+'/avatars/'+unicode(self.main.client.jid.userhost())
			if not os.path.isfile(file):
				file="images/32x32/apps/jabbim.png"
			selfavatar="<img src=\""+file+"\" width=\"16\" height=\""+str(widget.selfHeight/2)+"\" />"
	
			
			jid=unicode(jid.userhost())
			jid = quote(jid)
			d=threads.deferToThread(self.getLastMessages,jid,int(self.config['messagesNumber']),me,user,unicode(self.main.skin["my_message_history"]),unicode(self.main.skin["message_history"]),self.main.skin['color1'],avatar,selfavatar,self.config['messagesTime'])
			d.addCallback(self.gotLastMessages,widget)
			#html=self.getLastMessages(jid,5,me,user,unicode(self.main.skin["my_message"]),unicode(self.main.skin["message"]),self.main.skin['color1'])
			#self.gotLastMessages(html,widget)

	def gotLastMessages(self,html,widget):
		print "got last messages"
		old=widget.ui.textEdit.toHtml()
		widget.ui.textEdit.setHtml("")
		widget.textEditWrite(html,True)
		widget.textEditWrite(old)
		

	def buildGroupchatWidget(self,jid,layout,widget):
		button=QtGui.QToolButton()
		#button.setText("History")
		button.setIconSize(QtCore.QSize(16,16))
		button.setIcon(QtGui.QIcon("%s/plugins/%s/history.png"%(self.homeDir, self.fname)))
		button.jid=unicode(jid)
		button.setToolTip("History")

		self.group.addButton(button)
		layout.addWidget(button)

	
	def showSlot(self,j=None):
		self.window.ui.seznam.clear()
		self.window.ui.calendar.setDates([])
		self.window.ui.text.setText('')
		contact=QtGui.QTreeWidgetItem(self.window.ui.seznam)
		contact.setText(0,self.tr("Contacts in roster"))
		others=QtGui.QTreeWidgetItem(self.window.ui.seznam)
		others.setText(0,self.tr("Others"))
		self.window.ui.seznam.expandItem(contact)
		self.window.ui.seznam.expandItem(others)
		contact.setBackground(0,QtGui.QBrush(self.window.ui.seznam.palette().color(QtGui.QPalette.AlternateBase)))
		others.setBackground(0,QtGui.QBrush(self.window.ui.seznam.palette().color(QtGui.QPalette.AlternateBase)))
		seznam = os.listdir(self.main.homeDir+'/archive/'+self.jid)
		click=None
		for jid in seznam:
			if os.path.isdir(self.main.homeDir+'/archive/'+self.jid+'/'+jid):
				if self.main.client.roster['users'].has_key(unicode(unquote(jid).split('.history')[0])):
					item=QtGui.QTreeWidgetItem(contact)
					name=self.main.client.roster['users'][unicode(unquote(jid).split('.history')[0])].name
					if not name or len(name)==0:
						item.setText(0,unicode(unquote(jid).split('.history')[0]))
					else:
						item.setText(0,name)
				else:
					item=QtGui.QTreeWidgetItem(others)
					item.setText(0,unquote(jid).split('.history')[0])
				item.setData(0,32,QtCore.QVariant(unicode(unquote(jid).split('.history')[0])))
				#self.window.ui.seznam.addItem(item)
				if unicode(unquote(jid).split('.history')[0])==unicode(j):
					click=item
			else:
				continue
		if click:
			self.window.ui.seznam.setCurrentItem(click)
			self.itemClicked(click)
			
		self.window.show()
	
	def calChanged(self):	
		self.itemClicked(self.window.ui.seznam.currentItem(),setDate=False)
	
	
	def getDates(self,jid):
		dates=self.backend.getDates(jid)
		print "got dates"
		all=[]
		for date in list(dates):
			d=unicode(date).split('-')
			qdate=QtCore.QDate(int(d[0]),int(d[1]),int(d[2]))
			if not qdate in all:
				all.append(qdate)
		self.window.ui.calendar.setDates(all)
		item=self.window.ui.seznam.currentItem()
		jid = quote(unicode(item.data(0,32).toString()))
		
		self.window.ui.text.setText('')
		datum=self.window.ui.calendar.selectedDate()
		me=unicode(self.main.client.jid.user)

		user=self.main.ui.roster.getUserItems(unicode(item.data(0,32).toString()))
		if len(user)!=0:
			user=user[0].name
		else:
			user=None
		d=threads.deferToThread(self.getMessages,jid,str(datum.year())+"-"+str(datum.month())+"-"+str(datum.day()),me,user,unicode(self.skin["my_message"]),unicode(self.skin["message"]),self.skin['color1'])
		d.addCallback(self.gotMessages)

	def getLastMessages(self,jid,count,me,user,my_message,message,color,avatar,selfavatar,maxTime):
		action=["",jid,count,me,user,my_message,message,color,avatar]
		messages=self.backend.getLastMessages(action[1],action[2],maxTime)
		if not messages:
			return ""
		
		html=""
		me=action[3]
		user=action[4]

		for msg in messages:
			d=time.localtime(msg[0])
			#qdate=QtCore.QDate(d[0],d[1],d[2])
			#if datum==qdate:
			if msg[1]=='to':
				who=me
				html+=action[5].replace("[time]",str(d[3])+":"+str(d[4])+":"+str(d[5])).replace("[user]",who.replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")).replace("[message]",msg[3]).replace("<br/><br/>","<br/>").replace('[avatar]',selfavatar)
			else:
				if user:
					who=user
				else:
					who=msg[2]
				html+=action[6].replace("[time]",str(d[3])+":"+str(d[4])+":"+str(d[5])).replace("[user]",who.replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")).replace("[message]",msg[3]).replace("[foreground]",action[7][0]).replace("[background]",action[7][1]).replace("<br/><br/>","<br/>").replace('[avatar]',avatar)
		return html


	def getMessages(self,jid,datum,me,user,my_message,message,color):
		action=["",jid,datum,me,user,my_message,message,color]
		messages=self.backend.getMessages(action[1],action[2])
		if not messages:
			return ""
		
		html=""
		me=action[3]
		user=action[4]

		for msg in messages:
			d=time.localtime(msg[0])
			#qdate=QtCore.QDate(d[0],d[1],d[2])
			#if datum==qdate:
			if msg[1]=='to':
				who=me
				html+=action[5].replace("[time]",str(d[3])+":"+str(d[4])+":"+str(d[5])).replace("[user]",who.replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")).replace("[message]",msg[3]).replace("<br/><br/>","<br/>")
			else:
				if user:
					who=user
				else:
					who=msg[2]
				html+=action[6].replace("[time]",str(d[3])+":"+str(d[4])+":"+str(d[5])).replace("[user]",who.replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")).replace("[message]",msg[3]).replace("[foreground]",action[7][0]).replace("[background]",action[7][1]).replace("<br/><br/>","<br/>")
		return html

	def gotMessages(self,html):
		print "got messages"
		self.window.ui.text.setHtml(html)

	def itemClicked(self, item,column=0,setDate=True):
		jid = quote(unicode(item.data(0,32).toString()))
		if setDate:
			self.getDates(jid)
		else:
			self.window.ui.text.setText('')
			datum=self.window.ui.calendar.selectedDate()
			me=unicode(self.main.client.jid.user)
	
			user=self.main.ui.roster.getUserItems(unicode(item.data(0,32).toString()))
			if len(user)!=0:
				user=user[0].name
			else:
				user=None
			d=threads.deferToThread(self.getMessages,jid,str(datum.year())+"-"+str(datum.month())+"-"+str(datum.day()),me,user,unicode(self.skin["my_message"]),unicode(self.skin["message"]),self.skin['color1'])
			d.addCallback(self.gotMessages)
	def on_message(self,frm,typ,body,subject, xhtml,  chatstate,  delay, error=None):
		if body != None:
			#jid = quote(frm.split('/')[0])
			if typ=='groupchat':
				if delay!=None:
					return
				tab,index=self.main.chat.findTab(frm.split('/')[0])
				if tab:
					res=frm.split('/')
					if len(res)>1:
						if tab.name==res[1]:
							return
			self.backend.saveMessage(frm, body, typ, subject, xhtml, "from")

		
	def on_message_send (self, to, body, typ, subject,composing, xhtml,  muc):
		if not muc and body != None and len(body)!=0:
			self.backend.saveMessage(to, body, typ, subject, xhtml, "to")

