import os,sys
from configobj import ConfigObj

def cprint(color,text):
	text=unicode(text)
	if color=="yellow":
		print "\033[1;33m"+text+" \033[0m"
	elif color=="red":
		print "\033[0;31m"+text+" \033[0m"
	elif color=="green":
		print "\033[0;32m"+text+" \033[0m"
	elif color=="lightblue":
		print "\033[1;34m"+text+" \033[0m"
	elif color=="lightgray":
		print "\033[0;37m"+text+" \033[0m"
	elif color=="lightcyan":
		print "\033[1;36m"+text+" \033[0m"
	else:
		print text

def loadConfig(main):
	# loads config and repairs config file
	configs={"jid":"",
			"passwd":"",
			"savePasswd":"",
			"rosterIconSize":"16x16",
			"chat_skin":"default.conf",
			"theme":"template"
			}
	main.config=ConfigObj(main.homeDir+'/.jabbim/config',encoding='UTF8')
	if len(main.config)==0:
		if not os.path.isdir(main.homeDir+'/.jabbim'):
			os.mkdir(main.homeDir+'/.jabbim')
		main.config=ConfigObj(main.homeDir+'/.jabbim/config',encoding='UTF8')
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
	if not os.path.isdir(main.homeDir+'/.jabbim/avatars'):
		os.mkdir(main.homeDir+'/.jabbim/avatars')

def getHomeDir():
	# gets homedir on win32 or linux
	if sys.platform != 'win32' :
		return os.path.expanduser( '~' )
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
	return homeDir