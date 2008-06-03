#-*- coding: UTF-8 -*-

import sys,os,time, re
sys.path.append('.')
from include import plugins
from twisted.python import log
from configobj import ConfigObj
from pyxl import jid as jidT
from twisted.web import xmlrpc, server
from PyQt4 import QtCore, QtGui
from twisted.python import log
from time import time
from twisted.internet import threads
from twisted.words.xish.domish import escapeToXml
try:
	from hashlib import sha1
except:
	log.msg('Please upgrade to python2.5')
	from sha import new as sha1
from imp import load_source
from include import utils
from pyxl.xdata import *
from pyxl.adhoc import Stage, CancelStage
from twisted.python import log
class ResendFile(Stage):
	def exec_(self):
		self.status = "executing"
		self.actions = {"cancel":CancelStage, "next":ResendFile, 'prev': ResendFile, "execute":ResendFile}
		self.execute = "next"

		print self.session.args
		files = []
		dirs = []

		print self.data

		if self.data == None or len(self.data['file']) == 0:
			if not self.session.args.has_key('last'):
				print 'nemam last'
				pwd = self.session.args['home']
				self.session.args['last'] = pwd
			else:
				if self.session.args['last'] != self.session.args['home']:
					pwd = os.path.split(self.session.args['last'])[0]
				else:
					pwd = self.session.args['home']
		
		else:

			for file in self.data['file']:
				if file == os.path.pardir:
					dirs.insert(0, file)
				elif os.path.isdir(os.path.join(self.session.args['last'], file)):
					dirs.append(file)
				elif os.path.isfile(os.path.join(self.session.args['last'], file)):
					files.append(file)
		
			print dirs, files
			
			if len(files)>0:
				desc = {}
				fajly = []
				for f in files:
					ff = os.path.join(self.session.args['last'], f)
					desc[ff] = 'EasyShare'
					fajly.append(ff)
				self.main.events.addFTUploadEvent(self.session.jid, fajly, desc)
				self.status = "completed"
				self.execute = None
				self.actions={}
				self.xform = None
				return
			elif len(dirs)>0:
				if dirs[0] == os.path.pardir:
					pwd = os.path.split(self.session.args['last'])[0]
				else:
					pwd = os.path.join(self.session.args['last'], dirs[0])
			else:
				pwd = self.session.args['home']
					
#		elif os.path.isdir(os.path.join(self.data["pwd"][0], self.data["file"][0])):
#			if self.data["file"][0] == os.path.pardir:
#				pwd = os.path.split(self.data["pwd"][0])[0]
#			else:
#				pwd = os.path.join(self.data["pwd"][0], self.data["file"][0])
		files = []
		dirs = []
		
		self.session.args['last'] = pwd
		print pwd, pwd ==  self.session.args['home']
		print self.session.args['home']
		for f in os.listdir(unicode(pwd)):
			try:
				if os.access(os.path.join(pwd,f), os.R_OK):
					if os.path.isfile(os.path.join(pwd,f)):
						files.append([f, f])
					else:
						dirs.append(["%s%s" % (f, os.path.sep), f])
			except:
				print 'chyba v listovani'
		files.sort()
		dirs.sort()
		if pwd != self.session.args['home']:
			dirs.insert(0, ["%s%s (%s)" % (os.path.pardir, os.path.sep, self.main.tr("One directory up")), os.path.pardir])
		dirs.extend(files)

		field = Field("file", "list-multi", self.main.tr("Choose file or directory: "), required=True, options=dirs)
#		field2 = Field("pwd", "hidden", values=[pwd])
		self.xform = Xform("form", fields=[field], title=self.main.tr("Resend file"),instructions=[self.main.tr("Choose file you want to resend from remote system or directory you want to browse."),"PWD: %s" % unicode(pwd)]).buildElement()

class config:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['sharepath']={'type':'directory','label':self.main.tr("Path"),'value':''}
		self.config['sharejids']={'type':'jid-list','label':self.main.tr("Allow JIDs"),'value':[]}

class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'easyshare'
		self.description = 'Easy filesharing'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'EasyShare'
		self.version = '0.01'
		self.category = ['utils']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.plugindir = plugindir
		self.configDialog=config(self)
		self.public = []
		self.home = ''
		
		
		if main:
			self.loadConfig()
			self.home = self.config['sharepath']
			jids = self.config['sharejids']#.strip()
			#jids = jids.split(',')
			for jd in jids:  #tohle chce predelat asi
				if jd.strip() != '':
					self.public.append(jd.strip())
			print self.public
			self.registerHandler('on_authd',self.on_authd)

		else:
			self.loadConfig(homedir)
	
	def on_authd(self):
		self.main.client.commands.registerNode("http://dev.jabbim.cz/jabbim/rc#easyshare", "Get file", ResendFile, public = self.public, args = {'home':self.home})
	
	def on_configChanged(self):
			self.public = []
			self.main.client.commands.unregisterNode("http://dev.jabbim.cz/jabbim/rc#easyshare", "Get file")
			self.home = self.config['sharepath']
			jids = self.config['sharejids']
			#jids = jids.split(',')
			for jd in jids:  #tohle chce predelat asi
				if jd.strip() != '':
					self.public.append(jd.strip())
			self.main.client.commands.registerNode("http://dev.jabbim.cz/jabbim/rc#easyshare", "Get file", ResendFile, public = self.public, args = {'home':self.home})
	
	def on_remove(self):
		self.main.client.commands.unregisterNode("http://dev.jabbim.cz/jabbim/rc#easyshare", "Get file")
	
	def buildContactMenu(self, menu, contact):
		self.action=menu.addAction(self.tr("EasyShare"))
		self.action.setData(QtCore.QVariant(unicode(contact.jid)))
		self.action.setObjectName("easyshare")
		self.action.setIcon(QtGui.QIcon("%s/easy_share32.png" % self.pluginDir))
		self.action.setCheckable(True)
		if unicode(contact.jid) in self.public:
			self.action.setChecked(True)
		else:
			self.action.setChecked(False)
		QtCore.QObject.connect(self.action,QtCore.SIGNAL("triggered ( bool )"),self.toggled)
		
	def toggled(self, b):
		jid=unicode(self.action.data().toString())
		if jid in self.public:
			self.public.remove(jid)
			self.action.setChecked(False)
		else:
			self.public.append(jid)
			self.action.setChecked(True)
		self.config['sharejids'] = self.public
		self.writeConfig()
		self.on_configChanged()
		self.action.deleteLater()
