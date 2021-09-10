import os
import sys
import time
import socket
import random
import threading
import packages.const as const
from template import *
from _thread import start_new_thread
import packages.go_back_N as go_back_N
import packages.stop_and_wait as stop_and_wait
import packages.selective_repeat as selective_repeat


class Channel:

    def __init__(self) -> None:
        self.port = 65432
        self.host = '127.0.0.1'
        self.thread_count = 0
        self.channel_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channel_side_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.channel_side_socket.bind((self.host, self.port))
            self.channel_side_socket.listen(5)
            print("\nSocket has been created.\nChannel is waiting for client(s) to connect....")
        except Exception as ex:
            print("\n[ERROR 1] Error Description : " + str(sys.exc_info()))
            print("[EXCEPTION 1] Exception : " + str(ex))
            self.channel_side_socket.close()
            print("\nReceiver has been terminated. Socket has been closed.")
            sys.exit(1)


    def inject_biterror(self, packet: str) -> str:
        pkt_len = len(packet)
        digit_list = list(packet)
        index = random.randint(0, pkt_len-1)
        if digit_list[index] == '1': digit_list[index] = '0'
        elif digit_list[index] == '0': digit_list[index] = '1'
        return ("".join(digit_list))


    def send_packet_to_receiver(self, sender_conn: socket.socket):
        time.sleep(0.5)
        while True:
            pkt = sender_conn.recv(1024).decode('utf-8')             # data-packet
            receiver_conn, addr = sender_conn.accept()
            if random.random() <= const.drop_out_prob:
                print("CHANNEL : Packet has been discarded")
            else:
                if random.random() <= const.err_inject_prob:
                    print("CHANNEL : Injecting BIT-Error in Packet")
                    self.inject_biterror(pkt)

                if random.random() <= const.delay_prob: 
                    print("CHANNEL : Introducing delay in Packet")                        
                    time.sleep(const.delay)
                    
                receiver_conn.send(pkt)
                print("CHANNEL : Packet has been sent")


    def send_ack_to_sender(self, receiver_conn: socket.socket):
        time.sleep(0.5)
        while True:
            ack = receiver_conn.recv(1024).decode('utf-8')            # acknowledgement
            sender_conn, addr = receiver_conn.accept()
            if random.random() <= const.drop_out_prob:
                print("CHANNEL : Packet has been dropped out")
            else:
                if random.random() <= const.err_inject_prob:
                    print("CHANNEL : Injecting BIT-Error in Acknowledgement")
                    self.inject_biterror(ack)

                if random.random() <= const.delay_prob: 
                    print("CHANNEL : Introducing delay in Acknowledgement")                        
                    time.sleep(const.delay)
    
                sender_conn.send(ack)
                print("CHANNEL : Acknowledgement has been sent")


    def initiate_channel_process(self):
        sender_to_receiver_pkt_threadlist = []
        receiver_to_sender_ack_thread_list = []
        sndr_thrd_cnt = 0
        recvr_thrd_cnt = 0
        print("\nCHANNEL is running")
        while sndr_thrd_cnt <= const.total_sender_number:
            conn, addr = self.channel_side_socket.accept()
            ip, port = str(addr[0]), str(addr[1])
            with open("textfiles/sndr_addr.txt", 'a') as sndr_addr: sndr_addr.write(str(addr) + "\n")
            print("\nConnected to sender via address : " + ip + ':' + port)
            pkt_thrd = threading.Thread(name= 'PacketThread-' + str(sndr_thrd_cnt+1), target=self.send_packet_to_receiver, args=(conn,))
            sender_to_receiver_pkt_threadlist.append(pkt_thrd)
            sndr_thrd_cnt += 1
            print("Thread number = Sender number = " + str(sndr_thrd_cnt))
            
        while recvr_thrd_cnt <= const.total_receiver_number:
            conn, addr = self.channel_side_socket.accept()
            ip, port = str(addr[0]), str(addr[1])
            with open("textfiles/recv_addr.txt", 'a') as recv_addr: recv_addr.write(str(addr) + "\n")
            print("\nConnected to receiver via address : " + ip + ':' + port)
            ackn_thrd = threading.Thread(name= 'AckmntThread-' + str(recvr_thrd_cnt+1), target=self.send_ack_to_sender, args=(conn,))
            receiver_to_sender_ack_thread_list.append(ackn_thrd)
            recvr_thrd_cnt += 1
            print("Thread number = Receiver number = " + str(recvr_thrd_cnt))

        for thread in sender_to_receiver_pkt_threadlist:
            thread.start()
            
        for thread in receiver_to_sender_ack_thread_list:
            thread.start()

        for thread in sender_to_receiver_pkt_threadlist:
            thread.join()
            
        for thread in receiver_to_sender_ack_thread_list:
            thread.join()


if __name__ == "__main__":
    chnl = Channel()
    chnl.initiate_channel_process()
