import os,sys
from configobj import ConfigObj

def cprint(color,text):
	text=unicode(text)
	if color=="yellow":
		return "\033[1;33m"+text+" \033[0m"
	elif color=="red":
		return "\033[0;31m"+text+" \033[0m"
	elif color=="green":
		return "\033[0;32m"+text+" \033[0m"
	elif color=="lightblue":
		return "\033[1;34m"+text+" \033[0m"
	elif color=="lightgray":
		return "\033[0;37m"+text+" \033[0m"
	elif color=="lightcyan":
		return "\033[1;36m"+text+" \033[0m"
	else:
		return text

def loadConfig(main):
	# loads config and repairs config file
	configs={"jid":"",
			"passwd":"",
			"savePasswd":"",
			"rosterIconSize":"16x16",
			"chat_skin":"default.conf",
			"theme":"template",
			"log":"true",
			"logfile":"jabbim.log",
			"windowGeometry":[0,0,None,None],
			"chatGeometry":[0,0,None,None],
			"saveGeometry":True,
			"saveExpandedGroups":True,
			"expandedGroups":[],
			"plugins":['notification'],
			"rosterMode":"normal",
			"chatMode":"normal"
			}
	main.config=ConfigObj(main.homeDir+'/config',encoding='UTF8')
	if len(main.config)==0:
		if not os.path.isdir(main.homeDir):
			os.mkdir(main.homeDir)
		main.config=ConfigObj(main.homeDir+'/config',encoding='UTF8')
		for k,v in configs.iteritems():
			main.config[k]=v
		main.config.write()
	rewrite=False
	for k,v in configs.iteritems():
		try:
			main.config[k]
		except:
			main.config[k]=v
			rewrite=True
	if rewrite==True:
		main.config.write()
	if not os.path.isdir(main.homeDir+'/avatars'):
		os.mkdir(main.homeDir+'/avatars')
	if not os.path.isdir(main.homeDir+'/plugins'):
		os.mkdir(main.homeDir+'/plugins')

def getHomeDir():
	# gets homedir on win32 or linux
	if sys.platform != 'win32' :
		return os.path.expanduser( '~' )+'/.jabbim'
	def valid(path):
		if path and os.path.isdir(path):
			return True
		return False
	def env(name):
		return os.environ.get( name, '' )
	homeDir = env( 'USERPROFILE' )
	if not valid(homeDir):
		homeDir = env( 'HOME' )
		if not valid(homeDir):
			homeDir = '%s%s' % (env('HOMEDRIVE'),env('HOMEPATH'))
			if not valid(homeDir):
				homeDir = env( 'SYSTEMDRIVE' )
				if homeDir and (not homeDir.endswith('\\')):
					homeDir += '\\'
				if not valid(homeDir):
					homeDir = 'C:\\'
	homeDir = homeDir + './jabbim'
	return homeDir
