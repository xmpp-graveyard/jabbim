import help
class preferences:
	def __init__(self,preferencesWindow):
		self.config={}
		self.config['allowChatstate']={'type':'boolean','label':preferencesWindow.tr("Send chatstate notifications."),'value':'True'}
		self.config['sendOSInfo']={'type':'boolean','label':preferencesWindow.tr("Send OS info."),'value':'True'}
