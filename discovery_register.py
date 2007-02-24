try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

class discoveryRegisterWindow(QtGui.QDialog):
	def __init__(self,main,jab,form,jid,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.main=main
		self.jab=jab
		self.form=form
		self.jid=jid
		self.setModal(True)
		self.widgets={}
		self.labels=[]
		self.layout=QtGui.QVBoxLayout(self)
		self.layout.setMargin(1)
		self.layout.setSpacing(1)
		widget=QtGui.QWidget(self)
		layout=QtGui.QHBoxLayout(widget)
		layout.setMargin(1)
		layout.setSpacing(1)
		self.acp=QtGui.QPushButton(self.tr("OK"),widget)
		self.rej=QtGui.QPushButton(self.tr("Cancel"),widget)
		QtCore.QObject.connect(self.acp,QtCore.SIGNAL("clicked()"),self.accept)
		QtCore.QObject.connect(self.rej,QtCore.SIGNAL("clicked()"),self.reject)
		layout.addWidget(self.rej)
		layout.addWidget(self.acp)
		self.layout.addWidget(widget)
		print self.jid

		print unicode(self.form)
		for i in self.form.getPayload():
			print unicode(i.getName())
			if i.getName()=="title":
				self.addTitle(i.getData())
			elif i.getName()=="instructions":
				self.addInstructions(i.getData())
			elif i.getName()=="field":
				attrs=i.getAttrs()
				print unicode(attrs)
				lab=attrs["var"]
				if attrs.has_key("label"):
					lab=attrs["label"]
				if attrs["type"]=="text-single":
					self.addTextSingle(attrs["var"],lab)
				elif attrs["type"]=="text-private":
					self.addTextSingle(attrs["var"],lab,True)
				elif attrs["type"]=="boolean":
					self.addBoolean(attrs["var"],lab)
				elif attrs["type"]=="list-single":
					values={}
					for x in i.getChildren():
						if x.getName()=="option":
							label=x.getAttr("label")
							value=x.getChildren()[0].getData()
							values[label]=value
					self.addlistSingle(attrs["var"],lab,values)

	def accept(self):
		info={}
		for k,v in self.widgets.iteritems():
			if v.typ=="checkbox":
				bool=v.isChecked()
				value=0
				if bool==True:
					value=1
				info[k]=unicode(value)
			elif v.typ=="combobox":
				data=v.itemData(v.currentIndex())
				data=data.toString()
				info[k]=unicode(data)
			elif v.typ=="lineedit":
				info[k]=unicode(v.text())
		print unicode(info)
		self.jab.register(self.jid,info)
		self.done(1)

	def addBoolean(self,var,label):
		self.widgets[var]=QtGui.QCheckBox(label,self)
		self.widgets[var].typ="checkbox"
		self.layout.addWidget(self.widgets[var])

	def addlistSingle(self,var,label,values):
		widget=QtGui.QWidget(self)
		layout=QtGui.QHBoxLayout(widget)
		layout.setMargin(1)
		layout.setSpacing(1)

		self.labels.append(QtGui.QLabel(widget))
		self.labels[-1].setText(unicode(label)+":")
		self.widgets[var]=QtGui.QComboBox(widget)
		self.widgets[var].typ="combobox"
		for k,v in values.iteritems():
			self.widgets[var].addItem(k,QtCore.QVariant(v))

		layout.addWidget(self.labels[-1])
		layout.addWidget(self.widgets[var])
		self.layout.addWidget(widget)

	def addTextSingle(self,var,label,private=False):
		widget=QtGui.QWidget(self)
		layout=QtGui.QHBoxLayout(widget)
		layout.setMargin(1)
		layout.setSpacing(1)

		self.labels.append(QtGui.QLabel(widget))
		self.labels[-1].setText(unicode(label)+":")
		self.widgets[var]=QtGui.QLineEdit(widget)
		self.widgets[var].typ="lineedit"
		if private==True:
			self.widgets[var].setEchoMode(QtGui.QLineEdit.Password)

		layout.addWidget(self.labels[-1])
		layout.addWidget(self.widgets[var])
		self.layout.addWidget(widget)

	def addTitle(self,text):
		self.labels.append(QtGui.QLabel(self))
		self.labels[-1].setText("<h1>"+unicode(text)+"</h1>")
		self.layout.addWidget(self.labels[-1])
		
	def addInstructions(self,text):
		self.labels.append(QtGui.QTextBrowser(self))
		self.labels[-1].setReadOnly(True)
		self.labels[-1].setText(unicode(text))
		self.layout.addWidget(self.labels[-1])