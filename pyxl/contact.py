class Contact:
	def __init__(self, client, jid, name, subscription, items=[], groups = [], status = (),  tag = None,  order = 1):
		self.jid = jid
		self.name = name
		self.subscription = subscription
		self.groups = groups
		self.status = status
		self.rosterItems = items # user can be in many groups => more items
		self.resourcesItems={}
		self.metaItems=[]
		self.resources={} #resource:(show,status,priority)
		self.client = client
		self.tag = tag
		self.order = order


	def setStatus(self, resource, show, status):
		first = False
		if self.resources.has_key(resource):
			self.resources[resource].show = show
			self.resources[resource].status =  status
		elif self.resources.has_key(resource) and show == 'offline':
			del self.resources[resource]
			return
		else:
			self.resources[resource] = Resource(self, resource, show = show, status = status, priority = 0)
			first = True
		if resource == self.getHighestResource():
			self.status = (show, status)
		return first
##	def getResource(self, resource):
##		resource = False
##		for res in self.resources:
##			if res.name == resource:
##				resource = res
##		return resource
	
	def setPriority(self, resource, priority):
		if self.resources.has_key(resource):
			self.resources[resource].priority =priority
		else:
			self.resources[resource] = Resource(self, resource, priority = priority)
			
	def setFeatures(self, resource, features):
		if self.resources.has_key(resource):
			self.resources[resource].features = features
		else:
			self.resources[resource] = Resource(self, resource)
			self.resources[resource].features = features
			
	def getHighestResource(self):
		prio = None
		highest = self.resources.keys()[0]
		for res,val in self.resources.iteritems():
##			print val
				if val.priority>prio:
					highest = res
					prio = val.priority
		return highest

	def getUserItems(self):
		# get user QTreeWidget item from every group
		return self.rosterItems
		
class Resource:
	def __init__(self, contact, name, priority=0, show='offline', status=''):
		self.name = name
		self.priority = priority
		self.show = show
		self. status = status
		self.features = []
		self.contact = contact
	
	def hasFeature(self, feature):
		if feature in self.features:
			return True
		else:
			return False
