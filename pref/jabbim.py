class preferences:
	def __init__(self,preferencesWindow):
		self.config={}
		self.config['startInTray']={'type':'boolean','label':preferencesWindow.tr("Start Jabbim minimalized to the tray"),'value':'False'}
		self.config['notifyOnDND']={'type':'boolean','label':preferencesWindow.tr("Notify when DND status is active"),'value':'True'}
		#self.config['resource']={'type':'text-single','label':preferencesWindow.tr("Resource:"),'value':'jabbim'}
		self.config['autoDownload']={'type':'boolean','label':preferencesWindow.tr("Download incomming files automatically"),'value':'False','groupbox':preferencesWindow.tr('Incoming files'),'enable':['autoDownloadPath']}
		self.config['autoDownloadPath']={'type':'directory','label':preferencesWindow.tr("Path for automatic download:"),'value':'','groupbox':preferencesWindow.tr('Incoming files')}
		self.config['autoPriority']={'type':'boolean','label':preferencesWindow.tr("Set priority according to status"),'value':'True','groupbox':preferencesWindow.tr('Priority'),'disable':['priority'],'enable':['autoPriority_chat','autoPriority_online','autoPriority_away','autoPriority_xa','autoPriority_dnd']}
		self.config['priority']={'type':'number-spin','label':preferencesWindow.tr("Priority:"),'value':'0','groupbox':preferencesWindow.tr('Priority')}
		self.config['autoPriority_chat']={'type':'number-spin','label':preferencesWindow.tr("Chat:"),'value':'25','groupbox':preferencesWindow.tr('Priority'),'min':'-128','max':'128'}
		self.config['autoPriority_online']={'type':'number-spin','label':preferencesWindow.tr("Online:"),'value':'20','groupbox':preferencesWindow.tr('Priority'),'min':'-128','max':'128'}
		self.config['autoPriority_away']={'type':'number-spin','label':preferencesWindow.tr("Away:"),'value':'15','groupbox':preferencesWindow.tr('Priority'),'min':'-128','max':'128'}
		self.config['autoPriority_xa']={'type':'number-spin','label':preferencesWindow.tr("Extended away:"),'value':'10','groupbox':preferencesWindow.tr('Priority'),'min':'-128','max':'128'}
		self.config['autoPriority_dnd']={'type':'number-spin','label':preferencesWindow.tr("DND:"),'value':'5','groupbox':preferencesWindow.tr('Priority'),'min':'-128','max':'128'}
		self.config['__sort__']=['startInTray','notifyOnDND','autoDownload','autoDownloadPath','autoPriority','priority','autoPriority_chat','autoPriority_online','autoPriority_away','autoPriority_xa','autoPriority_dnd']