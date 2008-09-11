"""
Copyright (C) 2007 	Jan 'Hanzz' Kaluza (hanzz at njs.netlab.cz)
Copyright (C) 2007	Jiri 'Sef' Gabrys	(sef at njs.netlab.cz)

This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
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
from include import plugins as pluginTemplate
from pref import jabbim,connection,chat,roster,privacy
from preferences_bookmarks_ui import *
from configobj import ConfigObj
import os
import pyxl
from imp import load_source
import shutil
from twisted.python import log
import dataforms
from twisted.words.xish import domish
#from twisted.web.microdom import *
import traceback
from extra import extraDialog
from os.path import basename
from pyxl import jid as jidT
import webkitthemes
from configlib import *

class message(QtCore.QObject):
	def __init__(self,message):
		QtCore.QObject.__init__(self)
		self.messages=message
		self.scr=1
		self.setObjectName("messageObject")

	@QtCore.pyqtSignature("int",result="QString")
	def msg(self,i):
		return self.messages[i]

	@QtCore.pyqtSignature("",result="int")
	def scroll(self):
		return self.scr

class preferencesWindow(QtGui.QDialog):
	def __init__(self,main,parent=None,page=0):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.main=main
		self.setModal(False)
		self.ui=Ui_preferences()
		self.ui.setupUi(self)
		self.ui.stackedWidget.setCurrentIndex(page)

		self.var=[]

		self.justShowed=False
		self.showedPlugins={}

		self.globalCategories={}
		self.globalCategories['notification']=self.tr('Notification')
		self.globalCategories['archive']=self.tr('Archive')
		self.globalCategories['log']=self.tr('Log')
		self.globalCategories['misc']=self.tr('Misc')
		self.globalCategories['jgames']=self.tr('jGames')
		self.globalCategories['disk']=self.tr('Disk')
		self.globalCategories['utils']=self.tr('Utils')
		self.globalCategories['fun']=self.tr('Fun')
		self.globalCategories['other']=self.tr('Other')

		self.preferencesCount=6
		# Jabbim
		layout=QtGui.QGridLayout(self.ui.jabbimWidget)
		self.var.append(makePreferences(self.main.config,self.ui.jabbimWidget,layout,jabbim.preferences(self).config)[0])

		# Chat
		layout=QtGui.QGridLayout(self.ui.chatWidget)
		self.var.append(makePreferences(self.main.config,self.ui.chatWidget,layout,chat.preferences(self).config)[0])

		# Roster
		layout=QtGui.QGridLayout(self.ui.rosterWidget)
		self.var.append(makePreferences(self.main.config,self.ui.rosterWidget,layout,roster.preferences(self).config)[0])

		# connection
		layout=QtGui.QGridLayout(self.ui.connectionWidget)
		self.var.append(makePreferences(self.main.config,self.ui.connectionWidget,layout,connection.preferences(self).config)[0])

		# privacy
		layout=QtGui.QGridLayout(self.ui.privacyWidget)
		self.var.append(makePreferences(self.main.config,self.ui.privacyWidget,layout,privacy.preferences(self).config)[0])

		QtCore.QObject.connect(self.ui.emoticonsList,QtCore.SIGNAL('activated ( int )'),self.emoticonsListChanged)
		QtCore.QObject.connect(self.ui.chatskinVariant,QtCore.SIGNAL('activated ( int )'),self.chatskinVariantChanged)
		QtCore.QObject.connect(self.ui.groupchatskinVariant,QtCore.SIGNAL('activated ( int )'),self.groupchatskinVariantChanged)
		QtCore.QObject.connect(self.ui.groupchatskinStyle,QtCore.SIGNAL('activated ( int )'),self.groupchatskinStyleChanged)
		QtCore.QObject.connect(self.ui.chatSkin_list, QtCore.SIGNAL("activated ( int )"),self.chatSkin_listChanged)

		QtCore.QObject.connect(self.ui.rosterStyle,QtCore.SIGNAL('activated ( int )'),self.rosterStyleChanged)
		
		QtCore.QObject.connect(self.ui.useThemes,QtCore.SIGNAL("stateChanged ( int )"),self.useThemesChanged)
		QtCore.QObject.connect(self.ui.themes, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem *, QListWidgetItem *)"),self.themeChanged)

		self.chatMessageObject=message("")
		QtCore.QObject.connect(self.ui.chatskinPreview,QtCore.SIGNAL("loadFinished ( bool)"),self.chatskinPreviewFinished)
		QtCore.QObject.connect(self.ui.chatskinPreview.page().mainFrame(),QtCore.SIGNAL("javaScriptWindowObjectCleared ()"),self.chatskinPreviewCleared)
		

		self.groupchatMessageObject=message("")
		QtCore.QObject.connect(self.ui.groupchatskinPreview,QtCore.SIGNAL("loadFinished ( bool)"),self.groupchatskinPreviewFinished)
		QtCore.QObject.connect(self.ui.groupchatskinPreview.page().mainFrame(),QtCore.SIGNAL("javaScriptWindowObjectCleared ()"),self.groupchatskinPreviewCleared)


		# Plugins
		QtCore.QObject.connect(self.ui.applyButton, QtCore.SIGNAL("clicked()"),self.save)
		QtCore.QObject.connect(self.ui.pluginConfiguration, QtCore.SIGNAL("clicked()"),self.pluginConfigurationClicked)
		QtCore.QObject.connect(self.ui.plugins, QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.pluginsContextMenu)
		QtCore.QObject.connect(self.ui.plugins, QtCore.SIGNAL("itemClicked ( QTreeWidgetItem *, int)"),self.pluginSelected)
		QtCore.QObject.connect(self.ui.listWidget, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem * , QListWidgetItem * )"),self.currentItemChanged)
		
		QtCore.QObject.connect(self.ui.moreEmoticons, QtCore.SIGNAL("clicked()"),self.getMoreEmoticons)
		QtCore.QObject.connect(self.ui.morePlugins, QtCore.SIGNAL("clicked()"),self.getMorePlugins)
		QtCore.QObject.connect(self.ui.moreChatSkins, QtCore.SIGNAL("clicked()"),self.getMoreChatskins)
		QtCore.QObject.connect(self.ui.moreGroupchatSkins, QtCore.SIGNAL("clicked()"),self.getMoreChatskins)
	
	def getMoreChatskins(self):
		if self.main.client:
			d=extraDialog("chatskins",self.main,self.main)
			d.exec_()
		else:
			QtGui.QMessageBox.information(self, self.tr("Informations"),self.tr("You have to be connected to download new chatskins."))
	
	def getMoreEmoticons(self):
		if self.main.client:
			d=extraDialog("emoticons",self.main,self.main)
			d.exec_()
		else:
			QtGui.QMessageBox.information(self, self.tr("Informations"),self.tr("You have to be connected to download new emoticons."))

	def getMorePlugins(self):
		if self.main.client:
			d=extraDialog("plugins",self.main,self.main)
			d.exec_()
		else:
			QtGui.QMessageBox.information(self, self.tr("Informations"),self.tr("You have to be connected to download new plugins."))

	def currentItemChanged(self,item,previous):
		"""
		Called when current preferences item is changed
		"""
		row=self.ui.listWidget.row(item)
		if self.justShowed:
			if row==self.preferencesCount-1:
				self.reloadView()
				self.justShowed=False
				return
		if previous:
			name=unicode(previous.data(32).toString())
			if self.showedPlugins.has_key(name):
				self.plugins[name].on_endPreferences()
		
		name=unicode(item.data(32).toString())
		if self.showedPlugins.has_key(name):
			if not self.showedPlugins[name]:
				plug=self.plugins[name]
				widget=self.ui.stackedWidget.widget(row)
				layout=QtGui.QGridLayout(widget)
				var,row=makePreferences(plug.config,widget,layout,plug.configDialog.config)
				spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
				layout.addItem(spacerItem,row+1,0)
				self.showedPlugins[name]=var
			self.plugins[name].on_showPreferences(self.ui.stackedWidget.widget(row))

	def reloadView(self,extraPart='',extraRoot=''):
		"""
		Reload view preferences
		"""
		self.ui.emoticonsList.clear()
		self.ui.chatSkin_list.clear()
		self.ui.groupchatskinStyle.clear()
		self.ui.rosterStyle.clear()
		self.ui.themes.clear()
		if extraPart.find("emoticons/")!=-1:
			pack=os.listdir(self.main.realHomeDir+'/emoticons/'+extraRoot)
			for emoticon in pack:
				if emoticon.endswith('.cfg'):
					currentEmoticons=unicode(extraRoot+'/'+emoticon).replace("//",'/')
					print "USING DONWLOADED EMOTICONS:",currentEmoticons
					break
			self.ui.tabWidget.setCurrentIndex(2)
		else:
			currentEmoticons=self.main.config["emoticons"]


		# emoticons from Jabbim root directory
		packs=os.listdir("emoticons/")
		for pack in packs:
			if os.path.isdir('emoticons/'+pack):
				emoticons=os.listdir('emoticons/'+pack+"/")
				for emoticon in emoticons:
					if emoticon.endswith('.cfg'):
						emo=pack+"/"+emoticon
						#config=ConfigObj("emoticons/"+emo,encoding='UTF8')
						loaded,config=self.main.loadJabbimExtraConfig("emoticons/"+emo,'emoticons/default/smileys.cfg')
						if loaded:
							if emo==currentEmoticons:
								item=self.ui.emoticonsList.insertItem(0,QtGui.QIcon('emoticons/'+os.path.dirname(emo)+"/"+unicode(config['header']['frontImage'])),unicode(config['header']['name']),QtCore.QVariant(emo))
							else:
								item=self.ui.emoticonsList.addItem(QtGui.QIcon('emoticons/'+os.path.dirname(emo)+"/"+unicode(config['header']['frontImage'])),unicode(config['header']['name']),QtCore.QVariant(emo))
		
		# emoticons from users home directory
		packs=os.listdir(self.main.realHomeDir+"/emoticons")
		for pack in packs:
			if os.path.isdir(self.main.realHomeDir+"/emoticons/"+pack):
				emoticons=os.listdir(self.main.realHomeDir+"/emoticons/"+pack+"/")
				for emoticon in emoticons:
					if emoticon.endswith('.cfg'):
						emo=pack+"/"+emoticon
						#config=ConfigObj(self.main.realHomeDir+"/emoticons/"+emo,encoding='UTF8')
						loaded,config=self.main.loadJabbimExtraConfig(self.main.realHomeDir+"/emoticons/"+emo,'emoticons/default/smileys.cfg')
						if loaded:
							if emo==currentEmoticons:
								item=self.ui.emoticonsList.insertItem(0,QtGui.QIcon(self.main.realHomeDir+"/emoticons/"+os.path.dirname(emo)+"/"+unicode(config['header']['frontImage'])),unicode(config['header']['name']),QtCore.QVariant(emo))
							else:
								item=self.ui.emoticonsList.addItem(QtGui.QIcon(self.main.realHomeDir+"/emoticons/"+os.path.dirname(emo)+"/"+unicode(config['header']['frontImage'])),unicode(config['header']['name']),QtCore.QVariant(emo))

		self.emoticonsListChanged(0)
		self.ui.emoticonsList.setCurrentIndex(0)


		packs=os.listdir("rosterstyles/")
		loaded=[]
		for pack in packs:
			if os.path.isdir('rosterstyles/'+pack):
				#skins=os.listdir('chatskins/'+pack+"/")
				#for skin in skins:
				path=pack
				if not path in loaded:
					loaded.append(path)
					if path==self.main.config["rosterStyle"].split("/")[0]:
						self.ui.rosterStyle.insertItem(0,path,QtCore.QVariant(path))
					else:
						self.ui.rosterStyle.addItem(path,QtCore.QVariant(path))

		packs=os.listdir(self.main.realHomeDir+'/rosterstyles/')
		for pack in packs:
			if os.path.isdir(self.main.realHomeDir+'/rosterstyles/'+pack):
				#skins=os.listdir('chatskins/'+pack+"/")
				#for skin in skins:
				path=pack
				if not path in loaded:
					loaded.append(path)
					if path==self.main.config["rosterStyle"].split("/")[0]:
						self.ui.rosterStyle.insertItem(0,path,QtCore.QVariant(path))
					else:
						self.ui.rosterStyle.addItem(path,QtCore.QVariant(path))
						
		# chat skins from Jabbim root directory
		packs=os.listdir("chatskins/")
		for pack in packs:
			if os.path.isdir('chatskins/'+pack) and os.path.isdir('chatskins/'+pack+"/Incoming"):
				#skins=os.listdir('chatskins/'+pack+"/")
				#for skin in skins:
				path=pack
				if path==self.main.config["chatTheme"].split("/")[0]:
					self.ui.chatSkin_list.insertItem(0,path,QtCore.QVariant(path))
				else:
					self.ui.chatSkin_list.addItem(path,QtCore.QVariant(path))
				if path==self.main.config["groupchatTheme"].split("/")[0]:
					self.ui.groupchatskinStyle.insertItem(0,path,QtCore.QVariant(path))
				else:
					self.ui.groupchatskinStyle.addItem(path,QtCore.QVariant(path))

		# chat skins from Jabbim home directory
		packs=os.listdir(self.main.realHomeDir+"/chatskins/")
		for pack in packs:
			if os.path.isdir(self.main.realHomeDir+'/chatskins/'+pack) and os.path.isdir(self.main.realHomeDir+'/chatskins/'+pack+'/Incoming'):
				path=pack
				if path==self.main.config["chatTheme"].split("/")[0]:
					self.ui.chatSkin_list.insertItem(0,path,QtCore.QVariant(path))
				else:
					self.ui.chatSkin_list.addItem(path,QtCore.QVariant(path))
				if path==self.main.config["groupchatTheme"].split("/")[0]:
					self.ui.groupchatskinStyle.insertItem(0,path,QtCore.QVariant(path))
				else:
					self.ui.groupchatskinStyle.addItem(path,QtCore.QVariant(path))

		self.chatSkin_listChanged(0)
		self.groupchatskinStyleChanged(0)
		self.ui.chatSkin_list.setCurrentIndex(0)
		self.ui.groupchatskinStyle.setCurrentIndex(0)
		self.ui.rosterStyle.setCurrentIndex(0)

		# Themes
		skins=os.listdir("themes/")
		QtCore.QObject.disconnect(self.ui.themes, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem *, QListWidgetItem *)"),self.themeChanged)

		for skin in skins:

			if os.path.isdir("themes/"+skin) and os.path.exists("themes/"+skin+"/style.css"):
				preview=QtGui.QIcon('themes/'+skin+"/preview.png")
				log.msg('SKIN:'+skin)

				item=QtGui.QListWidgetItem(self.ui.themes)
				item.setIcon(preview)
				item.setSizeHint(QtCore.QSize(100,128))
				conf=ConfigObj("themes/"+skin+"/theme.ini",encoding='UTF8')
				if conf!=None and len(conf)!=0:
					#text="<b>"+self.tr("Name: ")+"</b> "+conf['name']+'<br/>'
					#text+="<b>"+self.tr("Author: ")+"</b> "+conf['author']+'<br/>'
					#text+="<b>"+self.tr("Version: ")+"</b> "+conf['version']
					#text="<b>"+self.tr("Name: ")+"</b> "+conf['name']+'<br/>'
					#text+="<b>"+self.tr("Author: ")+"</b> "+conf['author']+'<br/>'
					#text+="<b>"+self.tr("Version: ")+"</b> "+conf['version']
					try:
						text = self.tr("Name: %1\nAuthor: %2\nVersion: %3") \
											.arg(conf['name']) \
											.arg(conf['author']) \
											.arg(conf['version'])
					except:
						text = self.tr("Name: ") + skin
				else:
					text = self.tr("Name: ") + skin

				#widget=QtGui.QLabel(text,self.ui.themes)
				#widget.setTextFormat (QtCore.Qt.RichText)
				#widget.setMinimumHeight(128)
				item.setText(text)
				#widget.setText("test<br/>test")
				#self.ui.themes.setItemWidget(item,widget)
				item.setData(32,QtCore.QVariant(skin))
				if skin==self.main.config["theme"]:
					self.ui.themes.setCurrentItem(item)
		QtCore.QObject.connect(self.ui.themes, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem *, QListWidgetItem *)"),self.themeChanged)

	def reloadPlugins(self):
		for i in range(self.preferencesCount+1,int(self.ui.listWidget.count())):
			self.ui.listWidget.takeItem(self.preferencesCount+1)
			widget=self.ui.stackedWidget.widget(self.preferencesCount+1)
			self.ui.stackedWidget.removeWidget(widget)
			del widget
		for plugin,plug in self.plugins.iteritems():
			if plug.configDialog and plug.showInPreferences and plugin in self.loadedPlugins:
				listItem=QtGui.QListWidgetItem(plug.name,self.ui.listWidget)
				listItem.setData(32,QtCore.QVariant(plugin))
				listItem.setIcon(QtGui.QIcon(plug.preferencesIcon))
				widget=QtGui.QWidget()
				self.ui.stackedWidget.addWidget(widget)
				self.showedPlugins[plugin]=None

	def reloadPreferences(self):
		self.ui.stackedWidget.setCurrentIndex(0)
		self.ui.listWidget.setCurrentRow(0)
		if self.main.config['theme']=="None":
			self.ui.useThemes.setChecked(False)
		self.currentTheme=self.main.config['theme']
		self.justShowed=True
		if self.main.client:
			self.ui.profile.hide()
		else:
			self.ui.profile.setText("<b>"+self.tr("Profile:")+"</b> "+unicode(self.main.config['jid']))
			self.ui.profile.show()
		for cfg in self.var:
			updateVarData(cfg,self.main.config)

		self.reloadPlugins_()
		
	def reloadPlugins_(self):
		for i in range(self.preferencesCount+1,int(self.ui.listWidget.count())):
			self.ui.listWidget.takeItem(self.preferencesCount+1)
			widget=self.ui.stackedWidget.widget(self.preferencesCount+1)
			self.ui.stackedWidget.removeWidget(widget)
			del widget
		self.loadedPlugins=self.main.config['plugins']
		self.plugins={}
		self.showedPlugins={}
		self.ui.plugins.clear()
		self.main.findPlugins()
		plugins=self.main.plugins.keys()
		
		categories={}
		for category,translation in self.globalCategories.iteritems():
			categories[category]=QtGui.QTreeWidgetItem(self.ui.plugins)
			categories[category].setText(0,translation)
		for plugin in plugins:
			dir = self.main.plugins[plugin]['dir']
			path = '%s/%s.py' % (dir, plugin)
			try: 
				f=open(path)
			except:
				log.msg('plugin load error: '+plugin)
				continue

			try: 
				plug = load_source(plugin, path, f).Plugin(False, self.main.homeDir, dir)
			except Exception, ex:
				log.msg(plugin+': CHYBA PRI NAHRAVANI => SPATNA SYNTAXE V PLUGINU!')
				message = unicode(traceback.format_exc(), 'utf-8')
				print message
				f.close()
				continue
			plug.main=self.main
			f.close()
			if categories.has_key(plug.category[0]):
				item=QtGui.QTreeWidgetItem(categories[plug.category[0]])
			else:
				item=QtGui.QTreeWidgetItem(categories['other'])
			#widget=QtGui.QCheckBox(self.ui.plugins)
			print plugin,self.loadedPlugins
			item.setFlags(item.flags()|QtCore.Qt.ItemIsUserCheckable)
			if plugin in self.loadedPlugins:
				print "setChecked True"
				#widget.setChecked(True)
				item.setCheckState(0,QtCore.Qt.Checked)
				self.ui.plugins.setItemExpanded(item.parent(),True)
			else:
				item.setCheckState(0,QtCore.Qt.Unchecked)
			#self.ui.plugins.setItemWidget(item,0,widget)
			item.setText(1,plug.name)
			item.setData(32,1,QtCore.QVariant(unicode(plug.description)))
			item.setData(32,0,QtCore.QVariant(unicode(plugin)))
			
			
			self.plugins[plugin]=plug
			if plug.configDialog and plug.showInPreferences and plugin in self.loadedPlugins:
				listItem=QtGui.QListWidgetItem(plug.name,self.ui.listWidget)
				listItem.setData(32,QtCore.QVariant(plugin))
				listItem.setIcon(QtGui.QIcon(plug.preferencesIcon))
				widget=QtGui.QWidget()
				self.ui.stackedWidget.addWidget(widget)
				self.showedPlugins[plugin]=None
			log.msg("plugin "+plugin+" loaded.")
		self.ui.plugins.resizeColumnToContents (0)
		self.ui.plugins.resizeColumnToContents (1)
		for category,item in categories.iteritems():
			if item.childCount()==0:
				self.ui.plugins.setItemHidden(item, True)

	def emoticonsListChanged(self,index):
		path=unicode(self.ui.emoticonsList.itemData(index).toString())
		src='emoticons/'
		#config=ConfigObj("emoticons/"+path,encoding='UTF8')
		loaded,config=self.main.loadJabbimExtraConfig("emoticons/"+path,'emoticons/default/smileys.cfg')
		if len(config)==0 or not loaded:
			src=self.main.realHomeDir+'/emoticons/'
			#config=ConfigObj(self.main.realHomeDir+"/emoticons/"+path,encoding='UTF8')
			loaded,config=self.main.loadJabbimExtraConfig(self.main.realHomeDir+"/emoticons/"+path,'emoticons/default/smileys.cfg')
			if not loaded:
				return
		html=""
		values=[]
		for k,v in config['emoticons'].iteritems():
			#self.smileys[k.replace("<","&lt;").replace(">","&gt;")]=v
			if not v in values:
				html+='<img src="'+src+os.path.dirname(path)+'/'+v+'" />'
				values.append(v)
		self.ui.emoticonsPreview.setHtml(html)
		html=""
		html+=self.tr("Name: ")+unicode(config['header']['name'])+"<br/>"
		if config['header'].has_key('license'):
			html+=self.tr("License: ")+unicode(config['header']['license'])+"<br/>"
		self.ui.emoticonsInfo.setText(html)

	def useThemesChanged(self,state):
		if not self.ui.useThemes.isChecked():
			self.main.config['theme']='None'
			self.main.loadTheme()
			self.setStyleSheet("")
		else:
			item=list(self.ui.themes.selectedItems())
			if len(item)!=0:
				item=item[0]
				data=item.data(32)
				file=unicode(data.toString())
				self.reskin(file)

	def pluginSelected(self,item,i):
		if item.parent()==None:
			self.ui.pluginConfiguration.setEnabled(False)
			return
		data=item.data(32,0)
		self.ui.pluginDescription.setText(unicode(item.data(32,1).toString()))
		name=unicode(data.toString())
		plugin=self.plugins[name]
		if plugin.configDialog:
			self.ui.pluginConfiguration.setEnabled(True)
		else:
			self.ui.pluginConfiguration.setEnabled(False)

	def pluginsContextMenu(self,pos):
		# make groupchat bookmarks menu
		item=self.ui.plugins.itemFromIndex(self.ui.plugins.indexAt(pos)) # get selected item
		if item.parent()==None:
			return
		data=item.data(32,0)
		name=unicode(data.toString())
		plugin=self.plugins[name]
		if plugin.configDialog:
			menu=QtGui.QMenu(self.ui.plugins) # make menu
			# Join bookmarked groupchat
			action=menu.addAction(self.tr("Plugin Configuration"))
			action.setData(item.data(32,0))
			action.setObjectName("config")
			menu.connect(menu, QtCore.SIGNAL("triggered ( QAction * )"),self.pluginsContextMenuTriggered)
			# set menu position and show
			menu.move(self.ui.plugins.mapToGlobal(pos))
			menu.show()

	def savePluginConfiguration(self,name,var):
		plugin=self.plugins[name]
		plugin.on_saveConfig()
		for key,value in getVarData(var).iteritems():
			plugin.config[key]=value
			print key,"=",unicode(value)
		plugin.writeConfig()
		if self.main.plugins.has_key(name):
			if self.main.plugins[name]['module']:
				self.main.plugins[name]['module'].config=self.plugins[name].config
				self.main.plugins[name]['module'].on_configChanged()

	def pluginConfigurationClicked(self):
		item=self.ui.plugins.currentItem()
		data=item.data(32,0)
		name=unicode(data.toString())
		plugin=self.plugins[name]
		dialog=pluginConfiguration(self.plugins[name],self.ui.plugins)
		dialog.exec_()
		if self.main.plugins.has_key(name):
			if self.main.plugins[name]['module']:
				self.main.plugins[name]['module'].config=self.plugins[name].config
				self.main.plugins[name]['module'].on_configChanged()

	def pluginsContextMenuTriggered(self,action):
		cmd=action.objectName()
		if cmd=="config":
			data=action.data()
			name=unicode(data.toString())
			plugin=self.plugins[name]
			dialog=pluginConfiguration(self.plugins[name],self.ui.plugins)
			dialog.exec_()
		if self.main.plugins.has_key(name):
			if self.main.plugins[name]['module']:
				self.main.plugins[name]['module'].config=self.plugins[name].config
				self.main.plugins[name]['module'].on_configChanged()



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
			self.main.loadTheme(text,file)

	def themeChanged(self,item,old):
		if item:
			data=item.data(32)
			if data:
				file=unicode(data.toString())
				self.reskin(file)

	def chatskinVariantChanged(self,index):
		path=unicode(self.ui.chatSkin_list.itemData(self.ui.chatSkin_list.currentIndex()).toString())
		v=unicode(self.ui.chatskinVariant.itemData(index).toString())
		self.generateChatskinPreview(path+"/"+v)

	def groupchatskinStyleChanged(self,index):
		self.chatSkin_listChanged(index,"groupchat")
		
	def groupchatskinVariantChanged(self,index):
		path=unicode(self.ui.groupchatskinStyle.itemData(self.ui.groupchatskinStyle.currentIndex()).toString())
		v=unicode(self.ui.groupchatskinVariant.itemData(index).toString())
		self.generateChatskinPreview(path+"/"+v,'groupchat')
	
	def rosterStyleChanged(self,index):
		path=unicode(self.ui.rosterStyle.itemData(index).toString())
		self.ui.rosterVariant.clear()
		variants=[]
		if os.path.isdir("rosterstyles/"+path):
			variants+=os.listdir("rosterstyles/"+path)
		if os.path.isdir(self.main.realHomeDir+"/rosterstyles/"+path):
			variants+=os.listdir(self.main.realHomeDir+"/rosterstyles/"+path)
		v=""
		default=""
		for variant in variants:
			if variant.endswith(".cfg"):
				default=unicode(variant)
				if variant==self.main.config["rosterStyle"].split("/")[1]:
					self.ui.rosterVariant.insertItem(0,variant[:-4],QtCore.QVariant(variant))
					v=unicode(variant)
				else:
					self.ui.rosterVariant.addItem(variant[:-4],QtCore.QVariant(variant))
		if len(v)==0:
			v=default
		self.ui.rosterVariant.setCurrentIndex(0)
	
	def chatSkin_listChanged(self,index,typ='chat'):
		if typ=="chat":
			path=unicode(self.ui.chatSkin_list.itemData(index).toString())
			self.ui.chatskinVariant.clear()
		else:
			path=unicode(self.ui.groupchatskinStyle.itemData(index).toString())
			self.ui.groupchatskinVariant.clear()
		if os.path.exists("chatskins/"+path+"/Variants"):
			variants=os.listdir("chatskins/"+path+"/Variants")
		else:
			variants=os.listdir(self.main.realHomeDir+"/chatskins/"+path+"/Variants")
		v=""
		default=""
		for variant in variants:
			if variant.endswith(".css"):
				default=unicode(variant)
				if typ=="chat":
					if variant==self.main.config["chatTheme"].split("/")[1]:
						self.ui.chatskinVariant.insertItem(0,variant[:-4],QtCore.QVariant(variant))
						v=unicode(variant)
					else:
						self.ui.chatskinVariant.addItem(variant[:-4],QtCore.QVariant(variant))
				else:
					if variant==self.main.config["groupchatTheme"].split("/")[1]:
						self.ui.groupchatskinVariant.insertItem(0,variant[:-4],QtCore.QVariant(variant))
						v=unicode(variant)
					else:
						self.ui.groupchatskinVariant.addItem(variant[:-4],QtCore.QVariant(variant))
		if len(v)==0:
			v=default
		if typ=="chat":
			self.ui.chatskinVariant.setCurrentIndex(0)
		else:
			self.ui.groupchatskinVariant.setCurrentIndex(0)
		self.generateChatskinPreview(path+"/"+v,typ)

	def generateChatskinPreview(self,skin,typ="chat"):
		factory=webkitthemes.webkitThemeFactory(skin,skin,self.main.realHomeDir)
		stylesheet=factory.genChatStyleSheet()
		html="""
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<style type="text/css" media="screen,print"> @import url( "main.css" ); </style>
<style id="mainStyle" type="text/css" media="screen,print"> %s </style>
<script>
function addMessage(index) {
shouldScroll = nearBottom();
//Remove any existing insertion point
insert = document.getElementById("insert");
if(insert) insert.parentNode.removeChild(insert);

var ni = document.getElementById('myDiv');
var numi = document.getElementById('theValue');
var num = (document.getElementById('theValue').value -1)+ 2;
numi.value = num;
var divIdName = "my"+num+"Div";
var newdiv = document.createElement('div');
newdiv.setAttribute("id",divIdName);
newdiv.innerHTML = messageObject.msg(index);
ni.appendChild(newdiv);
if (shouldScroll) scrollToBottom();

}
function insertMessage(index) {
shouldScroll = nearBottom();

                        //Locate the insertion point
                        var insert = document.getElementById("insert");

                        //make new node
                        range = document.createRange();
                        range.selectNode(insert.parentNode);
                        newNode = range.createContextualFragment(messageObject.msg(index));

                        //swap
                        insert.parentNode.replaceChild(newNode,insert);

if (shouldScroll) scrollToBottom();

}
//Auto-scroll to bottom.  Use nearBottom to determine if a scrollToBottom is desired.
function nearBottom() {
		return ( document.body.scrollTop >= ( document.body.offsetHeight - ( window.innerHeight * 1.2 ) ) );
}
function scrollToBottom() {
		document.body.scrollTop = document.body.offsetHeight;
}

function makePreview(){
	addMessage(0);
	insertMessage(1);
	addMessage(2);
	addMessage(3);
	insertMessage(4);
}

</script>
</head>
<body>
<div id="Chat">
<input type="hidden" value="0" id="theValue" />
<div id="myDiv"> </div>
		""" % stylesheet
		

		html+="""
</div>
<a name='bottom'></a>
</body>
</html>
		"""
		
		self.messages=[]
		self.messages.append(factory.genIncomingContent(unicode(self.tr("User")),unicode(self.tr("Message for me")),self.main.now(),os.getcwd()+"/images/32x32/apps/jabbim.png"))
		self.messages.append(factory.genIncomingNextContent(unicode(self.tr("User")),unicode(self.tr("Second message for me")),self.main.now(),os.getcwd()+"/images/32x32/apps/jabbim.png"))
		self.messages.append(factory.genChatStatus(unicode(self.tr("User is now away")),self.main.now()))
		self.messages.append(factory.genOutgoingContent(unicode(self.tr("Me")),unicode(self.tr("Message for user")),self.main.now(),os.getcwd()+"/images/32x32/apps/jabbim.png"))
		self.messages.append(factory.genOutgoingNextContent(unicode(self.tr("Me")),unicode(self.tr("Second message for user")),self.main.now(),os.getcwd()+"/images/32x32/apps/jabbim.png"))

		
		if typ=="chat":
			self.ui.chatskinPreview.page().mainFrame().setHtml(html,QtCore.QUrl("file:///"+factory.chatPath()))
		else:
			self.ui.groupchatskinPreview.page().mainFrame().setHtml(html,QtCore.QUrl("file:///"+factory.chatPath()))

	def chatskinPreviewCleared(self):
		print "cleared"
		self.ui.chatskinPreview.page().mainFrame().addToJavaScriptWindowObject("messageObject",self.chatMessageObject)

	def groupchatskinPreviewCleared(self):
		self.ui.groupchatskinPreview.page().mainFrame().addToJavaScriptWindowObject("messageObject",self.groupchatMessageObject)

	def chatskinPreviewFinished(self,ok,later=False):
		self.chatMessageObject.messages=list(self.messages)
		self.ui.chatskinPreview.page().mainFrame().evaluateJavaScript("makePreview();")

	def groupchatskinPreviewFinished(self,ok,later=False):
		self.groupchatMessageObject.messages=list(self.messages)
		self.ui.groupchatskinPreview.page().mainFrame().evaluateJavaScript("makePreview();")

	def save(self):
		#if not self.justShowed:
			
			#self.main.skin=ConfigObj("skins/"+unicode(self.ui.chatSkin_list.currentText()),encoding='UTF8')
			#if not self.main.skin.has_key("spaces_between_lines"):
				#self.main.skin["spaces_between_lines"]='0'

		for name,var in self.showedPlugins.iteritems():
			if var:
				self.savePluginConfiguration(name,var)

		for cfg in self.var:
			for key,value in getVarData(cfg).iteritems():
				if key=='passwd':
					self.main.config[key]=rot13.scramble(unicode(value))
				else:
					self.main.config[key]=value
					print key,"=",unicode(value)
		if not self.justShowed:
			self.main.config['chatSkin']=unicode(self.ui.chatSkin_list.itemData(self.ui.chatSkin_list.currentIndex()).toString())
			if self.main.config['rosterStyle']!=unicode(self.ui.rosterStyle.itemData(self.ui.rosterStyle.currentIndex()).toString())+"/"+unicode(self.ui.rosterVariant.itemData(self.ui.rosterVariant.currentIndex()).toString()):
				self.main.config['rosterStyle']=unicode(self.ui.rosterStyle.itemData(self.ui.rosterStyle.currentIndex()).toString())+"/"+unicode(self.ui.rosterVariant.itemData(self.ui.rosterVariant.currentIndex()).toString())
				self.main.loadRosterStyle()
			if self.main.config['chatTheme']!=unicode(self.ui.chatSkin_list.itemData(self.ui.chatSkin_list.currentIndex()).toString())+"/"+unicode(self.ui.chatskinVariant.itemData(self.ui.chatskinVariant.currentIndex()).toString()) or self.main.config['groupchatTheme']!=unicode(self.ui.groupchatskinStyle.itemData(self.ui.groupchatskinStyle.currentIndex()).toString())+"/"+unicode(self.ui.groupchatskinVariant.itemData(self.ui.groupchatskinVariant.currentIndex()).toString()):
				self.main.config['chatTheme']=unicode(self.ui.chatSkin_list.itemData(self.ui.chatSkin_list.currentIndex()).toString())+"/"+unicode(self.ui.chatskinVariant.itemData(self.ui.chatskinVariant.currentIndex()).toString())
				self.main.config['groupchatTheme']=unicode(self.ui.groupchatskinStyle.itemData(self.ui.groupchatskinStyle.currentIndex()).toString())+"/"+unicode(self.ui.groupchatskinVariant.itemData(self.ui.groupchatskinVariant.currentIndex()).toString())
				self.main.loadSkin()
			if self.main.config['emoticons']!=unicode(self.ui.emoticonsList.itemData(self.ui.emoticonsList.currentIndex()).toString()):
				self.main.config['emoticons']=unicode(self.ui.emoticonsList.itemData(self.ui.emoticonsList.currentIndex()).toString())
				self.main.emoticonsWidget.reinit()
			#for i in range(self.main.chat.ui.chatTab.count()):
				#w=self.main.chat.ui.chatTab.widget(i)
				#w.chat.loadSmileys()

		#data=item.data(32)
		#file=unicode(data.toString())
		#self.reskin(file)
		
		#self.main.config['jid']=jid
		#self.main.config['resource']=''+resource+''
		#self.main.config['priority']=self.ui.connection_priority.text()
		if not self.justShowed:
			if not self.ui.useThemes.isChecked():
				self.main.config['theme']="None"
				self.main.loadTheme()
			else:
				self.main.config['theme']=unicode(self.ui.themes.currentItem().data(32).toString())
		#if self.main.config['rosterMode']=="compact":
		#	import compactrosterstyle
		#	self.main.ui.roster.setRosterStyle(compactrosterstyle.rosterStyle)
		#elif self.main.config['rosterMode']=='normal':
		#	import defaultrosterstyle
		#	self.main.ui.roster.setRosterStyle(defaultrosterstyle.rosterStyle)
		if self.main.config['rosterScrollBar']=="True":
			self.main.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
			QtCore.QObject.disconnect(self.main.scroll.verticalScrollBar(),QtCore.SIGNAL("valueChanged ( int )"),self.main.ui.roster.sliderChanged)
		else:
			self.main.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
			QtCore.QObject.connect(self.main.scroll.verticalScrollBar(),QtCore.SIGNAL("valueChanged ( int )"),self.main.ui.roster.sliderChanged)
		self.main.ui.roster.setSize()
		self.main.ui.roster.repaint()
		load=False
		for i in range(int(self.ui.plugins.topLevelItemCount())):
			it=self.ui.plugins.topLevelItem(i)
			for child in range(int(it.childCount())):
				item=it.child(child)
				data=item.data(32,0)
				plugin=unicode(data.toString())
				#widget=self.ui.plugins.itemWidget(item,0)
				if item.checkState(0)==QtCore.Qt.Checked and not plugin in self.loadedPlugins:
					if self.main.client:
						self.main.loadPlugin(plugin)
					self.main.config['plugins'].append(plugin)
					self.loadedPlugins=self.main.config['plugins']
					load=True
				elif item.checkState(0)==QtCore.Qt.Unchecked and plugin in self.loadedPlugins:
					if self.main.client:
						self.main.unloadPlugin(plugin)
					self.main.config['plugins'].remove(plugin)
					load=True
		self.main.config.write()
		self.reloadPlugins()

	def accept(self):
		self.save()
		self.done(1)

	def reject(self):
		if self.main.config['theme']!=self.currentTheme:
			self.main.config['theme']=self.currentTheme
			if self.currentTheme!="None":
				self.reskin(self.currentTheme)
			else:
				self.main.loadTheme()
		item=self.ui.listWidget.currentItem()
		print item
		if item:
			name=unicode(item.data(32).toString())
			print name,self.showedPlugins
			if self.showedPlugins.has_key(name):
				self.plugins[name].on_endPreferences()
		return QtGui.QDialog.reject(self)

class editBookmark(QtGui.QDialog):
	def __init__(self,main,room,server,name,nickname,password,autojoin,parent,edit=True):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.parent=parent
		self.room=room
		self.server=server
		self.jid="%s@%s" % (room,server)
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
			self.main.client.bookmarks['conference'][self.jid]=pyxl.client.Bookmark(name, 'conference', room+"@"+server, autojoin, nickname, password)
			#self.done(1)
			edited=True
		else:
			if self.edit==True:
				del self.main.client.bookmarks['conference'][self.jid]
			self.main.client.bookmarks['conference'][self.jid]=pyxl.client.Bookmark(name, 'conference', room+"@"+server, autojoin, nickname, password)
			edited=True
		if edited:
			#self.main.bookmarks=self.bookmarks
			self.main.client.setBookmarks()
			self.main.buildBookmarks()

			self.done(1)
