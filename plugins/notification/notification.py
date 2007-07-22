try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
import sys
sys.path.append('.')
from include import plugins
class Plugin(plugins.PluginBase):
	def __init__(self,main):
		plugins.PluginBase.__init__(self, main)
		self.fname = 'notification'
		self.description = 'System tray notification'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'Notification Plugin'
		self.version = '0.1'
		self.category = ['notification']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.config['notify'] = {'description':'', 'default':'True', 'value': '','type':'boolean'}
		if main:
			self.registerHandler('on_message', self.on_message)
			self.loadConfig()

	def on_message(self,frm,typ,body,subject, xhtml,  chatstate,  delay):
		if self.main.client.roster['users'].has_key(frm):
			user=self.main.client.roster['users'][frm].name
		else:
			user=frm
		if len(body)>40:
				traytext=body[:40]+" ..."
		else:
				traytext=body
		self.main.tray.showMessage(self.main.tr("New message from ")+unicode(user), traytext, QtGui.QSystemTrayIcon.Information, 5000)
