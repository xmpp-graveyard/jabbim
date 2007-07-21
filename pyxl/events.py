class EventDispatcher:
	def __init__(self, prefix="event_"):
		self.prefix = prefix
		self.callbacks = {}


	def registerHandler(self, name, meth, hname = 'nic'):
		self.callbacks.setdefault(name, {})[hname] = meth
	
	def unregisterHander(self, name, hname):
		try:
			del self.callbacks[name][hname]
		except:
			pass

	def publishEvent(self, name, *args, **kwargs):
		if self.callbacks.has_key(name):
			for cb in self.callbacks[name].itervalues():
				cb(*args, **kwargs)
