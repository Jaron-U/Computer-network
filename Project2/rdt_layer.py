# cited from https://classes.engr.oregonstate.edu/eecs/summer2021/cs372-001/projects/rdt_layer.py

from unreliable import *

class RDTLayer(object):
    # The length of the string data that will be sent per packet...
    DATA_LENGTH = 4 # characters
    # Receive window size for flow-control
    FLOW_CONTROL_WIN_SIZE = 15 # characters

    # Add class members as needed...
    #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None

        #send members
        self.dataToSend = ''
        self.sendWinStart = 0

        #receive members
        self.dataToReceive = ''
        self.dictReceived = {}

        #temp sent data
        self.tempToSend = []

        #stat
        self.currentIteration = 0 # <--- Use this for segment 'timeouts'
        self.countSegmentTimeouts = 0

        self.expectACK = 0

    # Called by main to set the unreliable sending lower-layer channel
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # Called by main to set the unreliable receiving lower-layer channel
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # Called by main to set the string data to send
    def setDataToSend(self,data):
        self.dataToSend = data

    def setDataReceived(self,data):
        self.dataToReceive = data

    # Called by main to get the currently received and buffered string data, in order
    def getDataReceived(self):
        # use for the error out of order
        sortedKeys = sorted(self.dictReceived.keys())
        data = [] 
        for key in sortedKeys:
            seg = self.dictReceived[key]
            data.append(seg.payload)

        return ''.join(data)

    # "timeslice". Called by main once per iteration
    def manage(self):
        self.currentIteration += 1
        self.manageSegmentTimeouts()
        self.manageSend()
        self.manageReceive()
    
    # function to get the ack
    def getAcknum(self): 
        ack = 0
        while 1:
            if ack not in self.dictReceived:
                break
            ack += RDTLayer.DATA_LENGTH
        return ack
    
    # Manage Segment send
    def manageSegmentTimeouts(self):
        print('manageSegmentTimeouts')
        # check every segment in the temptoSend
        for tempseg in self.tempToSend:
            # if the times of iteration is greate than 5 times
            if(self.currentIteration - tempseg.getStartIteration() > 5):
                # reset the iteration times
                tempseg.setStartIteration(self.currentIteration)
                # try to resend the packet.
                self.sendChannel.send(tempseg)
                print("resend data segment")
                tempseg.dump()
                # increaing the countSegmentTimeouts
                self.countSegmentTimeouts += 1
                tempseg.setStartIteration(self.currentIteration)


    # Manage Segment sending  tasks...
    def manageSend(self):
        print('mangeSend')
        if len(self.dataToSend) == 0:
            return
        # You should pipeline segments to fit the flow-control window
        # The flow-control window is the constant RDTLayer.FLOW_CONTROL_WIN_SIZE
        # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH
        # These constants are given in # characters

        # Somewhere in here you will be creating data segments to send.
        # The data is just part of the entire string that you are trying to send.
        # The seqnum is the sequence number for the segment (in character number, not bytes)

        # set the a flag to record the index of segment
        seqnum = self.sendWinStart
        
        # sent the data constantly
        while 1:
            # if it has send data which len greater than 15. out of loop
            if seqnum + RDTLayer.DATA_LENGTH >= self.sendWinStart + RDTLayer.FLOW_CONTROL_WIN_SIZE:
                break
            
            # get the data and slice them into several parts. 
            data = self.dataToSend[seqnum: seqnum + RDTLayer.DATA_LENGTH]

            # put current part into the segment
            seg = Segment()
            seg.setStartIteration(self.currentIteration)
            seg.setData(seqnum,data)
            segc = Segment()
            segc.setStartIteration(self.currentIteration)
            segc.setData(seqnum,data)
            if not len(self.tempToSend) == 0:
                hasSent = False
                # store the seg which sent into the temp list
                for tempseg in self.tempToSend:
                    if  tempseg.seqnum == seg.seqnum:
                        hasSent = True
                if not hasSent:
                    self.tempToSend.append(segc)
                    # Use the unreliable sendChannel to send the segment
                    print("sending segment: ")
                    seg.dump()
                    self.sendChannel.send(seg)    
            else:
                # Use the unreliable sendChannel to send the segment
                print("sending segment: ")
                seg.dump()
                self.sendChannel.send(seg)
                self.tempToSend.append(segc)
        
            # Increaing seq num
            seqnum += RDTLayer.DATA_LENGTH

        self.expectACK = seqnum
        

    # Manage Segment receive  tasks...
    def manageReceive(self):
        print("manageReceive")
        # This call returns a list of incoming segments (see Segment class)...
        listIncoming = self.receiveChannel.receive()

        #check whether we did receive sth
        if len(listIncoming) == 0:
            return 

        # set this flag to determine what ack should be send
        dataPacketsReceived = False

        # How can you tell data segments apart from ack segemnts?
        for seg in listIncoming:
        # if the seqnum greater than 0, which mean is we get the data
            if seg.seqnum >= 0:
                # try to corret the error packet
                if (seg.checkChecksum()):
                    # unpack the segment: get data
                    # updata dataToReceive
                    dataPacketsReceived = True
                    self.dictReceived[seg.seqnum] = seg
                    print ("received data seg: ")
                    seg.dump()
                else:
                    for everykey in list(self.dictReceived.keys()):
                        if everykey >= seg.seqnum:
                            del self.dictReceived[everykey]
            # if the ack is greater than we should send the data from the acknum
            elif seg.acknum >= 0:
                print("recack: ", seg.acknum)
                self.sendWinStart = seg.acknum
                for tempseg in list(self.tempToSend):
                    if seg.acknum >= tempseg.seqnum:
                        self.tempToSend.remove(tempseg)
                print("exACK: ", self.expectACK)
                if not seg.acknum == self.expectACK:
                    self.tempToSend.clear()
                    for everykey in list(self.dictReceived.keys()):
                        if everykey >= seg.acknum:
                            del self.dictReceived[everykey]


        # Somewhere in here you will be creating ack segments to send.
        # The goal is to employ cumulative ack, just like TCP does...
        # if dataPacketsReceived flag is f
        if dataPacketsReceived: 
            ack = Segment()
            # set cumulative ack
            ack.setAck(self.getAcknum())
            print("sending ack:")
            ack.dump()
            # Use the unreliable sendChannel to send the ack packet
            self.sendChannel.send(ack)

