import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from urllib import quote, unquote
from twisted.python import log
from configobj import ConfigObj

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
		self.archive=archive

	def saveMessage(self, to, body, typ, subject, xhtml, direction):
		jid = quote(to.split('/')[0])
		fp = open(self.archive.main.homeDir+'/archive/'+self.archive.jid+'/'+jid+'.history', 'a')
		if xhtml != None:
			telo = xhtml.replace('|', '&#124;').replace("\n","<br/>")
		else:
			telo = body.replace('|', '&#124;').replace("\n","<br/>")
		msg = '|'.join([unicode(time.time()), direction, jid, typ, quote(unicode(subject)), telo])
		msg = msg.encode('utf8')
		fp.write(msg+'\n')
		fp.close()

	def getMessages(self,jid):
		try:
			fp = open(self.archive.main.homeDir+'/archive/'+self.archive.jid+'/'+jid+'.history')
		except:
			log.err('no history file')
			return None
		ret=[] # timestamp,direction,message
		#zpravy = fp.readlines()
		#print zpravy
		#for msg in zpravy:
			#print msg
		#msg=fp.readline()
		#while len(msg)==0:
		for msg in fp.xreadlines():
			parsed=msg.split('|')
			ret.append([float(parsed[0]),str(parsed[1]),unicode(parsed[5],"utf8")])
		fp.close()
		return ret
		
		
			

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
# 		self.config['notify'] = {'description':'', 'default':'True', 'value': '','type':'boolean'}


		if main:
			self.backend=FileBackend(self)
			self.jid = quote(self.main.client.jid.userhost())
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
			QtCore.QObject.connect(self.window.ui.seznam, QtCore.SIGNAL("itemClicked ( QListWidgetItem* ) "),self.itemClicked)
			QtCore.QObject.connect(self.window.ui.calendar, QtCore.SIGNAL("selectionChanged()"),self.calChanged)
			self.group=QtGui.QButtonGroup(self.window)
			QtCore.QObject.connect(self.group,QtCore.SIGNAL("buttonClicked ( QAbstractButton * )"),self.buttonClicked)
		else:
			self.loadConfig(homedir)

	def buildRosterMenu(self):
		menu=self.rosterMenu()
		menu.addAction("Archive browser",self.showSlot)
	
	def buttonClicked(self,button):
		jid=button.jid
		self.showSlot(jid)
		

	
	def buildChatWidget(self,jid,layout):
		print "buildChatWidget"
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
		seznam = os.listdir(self.main.homeDir+'/archive/'+self.jid)
		click=None
		for jid in seznam:
			if os.path.isdir(self.main.homeDir+'/archive/'+self.jid+'/'+jid):
				continue
			else:
				item=QtGui.QListWidgetItem()
				item.setText(unquote(jid).split('.history')[0])
				self.window.ui.seznam.addItem(item)
				if unicode(unquote(jid).split('.history')[0])==unicode(j):
					click=item
		if click:
			self.window.ui.seznam.setCurrentItem(click)
			self.itemClicked(click)
			
		self.window.show()
	
	def calChanged(self):	
		self.itemClicked(self.window.ui.seznam.currentItem(),setDate=False)
	
	def itemClicked(self, item,setDate=True):

		self.window.ui.text.setText('')
		jid = quote(unicode(item.text()))
		messages=self.backend.getMessages(jid)

		datum=self.window.ui.calendar.selectedDate()
		dates=[]
		html=""
		me=unicode(self.main.client.jid.user)

		user=self.main.ui.roster.getUserItems(unicode(item.text()))
		if len(user)!=0:
			user=user[0].name
		else:
			user=unicode(item.text())

		for msg in messages:
			d=time.localtime(msg[0])
			qdate=QtCore.QDate(d[0],d[1],d[2])
			if datum==qdate:
				#message=self.main.skin["my_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",text).replace("[avatar]","<img src=\""+file+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
				if msg[1]=='to':
					who=me
				else:
					who=user
				html+=unicode('[%s] %s: %s<br/><br/>' %(str(d[3])+":"+str(d[4])+":"+str(d[5]),who, msg[2]))
			if not qdate in dates:
				dates.append(qdate)
		self.window.ui.text.setHtml(html)
		if setDate:
			self.window.ui.calendar.setDates(dates)
	
	def on_message(self,frm,typ,body,subject, xhtml,  chatstate,  delay, error=None):
		if body != None and chatstate==None:
			jid = quote(frm.split('/')[0])
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
