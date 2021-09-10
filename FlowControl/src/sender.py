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


class Sender:

    def __init__(self) -> None:
        self.port = 65432                                # arbitrary non-privileged port
        self.host = '127.0.0.1'
        self.sndr_thread_count = 0
        self.MAX = const.total_sender_number
        self.input_filename = "textfiles/input.txt"
        self.sender_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sender_side_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.sender_side_socket.bind((self.host, self.port))
            self.sender_side_socket.listen(5)
            print("\nSocket has been created.\nReceivers are listening.\nWaiting for sender(s) to connect....")

        except Exception as ex:
            print("\n[ERROR 1] Error Description : " + str(sys.exc_info()))
            print("[EXCEPTION 1] Exception : " + str(ex))
            self.sender_side_socket.close()
            print("\nReceiver has been terminated. Socket has been closed.")
            sys.exit(1)

    def gen_pkt(self) -> list[str]:
        self.data = read_file(self.input_filename)
        self.packet_list = create_pkt(self.data)
        return self.packet_list

    def send_pkt(self, connection: socket.socket):
        connection.sendall(packet)

    def recv_ack():
        pass

    def timeout():
        pass


if __name__ == "__main__":
    sndr = Sender()
    print(sndr.gen_pkt())