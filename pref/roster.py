class preferences:
	def __init__(self,preferencesWindow):
		self.config={}
		self.config['showTransports']={'type':'boolean','label':preferencesWindow.tr('Show transports'),'value':'False'}
		self.config['__sort__']=['showTransports']
