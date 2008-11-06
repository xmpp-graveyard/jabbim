# -*-coding: utf-8 -*-

import sys, os, locale
sys.path.append('.')
if sys.platform == 'win32':
	import win32gui
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
			self.config['player']={'type':'list-single','label':self.main.tr("Player"), 'items':{'MPD':'mpd', 'Amarok':'amarok', 'Amarok 2':'amarok2', 'Exaile':'exaile', 'Banshee':'banshee', 'Rhythmbox':'rhythmbox', 'Audacious':'audacious'}, 'value':'amarok'}

class Player:
	def __init__(self, plugin):
		self.plugin = plugin
		self.main = plugin.main
	def clear_PEP(self, reason=None):
		self.plugin.sendPEP({})
	def check(self):
		pass

class Winamp(Player):
	def __init__(self, plugin):
		Player.__init__(self, plugin)
	def check(self):
		out = {}
		try:
			hWinamp = win32gui.FindWindow('Winamp v1.x', None)
			text = win32gui.GetWindowText(hWinamp).decode(locale.getpreferredencoding())
		except Exception, ex:
			text = ''
		if len(text) > 0:
			parts = text.split(' - ')
			if len(parts) > 1:
				out['artist'] = parts[0].split(' ', 1)[1]
				out['title'] = parts[1]
			else:
				out = {}
			if text.find('[Stopped]')!= -1:
				out = {}
		self.plugin.sendPEP(out)

class Foobar2000(Player):
	def __init__(self, plugin):
		Player.__init__(self, plugin)
	def check(self):
		out = {}
		try:
			hfb2k = win32gui.FindWindow('{97E27FAA-C0B3-4b8e-A693-ED7881E99FC1}', None)
			text = win32gui.GetWindowText(hfb2k).decode(locale.getpreferredencoding())
		except Exception, ex:
			text = ''
		if len(text) > 0:
			parts = text.split(' - ')
			if len(parts) > 1:
				out['artist'] = parts[0]
				out['title'] = parts[1].split('[foobar2000 v', 1)[0].strip()
			else:
				out = {}
		self.plugin.sendPEP(out)

class MPDProtocol(ProcessProtocol):
	def __init__(self, plugin):
		self.plugin = plugin
		self.output = ''
	def outReceived(self, output):
		self.output += output
	def processEnded(self, reason):
		out = {}
		if isinstance(reason.value, ProcessDone) and self.output.find('\n[playing]') != -1:
			text = self.output.split('\n')[0]
			text = text.split(' - ', 1)
			if len(text)>1:
				out['artist'] = text[0]
				out['title'] = text[1]
			else:
				out['title'] = self.output.split('\n')[0].split('/')[-1]
			out['length'] = self.output.split('\n')[1].split('/')[-1].split('(')[0].strip()
		self.plugin.sendPEP(out)

class MPD(Player):
	def __init__(self, plugin):
		Player.__init__(self, plugin)
	def check(self):
		reactor.spawnProcess(
			MPDProtocol(self.plugin),
			'mpc', ['mpc', 'status'],
			env=os.environ)

class AmarokProtocol(ProcessProtocol):
	def __init__(self, plugin, out, field):
		self.plugin = plugin
		self.out = out
		self.field = field
	def outReceived(self, data):
		self.out[self.field] = unicode(data, "utf-8").strip()
	def processEnded(self, reason):
		if not isinstance(reason.value, ProcessDone):
			self.out = {}
		if len(self.out) == 2 or self.out == {}:
			self.plugin.sendPEP(self.out)

class Amarok(Player):
	def __init__(self, plugin):
		Player.__init__(self, plugin)
	def check(self):
		out = {}
		for field in ['artist', 'title']:
			reactor.spawnProcess(
				AmarokProtocol(self.plugin, out, field),
				'dcop', ['dcop', 'amarok', 'player', field],
				env=os.environ)

class Amarok2(Player):
	def __init__(self, plugin):
		Player.__init__(self, plugin)
		self.sig_receivers = []
	def got_metadata(self, song_info):
		out = {}
		try:
			out['artist'] = unicode(song_info['artist'])
			out['title'] = unicode(song_info['title'])
		except:
			out = {}
		self.plugin.sendPEP(out)
	def check(self, dummy=None):
		# I ignore the data supplied in DBus signals {Track,Status}Change,
		# because I couldn't make it work reliably. Instead I just always ask
		# Amarok again what the current song is. It's slower, but works.
		try:
			bus = self.main.session_dbus
			amarok_player = bus.get_object("org.mpris.amarok", "/Player")
			amarok_player.GetMetadata(reply_handler=self.got_metadata, error_handler=self.clear_PEP)
		except:
			self.clear_PEP()
	def start_listening(self):
		bus = self.main.session_dbus
		self.sig_receivers.append(bus.add_signal_receiver(self.check,
			'TrackChange',  "org.freedesktop.MediaPlayer", "org.mpris.amarok", "/Player"))
		self.sig_receivers.append(bus.add_signal_receiver(self.check,
			'StatusChange', "org.freedesktop.MediaPlayer", "org.mpris.amarok", "/Player"))
	def stop_listening(self):
		for receiver in self.sig_receivers:
			receiver.remove()
		self.sig_receivers = []

class Exaile(Player):
	def __init__(self, plugin):
		Player.__init__(self, plugin)
	def check(self):
		out = {}
		try:
			bus = self.main.session_dbus
			exa = bus.get_object("org.exaile.DBusInterface","/DBusInterfaceObject")
			out['artist'] = exa.get_artist()
			out['title'] = exa.get_title()
		except:
			out = {}
		self.plugin.sendPEP(out)

class Banshee(Player):
	def __init__(self, plugin):
		Player.__init__(self, plugin)
	def got_metadata(self, song_info):
		out = {}
		try:
			out['artist'] = song_info['artist']
			out['title'] = song_info['name']
		except:
			out = {}
		self.plugin.sendPEP(out)
	def check(self):
		try:
			bus = self.main.session_dbus
			banshee = bus.get_object("org.bansheeproject.Banshee", "/org/bansheeproject/Banshee/PlayerEngine")
			banshee.GetCurrentTrack(reply_handler=self.got_metadata, error_handler=self.clear_PEP)
		except:
			self.clear_PEP()

class Rhythmbox(Player):
	def __init__(self, plugin):
		Player.__init__(self, plugin)
	def check(self):
		out = {}
		try:
			bus = self.main.session_dbus
			rhythmboxplayer = bus.get_object("org.gnome.Rhythmbox", "/org/gnome/Rhythmbox/Player")
			rhythmboxshell = bus.get_object("org.gnome.Rhythmbox", "/org/gnome/Rhythmbox/Shell")
			currentTrackInfo = rhythmboxshell.getSongProperties(rhythmboxplayer.getPlayingUri())
			out['title'] = currentTrackInfo['title']
			out['artist'] = currentTrackInfo['artist']
		except:
			out = {}
		self.plugin.sendPEP(out)

#class AudaciousProtocol(ProcessProtocol):
#	def __init__(self, plugin, info, field):
#		self.plugin = plugin
#		self.info = info
#		self.field = field
#		self.info[field] = ''
#	def outReceived(self, data):
#		self.info[self.field] += data
#	def processEnded(self, reason):
#		if not isinstance(reason.value, ProcessDone):
#			self.info = {}
#		if len(self.info) == 3:
#			out = {}
#			if self.info['status'].strip() == 'playing':
#				out['artist'] = self.info['artist'].strip()
#				out['title'] = self.info['title'].strip()
#			self.plugin.sendPEP(out)
#		elif self.info == {}:
#			self.plugin.sendPEP({})
#
#class Audacious(Player):
#	def __init__(self, plugin):
#		Player.__init__(self, plugin)
#	def check(self):
#		info = {}
#		for query in [
#				['status', ['audtool', 'playback-status']],
#				['artist', ['audtool', 'current-song-tuple-data','artist']],
#				['title',  ['audtool', 'current-song-tuple-data','title' ]]]:
#			reactor.spawnProcess(
#				AudaciousProtocol(self.plugin, info, query[0]),
#				'audtool', query[1],
#				env=os.environ)

class Audacious(Player):
	def __init__(self, plugin):
		Player.__init__(self, plugin)
	def check(self):
		out = {}
		try:
			bus = self.main.session_dbus
			audacious_player = bus.get_object("org.mpris.audacious", "/Player")
			status = audacious_player.GetStatus()
			# Audacious's GetStatus() does not comply with MPRIS spec, it returns a single Int32
			if int(status) == 0:  # playing
				song_info = audacious_player.GetMetadata()
				out['title'] = song_info['title']
				out['artist'] = song_info['artist']
			else:
				out = {}
		except:
			out = {}
		self.plugin.sendPEP(out)

class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'tune'
		self.installTranslator()
		self.description = self.tr('Plugin for User Tune')
		self.author = "Jiri 'Sef' Gabrys + Josef 'PepeQ' Halicek + Krzysztof 'Grom' K. + Pinky + Michal 'Michich' Schmidt"
		self.name = self.tr('tune')
		self.version = '0.264'
		self.category = ['utils']
		self.configDialog=config(self)
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.player_installed = False
		if main:
			self.loadConfig()
			self.registerHandler('on_authd', self.on_authd)
			if self.main.client.xmlstream:
				self.on_authd()
		else:
			self.loadConfig(homedir)

	def on_authd(self):
		self.last = None
		self.loop = None
		player_map = {
			'winamp':    Winamp,
			'fb2k':      Foobar2000,
			'mpd':       MPD,
			'amarok':    Amarok,
			'amarok2':   Amarok2,
			'exaile':    Exaile,
			'banshee':   Banshee,
			'rhythmbox': Rhythmbox,
			'audacious': Audacious
		}
		# create the chosen Player instance
		self.player = player_map[self.config['player']](self)
		try:
			# if it can listen for events from the music player,
			# it will implement start_listening()
			self.player.start_listening()
			self.player.check()
		except AttributeError:
			# it is polling-based
			self.loop = LoopingCall(self.player.check)
			self.loop.start(30)
		self.player_installed = True

	def on_remove(self):
		if self.player_installed:
			if self.loop:
				self.loop.stop()
			else:
				self.player.stop_listening()
		self.sendPEP({})

	def on_configChanged(self):
		self.on_remove()
		self.on_authd()

	def sendPEP(self, out):
		if self.main.client.xmlstream == None:
			print "tune: Can't sendPEP yet, no xmlstream!"
			return
		if out != self.last:
			self.main.client.sendPEP('http://jabber.org/protocol/tune', self.main.client.getTunePayload(out))
			self.last = out
