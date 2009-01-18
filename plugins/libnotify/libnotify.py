# -*- coding: utf8 -*- 
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
try:
	import pygtk
	pygtk.require('2.0')
	import gtk
except:
	print "PyGTK or GTK+ is not installed or your version is too old."
import sys
import os
try:
	import pynotify
except:
	print "You need libnotify to make this plugin work."
sys.path.append('.')
from include import plugins, utils
import time
from twisted.words.protocols.jabber import jid as jidT
pynotify.init("Jabbim Notification")

class config:
	def __init__(self,main):
		self.main=main
		self.config={}
		
		self.config['sound_login']={'type':'boolean','label':self.main.tr("Play sound on login"),'value':'True','groupbox':self.main.tr('Sounds'),'tab':self.main.tr("Sounds")}
		self.config['sound_first_message']={'type':'boolean','label':self.main.tr("Play sound on first message from user"),'value':'True','groupbox':self.main.tr('Sounds'),'tab':self.main.tr("Sounds")}
		self.config['sound_message']={'type':'boolean','label':self.main.tr("Play sound on other messages from user"),'value':'True','groupbox':self.main.tr('Sounds'),'tab':self.main.tr("Sounds")}
		self.config['sound_gc_message']={'type':'boolean','label':self.main.tr("Play sound if groupchat message contains your nickname"),'value':'True','groupbox':self.main.tr('Sounds'),'tab':self.main.tr("Sounds")}
		self.config['sound_presence']={'type':'boolean','label':self.main.tr("Play sound on new presence"),'value':'True','groupbox':self.main.tr('Sounds'),'tab':self.main.tr("Sounds")}
		self.config['sound_ft']={'type':'boolean','label':self.main.tr("Play sound on file transfer"),'value':'True','groupbox':self.main.tr('Sounds'),'tab':self.main.tr("Sounds")}

		self.config['notification_timeout']={'type':'number-spin','label':self.main.tr("How long should be notification show? (10 = 1 second)"),'value':'15','groupbox':self.main.tr('Libnotify'),'tab':self.main.tr("Libnotify")}

		self.config['notify_on_presence']={'type':'boolean','label':self.main.tr("Use notifications for presences"),'value':'True','groupbox':self.main.tr('Libnotify'),'tab':self.main.tr("Libnotify")}
		self.config['notify_about_unavaiable']={'type':'boolean','label':self.main.tr("Notify about unavaiable status change?"),'value':'False','groupbox':self.main.tr('Libnotify'),'tab':self.main.tr("Libnotify")}
		self.config['notify_first_message']={'type':'boolean','label':self.main.tr("Use notifications for first message"),'value':'True','groupbox':self.main.tr('Libnotify'),'tab':self.main.tr("Libnotify")}
		self.config['notify_on_message']={'type':'boolean','label':self.main.tr("Use notifications for other messages"),'value':'True','groupbox':self.main.tr('Libnotify'),'tab':self.main.tr("Libnotify")}
		
		self.config['notify_on_gcmessage']={'type':'boolean','label':self.main.tr("Use notifications for groupchat messages"),'value':'False','groupbox':self.main.tr('Libnotify'),'tab':self.main.tr("Libnotify")}
		self.config['notify_muc_highlight']={'type':'boolean','label':self.main.tr("Use notifications when someone wrote my nick in groupchat"),'value':'False','groupbox':self.main.tr('Libnotify'),'tab':self.main.tr("Libnotify")}
		
		self.config['avatar_size']={'type':'list-single','label':self.main.tr("Avatar size:"), 'items':{'16':'16', '22':'22', '32':'32', '48':'48'}, 'value':'32','groupbox':self.main.tr('Libnotify'),'tab':self.main.tr("Libnotify")}
		
		#bubble
		self.config['bubble_first_message']={'type':'boolean','label':self.main.tr("Use bubble notifications instead of libnotify for first message"),'value':'False','groupbox':self.main.tr('Tray icon'),'tab':self.main.tr("Tray icon")}
		self.config['bubble_on_message']={'type':'boolean','label':self.main.tr("Use bubble notifications instead of libnotify for other messages"),'value':'False','groupbox':self.main.tr('Tray icon'),'tab':self.main.tr("Tray icon")}
		
		self.config['bubble_on_presence']={'type':'boolean','label':self.main.tr("Use bubble notifications instead of libnotify for presences"),'value':'False','groupbox':self.main.tr('Tray icon'),'tab':self.main.tr("Tray icon")}
		
		self.config['bubble_muc_highlight']={'type':'boolean','label':self.main.tr("Use bubble notifications instead of libnotify when someone wrote my nick on chatroom"),'value':'False','groupbox':self.main.tr('Tray icon'),'tab':self.main.tr("Tray icon")}
		self.config['bubble_on_gcmessage']={'type':'boolean','label':self.main.tr("Use bubble notifications instead of libnotify for all conference messages"),'value':'False','groupbox':self.main.tr('Tray icon'),'tab':self.main.tr("Tray icon")}

class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'libnotify' # jmeno adresare pluginu
		self.description = 'Simple notifications for GNOME/Xfce. It using libnotify or bubbles supported by QT4 tray icon. PS. I dedicate it for my love Agatka :*'
		self.author = "Krzysztof 'Grom' Klinikowski"
		self.name = 'Jabbim Libnotify'
		self.version = '0.3' # verze plugins, musi byt float (desetinne cislo)
		self.category = ['notification'] # kategorie pluginu 
		self.url = 'http://dev.jabbim.cz/jabbim' # url na domovskou stranku pluginu

		if sys.platform == 'win32':
			print 'This plugin wont work on Windows OS.'

		self.showInPreferences=True
		self.preferencesIcon=QtGui.QIcon(plugindir+"/notification-icon.png")

		self.configDialog=config(self)
		if main:
			self.registerHandler('firstChatMessageEvent',self.on_firstChatMessageEvent)
			self.registerHandler('chatMessageEvent',self.on_chatMessageEvent)
			self.registerHandler('groupchatMessageEvent',self.on_groupchatMessageEvent)
			self.registerHandler('groupchatMessageForMeEvent',self.on_groupchatMessageForMeEvent)
			self.registerHandler('presenceEvent',self.on_presence)
			self.registerHandler('FTStartedEvent',self.on_FTStarted)
			self.registerHandler('FTFinishedEvent',self.on_FTFinished)
			self.loadConfig() # nacteni konfiguracniho souboru pro plugin
			if self.config['sound_login']=="True":
				self.main.playsound('start')
			print "Plugin Jabbim Libnotify works :)" # informujeme do jabbim.log ze se plugin nacetl :)
		else:

			self.loadConfig(homedir)
			
	def on_FTStarted(self,sid,el):
		if self.config['sound_ft']=='True':
			self.main.playsound('ft_start')
	
	def on_FTFinished(self,sid,error):
		if self.config['sound_ft']=='True':
			self.main.playsound('ft_finish')
		
		
	def on_presence(self,jid,user,show,status,first):
		if first:
			return
		if self.config['notify_on_presence']=="True":
			if not status:
				status=""

			pixmap=gtk.gdk.pixbuf_new_from_file_at_size(self.main.getAvatarSrc(jid.userhost()), int(self.config['avatar_size']), int(self.config['avatar_size']))
			#pynotify.Notification(pixmap).show()
			if self.config['notify_about_unavaiable'] == 'False' and self.main.status[unicode(show)] == self.tr("Unavailable"):
				print "Skipping notify show..."
			else:
				#print self.config['notify_about_unavaiable']+' sasasaasasa '+self.main.status[unicode(show)]
				n = pynotify.Notification(str(user+self.tr(" is now ")+self.main.status[unicode(show)]), unicode(status));
				n.set_icon_from_pixbuf(pixmap)
				n.set_timeout((int(self.config['notification_timeout'])*100))
				n.show();
		if show=="offline":
			self.main.playsound("contact_offline")
		else:
			self.main.playsound("contact_online")
		
	def on_firstChatMessageEvent(self, msg,event=None):
		if msg.body == None or not self.isNotificationEnabled():
			return
		jid=msg.frm
		user=msg.user
		if msg.body.startswith('/me '):
			msg.body = msg.body.replace('/me', '*'+user)
		# cut message if it's too long
		if len(msg.body)>40:
			traytext=msg.body[:40]+" …"
		else:
			traytext=msg.body
		if not self.main.chat.isActiveWindow():
			if self.config['bubble_first_message']=="True":
				self.main.tray.showMessage(self.tr("First message from ")+unicode(user), traytext, QtGui.QSystemTrayIcon.Information, 4000)
			else:		
				# inform user about newly opened tab
				pixmap=gtk.gdk.pixbuf_new_from_file_at_size(self.main.getAvatarSrc(jid.userhost()), int(self.config['avatar_size']), int(self.config['avatar_size']))
				n = pynotify.Notification(str("First message from "+user), unicode(traytext));
				#n.attach_to_status_icon(self.main.tray)
				n.set_icon_from_pixbuf(pixmap)
				n.set_timeout((int(self.config['notification_timeout'])*100))
				n.show();
		if self.config['sound_first_message']=="True":
			self.main.playsound('new_message')

			
	def on_chatMessageEvent(self,msg,event=None):
		if msg.body == None:
			return
		jid=msg.frm
		user=msg.user
		if msg.body.startswith('/me '):
			msg.body = msg.body.replace('/me', '*'+user)
		# inform user about new message
		if self.config['notify_on_message']=="True" and not self.main.chat.isActiveWindow():
			if len(msg.body)>40:
				traytext=msg.body[:40]+" …"
			else:
				traytext=msg.body
			if self.config['bubble_on_message'] == 'True':
				self.main.tray.showMessage(self.tr("New message from ")+unicode(user), traytext, QtGui.QSystemTrayIcon.Information, 4000)
			else:
				pixmap=gtk.gdk.pixbuf_new_from_file_at_size(self.main.getAvatarSrc(jid.userhost()), int(self.config['avatar_size']), int(self.config['avatar_size']))
				n = pynotify.Notification(self.tr("New message from "+user), unicode(traytext));
				n.set_icon_from_pixbuf(pixmap)
				n.set_timeout((int(self.config['notification_timeout'])*100))
				n.show();
		if self.config['sound_message']=="True":
			self.main.playsound('message')


	def on_groupchatMessageEvent(self,frm,user,body,subject, xhtml):
		if body == None:
			return
		jid=frm
		user=user
		if body.startswith('/me '):
			body = body.replace('/me', '*'+user)
		# inform user about new message
		if self.config['notify_on_gcmessage']=="True" and not self.main.chat.isActiveWindow():
			if len(body)>40:
				traytext=body[:40]+" …"
			else:
				traytext=body
			is_none = self.main.getAvatarSrc(jid.userhost()+"/"+user).split("/")
			if str(is_none[-1]) != "None":
				pixmap=gtk.gdk.pixbuf_new_from_file_at_size(self.main.getAvatarSrc(jid.userhost()+"/"+str(user)), int(self.config['avatar_size']), int(self.config['avatar_size']))
			else:
				pixmap=gtk.gdk.pixbuf_new_from_file_at_size(self.main.getAvatarSrc(jid.userhost()), int(self.config['avatar_size']), int(self.config['avatar_size']))
			n = pynotify.Notification(self.tr("New groupchat message from "+user), unicode(traytext))
			n.set_icon_from_pixbuf(pixmap)
			n.set_timeout((int(self.config['notification_timeout'])*100))
			n.show();



	def on_groupchatMessageForMeEvent(self,frm,user,body,subject, xhtml):
		jid=frm
		user=user
		if self.config['notify_muc_highlight'] == "True" and not self.main.chat.isActiveWindow():
			if len(body)>40:
				text=body[:40]+" …"
			else:
				text=body
			traytext=unicode(user)+": "+text

			if self.config['bubble_muc_highlight'] == 'True':
				self.main.tray.showMessage(self.tr("New groupchat message for you"), traytext, QtGui.QSystemTrayIcon.Information, 4000)
			else:
				if jid.userhost()+"/"+user != None:
					pixmap=gtk.gdk.pixbuf_new_from_file_at_size(self.main.getAvatarSrc(jid.userhost()+"/"+user), int(self.config['avatar_size']), int(self.config['avatar_size']))
				else:
					pixmap=gtk.gdk.pixbuf_new_from_file_at_size(self.main.getAvatarSrc(jid.userhost()), int(self.config['avatar_size']), int(self.config['avatar_size']))
				pixmap=gtk.gdk.pixbuf_new_from_file_at_size(self.main.getAvatarSrc(jid.userhost()+"/"+user), int(self.config['avatar_size']), int(self.config['avatar_size']))
				n = pynotify.Notification(self.tr("New groupchat message for you"), traytext);
				n.set_icon_from_pixbuf(pixmap)
				n.set_timeout((int(self.config['notification_timeout'])*100))
				n.show();
		if self.config['sound_gc_message']=="True":
			self.main.playsound('message')
