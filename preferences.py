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
		self.setModal(False)
		self.ui=Ui_preferences()
		self.ui.setupUi(self)
		self.ui.stackedWidget.setCurrentIndex(page)
		self.ui.password.setText(self.main.config['passwd'])
		self.ui.jid.setText(self.main.config['jid'])
		skins=os.listdir("skins/")
		for skin in skins:
			if skin.endswith(".conf"):
				if skin==self.main.config["chat_skin"]:
					self.ui.chatSkins.insertItem(0,unicode(skin))
					self.chatSkinsChanged(skin)
				else:
					self.ui.chatSkins.addItem(unicode(skin))
					
		self.loadBookmarks()
		QtCore.QObject.connect(self.ui.bookmarks, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.bookmarkClicked)
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
		self.chatSkinPreviewtextEditWrite(testConfig["message"].replace("[time]",self.main.now()).replace("[user]",self.tr("User")).replace("[message]",self.tr("This is test message.")))
		self.chatSkinPreviewtextEditWrite(testConfig["my_message"].replace("[time]",self.main.now()).replace("[user]",self.tr("Me")).replace("[message]",self.tr("This is my test message.")))

	def loadBookmarks(self):
		self.ui.bookmarks.clear()
		for room,nick in self.main.bookmarks.iteritems():
			item=QtGui.QTreeWidgetItem(self.ui.bookmarks)
			item.setText(0,room)
			item.setText(1,nick)
		self.ui.bookmarks.resizeColumnToContents(0)
		self.ui.bookmarks.resizeColumnToContents(1)
	
	def bookmarkClicked(self,item,row):
		edit=editBookmark(self.main,unicode(item.text(0)),unicode(item.text(1)),self)
		ret=edit.exec_()
		if ret==1:
			self.loadBookmarks()
			# we need to update groupchat bookmarks menu
			self.main.buildGroupchatMenu()
			
	def accept(self):
		jid=unicode(self.ui.jid.text())
		password=unicode(self.ui.password.text())
		self.main.skin=ConfigObj("skins/"+unicode(self.ui.chatSkins.currentText()),encoding='UTF8')
		self.main.config['passwd']=password
		self.main.config['chat_skin']=unicode(self.ui.chatSkins.currentText())
		self.main.config['jid']=jid
		self.main.config.write()
		self.done(1)
		
class editBookmark(QtGui.QDialog):
	def __init__(self,main,room,nickname,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.room=room
		self.main=main
		self.setModal(True)
		self.ui=Ui_editbookmark()
		self.ui.setupUi(self)
		self.ui.room.setText(room)
		self.ui.nickname.setText(nickname)

	def accept(self):
		room=unicode(self.ui.room.text())
		nickname=unicode(self.ui.nickname.text())
		if self.room==room:
			self.main.bookmarks[room]=nickname
			self.main.bookmarks.write()
			self.done(1)
		else:
			if self.main.bookmarks.has_key(room):
				print "error"
			else:
				self.main.bookmarks[room]=nickname
				self.main.bookmarks.write()
				self.done(1)
		