class preferences:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['passwd']={'type':'text-private','label':self.main.tr("Password:"),'value':'','groupbox':self.main.tr('Connection')}
		self.config['jid']={'type':'text-single','label':self.main.tr("Jabber ID:"),'value':'','groupbox':self.main.tr('Connection')}
		self.config['autoJoin']={'type':'boolean','label':self.main.tr("Automatically join at startup."),'value':'False','groupbox':self.main.tr('Connection')}
		self.config['resource']={'type':'text-single','label':self.main.tr("Resource:"),'value':'jabbim','groupbox':self.main.tr('Advanced')}
		self.config['priority']={'type':'number-spin','label':self.main.tr("Priority:"),'value':'0','groupbox':self.main.tr('Advanced')}
		self.config['autoPriority']={'type':'boolean','label':self.main.tr("Change priority automatically due to status."),'value':'True','groupbox':self.main.tr('Advanced'),'column':'right'}
