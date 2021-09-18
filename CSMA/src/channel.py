import time
import const
import threading


class Channel():

    def __init__(self, sender_to_channel, channel_to_sender: list, receiver_to_channel: list, channel_to_receiver: list):
        self.is_active = False
        self.sender_to_channel = sender_to_channel
        self.channel_to_sender = channel_to_sender
        self.receiver_to_channel = receiver_to_channel
        self.channel_to_receiver = channel_to_receiver

    def transfer_pkt_from_sender_to_receiver(self):
        while True:
            pkt = self.sender_to_channel.recv()
            self.is_active = True
            time.sleep(const.channel_propagation_time)
            self.is_active = False
            receiver = pkt.decode_dest_address()
            self.channel_to_receiver[receiver].send(pkt)

    def tarnsfer_response_from_receiver_to_sender(self, sender: int):
        while True:
            if self.is_active: self.channel_to_sender[sender].send(str(1))  # channel is busy
            else: self.channel_to_sender[sender].send(str(0))  # channel is idle

    def initiate_channel_process(self):
        print("\nCHANNEL has been initialised\n")
        channel_to_receiver_thrdlst = []
        channel_to_sender_thrdlst = []
        sender = 0

        pkt_thrd = threading.Thread(name="PacketThread-"+str(sender+1), target=self.transfer_pkt_from_sender_to_receiver)
        channel_to_receiver_thrdlst.append(pkt_thrd)

        for _ in range(const.total_sender_number):
            resp_thrd = threading.Thread(name="ResponseThread-"+str(sender+1),
                                         target=self.tarnsfer_response_from_receiver_to_sender, args=(sender,))
            channel_to_sender_thrdlst.append(resp_thrd)
            sender += 1

        for thread in channel_to_receiver_thrdlst:
            thread.start()

        for thread in channel_to_sender_thrdlst:
            thread.start()

        for thread in channel_to_receiver_thrdlst:
            thread.join()

        for thread in channel_to_sender_thrdlst:
            thread.join()
