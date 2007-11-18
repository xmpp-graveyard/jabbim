#-*-encoding:UTF-8-*-

from xdata import *
from adhoc import Stage, CancelStage
from twisted.python import log

class fSetStatus(Stage):
	def exec_(self):
		self.status = "executing"
		self.actions = {"cancel":CancelStage, "complete":SetStatus, "execute":SetStatus}
		self.execute = "complete"
	
		sc = self.main.client.roster['users'][self.main.client.jid.userhost()].resources[self.main.client.jid.resource]
		sshow = sc.show
		if sshow == "online":
			sshow = "available"
		show = Field("show", "list-single", self.main.tr("Show: "), options=[
			[self.main.status[status], status] for status in ["available","chat","away","xa","dnd","offline"]
				], values = [sshow])
		status = Field("status", "text-multi", self.main.tr("Status message: "), values = [sc.status or u""])
		priority = Field("priority", "text-single", self.main.tr("Priority"), values = [sc.priority])

		self.xform = Xform("form",fields=[show,status,priority]).buildElement()

class SetStatus(Stage):
	def exec_(self):
		self.status = "completed"
		self.actions = {}
		
		typ = None
		show = self.data["show"][0]
		if show =="available":
			show = None
			typ = show
			self.data["show"][0] = "online"
		if show == "offline":
			show = None
			typ = "unavailable"

		self.main.client.sendPresence(
				typ = typ,
				show = show,
				status = self.data["status"][0],
				priority = self.data["priority"][0],
				)
		icon = self.main.getIcon(self.data["show"][0], size="16x16")
		self.main.ui.statusButton.setIcon(self.main.getIcon(status=self.data["show"][0], size="16x16"))
		self.main.ui.showWidget.setText(unicode(self.data["status"][0]))
		
		sc = self.main.client.roster['users'][self.main.client.jid.userhost()].resources[self.main.client.jid.resource]
		sc.show = self.data["show"][0]

		self.xform = Xform("result", instructions=[self.main.tr("Status changed.")]).buildElement()

class fLeaveGC(Stage):
	def exec_(self):
		self.status = "executing"
		self.actions = {"cancel":CancelStage, "complete":LeaveGC, "execute":LeaveGC}
		self.execute = "complete"

		gcop = [[key, key] for key in self.main.client.groupchats.keys()]
		
		field = Field("groupchats", "list-multi", self.main.tr("Groupchats to leave: "), options=gcop)
		self.xform = Xform("form", fields=[field], title=self.main.tr("Leave groupchats"),instructions=[self.main.tr("Choose groupchats you want remote client to leave.")]).buildElement()

class LeaveGC(Stage):
	def exec_(self):
		self.status = "completed"
		self.actions = {}
		
		for gc in self.data["groupchats"]:
			tab,index=self.main.chat.findTab(gc) 
			if tab != None:
				self.main.chat.ui.chatTab.setCurrentIndex(index) 
				self.main.chat.removeTab()
		self.xform = Xform("result", instructions=[self.main.tr("Groupchats left.")]).buildElement()

