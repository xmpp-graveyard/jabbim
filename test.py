#
import sys
try:
	f=open(sys.argv[1],'r')
except:
	print "can't open file"
	exit()
data=f.read()
f.close()
c=None
for line in data.split('\n'):
	if line.find("self.retranslateUi")!=-1:
		# self.retranslateUi(MainWindow)
		try:
			line=line.split("(")[1]
			c=line[:-1]
			print "class name:",c
		except:
			print "can't find class name"
			exit()
		break
print "replacing QtGui.QApplication.translate to "+c+"._translate"
data=data.replace("QtGui.QApplication.translate",c+"._translate")
f=open(sys.argv[1],'w')
f.write(data)
f.close()
print "done"