import os
import sys
import const
import socket
import random
import threading
from template import *
from _thread import start_new_thread
import packages.go_back_N as go_back_N
import packages.stop_and_wait as stop_and_wait
import packages.selective_repeat as selective_repeat


class Receiver:

    def __init__(self) -> None:
        self.max = 0
        self.host = '127.0.0.1'
        self.port = 65432                                # arbitrary non-privileged port
        self.recv_thread_count = 0
        self.receiver_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver_side_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.receiver_side_socket.bind((self.host, self.port))
            self.max = int(input("\nEnter max number of receivers : "))
            self.receiver_side_socket.listen(5)
            print("\nSocket has been created.\nReceivers are listening.\nWaiting for sender(s) to connect....")

        except Exception as ex:
            print("\n[ERROR 1] Error Description : " + str(sys.exc_info()))
            print("[EXCEPTION 1] Exception : " + str(ex))
            self.receiver_side_socket.close()
            print("\nReceiver has been terminated. Socket has been closed.")
            sys.exit(1)

        self.recv_thread_count += 1

    def recv_pkt():
        pass

    def send_ack():
        pass


if __name__ == "__main__":
    recvr = Receiver()
