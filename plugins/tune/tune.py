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
		self.config['player']={'type':'list-single','label':self.main.tr("Player"), 'items':{'MPD':'mpd', }, 'value':'mpd'}

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
    	if self.config['player'] == 'mpd':
    		output = commands.getoutput('mpc status 2>/dev/null')
    		out = {}
    		if output.find('\n[playing]') != -1:
    			text = output.split('\n')[0]
    			text = text.split(' - ')
    			out['artist'] = text[0]
    			out['title'] = text[1]
    			out['lenght'] = output.split('\n')[1].split('/')[-1].split('(')[0].strip()
    		
    		if out != self.last:
    			self.main.client.sendPEP('http://jabber.org/protocol/tune', self.main.client.getTunePayload(out))
    			self.last = out
    			

    def buildRosterMenu(self):
        pass

    def commandCalled(self, cmd, args, chat, type):
        if cmd != 'mpd':
            return

        if len(args) != 0:
            self.logMsg('Args: ', args)
            self.parseArgs(args)
            return

        # FIXME: not clear (?)
        self.chat = chat
        self.type = type

        #output = unicode(commands.getoutput('mpc status 2>/dev/null'), self.ENCODING)
        output = commands.getoutput('mpc status 2>/dev/null')
        
        if output.find('\n[paused]') != -1:
        # any more elegant solution for this?
            self.logMsg('PAUSED')
            self.sendAnswer(self.PAUSED)
            return

        output = output.split('\n')
        if len(output) <= 1:
            self.logMsg('STOPPED')
            self.sendAnswer(self.STOPPED)
            return
        else:
            msg = self.PLAYING + output[0]

        self.logMsg('Sending: ', msg)
        self.sendAnswer(msg)

    def parseArgs(self, args):
        pos_args = [u'next', u'prev', u'stop', u'pause', u'volume']
        req_another = [pos_args[2]]

        # FIXME: error msgs (?) + comments
        if args[0] not in pos_args:
            return
        if args[0] in req_another and len(args) < 2:
            return

        try:
            status = commands.getstatusoutput(u'mpc %s %s 2>/dev/null' % (args[0], args[1]))[0]
        except IndexError:
            status = commands.getstatusoutput(u'mpc %s 2>/dev/null' % args[0])[0]

        if status != 0:
            # omg, something failed...
            pass





# EOF
