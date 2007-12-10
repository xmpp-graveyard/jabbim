# -*- coding: utf8 -*-
import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from urllib import quote, unquote
from twisted.python import log
from include import utils
import time
import ctypes
from ctypes.util import find_library
class XScreenSaverInfo( ctypes.Structure):
	""" typedef struct { ... } XScreenSaverInfo; """
	_fields_ = [('window',      ctypes.c_ulong), # screen saver window
				('state',       ctypes.c_int),   # off,on,disabled
				('kind',        ctypes.c_int),   # blanked,internal,external
				('since',       ctypes.c_ulong), # milliseconds
				('idle',        ctypes.c_ulong), # milliseconds
				('event_mask',  ctypes.c_ulong)] # events

mutex=QtCore.QMutex()


class autoAwayThread(QtCore.QThread):
	def __init__(self,main):
		QtCore.QThread.__init__(self,None)
		self.main=main

	def run(self):
		locker = QtCore.QMutexLocker(mutex)
		config=self.main.config
		threadRun=True
		xlib = ctypes.cdll.LoadLibrary(find_library("X11"))
		dpy = xlib.XOpenDisplay( os.environ['DISPLAY'])
		root = xlib.XDefaultRootWindow( dpy)
		xss = ctypes.cdll.LoadLibrary(find_library("Xss"))
		status="online"
		while threadRun:
			awayTime=int(self.main.config['awayTime'])*60000
			xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
			xss_info = xss.XScreenSaverAllocInfo()
			xss.XScreenSaverQueryInfo( dpy, root, xss_info)
			if int(xss_info.contents.idle)>awayTime and int(xss_info.contents.idle)<awayTime+1000:
				self.emit(QtCore.SIGNAL("setAway()"))
				status="away"
			elif int(xss_info.contents.idle)<1000 and status!="online":
				self.emit(QtCore.SIGNAL("setOnline()"))
				status="online"

			#print "Idle time in milliseconds: %d" % ( xss_info.contents.idle)
			for i in range(2):
				time.sleep(0.5)
				threadRun=self.main.threadRun
				if not threadRun:
					break

class LASTINPUTINFO(ctypes.Structure):
	_fields_ = [("cbSize", ctypes.c_uint),
				("dwTime", ctypes.c_uint)]


class autoAwayThreadWin(QtCore.QThread):
	def __init__(self,main):
		QtCore.QThread.__init__(self,None)
		self.main=main

	def run(self):
		locker = QtCore.QMutexLocker(mutex)
		config=self.main.config
		threadRun=True
		#xlib = ctypes.cdll.LoadLibrary(find_library("X11"))
		#dpy = xlib.XOpenDisplay( os.environ['DISPLAY'])
		#root = xlib.XDefaultRootWindow( dpy)
		#xss = ctypes.cdll.LoadLibrary(find_library("Xss"))
		
		GetTickCount = ctypes.windll.kernel32.GetTickCount
		GetLastInputInfo = ctypes.windll.user32.GetLastInputInfo
		lastInputInfo = LASTINPUTINFO()
		lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)
#for i in range(10):
    #GetLastInputInfo(byref(lastInputInfo))
    #idleDelta = float(GetTickCount() - lastInputInfo.dwTime) / 1000
    #print "Last input event was %.2f seconds ago." % idleDelta
    #time.sleep(1)
		
		status="online"
		while threadRun:
			awayTime=int(self.main.config['awayTime'])*60000
			#xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
			#xss_info = xss.XScreenSaverAllocInfo()
			#xss.XScreenSaverQueryInfo( dpy, root, xss_info)
			GetLastInputInfo(ctypes.byref(lastInputInfo))
			idleDelta = int(GetTickCount() - lastInputInfo.dwTime)
			if int(idleDelta)>awayTime and idleDelta<awayTime+1000:
				self.emit(QtCore.SIGNAL("setAway()"))
				status="away"
			elif int(idleDelta)<1000 and status!="online":
				self.emit(QtCore.SIGNAL("setOnline()"))
				status="online"

			#print "Idle time in milliseconds: %d" % ( xss_info.contents.idle)
			for i in range(2):
				time.sleep(0.5)
				threadRun=self.main.threadRun
				if not threadRun:
					break

class config:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['awayTime']={'type':'number-spin','label':self.main.tr("Away time (minutes):"),'value':'5'}
		self.config['awayMessage']={'type':'text-multi','label':self.main.tr("Away text"),'value':self.main.tr("I'm not here for more than [time] minutes.")}
		self.config['__sort__']=['awayTime','awayMessage']

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'autoaway'
		self.description = 'Auto away'
		self.author = u"Jan 'HanzZ' Kaluža"
		self.name = 'Autoaway Plugin'
		self.version = '0.022'
		self.category = ['misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.kontakty = {} # jid:contact
		self.developMode=True
		#self.config['away_time'] = {'description':'Minutes to autoaway', 'default':'10', 'value': '','type':'text'}
		#self.config['away_text'] = {'description':'Text to show while auto away', 'default':'User is away for %i minutes.', 'value': '','type':'text'}
		#self.config['preserve_show'] = {'description':"Change only status message", 'default':'True', 'value': '','type':'boolean'}
		self.threadRun=True
		self.awayTime=1
		self.installTranslator()
		self.configDialog=config(self)
		if main:
			self.loadConfig()

##			self.window = self.loadWindow("%s/plugins/%s/news.ui.py"%(self.homeDir, self.fname))
##			self.window.setWindowIcon(self.main.windowIcon())
			self.log = False
			#self.registerHandler('onInactivity', self.on_idle, priority=4)
			#self.registerHandler('onActivity', self.on_active, priority=4)
			if sys.platform == 'win32':
				self.thread=autoAwayThreadWin(self)
			else:
				self.thread=autoAwayThread(self)

			QtCore.QObject.connect(self.thread, QtCore.SIGNAL("setAway()"), self.setAway,QtCore.Qt.QueuedConnection)
			QtCore.QObject.connect(self.thread, QtCore.SIGNAL("setOnline()"), self.setOnline,QtCore.Qt.QueuedConnection)
			self.thread.start()
		else:
			self.loadConfig(homedir)
		
		self.message_set = False
		self.idletime = 0
		self.old_show = 'away'
		self.old_status = ''
	
	def setOnline(self):
		print "autoaway online"
		if self.message_set:
			self.message_set=False
			self.main.client.sendPresence(show = 'online', status = "autoaway")
			for muc in self.main.client.groupchats.itervalues():
				self.main.client.sendPresence(show = 'online', status = "", to = '%s/%s'%(muc.jid, muc.nick))

	def setAway(self):
		print "autoaway away"
		self.message_set=True
		contact = self.main.client.roster['users'][self.main.client.jid.userhost()]
		print "current show:",contact.resources[self.main.client.jid.resource].show
		if contact.resources[self.main.client.jid.resource].show=="online":
			self.main.client.sendPresence(show = 'away', status = "autoaway")
			for muc in self.main.client.groupchats.itervalues():
				self.main.client.sendPresence(show = 'away', status = self.config['awayMessage'].replace('[time]',self.config['awayTime']), to = '%s/%s'%(muc.jid, muc.nick))


	def on_remove(self):
		self.threadRun=False
		self.thread.wait()

	#def on_idle(self, cas):
		#self.idletime += cas
		#if self.idletime > (int(self.config['away_time']['value'])*60) and not self.message_set:
			#contact = self.main.client.roster['users'][self.main.client.jid.userhost()]
			#self.old_show = contact.resources[self.main.client.jid.resource].show
			#self.old_status = contact.resources[self.main.client.jid.resource].status
			#try:
				#text = self.config['away_text']['value']%(self.idletime/60)
			#except:
				#text = self.config['away_text']['value']
			#self.main.client.sendPresence(show = 'away', status = text)
			#for muc in self.main.client.groupchats.itervalues():
					#self.main.client.sendPresence(show = 'away', status = text, to = '%s/%s'%(muc.jid, muc.nick))
			#self.message_set = True
			#log.msg('idle status poslan')
	
	#def on_active(self):
		#if self.message_set:
			#self.idletime = 0
			#self.message_set = False
			#self.main.client.sendPresence(show = self.old_show, status = self.old_status)
			#for muc in self.main.client.groupchats.itervalues():
				#self.main.client.sendPresence(show = self.old_show, status = self.old_status, to = '%s/%s'%(muc.jid, muc.nick))
