# -*-coding: utf-8 -*-

import sys, os, time, locale
sys.path.append('.')
if sys.platform != 'win32':
	import commands
import traceback
from PyQt4 import QtCore, QtGui
from twisted.python import log
from include import plugins
from twisted.internet.task import LoopingCall
from twisted.internet.protocol import ProcessProtocol
from twisted.internet.error import ProcessDone
from twisted.internet import reactor

class config:
	def __init__(self,main):
		self.main=main
		self.config={}
		if sys.platform == 'win32':
			self.config['player']={'type':'list-single','label':self.main.tr("Player"), 'items':{'Winamp':'winamp', 'Foobar 2000':'fb2k' }, 'value':'winamp'}
			
		else:
			self.config['player']={'type':'list-single','label':self.main.tr("Player"), 'items':{'MPD':'mpd', 'Amarok':'amarok','Exaile':'exaile','Banshee':'banshee','Rhythmbox':'rhythmbox', 'Audacious':'audacious' }, 'value':'amarok'}

class AmarokProcessProtocol(ProcessProtocol):
	def __init__(self, plugin, out, field):
		self.plugin = plugin
		self.out = out
		self.field = field

	# Will get called when the subprocess has data on stdout
	def outReceived(self, data):
		self.out[self.field] = unicode(data, "utf-8").strip()

	# Will get called when the subprocess has data on stderr
	def errReceived(self, data):
		pass

	# Will get called when the subprocess starts
	def connectionMade(self):
		pass

	# Will get called when the subprocess ends
	def processEnded(self, reason):
		# ProcessDone indicates successful exit
		if not isinstance(reason.value, ProcessDone):
			self.out = {}
		if (len(self.out) == 2 or self.out == {}):
			self.plugin.sendPEP(self.out)

class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'tune'
		self.installTranslator()
		self.description = self.tr('Plugin for User Tune')
		self.author = "Jiri 'Sef' Gabrys + Josef 'PepeQ' Halicek + Krzysztof 'Grom' K. + Pinky"
		self.name = self.tr('tune')
		self.version = '0.263'
		self.category = ['utils']
		self.configDialog=config(self)
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.loop = LoopingCall(self.check)
		self.last = None
		if main:
			self.loadConfig()
			self.loop.start(30)
		else:
			self.loadConfig(homedir)

	def on_remove(self):
		self.loop.stop()
		self.sendPEP({})

	def sendPEP(self, out):
		if out != self.last and self.main.client.xmlstream != None:
			self.main.client.sendPEP('http://jabber.org/protocol/tune', self.main.client.getTunePayload(out))
			self.last = out

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
				
		
		elif self.config['player'] == 'banshee':
			try:
				import dbus
				bus = dbus.SessionBus()
				banshee = bus.get_object("org.bansheeproject.Banshee", "/org/bansheeproject/Banshee/PlayerEngine")
				currentTrack = banshee.GetCurrentTrack()
				out['artist'] = currentTrack['artist']
				out['title'] = currentTrack['name']
			except:
				text = ''
				out = {}

		elif self.config['player'] == 'winamp':
			print "getting current song from winamp"
			try:
				import win32gui
				hWinamp = win32gui.FindWindow('Winamp v1.x', None)
				text = win32gui.GetWindowText(hWinamp).decode(locale.getpreferredencoding())
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


		elif self.config['player'] == 'rhythmbox':
			try:
				import dbus
				bus = dbus.SessionBus()
				rhythmboxplayer = bus.get_object("org.gnome.Rhythmbox", "/org/gnome/Rhythmbox/Player")
				rhythmboxshell = bus.get_object("org.gnome.Rhythmbox", "/org/gnome/Rhythmbox/Shell")
				currentTrackInfo = rhythmboxshell.getSongProperties(rhythmboxplayer.getPlayingUri())
				out['title'] = currentTrackInfo['title']
				out['artist'] = currentTrackInfo['artist']
			except:
				text = ''
				out = {}

		elif self.config['player'] == 'amarok':
			try:
				for field in ['artist', 'title']:
					reactor.spawnProcess(
						AmarokProcessProtocol(self, out, field),
						'dcop', ['dcop', 'amarok', 'player', field],
						env=os.environ)
				return  # PEP will be sent when the spawned processes exit
			except:
				out = {}

		elif self.config['player'] == 'fb2k':
			print "getting current song from foobar"
			try:
				import win32gui
				hfb2k = win32gui.FindWindow('{97E27FAA-C0B3-4b8e-A693-ED7881E99FC1}', None)
				text = win32gui.GetWindowText(hfb2k).decode(locale.getpreferredencoding())
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
					out['artist'] = parts[0]
					out['title'] = parts[1].split('[foobar2000 v', 1)[0].strip()
				else:
					out={}

		elif self.config['player'] == 'audacious':
			try:
				output = commands.getoutput('audtool playback-status')
				if output.find('playing') != -1:
					text = text = commands.getoutput('audtool current-song')
					text = text.split(' - ', 1)
					out['artist'] = text[0]
					out['title'] = text[1]
			except:
				out = {}

		self.sendPEP(out)


# EOF
