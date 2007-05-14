class derived:
	def on_authFailed(self,xmlstream):
		pass
	def on_init(self):
		pass
	def on_presence(self,frm,show):
		pass
	def on_firstpresence(self,  bulk):
		for pres in bulk:
			print pres[0], pres[1]
			self.on_presence(pres[0], pres[1])
		pass
	def on_shutdown(self):
		pass
	def on_xml(self, xml):
		pass
	def on_metaFail(self, err):
		pass
	def on_UpdateContact(self,jid):
		pass
	def on_DeleteContact(self,jid):
		pass
	
	def on_subscribe(self, msg):
		pass
	def on_unsubscribe(self):
		pass
	def on_unsubscribed(self):
		pass
	def on_subscribed(self):
		pass
	
	def on_message(self, frm, typ, body, subject = None, xhtml = None,  chatstate = None,  delay = None):
		pass
	def on_GCmessage(self, frm, typ, body, subject = None, xhtml = None,  chatstate = None,  delay = None):
		pass
	
	def on_GCpresence(self,  muc, nick,  show,  status,  codes = []):
		pass
	
	def on_versionreceive(self, jid, version):
		#version = (name, version, os)
		pass
	
	def on_discoInfoReceived(self, jid, node):
		# v self.disco[jid][node] jsou info data nebo error
		pass
	def on_discoItemsReceived(self, jid, node):
		# v self.disco[jid][node] jsou info data nebo error
		pass
	
	def on_privacyReceived(self):
		print self.privacy_lists
		pass

	def on_time202Received(self, jid, utc, tzo):
		pass
	
	def on_rosterAddUser(self, contact):
		pass
	
	def on_rosterArrived(self):
		pass
	
	def on_roleErr(self,  muc,  err,  nick):
		pass
	
	def on_affiliationErr(self,  muc,  err,  nick):
		pass
