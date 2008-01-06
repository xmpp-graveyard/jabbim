class preferences:
	def __init__(self,preferencesWindow):
		self.config={}
		self.config['passwd']={'type':'text-private','label':preferencesWindow.tr("Password:"),'value':'','groupbox':preferencesWindow.tr('Connection')}
		self.config['jid']={'type':'text-single','label':preferencesWindow.tr("Jabber ID:"),'value':'','groupbox':preferencesWindow.tr('Connection')}
		self.config['autoJoin']={'type':'boolean','label':preferencesWindow.tr("Automatically join at startup."),'value':'False','groupbox':preferencesWindow.tr('Connection')}
		self.config['resource']={'type':'text-single','label':preferencesWindow.tr("Resource:"),'value':'jabbim','groupbox':preferencesWindow.tr('Advanced')}
		self.config['priority']={'type':'number-spin','label':preferencesWindow.tr("Priority:"),'value':'0','groupbox':preferencesWindow.tr('Advanced')}
		self.config['specifyHost']={'type':'boolean','label':preferencesWindow.tr("Specify host for connection"),'value':'False','groupbox':preferencesWindow.tr('Advanced'), 'enable': ['connectHost', 'connectPort'], 'column':'right', 'tooltip':preferencesWindow.tr("Enable only if your server has broken DNS SRV record or if you REALLY know what are you doing.")}
		self.config['connectHost']={'type':'text-single','label':preferencesWindow.tr("Host:"),'value':'','groupbox':preferencesWindow.tr('Advanced')}
		self.config['connectPort']={'type':'text-single','label':preferencesWindow.tr("Port:"),'value':'5222','groupbox':preferencesWindow.tr('Advanced')}
		self.config['autoPriority']={'type':'boolean','label':preferencesWindow.tr("Change priority automatically due to status."),'value':'True','groupbox':preferencesWindow.tr('Advanced'),'column':'right'}
		self.config['__sort__'] = ['jid', 'passwd','resource', 'autoJoin', 'autoPriority', 'priority', 'connectHost', 'connectPort', 'specifyHost']
