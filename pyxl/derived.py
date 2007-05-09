class derived:
	def on_authFailed(self,xmlstream):
		pass
	def on_init(self):
		pass
	def on_presence(self,frm,show):
		pass
	def on_shutdown(self):
		pass
	def on_xml(self, xml):
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
	
	def on_message(self, frm, typ, body, subject = None):
		pass
	
	def on_versionreceive(self, jid, version):
		#version = (name, version, os)
		pass
