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


class Receiver:

    def __init__(self) -> None:
        self.port = 65432
        self.host = '127.0.0.1'
        self.recv_thread_count = 0
        self.MAX = const.total_receiver_number

    def gen_ack(self, pkt: str) -> str:
        return "ack-" + pkt

    def recv_pkt(self, conn: socket.socket):
        pkt = conn.recv(1024).decode("utf-8")
        return pkt

    def send_ack(self, ack: str, conn: socket.socket):
        ack = conn.sendall(ack)

    def initiate_receiver_process(self):
        self.receiver_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver_side_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try: self.receiver_side_socket.connect((self.host, self.port))
        except socket.error as se:
            print("\nChannel is currently inactive. Connection failed!\n\n[Error 1] : " + str(sys.exc_info()))
            print("\n[EXCEPTION 1] SOCK_ERR Caught : " + str(se) + "\nConnection has been closed")
            self.receiver_side_socket.close()
            sys.exit(1)

        print("\nChannel is currently active.\Waiting for sender to send request.")

        self.sndr_req = self.receiver_side_socket.recv(2048)
        recvd_pkt, choice = [str(i) for i in self.sndr_req.decode("utf-8").split("\n")]

        if choice == '1':
            ack_to_be_sent = self.gen_ack(recvd_pkt)
            self.receiver_side_socket.sendall(ack_to_be_sent)


        elif choice == '2':
            ack_to_be_sent = self.gen_ack(recvd_pkt)
            self.receiver_side_socket.sendall(ack_to_be_sent)

        elif choice == '3':
            ack_to_be_sent = self.gen_ack(recvd_pkt)
            self.receiver_side_socket.sendall(ack_to_be_sent)


if __name__ == "__main__":
    recvr = Receiver()
    recvr.initiate_receiver_process()
