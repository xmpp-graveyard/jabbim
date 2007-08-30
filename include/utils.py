"""
Copyright (C) 2007 	Jan 'Hanzz' Kaluza (hanzz at njs.netlab.cz)
Copyright (C) 2007	Jiri 'Sef' Gabrys	(sef at njs.netlab.cz)

Copyright (C) 2003-2006 Yann Le Boulanger <asterix@lagaule.org>
Copyright (C) 2005-2006 Nikos Kouremenos <kourem@gmail.com>
Copyright (C) 2005
                   Dimitur Kirov <dkirov@gmail.com>
                   Travis Shirk <travis@pobox.com>
Copyright (C) 2007 Lukas Petrovicky <lukas@petrovicky.net>

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
import os,sys, re
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
			"chat_skin":"gajim.conf",
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
# 	if sys.platform != 'win32' :
# 		return os.path.expanduser( '~' )+'/.jabbim'
# 	def valid(path):
# 		if path and os.path.isdir(path):
# 			return True
# 		return False
# 	def env(name):
# 		return os.environ.get( name, '' )
# 	homeDir = env( 'USERPROFILE' )
# 	if not valid(homeDir):
# 		homeDir = env( 'HOME' )
# 		if not valid(homeDir):
# 			homeDir = '%s%s' % (env('HOMEDRIVE'),env('HOMEPATH'))
# 			if not valid(homeDir):
# 				homeDir = env( 'SYSTEMDRIVE' )
# 				if homeDir and (not homeDir.endswith('\\')):
# 					homeDir += '\\'
# 				if not valid(homeDir):
# 					homeDir = 'C:\\'
	homeDir = os.path.expanduser( '~' )+'/.jabbim'
# 	homeDir = homeDir + './jabbim'
	return unicode(homeDir, sys.getfilesystemencoding())

def path(cesta):
  return cesta.encode(sys.getfilesystemencoding())

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

distro_info = {
	'Arch Linux': '/etc/arch-release',
	'Aurox Linux': '/etc/aurox-release',
	'Conectiva Linux': '/etc/conectiva-release',
	'CRUX': '/usr/bin/crux',
	'Debian GNU/Linux': '/etc/debian_release',
	'Debian GNU/Linux': '/etc/debian_version',
	'Fedora Linux': '/etc/fedora-release',
	'Gentoo Linux': '/etc/gentoo-release',
	'Linux from Scratch': '/etc/lfs-release',
	'Mandrake Linux': '/etc/mandrake-release',
	'Slackware Linux': '/etc/slackware-release',
	'Slackware Linux': '/etc/slackware-version',
	'Solaris/Sparc': '/etc/release',
	'Source Mage': '/etc/sourcemage_version',
	'SUSE Linux': '/etc/SuSE-release',
	'Sun JDS': '/etc/sun-release',
	'PLD Linux': '/etc/pld-release',
	'Yellow Dog Linux': '/etc/yellowdog-release',
	# many distros use the /etc/redhat-release for compatibility
	# so Redhat is the last
	'Redhat Linux': '/etc/redhat-release'
}

def get_os_info():
	if os.name == 'nt':
		ver = os.sys.getwindowsversion()
		ver_format = ver[3], ver[0], ver[1]
		win_version = {
			(1, 4, 0): '95',
			(1, 4, 10): '98',
			(1, 4, 90): 'ME',
			(2, 4, 0): 'NT',
			(2, 5, 0): '2000',
			(2, 5, 1): 'XP',
			(2, 5, 2): '2003',
			(2, 6, 0): 'Vista',
		}
		if win_version.has_key(ver_format):
			return 'Windows' + ' ' + win_version[ver_format]
		else:
			return 'Windows'
	elif os.name == 'posix':
		executable = 'lsb_release'
		params = ' --id --codename --release --short'
		full_path_to_executable = is_in_path(executable, return_abs_path = True)
		if full_path_to_executable:
			command = executable + params
			child_stdin, child_stdout = os.popen2(command)
			output = temp_failure_retry(child_stdout.readline).strip()
			child_stdout.close()
			child_stdin.close()
			os.wait()
			# some distros put n/a in places, so remove those
			output = output.replace('n/a', '').replace('N/A', '')
			return output

		# lsb_release executable not available, so parse files
		for distro_name in distro_info:
			path_to_file = distro_info[distro_name]
			if os.path.exists(path_to_file):
				if os.access(path_to_file, os.X_OK):
					# the file is executable (f.e. CRUX)
					# yes, then run it and get the first line of output.
					text = get_output_of_command(path_to_file)[0]
				else:
					fd = open(path_to_file)
					text = fd.readline().strip() # get only first line
					fd.close()
					if path_to_file.endswith('version'):
						# sourcemage_version and slackware-version files
						# have all the info we need (name and version of distro)
						if not os.path.basename(path_to_file).startswith(
						'sourcemage') or not\
						os.path.basename(path_to_file).startswith('slackware'):
							text = distro_name + ' ' + text
					elif path_to_file.endswith('aurox-release'):
						# file doesn't have version
						text = distro_name
					elif path_to_file.endswith('lfs-release'): # file just has version
						text = distro_name + ' ' + text
				return text

		# our last chance, ask uname and strip it
		uname_output = get_output_of_command('uname -a | cut -d" " -f1,3')
		if uname_output is not None:
			return uname_output[0] # only first line
	return 'N/A'

def is_in_path(name_of_command, return_abs_path = False):
	# if return_abs_path is True absolute path will be returned
	# for name_of_command
	# on failures False is returned
	is_in_dir = False
	found_in_which_dir = None
	path = os.getenv('PATH').split(':')
	for path_to_directory in path:
		try:
			contents = os.listdir(path_to_directory)
		except OSError: # user can have something in PATH that is not a dir
			pass
		else:
			is_in_dir = name_of_command in contents
		if is_in_dir:
			if return_abs_path:
				found_in_which_dir = path_to_directory
			break

	if found_in_which_dir:
		abs_path = os.path.join(path_to_directory, name_of_command)
		return abs_path
	else:
		return is_in_dir

def get_output_of_command(command):
	try:
		child_stdin, child_stdout = os.popen2(command)
	except ValueError:
		return None

	output = child_stdout.readlines()
	child_stdout.close()
	child_stdin.close()

	return output

def temp_failure_retry(func, *args, **kwargs):
	while True:
		try:
			return func(*args, **kwargs)
		except (os.error, IOError, select.error), ex:
			if ex.errno == errno.EINTR:
				continue
			else:
				raise

def replace_url(text):
	exp = re.compile("([A-Za-z][A-Za-z0-9+.-]{1,120}:[A-Za-z0-9/](([A-Za-z0-9$_.+!*,;/?:@&~=-])|%[A-Fa-f0-9]{2}){1,333}(#([a-zA-Z0-9][a-zA-Z0-9$_.+!*,;/?:@&~=%-]{0,1000}))?)")
	for link in exp.findall(text):
		text = text.replace(link[0], '<a href="%s">%s</a>'%(link[0], link[0]))
	print text
	return text


