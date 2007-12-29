class preferences:
	def __init__(self,preferencesWindow):
		self.config={}
		self.config['passwd']={'type':'text-private','label':preferencesWindow.tr("Password:"),'value':'','groupbox':preferencesWindow.tr('Connection')}
		self.config['jid']={'type':'text-single','label':preferencesWindow.tr("Jabber ID:"),'value':'','groupbox':preferencesWindow.tr('Connection')}
		self.config['autoJoin']={'type':'boolean','label':preferencesWindow.tr("Automatically join at startup."),'value':'False','groupbox':preferencesWindow.tr('Connection')}
		self.config['resource']={'type':'text-single','label':preferencesWindow.tr("Resource:"),'value':'jabbim','groupbox':preferencesWindow.tr('Advanced')}
		self.config['priority']={'type':'number-spin','label':preferencesWindow.tr("Priority:"),'value':'0','groupbox':preferencesWindow.tr('Advanced')}
		self.config['autoPriority']={'type':'boolean','label':preferencesWindow.tr("Change priority automatically due to status."),'value':'True','groupbox':preferencesWindow.tr('Advanced'),'column':'right'}
