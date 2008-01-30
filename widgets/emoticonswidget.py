"""
Copyright (C) 2007 	Jan 'Hanzz' Kaluza (hanzz at njs.netlab.cz)
Copyright (C) 2007	Jiri 'Sef' Gabrys	(sef at njs.netlab.cz)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
import os
from configobj import ConfigObj

class emoticonsWidget(QtGui.QLabel):
	def __init__(self,main,parent=None):
		apply(QtGui.QLabel.__init__,(self,parent))
		self.setWindowFlags(QtCore.Qt.Popup)
		self.setObjectName('emoticonList')
		self.main=main
		self.acceptor=None
		self.l=[]
		self.emoWidth=None
		self.emoHeight=None
		self.reinit()

	def event(self,event):
		# tooltip request:
		if int(event.type())==110:
			x=event.x()
			y=event.y()
			if x>0 and y>0 and x<self.pixmap.width() and y<self.pixmap.height():
				self.setToolTip(unicode(self.emoticonAt(x,y)))
			else:
				self.setToolTip("")
		return QtGui.QLabel.event(self,event)

	def emoticonAt(self,x,y):
		x=int(x/(self.emoWidth+2))
		y=int(y/(self.emoHeight+2))
		return self.l[y][x]
		
	def mousePressEvent(self,event):
		x=event.x()
		y=event.y()
		if x>0 and y>0 and x<self.pixmap.width() and y<self.pixmap.height():
			x=int(x/(self.emoWidth+2))
			y=int(y/(self.emoHeight+2))
			if self.acceptor:
				self.acceptor.addEmoticon(self.l[y][x])
		if self.acceptor:
			self.acceptor.ui.smileys.setChecked(False)
		self.hide()

	def reinit(self):
		# load emoticons pack
		smileys=ConfigObj("emoticons/"+self.main.config['emoticons'],encoding='UTF8')
		src='emoticons/'
		if len(smileys)==0:
			smileys=ConfigObj(self.main.realHomeDir+"/emoticons/"+self.main.config['emoticons'],encoding='UTF8')
			src=self.main.realHomeDir+'/emoticons/'
		if len(smileys)==0:
			# emotions pack doesn't exist
			return

		# load images
		self.smileys={} #: images for emoticons. for example {":-)":"emoticons/default/smile.png"}
		for k,v in smileys['emoticons'].iteritems():
			self.smileys[k.replace("<","&lt;").replace(">","&gt;")]=src+os.path.dirname(self.main.config['emoticons'])+"/"+v
		
		added=[]
		x=0
		y=0
		# make QToolButton for every image, add it to layout of self.s, and connnect to self.addEmotion
		self.emoWidth=None
		self.emoHeight=None
		self.l=[[]]
		for k,v in smileys['emoticons'].iteritems():
			if added.count(v)==0:
				added.append(v)
				if not self.emoWidth:
					p=QtGui.QPixmap(src+os.path.dirname(self.main.config['emoticons'])+"/"+v)
					self.emoWidth=int(p.width())
					self.emoHeight=int(p.height())
				self.l[-1].append(unicode(k))
				y+=1
				if y==6:
					self.l.append([])
					y=0
					x+=1
		width=6*(self.emoWidth+2)
		height=(x+1)*(self.emoHeight+2)
		# make QFrame for images preview
		self.pixmap=QtGui.QPixmap(width,height)
		self.pixmap.fill(self.palette().base().color())
		added=[]
		x=0
		y=0
		painter=QtGui.QPainter(self.pixmap)
		# make QToolButton for every image, add it to layout of self.s, and connnect to self.addEmotion
		for k,v in smileys['emoticons'].iteritems():
			print k
			if added.count(v)==0:
				added.append(v)
				p=QtGui.QPixmap(src+os.path.dirname(self.main.config['emoticons'])+"/"+v)
				em=p.scaled(self.emoWidth,self.emoHeight,QtCore.Qt.KeepAspectRatio)
				painter.drawPixmap(y*self.emoWidth+y*2,x*self.emoHeight+x*2,em)
				y+=1
				if y==6:
					y=0
					x+=1
		painter.end()
		self.setPixmap(self.pixmap)