try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
import plugins
class plugin:
	def __init__(self,main,jab):
		self.main=main
		self.jab=jab
		menu=plugins.addChatWindowMenu(self.main,"Notification",self.menuHandle)
		plugins.addChatWindowMenuAction(menu,"Show all","show_all")

	def menuHandle(self,action):
		ID=plugins.getActionID(action)
		print ID

	def onNewChatMessage(self,user,message):
		if len(message)>40:
			traytext=message[:40]+" ..."
		else:
			traytext=message
		self.main.tray.showMessage(self.main.tr("New message from ")+unicode(user), traytext, QtGui.QSystemTrayIcon.Information, 5000)
	
	def onRosterPresence(self,user,status,statusMessage,statusNum):
		if self.main.config["tray_message_view_connect"]=="all" or (self.main.config["tray_message_view_connect"]=="online" and status=="None") or (self.main.config["tray_message_view_connect"]=="logged_in" and statusNum==9):
			self.main.tray.showMessage(self.main.tr("User status"), self.main.tr("User ")+user+self.main.tr(" is now ")+self.main.status[status]+"\n"+statusMessage, QtGui.QSystemTrayIcon.Information, 5000)
	
	def onSubscribed(self,jid):
		pass
	
	def onSubscribe(self,jid):
		pass
	
	def onNewGroupchatMessage(self,jid,user,timestamp):
		pass
	
	def onNewHeadlineMessage(self,jid,text,subject,urls,descs,timestamp):
		pass
	
	def onDisconnected(self):
		pass
	
	def onConnected(self):
		pass