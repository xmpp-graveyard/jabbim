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
		self.db.runQuery('select avatar_file, avatar_hash from vcards where jid = "%s"'%jid).addCallback(self.got_avatar, handler)
	
	def got_avatar(self, result, handler):
		for x in result:
			handler(x[0], x[1])
		
