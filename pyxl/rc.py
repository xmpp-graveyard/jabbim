#-*-encoding:UTF-8-*-

from xdata import *
from adhoc import Stage, CancelStage

class fSetStatus(Stage):
	def exec_(self):
		self.status = "executing"
		self.actions = {"cancel":CancelStage, "complete":SetStatus, "execute":SetStatus}
		self.execute = "complete"
		
		sc = self.main.client.roster['users'][self.main.client.jid.userhost()].resources[self.main.client.jid.resource]
		show = Field("show", "list-single", self.main.tr("Show: "), options=[
			[self.main.status[status], status] for status in ["available","chat","away","xa","dnd","offline"]
				], values = [sc.show])
		status = Field("status", "text-multi", self.main.tr("Status message: "), values = [sc.status or u""])
		priority = Field("priority", "text-single", self.main.tr("Priority"), values = [sc.priority])

		self.xform = Xform("form",fields=[show,status,priority]).buildElement()

class SetStatus(Stage):
	def exec_(self):
		self.status = "completed"
		self.actions = {}

		self.main.client.sendPresence(
				show = self.data["show"],
				status = self.data["status"],
				priority = self.data["priority"],
				)
		self.main.ui.statusButton.setIcon(self.main.getIcon(self.data["show"], size="16x16"))
		self.ui.showWidget.setText(unicode(self.data["status"]))
