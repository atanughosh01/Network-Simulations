import sys
import socket
import random
import threading
from _thread import start_new_thread
import packages.go_back_N as go_back_N
import packages.stop_and_wait as stop_and_wait
import packages.selective_repeat as selective_repeat


class Receiver:

    def __init__(self) -> None:
        self.host = '127.0.0.1'
        self.port = 65432                                # arbitrary non-privileged port
        self.thread_count = 0
        self.channel_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channel_side_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def recv_pkt():
        pass

    def send_ack():
        pass


recvr = Receiver()
