class preferences:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['saveGeometry']={'type':'boolean','label':self.main.tr("Save Jabbim position on close"),'value':'True'}
		self.config['autoDownload']={'type':'boolean','label':self.main.tr("Download incomming files automatically"),'value':'False','groupbox':self.main.tr('Incoming files')}
		self.config['autoDownloadPath']={'type':'text-single','label':self.main.tr("Path for automatic download:"),'value':'','groupbox':self.main.tr('Incoming files')}
		self.config['__sort__']=['saveGeometry','autoDownload','autoDownloadPath']