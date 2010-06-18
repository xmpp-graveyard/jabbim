'''
Created on 17.4.2010

@author: sef
'''
import sys
import os
from include import utils
from os.path import isfile, dirname
from urllib import quote, unquote
from os.path import basename, dirname, isfile
from hashlib import sha1
from imp import load_source
from twisted.python import log
import traceback
import gc

class PluginManager(object):
	'''
    Used for manipulation with plugins. Loading/unloading etc.
    '''


	def __init__(self, main):
		'''
        Constructor
        '''
		self.main = main
		self.plugins = {}


	def findPlugins(self):
		"""
		Finds plugins in plugins/ and ~/plugins and saves informations about them to the self.plugins
		"""
		if len(self.plugins) != 0:
			return  # we've done this already
		plugin_paths = [unicode(os.getcwd(), sys.getfilesystemencoding()) + '/plugins/', self.main.realHomeDir + '/plugins/']
		for plugin_path in plugin_paths:
			for plugin_name in os.listdir(plugin_path):
				dir = '%s/%s' % (plugin_path, plugin_name)
				if plugin_name == '.svn' or isfile(dir):
					continue
				path = '%s/%s.py' % (dir, plugin_name)

				try:
					f = open(utils.path(path))
					module = load_source(plugin_name, path.encode(sys.getfilesystemencoding()), f)
					f.close()
					plug = module.Plugin(False, self.main.homeDir, dir)
					version = float(plug.version)
				except Exception, ex:
					log.msg(path + ': BAD PLUGIN!')
					log.msg(traceback.format_exc())
					continue

				if not self.plugins.has_key(plugin_name) or version > self.plugins[plugin_name]['version']:
					self.plugins[plugin_name] = { 'dir': dir, 'version': version, 'module': None }
		return self.plugins
	
	def getPlugin(self, plugin):
		if self.plugins.has_key(plugin):
			return self.plugins[plugin]['module']
		else:
			return None
	
	def loadPlugins(self):
		"""
		Loads plugins according to config file (self.config['plugins'])
		"""
		print "loadplugins"
		for plugin_name in self.plugins.keys():
			if plugin_name in self.main.config['plugins']:
				try:
					self.loadPlugin(plugin_name)
				except Exception, ex:
					print "1"
					log.msg(plugin_name + ': ' + unicode(ex))
		if self.main.client:
			self.main.client.dispatcher.publishEvent('on_pluginsLoaded')
		#log.msg("PLUGINS:"+unicode(self.plugins))

	def loadPlugin(self, plugin):
		"""
		Loads plugin. Plugin is loaded to the self.plugins[name]['module'].
		@type plugin: unicode
		@param plugin: plugins name
		"""
		dir = self.plugins[plugin]['dir']
		path = utils.path('%s/%s.py' % (dir, plugin))
		log.msg("loading " + unicode(plugin) + " plugin")

		try:
			f = open((path))
		except:
			log.msg('plugin load error: ' + plugin)
			return
		try:
			if not self.plugins[plugin]['module']:
				#plug =  # load plugin module
				module = load_source(plugin, path, f)
				f.close()
				self.plugins[plugin]['module'] = module.Plugin(self.main, self.main.homeDir, dir)
				self.runPluginCommand(self.plugins[plugin]['module'].buildMainWindowMenu, []) # build menu for plugin
				self.runPluginCommand(self.plugins[plugin]['module'].buildMainWindowToolBar, [])
			else:
				log.msg("plugin already loaded")
				f.close()
		except Exception, ex:
					#log.msg(unicode(plugin)+u': '+unicode(ex))
					traceback.print_exc()
					f.close()
					pass
		#log.msg("PLUGINS:"+unicode(self.plugins))
	
	def clientCreated(self):
		for plug in self.plugins.itervalues():
			if plug['module']:
				#print "calling client created"
				self.runPluginCommand(plug['module'].clientCreated,[])
	
	def buildContactMenu(self, contactMenu, contact):
		for key,value in self.plugins.iteritems():
			if value['module']:
				self.runPluginCommand(value['module'].buildContactMenu,[contactMenu,contact])
	def buildGroupchatContactMenu(self, menu, jid, user):
		for key,value in self.plugins.iteritems():
				if value['module']:
					self.runPluginCommand(value['module'].buildGroupchatContactMenu,[menu,jid,user])
			
	def buildMainWindowMenu(self):
		for plug in self.plugins.itervalues():
			if plug['module']:
				self.runPluginCommand(plug['module'].buildMainWindowMenu,[])
	def buildGroupchatWidget(self, jid, layout, groupchat):
		for key,value in self.plugins.iteritems():
			if value['module']:
				self.runPluginCommand(value['module'].buildGroupchatWidget,[jid, layout, groupchat])
	
	def on_groupchatMessageSend(self, jid, text, xhtml, state):
		ret = []
		for key,value in self.plugins.iteritems():
					if value['module']:
						ret.append(self.runPluginCommand(value['module'].on_groupchatMessageSend,[jid,text,xhtml,state]))

	def unloadPlugins(self):
		"""
		Unloads all currently loaded plugins plugins
		"""
		for i in self.plugins.keys():
			self.unloadPlugin(i)

	def unloadPlugin(self, plugin):
		"""
		Unloads plugin. Plugin module is deleted and self.plugins[plugin]=None
		@type plugin: unicode
		@param plugin: plugins name
		"""
		if self.plugins[plugin]['module']:
			self.main.ui.menuPlugins.clear() # clear plugins menu
			self.runPluginCommand(self.plugins[plugin]['module']._remove, []) # inform plugin that it will be removed

			l = gc.get_referents(self.plugins[plugin]['module'])
			for x in range(len(l)):
				del l[0]
			l = gc.get_referrers(self.plugins[plugin]['module'])
			for x in range(len(l)):
				del l[0]
			#del self.plugins[plugin]['module']
			self.plugins[plugin]['module'] = None
			#del self.plugins[plugin]
			gc.collect()
			del gc.garbage[:] # delete plugin from python
			# rebuild plugins menu
			self.buildMainWindowMenu()
		#else:
			#print "plugin is not loaded:",plugin
		#log.msg("PLUGINS:"+unicode(self.plugins))

	def runPluginCommand(self, command, args):
		"""
		Safely runs plugins command.
		@type command: pointer to function
		@param command: pointer to plugins function
		@type args: list
		@param args: list of arguments for function
		"""
		try:
			ret = command(*args)
			return ret
		except Exception, ex:
#	temporary bugfix by triak
#			log.msg('Plugin error: ' +unicode(ex))
			log.msg('In function:' + unicode(command))
			try:
				message = unicode(traceback.format_exc(), "utf-8")
				log.msg(message)
			except:
				try:
					message = unicode(traceback.format_exc(), "utf-8")
					log.msg(message)
				except:
					log.msg("can't decode traceback")   
	def _reloadPlugins(self):
		self.unloadPlugins()
		self.loadPlugins()
		for plug in self.plugins.itervalues():
			if plug['module']:
				self.runPluginCommand(plug['module'].userChanged,[self.main.config["jid"]])
