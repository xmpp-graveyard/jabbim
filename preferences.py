try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from preferences_ui import *
from preferences_bookmarks_ui import *
from configobj import ConfigObj
import os

class preferencesWindow(QtGui.QDialog):
	def __init__(self,main,parent=None,page=0,jab=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.main=main
		self.jab=jab
		self.setModal(False)
		self.ui=Ui_preferences()
		self.ui.setupUi(self)
		self.ui.stackedWidget.setCurrentIndex(page)
		self.ui.password.setText(self.main.config['passwd'])
		self.ui.jid.setText(self.main.config['jid'])
		if self.main.config["proxy_type"]=="none":
			self.ui.proxy_type.setCurrentIndex(0)
		elif self.main.config["proxy_type"]=="http":
			self.ui.proxy_type.setCurrentIndex(1)
		elif self.main.config["proxy_type"]=="socks4":
			self.ui.proxy_type.setCurrentIndex(2)
		elif self.main.config["proxy_type"]=="socks5":
			self.ui.proxy_type.setCurrentIndex(3)
		self.ui.proxy_server.setText(self.main.config['proxy_server'])
		self.ui.proxy_port.setText(self.main.config['proxy_port'])
		self.ui.proxy_username.setText(self.main.config['proxy_user'])
		self.ui.proxy_password.setText(self.main.config['proxy_passwd'])
		
		if self.main.config["tray_message_view_connect"]=="all":
			self.ui.notificationAll.setChecked(True)
		elif self.main.config["tray_message_view_connect"]=="online":
			self.ui.notificationOnline.setChecked(True)
		elif self.main.config["tray_message_view_connect"]=="logged_in":
			self.ui.notificationLoggedIn.setChecked(True)
		
		if self.main.config["tray_message_view_new_message"]=="all":
			self.ui.notification_new_message_all.setChecked(True)
		elif self.main.config["tray_message_view_new_message"]=="not_chat":
			self.ui.notification_new_message_chat.setChecked(True)
		
		
		skins=os.listdir("skins/")
		for skin in skins:
			if skin.endswith(".conf"):
				if skin==self.main.config["chat_skin"]:
					self.ui.chatSkins.insertItem(0,unicode(skin))
					self.chatSkinsChanged(skin)
				else:
					self.ui.chatSkins.addItem(unicode(skin))
		self.ui.chatSkins.setCurrentIndex(0)

		QtCore.QObject.connect(self.ui.chatSkins, QtCore.SIGNAL("activated ( const QString & )"),self.chatSkinsChanged)


	def chatSkinPreviewtextEditWrite(self,text):
		cur=self.ui.chatSkinPreview.textCursor()
		cur.movePosition(QtGui.QTextCursor.End)
		self.ui.chatSkinPreview.setTextCursor(cur)
		self.ui.chatSkinPreview.insertHtml(text)
		cur=self.ui.chatSkinPreview.textCursor()
		cur.movePosition(QtGui.QTextCursor.End)
		self.ui.chatSkinPreview.setTextCursor(cur)

	def chatSkinsChanged(self,file):
		file=unicode(file)
		testConfig=ConfigObj("skins/"+file,encoding='UTF8')
		self.ui.chatSkinPreview.clear()
		self.chatSkinPreviewtextEditWrite(testConfig["message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("This is test message."))))
		self.chatSkinPreviewtextEditWrite(testConfig["my_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("Me"))).replace("[message]",unicode(self.tr("This is my test message."))))
		self.chatSkinPreviewtextEditWrite(testConfig["status_message"].replace("[time]",self.main.now()).replace("[message]",unicode(self.tr("User has set the subject to: Subject"))))

	def accept(self):
		jid=unicode(self.ui.jid.text())
		password=unicode(self.ui.password.text())
		self.main.skin=ConfigObj("skins/"+unicode(self.ui.chatSkins.currentText()),encoding='UTF8')
		self.main.config['passwd']=password
		self.main.config['chat_skin']=unicode(self.ui.chatSkins.currentText())
		self.main.config['jid']=jid
		index=int(self.ui.proxy_type.currentIndex())
		if index==0:
			self.main.config["proxy_type"]="none"
		elif index==1:
			self.main.config["proxy_type"]="http"
		elif index==2:
			self.main.config["proxy_type"]="socks4"
		elif index==3:
			self.main.config["proxy_type"]="socks5"
		self.main.config['proxy_server']=unicode(self.ui.proxy_server.text())
		self.main.config['proxy_port']=unicode(self.ui.proxy_port.text())
		self.main.config['proxy_user']=unicode(self.ui.proxy_username.text())
		self.main.config['proxy_passwd']=unicode(self.ui.proxy_password.text())
		if self.ui.notificationAll.isChecked()==True:
			self.main.config["tray_message_view_connect"]="all"
		if self.ui.notificationOnline.isChecked()==True:
			self.main.config["tray_message_view_connect"]="online"
		if self.ui.notificationLoggedIn.isChecked()==True:
			self.main.config["tray_message_view_connect"]="logged_in"
		if self.ui.notification_new_message_chat.isChecked()==True:
			self.main.config["tray_message_view_new_message"]="not_chat"
		if self.ui.notification_new_message_all.isChecked()==True:
			self.main.config["tray_message_view_new_message"]="all"
		
		self.main.config.write()
		self.done(1)
		
class editBookmark(QtGui.QDialog):
	def __init__(self,main,jab,room,server,name,nickname,password,parent,edit=True):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.parent=parent
		self.room=room
		self.jab=jab
		self.server=server
		self.main=main
		self.edit=edit
		self.setModal(True)
		self.ui=Ui_editbookmark()
		self.ui.setupUi(self)
		self.ui.room.setText(room)
		self.ui.server.setText(server)
		self.ui.name.setText(name)
		self.ui.nickname.setText(nickname)
		self.ui.password.setText(password)

	def accept(self):
		room=unicode(self.ui.room.text())
		server=unicode(self.ui.server.text())
		name=unicode(self.ui.name.text())
		nickname=unicode(self.ui.nickname.text())
		password=unicode(self.ui.password.text())
		edited=False
		if self.room+"@"+self.server==room+"@"+server:
			self.main.bookmarks[room+"@"+server]={"name":name,"nick":nickname,"autojoin":"0","password":password}
			#self.done(1)
			edited=True
		else:
			if self.main.bookmarks.has_key(room):
				print "error"
			else:
				if self.edit==True:
					del self.main.bookmarks[self.room+"@"+self.server]
				self.main.bookmarks[room+"@"+server]={"name":name,"nick":nickname,"autojoin":"0","password":password}
				edited=True
		if edited:
			#self.main.bookmarks=self.bookmarks
			self.jab.setBookmarks(self.main.bookmarks)
			#self.main.buildGroupchatMenu()

			self.done(1)
		