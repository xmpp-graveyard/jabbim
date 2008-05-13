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
from twisted.words.protocols.jabber import jid as jidT


class pluginConfiguration(QtGui.QDialog):
	def __init__(self,plugin,parent):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.plugin=plugin
		self.setWindowTitle(plugin.name+" preferences")

		self.plugin.on_showPreferences(self)

		layout=QtGui.QGridLayout(self)
		self.var,row=makePreferences(self.plugin.config,self,layout,self.plugin.configDialog.config)

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
		self.plugin.on_saveConfig()
		for key,value in getVarData(self.var).iteritems():
			self.plugin.config[key]=value
			print key,"=",unicode(value)
		self.plugin.writeConfig()
		self.done(1)

	def reject(self):
		self.plugin.on_endPreferences()
		#self.close()
		return QtGui.QDialog.reject(self)

def updateVarData(var,main):
	for key,value in var.iteritems():
		if main.has_key(key):
			val=main[key]
			if key=="passwd":
				val=rot13.scramble(val)
		else:
			continue
		
		typ=value['type']
		widget=value['widget']
		if (typ=="text-single" or typ=="text-private") or typ=='directory':
			widget.setText(val)
		elif typ=="time-interval":
			d=val.split(":")
			t=QtCore.QTime(int(d[0]),int(d[1]),int(d[2]))
			widget.setTime(t)
		elif typ=="text-multi":
			widget.setText(unicode(val))
		elif typ=="boolean":
			if unicode(val)=="0" or unicode(val).lower()=="false":
				widget.setChecked(False)
			elif unicode(val)=="1" or unicode(val).lower()=="true":
				widget.setChecked(True)
		elif typ=="list-single":
			if widget.findData(QtCore.QVariant(unicode(val)))!=None:
				widget.setCurrentIndex(widget.findData(QtCore.QVariant(unicode(val))))
		elif typ=="number-spin":
			widget.setValue(int(val))
		elif typ=="boolean-radio":
			data=widget.checkedButton().data
			if unicode(val)==unicode(data):
				widget.checkedButton().setChecked(True)
			else:
				widget.checkedButton().setChecked(False)
		elif typ=="jid-list":
			widget.jids.clear()
			if isinstance(val,list):
				for jid in val:
					QtGui.QListWidgetItem(unicode(jid),widget.jids)
		elif typ=="custom":
			widget.setWidgetValue(val)

def getVarData(var):
	ret={}
	for key,value in var.iteritems():
		typ=value['type']
		widget=value['widget']
		if (typ=="text-single" or typ=="text-private") or typ=='directory':
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
		elif typ=="jid-list":
			jids=[]
			for i in range(widget.jids.count()):
				item=widget.jids.item(i)
				jids.append(unicode(item.text()))
			ret[key]=jids
		elif typ=="custom":
			ret[key]=widget.getWidgetValue()
	return ret

class directoryWidget(QtGui.QLineEdit):
	def getDirectory(self):
		directory=unicode(QtGui.QFileDialog.getExistingDirectory(self,self.tr("Choose directory"),self.text(),QtGui.QFileDialog.ShowDirsOnly| QtGui.QFileDialog.DontResolveSymlinks))
		if len(directory)!=0:
			self.setText(directory)

class jidListWidget(QtGui.QWidget):
	"""
	Widget for displaying jid-list type in configAPI
	"""
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent)
		# layout
		layout=QtGui.QGridLayout(self)
		self.jids=QtGui.QListWidget(self)
		add=QtGui.QPushButton(self.tr("Add"),self)
		remove=QtGui.QPushButton(self.tr("Remove"),self)
		layout.addWidget(self.jids,0,0,1,2)
		layout.addWidget(add,1,0,1,1)
		layout.addWidget(remove,1,1,1,1)
		# signals
		QtCore.QObject.connect(add,QtCore.SIGNAL("clicked()"),self.addJid)
		QtCore.QObject.connect(remove,QtCore.SIGNAL("clicked()"),self.removeJid)
	
	def removeJid(self):
		items=self.jids.selectedItems()
		if len(items)==0:
			return
		# TODO => allow to remove more items
		self.jids.takeItem(self.jids.row(items[0]))
		del items[0]
		
	def addJid(self):
		jid=""
		while 1:
			jid,b=QtGui.QInputDialog.getText(self,self.tr("Add Jabber ID"),self.tr("Enter Jabber ID:"), QtGui.QLineEdit.Normal, jid)
			jid=unicode(jid)
			if b==True and len(jid)!=0:
				try:
					isJid=jidT.JID(jid)
				except:
					isJid=None
				if isJid:
					QtGui.QListWidgetItem(jid,self.jids)
					break
			else:
				break

def makePreferences(main,parent,layout,form,row=1):
	var={}
	boxes={}
	tabs={}
	getBox=False
	getTab=False
	par=parent
	lay=layout
	keys=form.keys()
	if "__sort__" in keys:
		keys=form['__sort__']
	usingTabs=False
	for key in keys:
		if form[key].has_key("tab"):
			if not usingTabs:
				usingTabs=True
				tabWidget=QtGui.QTabWidget(parent)
				layout.addWidget(tabWidget,row,0,1,2)
				row+=1
			if not tabs.has_key(form[key]['tab']):
				tabs[form[key]['tab']]=[QtGui.QWidget(tabWidget)]
				tabs[form[key]['tab']].append(QtGui.QGridLayout(tabs[form[key]['tab']][0]))
				tabs[form[key]['tab']].append(0)
				tabWidget.addTab(tabs[form[key]['tab']][0],form[key]['tab'])
	row_=int(row)
	for key in keys:
		x=form[key]
		val=x['value']
		if x.has_key('tab'):
			par=tabs[x['tab']][0]
			lay=tabs[x['tab']][1]
			getTab=True
			row=tabs[x['tab']][2]
			tabs[x['tab']][2]+=1
		if x.has_key('groupbox'):
			if not boxes.has_key(x['groupbox']):
				if x.has_key('tab'):
					boxes[x['groupbox']]=[QtGui.QGroupBox(x['groupbox'],tabs[x['tab']][0])]
					boxes[x['groupbox']].append(QtGui.QGridLayout(boxes[x['groupbox']][0]))
					tabs[x['tab']][1].addWidget(boxes[x['groupbox']][0],row,0,1,2)
				else:
					boxes[x['groupbox']]=[QtGui.QGroupBox(x['groupbox'],parent)]
					boxes[x['groupbox']].append(QtGui.QGridLayout(boxes[x['groupbox']][0]))
					layout.addWidget(boxes[x['groupbox']][0],row,0,1,2)
					row+=1
				boxes[x['groupbox']].append(0)
				oldrow=int(row)
			boxes[x['groupbox']][2]+=1
			row=boxes[x['groupbox']][2]
			par=boxes[x['groupbox']][0]
			lay=boxes[x['groupbox']][1]
			getBox=True
		elif getBox:
			getBox=False
			if not usingTabs:
				row=int(oldrow)
				par=parent
				lay=layout
			#if not tabs.has_key(x['tab']):
				#tabs[x['tab']]=[QtGui.QGroupBox(x['groupbox'],parent)]
		if main.has_key(key):
			val=main[key]
			if key=="passwd":
				val=rot13.scramble(val)
		if x['type']=="text-single":
			try:
				label=QtGui.QLabel(x['label'],par)
				label.setOpenExternalLinks(True)
				label.setWordWrap(True)
				label.setTextFormat(QtCore.Qt.RichText)
				policy=label.sizePolicy()
				policy.setHeightForWidth(True)
				policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
				label.setSizePolicy(policy)
			except KeyError:
				label=None
			lay.addWidget(label,row,0)
			widget=QtGui.QLineEdit(par)
			widget.setText(unicode(val))
			lay.addWidget(widget,row,1)
			var[key]={'widget':widget,'type':x['type']}
			row+=1
		elif x['type']=="custom":
			try:
				label=QtGui.QLabel(x['label'],par)
				label.setOpenExternalLinks(True)
				label.setWordWrap(True)
				label.setTextFormat(QtCore.Qt.RichText)
				policy=label.sizePolicy()
				policy.setHeightForWidth(True)
				policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
				label.setSizePolicy(policy)
			except KeyError:
				label=None
			lay.addWidget(label,row,0)
			
			widget=x['widget'](par)
			widget.setWidgetValue(val)
			if not label:
				lay.addWidget(widget,row,0,1,2)
			else:
				lay.addWidget(widget,row,1)
			var[key]={'widget':widget,'type':x['type']}
			row+=1
		elif x['type']=="directory":
			try:
				label=QtGui.QLabel(x['label'],par)
				label.setOpenExternalLinks(True)
				label.setWordWrap(True)
				label.setTextFormat(QtCore.Qt.RichText)
				policy=label.sizePolicy()
				policy.setHeightForWidth(True)
				policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
				label.setSizePolicy(policy)
			except KeyError:
				label=None
			lay.addWidget(label,row,0)
			widget=directoryWidget(par)
			widget.setText(unicode(val))
			chooser=QtGui.QPushButton("...")
			QtCore.QObject.connect(chooser,QtCore.SIGNAL("clicked()"),widget.getDirectory)
			l_=QtGui.QHBoxLayout()
			l_.addWidget(widget)
			l_.addWidget(chooser)
			lay.addLayout(l_,row,1)
			var[key]={'widget':widget,'type':x['type'],'widgets':[chooser]}
			row+=1
		elif x['type']=="jid-list":
			try:
				label=QtGui.QLabel(x['label'],par)
				label.setOpenExternalLinks(True)
				label.setWordWrap(True)
				label.setTextFormat(QtCore.Qt.RichText)
				policy=label.sizePolicy()
				policy.setHeightForWidth(True)
				policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
				label.setSizePolicy(policy)
			except KeyError:
				label=None
			lay.addWidget(label,row,0)
			widget=jidListWidget(par)
			print "variables lol:",type(val)
			if isinstance(val,list):
				for jid in val:
					QtGui.QListWidgetItem(unicode(jid),widget.jids)
			lay.addWidget(widget,row,1)
			var[key]={'widget':widget,'type':x['type']}
			row+=1
		elif x['type']=="time-interval":
			try:
				label=QtGui.QLabel(x['label'],par)
				label.setOpenExternalLinks(True)
				label.setWordWrap(True)
				label.setTextFormat(QtCore.Qt.RichText)
				policy=label.sizePolicy()
				policy.setHeightForWidth(True)
				policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
				label.setSizePolicy(policy)
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
				label.setOpenExternalLinks(True)
				label.setWordWrap(True)
				label.setTextFormat(QtCore.Qt.RichText)
				policy=label.sizePolicy()
				policy.setHeightForWidth(True)
				policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
				label.setSizePolicy(policy)
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
			label.setOpenExternalLinks(True)
			label.setWordWrap(True)
			label.setTextFormat(QtCore.Qt.RichText)
			policy=label.sizePolicy()
			policy.setHeightForWidth(True)
			policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
			label.setSizePolicy(policy)
			label.setText(unicode(val))
			lay.addWidget(label,row,0,1,2)
			#for d in x.elements():
				#if d.name == "desc":
					#widget.setToolTip(unicode(d))
			row+=1
		elif x['type']=="text-multi":
			try:
				label=QtGui.QLabel(x['label'],par)
				label.setOpenExternalLinks(True)
				label.setWordWrap(True)
				label.setTextFormat(QtCore.Qt.RichText)
				policy=label.sizePolicy()
				policy.setHeightForWidth(True)
				policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
				label.setSizePolicy(policy)
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
				label.setOpenExternalLinks(True)
				label.setWordWrap(True)
				label.setTextFormat(QtCore.Qt.RichText)
				policy=label.sizePolicy()
				policy.setHeightForWidth(True)
				policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
				label.setSizePolicy(policy)
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
			try:
				label=QtGui.QLabel(x['label'],par)
				label.setOpenExternalLinks(True)
				label.setWordWrap(True)
				label.setTextFormat(QtCore.Qt.RichText)
				policy=label.sizePolicy()
				policy.setHeightForWidth(True)
				policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
				label.setSizePolicy(policy)
			except KeyError:
				label=None
			lay.addWidget(label,row,0)
			widget=QtGui.QComboBox(par)
			for iKey,iValue in x['items'].iteritems():
				widget.addItem(unicode(iKey),QtCore.QVariant(unicode(iValue)))
			if widget.findData(QtCore.QVariant(unicode(val)))!=None:
				widget.setCurrentIndex(widget.findData(QtCore.QVariant(unicode(val))))
			lay.addWidget(widget,row,1)
			var[key]={'widget':widget,'type':x['type']}
			row+=1
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
		if var.has_key(key):
			if x.has_key("tooltip"):
				var[key]['widget'].setToolTip(unicode(x['tooltip']))
		
	for key in keys:
		x=form[key]
		val=x['value']
		if main.has_key(key):
			val=main[key]
			if key=="passwd":
				val=rot13.scramble(val)
		if x.has_key("disabled"):
			var[key]['widget'].setDisabled(True)
		if x['type']=="boolean":
			if x.has_key("enable"):
				for w in x['enable']:
					widgets=[var[w]['widget']]
					if var[w].has_key("widgets"):
						widgets+=var[w]['widgets']
					for widget in widgets:
						QtCore.QObject.connect(var[key]['widget'],QtCore.SIGNAL("toggled (bool)"),widget.setEnabled)
						if unicode(val)=="0" or unicode(val).lower()=="false":
							widget.setEnabled(False)
						elif unicode(val)=="1" or unicode(val).lower()=="true":
							widget.setEnabled(True)
			if x.has_key("disable"):
				for w in x['disable']:
					widgets=[var[w]['widget']]
					if var[w].has_key("widgets"):
						widgets+=var[w]['widgets']
					for widget in widgets:
						QtCore.QObject.connect(var[key]['widget'],QtCore.SIGNAL("toggled (bool)"),widget.setDisabled)
						if unicode(val)=="0" or unicode(val).lower()=="false":
							widget.setDisabled(False)
						elif unicode(val)=="1" or unicode(val).lower()=="true":
							widget.setDisabled(True)
			if x.has_key("show"):
				for w in x['show']:
					widgets=[var[w]['widget']]
					if var[w].has_key("widgets"):
						widgets+=var[w]['widgets']
					for widget in widgets:
						QtCore.QObject.connect(var[key]['widget'],QtCore.SIGNAL("toggled (bool)"),widget.setVisible)
						if unicode(val)=="0" or unicode(val).lower()=="false":
							widget.setVisible(False)
						elif unicode(val)=="1" or unicode(val).lower()=="true":
							widget.setVisible(True)
			if x.has_key("hide"):
				for w in x['hide']:
					widgets=[var[w]['widget']]
					if var[w].has_key("widgets"):
						widgets+=var[w]['widgets']
					for widget in widgets:
						QtCore.QObject.connect(var[key]['widget'],QtCore.SIGNAL("toggled (bool)"),widget.setHidden)
						if unicode(val)=="0" or unicode(val).lower()=="false":
							widget.setHidden(False)
						elif unicode(val)=="1" or unicode(val).lower()=="true":
							widget.setHidden(True)


	if usingTabs:
		return var,row_
	else:
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
		QtCore.QObject.connect(self.ui.chatSkin_list, QtCore.SIGNAL("activated ( int )"),self.chatSkin_listChanged)

		QtCore.QObject.connect(self.ui.useThemes,QtCore.SIGNAL("stateChanged ( int )"),self.useThemesChanged)
		QtCore.QObject.connect(self.ui.themes, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem *, QListWidgetItem *)"),self.themeChanged)

		# Plugins
		QtCore.QObject.connect(self.ui.applyButton, QtCore.SIGNAL("clicked()"),self.save)
		QtCore.QObject.connect(self.ui.pluginConfiguration, QtCore.SIGNAL("clicked()"),self.pluginConfigurationClicked)
		QtCore.QObject.connect(self.ui.plugins, QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.pluginsContextMenu)
		QtCore.QObject.connect(self.ui.plugins, QtCore.SIGNAL("itemClicked ( QTreeWidgetItem *, int)"),self.pluginSelected)
		QtCore.QObject.connect(self.ui.listWidget, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem * , QListWidgetItem * )"),self.currentItemChanged)
		
		QtCore.QObject.connect(self.ui.moreEmoticons, QtCore.SIGNAL("clicked()"),self.getMoreEmoticons)
		QtCore.QObject.connect(self.ui.morePlugins, QtCore.SIGNAL("clicked()"),self.getMorePlugins)
	
	def getMoreEmoticons(self):
		d=extraDialog("emoticons",self.main,self.main)
		d.exec_()

	def getMorePlugins(self):
		d=extraDialog("plugins",self.main,self.main)
		d.exec_()

	def currentItemChanged(self,item,previous):
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
		self.ui.emoticonsList.clear()
		self.ui.chatSkin_list.clear()
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

		# chat skins from Jabbim root directory
		packs=os.listdir("chatskins/")
		for pack in packs:
			if os.path.isdir('chatskins/'+pack):
				skins=os.listdir('chatskins/'+pack+"/")
				for skin in skins:
					if skin.endswith('.cfg'):
						path=pack+"/"+skin
						#config=ConfigObj("chatskins/"+path,encoding='UTF8')
						loaded,config=self.main.loadJabbimExtraConfig("chatskins/"+path,'chatskins/cool/cool.cfg')
						if loaded:
							if path==self.main.config["chatSkin"]:
								self.ui.chatSkin_list.insertItem(0,unicode(config['header']['name']),QtCore.QVariant(path))
							else:
								self.ui.chatSkin_list.addItem(unicode(config['header']['name']),QtCore.QVariant(path))

		# chat skins from Jabbim root directory
		packs=os.listdir(self.main.realHomeDir+"/chatskins/")
		for pack in packs:
			if os.path.isdir(self.main.realHomeDir+'/chatskins/'+pack):
				skins=os.listdir(self.main.realHomeDir+'/chatskins/'+pack+"/")
				for skin in skins:
					if skin.endswith('.cfg'):
						path=pack+"/"+skin
						#config=ConfigObj(self.main.realHomeDir+"/chatskins/"+path,encoding='UTF8')
						loaded,config=self.main.loadJabbimExtraConfig(self.main.realHomeDir+"/chatskins/"+path,'chatskins/cool/cool.cfg')
						if loaded:
							if path==self.main.config["chatSkin"]:
								self.ui.chatSkin_list.insertItem(0,unicode(config['header']['name']),QtCore.QVariant(path))
							else:
								self.ui.chatSkin_list.addItem(unicode(config['header']['name']),QtCore.QVariant(path))

		#skins=os.listdir("skins/")
		#for skin in skins:
			#if skin.endswith(".conf"):
				#if skin==self.main.config["chat_skin"]:
					#self.ui.chatSkin_list.insertItem(0,unicode(skin))
					#self.chatSkin_listChanged(skin)
				#else:
					#self.ui.chatSkin_list.addItem(unicode(skin))
		self.chatSkin_listChanged(0)
		self.ui.chatSkin_list.setCurrentIndex(0)

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
			
			f.close()
			if categories.has_key(plug.category[0]):
				item=QtGui.QTreeWidgetItem(categories[plug.category[0]])
			else:
				item=QtGui.QTreeWidgetItem(categories['other'])
			widget=QtGui.QCheckBox(self.ui.plugins)
			print plugin,self.loadedPlugins
			if plugin in self.loadedPlugins:
				print "setChecked True"
				widget.setChecked(True)
				self.ui.plugins.setItemExpanded(item.parent(),True)
			self.ui.plugins.setItemWidget(item,0,widget)
			item.setText(1,plug.name)
			item.setText(2,plug.description)
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

	def chatSkin_listChanged(self,index):
		path=unicode(self.ui.chatSkin_list.itemData(index).toString())
		src='chatskins/'

		loaded,config=self.main.loadJabbimExtraConfig("chatskins/"+path,'chatskins/cool/cool.cfg')
		if len(config)==0 or not loaded:
			src=self.main.realHomeDir+'/chatskins/'
			#config=ConfigObj(self.main.realHomeDir+"/emoticons/"+path,encoding='UTF8')
			loaded,config=self.main.loadJabbimExtraConfig(self.main.realHomeDir+"/chatskins/"+path,'chatskins/cool/cool.cfg')
			if not loaded:
				return
		html=""
		html+=self.tr("Name: ")+unicode(config['header']['name'])+"<br/>"
		if config['header'].has_key('license'):
			html+=self.tr("License: ")+unicode(config['header']['license'])+"<br/>"
		self.ui.chatSkinInfo.setText(html)
		
		self.ui.chatSkin_preview.clear()
		self.chatSkinPreviewtextEditWrite(config['chatskin']["message_history"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("This is test message send in past."))).replace('[background]',config['chatskin']['color1'][0]).replace('[foreground]',config['chatskin']['color1'][1]).replace("[avatar]","<img src=\"images/16x16/apps/jabbim.png\" width=\"16\" height=\"16\" />"))
		self.chatSkinPreviewtextEditWrite(config['chatskin']["my_message_history"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("Me"))).replace("[message]",unicode(self.tr("This is my test message send in past."))).replace("[avatar]","<img src=\"images/16x16/apps/jabbim.png\" width=\"16\" height=\"16\" />"))
		self.chatSkinPreviewtextEditWrite(config['chatskin']["message_for_me_history"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("Me"))+", "+unicode(self.tr("this is message contains my name send in past."))).replace("[avatar]","<img src=\"images/16x16/apps/jabbim.png\" width=\"16\" height=\"16\" />"))
		self.chatSkinPreviewtextEditWrite(config['chatskin']["message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("This is test message."))).replace('[background]',config['chatskin']['color1'][0]).replace('[foreground]',config['chatskin']['color1'][1]).replace("[avatar]","<img src=\"images/32x32/apps/jabbim.png\" width=\"32\" height=\"32\" />"))
		self.chatSkinPreviewtextEditWrite(config['chatskin']["my_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("Me"))).replace("[message]",unicode(self.tr("This is my test message."))).replace("[avatar]","<img src=\"images/32x32/apps/jabbim.png\" width=\"32\" height=\"32\" />"))
		self.chatSkinPreviewtextEditWrite(config['chatskin']["message_for_me"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("Me"))+", "+unicode(self.tr("this is message contains my name."))).replace("[avatar]","<img src=\"images/32x32/apps/jabbim.png\" width=\"32\" height=\"32\" />"))
		self.chatSkinPreviewtextEditWrite(config['chatskin']["status_message"].replace("[time]",self.main.now()).replace("[message]",unicode(self.tr("User has set the subject to: Subject"))))


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
			self.main.loadSkin()
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
		if self.main.config['rosterMode']=="compact":
			import compactrosterstyle
			self.main.ui.roster.setRosterStyle(compactrosterstyle.rosterStyle)
		elif self.main.config['rosterMode']=='normal':
			import defaultrosterstyle
			self.main.ui.roster.setRosterStyle(defaultrosterstyle.rosterStyle)
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
				widget=self.ui.plugins.itemWidget(item,0)
				if widget.isChecked()==True and not plugin in self.loadedPlugins:
					if self.main.client:
						self.main.loadPlugin(plugin)
					self.main.config['plugins'].append(plugin)
					self.loadedPlugins=self.main.config['plugins']
					load=True
				elif widget.isChecked()==False and plugin in self.loadedPlugins:
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
