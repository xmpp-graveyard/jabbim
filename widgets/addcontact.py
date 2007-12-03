import os
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from addcontact_ui import *
from search import *

class addContactDialog(QtGui.QDialog):
	def __init__(self,main,parent=None,jid="",group=None,name="",add=True):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(False)
		self.ui=Ui_addContact()
		self.ui.setupUi(self)
		self.main=main
		self.add=add
		for k,v in self.main.client.roster['groups'].iteritems():
			if k==group:
				self.ui.add_group.insertItem(0,unicode(k))
			else:
				self.ui.add_group.addItem(unicode(k))
		self.ui.add_group.setCurrentIndex(0)
		self.ui.add_nickname.setText(unicode(name))
		self.ui.add_jid.setText(unicode(jid))
		if not self.add:
			self.ui.add_jid.setEnabled(False)
			self.ui.add_message.hide()
			self.ui.add_messageLabel.hide()
		QtCore.QObject.connect(self.ui.search,QtCore.SIGNAL("clicked()"),self.search)

		self.searchJid=None
		#key=self.main.client.jid.host
		#print key,self.main.client.disco.keys()
		for key in self.main.client.disco.keys():
			#if self.main.client.disco[key][None].has_key("identities"):
				##for identity,values in self.main.client.disco[key][None].iteritems():
					#if values.has_key('category'):
						#pass
			got=False
			if self.main.client.disco[key][None].has_key("identities"):
				for identity in self.main.client.disco[key][None]["identities"].itervalues():
					if identity['category']=="directory" and identity['type']=='user':
						got=True
			if self.main.client.disco[key][None].has_key("features") and got:
				if "jabber:iq:search" in list(self.main.client.disco[key][None]['features']):
					#print self.main.client.disco[key]
					self.searchJid=unicode(key)
		print 'searchJid',self.searchJid
		if not self.searchJid:
			self.ui.search.hide()

	def search(self):
		d=self.main.client.getSearchForm(self.searchJid)
		d.addCallback(self._gotSearchForm)
		
	def _gotSearchForm(self,data):
		if not data:
			return
		jid,legacy,form=data
		if form!=None:
			self.dialog=searchDialog(self.main,jid,form,self)
			self.dialog.show()


		
	def accept(self):
		jid=unicode(self.ui.add_jid.text())
		nickname=unicode(self.ui.add_nickname.text())
		group=unicode(self.ui.add_group.currentText())
		message=unicode(self.ui.add_message.toPlainText())
		if self.add:
			self.main.client.addContact(jid,message,nickname,[group])
		else:
			contact=self.main.client.roster['users'][jid]
			self.main.client.sendRosterUpdate(jid,nickname, contact.subscription, [group])


		self.done(1)
