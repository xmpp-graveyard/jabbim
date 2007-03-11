##   filetransfer.py 
##
##   Copyright (C) 2004 Alexey "Snake" Nezhdanov
##
##   This program is free software; you can redistribute it and/or modify
##   it under the terms of the GNU General Public License as published by
##   the Free Software Foundation; either version 2, or (at your option)
##   any later version.
##
##   This program is distributed in the hope that it will be useful,
##   but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##   GNU General Public License for more details.

# $Id: filetransfer.py,v 1.6 2004/12/25 20:06:59 snakeru Exp $

"""
This module contains IBB class that is the simple implementation of JEP-0047,
S5B class that is the  implementation of JEP-0065
and SIFileTransfer that is the implmentation of JEP-0096
"""

from protocol import *
from dispatcher import PlugIn
import base64
import os
import features
import socks5
import socket
import si
from si import makeKey

#Events name
SEND_SUCCESS='SUCCESSFULL SEND'
RECEIVE_SUCCESS='SUCCESSFULL RECEIVE'
SEND_ERROR='ERROR ON SEND'
RECEIVE_ERROR='ERROR ON RECEIVE'

NS_PROFILE_TREE_FT='http://jabber.org/protocol/si/profile/tree-transfer'


class IBB(PlugIn):
    """ IBB used to transfer small-sized data chunk over estabilished xmpp connection.
        Data is split into small blocks (by default 3000 bytes each), encoded as base 64
        and sent to another entity that compiles these blocks back into the data chunk.
        This is very inefficiend but should work under any circumstances. Note that 
        using IBB normally should be the last resort.
    """
    def __init__(self):
        """ Initialise internal variables. """
        PlugIn.__init__(self)
        self.DBG_LINE='ibb'
        self._exported_methods=[self.OpenStream,self.SetIBBFileDestination]
        self._streams={}
        self._ampnode=Node(NS_AMP+' amp',payload=[Node('rule',{'condition':'deliver-at','value':'stored','action':'error'}),Node('rule',{'condition':'match-resource','value':'exact','action':'error'})])
        self._fileDestination=dict()

    def plugin(self,owner):
        """ Register handlers for receiving incoming datastreams. Used internally. """
        self._owner.RegisterHandlerOnce('iq',self.StreamOpenReplyHandler) # Move to StreamOpen and specify stanza id
        self._owner.RegisterHandler('iq',self.IqHandler,ns=NS_IBB)
        self._owner.RegisterHandler('message',self.ReceiveHandler,ns=NS_IBB)

        

    def IqHandler(self,conn,stanza):
        """ Handles streams state change. Used internally. """
        typ=stanza.getType()
        self.DEBUG('IqHandler called typ->%s'%typ,'info')
        if typ=='set' and stanza.getTag('open',namespace=NS_IBB): self.StreamOpenHandler(conn,stanza)
        elif typ=='set' and stanza.getTag('close',namespace=NS_IBB): self.StreamCloseHandler(conn,stanza)
        elif typ=='result': self.StreamCommitHandler(conn,stanza)
        elif typ=='error': self.StreamOpenReplyHandler(conn,stanza)
        else: conn.send(Error(stanza,ERR_BAD_REQUEST))
        raise NodeProcessed

    def StreamOpenHandler(self,conn,stanza):
        """ Handles opening of new incoming stream. Used internally. """
        """
<iq type='set' 
    from='romeo@montague.net/orchard'
    to='juliet@capulet.com/balcony'
    id='inband_1'>
  <open sid='mySID' 
        block-size='4096'
        xmlns='http://jabber.org/protocol/ibb'/>
</iq>
"""
        err=None
        sid,blocksize=stanza.getTagAttr('open','sid'),stanza.getTagAttr('open','block-size')
        self.DEBUG('StreamOpenHandler called sid->%s blocksize->%s'%(sid,blocksize),'info')
        try: blocksize=int(blocksize)
        except: err=ERR_BAD_REQUEST
        key=None
        if sid : key=makeKey(sid,stanza.getFrom(),stanza.getTo())

        if not sid or not blocksize: err=ERR_BAD_REQUEST
        #Check if SI has been done before receiving the file
        elif key not in self._fileDestination.keys(): err=ERR_UNEXECTED_REQUEST
        elif sid in self._streams.keys(): err=ERR_UNEXPECTED_REQUEST
        if err: rep=Error(stanza,err)
        else:
            self.DEBUG("Opening stream: id %s, block-size %s"%(sid,blocksize),'info')
            rep=Protocol('iq',stanza.getFrom(),'result',stanza.getTo(),{'id':stanza.getID()})
            self._streams[sid]={'direction':'<'+str(stanza.getFrom()),'block-size':blocksize,'fp':open(self._fileDestination[key],'w'),'seq':0,'syn_id':stanza.getID()}
        conn.send(rep)
        del self._fileDestination[sid]

    def OpenStream(self,sid,to,fp,blocksize=3000):
        """ Start new stream. You should provide stream id 'sid', the endpoind jid 'to',
            the file object containing info for send 'fp'. Also the desired blocksize can be specified.
            Take into account that recommended stanza size is 4k and IBB uses base64 encoding
            that increases size of data by 1/3."""
        if sid in self._streams.keys(): return
        if not JID(to).getResource(): return
        self._streams[sid]={'direction':'|>'+to,'block-size':blocksize,'fp':fp,'seq':0}
        self._owner.RegisterCycleHandler(self.SendHandler)
        syn=Protocol('iq',to,'set',payload=[Node(NS_IBB+' open',{'sid':sid,'block-size':blocksize})])
        self._owner.send(syn)
        self._streams[sid]['syn_id']=syn.getID()
        return self._streams[sid]

    def SendHandler(self,conn):
        """ Send next portion of data if it is time to do it. Used internally. """
        self.DEBUG('SendHandler called','info')
        for sid in self._streams.keys():
            stream=self._streams[sid]
            if stream['direction'][:2]=='|>': cont=1
            elif stream['direction'][0]=='>':
                chunk=stream['fp'].read(stream['block-size'])
                if chunk:
                    datanode=Node(NS_IBB+' data',{'sid':sid,'seq':stream['seq']},base64.encodestring(chunk))
                    stream['seq']+=1
                    if stream['seq']==65536: stream['seq']=0
                    conn.send(Protocol('message',stream['direction'][1:],payload=[datanode,self._ampnode]))
                else:
                    """ notify the other side about stream closing
                        notify the local user about sucessfull send
                        delete the local stream"""
                    conn.send(Protocol('iq',stream['direction'][1:],'set',payload=[Node(NS_IBB+' close',{'sid':sid})]))
                    conn.Event(self.DBG_LINE,'SUCCESSFULL SEND',stream)
                    del self._streams[sid]
                    self._owner.UnregisterCycleHandler(self.SendHandler)

                    """
<message from='romeo@montague.net/orchard' to='juliet@capulet.com/balcony' id='msg1'>
  <data xmlns='http://jabber.org/protocol/ibb' sid='mySID' seq='0'>
    qANQR1DBwU4DX7jmYZnncmUQB/9KuKBddzQH+tZ1ZywKK0yHKnq57kWq+RFtQdCJ
    WpdWpR0uQsuJe7+vh3NWn59/gTc5MDlX8dS9p0ovStmNcyLhxVgmqS8ZKhsblVeu
    IpQ0JgavABqibJolc3BKrVtVV1igKiX/N7Pi8RtY1K18toaMDhdEfhBRzO/XB0+P
    AQhYlRjNacGcslkhXqNjK5Va4tuOAPy2n1Q8UUrHbUd0g+xJ9Bm0G0LZXyvCWyKH
    kuNEHFQiLuCY6Iv0myq6iX6tjuHehZlFSh80b5BVV9tNLwNR5Eqz1klxMhoghJOA
  </data>
  <amp xmlns='http://jabber.org/protocol/amp'>
    <rule condition='deliver-at' value='stored' action='error'/>
    <rule condition='match-resource' value='exact' action='error'/>
  </amp>
</message>
"""

    def ReceiveHandler(self,conn,stanza):
        """ Receive next portion of incoming datastream and store it write
            it to temporary file. Used internally.
        """
        sid,seq,data=stanza.getTagAttr('data','sid'),stanza.getTagAttr('data','seq'),stanza.getTagData('data')
        self.DEBUG('ReceiveHandler called sid->%s seq->%s'%(sid,seq),'info')
        try: seq=int(seq); data=base64.decodestring(data)
        except: seq=''; data=''
        err=None
        if not sid in self._streams.keys(): err=ERR_ITEM_NOT_FOUND
        else:
            stream=self._streams[sid]
            if not data: err=ERR_BAD_REQUEST
            elif seq<>stream['seq']: err=ERR_UNEXPECTED_REQUEST
            else:
                self.DEBUG('Successfull receive sid->%s %s+%s bytes'%(sid,stream['fp'].tell(),len(data)),'ok')
                stream['seq']+=1
                stream['fp'].write(data)
        if err:
            self.DEBUG('Error on receive: %s'%err,'error')
            conn.send(Error(Iq(to=stanza.getFrom(),frm=stanza.getTo(),payload=[Node(NS_IBB+' close')]),err,reply=0))


    def StreamCloseHandler(self,conn,stanza):
        """ Handle stream closure due to all data transmitted.
            Raise xmpppy event specifying successfull data receive. """
        sid=stanza.getTagAttr('close','sid')
        self.DEBUG('StreamCloseHandler called sid->%s'%sid,'info')
        if sid in self._streams.keys():
            conn.send(stanza.buildReply('result'))
            conn.Event(self.DBG_LINE,'SUCCESSFULL RECEIVE',self._streams[sid])
            del self._streams[sid]
        else: conn.send(Error(stanza,ERR_ITEM_NOT_FOUND))

    def StreamBrokenHandler(self,conn,stanza):
        """ Handle stream closure due to all some error while receiving data.
            Raise xmpppy event specifying unsuccessfull data receive. """
        syn_id=stanza.getID()
        self.DEBUG('StreamBrokenHandler called syn_id->%s'%syn_id,'info')
        for sid in self._streams.keys():
            stream=self._streams[sid]
            if stream['syn_id']==syn_id:
                if stream['direction'][0]=='<': conn.Event(self.DBG_LINE,'ERROR ON RECEIVE',stream)
                else: conn.Event(self.DBG_LINE,'ERROR ON SEND',stream)
                del self._streams[sid]

    def StreamOpenReplyHandler(self,conn,stanza):
        """ Handle remote side reply about is it agree or not to receive our datastream.
            Used internally. Raises xmpppy event specfiying if the data transfer
            is agreed upon."""
        syn_id=stanza.getID()
        self.DEBUG('StreamOpenReplyHandler called syn_id->%s'%syn_id,'info')
        for sid in self._streams.keys():
            stream=self._streams[sid]
            if stream['syn_id']==syn_id:
                if stanza.getType()=='error':
                    if stream['direction'][0]=='<': conn.Event(self.DBG_LINE,'ERROR ON RECEIVE',stream)
                    else: conn.Event(self.DBG_LINE,'ERROR ON SEND',stream)
                    del self._streams[sid]
                elif stanza.getType()=='result':
                    if stream['direction'][0]=='|':
                        stream['direction']=stream['direction'][1:]
                        conn.Event(self.DBG_LINE,'STREAM COMMITTED',stream)
                    else: conn.send(Error(stanza,ERR_UNEXPECTED_REQUEST))

    def SetIBBFileDestination(self,sid,path):
        """ Set the destination of the file obtained with the stream identified by the Stream ID : sid
        Usualy called by SIFileTransfer"""
        self._fileDestination[sid]=path


class S5B(PlugIn):
    """Socks5 Bytestream (JEP-0065) can be used to send and receive big files, it is the preferred method for file transfer
    This class implement jabber part of JEP-0065, the socks5 part is in the socks5.py module.
    The method that you may need to use are :
    addProxy : to add a proxy to the list of streamhosts if you aleady know his jid, ip and port
    seekProxy : search a server for proxy.
    addStreamHost : to add a manually a streamhost.
    You shouldn't send a file using only this class, you should prefer the SIFileTransfer class.
    """
    def __init__(self):
        PlugIn.__init__(self)
        self.DBG_LINE='s5b'
        self._exported_methods=[self.addStreamHost,self.SetS5BFileDestination,self.addProxy,self.seekProxy]
        self.streamHosts={}
        self.fileToSend={}
        self._fileDestination={}
        self.SOCKS5=socks5.SOCKSv5(self)

    def plugin(self,owner):
        """Initialise some variables and set up handlers."""
        self.ownJID=owner._User+'@'+owner._Server[0]+'/'+owner._Resource
        owner.RegisterHandler('iq',self.ConnectionAckCB,ns=NS_BYTESTREAMS,typ='result')
        owner.RegisterHandler('iq',self.StreamHostCB,typ='set',ns=NS_BYTESTREAMS)

    def plugout(self):
        """Close every socket.
        Clear all data"""
        self.SOCKS5.closeSockets()
        del self.streamHosts
        del self.fileToSend
        del self._fileDestination
        del self.SOCKS5
        

    def addProxy(self,jid,verify=False):
		"""Discover information about the proxy65 given in argument
		and add it to the list of known streamhosts
		Return False if the jid doesn't support bytestreams
		"""
		#verify that the jid support bytestream
		if verify:
			info=features.discoverInfo(self._owner,jid)
			if info[1].count(NS_BYTESTREAMS)==0 or info[0][0]['category']!='proxy' or info[0][0]['type']!='bytestreams':
				return False
		self.DEBUG('%s is a proxy65'% jid,'info')
		#Get ip and port
		iq=Iq(typ='get',to=jid,queryNS=NS_BYTESTREAMS)
		rec=self._owner.SendAndCallForResponse(iq,self._addProxy,args={"jid":jid})

    def _addProxy(self,conn,rec,jid):
		try:
			for streamhost in rec.getQueryChildren():
				self.addStreamHost(jid,'proxy',ip=streamhost.getAttr('host'),port=streamhost.getAttr('port'),zeroconf=streamhost.getAttr('zeroconf'))
			return True
		except:
			return False

    def seekProxy(self,server=None):
        """Seek for bytestreams proxy on the server, if no server is specified, use the current server.
        Return True if we found at least one proxy."""
        if server == None:
            server=self._owner._Server[0]
        if server.count('@'):
            self.DEBUG('%s is not a valid server'%server,'error')
            return False
        items=features.discoverItems(self._owner,server)
        found=False
        for item in items:
            if self.addProxy(item['jid']):
                found=True
        return found


    def SetS5BFileDestination(self,key,path,offset,length):
        """ Set the destination of the file obtained with the stream identified by the Stream ID : sid
        offset and length have the same meaning as in SIFileTransfer.AcceptStream
        Usualy called by SIFileTransfer"""
        self._fileDestination[key]={'path':path,'offset':offset,'length':length}

    def ConnectionAckCB(self,conn,iq):
		"""Handler for when the target acknowledges SOCKS5 connection
		Used internally"""
		print "ackcb"
		try:
			jidUsed=iq.getTag('query',namespace=NS_BYTESTREAMS).getTag('streamhost-used').getAttr('jid')
		except:
			jidUsed=None
		key=None
		for keyt in self.fileToSend.keys():
			if self.fileToSend[keyt]['id']==iq.getID() and self.fileToSend[keyt]['to']==iq.getFrom():
				key=keyt
				del keyt
				break
		if key and jidUsed:
			fil=self.fileToSend[key]
			#Check if the stream used is local or is a proxy
			stream=self.streamHosts[jidUsed]
			if stream['type']=='self':
				self.SOCKS5.activate(key,fil['file'],fil['offset'],fil['length'])
			elif stream['type']=='proxy':
				if self.SOCKS5.connectTo(key,stream['host'],int(stream['port'])):
					reply=self.SOCKS5.sendRequest(key,socks5.CMD_CONNECT,socks5.ADDR_DOMAINNAME,key,0)
					if reply is not None and reply==(key,0):
						iq=Iq(typ='set',to=jidUsed,queryNS=NS_BYTESTREAMS,payload=[Node('activate',payload=[fil['to']])])
						iq.getTag('query').setAttr('sid',fil['sid'])
						self._owner.SendAndCallForResponse(iq,self.proxyActivatedHandler,args={'fil':fil,'key':key})
					else:
						self.eventSendError(key)
				else:
					self.eventSendError(key)
									
					
				
			del self.fileToSend[key]
		else:
			self._owner.send(Error(iq,ERR_UNEXPECTED_REQUEST))
		raise NodeProcessed
        

    def proxyActivatedHandler(self,conn,iq,fil,key):
		"""Called when we received the activation ack from the proxy
		Used internally"""
		self.DEBUG('sending file offset','info')
		if iq and isResultNode(iq) and int(iq.getTag('query').getAttr('sid'))==int(fil['sid']):
			self.SOCKS5.sendToProxy(key,fil['file'],fil['offset'],fil['length'])
		raise NodeProcessed
                    
    def StreamHostCB(self,conn,iq):
        """Called when we receive the list of streamhosts
        Used internally"""
        self.DEBUG('Received a list of streamhost','info')
        query=iq.getTag('query',namespace=NS_BYTESTREAMS)
        if query is not None:
            sid=query.getAttr('sid')
        else:
            sid=None
        id=iq.getID()
        err=None
        rep=None
        key=makeKey(sid,iq.getFrom().__str__(),iq.getTo().__str__())
        if not sid: err=ERR_BAD_REQUEST
        elif not key in self._fileDestination.keys():err=ERR_UNEXPECTED_REQUEST
        s=False
        if query.getAttr('mode')=='udp':
            self.DEBUG('UDP bytestreams not implemented','error')
        if not err and query.getAttr('mode')=='tcp':
            for streamhost in query.getTags('streamhost'):
                #We try to connect to each streamhost in the given order
                if not streamhost.getAttr('host') or not streamhost.getAttr('port'):pass
                s=self.SOCKS5.connectTo(key,streamhost.getAttr('host'),int(streamhost.getAttr('port')))
                if s:
                    self.DEBUG('Connected to streamhost %s'%streamhost.getAttr('jid'),'info')
                    self.SOCKS5.sendRequest(key,socks5.CMD_CONNECT,socks5.ADDR_DOMAINNAME,key,0)
                    self.DEBUG('Waiting for data','info')
                    fil=self._fileDestination[key]
                    self.SOCKS5.threadWaitForData(key,fil['path'],fil['offset'],fil['length'])
                    self.sendStreamhostACK(iq.getFrom(),streamhost.getAttr('jid'),id)
                    break
        if not err and not s:
            self.DEBUG('No suitable streamhost','error')
            rep=Protocol('iq',to=iq.getFrom(),typ='error',payload=[ErrorNode('item-not-found','404','cancel')])
            rep.getTag('error').getTag('item-not-found').setAttr('xmlns',NS_STANZAS)
            rep.setID(id)
        if err:rep=Error(iq,err)
        if rep:self._owner.send(rep)
        if err or not s:
            self.eventReceiveError(key)
        raise NodeProcessed


    def sendStreamhostACK(self,to,jid,id):
        """Send the stream used to the sender.
        Used internally."""
        iq=Iq(typ='result',to=to,queryNS=NS_BYTESTREAMS,payload=[Node('streamhost-used',attrs={'jid':jid})])
        iq.setID(id)
        self._owner.send(iq)
        
    def addStreamHost(self,jid,type='self',ip='',port=0,zeroconf=''):
        """Add another streamhost, for example a S5B proxy
           type can be 'self' or 'proxy'
           self mean that the Streamhost is us, and proxy is a ... proxy
           We can't have more than one 'self' streamhost.
           """
        if type=='self':
            for host in self.streamHosts:
                if type=='self':return False
        self.DEBUG('Added streamhost type : %s, jid : %s'%(type,jid),'info')
        host={'jid':jid,'type':type}
        if ip!='':
            host['host']=ip
        if port!=0:
            host['port']=port
        if type=='self':
            port=self.SOCKS5.listenTCP(ip,port)
            host['port']=port
        if zeroconf!='' and zeroconf!=None:
            host['zeroconf']=zeroconf
        self.streamHosts[jid]=host
        
    def OpenBytestream(self,sid,to,fp,offset,length):
        """Send the previously opened file fp to the JID designed by to with the Stream ID : sid"""
        self.DEBUG('sending file','info')
        iq=Iq(typ='set',queryNS=NS_BYTESTREAMS,to=to)
        query=iq.getTag('query')
        query.setAttr('sid',sid)
        query.setAttr('mode','tcp')
        key=makeKey(sid,self.ownJID,to)
        self.SOCKS5.authorise(key)
        for hostJID in self.streamHosts.keys():
            host=self.streamHosts[hostJID]
            typ=host['type']
            del host['type']
            query.addChild('streamhost',attrs=host)
            host['type']=typ
        #time.sleep(0.1)
        self._owner.send(iq)
        self.fileToSend[key]={'file':fp,'id':iq.getID(),'to':to,'offset':offset,'length':length,'sid':sid}

    def eventSendSuccess(self,key):
		"""raise an xmpppy event SEND_SUCCESS.
		The data is the key of stream
		Used internally (called by socks5.py"""
		print "event",key
		self._owner.Dispatcher.Event(NS_BYTESTREAMS,SEND_SUCCESS,key)

    def eventSendError(self,key):
        """raise an xmpppy event SEND_ERROR.
        The data is the key of stream
        Used internally (called by socks5.py"""
        self._owner.Dispatcher.Event(NS_BYTESTREAMS,SEND_ERROR,key)

    def eventReceiveSuccess(self,key):
        """raise an xmpppy event RECEIVE_SUCCESS.
        The data is the key of stream
        Used internally (called by socks5.py"""
        self._owner.Dispatcher.Event(NS_BYTESTREAMS,RECEIVE_SUCCESS,key)

    def eventReceiveError(self,key):
        """raise an xmpppy event RECEIVE_ERROR.
        The data is the key of stream
        Used internally (called by socks5.py"""
        self._owner.Dispatcher.Event(NS_BYTESTREAMS,RECEIVE_ERROR,key)

class SIFileTransfer(si.SI):
    """Implement sending files with stream inititiation (JEP-0096)
    To send a file you must call the sendSIFile method
    To receive a file you must handle SI_REQUEST events in the NS_SI realm (cf SIOfferCB method)
    """
    def __init__(self,localip='',port=0):
        si.SI.__init__(self,NS_PROFILE_FT)
        if localip=='':
            self.localip=socket.gethostbyname(socket.gethostname())
        else:
            self.localip=localip
        self.port=port
        self.authorisedStream={}   #contain keys and path of streams to auto-accept (used by tree transfer)
        self._exported_methods.append(self.sendSIFile)

    def plugin(self,owner):
        si.SI.plugin(self,owner)
        self.ownJID=owner._User+'@'+owner._Server[0]+'/'+owner._Resource
        try:
            S5B().PlugIn(owner)
            owner.addStreamHost(self.ownJID,ip=self.localip,port=self.port)
            self.streamMethod.append(NS_BYTESTREAMS)
        except None:
            pass
        try:
            IBB().PlugIn(owner)
            self.streamMethod.append(NS_IBB)
        except:
            pass

    def plugout(self):
        if self.streamMethod.count(NS_IBB):
            self._owner.IBB.PlugOut()
        if self.streamMethod.count(NS_BYTESTREAMS):
            self._owner.S5B.PlugOut()

    def authoriseStream(self,key,path,method=None):
        """Auto authorise the stream identified by key. The method is the default stream method to use."""
        self.authorisedStream[key]={'path':path,'method':method}

    def siOffered(self,conn,info):
        """If a stream is authorised accept it otherwise we raise an event"""
        if self.authorisedStream.has_key(info['key']):
            self.AcceptStream(info['key'],self.authorisedStream[info['key']]['path'])
            del self.authorisedStream[info['key']]
        else:
            si.SI.siOffered(self,conn,info)

    def selectStreamMethod(self,conn,iq,key=None):
        """If the stream was negociated with tree-transfer, use the method previously found."""
        if self.authorisedStream.has_key(key) and self.authorisedStream[key]['method'] is not None:
            return self.authorisedStream[key]['method'],True
        else:
            return si.SI.selectStreamMethod(self,conn,iq,key)
            

    def parseInfo(self,node):
        """Parse the file node (cf JEP-0096)
        retrun a dictionnary containing :
        'filename' : the name of the file offered
        'filesize' : the size of the file (in bytes)
        'desc' : a description of the file
        'range' : a boolean, if True the peer accept ranged transfer
        """
        filename=node.getAttr('name')
        filesize=node.getAttr('size')
        desc=node.getTagData('desc')
        if node.getTag('range'):
            rang=True
        else:
            rang=False
        if desc is None:
            desc=''
        return {'filename': filename,'filesize':filesize,'desc':desc,'range':rang}

    def AcceptStream(self,key,path,offset=None,length=None,cont=False):
        """Accept an incomming SI, path is the emplacement where to download the file
        length specify the number of bytes to retrieve and offset specify where to start in the file.
        ex : offset=128,length=256 tell that you whish to retrieve only 256 bytes starting at the 128th bytes in the file.
        If cont is set to True, we'll ask only for the remaining of the file, in this case offset attribute is overidden (and lenght shouldn't be set)
        """
        rang=None
        if self.streamsOfferedInfo[key]['info']['range']:
            rang=Node('range')
            if cont:
                if os.path.exists(path):
                    offset=os.path.getsize(path)
                    

        if offset and rang:
            rang.setAttr('offset',offset)
        else: offset=0
        if length and rang:
            rang.setAttr('length',length)
        else:
            #download only the filesize given by the sender
            length=int(self.streamsOfferedInfo[key]['info']['filesize'])-offset
            
        self.streamsOfferedInfo[key]['offset']=offset
        self.streamsOfferedInfo[key]['length']=length
        node=Node('file',attrs={'xmlns':NS_PROFILE_FT},payload=[rang])
        method=si.SI.AcceptStream(self,key,node)
        if (method==NS_IBB):
            self._owner.SetIBBFileDestination(key,path,offset,length)
        elif (method==NS_BYTESTREAMS):
               self._owner.SetS5BFileDestination(key,path,offset,length)
          
    def openStream(self,method,streamInfo,profileData):
        """Open the stream
        Is called by responseHandler method
        Used internally"""

        sid=None
        offset=None
        length=None
        try:
            offset=int(profileData.getTag('range').getAttr('offset'))
            length=int(profileData.getTag('range').getAttr('length'))
        except:
            pass
        
        file=streamInfo['file']
        size=streamInfo['filesize']
        sid=streamInfo['sid']
        to=streamInfo['to']
        if method=='http://jabber.org/protocol/ibb':
            fp=open(file)
            self._owner.OpenStream(sid=sid,to=to,fp=fp)
        if method=='http://jabber.org/protocol/bytestreams':
            if offset is None:
                offset=0
            if length is None:
                length=size-offset
            fp=open(file)
            self.DEBUG('opening stream','info')
            self._owner.S5B.OpenBytestream(sid=sid,to=to,fp=fp,offset=offset,length=length)

            
    def sendSIFile(self,to,file,desc='',sid=None,method=None):
        """Send a file
        to:target
        file:path of the file
        desc:description of the file
        Return an unique key generated from the stream id, the jid of the sender and the jid of the target
        """

        fileSize=os.path.getsize(file)
        fileName=file[file.rfind('/')+1:]
        node=Node('file',attrs={'xmlns':NS_PROFILE_FT,'name':fileName,'size':fileSize},payload=[Node('desc',payload=[desc]),Node('range')])
          
        fileInfo={'file':file,'filesize':fileSize}
        return si.SI.sendSI(self,to,node,fileInfo,sid,method)

class SITreeTransfer(si.SI):

    def __init__(self,siFT):
        """siFT is an SIFileTransfer instance"""
        si.SI.__init__(self,NS_PROFILE_TREE_FT)
        self._exported_methods.append(self.sendSITree)
        self.siFT=siFT
        self.streamMethod=self.siFT.streamMethod

    def plugin(self,owner):
        si.SI.plugin(self,owner)
        self.ownJID=owner._User+'@'+owner._Server[0]+'/'+owner._Resource



    def parseInfo(self,node):
        info={}
        if node is None:
            return {}
        if node.has_attr('numfiles'):
            info['numfiles']=node.getAttr('numfiles')
        if node.has_attr('size'):
            info['size']=node.getAttr('size')
        info['tree']=self.parseDirectory(node)
        return info

    def parseDirectory(self,node):
        """Parse recursivly a directory node
        return a dictionnary containing the tree
        """
        info={}
        for di in node.getTags('directory'):
            info[di.getAttr('name')]=self.parseDirectory(di)
        for fil in node.getTags('file'):
            info[fil.getAttr('name')]=fil.getAttr('sid')
        return info
        

    def AcceptStream(self,key,path):
        """Accept an incomming SI Tree Transfer, path is the emplacement where to download the tree (it must be a directory)"""
        tree=self.streamsOfferedInfo[key]['info']['tree']
        fro=self.streamsOfferedInfo[key]['from']
        method=si.SI.AcceptStream(self,key)
        self.createDirectory(path,tree,fro,method)
        print fro, tree


    def createDirectory(self,path,tree,fro,method=None):
        for dirname in tree.keys():
            if type(tree[dirname])==dict:
                dirpath=path+os.path.sep+dirname
                if not os.path.exists(dirpath):
                    os.mkdir(dirpath)
                self.createDirectory(dirpath,tree[dirname],fro,method)
            elif type(tree[dirname])==unicode:
                key=makeKey(tree[dirname],fro,self.ownJID)
                self.siFT.authoriseStream(key,path+os.path.sep+dirname,method)
          
    def openStream(self,method,streamInfo,profileData):
        """Open the stream
        Is called by responseHandler method
        Used internally"""

        filelist=streamInfo['filelist']
        sid=streamInfo['sid']
        to=streamInfo['to']
        if self.streamMethod.count(method)==0:
            self._owner.send(Error(iq,ERR_BAD_REQUEST))
            return
        for fileName in filelist:
            self.siFT.sendSIFile(to,fileName[0],sid=fileName[1],method=method)


    def sendSITree(self,to,path):
        """Send a directory
        to:target
        path:path of the directory
        Return an unique key generated from the stream id, the jid of the sender and the jid of the target
        """
        path=os.path.realpath(path)
        dirSize,numFiles,dirNode,fileList=self.walkDirectory(path,node=Node('directory',attrs={'name':os.path.basename(path)}))
        node=Node('tree',attrs={'xmlns':NS_PROFILE_TREE_FT,'numfiles':numFiles,'dirsize':dirSize},payload=[dirNode])
        return si.SI.sendSI(self,to,node,{'filelist':fileList})

    def walkDirectory(self,path,size=0,numFiles=0,node=None,fileList=[]):
        """Return the size of the directory, the number of files, the directory node and a liste of file to send"""
        for fileName in os.listdir(path):
            fullPath=os.path.join(path,fileName)
            if os.path.isdir(fullPath):
                newNode=Node('directory',attrs={'name':fileName})
                size,numFiles,newNode,fileList=self.walkDirectory(fullPath,size,numFiles,newNode)
            if os.path.isfile(fullPath):
                numFiles=numFiles+1
                size=size+os.path.getsize(fullPath)
                fileList.append([fullPath,'tree'+str(self.ID)])
                newNode=Node('file',attrs={'name':fileName,'sid':'tree'+str(self.ID)})
                self.ID=self.ID+1
            if node is None:
                node=newNode
            else:
                node.addChild(node=newNode)
        return size,numFiles,node,fileList
