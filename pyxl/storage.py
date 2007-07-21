##DB_DRIVER = "MySQLdb"
##DB_ARGS = {
##    'db': 'rss',
##    'user': 'root',
##    'passwd': '',
##    }
from twisted.enterprise import adbapi, util as dbutil
from twisted.python import log

##class Log:
##	def msg(self, zprava):
##		pass
##	def err(self, zprava):
##		pass
##
##log = Log()	

class Cache:
	def __init__(self, DB_DRIVER = 'sqlite3', db='cache.db'):
		if DB_DRIVER == 'sqlite3':
			try:
				self.db = adbapi.ConnectionPool(DB_DRIVER, db)
			except ImportError:
				self.db = adbapi.ConnectionPool('pysqlite2.dbapi2', db)
			except:
				log.msg('Unknown DB error')
		q = self.db.runQuery('create table avatars (file text, hash text, jid text);').addCallback(self.table_created)
		q.addErrback(self.table_present)
		
	def table_created(self, res):
		log.msg( 'created new cache DB')
	
	def table_present(self, result):
		log.msg( 'table here? '+unicode( result))
	
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

		
