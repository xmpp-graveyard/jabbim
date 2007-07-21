try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

class pluginClass:
	def __init__(self,main):
		self.main=main
		self.main.client.dispatcher.registerHandler('on_message', self.on_message)

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
