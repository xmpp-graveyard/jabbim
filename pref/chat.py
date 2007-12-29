class preferences:
	def __init__(self,preferencesWindow):
		self.config={}
		self.config['sendByCtrl']={'type':'boolean','label':preferencesWindow.tr("Sends messages with ctrl+enter."),'value':'False'}
		self.config['showChatStatusChanges']={'type':'boolean','label':preferencesWindow.tr("Show status message."),'value':'True','groupbox':preferencesWindow.tr('Normal chat')}
		self.config['useMUCNames']={'type':'boolean','label':preferencesWindow.tr("Use names for tabs."),'value':'True','groupbox':preferencesWindow.tr('Groupchat')}
		self.config["askBeforeQuitMUC"]={'type':'boolean','label':preferencesWindow.tr("Ask before quit room."),'value':'True','groupbox':preferencesWindow.tr('Groupchat')}