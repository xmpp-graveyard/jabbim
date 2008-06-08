# -*-coding: utf-8 -*-

import sys, os, time
sys.path.append('.')
if sys.platform != 'win32':
	import commands
import traceback
from PyQt4 import QtCore, QtGui
from twisted.python import log
from include import plugins
from twisted.internet.task import LoopingCall

class config:
	def __init__(self,main):
		self.main=main
		self.config={}
		if sys.platform == 'win32':
			self.config['player']={'type':'list-single','label':self.main.tr("Player"), 'items':{'Winamp':'winamp' }, 'value':'winamp'}
			
		else:
			self.config['player']={'type':'list-single','label':self.main.tr("Player"), 'items':{'MPD':'mpd', 'Winamp':'winamp', 'Amarok':'amarok','Exaile':'exaile' }, 'value':'amarok'}

class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'tune'
		self.description = 'Plugin for User Tune'
		self.author = "Jiri 'Sef' Gabrys + Josef 'PepeQ' Halicek"
		self.name = 'tune'
		self.version = '0.23'
		self.category = ['utils']
		self.configDialog=config(self)
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.loop = LoopingCall(self.check)
		self.last = {}
		if main:
			self.loadConfig()
			self.loop.start(30)
		else:
			self.loadConfig(homedir)

	def on_remove(self):
		self.loop.stop()
		self.main.client.sendPEP('http://jabber.org/protocol/tune', self.main.client.getTunePayload({}))
	def check(self):
		out = {}
		if self.config['player'] == 'mpd':
			try:
				output = commands.getoutput('mpc status 2>/dev/null')
			except:
				pass
			if output.find('\n[playing]') != -1:
					text = output.split('\n')[0]
					text = text.split(' - ', 1)
					if len(text)>1:
						out['artist'] = text[0]
						out['title'] = text[1]
					else:
						out['title'] = output.split('\n')[0].split('/')[-1]
					out['lenght'] = output.split('\n')[1].split('/')[-1].split('(')[0].strip()

		elif self.config['player'] == 'exaile':
			
			try:
				import dbus
				bus = dbus.SessionBus()
				obj = bus.get_object("org.exaile.DBusInterface","/DBusInterfaceObject")
				exa = dbus.Interface(obj,"org.exaile.DBusInterface")
				out['artist'] = exa.get_artist()
				if exa.get_title() !='':
					out['title'] = exa.get_title() #nebudu zavadet novou promenou, zbytecne.
				else:	
					out = {}
			except:
				text = ''
				out = {}
				
		
		elif self.config['player'] == 'winamp':
			print "getting current song from winamp"
			try:
				import win32gui
				hWinamp = win32gui.FindWindow('Winamp v1.x', None)
				text = win32gui.GetWindowText(hWinamp)
			except Exception, ex:
				print 'Tune error: ' +unicode(ex)
				message = unicode(traceback.format_exc())
				print message
				text = ''
				out = {}
			print "got:",[text]
			if len(text) > 0:
				parts = text.split(' - ')
				if len(parts)>1:
					out['artist'] = parts[0].split(' ', 1)[1]
					out['title'] = parts[1]
				else:
					out={}
				if text.find('[Stopped]')!= -1:
					out = {}

		elif self.config['player'] == 'amarok':
			try:
				for field in ['artist', 'title']:
					(err, cmd_output) = commands.getstatusoutput("dcop amarok player %s" % field)
					if err != 0:
						raise Exception
					out[field] = unicode(cmd_output, "utf-8")
				if len(out['title'].strip()) == 0 and len(out['artist'].strip()) == 0:
					out = {}
			except:
				out = {}

    		

		if out != self.last and self.main.client.xmlstream != None:
			self.main.client.sendPEP('http://jabber.org/protocol/tune', self.main.client.getTunePayload(out))
			self.last = out


# EOF
