try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
import sys; sys.path.append('..')
from preferences_ui import *
from preferences_bookmarks_ui import *
from configobj import ConfigObj
import os
import pyxl
from imp import load_source
import shutil
from twisted.python import log


class preferencesWindow(QtGui.QDialog):
	def __init__(self,main,parent=None,page=0):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.main=main
		self.setModal(False)
		self.ui=Ui_preferences()
		self.ui.setupUi(self)
		self.ui.stackedWidget.setCurrentIndex(page)

		# Jabbim
		if self.main.config['saveGeometry']=='True':
			self.ui.savePosition.setChecked(True)
		else:
			self.ui.savePosition.setChecked(False)

		# connection
		self.ui.connection_password.setText(self.main.config['passwd'])
		self.ui.connection_jid.setText(self.main.config['jid'])

		# chat skins
		skins=os.listdir("skins/")
		for skin in skins:
			if skin.endswith(".conf"):
				if skin==self.main.config["chat_skin"]:
					self.ui.chatSkin_list.insertItem(0,unicode(skin))
					self.chatSkin_listChanged(skin)
				else:
					self.ui.chatSkin_list.addItem(unicode(skin))
		self.ui.chatSkin_list.setCurrentIndex(0)
		QtCore.QObject.connect(self.ui.chatSkin_list, QtCore.SIGNAL("activated ( const QString & )"),self.chatSkin_listChanged)

		# roster
		#index=self.ui.roster_iconSize.findText(self.main.config['rosterIconSize'])
		#self.ui.roster_iconSize.setCurrentIndex(int(index))

		# Themes
		skins=os.listdir("themes/")
		for skin in skins:
			if os.path.isdir("themes/"+skin) and os.path.exists("themes/"+skin+"/style.css"):
				preview=QtGui.QIcon('themes/'+skin+"/preview.png")
				item=QtGui.QListWidgetItem(preview,skin,self.ui.themes)
				item.setData(32,QtCore.QVariant(skin))
				if skin==self.main.config["theme"]:
					self.ui.themes.setCurrentItem(item)
		QtCore.QObject.connect(self.ui.themes, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem *, QListWidgetItem *)"),self.themeChanged)

		# Plugins
		#self.ui.plugins.header().hide()
		plugins=os.listdir("plugins/")
		self.loadedPlugins=self.main.config['plugins']
		for plugin in plugins:
			path = 'plugins/%s/%s.py'%(plugin, plugin)
			try: 
				f=open(path)
			except:
				log.msg('plugin load error: '+plugin)
				continue
			plug = load_source(plugin, path, f).Plugin(False)
			f.close()
			item=QtGui.QTreeWidgetItem(self.ui.plugins)
			widget=QtGui.QCheckBox(self.ui.plugins)
			if plugin in self.loadedPlugins:
				widget.setChecked(True)
			self.ui.plugins.setItemWidget(item,0,widget)
			item.setText(1,plug.name)
			item.setText(2,plug.description)
			item.setData(32,0,QtCore.QVariant(unicode(plugin)))
			log.msg("plugin "+plugin+" loaded.")
		self.ui.plugins.resizeColumnToContents (0)
		self.ui.plugins.resizeColumnToContents (1)

	def reskin(self,file=None):
		if file==None:
			file=self.main.config['theme']
			style=open("styles/"+file+"/style.css")
			self.setStyleSheet(style.read())
			style.close()
		else:
			style=open("themes/"+file+"/style.css")
			text=style.read()
			self.setStyleSheet(text)
			style.close()
			self.main.loadTheme(text)

	def themeChanged(self,item,old):
		data=item.data(32)
		file=unicode(data.toString())
		self.reskin(file)

	def chatSkinPreviewtextEditWrite(self,text):
		cur=self.ui.chatSkin_preview.textCursor()
		cur.movePosition(QtGui.QTextCursor.End)
		self.ui.chatSkin_preview.setTextCursor(cur)
		self.ui.chatSkin_preview.insertHtml(text)
		cur=self.ui.chatSkin_preview.textCursor()
		cur.movePosition(QtGui.QTextCursor.End)
		self.ui.chatSkin_preview.setTextCursor(cur)

	def chatSkin_listChanged(self,file):
		file=unicode(file)
		testConfig=ConfigObj("skins/"+file,encoding='UTF8')
		self.ui.chatSkin_preview.clear()
		self.chatSkinPreviewtextEditWrite(testConfig["message_history"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("This is test message send in past."))))
		self.chatSkinPreviewtextEditWrite(testConfig["my_message_history"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("Me"))).replace("[message]",unicode(self.tr("This is my test message send in past."))))
		self.chatSkinPreviewtextEditWrite(testConfig["message_for_me_history"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("Me"))+", "+unicode(self.tr("this is message contains my name send in past."))))
		self.chatSkinPreviewtextEditWrite(testConfig["message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("This is test message."))))
		self.chatSkinPreviewtextEditWrite(testConfig["my_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("Me"))).replace("[message]",unicode(self.tr("This is my test message."))))
		self.chatSkinPreviewtextEditWrite(testConfig["message_for_me"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("Me"))+", "+unicode(self.tr("this is message contains my name."))))
		self.chatSkinPreviewtextEditWrite(testConfig["status_message"].replace("[time]",self.main.now()).replace("[message]",unicode(self.tr("User has set the subject to: Subject"))))

	def accept(self):
		jid=unicode(self.ui.connection_jid.text())
		password=unicode(self.ui.connection_password.text())
		self.main.skin=ConfigObj("skins/"+unicode(self.ui.chatSkin_list.currentText()),encoding='UTF8')
		self.main.config['passwd']=password
		self.main.config['saveGeometry']=str(self.ui.savePosition.isChecked())
		self.main.config['chat_skin']=unicode(self.ui.chatSkin_list.currentText())
		self.main.config['jid']=jid
		#self.main.config['rosterIconSize']=unicode(self.ui.roster_iconSize.currentText())
		self.main.config['theme']=unicode(self.ui.themes.currentItem().data(32).toString())
		self.main.config.write()
		
		for i in range(int(self.ui.plugins.topLevelItemCount())):
			item=self.ui.plugins.topLevelItem(i)
			data=item.data(32,0)
			plugin=unicode(data.toString())
			widget=self.ui.plugins.itemWidget(item,0)
			if widget.isChecked()==True and not plugin in self.loadedPlugins:
				#shutil.copytree("plugins/"+plugin, self.main.homeDir+"/.jabbim/plugins/"+plugin)
				self.main.config['plugins'].append(plugin)
			elif widget.isChecked()==False and plugin in self.loadedPlugins:
				self.main.config['plugins'].remove(plugin)
				#shutil.rmtree(self.main.homeDir+"/.jabbim/plugins/"+plugin)
		
		#size=unicode(self.main.config['rosterIconSize']).rsplit("x")
		#self.main.ui.roster.setIconSize(QtCore.QSize(int(size[0]),int(size[1])))
		self.done(1)

class editBookmark(QtGui.QDialog):
	def __init__(self,main,room,server,name,nickname,password,autojoin,parent,edit=True):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.parent=parent
		self.room=room
		self.server=server
		self.main=main
		self.edit=edit
		self.name=name
		self.autojoin=autojoin
		self.setModal(True)
		self.ui=Ui_editbookmark()
		self.ui.setupUi(self)
		self.ui.room.setText(room)
		self.ui.server.setText(server)
		self.ui.name.setText(name)
		self.ui.nickname.setText(nickname)
		self.ui.password.setText(password)
		if (self.autojoin==True or self.autojoin=="True") or (self.autojoin==1 or self.autojoin=="1"):
			self.ui.autojoin.setChecked(True)
		else:
			self.ui.autojoin.setChecked(False)
			
	def accept(self):
		room=unicode(self.ui.room.text())
		server=unicode(self.ui.server.text())
		name=unicode(self.ui.name.text())
		nickname=unicode(self.ui.nickname.text())
		password=unicode(self.ui.password.text())
		autojoin=self.ui.autojoin.isChecked()
		edited=False
		if name==self.name:
			self.main.client.bookmarks['conference'][name]=pyxl.client.Bookmark(name, 'conference', room+"@"+server, autojoin, nickname, password)
			#self.done(1)
			edited=True
		else:
			if self.edit==True:
				del self.main.client.bookmarks['conference'][self.name]
			self.main.client.bookmarks['conference'][name]=pyxl.client.Bookmark(name, 'conference', room+"@"+server, autojoin, nickname, password)
			edited=True
		if edited:
			#self.main.bookmarks=self.bookmarks
			self.main.client.setBookmarks()
			self.main.buildBookmarks()

			self.done(1)
