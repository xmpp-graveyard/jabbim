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

from twisted.enterprise import adbapi, util as dbutil
from twisted.python import log
from twisted.internet.defer import DeferredList
class Cache:
	def __init__(self, DB_DRIVER = 'sqlite3', db='cache.db'):
		if DB_DRIVER == 'sqlite3':
			try:
				self.db = adbapi.ConnectionPool(DB_DRIVER, db)
			except ImportError:
				self.db = adbapi.ConnectionPool('pysqlite2.dbapi2', db)
			except:
				log.msg('Unknown DB error')
				
	def create_tables(self):				
		t1 = self.db.runQuery('create table caps (node text, feature text);').addCallback(self.table_created).addErrback(self.table_present)
		t2 = self.db.runQuery('create table status (show text, desc text, id integer primary key);').addErrback(self.table_present)
		t3 = self.db.runQuery('create table avatars (file text, hash text, jid text);').addCallback(self.table_created2).addErrback(self.table_present)
		return DeferredList([t1,t2,t3], consumeErrors = True)
		
	def table_created(self, res):
		log.msg( 'created new cache DB')
# 		self.db.runOperation('create table caps (node text, feature text);')
		#self.db.runQuery('create table avatars (file text, hash text, jid text);').addCallback(self.table_created2).addErrback(self.table_present)
	
	def table_created2(self, res):
		print 'avatars created'
		#self.db.runQuery('create table status (show text, desc text, id int auto_increment primary key);').addErrback(self.table_present)
		
	def table_present(self, result):
		log.msg( 'table here? ')
		print result
	
	def get_avatar(self, jid, handler):
		self.db.runQuery('select file, hash, jid from avatars where jid = "%s"'%(dbutil.safe(jid),)).addCallback(self.got_avatar, handler)

	
	def got_avatar(self, result, handler):
		for x in result:
			handler(x[0], x[1], x[2])

	def set_avatar(self, jid, avatar): #avatar = (file,hash)
		log.msg('ukladam ' + jid)
		self.db.runQuery('select jid from avatars where jid = "%s"'%(dbutil.safe(jid),)).addCallback(self._has_avatar, jid, avatar)

	
	def _has_avatar(self, result, jid, avatar):
		if len(result)==0:
			self.db.runOperation('insert into avatars (jid, file, hash) values("%s","%s","%s")'%(dbutil.safe(jid), dbutil.safe(avatar[0]), avatar[1]))
		else:
			self.db.runOperation('update avatars set file="%s", hash="%s" where jid="%s"'%(dbutil.safe(avatar[0]), avatar[1], dbutil.safe(jid)))
	
	def set_caps(self, node, features):
		for feature in features:
			self.db.runOperation('insert into caps (node, feature) values ("%s", "%s")'%(node, feature))
	
	def get_caps(self, cb):
		self.db.runQuery('select * from caps;').addCallback(self._got_caps, cb)
	
	def _got_caps(self, result, cb):
		cb(result)
	
	def get_status(self):
		return self.db.runQuery('select * from status;')
	
	def get_status_by_id(self,id):
		return self.db.runQuery('select * from status where id = %s'%id)
	
	def del_status(self, id):
		return self.db.runOperation('delete from status where id = %s'%id)

	def set_status(self, show, message):
		message=message.replace("'","''")
		return self.db.runOperation('insert into status (show, desc,id) values ("%s", "%s",NULL)'%(show, message))
	
	def update_status(self,show,message,ID):
		return self.db.runOperation('update status set show="%s", desc="%s" where id=%s'%(dbutil.safe(show), dbutil.safe(message), str(ID)))

	
	def close(self):
		self.db.close()

		
