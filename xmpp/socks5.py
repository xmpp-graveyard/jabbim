##   socks5.py 
##
##   Copyright (C) 2005 Gregoire Menuel
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

"""
This module is used by the filetransfer module for Socks5 Bytestream file transfer.
This is the socks5 part of JEP-0065.
None of the method defined here should be used directly.
"""

import socket
import struct
import threading
import SocketServer


CMD_CONNECT=0x01

REPLY_SUCCESS=0x00

ADDR_IPV4=0x01
ADDR_DOMAINNAME=0x03

METHOD_NOAUTH=0x00
METHOD_INVALID=0XFF

STATE_INITIAL=1#Waiting for initial negotiation
STATE_REQUEST=2#waiting for request
STATE_READY=3#ready to send file

RSV=0x00
SOCKS_VERSION=0x05

ERR_REFUSED=0x05
ERR_CMD_TYPE=0x07
ERR_ADDR_TYPE=0x08

def sendData(socket,fp,offset=None,length=None):
    """Send data to a socket, the file is given by fp.
    offset and length specifie the part of the file to send.
    Return True if the file has been succesfully send, False otherwise.
    """
    if offset:
        fp.seek(offset)
    remaining=length
    snd=None
    while ((remaining!=0 or remaining==None) and snd!=''):
        if remaining!=None and remaining<1024:
            bufsize=remaining
        else:
            bufsize=1024
        try:
            snd=fp.read(bufsize)
        except:
            return False
        if snd!='':
            try:
                socket.send(snd)
            except socket.error:
                snd=''
        if remaining!=None:
            remaining=remaining-len(snd)
    if remaining!=0 and remaining!=None:
        return False
    else:
        return True


class SOCKSv5Handler(SocketServer.StreamRequestHandler):
    """Handler used when someone connect to the server"""
    
    def handle(self):
         """handle TCP requests"""
         peer=self.request.getpeername()
         #look if the peer has already been seen
         if not self.server._owner._connectionsState.has_key(peer):
             self.server._owner._connectionsState[peer]=STATE_INITIAL
         rec=None
         while rec!='':
             state=self.server._owner._connectionsState[peer]
             if not state==STATE_READY:
                 try:
                     rec=self.request.recv(1024)
                 except:
                     del self.server._owner._connectionState[peer]
                     return
             else: rec=''
             if state==STATE_INITIAL:
                 self.handle_negotiation(self.request,rec)
             elif state==STATE_REQUEST:
                 self.handle_request(self.request,rec)
             state=self.server._owner._connectionsState[peer]

         if state==STATE_READY:
             #waiting for the activate command
             while(not self.server._owner._activated.has_key(peer)):
                 pass
         fil=self.server._owner._activated[peer]
         success=sendData(self.request,fil['file'],fil['offset'],fil['length'])
         if not success and self.server._owner.s5b:
             self.server._owner.s5b.eventSendError(fil['key'])
         elif success and self.server._owner.s5b:
             self.server._owner.s5b.eventSendSuccess(fil['key'])
         del self.server._owner._activated[peer]
             
    def handle_negotiation(self,request,rec):
        """Handle the negotiation part of socks5"""
        try:
            ver,nmethod=struct.unpack('!BB',rec[:2])
            if ver!=SOCKS_VERSION:
                request.send(struct.pack('!BB',SOCKS_VERSION,METHOD_INVALID))
                request.close()
                return
            methods=struct.unpack('%dB'%nmethod,rec[2:nmethod+2])
            goodMethod=False
            for i in methods:
                if i==METHOD_NOAUTH:#the only auth method supported
                    goodMethod=True
                    self.server._owner._connectionsState[request.getpeername()]=STATE_REQUEST
                    self.request.send(struct.pack('!BB',SOCKS_VERSION,METHOD_NOAUTH))
            if not goodMethod:
                request.send(struct.pack('!BB',SOCKS_VERSION,METHOD_INVALID))
                request.close()
        except:
            request.close()
                    
    def handle_request(self,request,rec):
        """Handle requests.
        Only CONNECT is supported as it is the only command needed by JEP-0065
        """
        try:
            ver,cmd,rsv,atyp=struct.unpack('!BBBB',rec[:4])

            if atyp==ADDR_IPV4:
                addr,port=struct.unpack('!IH'),rec[4:10]
            elif atyp==ADDR_DOMAINNAME:
                lenght=ord(rec[4])
                addr,port=struct.unpack('!%dsH'% lenght ,rec[5:])
            else:
                self.server._owner.send_error(request,ERR_ADDR_TYPE)
                return None
            if cmd==CMD_CONNECT:
                self.server._owner._connectionsState[request.getpeername()]=STATE_READY
                self.handle_connect_request(request,atyp,addr,port)
            else:
                self.server._owner.send_error(request,ERR_CMD_TYPE)
            
                 

        except struct.error:
            pass
             
    def handle_connect_request(self,request,atyp,addr,port):
        """Handle the connect request"""
        #check if the addr correspond to a known key (key=SHA1(sid+initiator.getJID()+target.getJID()))
        try:
            if atyp!=ADDR_DOMAINNAME:
                self.server._owner.send_error(request,ERR_REFUSED)
                return None
            if port ==0 and addr in self.server._owner._authorisedConnection.keys():
                self.server._owner._authorisedConnection[addr]=self.request.getpeername()
                stru=struct.pack('!BBBBB%dsH'%len(addr),SOCKS_VERSION,REPLY_SUCCESS,RSV,ADDR_DOMAINNAME,len(addr),addr,port)
                request.send(struct.pack('!BBBBB%dsH'%len(addr),SOCKS_VERSION,REPLY_SUCCESS,RSV,ADDR_DOMAINNAME,len(addr),addr,port))
            else:
                self.server._owner.send_error(request,ERR_REFUSED)
        except:
            return None
 


class SOCKSv5:

    def __init__(self,s5b=None):
        self.sock={}
        self._connectionsState={}
        self._authorisedConnection={}
        self._activated={}
        self.s5b=s5b

    def listenTCP(self,ip='',port=0):
        """Create a SOCKS5 TCP server
        return the listenning port if none is specified
        """
        self.serv=SocketServer.TCPServer((ip,port),SOCKSv5Handler)
        self.serv._owner=self
        t=threading.Thread(target=self.serv.serve_forever)
        t.setDaemon(True)
        t.start()
        return self.serv.socket.getsockname()[1]

    def closeSockets(self):
        """Close all currently oppened sockets and close the tcp server"""
        self.serv.server_close()
        for key in self.sock.keys():
            self.sock[key].close()
            del self.sock[key]


    def send_error(self,request,errorcode):
        """Send a socks5 error reply"""
        try:
            request.send(struct.pack('!BBBIH',SOCKS_VERSION,errorcode,RSV,ADDR_IPV4,0,0))
        except: pass
        request.close()
        
    def authorise(self,key):
        """Authorise the stream designed by the key to be send by the server"""
        if self._authorisedConnection.has_key(key):
            return 0
        self._authorisedConnection[key]=None

    def activate(self,key,fp,offset=None,length=None):
        """Activate the stream
        Send the file given by fp to the person designed by the key"""
        self._activated[self._authorisedConnection[key]]={'file':fp,'offset':offset,'length':length,'key':key}
        del self._authorisedConnection[key]
        
    def connectTo(self,key,addr,port):
        """Open a connection to the host
        addr:ip or hostname of the host
        key:is the SHA1(sid+initiator.getJID()+target.getJID()), it is used internally to identifiate the socket
        Retrn True if we successed."""
        
        try:
            if key in self.sock.keys():
                #socket already exist
                return False
            self.sock[key]=socket.socket()
            self.sock[key].settimeout(5)
            self.sock[key].bind(('',0))
            self.sock[key].connect((addr,port))
            self.sock[key].send(struct.pack('!BBB',SOCKS_VERSION,0x01,0x00))
            rec=struct.unpack('!BB',self.sock[key].recv(1024))
            if rec[0]!=SOCKS_VERSION or rec[1]!=0:
                self.sock[key].close()
                del self.sock[key]
                return False
            else:
                return True
        except socket.timeout:
            self.sock[key].close()
            del self.sock[key]
            return False

    def sendToProxy(self,key,fp,offset,length):
		"""Send the file to the proxy."""
		
		if key not in self.sock.keys():
			#socket doesn't exist
			return False
		print "sendtoproxy"
		success=sendData(self.sock[key],fp,offset,length)
		if not success and self.s5b:
			print "False"
			self.s5b.eventSendError(key)
		elif success and self.s5b:
			print "True"
			self.s5b.eventSendSuccess(key)

    def sendRequest(self,key,req,addrType,addr,port):
        """Send a SOCKS5 request
        addrType:ADDR_IPV4 or ADDR_DOMAINNAME : the type of address to connect
        req should be CMD_CONNECT
        """
        try:
            if not key in self.sock.keys():
                return None
            stru=struct.pack('!BBBBB%dsH' % len(addr),SOCKS_VERSION,req,RSV,addrType,len(addr),addr,port)
            self.sock[key].send(stru)
            rec=self.sock[key].recv(1024)
            ver,replycmd,replyrsv,replyaddrType=struct.unpack('!BBBB',rec[:4])
            if replycmd!=REPLY_SUCCESS:
                return None
            if replyaddrType==ADDR_DOMAINNAME:
                nlen = ord(rec[4])
                replyaddr, replyport = struct.unpack('!%dsH' % nlen, rec[5:])
            
            return (replyaddr,replyport)
        except:
            return None

    def threadWaitForData(self,key,filepath,offset=None,length=None):
        """Run waitForData in a thread."""
        t=threading.Thread(target=self.waitForData, args=(key,filepath,offset,length))
        t.start()
        
    def waitForData(self,key,filepath,offset=None,length=None):
        """Wait until the data is being transmited and then write the data in the file given by filepath;
        """
        if not key in self.sock.keys():
            return None
        fp=open(filepath,'a')
        if offset:
            #move to the right position in the file
            fp.seek(offset)
        firstloop=True
        rec=''
        remaining=length
        while ((firstloop==True or rec!='') and (remaining!=0 or remaining==None)):
            if remaining!=None:
                if remaining<1024:
                    bufsize=remaining
                else:
                    bufsize=1024
            else:
                bufsize=1024
            
            firstloop=False
            try:
                rec=self.sock[key].recv(bufsize)
                fp.write(rec)
            except:
                rec=''
            if remaining:
                remaining=remaining-len(rec)            

        fp.close()
        self.sock[key].close()
        del self.sock[key]
        if self.s5b:
            if remaining!=0 or remaining==None:
                self.s5b.eventReceiveError(key)
            else:
                self.s5b.eventReceiveSuccess(key)
            
                
