import sys,os,time
sys.path.append('.')
from include import plugins

from urllib import quote, unquote


class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'archive'
		self.description = 'Message Archiving'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'Archive Plugin'
		self.version = '0.1'
		self.category = ['archive']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.config['notify'] = {'description':'', 'default':'True', 'value': '','type':'boolean'}

		if main:
			if not os.path.isdir(self.main.homeDir+'/archive'):
				os.mkdir(self.main.homeDir+'/archive')
			self.registerHandler('on_message', self.on_message)
			self.registerHandler('on_message_send', self.on_message_send)
			self.loadConfig()
		

	def on_message(self,frm,typ,body,subject, xhtml,  chatstate,  delay):
		jid = quote(frm.split('/')[0])
		fp = open(self.main.homeDir+'/archive/'+jid+'.history', 'a')
		if xhtml != None:
			telo = quote(xhtml)
		else:
			telo = quote(body)
		msg = '|'.join([unicode(time.time()), 'from', jid, typ, quote(unicode(subject)), telo])
		fp.write(msg+'\n')
		fp.close()
	
	def on_message_send (self, to, body, typ, subject,composing, xhtml,  muc):
		if not muc:
			jid = quote(to.split('/')[0])
			fp = open(self.main.homeDir+'/archive/'+jid+'.history', 'a')
			if xhtml != None:
				telo = quote(xhtml)
			else:
				telo = quote(body)
			msg = '|'.join([unicode(time.time()), 'to', jid, typ, quote(unicode(subject)), telo])
			fp.write(msg+'\n')
			fp.close()
