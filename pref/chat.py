class preferences:
	def __init__(self,preferencesWindow):
		self.config={}
		self.config['sendByCtrl']={'type':'boolean','label':preferencesWindow.tr("Sends messages with ctrl+enter."),'value':'False'}
		self.config['showChatStatusChanges']={'type':'boolean','label':preferencesWindow.tr("Show status message."),'value':'True','groupbox':preferencesWindow.tr('Normal chat')}
		self.config["showMoodChanges"]={'type':'boolean','label':preferencesWindow.tr("Show messages about users mood."),'value':'True','groupbox':preferencesWindow.tr('Normal chat')}
		self.config["showTuneChanges"]={'type':'boolean','label':preferencesWindow.tr("Show messages about user tune."),'value':'True','groupbox':preferencesWindow.tr('Normal chat')}
		self.config['useMUCNames']={'type':'boolean','label':preferencesWindow.tr("Use names for tabs."),'value':'True','groupbox':preferencesWindow.tr('Groupchat')}
		self.config["askBeforeQuitMUC"]={'type':'boolean','label':preferencesWindow.tr("Ask before quit room."),'value':'True','groupbox':preferencesWindow.tr('Groupchat')}
		self.config["autochangenickMUC"]={'type':'boolean','label':preferencesWindow.tr("Auto change nick if nick conflict join to room"),'value':'True','groupbox':preferencesWindow.tr('Groupchat')}
