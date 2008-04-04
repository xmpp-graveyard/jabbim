# -*-coding: utf-8 -*-

import sys, os, time
sys.path.append('.')
import commands

from PyQt4 import QtCore, QtGui
from twisted.python import log
from include import plugins
from twisted.internet.task import LoopingCall

class config:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['player']={'type':'list-single','label':self.main.tr("Player"), 'items':{'MPD':'mpd', 'Winamp':'winamp', 'Amarok':'amarok' }, 'value':'mpd'}

class Plugin(plugins.PluginBase):
    def __init__(self, main, homedir, plugindir):
        plugins.PluginBase.__init__(self, main, homedir, plugindir)
        self.fname = 'tune'
        self.description = 'Plugin for User Tune'
        self.author = "Jiri 'Sef' Gabrys"
        self.name = 'tune'
        self.version = '0.1'
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

		elif self.config['player'] == 'winamp':
			
			try:
				import win32gui
				hWinamp = win32gui.FindWindow('Winamp v1.x', None)
				text = win32gui.GetWindowText(hWinamp)
			except:
				text = ''
				out = {}
				
			if len(text) > 0:
				parts = text.split(' - ')
				out['artist'] = parts[0].split(' ', 1)[1]
				out['title'] = parts[1]
				if text.find('[Stopped]')!= -1:
					out = {}
		elif self.config['player'] == 'amarok':
			try:
				out['artist'] = unicode(commands.getoutput("dcop amarok player artist"), "utf-8")
				out['title'] = unicode(commands.getoutput("dcop amarok player title"), "utf-8")
			except:
				out = {}
			
			if len(out['title'].strip()) == 0 and len(out['artist'].strip()) == 0:
				out = {}
			elif out['title'].strip() == "call failed" or out['artist'] == "call failed":
				out = {}

    		

		if out != self.last:
			self.main.client.sendPEP('http://jabber.org/protocol/tune', self.main.client.getTunePayload(out))
			self.last = out
    			


# EOF
