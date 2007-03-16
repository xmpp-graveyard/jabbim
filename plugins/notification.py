try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
import plugins
class plugin:
	def __init__(self,main):
		menu=plugins.addChatWindowMenu(main,"Notification",self.menuHandle)
		plugins.addChatWindowMenuAction(menu,"Show all","show_all")

	def menuHandle(self,action):
		ID=plugins.getActionID(action)
		print ID

	def onNewChatMessage(self,main,user,message):
		if len(message)>40:
			traytext=message[:40]+" ..."
		else:
			traytext=message
		main.tray.showMessage(main.tr("New message from ")+unicode(user), traytext, QtGui.QSystemTrayIcon.Information, 5000)
	
	def onRosterPresence(self,main,user,status,statusMessage,statusNum):
		if main.config["tray_message_view_connect"]=="all" or (main.config["tray_message_view_connect"]=="online" and status=="None") or (main.config["tray_message_view_connect"]=="logged_in" and statusNum==9):
			main.tray.showMessage(main.tr("User status"), main.tr("User ")+user+main.tr(" is now ")+main.status[status]+"\n"+statusMessage, QtGui.QSystemTrayIcon.Information, 5000)
	
	def onSubscribed(self,main,jid):
		pass
	
	def onSubscribe(self,main,jid):
		pass
	
	def onNewGroupchatMessage(self,main,jid,user,timestamp):
		pass
	
	def onNewHeadlineMessage(self,main,jid,text,subject,urls,descs,timestamp):
		pass
	
	def onDisconnected(self,main):
		pass
	
	def onConnected(self,main):
		pass