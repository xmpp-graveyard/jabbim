"""
Copyright (C) 2007 	Jan 'Hanzz' Kaluza (hanzz at njs.netlab.cz)
Copyright (C) 2007	Jiri 'Sef' Gabrys	(sef at njs.netlab.cz)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
import sys; sys.path.append('..')
from preferences_ui import *
from include import rot13
from preferences_bookmarks_ui import *
from configobj import ConfigObj
import os
import pyxl
from imp import load_source
import shutil
from twisted.python import log

class pluginConfiguration(QtGui.QDialog):
	def __init__(self,plugin,parent):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.plugin=plugin
		self.setWindowTitle(plugin.name+" preferences")
		
		self.widgets={}
		
		#l=self.layout()
		
		layout=QtGui.QVBoxLayout(self)
		for key,item in plugin.config.iteritems():
			if item['type']=="boolean":
				widget=QtGui.QCheckBox(item['description'],self)
				if len(item['value'])==0:
					if item['default']=='True':
						widget.setChecked(True)
				else:
					if item['value']=='True':
						widget.setChecked(True)
				layout.addWidget(widget)
				self.widgets[key]=widget
			elif item['type']=="text":
				label=QtGui.QLabel(item['description'],self)
				if len(item['value'])==0:
					widget=QtGui.QLineEdit(item['default'],self)
				else:
					widget=QtGui.QLineEdit(item['value'],self)
				layout2=QtGui.QHBoxLayout()
				layout2.addWidget(label)
				layout2.addWidget(widget)
				layout.addLayout(layout2)
				self.widgets[key]=widget
				
		layout2=QtGui.QHBoxLayout()
		close=QtGui.QPushButton("Close",self)
		save=QtGui.QPushButton("Save",self)
		layout2.addStretch()
		layout2.addWidget(close)
		layout2.addWidget(save)
		
		QtCore.QObject.connect(save, QtCore.SIGNAL("clicked()"),self.accept)
		QtCore.QObject.connect(close, QtCore.SIGNAL("clicked()"),self.reject)
		
		layout.addLayout(layout2)
	
	def accept(self):
		for key, widget in self.widgets.iteritems():
			item=self.plugin.config[key]
			if item['type']=="boolean":
				self.plugin.config[key]['value']=str(widget.isChecked())
			elif item['type']=="text":
				print unicode(widget.text())
				self.plugin.config[key]['value']=unicode(widget.text())
		self.plugin.writeConfig()
		self.done(1)

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

		# Chat
		if self.main.config['showChatStatusChanges']=='True':
			self.ui.showChatStatusChanges.setChecked(True)
		else:
			self.ui.showChatStatusChanges.setChecked(False)

		if self.main.config['useMUCNames']=='True':
			self.ui.useMUCNames.setChecked(True)
		else:
			self.ui.useMUCNames.setChecked(False)
		if self.main.config['sendByCtrl']=='True':
			self.ui.sendByCtrl.setChecked(True)
		else:
			self.ui.sendByCtrl.setChecked(False)
		if self.main.config['showTransports']=='True':
			self.ui.showTransports.setChecked(True)
		else:
			self.ui.showTransports.setChecked(False)
		
		

		# connection
		self.ui.connection_password.setText(rot13.scramble(self.main.config['passwd']))
		self.ui.connection_jid.setText(self.main.config['jid'])
		if self.main.config.has_key('resource'):
			self.ui.connection_source.setText(self.main.config['resource'])
		else:
			self.ui.connection_source.setText('jabbim')
		if self.main.config.has_key('priority'):
			self.ui.connection_priority.setText(self.main.config['priority'])
		else:
			self.ui.connection_priority.setText('0')
		if self.main.config['autoJoin']=='True':
			self.ui.connection_autojoin.setChecked(True)
		else:
			self.ui.connection_autojoin.setChecked(False)
		
		if self.main.config.has_key('autoPriority'):
			if self.main.config['autoPriority']=='True':
				self.ui.connection_autoPriority.setChecked(True)
			else:
				self.ui.connection_autoPriority.setChecked(False)
		

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
#		index=self.ui.roster_iconSize.findText(self.main.config['rosterIconSize'])
#		log.msg(self.main.config['rosterIconSize'])
#		self.ui.roster_iconSize.setCurrentIndex(int(index))
		if self.main.config['rosterMode']=='compact':
			self.ui.roster_compact.toggle()

		# Themes
		skins=os.listdir("themes/")
		if self.main.config['theme']=="None":
			self.ui.useThemes.setChecked(False)
		for skin in skins:
			if os.path.isdir("themes/"+skin) and os.path.exists("themes/"+skin+"/style.css"):
				preview=QtGui.QIcon('themes/'+skin+"/preview.png")
				item=QtGui.QListWidgetItem(self.ui.themes)
				item.setIcon(preview)
				item.setSizeHint(QtCore.QSize(100,128))
				conf=ConfigObj("themes/"+skin+"/theme.ini",encoding='UTF8')
				if conf!=None and len(conf)!=0:
					text="<b>"+self.tr("Name: ")+"</b> "+conf['name']+'<br/>'
					text+="<b>"+self.tr("Author: ")+"</b> "+conf['author']+'<br/>'
					text+="<b>"+self.tr("Version: ")+"</b> "+conf['version']
				else:
					text="<b>"+self.tr("Name: ")+"</b> "+skin
				widget=QtGui.QLabel(text,self.ui.themes)
				widget.setTextFormat (QtCore.Qt.RichText)
				#widget.setMinimumHeight(128)
				#widget.setText("test<br/>test")
				self.ui.themes.setItemWidget(item,widget)
				item.setData(32,QtCore.QVariant(skin))
				if skin==self.main.config["theme"]:
					self.ui.themes.setCurrentItem(item)
					
		QtCore.QObject.connect(self.ui.themes, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem *, QListWidgetItem *)"),self.themeChanged)

		# Plugins
		#self.ui.plugins.header().hide()
		QtCore.QObject.connect(self.ui.pluginConfiguration, QtCore.SIGNAL("clicked()"),self.pluginConfigurationClicked)
		QtCore.QObject.connect(self.ui.plugins, QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.pluginsContextMenu)
		self.main.copyPlugins()
		plugins=os.listdir("plugins/")
		self.loadedPlugins=self.main.config['plugins']
		self.plugins={}
		for plugin in plugins:
			path = 'plugins/%s/%s.py'%(plugin, plugin)
			try: 
				f=open(path)
			except:
				log.msg('plugin load error: '+plugin)
				continue
			plug = load_source(plugin, path, f).Plugin(False,self.main.homeDir)
			f.close()
			item=QtGui.QTreeWidgetItem(self.ui.plugins)
			widget=QtGui.QCheckBox(self.ui.plugins)
			if plugin in self.loadedPlugins:
				widget.setChecked(True)
			self.ui.plugins.setItemWidget(item,0,widget)
			item.setText(1,plug.name)
			item.setText(2,plug.description)
			item.setData(32,0,QtCore.QVariant(unicode(plugin)))
			self.plugins[plugin]=plug
			log.msg("plugin "+plugin+" loaded.")
		self.ui.plugins.resizeColumnToContents (0)
		self.ui.plugins.resizeColumnToContents (1)

	def pluginsContextMenu(self,pos):
		# make groupchat bookmarks menu
		item=self.ui.plugins.itemFromIndex(self.ui.plugins.indexAt(pos)) # get selected item
		data=item.data(32,0)
		name=unicode(data.toString())
		plugin=self.plugins[name]
		menu=QtGui.QMenu(self.ui.plugins) # make menu
		# Join bookmarked groupchat
		action=menu.addAction(self.tr("Plugin Configuration"))
		action.setData(item.data(32,0))
		action.setObjectName("config")
		menu.connect(menu, QtCore.SIGNAL("triggered ( QAction * )"),self.pluginsContextMenuTriggered)
		# set menu position and show
		menu.move(self.ui.plugins.mapToGlobal(pos))
		menu.show()

	def pluginConfigurationClicked(self):
		item=self.ui.plugins.currentItem()
		data=item.data(32,0)
		name=unicode(data.toString())
		plugin=self.plugins[name]
		dialog=pluginConfiguration(self.plugins[name],self.ui.plugins)
		dialog.exec_()
		self.main.plugins[name].config=self.plugins[name].config

	def pluginsContextMenuTriggered(self,action):
		cmd=action.objectName()
		if cmd=="config":
			data=action.data()
			name=unicode(data.toString())
			plugin=self.plugins[name]
			dialog=pluginConfiguration(self.plugins[name],self.ui.plugins)
			dialog.exec_()
			self.main.plugins[name].config=self.plugins[name].config



	def reskin(self,file=None):
		if file==None:
			file=self.main.config['theme']
			style=open("themes/"+file+"/style.css")
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
		resource=unicode(self.ui.connection_source.text())
		password=unicode(self.ui.connection_password.text())
		self.main.skin=ConfigObj("skins/"+unicode(self.ui.chatSkin_list.currentText()),encoding='UTF8')
		if not self.main.skin.has_key("spaces_between_lines"):
			self.main.skin["spaces_between_lines"]='0'
		self.main.config['passwd']=rot13.scramble(password)
		self.main.config['autoJoin']=str(self.ui.connection_autojoin.isChecked())
		self.main.config['autoPriority']=str(self.ui.connection_autoPriority.isChecked())
		self.main.config['saveGeometry']=str(self.ui.savePosition.isChecked())
		self.main.config['useMUCNames']=str(self.ui.useMUCNames.isChecked())
		self.main.config['sendByCtrl']=str(self.ui.sendByCtrl.isChecked())
		self.main.config['showTransports']=str(self.ui.showTransports.isChecked())
		self.main.config['showChatStatusChanges']=str(self.ui.showChatStatusChanges.isChecked())
		self.main.config['chat_skin']=unicode(self.ui.chatSkin_list.currentText())
		self.main.config['jid']=jid
		self.main.config['resource']=''+resource+''
		self.main.config['priority']=self.ui.connection_priority.text()
		if not self.ui.useThemes.isChecked():
			self.main.config['theme']="None"
			self.main.loadTheme()
		else:
			self.main.config['theme']=unicode(self.ui.themes.currentItem().data(32).toString())
		if self.ui.roster_compact.isChecked()==True:
			self.main.config['rosterMode']="compact"
			self.main.ui.roster.userHeight=22
			self.main.ui.roster.groupHeight=22
			self.main.ui.roster.compact=True
			self.main.ui.roster.reshow=True
			self.main.ui.roster.statusLabel.hide()
		else:
			self.main.config['rosterMode']="normal"
			self.main.ui.roster.userHeight=32
			self.main.ui.roster.groupHeight=32
			self.main.ui.roster.compact=False
			self.main.ui.roster.reshow=True
			self.main.ui.roster.statusLabel.hide()
		self.main.ui.roster.repaint()
		self.main.config.write()
		
		for i in range(int(self.ui.plugins.topLevelItemCount())):
			item=self.ui.plugins.topLevelItem(i)
			data=item.data(32,0)
			plugin=unicode(data.toString())
			widget=self.ui.plugins.itemWidget(item,0)
			if widget.isChecked()==True and not plugin in self.loadedPlugins:
				#shutil.copytree("plugins/"+plugin, self.main.homeDir+"/.jabbim/plugins/"+plugin)
				self.main.loadPlugin(plugin)
				self.main.config['plugins'].append(plugin)
			elif widget.isChecked()==False and plugin in self.loadedPlugins:
				self.main.unloadPlugin(plugin)
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
		if ((self.autojoin==True or self.autojoin=="True") or (self.autojoin==1 or self.autojoin=="1")) or self.autojoin=="true":
			self.ui.autojoin.setChecked(True)
		else:
			self.ui.autojoin.setChecked(False)
			
	def accept(self):
		room=unicode(self.ui.room.text())
		server=unicode(self.ui.server.text())
		name=unicode(self.ui.name.text())
		nickname=unicode(self.ui.nickname.text())
		password=unicode(self.ui.password.text())
		autojoin=unicode(self.ui.autojoin.isChecked()).lower()
		if len(name.strip())<1:
			name = room
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
