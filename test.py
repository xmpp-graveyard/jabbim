import pynotify
if pynotify.init("My Application Name"):
	n = pynotify.Notification("Title", "message")
	n.show()
