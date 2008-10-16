try: from PyQt4 import QtCore, QtGui,QtWebKit
except: print "PyQt4 is not installed."
import subprocess
from Queue import *
#p = Popen(cmd, shell=True, bufsize=bufsize,
          #stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)

mutex=QtCore.QMutex()
newWords=QtCore.QWaitCondition()

class spellThread(QtCore.QThread):
	def __init__(self,parent=None):
		QtCore.QThread.__init__(self,parent)
		self.words=Queue()
		self.stopped=False
	
	def run(self):
		self.stopped=False
		#self.words.cle
		aspell = subprocess.Popen(["aspell", "-a", "-l", "en"],
										stdin=subprocess.PIPE,
										stdout=subprocess.PIPE)
		aspell.stdout.readline()
		stopped=False
		while not stopped:
			newWords.wait(mutex)
			mutex.lock()
			try:
				word=unicode(self.words.get())
			except:
				word=None
			mutex.unlock()
			while word:
				if not stopped:
					#msg.decode("utf-8").encode("latin-1")
					aspell.stdin.write(word.decode("utf-8").encode("latin-1")+"\n")
					line=""
					i=0
					while not line:
						i+=1
						if i>4:
							print "something is wrong..."
							break
						line = aspell.stdout.readline().strip()
					# "line",word,[line]
					if line=="*":
						#print word,l,len(word)
						#print line
						mutex.lock()
						#print "+",word
						if not word in self.correctWords:
							self.correctWords.append(word)
						mutex.unlock()
					else:
						mutex.lock()
						#print "-",word
						if not word in self.badWords:
							self.badWords.append(word)
						mutex.unlock()
					self.msleep(20)
					try:
						word=unicode(self.words.get())
					except:
						word=None
				

class highlighter(QtGui.QSyntaxHighlighter):
	def __init__(self,parent=None):
		QtGui.QSyntaxHighlighter.__init__(self,parent)
		self.spellCheckFormat=QtGui.QTextCharFormat()
		self.spellCheckFormat.setUnderlineColor(QtGui.QColor(QtCore.Qt.red))
		self.spellCheckFormat.setUnderlineStyle(QtGui.QTextCharFormat.SpellCheckUnderline)
		self.badWords=[]
		self.correctWords=[]

		self.thread=spellThread(self)
		self.thread.correctWords=self.correctWords
		self.thread.badWords=self.badWords
		self.thread.start()

	def highlightBlock(self,text):
		t=unicode(QtCore.QString(text).simplified())
		l=0
		words=QtCore.QString(t).split(QtCore.QRegExp("([^\\w,^\\\\]|(?=\\\\))+"))
		for w in words:
			word=unicode(w)
			if word in ['']:
				l+=1
				continue
			line=""
			i=0
			mutex.lock()
			if word in self.badWords:
				mutex.unlock()
				l = text.indexOf(QtCore.QRegExp("\\b" + word + "\\b"),0);
				if l>=0:
					self.setFormat(l,len(word),self.spellCheckFormat)
				
			elif word in self.correctWords:
				mutex.unlock()
				pass
			else:
				self.thread.words.put(QtCore.QString(word))
				mutex.unlock()
				newWords.wakeAll()
			l+=1+len(word)

class textEdit(QtGui.QTextEdit):
	def __init__(self,parent=None):
		QtGui.QTextEdit.__init__(self,parent)
		
	

app=QtGui.QApplication([])
w=textEdit()
h=highlighter(w)
w.show()
app.exec_()