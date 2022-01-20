import time
import const
import sys
from gen_packet import Packet
# from gen_packet import *


class Receiver:
    def __init__(self, name, receiverToChannel, channelToReceiver):
        self.seqNo = 0
        self.name = name
        self.senderList = {}
        self.packetType = {'data': 0, 'ack': 1}
        self.receiverToChannel = receiverToChannel  # write
        self.channelToReceiver = channelToReceiver  # read
        self.recentACK = Packet(1, 0, "Acknowledgement Packet", self.name, 0).makePacket()

    def sendAck(self, sender, seqNo):
        pkt = Packet(_type=self.packetType['ack'], seqNo=self.seqNo,
                        segmentData='acknowledgement Packet',
                        sender=self.name,
                        dest=sender).makePacket()
        print(str(seqNo))
        self.recentACK = pkt
        self.receiverToChannel.send(pkt)

    def resendPreviousACK(self):
        self.receiverToChannel.send(self.recentACK)

    def openFile(self, filepath):
        try:
            file = open(filepath, 'a+', encoding='utf-8')
        except IOError:
            sys.exit("File path not exit!")
        return file

    def decodeSeqNo(self, pkt):
        return pkt.decodeSeqNo()

    def decodeSender(self, pkt):
        senderAddress = pkt.decodeSourceAddress()
        return senderAddress

    def startReceiving(self):
        time.sleep(0.4)
        while True:
            pkt = self.channelToReceiver.recv()
            print("RECEIVER{} -->> PACKET RECEIVED".format(self.name+1))

            if pkt.checkForError():
                print("RECEIVER{} -->> ERROR CHECKED".format(self.name+1))
                sender = self.decodeSender(pkt)
                seqNo = self.decodeSeqNo(pkt)
                if self.seqNo == seqNo:
                    if sender not in self.senderList.keys():
                        self.senderList[sender] = const.outFilePath + 'output' + str(sender)
                    outFile = self.senderList[sender]
                    file = self.openFile(outFile)
                    data = pkt.extractData()
                    file.write(data)
                    file.close()
                    self.seqNo = (self.seqNo+1) % const.windowSize
                    self.sendAck(sender, self.seqNo)
                    print("RECEIVER{} -->> ACK SENT FROM RECEIVER".format(self.name+1))
                else:
                    self.resendPreviousACK()
                    print("RECEIVER{} -->> ACK RESENDED".format(self.name+1))
            else:
                print("RECEIVER{} -->> PACKET DISCARDED".format(self.name+1))
