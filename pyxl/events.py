from twisted.python import log
class EventDispatcher:
	def __init__(self, prefix="event_"):
		self.prefix = prefix
		self.callbacks = {}


	def registerHandler(self, name, meth, hname = 'nic'):
		self.callbacks.setdefault(name, {})[hname] = meth
	
	def unregisterHandler(self, name, hname):
		try:
			del self.callbacks[name][hname]
		except:
			pass

	def publishEvent(self, name, *args, **kwargs):
		if self.callbacks.has_key(name):
			for cb in self.callbacks[name].itervalues():
				try:
					cb(*args, **kwargs)
				except Exception, ex:
					log.msg('Plugin error: ' +unicode(ex))
