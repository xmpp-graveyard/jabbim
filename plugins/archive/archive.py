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
		self.repaint()

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
		

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'archive'
		self.description = 'Message Archiving'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'Archive Plugin'
		self.version = '0.141'
		self.category = ['archive']
		self.url = 'http://dev.jabbim.cz/jabbim'
# 		self.config['notify'] = {'description':'', 'default':'True', 'value': '','type':'boolean'}


		if main:
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
		else:
			self.loadConfig(homedir)
	def buildRosterMenu(self):
		menu=self.rosterMenu()
		menu.addAction("Archive browser",self.showSlot)
	
	def showSlot(self):
		self.window.ui.seznam.clear()
		self.window.ui.calendar.setDates([])
		self.window.ui.text.setText('')
		seznam = os.listdir(self.main.homeDir+'/archive/'+self.jid)
		for jid in seznam:
			if os.path.isdir(self.main.homeDir+'/archive/'+self.jid+'/'+jid):
				continue
			else:
				self.window.ui.seznam.addItem(unquote(jid).split('.history')[0])

		self.window.show()
	
	def calChanged(self):	
		log.msg("date clicked")
		self.itemClicked(self.window.ui.seznam.currentItem())
		#self.window.ui.text.setText('')
		#jid = quote(unicode(self.window.ui.seznam.currentItem ().text()))
		#try:
			#fp = open(self.main.homeDir+'/archive/'+self.jid+'/'+jid+'.history')
			#zpravy = fp.readlines()
			#fp.close()
		#except:
			#log.err('no history file')
			#return
		#datum = self.window.ui.calendar.selectedDate().toString('dd-MM-yyyy')
		#if len(zpravy)>0:
			#for zprava in zpravy:
	## 			log.msg(zprava)
				#casti = zprava.split('|')
	## 			log.msg(unicode(casti))
				#if datum == time.strftime('%d-%m-%Y', time.localtime(float(casti[0]))):
					#self.window.ui.text.append(unicode('[%s] %s' %(time.strftime('%X', time.localtime(float(casti[0]))), casti[5]), 'utf8'))

	
	def itemClicked(self, item):
		log.msg("item clicked")
		self.window.ui.text.setText('')
		jid = quote(unicode(item.text()))
		fp = ConfigObj(self.main.homeDir+'/archive/'+self.jid+'/'+jid+'.history')
		#try:
			#fp = open(self.main.homeDir+'/archive/'+self.jid+'/'+jid+'.history')
			#zpravy = fp.readlines()
			#fp.close()
		#except:
		if len(fp)==0:
			log.err('no history file')
			return
		#datum = self.window.ui.calendar.selectedDate().toString('dd-MM-yyyy')
		datum=self.window.ui.calendar.selectedDate()
		dates=[]
		for date,value in fp.iteritems():
			d=time.localtime(float(date))
			qdate=QtCore.QDate(d[0],d[1],d[2])
			if datum==qdate:
				msg=""
				for m in value[4:]:
					msg+=m+"\n"
				self.window.ui.text.append(unicode('[%s] %s' %(str(d[3])+":"+str(d[4])+":"+str(d[5]), msg),"utf8"))
			if not qdate in dates:
				dates.append(qdate)
		print dates
		self.window.ui.calendar.setDates(dates)
		#if len(zpravy)>0:
			#for zprava in zpravy:
				#casti = zprava.split('|')
				#log.msg(unicode(casti))
				#if len(casti)!=0:
					#if datum == time.strftime('%d-%m-%Y', time.localtime(float(casti[0]))):
						#self.window.ui.text.append(unicode('[%s] %s' %(time.strftime('%X', time.localtime(float(casti[0]))), casti[5]), 'utf8'))
	
	def on_message(self,frm,typ,body,subject, xhtml,  chatstate,  delay):
		if body != None:
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
				
			fp=ConfigObj(self.main.homeDir+'/archive/'+self.jid+'/'+jid+'.history',encoding='UTF8')
			if xhtml != None:
				telo = xhtml
			else:
				telo = body
			telo=telo.split("\n")
			fp[unicode(time.time())]=['from',jid, typ, unicode(subject)]+telo
			fp.write()
	
	def on_message_send (self, to, body, typ, subject,composing, xhtml,  muc):
		if not muc and body != None:
			jid = quote(to.split('/')[0])
			fp=ConfigObj(self.main.homeDir+'/archive/'+self.jid+'/'+jid+'.history',encoding='UTF8')
			if xhtml != None:
				telo = xhtml
			else:
				telo = body
			telo=telo.split("\n")
			fp[unicode(time.time())]=['to',jid, typ, unicode(subject)]+telo
			#msg = '|'.join([unicode(time.time()), 'to', jid, typ, quote(unicode(subject)), telo])
			#msg = msg.encode('utf8')
			fp.write()
			#fp.close()
