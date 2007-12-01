class preferences:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['sendByCtrl']={'type':'boolean','label':self.main.tr("Sends messages with ctrl+enter."),'value':'False'}
		self.config['showChatStatusChanges']={'type':'boolean','label':self.main.tr("Show status message."),'value':'True','groupbox':self.main.tr('Normal chat')}
		self.config['useMUCNames']={'type':'boolean','label':self.main.tr("Use names for tabs."),'value':'True','groupbox':self.main.tr('Groupchat')}
		self.config["askBeforeQuitMUC"]={'type':'boolean','label':self.main.tr("Ask before quit room."),'value':'True','groupbox':self.main.tr('Groupchat')}