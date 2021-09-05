import os
import sys
import time
import const
import socket
import random
import threading
from _thread import start_new_thread
import packages.go_back_N as go_back_N
import packages.stop_and_wait as stop_and_wait
import packages.selective_repeat as selective_repeat


class Channel:

    def __init__(self, sender_to_channel: list, channel_to_sender: list, receiver_to_channel: list, channel_to_receiver: list):
        self.sender_to_channel = sender_to_channel
        self.channel_to_sender = channel_to_sender
        self.receiver_to_channel = receiver_to_channel
        self.channel_to_receiver = channel_to_receiver


    def inject_biterror(self, packet: str) -> str:
        pkt_len = len(packet)
        digit_list = list(packet)
        index = random.randint(0, pkt_len-1)
        if digit_list[index] == '1': digit_list[index] = '0'
        elif digit_list[index] == '0': digit_list[index] = '1'
        return ("".join(digit_list))


    def send_packet_to_receiver(self, sender: int):
        time.sleep(0.5)
        while True:
            packet = self.sender_to_channel[sender].recv()              # data-packet
            receiver = packet.decodeDestAddress()
            if random.random() <= const.drop_out_prob:
                print("CHANNEL : Packet has been discarded")
            else:
                if random.random() <= const.err_inject_prob:
                    print("CHANNEL : Injecting BIT-Error in Packet")
                    self.inject_biterror(packet)

                if random.random() <= const.delay_prob: 
                    print("CHANNEL : Introducing delay in Packet")                        
                    time.sleep(const.delay)
                    
                self.channel_to_receiver[receiver].send(packet)
                print("CHANNEL : Packet has been sent")


    def send_ack_to_sender(self, receiver: int):
        time.sleep(0.5)
        while True:
            ackmnt = self.receiverToChannel[receiver].recv()            # acknowledgement
            sender = ackmnt.decodeDestAddress()
            if random.random() <= const.drop_out_prob:
                print("CHANNEL : Packet has been dropped out")
            else:
                if random.random() <= const.err_inject_prob:
                    print("CHANNEL : Injecting BIT-Error in Acknowledgement")
                    self.inject_biterror(ackmnt)

                if random.random() <= const.delay_prob: 
                    print("CHANNEL : Introducing delay in Acknowledgement")                        
                    time.sleep(const.delay)
    
                self.channel_to_sender[sender].send(ackmnt)
                print("CHANNEL : Acknowledgement has been sent")


    def initiate_channel_process(self):
        sender_to_receiver_pkt_threadlist = []
        receiver_to_sender_ack_thread_list = []
        sender = 0
        receiver = 0
        print("\nCHANNEL is running")
        for _ in range(const.total_sender_number):
            pkt_thrd = threading.Thread(name= 'PacketThread-' + str(sender+1), target=self.send_packet_to_receiver, args=(sender,))
            sender_to_receiver_pkt_threadlist.append(pkt_thrd)
            sender += 1
            
        for _ in range(const.totalReceiverNumber):
            ackn_thrd = threading.Thread(name= 'AckmntThread-' + str(receiver+1), target=self.send_ack_to_sender, args=(receiver,))
            receiver_to_sender_ack_thread_list.append(ackn_thrd)
            receiver += 1

        for thread in sender_to_receiver_pkt_threadlist:
            thread.start()
            
        for thread in receiver_to_sender_ack_thread_list:
            thread.start()

        for thread in sender_to_receiver_pkt_threadlist:
            thread.join()
            
        for thread in receiver_to_sender_ack_thread_list:
            thread.join()
