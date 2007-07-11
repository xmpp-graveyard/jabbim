from twisted.internet import reactor
import pyxl

class uiClass:
	def _connected(self):
		print 'we are connected'
	
	def _addGroup(self, group):
		print 'add group to roster'
	
	def _addUser(self, itemjid, name, grp):
		print ' add user'

class testClass(pyxl.client.Client):
	def on_xml(self, xml):
##		print xml
		pass
	def on_authd(self):
		print 'we are authed now'
		self.joinGC('robots@conf.netlab.cz',  'Vybliz')
		self.factory.stopFactory()

klient = testClass('vybliz@njs.netlab.cz/test', 'da_heslo', 'njs.netlab.cz', 5222, uiClass())
klient.connect()
reactor.run()
