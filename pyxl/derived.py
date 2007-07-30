"""
Copyright (C) 2007 	Jan 'Hanzz' Kaluza (hanzz at njs.netlab.cz)
Copyright (C) 2007	Jiri 'Sef' Gabrys	(sef at njs.netlab.cz)

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
class derived:
	def on_authFailed(self,xmlstream):
		pass
	def on_init(self):
		pass
	def on_presence(self,frm,show):
		pass
	def on_GCpresenceError(self,  fromjid,  code,  type,  name, text):
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
	def on_authd(self):
		pass
	def on_metaFail(self, err):
		pass
	def on_UpdateContact(self,jid):
		pass
	def on_DeleteContact(self,jid):
		pass
	
	def on_subscribe(self,kdo, msg):
		pass
	def on_unsubscribe(self, kdo):
		pass
	def on_unsubscribed(self, kdo):
		pass
	def on_subscribed(self, kdo):
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
	def on_vcardReceived(self,  jid, card):
		pass
	
	def on_fileReceived(self, jid, file, methods, id):
		pass
	
	def on_ftEnd(self, sid, error = None): #pokud je error None je vse v poradku, jinak strucny popis chyby.
		del self.ft[sid]
	
	def on_ftTransfered(self, sid, bytes): #pocet prenesenych bajtu pro prenos se SID
		pass
		
	def on_disconnect(self):
		pass
	
	def on_verify(self, id, thread, props, frm, typ): #xep0070
		self.replyVerify(id, thread, props, frm, typ, False)
		pass
