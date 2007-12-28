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
from pref import jabbim,connection,chat,roster
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

class pluginConfiguration(QtGui.QDialog):
	def __init__(self,plugin,parent):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.plugin=plugin
		self.setWindowTitle(plugin.name+" preferences")

		self.plugin.on_showPreferences(self)

		layout=QtGui.QGridLayout(self)
		self.var,row=makePreferences(self.plugin.config,self,layout,self.plugin.configDialog.config)
		#self.widgets={}
		
		##l=self.layout()
		
		#layout=QtGui.QVBoxLayout(self)
		#for key,item in plugin.config.iteritems():
			#if item['type']=="boolean":
				#widget=QtGui.QCheckBox(item['description'],self)
				#if len(item['value'])==0:
					#if item['default']=='True':
						#widget.setChecked(True)
				#else:
					#if item['value']=='True':
						#widget.setChecked(True)
				#layout.addWidget(widget)
				#self.widgets[key]=widget
			#elif item['type']=="text":
				#label=QtGui.QLabel(item['description'],self)
				#if len(item['value'])==0:
					#widget=QtGui.QLineEdit(item['default'],self)
				#else:
					#widget=QtGui.QLineEdit(item['value'],self)
				#layout2=QtGui.QHBoxLayout()
				#layout2.addWidget(label)
				#layout2.addWidget(widget)
				#layout.addLayout(layout2)
				#self.widgets[key]=widget
				
		layout2=QtGui.QHBoxLayout()
		close=QtGui.QPushButton("Close",self)
		save=QtGui.QPushButton("Save",self)
		layout2.addStretch()
		layout2.addWidget(close)
		layout2.addWidget(save)
		
		QtCore.QObject.connect(save, QtCore.SIGNAL("clicked()"),self.accept)
		QtCore.QObject.connect(close, QtCore.SIGNAL("clicked()"),self.reject)
		
		layout.addLayout(layout2,row,0,1,2)
	
	def accept(self):
		#for key, widget in self.widgets.iteritems():
			#item=self.plugin.config[key]
			#if item['type']=="boolean":
				#self.plugin.config[key]['value']=str(widget.isChecked())
			#elif item['type']=="text":
				#print unicode(widget.text())
				#self.plugin.config[key]['value']=unicode(widget.text())

		self.plugin.on_saveConfig()
		for key,value in getVarData(self.var).iteritems():
			self.plugin.config[key]=unicode(value)
			print key,"=",unicode(value)
		self.plugin.writeConfig()
		self.done(1)

	def reject(self):
		self.plugin.on_endPreferences()
		self.close()

def getVarData(var):
	ret={}
	for key,value in var.iteritems():
		typ=value['type']
		widget=value['widget']
		if typ=="text-single" or typ=="text-private":
			ret[key]=unicode(widget.text())
		elif typ=="time-interval":
			ret[key]=unicode(widget.time().toString("H:m:s"))
		elif typ=="text-multi":
			text=unicode(widget.toPlainText())
			ret[key]=unicode(text)
		elif typ=="boolean":
			if widget.isChecked():
				text="True"
			else:
				text="False"
			ret[key]=unicode(text)
		elif typ=="list-single":
			ret[key]=unicode(widget.itemData(widget.currentIndex()).toString())
		elif typ=="number-spin":
			ret[key]=unicode(widget.value())
		elif typ=="boolean-radio":
			ret[key]=unicode(widget.checkedButton().data)
	return ret

def makePreferences(main,parent,layout,form,row=1):
	var={}
	boxes={}
	getBox=False
	par=parent
	lay=layout
	keys=form.keys()
	if "__sort__" in keys:
		keys=form['__sort__']
	for key in keys:
		x=form[key]
		val=x['value']
		if x.has_key('groupbox'):
			if not boxes.has_key(x['groupbox']):
				boxes[x['groupbox']]=[QtGui.QGroupBox(x['groupbox'],parent)]
				boxes[x['groupbox']].append(QtGui.QGridLayout(boxes[x['groupbox']][0]))
				layout.addWidget(boxes[x['groupbox']][0],row,0,1,2)
				row+=1
				oldrow=int(row)
			par=boxes[x['groupbox']][0]
			lay=boxes[x['groupbox']][1]
			getBox=True
		elif getBox:
			getBox=False
			row=int(oldrow)
			par=parent
			lay=layout
		if main.has_key(key):
			val=main[key]
			if key=="passwd":
				val=rot13.scramble(val)
		if x['type']=="text-single":
			try:
				label=QtGui.QLabel(x['label'],par)
			except KeyError:
				label=None
			lay.addWidget(label,row,0)
			widget=QtGui.QLineEdit(par)
			widget.setText(unicode(val))
			lay.addWidget(widget,row,1)
			var[key]={'widget':widget,'type':x['type']}
			row+=1
			#for d in x.elements():
				#if d.name == "desc":
					#widget.setToolTip(unicode(d))
		elif x['type']=="time-interval":
			try:
				label=QtGui.QLabel(x['label'],par)
			except KeyError:
				label=None
			lay.addWidget(label,row,0)
			widget=QtGui.QTimeEdit(par)
			d=val.split(":")
			t=QtCore.QTime(int(d[0]),int(d[1]),int(d[2]))
			widget.setTime(t)
			lay.addWidget(widget,row,1)
			var[key]={'widget':widget,'type':x['type']}
			row+=1
		elif x['type']=="number-spin":
			try:
				label=QtGui.QLabel(x['label'],par)
			except KeyError:
				label=None
			lay.addWidget(label,row,0)
			widget=QtGui.QSpinBox(par)
			widget.setValue(int(val))
			lay.addWidget(widget,row,1)
			var[key]={'widget':widget,'type':x['type']}
			row+=1
		elif x['type']=="fixed":
			label=QtGui.QLabel(par)
			label.setWordWrap(True)
			label.setText(unicode(val))
			lay.addWidget(label,row,0,1,2)
			#for d in x.elements():
				#if d.name == "desc":
					#widget.setToolTip(unicode(d))
			row+=1
		elif x['type']=="text-multi":
			try:
				label=QtGui.QLabel(x['label'],par)
			except KeyError:
				label=None
			lay.addWidget(label,row,0)
			widget=QtGui.QTextEdit(par)
			#text=""
			#for child in x.elements():
				#if child.name == 'value':
					#text+=unicode(child)+"\n"
			widget.setText(unicode(val))
			lay.addWidget(widget,row,1)
			var[key]={'widget':widget,'type':x['type']}
			#for d in x.elements():
				#if d.name == "desc":
					#widget.setToolTip(unicode(d))
			row+=1
		elif x['type']=="boolean":
			try:
					ltext=x['label']
			except KeyError:
					ltext=""
			widget=QtGui.QCheckBox(ltext,par)
			#for child in x.elements():
				#if child.name == 'value':
			if unicode(val)=="0" or unicode(val).lower()=="false":
				widget.setChecked(False)
			elif unicode(val)=="1" or unicode(val).lower()=="true":
				widget.setChecked(True)
			if x.has_key('column'):
				if x['column']=='right':
					lay.addWidget(widget,row,1,1,1)
				else:
					lay.addWidget(widget,row,0,1,2)
			else:
				lay.addWidget(widget,row,0,1,2)
			var[key]={'widget':widget,'type':x['type']}
			#for d in x.elements():
				#if d.name == "desc":
					#widget.setToolTip(unicode(d))
			row+=1
		elif x['type']=="boolean-radio":
			group=QtGui.QButtonGroup()
			for data,lab in x['options'].iteritems():
				widget=QtGui.QRadioButton(lab,par)
				widget.data=unicode(data)
				if unicode(val)==unicode(data):
					widget.setChecked(True)
				else:
					widget.setChecked(False)
				if x.has_key('column'):
					if x['column']=='right':
						lay.addWidget(widget,row,1,1,1)
					else:
						lay.addWidget(widget,row,0,1,2)
				else:
					lay.addWidget(widget,row,0,1,2)
				group.addButton(widget)
				row+=1
			var[key]={'widget':group,'type':x['type']}
		elif x['type']=="text-private":
			try:
				label=QtGui.QLabel(x['label'],par)
			except KeyError:
				label=None
			lay.addWidget(label,row,0)
			widget=QtGui.QLineEdit(par)
			widget.setEchoMode(QtGui.QLineEdit.Password)
			#for child in x.elements():
				#if child.name == 'value':
			widget.setText(unicode(val))
			lay.addWidget(widget,row,1)
			var[key]={'widget':widget,'type':x['type']}
			#for d in x.elements():
				#if d.name == "desc":
					#widget.setToolTip(unicode(d))
			row+=1
		elif x['type']=="list-single":
			# TODO
			##<field var='userlist' type='list-single' label='Userlist on GG server'><value>get</value><option label='ignore'><value>ignore</value></option><option label='retrieve'><value>get</value></option></field>
			#try:
				#label=QtGui.QLabel(x['label'],parent)
			#except KeyError:
				#label=None
			#layout.addWidget(label,row,0)
			#widget=QtGui.QComboBox(parent)
			#default=""
			#for child in x.elements():
				#if child.name == 'value':
					#default=unicode(child)
				#elif child.name=="option":
					#for ch in child.elements():
						#if ch.name=="value":
							#if unicode(ch)==default:
								#widget.insertItem(0,unicode(child['label']),QtCore.QVariant(unicode(ch)))
							#else:
								#widget.addItem(child['label'], QtCore.QVariant(unicode(ch)))
			#widget.setCurrentIndex(0)
			#layout.addWidget(widget,row,1)
			#var[key]={'widget':widget,'type':x['type']}
			#for d in x.elements():
				#if d.name == "desc":
					#widget.setToolTip(unicode(d))
			row+=1
	return var,row


class preferencesWindow(QtGui.QDialog):
	def __init__(self,main,parent=None,page=0):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.main=main
		self.setModal(False)
		self.ui=Ui_preferences()
		self.ui.setupUi(self)
		self.ui.stackedWidget.setCurrentIndex(page)

		self.var=[]

		if self.main.client:
			self.ui.profile.hide()
		else:
			self.ui.profile.setText("<b>"+self.tr("Profile:")+"</b> "+unicode(self.main.config['jid']))
			self.ui.profile.show()

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


		# Themes
		skins=os.listdir("themes/")
		if self.main.config['theme']=="None":
			self.ui.useThemes.setChecked(False)
			QtCore.QObject.connect(self.ui.useThemes,QtCore.SIGNAL("stateChanged ( int )"),self.useThemesChanged)
		self.currentTheme=self.main.config['theme']
		for skin in skins:
			if os.path.isdir("themes/"+skin) and os.path.exists("themes/"+skin+"/style.css"):
				preview=QtGui.QIcon('themes/'+skin+"/preview.png")
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
					text = self.tr("Name: %1\nAuthor: %2\nVersion: %3") \
											.arg(conf['name']) \
											.arg(conf['author']) \
											.arg(conf['version'])
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

		# Plugins
		#self.ui.plugins.header().hide()
		QtCore.QObject.connect(self.ui.applyButton, QtCore.SIGNAL("clicked()"),self.save)
		QtCore.QObject.connect(self.ui.pluginConfiguration, QtCore.SIGNAL("clicked()"),self.pluginConfigurationClicked)
		QtCore.QObject.connect(self.ui.plugins, QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.pluginsContextMenu)
		QtCore.QObject.connect(self.ui.plugins, QtCore.SIGNAL("itemClicked ( QTreeWidgetItem *, int)"),self.pluginSelected)

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

			try: 
				plug = load_source(plugin, path, f).Plugin(False,self.main.homeDir)
			except Exception, ex:
				log.msg(plugin+': CHYBA PRI NAHRAVANI => SPATNA SYNTAXE V PLUGINU!')
				message = unicode(traceback.format_exc())
				print message
				f.close()
				continue
			
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
		data=item.data(32,0)
		name=unicode(data.toString())
		plugin=self.plugins[name]
		if plugin.configDialog:
			self.ui.pluginConfiguration.setEnabled(True)
		else:
			self.ui.pluginConfiguration.setEnabled(False)

	def pluginsContextMenu(self,pos):
		# make groupchat bookmarks menu
		item=self.ui.plugins.itemFromIndex(self.ui.plugins.indexAt(pos)) # get selected item
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

	def pluginConfigurationClicked(self):
		item=self.ui.plugins.currentItem()
		data=item.data(32,0)
		name=unicode(data.toString())
		plugin=self.plugins[name]
		dialog=pluginConfiguration(self.plugins[name],self.ui.plugins)
		dialog.exec_()
		if self.main.plugins.has_key(name):
			self.main.plugins[name].config=self.plugins[name].config
			self.main.plugins[name].on_configChanged()

	def pluginsContextMenuTriggered(self,action):
		cmd=action.objectName()
		if cmd=="config":
			data=action.data()
			name=unicode(data.toString())
			plugin=self.plugins[name]
			dialog=pluginConfiguration(self.plugins[name],self.ui.plugins)
			dialog.exec_()
		if self.main.plugins.has_key(name):
			self.main.plugins[name].config=self.plugins[name].config
			self.main.plugins[name].on_configChanged()



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
		self.chatSkinPreviewtextEditWrite(testConfig["message_history"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("This is test message send in past."))).replace('[background]',testConfig['color1'][0]).replace('[foreground]',testConfig['color1'][1]))
		self.chatSkinPreviewtextEditWrite(testConfig["my_message_history"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("Me"))).replace("[message]",unicode(self.tr("This is my test message send in past."))))
		self.chatSkinPreviewtextEditWrite(testConfig["message_for_me_history"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("Me"))+", "+unicode(self.tr("this is message contains my name send in past."))))
		self.chatSkinPreviewtextEditWrite(testConfig["message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("This is test message."))).replace('[background]',testConfig['color1'][0]).replace('[foreground]',testConfig['color1'][1]))
		self.chatSkinPreviewtextEditWrite(testConfig["my_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("Me"))).replace("[message]",unicode(self.tr("This is my test message."))))
		self.chatSkinPreviewtextEditWrite(testConfig["message_for_me"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("Me"))+", "+unicode(self.tr("this is message contains my name."))))
		self.chatSkinPreviewtextEditWrite(testConfig["status_message"].replace("[time]",self.main.now()).replace("[message]",unicode(self.tr("User has set the subject to: Subject"))))


	def save(self):
		self.main.skin=ConfigObj("skins/"+unicode(self.ui.chatSkin_list.currentText()),encoding='UTF8')
		if not self.main.skin.has_key("spaces_between_lines"):
			self.main.skin["spaces_between_lines"]='0'

		for cfg in self.var:
			for key,value in getVarData(cfg).iteritems():
				if key=='passwd':
					self.main.config[key]=rot13.scramble(unicode(value))
				else:
					self.main.config[key]=unicode(value)
					print key,"=",unicode(value)

		self.main.config['chat_skin']=unicode(self.ui.chatSkin_list.currentText())
		
		#data=item.data(32)
		#file=unicode(data.toString())
		#self.reskin(file)
		
		#self.main.config['jid']=jid
		#self.main.config['resource']=''+resource+''
		#self.main.config['priority']=self.ui.connection_priority.text()
		if not self.ui.useThemes.isChecked():
			self.main.config['theme']="None"
			self.main.loadTheme()
		else:
			self.main.config['theme']=unicode(self.ui.themes.currentItem().data(32).toString())
		if self.main.config['rosterMode']=="compact":
			#self.main.config['rosterMode']="compact"
			self.main.ui.roster.userHeight=22
			self.main.ui.roster.groupHeight=22
			self.main.ui.roster.compact=True
			self.main.ui.roster.reshow=True
			self.main.ui.roster.statusLabel.hide()
		elif self.main.config['rosterMode']=='normal':
			#self.main.config['rosterMode']="normal"
			self.main.ui.roster.userHeight=32
			self.main.ui.roster.groupHeight=32
			self.main.ui.roster.compact=False
			self.main.ui.roster.reshow=True
			self.main.ui.roster.statusLabel.hide()
		self.main.ui.roster.setSize()
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

	def accept(self):
		self.save()
		self.done(1)

	def reject(self):
		self.main.config['theme']=self.currentTheme
		if self.currentTheme!="None":
			self.reskin(self.currentTheme)
		else:
			self.main.loadTheme()
		self.close()
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
