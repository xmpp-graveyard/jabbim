class preferences:
	def __init__(self,preferencesWindow):
		self.config={}
		self.config['showTransports']={'type':'boolean','label':preferencesWindow.tr('Show transports'),'value':'False'}
		self.config['rosterScrollBar']={'type':'boolean','label':preferencesWindow.tr('Display scroll bar'),'value':'True',"category":"advanced"}
		self.config['__sort__']=['showTransports','rosterScrollBar']
