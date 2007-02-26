try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from preferences_ui import *
from preferences_bookmarks_ui import *
from configobj import ConfigObj
import os

class preferencesWindow(QtGui.QDialog):
	def __init__(self,main,parent=None,page=0):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.main=main
		self.bookmarks=self.main.bookmarks
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
		self.loadBookmarks()
		QtCore.QObject.connect(self.ui.bookmarks, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.bookmarkClicked)
		QtCore.QObject.connect(self.ui.addBookmark, QtCore.SIGNAL("clicked()"),self.addBookmark)
		QtCore.QObject.connect(self.ui.editBookmark, QtCore.SIGNAL("clicked()"),self.bookmarkClicked)
		QtCore.QObject.connect(self.ui.removeBookmark, QtCore.SIGNAL("clicked()"),self.removeBookmark)
		QtCore.QObject.connect(self.ui.chatSkins, QtCore.SIGNAL("activated ( const QString & )"),self.chatSkinsChanged)

	def removeBookmark(self):
		item=self.ui.bookmarks.currentItem()
		self.ui.bookmarks.takeTopLevelItem(self.ui.bookmarks.indexOfTopLevelItem(item))
		del self.bookmarks[unicode(item.text(0))]

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
		self.chatSkinPreviewtextEditWrite(testConfig["message"].replace("[time]",self.main.now()).replace("[user]",self.tr("User")).replace("[message]",self.tr("This is test message.")))
		self.chatSkinPreviewtextEditWrite(testConfig["my_message"].replace("[time]",self.main.now()).replace("[user]",self.tr("Me")).replace("[message]",self.tr("This is my test message.")))
		self.chatSkinPreviewtextEditWrite(testConfig["status_message"].replace("[time]",self.main.now()).replace("[message]",self.tr("User has set the subject to: Subject")))

	def loadBookmarks(self):
		self.ui.bookmarks.clear()
		for room,nick in self.bookmarks.iteritems():
			item=QtGui.QTreeWidgetItem(self.ui.bookmarks)
			item.setText(0,room)
			item.setText(1,nick)
		self.ui.bookmarks.resizeColumnToContents(0)
		self.ui.bookmarks.resizeColumnToContents(1)

	def addBookmark(self):
		edit=editBookmark(self.main,"","",self,False)
		ret=edit.exec_()
		if ret==1:
			self.loadBookmarks()

	def bookmarkClicked(self,item=None,row=None):
		if item==None:
			item=self.ui.bookmarks.currentItem()
			if item==None:
				return
		edit=editBookmark(self.main,unicode(item.text(0)),unicode(item.text(1)),self)
		ret=edit.exec_()
		if ret==1:
			self.loadBookmarks()
			
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
		# we need to update groupchat bookmarks menu
		self.main.bookmarks=self.bookmarks
		self.main.bookmarks.write()
		self.main.buildGroupchatMenu()
		self.done(1)
		
class editBookmark(QtGui.QDialog):
	def __init__(self,main,room,nickname,parent,edit=True):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.parent=parent
		self.room=room
		self.main=main
		self.edit=edit
		self.setModal(True)
		self.ui=Ui_editbookmark()
		self.ui.setupUi(self)
		self.ui.room.setText(room)
		self.ui.nickname.setText(nickname)

	def accept(self):
		room=unicode(self.ui.room.text())
		nickname=unicode(self.ui.nickname.text())
		if self.room==room:
			self.parent.bookmarks[room]=nickname
			self.parent.bookmarks.write()
			self.done(1)
		else:
			if self.parent.bookmarks.has_key(room):
				print "error"
			else:
				if self.edit==True:
					del self.parent.bookmarks[self.room]
				self.parent.bookmarks[room]=nickname
				self.done(1)
		