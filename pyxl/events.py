class EventDispatcher:
	def __init__(self, prefix="event_"):
		self.prefix = prefix
		self.callbacks = {}


	def registerHandler(self, name, meth):
		self.callbacks.setdefault(name, []).append(meth)


	def publishEvent(self, name, *args, **kwargs):
		if self.callbacks.has_key(name):
			for cb in self.callbacks[name]:
				cb(*args, **kwargs)
