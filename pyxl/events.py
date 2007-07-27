from twisted.python import log
class EventDispatcher:
	def __init__(self, prefix="event_"):
		self.prefix = prefix
		self.callbacks = {}


	def registerHandler(self, name, meth, hname = 'nic', priority = 5):
		self.callbacks.setdefault(name, {})[hname] = {'method':meth, 'prio':priority}
	
	def unregisterHandler(self, name, hname):
		try:
			del self.callbacks[name][hname]
		except:
			pass

	def publishEvent(self, name, *args, **kwargs):
		if self.callbacks.has_key(name):
			seznam = self.callbacks[name].itervalues()
			serazeno = sorted(seznam, key = self.k)
			for cb in serazeno:
				try:
					vysl = cb['method'](*args, **kwargs)
					if vysl == False:
						return
				except Exception, ex:
					log.msg('Plugin error: ' +unicode(ex))
	
	def k(self, key):
		return key['prio']
