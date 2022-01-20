
import time
import random
import threading
import sys
import const
from gen_packet import Packet


class Sender:
    def __init__(self, name, fileName, senderToChannel, channelToSender): #, channelEvent): # last two needs to be shared queue
        self.name               = name
        self.fileName           = fileName
        self.packetType         = {'data' : 0, 'ack' : 1}
        self.dest               = self.selectReceiver()
        self.senderToChannel    = senderToChannel
        self.channelToSender    = channelToSender
        self.timeoutEvent       = threading.Event()
        self.seqNo              = 0
        self.start              = 0
        self.endTransmitting    = False
        self.receivedAck        = False # true if ack received and verified as valid
        self.recentPacket       = None
        #self.recentPacket exists

    def selectReceiver(self):
        return random.randint(0, const.totalReceiverNumber-1)
        # return 0 # for testing with 1 sender

    def openFile(self, filename):
        try:
            file = open(filename, 'r', encoding='utf-8')
        except IOError:
            sys.exit("No file exit with name {} !".format(filename))
        return file

    def resendCurrentPacket(self):
        self.senderToChannel.send(self.recentPacket)

    def dataIntoFrames(self):

        time.sleep(0.2)
        # print("***********************************")
        print("SENDER{} starts sending data to RECEIVER{}\n".format(self.name+1, self.dest+1))
        # print("***********************************")
        file = self.openFile(self.fileName)

        byte = file.read(const.defaultDataPacketSize)
        self.seqNo = 0
        pktCount = 0
        totalPktCount = 0
        while byte:
            pkt = Packet(self.packetType['data'], self.seqNo, byte, self.name, self.dest).makePacket()
            self.recentPacket = pkt
            self.senderToChannel.send(pkt)
            self.seqNo = (self.seqNo+1)%2
            pktCount += 1
            totalPktCount += 1
            print("SENDER{} -->> PACKET {} SENT TO CHANNEL".format(self.name+1, pktCount))
            while not self.receivedAck: # timeout does happen
                #resend needed
                self.timeoutEvent.wait(const.senderTimeout)# if timeout resend
                time.sleep(0.2)
                if not self.timeoutEvent.is_set():
                    self.resendCurrentPacket()
                    totalPktCount += 1
                    print("SENDER{} -->> PACKET {} HAS BEEN RESENDING".format(self.name+1, pktCount))
                else: break
            self.timeoutEvent.clear()

            byte = file.read(const.defaultDataPacketSize)
            # if len(byte) == 0: break
            # if len(byte) < const.defaultDataPacketSize: 
            #     tempLength = len(byte)
            #     for _ in range(const.defaultDataPacketSize - tempLength):
            #         byte += '\0'

        self.endTransmitting = True
        file.close()

        print("\n*****************(Sender{}:)STATS******************".format(self.name+1))
        print("Total packets: {}\nTotal Packets send {}".format(pktCount, totalPktCount))
        print("Time Taken till now: ", round((time.time() - self.start)/60, 2), " mins\n")
        print("******************************************************\n\n")


    def checkAckPackets(self):
        time.sleep(0.2)
        while True:
            if not self.endTransmitting: packet = self.channelToSender.recv()
            else: break
            if packet.type == 1:
                if packet.checkForError():
                    if packet.seqNo == self.seqNo:
                        self.timeoutEvent.set()
                        print("SENDER{} -->> PACKET HAS REACHED SUCCESSFULLY".format(self.name+1))
                    else: # resend needed
                        print("SENDER{} -->> ACK RESENDED".format(self.name+1))
                        self.timeoutEvent.clear()
                else:
                    print("SENDER{} -->> ACK DISCARDED".format(self.name+1))
                    self.timeoutEvent.clear()
            else:
                print("SENDER{} -->> ACK DISCARDED".format(self.name+1))
                self.timeoutEvent.clear()


    def transmit(self):

        self.start = time.time()
        sendingThread = threading.Thread(name="SendingThread", target=self.dataIntoFrames)
        ackCheckThread = threading.Thread(name='ackCheckThread', target=self.checkAckPackets)

        sendingThread.start()
        ackCheckThread.start()

        sendingThread.join()
        ackCheckThread.join()
