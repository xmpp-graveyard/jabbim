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
			"autoJoin":False,
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

def need_highlight(nick, text):
	# upraveno z gajimu
		special_words = []
		special_words.append(nick)
		# Strip empties: ''.split(';') == [''] and would highlight everything.
		# Also lowercase everything for case insensitive compare.
		special_words = [word.lower() for word in special_words if word]
		text = text.lower()

		text_splitted = text.split()
		for word in text_splitted: # get each word of the text
			for special_word in special_words:
				if word.startswith(special_word):
					# get char after the word that highlight us
					char_position = len(special_word)
					refer_to_nick_char = \
						word[char_position:char_position+1]
					if (refer_to_nick_char != ''):
						refer_to_nick_char_code = ord(refer_to_nick_char)
						if ((refer_to_nick_char_code < 65 or \
						refer_to_nick_char_code > 123) or \
						(refer_to_nick_char_code < 97 and \
						refer_to_nick_char_code > 90)):
							return True
						else: 
							# This is A->Z or a->z, we can be sure our nick is the
							# beginning of a real word, do not highlight. Note that we
							# can probably do a better detection of non-punctuation
							# characters
							return False
					else: # Special word == word, no char after in word
						return True 
		return False
