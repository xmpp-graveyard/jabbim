import sys,os,time,tempfile,string
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from urllib import quote, unquote
from twisted.python import log
from twisted.words.protocols.jabber import jid

class config:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['self_gpg_id']={'type':'text-single','label':self.main.tr("Your long GPG id"),'value':self.main.tr('AABBCCDDEEFF0011')}
		self.config['passphrase']={'type':'text-private','label':self.main.tr("Passphrase"),'value':''}
		self.config['gpg_enabled_list']={'type':'jid-list','label':self.main.tr("GPG is enabled for:"),'value':''}
		self.config['remember_passphrase']={'type':'boolean','label':self.main.tr("Remember passphrase"),'value':''}

class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'gpg'
		self.installTranslator()
		self.description = self.tr('CAREFUL!\n' +
			'Plugin that allows you to use gnupg on linux.\n\n' +
			'This plugin requires gpg and all used keys imported.\n' +
			'If you enable this plugin, you can receive gpg encrypted messages ' +
			'set gpg key ids for jids and select to which people you send encrypted messages.\n\n' +
			'This version is very UNSECURE, it stores your passphrase in plaintext and everytime you ' +
			'decrypt a message, passphrase could be probably seen in /proc.')
		self.author = "Marek Hulan"
		self.name = self.tr('GPG plugin')
		self.version = '0.004'
		self.category = ['misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.passphrase = None
		self.configDialog=config(self)
		if main:
			self.registerHandler('on_message', self.on_message, priority = 4)

			self.loadConfig()
			self.key_dialog=self.loadDialog("%s/gpg_dialog.py" % self.pluginDir,self.main)

			if self.config['remember_passphrase'] == 'False':
				event=self.main.events.addLineEditEvent()
				event.setAcceptHandler(self.set_passphrase)
				event.setRejectHandler(self.unset_passphrase)
				widget=event.getWidgets()[0]
				widget.setText('Type a passphrase for your GPG key')
				widget.setEchoMode(2)
				widget.setLabel('Passphrase:')
				widget.setAcceptText(self.main.tr("OK"))
				widget.setRejectText(self.main.tr("Cancel"))
		else:
			self.loadConfig(homedir)

	def set_passphrase(self, phrase):
		self.passphrase = phrase

	def unset_passphrase(self):
		self.passphrase = None

	def on_message(self,msg):
		if self.config['remember_passphrase'] == 'False' and self.passphrase is None:
			# neni zadna passphrase
			# mela by vyskocit bublina, idealne spis pockat nez se pass zada
			return True
		else:
			passphrase = self.passphrase or self.config['passphrase']

		if not msg.getGpgEncryptedBody() is None:
			lines = os.popen('echo "' + passphrase + "\n-----BEGIN PGP MESSAGE-----\n\n" +
				msg.getGpgEncryptedBody() + '\n-----END PGP MESSAGE-----"' +
				' | gpg --charset utf8 --yes --passphrase-fd 0 --decrypt').readlines()
			message = string.join(lines, '')
			msg.setBody(message.rstrip("\n\x00"))
		return True

	def on_messageSend(self,msg):
		for jid_with_resource in self.config['gpg_enabled_list']:
			if (jid_with_resource == msg.to.userhost() or jid_with_resource == msg.to.full()) and self.config.has_key(msg.to.userhost()) and len(self.config[msg.to.userhost()]['long_key_id']) == 16:
				lines = os.popen('echo "' + msg.getBody() +
					'"| gpg --charset utf8 --batch --yes --armor --no-version --recipient ' +
					self.config[msg.to.userhost()]['long_key_id'] + ' --trusted-key="' +
					self.config[msg.to.userhost()]['long_key_id'] + '" --encrypt').readlines()
				message = string.join(lines[2:-1], '')
				msg.setGpgEncryptedBody(message)
		return msg

	def keyAccepted(self):
		key_id=unicode(self.key_dialog.ui.key_id.text())
		if not (self.config.has_key(self.jid) and self.config[self.jid].has_key('long_key_id')):
			self.config[self.jid]={'long_key_id':key_id}
		else:
			self.config[self.jid]['long_key_id']=key_id
		self.writeConfig()

	def showSlot(self,jid=None):
		self.key_dialog.show()
		self.jid=jid
		self.key_dialog.setWindowTitle(unicode(self.jid))
		if self.config.has_key(self.jid) and self.config[self.jid].has_key('long_key_id'):
			self.key_dialog.ui.key_id.setText(self.config[self.jid]['long_key_id'])
		else:
			self.key_dialog.ui.key_id.setText('')
		QtCore.QObject.connect(self.key_dialog,QtCore.SIGNAL("accepted ( )"),self.keyAccepted)

	def buildContactMenu(self,menu,contact):
		self.action=menu.addAction(self.tr("GPG key ID"))
		self.action.setData(QtCore.QVariant(unicode(contact.jid)))
		self.action.setObjectName("key_dialog")
		self.action.setIcon(QtGui.QIcon("%s/kgpg.png" % self.pluginDir))
		QtCore.QObject.connect(self.action,QtCore.SIGNAL("triggered ( bool )"),self.contactMenuToggled)
        
	def contactMenuToggled(self,b):
		"""
		User choose our QAction from contactMenu (menu above contact)
		"""
		jid=unicode(self.action.data().toString())
		log.err(jid)
		self.showSlot(jid)
		self.action.deleteLater()
