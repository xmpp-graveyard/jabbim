class Contact:
	def __init__(self, jid, name, subscription, items=[], groups = [], status = ()):
		self.jid = jid
		self.name = name
		self.subscription = subscription
		self.groups = groups
		self.status = status
		self.rosterItems = items # user can be in many groups => more items
		self.resources={} #resource:(show,status,priority)

	def setStatus(self, resource, show, status):
		if self.resources.has_key(resource):
			self.resources[resource] = {'show': show, 'status': status}
		else:
			self.resources[resource] = {'show': show, 'status': status, 'priority' : 0}
		if resource == self.getHighestResource():
			self.status = (show, status)
			
	def setPriority(self, resource, priority):
		if self.resources.has_key(resource):
			self.resources[resource]['priority'] = priority
		else:
			self.resources[resource] = {'show': None, 'status': '', 'priority' : priority}
			
	def getHighestResource(self):
		prio = None
		highest = None
		for res,val in self.resources.iteritems():
##			print val
			if val.has_key('priority') :
				if val['priority']>prio:
					highest = res
					prio = val['priority']
		return highest

	def getUserItems(self):
		# get user QTreeWidget item from every group
		return self.rosterItems
		
##class Resource:
##	def __init__(self, name, priority, show, status):
##		self.name = name
##		self.priority = priority
##		self.show = show
##		self. status = status
##		self.features = []
