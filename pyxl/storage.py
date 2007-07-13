##DB_DRIVER = "MySQLdb"
##DB_ARGS = {
##    'db': 'rss',
##    'user': 'root',
##    'passwd': '',
##    }
from twisted.enterprise import adbapi, util as dbutil

class Cache:
	def __init__(self, DB_DRIVER = 'sqlite3', db='cache.db'):
		self.db = adbapi.ConnectionPool(DB_DRIVER, db)

		q = self.db.runQuery('create table avatars (file text, hash text, jid text);').addCallback(self.table_created)
		q.addErrback(self.table_present)
		
	def table_created(self, res):
		print 'created new cache DB'
	
	def table_present(self, result):
		print 'table here? ', result
	
	def get_avatar(self, jid, handler):
		self.db.runQuery('select file, hash, jid from avatars where jid = "%s"'%dbutil.safe(jid)).addCallback(self.got_avatar, handler)
	
	def got_avatar(self, result, handler):
		for x in result:
			handler(x[0], x[1], x[2])

	def set_avatar(self, jid, avatar): #avatar = (file,hash)
		print 'ukladam ', jid
		self.db.runQuery('select jid from avatars where jid = "%s"'%dbutil.safe(jid)).addCallback(self._has_avatar, jid, avatar)
	
	def _has_avatar(self, result, jid, avatar):
		if len(result)==0:
			self.db.runOperation('insert into avatars (jid, file, hash) values("%s","%s","%s")'%(dbutil.safe(jid), dbutil.safe(avatar[0]), avatar[1]))
		else:
			self.db.runOperation('update avatars set file="%s", hash="%s" where jid="%s"'%(dbutil.safe(avatar[0]), avatar[1], dbutil.safe(jid)))
		
