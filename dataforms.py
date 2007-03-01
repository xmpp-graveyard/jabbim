try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

class dataFormsWindow(QtGui.QDialog):
	def __init__(self,main,jab,form,jid,typ="muc#owner",parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.main=main
		self.jab=jab
		self.typ=typ
		self.form=form
		self.jid=jid
		self.setModal(True)
		self.widgets={}
		self.labels=[]
		self.layout=QtGui.QVBoxLayout(self)
		self.layout.setMargin(1)
		self.layout.setSpacing(1)
		print "FORM",unicode(self.form)
		unreg=False
		for i in self.form.getXPayload():
			if not isinstance(i,unicode):
				print unicode(i.getName())
				if i.getName()=="title":
					self.addTitle(i.getData())
				elif i.getName()=="instructions":
					self.addInstructions(i.getData())
				elif i.getName()=="field":
					attrs=i.getAttrs()
					print unicode(attrs)
					lab=None
					if attrs.has_key("var"):
						lab=attrs["var"]
					if lab=="key":
						values=[""]
						for x in i.getChildren():
							if x.getName()=="value":
								if values[0]=="":
									values=[]
								values.append(x.getData())
						self.addKey(values[0])
					elif lab=="registered":
						unreg=True
					else:
						if attrs.has_key("label"):
							lab=attrs["label"]
						if attrs["type"]=="text-single":
							values=[""]
							for x in i.getChildren():
								if x.getName()=="value":
									if values[0]=="":
										values=[]
									values.append(x.getData())
							self.addTextSingle(attrs["var"],lab,values[0])
						elif attrs["type"]=="text-private":
							values=[""]
							for x in i.getChildren():
								if x.getName()=="value":
									if values[0]=="":
										values=[]
									values.append(x.getData())
							self.addTextSingle(attrs["var"],lab,values[0],True)
						elif attrs["type"]=="text-multi":
							values=[""]
							for x in i.getChildren():
								if x.getName()=="value":
									if values[0]=="":
										values=[]
									values.append(x.getData())
							self.addTextMulti(attrs["var"],lab,values[0])
						elif attrs["type"]=="boolean":
							values=[""]
							for x in i.getChildren():
								if x.getName()=="value":
									if values[0]=="":
										values=[]
									values.append(x.getData())
							self.addBoolean(attrs["var"],lab,values[0])
						elif attrs["type"]=="fixed":
							values=[""]
							for x in i.getChildren():
								if x.getName()=="value":
									if values[0]=="":
										values=[]
									values.append(x.getData())
							self.addFixed(values[0])
						elif attrs["type"]=="list-single":
							values={}
							for x in i.getChildren():
								if x.getName()=="option":
									label=x.getAttr("label")
									value=x.getChildren()[0].getData()
									values[label]=value
							self.addlistSingle(attrs["var"],lab,values)

		widget=QtGui.QWidget(self)
		layout=QtGui.QHBoxLayout(widget)
		layout.setMargin(1)
		layout.setSpacing(1)
		self.acp=QtGui.QPushButton(self.tr("Save"),widget)
		self.rej=QtGui.QPushButton(self.tr("Cancel"),widget)
		QtCore.QObject.connect(self.acp,QtCore.SIGNAL("clicked()"),self.accept)
		QtCore.QObject.connect(self.rej,QtCore.SIGNAL("clicked()"),self.reject)
		
		layout.addWidget(self.acp)
		if unreg==True:
			self.unreg=QtGui.QPushButton(self.tr("Unregister"),widget)
			QtCore.QObject.connect(self.unreg,QtCore.SIGNAL("clicked()"),self.unregister)
			layout.addWidget(self.unreg)
		layout.addWidget(self.rej)
		self.layout.addWidget(widget)
		self.resize(1,1)

	def unregister(self):
		self.jab.unregister(self.jid)

	def accept(self):
		info={}
		for k,v in self.widgets.iteritems():
			if k=="key":
				info["key"]=unicode(v)
			else:
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
				elif v.typ=="textbrowser":
					info[k]=unicode(v.toPlainText())
		print unicode(info)
		if self.typ=="muc#owner":
			self.jab.setGroupchatConfig(self.jid,info)
		self.done(1)

	def addKey(self,value):
		self.widgets["key"]=unicode(value)

	def addBoolean(self,var,label,value):
		self.widgets[var]=QtGui.QCheckBox(label,self)
		self.widgets[var].typ="checkbox"
		if int(value)==1:
			self.widgets[var].setChecked(True)
		else:
			self.widgets[var].setChecked(False)
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

	def addTextSingle(self,var,label,value,private=False):
		widget=QtGui.QWidget(self)
		layout=QtGui.QHBoxLayout(widget)
		layout.setMargin(1)
		layout.setSpacing(1)

		self.labels.append(QtGui.QLabel(widget))
		self.labels[-1].setText(unicode(label)+":")
		self.widgets[var]=QtGui.QLineEdit(widget)
		self.widgets[var].typ="lineedit"
		self.widgets[var].setText(unicode(value))
		if private==True:
			self.widgets[var].setEchoMode(QtGui.QLineEdit.Password)

		layout.addWidget(self.labels[-1])
		layout.addWidget(self.widgets[var])
		self.layout.addWidget(widget)

	def addFixed(self,text):
		self.labels.append(QtGui.QLabel(self))
		#self.labels[-1].setReadOnly(True)
		self.labels[-1].setText(unicode(text))
		self.labels[-1].setAlignment(QtCore.Qt.AlignCenter)
		self.labels[-1].setMaximumWidth(400)
		self.layout.addWidget(self.labels[-1],QtCore.Qt.AlignCenter)

	def addTitle(self,text):
		#self.labels.append(QtGui.QLabel(self))
		#self.labels[-1].setText("<h1>"+unicode(text)+"</h1>")
		#self.layout.addWidget(self.labels[-1])
		self.setWindowTitle(unicode(text))
	
	def addTextMulti(self,var,label,value):
		widget=QtGui.QWidget(self)
		layout=QtGui.QHBoxLayout(widget)
		layout.setMargin(1)
		layout.setSpacing(1)

		self.labels.append(QtGui.QLabel(widget))
		self.labels[-1].setText(unicode(label)+":")
		self.widgets[var]=QtGui.QTextBrowser(widget)
		self.widgets[var].typ="textbrowser"
		self.widgets[var].setPlainText(unicode(value))
		self.widgets[var].setReadOnly(False)

		layout.addWidget(self.labels[-1])
		layout.addWidget(self.widgets[var])
		self.layout.addWidget(widget)
		
	def addInstructions(self,text):
		self.labels.append(QtGui.QTextBrowser(self))
		self.labels[-1].setReadOnly(True)
		self.labels[-1].setText(unicode(text))
		#self.labels[-1].setMinimumSize( 100, 40 )
		#self.labels[-1].setSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
		#self.labels[-1].updateGeometry()
		self.layout.addWidget(self.labels[-1])