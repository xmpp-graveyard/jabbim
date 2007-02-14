##   si.py 
##
##   Copyright (C) 2004 Gregoire Menuel <omega@gpl.insa-lyon.fr>
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


from protocol import *
from dispatcher import PlugIn
import base64
import sha

#Events name
SI_OFFERED='STREAM INITIATION OFFERED'
NO_VALID_STREAM='NO VALID STREAM'#We received a SI request but no valid stream can be found
SI_ERROR='STREAM INITIATION ERROR'


def makeKey(sid,source,target):
    """Generate the key used to identifiate the stream.
    Used by SI, IBB,S5B and SIFileTransfer class """
    return sha.new("%s%s%s" % (sid, source, target)).hexdigest()

class SI(PlugIn):

    def __init__(self,profile):
        PlugIn.__init__(self)           
        self.DBG_LINE='si'
        self._exported_methods=[]
        self.ID=1
        self.profile=profile
        self.streamMethod=[]
        self.streamsInfo={}
        self.streamsOfferedInfo={}

    def plugin(self,owner):
        owner.RegisterHandler('iq',self.SIOfferCB,typ='set',ns=NS_SI)


    def parseInfo(self,node):
        """Method used for arsing info tag for some SI profiles
        MUST be overridden if the profile require it"""
        return None
            
    def SIOfferCB(self,conn,iq):
        """Called when receiving an SI request
        Raise an xmpppy event in the realm defined by the profile namespace:
        SI_OFFERED if we found a valid stream and NO_VALID_STREAM otherwise.
        In both case we give a dictionnary as the event data.
        This dictionnary contains the following keys : filename, filsize, desc (description of the file),range (True if the sender support ranged file transfer, False otherwise) and key"""
        profile=None
        infoNode=None
        try:
            #We try to find the info of the stream
            #first the profile
            profile=iq.getTag('si',namespace=NS_SI).getAttr('profile')
        except: pass
        if profile is None:
            conn.send(Error(iq,ERR_BAD_REQUEST))
            return
        if profile != self.profile:
            return
        try:
            children=iq.getTag('si',namespace=NS_SI).getChildren()
            for node in children:
                if node.getNamespace()==profile:
                    infoNode=node
        except: pass

        if infoNode is not None:
            info=self.parseInfo(infoNode)
        else:
            info={}
        key=makeKey(iq.getTag('si',attrs={'profile':profile}).getAttr('id'),iq.getFrom(),iq.getTo())
        useStream,knownMethod=self.selectStreamMethod(conn,iq,key)
        self.streamsOfferedInfo[key]={'profile':profile,'stream':useStream,'knownMethod':knownMethod,'id':iq.getID(),'info':info,'from':iq.getFrom(),'sid':iq.getTag('si',attrs={'profile':profile}).getAttr('id')}
        info['key']=key
        self.siOffered(conn,info)
        raise NodeProcessed

    def selectStreamMethod(self,conn,iq,key=None):
        """Select the best stream to use.
        Must be extended or overidden if the profile specifie no feature negotiation (like the JEP-0096 part of JEP-0105)
        Return a tupple containing the namespace of the choosen method and a boolean, if this boolean is True then the peer already know which stream we're going to use, so we don't send it back.
        """
        avaibleStreams=[]
        useStream=None
        try:
            streamMethod=iq.getTag('si',attrs={'profile':self.profile}).getTag('feature',namespace=NS_FEATURE_NEG).getTag('x',namespace=NS_DATA).getTag('field',attrs={'var':'stream-method','type':'list-single'}).getTags('option')
        except:
            conn.send(Error(iq,ERR_BAD_REQUEST))
            raise NodeProcessed
        for stream in streamMethod:
            avaibleStreams.append(stream.getTag('value').getData())
        useStream=None
        for stream in self.streamMethod:
            if avaibleStreams.count(stream)!=0:
                useStream=stream
                break
        if useStream==None:
            self.NoValidStream(key)
            conn.Event(self.profile,NO_VALID_STREAM,info)
            raise NodeProcessed

        return useStream,False

        

    def siOffered(self,conn,info):
        """Raise a SI_OFFERED xmpp.py event with a dictionnary containing information about the stream.
        May be overridden or extended.
        """
        conn.Event(self.profile,SI_OFFERED,info)

    def NoValidStream(self,key):
        """No valid stream found in the SI request.
        Raise a NO_VALID_STREAM event in the NS_BYTESTREAMS realm
        Used internally"""
        self._owner.Dispatcher.Event(NS_BYTESTREAMS,NO_VALID_STREAM,key)
        id=self.streamsOfferedInfo[key]['id']
        error=Protocol('iq',to=self.streamsOfferedInfo[key]['from'],typ='error',payload=[ ErrorNode('bad-request','400','cancel')])
        error.setID(id)
        error.getTag('error').addChild('no-valid-streams',namespace=NS_SI)
        error.getTag('error').getTag('bad-request').setAttr('xmlns',NS_STANZAS)
        del self.streamsOfferedInfo[key]
        self._owner.send(error)        

    def RejectStream(self,key):
        """Reject the stream initiation designed by the key"""
        error=Protocol('iq',to=self.streamsOfferedInfo[key]['from'],typ='error',payload=[ ErrorNode('forbidden','403','cancel','Offer Declined')])
        error.getTag('error').getTag('forbidden').setAttr('xmlns',NS_STANZAS)
        error.setID(self.streamsOfferedInfo[key]['id'])
        self._owner.send(error)
        del self.streamsOfferedInfo[key]


    def AcceptStream(self,key,profileData=None):
        """Accept an incomming SI
        profileData is a node conatining data to sent back to the sender
        e.g. :
        <file xmlns='http://jabber.org/protocol/si/profile/profile-name'>
        <value>returned value</value>
        </file>

        May be extented
        """
        iq=Node('iq',attrs={'type':'result','to':self.streamsOfferedInfo[key]['from'],'id':self.streamsOfferedInfo[key]['id']},payload=
                [Node('si',attrs={'xmlns':NS_SI},payload=
                      [profileData]
                      )]
                )
        siNode=iq.getTag('si')
        if not self.streamsOfferedInfo[key]['knownMethod']:
            xNode=Node('feature',attrs={'xmlns':NS_FEATURE_NEG},payload=
                       [Node('x',attrs={'xmlns':NS_DATA,'type':'submit'},payload=[Node('field',attrs={'var':'stream-method'},payload=[Node('value',payload=[self.streamsOfferedInfo[key]['stream']])])])]
                       )
            siNode.addChild(node=xNode)
        method=self.streamsOfferedInfo[key]['stream']
        self._owner.send(iq)
        del self.streamsOfferedInfo[key]
        return method

    def sendSI(self,to,profileData=None,streamInfo={},sid=None,method=None):
        """Send a SI
        to:target
        profileData : profile specific node
        e.g.:
        <file xmlns='http://jabber.org/protocol/si/profile/file-transfer'
        name='test.txt'
        size='1022'>
        <desc>This is info about the file.</desc>
        </file>
        streamInfo is a dictionnary containing some information about the stream. The key and the sid will be added to this dictionnary. This dictionnary will be passed to the ReponseHandler method.
        sid is an unique identifier of the stream, may be omited.
        You can specify a stream method to use, this way we don't do the feature negociation part of si. This method should be in self.streamMethod.
        Return an unique key generated from the stream id, the jid of the sender and the jid of the target
        """
        if sid is None:
            sid=str(self.ID)
            self.ID+=1
        
        siIq=Protocol(name='iq',to=to,typ='set',payload=[Node(tag='si',attrs={'xmlns':NS_SI,'id':sid,'mime-type':'application/octet-stream','profile':self.profile},payload=[profileData])])
        
        if method is None:
            featureNode=siIq.getTag('si').addChild('feature',attrs={'xmlns':NS_FEATURE_NEG},payload=[Node('x',attrs={'xmlns':NS_DATA,'type':'form'})])
            fieldNode=featureNode.getTag('x').addChild('field',attrs={'var':'stream-method','type':'list-single'})
            for feat in self.streamMethod :
                fieldNode.addChild('option',payload=[Node('value',payload=feat)])
        key=makeKey(sid,self.ownJID,siIq.getTo())
        streamInfo['key']=key
        streamInfo['sid']=sid
        self._owner.SendAndCallForResponse(siIq,self.ResponseHandler,args={'streamInfo':streamInfo,'method':method})
        return key


    def ResponseHandler(self,conn,iq,streamInfo,method=None):
        """Handler used when a response to SI is received.
        Raise an xmppy Event on error. The realm is the profle namespace, the event : SI_ERROR.
        The data passed to the Event handler is a tupple containing the key of the si (cf sendSIFile method), the error code, the error general condition, the error specific condition and optionnaly an error text. See JEP-0095 for more info about these error types.
        Set streamInfo['to'] to the full jid of the target
        Call openStream
        """
        err=None
        #Check if the reponse is an error
        errCode=None
        errType=None
        errSpec=None
        errText=None
        if iq.getAttr('type')=='error':
            try:
                
                errCode=int(iq.getTag('error').getAttr('code'))
                for node in iq.getTag('error').getChildren():
                    if node.getAttr('xmlns')==NS_STANZA:
                        if node.getName()=='text':
                            errText=node.getData()
                        else:
                            errType=node.getName()
                    elif node.getAttr('xmlns')==NS_SI:
                              errSpec=node.getName()
            except:
                err=ERR_BAD_REQUEST
        sid=None

        
        if not err and not errCode:
            #if we don't have already negociated the  method :
            if method is None:
                method=iq.getTag('si',namespace=NS_SI).getTag('feature',namespace=NS_FEATURE_NEG).getTag('x',namespace=NS_DATA).getTag('field').getTag('value').getData()
            profileData=None
            try:
                children=iq.getTag('si',namespace=NS_SI).getChildren()
                for node in children:
                    if node.getNamespace()==self.profile:
                        profileData=node
            except:
                pass
            streamInfo['to']=str(iq.getFrom())
            self.openStream(method,streamInfo,profileData)

        elif errCode:
            conn.Event(self.profile,SI_ERROR,(streamInfo['key'],errCode,errType,errSpec,errText))
        else: conn.send(Error(iq,err))
        raise NodeProcessed


    def openStream(self,method,streamInfo={},profileData=None):
        """open the stream
        Called by responseHandler.
        method is the method used for the stream
        streamInfo is the same as the one given by the  sendSI method
        profileData is an xml node specific for the profile
        Must be overriden"""
        pass
      
