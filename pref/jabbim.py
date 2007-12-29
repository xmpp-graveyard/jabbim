class preferences:
	def __init__(self,preferencesWindow):
		self.config={}
		self.config['saveGeometry']={'type':'boolean','label':preferencesWindow.tr("Save Jabbim position on close"),'value':'True'}
		self.config['autoDownload']={'type':'boolean','label':preferencesWindow.tr("Download incomming files automatically"),'value':'False','groupbox':preferencesWindow.tr('Incoming files')}
		self.config['autoDownloadPath']={'type':'text-single','label':preferencesWindow.tr("Path for automatic download:"),'value':'','groupbox':preferencesWindow.tr('Incoming files')}
		self.config['__sort__']=['saveGeometry','autoDownload','autoDownloadPath']