'''
Created on 17.4.2010

@author: sef
'''
from configobj import ConfigObj
from include.constants import RESOURCEPATH
from os.path import basename,dirname, isfile
from PyQt4 import QtGui
import os
import sys
import traceback
import widgets.webkitthemes
from imp import load_source

class ResourceManager(object):
	'''
	Manages access to various client resources
	'''


	def __init__(self, main):
		self.main = main
	
	def isValidExtraPart(self,config):
		if not config.has_key('header'):
			#log.err("error, config doesn't have 'header' section")
			return False
		if not config['header'].has_key('type'):
			#log.err("error, config doesn't have 'type' key in 'header' section")
			##############################################################
			# We're tolerant for RPC emoticons, so I have to enable them #
			##############################################################
			typ='emoticons' # will be commented
			#return False # will be uncommented
		else: # will be commented
			typ=unicode(config['header']['type']) # will be commented
		keys=['name','license','author','version','description']
		if typ=="moodIcons":
			keys.append('frontImage')
			if not config.has_key('moods'):
				#log.err("error, config doesn't have 'moods' section")
				return False
		elif typ=="emoticons":
			keys.append('frontImage')
			##############################################################
			# We're tolerant for RPC emoticons, so I have to enable them #
			##############################################################
			keys=[] # will be commented
			if not config.has_key('emoticons'):
				#log.err("error, config doesn't have 'emoticons' section")
				return False
		elif typ=='chatskin':
			if not config.has_key('chatskin'):
				#log.err("error, config doesn't have 'chatskin' section")
				return False
		for key in keys:
			if not config['header'].has_key(key):
				#log.err("error, config doesn't have '"+key+"' key in 'header' section")
				return False
		return True

	def loadJabbimExtraConfig(self,config,fallback):
		#log.err('loading JabbimExtra config '+ unicode(config))
		# try to load config
		try:
			config=ConfigObj(config,encoding='UTF8')
			loaded=True
		except:
			loaded=False
		# check config validity
		if loaded:
			loaded=self.isValidExtraPart(config)
		# config is valid
		if loaded:
			return True,config
		else:
			# try to load fallback config
			try:
				config=ConfigObj(fallback,encoding='UTF8')
				loaded=True
			except:
				loaded=False
			# check config validity
			if loaded:
				loaded=self.isValidExtraPart(config)
			if loaded:
				return False,config
			else:
				return None,None

	def loadMoods(self):
		"""
		Loads user mood icons
		"""
		loaded,config=self.loadJabbimExtraConfig(RESOURCEPATH+'moods/'+self.main.config['moods'],'moods/default/default.cfg')
		if loaded!=None:
			if loaded:
				src=dirname(RESOURCEPATH+"moods/"+self.main.config["moods"])+"/"
			else:
				src=dirname(RESOURCEPATH+"moods/default/")
			self.main.ui.moodButton.setIcon(QtGui.QIcon(src+config['header']['frontImage']))
			self.main.moodIcons=config['moods']
			for mood in self.main.moodIcons.keys():
				path=unicode(src+self.main.moodIcons[mood])
				self.main.moodIcons[mood]=QtGui.QIcon(path)
				self.main.moodIcons[mood].src=unicode(os.getcwd(), sys.getfilesystemencoding())+"/"+path
			self.main.moodIcons["none"]=QtGui.QIcon(self.main.moodIcons[mood].pixmap(16,16,QtGui.QIcon.Disabled))

	def loadActivities(self):
		"""
		Loads user mood icons
		"""
		loaded,config=self.loadJabbimExtraConfig(RESOURCEPATH+'activities/'+self.main.config['activities'],'activities/default/default.cfg')
		#print "ACTIVITIES",loaded,config
		if loaded!=None:
			if loaded:
				src=dirname(RESOURCEPATH+"activities/"+self.main.config["activities"])+"/"
			else:
				src=dirname(RESOURCEPATH+"activities/default/")
			#self.ui.moodButton.setIcon(QtGui.QIcon(src+config['header']['frontImage']))
			self.main.activityIcons=config['activities']
			for mood in self.main.activityIcons.keys():
				path=unicode(src+self.main.activityIcons[mood])
				self.main.activityIcons[mood]=QtGui.QIcon(path)
				self.main.activityIcons[mood].src=unicode(os.getcwd(), sys.getfilesystemencoding())+"/"+path
			self.main.activityIcons["none"]=QtGui.QIcon(self.main.activityIcons[mood].pixmap(16,16,QtGui.QIcon.Disabled))
		#print "ACTIVITIES",self.activityIcons

	def loadSounds(self):
		src=dirname(RESOURCEPATH +"sounds/"+self.main.config["soundPack"])
		self.main.sounds=ConfigObj(RESOURCEPATH+"sounds/"+self.main.config["soundPack"],encoding='UTF8')
		if len(self.main.sounds)==0:
			self.main.sounds=ConfigObj(self.main.realHomeDir+"/sounds/"+self.main.config["soundPack"],encoding='UTF8')
			src=dirname(self.main.realHomeDir+"/sounds/"+self.main.config["soundPack"])
		src+="/"
		self.main.sounds=self.main.sounds['sounds']
		for sound in self.main.sounds.keys():
			self.main.sounds[sound]=src+self.main.sounds[sound]

	def playsound(self,sound):
		if self.main.sounds.has_key(sound):
			if sys.platform == 'linux2': # linux sounds are produced using aplay
				os.system('aplay -q "'+self.main.sounds[sound].strip('\n')+'" &')
			else:
				QtGui.QSound.play(self.main.sounds[sound].strip('\n'))
			return True
		return False

	def loadThemePackage(self):
		self.main.themePackage = None
		if len(self.main.config['themePackage'])==0:
			self.main.config['themePackage']="default/default.cfg"
			self.main.config.write()
		theme = RESOURCEPATH+"themepackages/" + unicode(self.main.config['themePackage'])
		if not isfile(theme):
			theme = self.main.realHomeDir + "/themepackages/" + unicode(self.main.config['themePackage'])
			if not isfile(theme):
				theme=RESOURCEPATH+"themepackages/default/default.cfg"
		
		self.main.themePackage = ConfigObj(theme,encoding='UTF8')
		if len(self.main.themePackage)!=0:
			for key in ["chatTheme","groupchatTheme","soundPack","mood","emoticons","activities","rosterStyle","theme"]:
				if self.main.themePackage.has_key(key):
					if len(self.main.themePackage[key]["value"])!=0:
						if len(self.main.config[key])==0:
							self.main.config[key] = self.main.themePackage[key]["value"]
		
		

	def loadRosterStyle(self):
		self.main.rosterStyle=None
		if self.main.config['rosterStyle']==None or len(self.main.config['rosterStyle'])==0:
			self.main.config['rosterStyle']="ng/config.cfg"
			self.main.config.write()
		path=RESOURCEPATH+"rosterstyles/"+unicode(self.main.config['rosterStyle'].split("/")[0])+"/style.py"
		if not isfile(path):
			path=self.main.realHomeDir+"/rosterstyles/"+unicode(self.main.config['rosterStyle'].split("/")[0])+"/style.py"
			if not isfile(path):
				path=RESOURCEPATH+"rosterstyles/ng/style.py"


		variant=self.main.realHomeDir+"/rosterstyles/"+unicode(self.main.config['rosterStyle'])
		if not isfile(variant):
			variant=RESOURCEPATH+"rosterstyles/"+unicode(self.main.config['rosterStyle'])
			if not isfile(variant):
				variant=RESOURCEPATH+"rosterstyles/ng/config.cfg"

		try:
			f=open(unicode(path))
		except:
			return
		try:
			#plug =  # load plugin module
			module = load_source('rosterStyle', path, f)
			f.close()
			self.main.ui.roster.setRosterStyle(module.rosterStyle,variant)
		except Exception, ex:
					#log.msg(unicode(plugin)+u': '+unicode(ex))
					traceback.print_exc()
					f.close()
					pass

	def loadSkin(self):
		"""
		Loads chat skin. Skin is loaded to self.skin.
		"""
		#loaded,self.skin=self.loadJabbimExtraConfig("chatskins/"+self.config['chatSkin'],"chatskins/cool/cool.cfg")
		self.main.skin={}
		#if not self.skin.has_key("spaces_between_lines"):
		#	self.skin["spaces_between_lines"]='0'
		self.main.webkitThemeFactory=widgets.webkitthemes.webkitThemeFactory(self.main.config['chatTheme'],self.main.config['groupchatTheme'],self.main.realHomeDir)
		for i in range(self.main.chat.ui.chatTab.count()):
			w=self.main.chat.ui.chatTab.widget(i)
			w.chat.loadWebkit()		
			
	def loadTheme(self,text=None,file=None):
		"""
		Loads theme. If text==None, self.config['theme'] is used. Otherwise is stylesheet sets to `text`.
		@type text: unicode
		@param text: stylesheet css
		"""
		self.main.setStyleSheet("") # windows hack

		if self.main.config['theme']=="None" and not text:
			# theme isn't used
			text=""
			self.main.ui.roster.theme=False
			self.main.app.setStyle(self.main.qtStylesDefault)
		else:
			self.main.ui.roster.theme=True
		if text==None:
			# open theme according to self.config
			try:
				conf=ConfigObj(RESOURCEPATH+"themes/"+self.main.config['theme']+"/theme.ini",encoding='UTF8')
				style=False
				if conf!=None and len(conf)!=0:
					if conf.has_key('style'):
						if conf['style'] in self.qtStyles:
							self.main.app.setStyle(QtGui.QStyleFactory.create(conf['style']))
							style=True
				if not style:

					self.main.app.setStyle(self.main.qtStylesDefault)
				theme=open(RESOURCEPATH+"themes/"+self.main.config['theme']+"/style.css")
				text=theme.read()
				self.main.setStyleSheet(text)
				self.main.chat.setStyleSheet(text)
				theme.close()
			except IOError:
				# theme isn't used
				text=""
				self.main.ui.roster.theme=False
				self.main.app.setStyle(self.main.qtStylesDefault)
		else:
			# use text for stylesheet css
			if file:
				conf=ConfigObj(RESOURCEPATH+"themes/"+file+"/theme.ini",encoding='UTF8')
				style=False
				if conf!=None and len(conf)!=0:
					if conf.has_key('style'):
						if conf['style'] in self.main.qtStyles:
							self.main.app.setStyle(QtGui.QStyleFactory.create(conf['style']))
							style=True
				if not style:

					self.main.app.setStyle(self.main.qtStylesDefault)
			self.main.setStyleSheet(text)
			self.main.chat.setStyleSheet(text)
			if text:
				if len(text)==0:
					self.main.ui.roster.theme=False
		self.main.styleSheetText=text
		self.main.ui.roster.reskin(text) # reskin roster